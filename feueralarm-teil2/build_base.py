"""Baut die Grund-Szenen einmal und speichert sie als .blend (schnelles Laden je Einstellung).

  EGL_PLATFORM=surfaceless bl/bin/python build_base.py klasse|flur|keller <ausgabe.blend>

Unbewegtes (Raum, Mitschüler) wird zu einer Mesh verschmolzen, Hauptfiguren je Gelenk.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402

import cast as C  # noqa: E402
import set_flur as F  # noqa: E402
import set_hof as HOF  # noqa: E402
import set_klasse as K  # noqa: E402
import toon as T  # noqa: E402

RIG_KEYS = ("root", "becken", "torso", "hals", "kopf", "mund", "schulter_l", "schulter_r", "ellbogen_l", "ellbogen_r",
            "hand_l", "hand_r", "huefte_l", "huefte_r", "knie_l", "knie_r")


def rig_names(R):
    out = {k: R[k].name for k in RIG_KEYS if k in R}
    out["augen"] = [o.name for o in R["augen"]]
    out["pupillen"] = [o.name for o in R["pupillen"]]
    out["brauen"] = [o.name for o in R["brauen"]]
    return out


def kids_klasse():
    T.QUALITY = 0.5
    k = 0
    for cx in K.COLS:
        for ry in K.ROWS:
            for sx in (-1, 1):
                x = cx + sx * K.SEAT_DX
                taken = [(K.NOAH, 0), (K.BEN, 0), (K.LINA, 0)] + [(f, 0) for f in K.FREI]
                if any(abs(x - p[0]) < 0.01 and abs(ry - p[1]) < 0.01 for p, _ in taken):
                    continue
                k += 1
                R = C.baue(f"kid{k}", f"kid{k}", pose="sitzen", loc=(x, ry, 0), rot=180, detail=False, line=0.006)
                # etwas Leben: Köpfe leicht unterschiedlich gedreht
                R["kopf"].rotation_euler[2] = math.radians(-25 + 50 * ((k * 37) % 11) / 10)
                R["kopf"].rotation_euler[0] = math.radians(-6 + 12 * ((k * 53) % 7) / 6)
    T.QUALITY = 1.0


def _auto_getrennt(baue):
    """Set bauen; das blaue Auto bleibt beweglich (eigene Wurzel), Glas einzeln (für Innenansichten ausblendbar)."""
    vorher = set(bpy.data.objects)
    res = baue()
    root = bpy.data.objects["blaues_auto"]
    glas = [o for o in root.children_recursive if "_glas_" in o.name]
    halter = [o for o in root.children_recursive if o.name.endswith("_handyhalter")]
    for g in glas:  # Glas eigenständig, aber am Auto
        mw = g.matrix_world.copy()
        g.parent = root
        g.matrix_world = mw
    schilder = [o for o in root.children_recursive if "_kennzeichen_" in o.name]   # UV-Flächen nicht verbinden
    keep = set(glas) | set(halter) | set(halter[0].children_recursive if halter else []) | set(schilder)
    for o in list(root.children):
        if o not in keep and o.type == "EMPTY":
            T.merge_children(o, recursive=True)
    T.merge_children(root, recursive=False, keep=list(keep))
    statisch = [o for o in bpy.data.objects if o not in vorher or True]
    # alles außer Auto zu einer Mesh
    for o in [o for o in bpy.context.scene.objects if o.type == "MESH" and o.parent is not None
              and o.parent != root and root not in getattr(o.parent, "children_recursive", []) and not _unter(o, root)]:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    T.merge_children(None, name="set_statisch")
    return res


def _unter(o, root):
    p = o.parent
    while p is not None:
        if p == root:
            return True
        p = p.parent
    return False


def main():
    which, out = sys.argv[-2], sys.argv[-1]
    T.reset()
    T.setup(res=(720, 1280), aa="FXAA")
    rigs = {}
    if which == "klasse":
        K.build(outside=True)
        kids_klasse()
        T.flatten_static()
        for nm, key, pose in (("Ben", "ben", "sitzen"), ("Lina", "lina", "sitzen"), ("Sander", "sander", "stehen")):
            R = C.baue(nm, key, pose=pose)
            T.merge_rig(R)
            rigs[nm] = rig_names(R)
    elif which == "flur":
        F.flur()
        T.flatten_static()
        for nm, key in (("Ben", "ben"), ("Sander", "sander")):
            R = C.baue(nm, key)
            T.merge_rig(R)
            rigs[nm] = rig_names(R)
    elif which == "keller":
        F.keller()
        T.flatten_static()
        for nm, key in (("Ben", "ben"), ("Pohl", "pohl")):
            R = C.baue(nm, key)
            T.merge_rig(R)
            rigs[nm] = rig_names(R)
    elif which == "hof":
        _auto_getrennt(HOF.hof)
        for nm, key, pose in (("Ben", "ben", "stehen"), ("Fahrer", "fahrer", "stehen"), ("Sander", "sander", "stehen")):
            R = C.baue(nm, key, pose=pose)
            T.merge_rig(R)
            rigs[nm] = rig_names(R)
    elif which == "auto":
        HOF.strasse()
        T.flatten_static()
        _auto_getrennt(lambda: HOF.auto("blaues_auto", loc=(HOF.SPUR_X, 0, 0), rot=0, innen=True, glas=True))
        for nm, key, pose in (("Ben", "ben", "sitzen"), ("Fahrer", "fahrer", "sitzen")):
            R = C.baue(nm, key, pose=pose)
            T.merge_rig(R)
            rigs[nm] = rig_names(R)
    cam = T.camera(lens=15)
    H = C.pov_haende(cam)
    for k, v in list(H.items()):
        if hasattr(v, "name"):
            H[k] = v.name
    rigs["_pov"] = {k: v for k, v in H.items() if isinstance(v, str)}
    hand_rig = bpy.data.objects["pov_rig"]
    T.merge_children(bpy.data.objects["pov_hand_r"], recursive=True)
    hand_rig.hide_render = False
    # versteckte (zusammengeführte) Originale endgültig entfernen, Datei klein halten
    for o in [o for o in bpy.data.objects if o.hide_render and o.type == "MESH"]:
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.outliner.orphans_purge(do_recursive=True) if hasattr(bpy.ops.outliner, "orphans_purge") else None
    json.dump(rigs, open(out.replace(".blend", ".json"), "w"), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print("gespeichert", out, len(bpy.data.objects), "Objekte")


if __name__ == "__main__":
    main()

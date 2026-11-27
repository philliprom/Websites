"""Eine Einstellung rendern.

  EGL_PLATFORM=surfaceless bl/bin/python render_shot.py <shot-id|alle|liste> <base-ordner> <frames-ordner> [test]

test: nur 3 Bilder (Anfang, Mitte, Ende) in halber Auflösung -> <frames-ordner>/test_<shot>_*.png
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from mathutils import Vector  # noqa: E402

import anim as AN  # noqa: E402
import shots as SH  # noqa: E402
import toon as T  # noqa: E402

FPS = AN.FPS
TL = json.load(open(os.path.join(HERE, "timeline.json")))
LINE = {l["id"]: l for l in TL["lines"]}
SETLOOK = {
    "klasse": dict(bg="#bcd9ee", light=(-0.75, -0.25, 0.62), shadow=0.32),
    "flur": dict(bg="#d8d4cc", light=(0.35, -0.2, 0.9), shadow=0.3),
    "keller": dict(bg="#151515", light=(0.1, 0.25, 0.95), shadow=0.42),
}


class Times:
    def S(self, i):
        return LINE[i]["start"]

    def E(self, i):
        return LINE[i]["end"]


def shot_times():
    tm = Times()
    starts = [max(0.0, s["start"](tm)) for s in SH.SHOTS]
    out = []
    for k, s in enumerate(SH.SHOTS):
        t1 = starts[k + 1] if k + 1 < len(starts) else TL["total"]
        out.append((s, starts[k], t1))
    return out


class Ctx(Times):
    def __init__(self, shot, t0, t1, allt):
        self.id = shot["id"]
        self.set = shot["set"]
        self.t0, self.t1 = t0, t1
        self._all = {s["id"]: (a, b) for s, a, b in allt}
        self.a = {}
        self.pov = None
        self.phone_plan = None
        self.list_prop = False
        self.phone_prop = None
        self._env = {}

    def shot_start(self, sid):
        return self._all[sid][0]

    def env(self, i):
        if i not in self._env:
            w, sr = sf.read(os.path.join(HERE, "tts_cache", "trim", f"{i}.wav"), dtype="float32")
            self._env[i] = AN.envelope(w, sr)
        return self._env[i]

    def phone(self, state, raise_at=None, lower_at=None, low=False):
        self.phone_plan = dict(state=state, raise_at=raise_at, lower_at=lower_at, low=low)


def hand_offset(plan, t, t0):
    """y-Versatz des Hand-Rigs (0 = Handy im Bild, -0.6 = weg)."""
    hidden, shown = -0.6, (-0.07 if plan and plan.get("low") else 0.0)
    if plan is None:
        return hidden
    st = plan["state"]
    ra, lo = plan["raise_at"], plan["lower_at"]
    if st is None and lo is None:
        return hidden
    v = shown
    if ra is not None:
        v = hidden + (shown - hidden) * AN.smooth(ra, ra + 0.35, t)
    if lo is not None:
        v = v + (hidden - v) * AN.smooth(lo, lo + 0.35, t)
    return v


def run(shot, t0, t1, allt, base_dir, out_dir, test=False, only=None, out_path=None):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(base_dir, f'{shot["set"]}.blend'))
    names = json.load(open(os.path.join(base_dir, f'{shot["set"]}.json')))
    sc = bpy.context.scene
    look = SETLOOK[shot["set"]]
    T.setup(res=(720, 1280), aa="FXAA", bg=look["bg"], shadow=look["shadow"], light=look["light"])
    if test and only is None:
        sc.render.resolution_percentage = 50
    if only is not None:
        sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
        sc.display.render_aa = "8"
    c = Ctx(shot, t0, t1, allt)
    seeds = {"Ben": 3, "Lina": 7, "Sander": 11, "Pohl": 5}
    for nm, rn in names.items():
        if nm.startswith("_"):
            continue
        seated = shot["set"] == "klasse" and nm in ("Ben", "Lina")
        c.a[nm] = AN.Actor(rn, seated=seated, seed=seeds.get(nm, 1))
    cam = sc.camera
    c.pov = AN.POV(cam, seed=hash(shot["id"]) % 97)
    shot["fn"](c)
    # Requisiten
    if c.list_prop and "Sander" in c.a:
        hand = c.a["Sander"].o["hand_l"]
        T.box("liste_blatt", (0.21, 0.30, 0.004), T.mat("Papier", "#fbfbf6"), loc=(0.06, -0.12, -0.08), parent=hand,
              line=0.003)
    if c.phone_prop and c.phone_prop in c.a:
        hand = c.a[c.phone_prop].o["hand_r"]
        o = T.box("fremdes_handy", (0.07, 0.012, 0.145), T.mat("HandySchwarz", "#151518"), loc=(0.0, -0.04, -0.07),
                  parent=hand, line=0.003, bevel=0.006)
        o.rotation_euler[2] = math.radians(15)
    # Handy-Bildschirm
    plan = c.phone_plan
    if plan and plan["state"]:
        img = bpy.data.images.load(os.path.join(HERE, "assets", f'handy_{plan["state"]}.png'), check_existing=True)
        m = bpy.data.materials.get("Handy_bild")
        nt = m.node_tree
        tn = next((n for n in nt.nodes if n.type == "TEX_IMAGE"), None)
        if tn is None:
            tn = nt.nodes.new("ShaderNodeTexImage")
            bsdf = nt.nodes.get("Principled BSDF")
            if bsdf:
                nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
        tn.image = img
        nt.nodes.active = tn
    rig = bpy.data.objects["pov_rig"]
    unused = [a for a in c.a.values() if a.base_pos is None]
    for a in unused:
        a.o["root"].location = (0, -80, -40)
    f0 = int(round(t0 * FPS)) + 1
    f1 = max(f0, int(round(t1 * FPS)))
    frames = list(range(f0, f1 + 1))
    if test:
        frames = sorted(set([f0, (f0 + f1) // 2, f1]))
    if only is not None:
        frames = [int(round(only * FPS)) + 1]
    for f in frames:
        t = (f - 1) / FPS
        c.pov.pose_at(t)
        c.pov.keys(f)
        cp = cam.location.copy()
        for a in c.a.values():
            if a.base_pos is not None:
                a.pose_at(t, cp)
                a.keys(f)
        rig.location = (0, hand_offset(plan, t, t0), 0)
        rig.keyframe_insert("location", frame=f)
    for a in unused:
        a.o["root"].keyframe_insert("location", frame=f0)
    os.makedirs(out_dir, exist_ok=True)
    if test:
        sc.render.image_settings.file_format = "PNG"
    else:  # JPEG 95 spart Platz (4000 Bilder), Qualität reicht für TikTok locker
        sc.render.image_settings.file_format = "JPEG"
        sc.render.image_settings.quality = 95
    sc.render.image_settings.color_mode = "RGB"
    t_start = time.time()
    if test:
        for f in frames:
            sc.frame_set(f)
            if os.environ.get("FA_DEBUG"):
                print("DEBUG", f, "lens", round(cam.data.lens, 1), "cam", tuple(round(v, 2) for v in cam.location),
                      "anim", cam.data.animation_data is not None, flush=True)
            sc.render.filepath = out_path or os.path.join(out_dir, f'test_{shot["id"]}_{f:05d}.png')
            bpy.ops.render.render(write_still=True)
    else:
        sc.frame_start, sc.frame_end = f0, f1
        sc.render.filepath = os.path.join(out_dir, "f_#####")
        bpy.ops.render.render(animation=True)
    print(f'{shot["id"]}: {len(frames)} Bilder ({t0:.2f}-{t1:.2f}s) in {time.time() - t_start:.0f}s', flush=True)


def still(shot_id, t, base_dir, path):
    """Einzelbild in voller Auflösung (1080x1920, 8-fach geglättet) für das Titelbild."""
    allt = shot_times()
    for s, a, b in allt:
        if s["id"] == shot_id:
            run(s, a, b, allt, base_dir, os.path.dirname(path), test=True, only=t, out_path=path)


def main():
    if sys.argv[-4] == "standbild":
        shot_id, t, path = sys.argv[-3].split(":")[0], float(sys.argv[-3].split(":")[1]), sys.argv[-1]
        still(shot_id, t, sys.argv[-2], path)
        return
    which, base_dir, out_dir = sys.argv[-4:-1] if sys.argv[-1] == "test" else sys.argv[-3:]
    test = sys.argv[-1] == "test"
    allt = shot_times()
    if which == "liste":
        os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
        json.dump([dict(id=s["id"], set=s["set"], t0=round(a, 3), t1=round(b, 3)) for s, a, b in allt],
                  open(os.path.join(HERE, "build", "shots.json"), "w"), indent=1)
        for s, a, b in allt:
            print(f'{s["id"]:24} {s["set"]:7} {a:7.2f} {b:7.2f} {b - a:5.2f}s')
        return
    ids = [s["id"] for s, _, _ in allt] if which == "alle" else which.split(",")
    for s, a, b in allt:
        if s["id"] in ids:
            run(s, a, b, allt, base_dir, out_dir, test)


if __name__ == "__main__":
    main()

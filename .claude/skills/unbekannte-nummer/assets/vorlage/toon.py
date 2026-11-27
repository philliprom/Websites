"""Toon-Baukasten für Blender (bpy, Workbench-Render): Materialien, Formen, Konturen, Figuren.

Look wie bei animierten POV-Dramen: kräftige Flächenfarben, weiches Zwei-Ton-Shading (eigene Matcap),
schwarze Konturen (umgedrehte Hülle per Geometry Nodes), harte Schlagschatten.
Workbench rendert ohne Grafikkarte über Mesa/EGL (EGL_PLATFORM=surfaceless).
"""
import math
import os

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
QUALITY = 1.0  # < 1: weniger Polygone (Hintergrundfiguren)


def _q(n, lo):
    return max(lo, int(round(n * QUALITY)))


# ---------------------------------------------------------------- Szene
def reset():
    global _BLACK
    _BLACK = None
    bpy.ops.wm.read_factory_settings(use_empty=True)


def setup(res=(1080, 1920), aa="8", matcap=None, shadow=0.38, light=(-0.55, -0.45, 0.70), bg=(0.6, 0.7, 0.8),
          cavity=False):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.fps = 30
    sc.display.render_aa = aa
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sh = sc.display.shading
    sh.light = "MATCAP"
    path = matcap or os.path.join(HERE, "assets", "toon_matcap.png")
    sl = bpy.context.preferences.studio_lights.load(path, "MATCAP")
    sh.studio_light = sl.name
    sh.color_type = "TEXTURE"
    sh.show_shadows = shadow > 0
    sh.shadow_intensity = shadow
    sc.display.light_direction = light
    sc.display.shadow_shift = 0.05
    sc.display.shadow_focus = 0.9
    sh.show_backface_culling = True  # nötig für die Kontur-Hülle (Rückseiten weg)
    sh.show_object_outline = False
    sh.show_cavity = cavity
    if cavity:
        sh.cavity_type = "WORLD"
        sh.cavity_ridge_factor = 0.0
        sh.cavity_valley_factor = 0.6
    sh.show_specular_highlight = False
    if sc.world is None:
        sc.world = bpy.data.worlds.new("Welt")
    sc.world.color = srgb(bg)
    return sc


def srgb(c):
    """sRGB (0..1 oder Hex) -> linear."""
    if isinstance(c, str):
        c = c.lstrip("#")
        c = tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def f(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return tuple(f(v) for v in c[:3])


# ---------------------------------------------------------------- Materialien
_BLACK = None


def mat(name, color, tex=None, cull=False):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    lin = srgb(color)
    m.diffuse_color = (*lin, 1.0)
    m.use_backface_culling = cull
    m.roughness = 1.0
    m.metallic = 0.0
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*lin, 1)
    if tex:
        img = bpy.data.images.load(tex, check_existing=True)
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = img
        tn.interpolation = "Linear"
        tn.extension = "CLIP"
        if bsdf:
            nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
        nt.nodes.active = tn
    return m


def black():
    global _BLACK
    try:
        if _BLACK is not None and _BLACK.name in bpy.data.materials:
            return _BLACK
    except ReferenceError:  # Datei wurde neu geladen
        pass
    _BLACK = bpy.data.materials.get("Kontur") or mat("Kontur", (0.02, 0.02, 0.025), cull=True)
    return _BLACK


# ---------------------------------------------------------------- Kontur (umgedrehte Hülle)
def outline_group():
    ng = bpy.data.node_groups.get("Kontur")
    if ng:
        return ng
    ng = bpy.data.node_groups.new("Kontur", "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    w = ng.interface.new_socket("Breite", in_out="INPUT", socket_type="NodeSocketFloat")
    w.default_value = 0.01
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    N = ng.nodes
    gi = N.new("NodeGroupInput")
    go = N.new("NodeGroupOutput")
    nrm = N.new("GeometryNodeInputNormal")
    sc = N.new("ShaderNodeVectorMath")
    sc.operation = "SCALE"
    sp = N.new("GeometryNodeSetPosition")
    fl = N.new("GeometryNodeFlipFaces")
    sm = N.new("GeometryNodeSetMaterial")
    sm.inputs["Material"].default_value = black()
    j = N.new("GeometryNodeJoinGeometry")
    L = ng.links
    L.new(nrm.outputs["Normal"], sc.inputs[0])
    L.new(gi.outputs["Breite"], sc.inputs["Scale"])
    L.new(gi.outputs["Geometry"], sp.inputs["Geometry"])
    L.new(sc.outputs["Vector"], sp.inputs["Offset"])
    L.new(sp.outputs["Geometry"], fl.inputs["Mesh"])
    L.new(fl.outputs["Mesh"], sm.inputs["Geometry"])
    L.new(gi.outputs["Geometry"], j.inputs["Geometry"])
    L.new(sm.outputs["Geometry"], j.inputs["Geometry"])
    L.new(j.outputs["Geometry"], go.inputs["Geometry"])
    return ng


def outline(obj, width=0.01):
    if width <= 0:
        return obj
    md = obj.modifiers.new("Kontur", "NODES")
    md.node_group = outline_group()
    key = [s.identifier for s in md.node_group.interface.items_tree
           if getattr(s, "in_out", "") == "INPUT" and s.name == "Breite"][0]
    try:
        getattr(md.properties.inputs, key).value = width  # Blender 5.x
    except AttributeError:
        md[key] = width  # Blender 4.x
    if black().name not in [m.name for m in obj.data.materials if m]:
        obj.data.materials.append(black())
    return obj


# ---------------------------------------------------------------- Formen
def _obj(name, bm, material, parent=None, smooth=True, line=0.01, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if material is not None:
        me.materials.append(material)
    if parent is not None:
        ob.parent = parent
    ob.location = loc
    outline(ob, line)
    return ob


def ellipsoid(name, size, material, loc=(0, 0, 0), parent=None, line=0.01, segs=32, rings=16, rot=None, cut=None):
    """Ellipsoid mit Durchmessern size=(x,y,z). cut(v)->True entfernt Punkte (z. B. Haarkappe)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=_q(segs, 8), v_segments=_q(rings, 6), radius=0.5)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if rot:
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(rot[1]), 3, rot[0]))
    if cut:
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if cut(v.co)], context="VERTS")
    return _obj(name, bm, material, parent, True, line, loc)


def cap(name, size, material, theta_max, loc=(0, 0, 0), parent=None, line=0.01, segs=48, rings=14):
    """Haarkappe: Ellipsoid-Ausschnitt von oben bis zum Haaransatz theta_max(phi) (Grad ab Scheitel), glatte Kante.
    phi: 0 = +X (links der Figur), -90 = vorn (-Y), 90 = hinten."""
    bm = bmesh.new()
    segs, rings = _q(segs, 12), _q(rings, 5)
    sx, sy, sz = (v / 2 for v in size)
    top = bm.verts.new((0, 0, sz))
    grid = []
    for i in range(segs):
        phi = 2 * math.pi * i / segs
        tm = math.radians(theta_max(math.degrees(phi) if math.degrees(phi) <= 180 else math.degrees(phi) - 360))
        col = []
        for j in range(1, rings + 1):
            th = tm * j / rings
            col.append(bm.verts.new((sx * math.sin(th) * math.cos(phi), sy * math.sin(th) * math.sin(phi),
                                     sz * math.cos(th))))
        grid.append(col)
    for i in range(segs):
        a, b = grid[i], grid[(i + 1) % segs]
        bm.faces.new((top, a[0], b[0]))
        for j in range(rings - 1):
            bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _obj(name, bm, material, parent, True, line, loc)


def box(name, size, material, loc=(0, 0, 0), parent=None, line=0.01, bevel=0.0, smooth=False):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=3, profile=0.5, affect="EDGES")
    return _obj(name, bm, material, parent, smooth or bevel > 0, line, loc)


def cylinder(name, r, h, material, loc=(0, 0, 0), parent=None, line=0.01, segs=24, axis="Z", r2=None, caps=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=_q(segs, 6), radius1=r, radius2=r if r2 is None else r2,
                          depth=h)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    ob = _obj(name, bm, material, parent, True, line, loc)
    # Deckel flach schattieren, Mantel weich
    me = ob.data
    for p in me.polygons:
        n = p.normal
        p.use_smooth = not (abs(n.z if axis == "Z" else (n.x if axis == "X" else n.y)) > 0.99)
    return ob


def capsule(name, r, length, material, loc=(0, 0, 0), parent=None, line=0.01, axis="Z", segs=20, r2=None):
    """Kapsel entlang -axis ab Ursprung (Gelenk am Ursprung, Glied hängt nach unten bzw. -axis)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=_q(segs, 8), v_segments=_q(12, 6), radius=1.0)
    rb = r if r2 is None else r2
    for v in bm.verts:
        z = v.co.z
        if z >= 0:
            v.co = Vector((v.co.x * r, v.co.y * r, z * r))
        else:
            v.co = Vector((v.co.x * rb, v.co.y * rb, z * rb - length))
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    return _obj(name, bm, material, parent, True, line, loc)


def torus(name, R, r, material, loc=(0, 0, 0), parent=None, line=0.0, segs=32, rsegs=10, axis="Y"):
    """Ring (Brillengestell, Schlüsselring). Achse = Blickrichtung durch den Ring."""
    bm = bmesh.new()
    rings = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        c, s_ = math.cos(a), math.sin(a)
        ring = []
        for j in range(rsegs):
            b = 2 * math.pi * j / rsegs
            rr = R + r * math.cos(b)
            ring.append(bm.verts.new((rr * c, rr * s_, r * math.sin(b))))
        rings.append(ring)
    for i in range(segs):
        for j in range(rsegs):
            a1, a2 = rings[i], rings[(i + 1) % segs]
            bm.faces.new((a1[j], a2[j], a2[(j + 1) % rsegs], a1[(j + 1) % rsegs]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    elif axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    return _obj(name, bm, material, parent, True, line, loc)


def plane(name, size, material, loc=(0, 0, 0), rot=(90, 0, 0), parent=None, line=0.0):
    """Rechteck (Breite, Höhe), standardmäßig aufrecht, Vorderseite nach -Y (UV 0..1)."""
    bm = bmesh.new()
    w, h = size
    vs = [bm.verts.new((x, y, 0)) for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for loop, c in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        loop[uv].uv = c
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0),
                     matrix=Matrix.Rotation(math.radians(rot[0]), 3, "X"))
    if rot[2]:
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(rot[2]), 3, "Z"))
    return _obj(name, bm, material, parent, False, line, loc)


def empty(name, loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.parent = parent
    e.location = loc
    e.rotation_euler = [math.radians(a) for a in rot]
    e.empty_display_size = 0.05
    return e


def camera(name="Kamera", loc=(0, 0, 1.2), rot=(90, 0, 0), lens=16.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36
    cd.sensor_fit = "AUTO"
    cd.clip_start = 0.02
    cd.clip_end = 300
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = loc
    cam.rotation_euler = [math.radians(a) for a in rot]
    bpy.context.scene.camera = cam
    return cam


def look_at(obj, target, roll=0.0):
    bpy.context.view_layer.update()
    d = Vector(target) - obj.matrix_world.translation
    q = d.to_track_quat("-Z", "Y")
    obj.rotation_euler = q.to_euler()
    if roll:
        obj.rotation_euler.rotate_axis("Z", math.radians(roll))


# ---------------------------------------------------------------- Zusammenfassen (Tempo)
def merge_children(pivot, name=None, recursive=False, keep=()):
    """Alle Mesh-Kinder eines Drehpunkts (inkl. Kontur) zu EINEM Objekt verschmelzen (Blender: Umwandeln + Verbinden).
    pivot=None: alle Objekte ohne Elternteil (statisches Set). keep: Drehpunkte, deren Teile einzeln bleiben."""
    if pivot is None:
        # Flächen mit Texturkoordinaten (Tafel, Uhr, Schilder) einzeln lassen: beim Verbinden gingen ihre UVs verloren
        kids = [o for o in bpy.context.scene.objects if o.parent is None and o.type == "MESH" and o not in keep
                and not o.data.uv_layers]
    else:
        kids = [o for o in (pivot.children_recursive if recursive else pivot.children)
                if o.type == "MESH" and o not in keep and not any(k in keep for k in _ancestors(o, pivot))]
    if not kids:
        return None
    vl = bpy.context.view_layer
    vl.update()
    for o in vl.objects:
        if o is not None:
            o.select_set(False)
    for o in kids:
        o.select_set(True)
    vl.objects.active = kids[0]
    with bpy.context.temp_override(active_object=kids[0], object=kids[0], selected_objects=kids,
                                   selected_editable_objects=kids):
        bpy.ops.object.convert(target="MESH")
        if len(kids) > 1:
            bpy.ops.object.join()
    ob = vl.objects.active
    if pivot is not None and ob.parent != pivot:
        mw = ob.matrix_world.copy()
        ob.parent = pivot
        ob.matrix_world = mw
    if name:
        ob.name = name
    ob.select_set(False)
    return ob


def _ancestors(o, stop):
    out = []
    p = o.parent
    while p is not None and p != stop:
        out.append(p)
        p = p.parent
    return out


def merge_rig(R, animated=("kopf", "hals", "torso", "mund", "augen", "pupillen", "brauen", "schulter_l", "schulter_r",
                           "ellbogen_l", "ellbogen_r", "hand_l", "hand_r", "huefte_l", "huefte_r", "knie_l", "knie_r",
                           "becken"), frozen=False):
    """Figur zusammenfassen: frozen=True -> eine einzige Mesh (unbewegt); sonst je Drehpunkt eine Mesh."""
    if frozen:
        return merge_children(R["root"], recursive=True)
    pivots = set()
    for k in animated:
        v = R.get(k)
        if v is None:
            continue
        for p in (v if isinstance(v, list) else [v]):
            pivots.add(p)
    # Drehpunkte, die nicht animiert werden (z. B. Füße, Zopf), hängen am nächsten animierten Elternteil
    allp = [o for o in R["root"].children_recursive if o.type == "EMPTY"] + [R["root"]]
    for p in allp:
        if p in pivots or p == R["root"]:
            keep = [q for q in pivots if q != p]
            merge_children(p, recursive=True, keep=keep)


def flatten_static(name="set_statisch"):
    """Alle bisherigen Meshes (Raum, Möbel, eingefrorene Figuren) in Weltlage lösen und zu einer Mesh verschmelzen."""
    bpy.context.view_layer.update()
    for o in [o for o in bpy.context.scene.objects if o.type == "MESH" and o.parent is not None]:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
    ob = merge_children(None, name=name)
    for e in [o for o in bpy.context.scene.objects if o.type == "EMPTY" and not o.children]:
        bpy.data.objects.remove(e, do_unlink=True)
    bpy.context.view_layer.update()
    return ob

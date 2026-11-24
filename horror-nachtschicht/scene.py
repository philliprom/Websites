"""Horror-Test „Nachtschicht“: Überwachungskamera in einer Tankstelle bei Nacht. Draußen im Regen steht eine Gestalt am
Fenster. Das Licht flackert, geht kurz aus – und danach steht sie direkt an der Glastür.

Alles prozedural (keine fremden Modelle/Texturen), gerendert mit Blender/Cycles auf der CPU.
  <bl>/bin/python horror-nachtschicht/scene.py --still 20          # ein Standbild -> build/still_0020.png
  <bl>/bin/python horror-nachtschicht/scene.py --frames 1-75       # Bildfolge   -> build/frames/0001.png …
  <bl>/bin/python horror-nachtschicht/scene.py --save               # zusätzlich build/nachtschicht.blend speichern
Danach horror-nachtschicht/post.sh (Kamera-Look, Zeitstempel, Ton).
"""
import math
import os
import random
import sys

import bpy  # noqa: I001 (bpy zuerst, es macht addon_utils importierbar)
import addon_utils
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
FPS, N_FRAMES = 15, 75
BLACK = (47, 50)      # Licht aus (Bilder 47–50)
JUMP = 51             # ab hier steht die Gestalt an der Tür
RES = (450, 800)

addon_utils.enable("cycles", default_set=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
R = random.Random(7)
# Flackern soll hart schalten, nicht weich überblenden
bpy.context.preferences.edit.keyframe_new_interpolation_type = "CONSTANT"


# ---------------------------------------------------------------- Materialien
def mat(name, color=(0.8, 0.8, 0.8), rough=0.6, metal=0.0, emit=None, strength=0.0, alpha=1.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
    return m


def tiles_mat():
    """Bodenfliesen: Schachbrett aus zwei Grautönen, leicht glänzend."""
    m = bpy.data.materials.new("Fliesen")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    ch = nt.nodes.new("ShaderNodeTexChecker")
    ch.inputs["Scale"].default_value = 1.0
    ch.inputs["Color1"].default_value = (0.20, 0.20, 0.19, 1)
    ch.inputs["Color2"].default_value = (0.15, 0.15, 0.145, 1)
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.7, 1.7, 1.7)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], ch.inputs["Vector"])
    nt.links.new(ch.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.35
    return m


def asphalt_mat():
    """Nasser Asphalt: dunkel, Pfützen glänzen (Rauschmuster steuert die Rauheit)."""
    m = bpy.data.materials.new("Asphalt")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.025, 0.025, 0.028, 1)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.4
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.45
    cr.color_ramp.elements[0].color = (0.05, 0.05, 0.05, 1)
    cr.color_ramp.elements[1].position = 0.6
    cr.color_ramp.elements[1].color = (0.45, 0.45, 0.45, 1)
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Roughness"])
    return m


M = {
    "wall": mat("Wand", (0.30, 0.31, 0.28), 0.9),
    "ceil": mat("Decke", (0.22, 0.22, 0.21), 0.95),
    "floor": tiles_mat(),
    "frame": mat("Rahmen", (0.08, 0.08, 0.09), 0.4, 0.6),
    "glass": mat("Glas", (0.6, 0.65, 0.7), 0.02, alpha=0.05, spec=0.35),
    "counter": mat("Theke", (0.18, 0.2, 0.24), 0.5),
    "top": mat("Platte", (0.3, 0.3, 0.3), 0.35),
    "shelf": mat("Regal", (0.28, 0.29, 0.3), 0.45, 0.5),
    "asphalt": asphalt_mat(),
    "concrete": mat("Beton", (0.18, 0.18, 0.18), 0.9),
    "canopy": mat("Dach", (0.25, 0.26, 0.28), 0.6),
    "pump": mat("Zapfsäule", (0.55, 0.08, 0.08), 0.45),
    "cloth": mat("Stoff", (0.012, 0.012, 0.014), 0.95),
    "skin": mat("Haut", (0.62, 0.58, 0.54), 0.6, emit=(0.6, 0.58, 0.55), strength=0.03),
    "eye": mat("Augen", (0.0, 0.0, 0.0), 1.0),
    "rain": mat("Regen", (0.8, 0.85, 0.9), 0.2, emit=(0.7, 0.75, 0.8), strength=0.35, alpha=0.35),
}
# Leuchtröhren: Emission per Keyframes (Flackern)
TUBE = mat("Röhre", (1, 1, 1), 0.5, emit=(0.86, 0.93, 1.0), strength=9.0)
TUBE_FLICK = mat("Röhre flackernd", (1, 1, 1), 0.5, emit=(0.86, 0.93, 1.0), strength=9.0)
FRIDGE = mat("Kühlschrank Licht", (1, 1, 1), 0.5, emit=(0.75, 0.88, 1.0), strength=3.0)
CANOPY_L = mat("Dachlicht", (1, 1, 1), 0.5, emit=(1.0, 0.92, 0.8), strength=30.0)


def box(name, loc, size, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    o.data.materials.append(material)
    return o


def cyl(name, loc, r, h, material, rot=(0, 0, 0), verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o


def sphere(name, loc, r, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o


# ---------------------------------------------------------------- Laden (innen)
W0, W1, D0, D1, H = -4.0, 4.0, -4.0, 3.0, 3.0      # x von/bis, y hinten/vorn (Glasfront), Höhe
box("Boden", (0, (D0 + D1) / 2, -0.05), (W1 - W0, D1 - D0, 0.1), M["floor"])
box("Decke", (0, (D0 + D1) / 2, H + 0.05), (W1 - W0, D1 - D0, 0.1), M["ceil"])
box("Wand hinten", (0, D0 - 0.05, H / 2), (W1 - W0, 0.1, H), M["wall"])
box("Wand links", (W0 - 0.05, (D0 + D1) / 2, H / 2), (0.1, D1 - D0, H), M["wall"])
box("Wand rechts", (W1 + 0.05, (D0 + D1) / 2, H / 2), (0.1, D1 - D0, H), M["wall"])
# Glasfront: Sockel, Sturz, Pfosten, Glas, Glastür in der Mitte
box("Sockel", (0, D1, 0.2), (W1 - W0, 0.14, 0.4), M["frame"])
box("Sturz", (0, D1, H - 0.25), (W1 - W0, 0.14, 0.5), M["frame"])
for x in (-4.0, -2.4, -0.8, 0.8, 2.4, 4.0):
    box(f"Pfosten {x}", (x, D1, H / 2), (0.1, 0.14, H), M["frame"])
box("Glas", (0, D1, 1.45), (W1 - W0, 0.002, 2.1), M["glass"])
box("Türgriff", (0.55, D1 - 0.12, 1.05), (0.04, 0.04, 0.8), M["frame"])
box("Öffnungszeiten", (-1.3, D1 - 0.02, 1.55), (0.36, 0.01, 0.5), mat("Schild", (0.85, 0.85, 0.8), 0.6))
# Leuchtröhren an der Decke
tubes = []
for i, (x, y) in enumerate([(-2, -2.5), (1.5, -2.5), (-2, 0), (1.5, 0), (-2, 2.2), (1.5, 2.2)]):
    dead = i in (0, 3)
    t = box(f"Röhre {i}", (x, y, H - 0.03), (1.3, 0.22, 0.04), mat("Röhre kaputt", (0.6, 0.62, 0.6), 0.4) if dead else (TUBE_FLICK if i == 5 else TUBE))
    if not dead:
        tubes.append((i, t))
# Kühlregale links (leuchtende Türen)
for i, y in enumerate((-3.0, -1.6, -0.2, 1.2)):
    box(f"Kühltür {i}", (W0 + 0.35, y, 1.15), (0.6, 1.3, 2.0), M["frame"])
    box(f"Kühllicht {i}", (W0 + 0.66, y, 1.15), (0.02, 1.2, 1.85), FRIDGE)
# Regalreihen mit Waren
for gx in (-1.6, 0.3):
    box(f"Regal {gx}", (gx, -1.2, 0.8), (0.9, 3.6, 1.6), M["shelf"])
    for side in (-1, 1):
        for lvl in range(3):
            y = -2.9
            while y < 0.5:
                w = R.uniform(0.12, 0.3)
                c = R.choice([(0.45, 0.06, 0.05), (0.05, 0.15, 0.4), (0.55, 0.4, 0.05), (0.06, 0.28, 0.1), (0.5, 0.5, 0.48), (0.25, 0.08, 0.25), (0.6, 0.3, 0.05)])
                if R.random() < 0.35:
                    for k in range(max(1, int(w / 0.07))):
                        cyl("Flasche", (gx + side * 0.5, y + 0.035 + k * 0.07, 0.35 + lvl * 0.48), 0.03, R.uniform(0.22, 0.3), mat("Flasche", c, 0.15), verts=10)
                else:
                    box("Ware", (gx + side * 0.5, y + w / 2, 0.35 + lvl * 0.48), (0.14, w * 0.9, R.uniform(0.2, 0.32)), mat("Ware", c, 0.6))
                y += w
# Theke mit Kasse rechts vorn
box("Theke", (2.9, 0.6, 0.5), (1.6, 2.6, 1.0), M["counter"])
box("Thekenplatte", (2.9, 0.6, 1.02), (1.7, 2.7, 0.05), M["top"])
box("Kasse", (2.7, 0.2, 1.17), (0.45, 0.4, 0.25), M["frame"])
box("Kassenbildschirm", (2.62, 0.2, 1.42), (0.05, 0.36, 0.26), mat("Bildschirm", (0.1, 0.2, 0.3), 0.3, emit=(0.4, 0.7, 1.0), strength=2.0))
box("Zigarettenregal", (3.85, 0.6, 1.9), (0.3, 2.4, 1.2), M["shelf"])

# ---------------------------------------------------------------- Draußen
box("Asphalt", (0, 18, -0.06), (60, 30, 0.1), M["asphalt"])
box("Gehweg", (0, D1 + 0.8, 0.0), (12, 1.6, 0.12), M["concrete"])
box("Tankdach", (0, 9.5, 4.6), (14, 7, 0.4), M["canopy"])
for x in (-4.5, 0, 4.5):
    for y in (7.5, 11.5):
        box("Dachlicht", (x, y, 4.38), (1.2, 0.5, 0.02), CANOPY_L)
for x in (-3, 3):
    box("Insel", (x, 9.5, 0.1), (1.2, 4, 0.2), M["concrete"])
    box("Zapfsäule", (x, 9.5, 1.0), (0.6, 0.9, 1.8), M["pump"])
    box("Säulenlicht", (x, 9.03, 1.45), (0.45, 0.02, 0.3), mat("Display", (1, 1, 1), 0.5, emit=(1.0, 0.95, 0.85), strength=3))
    cyl("Dachstütze", (x * 1.8, 9.5, 2.3), 0.15, 4.6, M["frame"])
# ferne Straßenlaternen
for x in (-14, 10, 22):
    cyl("Mast", (x, 24, 3), 0.08, 6, M["frame"])
    sphere("Laterne", (x, 24, 6.0), 0.25, mat("Laterne", (1, 1, 1), 0.5, emit=(1.0, 0.65, 0.3), strength=25))

# ---------------------------------------------------------------- Die Gestalt (zu groß, zu dünn, Arme zu lang)
def cone(name, loc, r1, r2, h, material, scale=(1, 1, 1), rot=(0, 0, 0), verts=32):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=h, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o


EYESHINE = mat("Augenglanz", (0.0, 0.0, 0.0), 0.3, emit=(0.85, 0.9, 0.8), strength=1.2)


def figure(name, pos, tilt=0.0):
    """Großer, hagerer Mensch im langen dunklen Mantel mit Kapuze. Gesicht im Schatten, nur schwacher Augenglanz."""
    x, y = pos
    parts = [
        cyl(name + " Bein L", (x - 0.09, y, 0.3), 0.06, 0.6, M["cloth"]),
        cyl(name + " Bein R", (x + 0.09, y, 0.3), 0.06, 0.6, M["cloth"]),
        cone(name + " Mantel", (x, y, 1.12), 0.3, 0.2, 1.15, M["cloth"], scale=(1.0, 0.62, 1.0)),
        sphere(name + " Schultern", (x, y, 1.68), 0.25, M["cloth"], scale=(1.0, 0.55, 0.42)),
        cyl(name + " Arm L", (x - 0.27, y + 0.02, 1.22), 0.05, 0.92, M["cloth"], rot=(0, math.radians(-5), 0)),
        cyl(name + " Arm R", (x + 0.27, y + 0.02, 1.22), 0.05, 0.92, M["cloth"], rot=(0, math.radians(5), 0)),
        sphere(name + " Hand L", (x - 0.31, y + 0.02, 0.72), 0.05, M["skin"], scale=(0.7, 0.7, 1.7)),
        sphere(name + " Hand R", (x + 0.31, y + 0.02, 0.72), 0.05, M["skin"], scale=(0.7, 0.7, 1.7)),
        cyl(name + " Hals", (x, y, 1.82), 0.055, 0.16, M["cloth"]),
        sphere(name + " Kapuze", (x, y + 0.02, 2.0), 0.155, M["cloth"], scale=(1.0, 1.05, 1.22)),
        sphere(name + " Gesicht", (x, y - 0.075, 1.97), 0.1, mat("Gesicht", (0.05, 0.045, 0.04), 0.8), scale=(0.85, 0.6, 1.15)),
    ]
    for dx in (-0.038, 0.038):
        parts.append(sphere(name + " Auge", (x + dx, y - 0.13, 2.0), 0.011, EYESHINE))
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[2]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    # Ursprung an die Füße, leicht geneigter Kopf/Körper
    bpy.context.scene.cursor.location = (x, y, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    o.rotation_euler = (0, math.radians(tilt), 0)
    return o


far = figure("Gestalt weit", (-1.55, 6.4))
near = figure("Gestalt Tür", (0.25, D1 + 0.3), tilt=-7)
# Sichtbarkeit: weit bis vor dem Blackout, nah danach
for o, vis in ((far, lambda f: f < JUMP), (near, lambda f: f >= JUMP)):
    for f in range(1, N_FRAMES + 1):
        o.hide_render = not vis(f)
        o.keyframe_insert("hide_render", frame=f)
# leichtes Schwanken der weiten Gestalt (fast unmerklich)
for f in range(1, JUMP, 5):
    far.rotation_euler = (0, math.radians(0.8 * math.sin(f * 0.4)), 0)
    far.keyframe_insert("rotation_euler", frame=f)

# ---------------------------------------------------------------- Regen (nur draußen)
def rain_sheet(name, z0):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rr = random.Random(hash(name) & 0xFFFF)
    for _ in range(900):
        x, y, z = rr.uniform(-6, 6), rr.uniform(D1 + 0.3, 12), rr.uniform(0, 5)
        l, w = rr.uniform(0.25, 0.45), 0.006
        v = [bm.verts.new((x - w, y, z)), bm.verts.new((x + w, y, z)), bm.verts.new((x + w + 0.02, y, z + l)), bm.verts.new((x - w + 0.02, y, z + l))]
        bm.faces.new(v)
    bm.to_mesh(me)
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.data.materials.append(M["rain"])
    o.location.z = z0
    fc = o.driver_add("location", 2)
    fc.driver.expression = f"{z0} - ((frame * 0.55) % 5.0)"
    return o


rain_sheet("Regen A", 0.0)
rain_sheet("Regen B", 5.0)

# ---------------------------------------------------------------- Licht-Flackern und Blackout (Emissionsstärke)
def strength_keys(material, base, flicker=False):
    sock = material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    rr = random.Random(11)
    for f in range(1, N_FRAMES + 1):
        v = base
        if flicker and rr.random() < 0.22:
            v = base * rr.choice([0.05, 0.2, 0.5])
        if BLACK[0] <= f <= BLACK[1]:
            v = 0.0
        if f in (BLACK[0] - 2, BLACK[0] - 4) or f == JUMP:
            v = base * 0.15
        sock.default_value = v
        sock.keyframe_insert("default_value", frame=f)


strength_keys(TUBE, 4.0)
strength_keys(TUBE_FLICK, 4.0, flicker=True)
strength_keys(FRIDGE, 1.6)

# Zusatzlicht innen (Flächenlichter unter den Röhren, damit es sauber ausleuchtet) – flackert mit
lamps = []
for i, t in tubes:
    bpy.ops.object.light_add(type="AREA", location=(t.location.x, t.location.y, H - 0.15))
    L = bpy.context.object
    L.data.shape = "RECTANGLE"
    L.data.size, L.data.size_y = 1.3, 0.3
    L.data.color = (0.86, 0.93, 1.0)
    L.data.energy = 38
    lamps.append(L)
    rr = random.Random(11)
    for f in range(1, N_FRAMES + 1):
        e = 38
        if i == 5 and rr.random() < 0.22:
            e = 38 * rr.choice([0.05, 0.2, 0.5])
        if BLACK[0] <= f <= BLACK[1]:
            e = 0
        if f in (BLACK[0] - 2, BLACK[0] - 4) or f == JUMP:
            e = 6
        L.data.energy = e
        L.data.keyframe_insert("energy", frame=f)
# Licht unter dem Tankdach (draußen, bleibt an)
for x in (-4.5, 0, 4.5):
    for y in (7.5, 11.5):
        bpy.ops.object.light_add(type="AREA", location=(x, y, 4.3))
        L = bpy.context.object
        L.data.size = 1.2
        L.data.color = (1.0, 0.9, 0.75)
        L.data.energy = 1300
# schwaches Gegenlicht auf die Gestalten (vom Dach aus), damit die Silhouette sichtbar ist
bpy.ops.object.light_add(type="SPOT", location=(1.0, 8.0, 4.2), rotation=(math.radians(-55), 0, math.radians(180)))
sp = bpy.context.object
sp.data.energy = 300
sp.data.spot_size = math.radians(45)
sp.data.color = (1.0, 0.88, 0.7)

# ---------------------------------------------------------------- Welt, Kamera, Render
w = bpy.data.worlds.new("Nacht")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.005, 0.009, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
sc.world = w

bpy.ops.object.camera_add(location=(3.55, -2.2, 2.75))
cam = bpy.context.object
cam.data.lens = 17
cam.data.sensor_width = 36
cam.data.sensor_fit = "VERTICAL"
target = Vector((-0.2, 3.0, 0.95))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam

sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 40
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.cycles.diffuse_bounces = 2
sc.cycles.glossy_bounces = 2
sc.cycles.transparent_max_bounces = 4
sc.cycles.blur_glossy = 1.0
sc.cycles.sample_clamp_indirect = 3.0
sc.render.resolution_x, sc.render.resolution_y = RES
sc.render.resolution_percentage = 100
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N_FRAMES
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "None"
sc.view_settings.exposure = -0.3
sc.render.image_settings.file_format = "PNG"

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
os.makedirs(os.path.join(BUILD, "frames"), exist_ok=True)
if "--save" in args:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BUILD, "nachtschicht.blend"))
if "--still" in args:
    for f in args[args.index("--still") + 1].split(","):
        sc.frame_set(int(f))
        sc.render.filepath = os.path.join(BUILD, f"still_{int(f):04d}.png")
        bpy.ops.render.render(write_still=True)
if "--frames" in args:
    a, b = (int(v) for v in args[args.index("--frames") + 1].split("-"))
    for f in range(a, b + 1):
        out = os.path.join(BUILD, "frames", f"{f:04d}.png")
        if os.path.exists(out):
            continue
        sc.frame_set(f)
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print(f"Bild {f}/{b} fertig", flush=True)

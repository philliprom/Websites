"""Nachtschicht – Teil 1: Blender-Szene (Tankstelle bei Nacht) mit mehreren Einstellungen.
Geometrie wie im Test (horror-nachtschicht/scene.py), dazu Außenkamera, Fassade, bessere Zapfsäulen, Regel-Zettel.

  <bl>/bin/python nachtschicht-teil1/scene.py --shot r1 --still 5        # Standbild einer Einstellung
  <bl>/bin/python nachtschicht-teil1/scene.py --shot r2 --frames all     # alle Bilder -> build/r2/0001.png …
  <bl>/bin/python nachtschicht-teil1/scene.py --shot note                # Regel-Zettel (Standbild + Textkästen)
Einstellungen und Ereignisse (Flackern, Stromausfall, Sprung) kommen aus build/shots.json (shots.py), sonst Testwerte.
  r1  CAM 01 Eingang, Laden leer, am Ende flackert das Licht
  r2  CAM 03 Zapfsäulen, Gestalt steht im Regen, Tankdach-Licht flackert, Gestalt verschwindet
  r3  CAM 01 Eingang, Licht dippt, Stromausfall, danach steht die Gestalt mit der Hand an der Tür
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
FPS = 10
RES = (432, 768)

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
    """Bodenfliesen 30 cm mit dunklen Fugen, Schmutz (Rauschen) und nassen Stellen am Eingang (glänzender)."""
    m = bpy.data.materials.new("Fliesen")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = 3.33
    br.inputs["Color1"].default_value = (0.22, 0.22, 0.205, 1)
    br.inputs["Color2"].default_value = (0.19, 0.19, 0.18, 1)
    br.inputs["Mortar"].default_value = (0.06, 0.06, 0.055, 1)
    br.inputs["Mortar Size"].default_value = 0.012
    br.inputs["Brick Width"].default_value = 1.0
    br.inputs["Row Height"].default_value = 1.0
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.5
    nz.inputs["Detail"].default_value = 8
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 0.55
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(br.outputs["Color"], mix.inputs["A"])
    nt.links.new(nz.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    rr = nt.nodes.new("ShaderNodeMapRange")
    rr.inputs["To Min"].default_value = 0.18
    rr.inputs["To Max"].default_value = 0.55
    nt.links.new(nz.outputs["Fac"], rr.inputs["Value"])
    nt.links.new(rr.outputs["Result"], b.inputs["Roughness"])
    return m


def grid_mat(name, c1, c2, line, scale):
    """Rasterdecke: helle Platten mit dunklen Schienen."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = scale
    br.inputs["Color1"].default_value = (*c1, 1)
    br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (*line, 1)
    br.inputs["Mortar Size"].default_value = 0.015
    br.inputs["Brick Width"].default_value = 1.0
    br.inputs["Row Height"].default_value = 0.5
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.9
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
    "ceil": grid_mat("Decke", (0.24, 0.24, 0.23), (0.22, 0.22, 0.21), (0.08, 0.08, 0.08), 1.65),
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
    box(f"Kühlkorpus {i}", (W0 + 0.3, y, 1.15), (0.6, 1.36, 2.1), M["frame"])
    box(f"Kühllicht {i}", (W0 + 0.12, y, 1.15), (0.02, 1.2, 1.85), FRIDGE)
    for z in (0.35, 0.8, 1.25, 1.7):
        box("Kühlboden", (W0 + 0.35, y, z - 0.03), (0.45, 1.2, 0.02), M["shelf"])
        for k in range(9):
            c = R.choice([(0.6, 0.05, 0.05), (0.05, 0.3, 0.08), (0.75, 0.55, 0.05), (0.08, 0.12, 0.4), (0.7, 0.7, 0.7)])
            cyl("Kühlflasche", (W0 + 0.42, y - 0.52 + k * 0.13, z + 0.12), 0.032, 0.24, mat("Fl", c, 0.12), verts=10)
    for dy in (-0.66, 0.66):
        box("Türrahmen", (W0 + 0.61, y + dy, 1.15), (0.03, 0.05, 2.06), M["frame"])
    box("Türgriff Kühl", (W0 + 0.64, y + 0.55, 1.2), (0.03, 0.03, 0.6), mat("Chrom", (0.8, 0.8, 0.8), 0.2, 1.0))
    box("Kühlglas", (W0 + 0.61, y, 1.15), (0.002, 1.3, 2.0), M["glass"])
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

# ---------------------------------------------------------------- Details
def text(name, body, loc, size, material, rot=(math.radians(90), 0, 0), extrude=0.0, align="CENTER", mirror=False):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.data.body = body
    o.data.size = size
    o.data.extrude = extrude
    o.data.align_x = align
    o.data.align_y = "CENTER"
    o.data.materials.append(material)
    if mirror:
        o.scale.x = -1
    return o


NEON = mat("Neon rot", (1, 0.1, 0.1), 0.4, emit=(1.0, 0.08, 0.06), strength=14.0)
WHITE = mat("Papier", (0.8, 0.8, 0.76), 0.7)
PRINT = mat("Druck", (0.05, 0.05, 0.06), 0.6)
YEL = mat("Plakat gelb", (0.85, 0.65, 0.05), 0.6)
RED = mat("Plakat rot", (0.6, 0.04, 0.04), 0.6)
# „OFFEN“-Neonschild im Fenster, Schrift zeigt nach draußen (von innen spiegelverkehrt)
text("Neon OFFEN", "OFFEN", (-2.0, D1 - 0.09, 2.25), 0.36, NEON, extrude=0.01, mirror=True)
box("Neon Rahmen", (-2.0, D1 - 0.03, 2.25), (1.15, 0.01, 0.46), mat("Neonrahmen", (0.02, 0.02, 0.02), 0.5))
bpy.ops.object.light_add(type="POINT", location=(-2.0, D1 - 0.35, 2.25))
nl = bpy.context.object
nl.data.color = (1.0, 0.15, 0.1)
nl.data.energy = 25
nl.data.shadow_soft_size = 0.4
# „24/7“-Aufkleber, Öffnungszeiten, „ZIEHEN“ an der Tür (spiegelverkehrt von innen gesehen)
text("24/7", "24/7", (1.6, D1 - 0.02, 1.9), 0.22, YEL, mirror=True)
text("Ziehen", "DRÜCKEN", (0.0, D1 - 0.02, 1.3), 0.07, WHITE)
text("Zeiten", "MO–SO\n0–24 UHR", (-1.3, D1 - 0.03, 1.6), 0.06, PRINT)
# Plakate an der Rückwand und rechts
box("Plakat 1", (-0.8, D0 + 0.01, 1.9), (0.9, 0.01, 1.2), YEL)
text("Plakat 1 Text", "KAFFEE\n1,50 €", (-0.8, D0 + 0.03, 1.9), 0.18, RED, rot=(math.radians(90), 0, 0))
box("Plakat 2", (W1 - 0.01, -2.6, 1.9), (0.01, 0.8, 1.0), RED)
text("Plakat 2 Text", "2 FÜR 1", (W1 - 0.03, -2.6, 1.9), 0.16, mat("Weiß", (0.9, 0.9, 0.9), 0.6), rot=(math.radians(90), 0, math.radians(90)))
# Preisschilder an den Regalkanten
for gx in (-1.6, 0.3):
    for side in (-1, 1):
        for lvl in range(3):
            box("Preisleiste", (gx + side * 0.46, -1.2, 0.2 + lvl * 0.48), (0.02, 3.5, 0.05), WHITE)
            for k in range(10):
                box("Preisschild", (gx + side * 0.475, -2.85 + k * 0.36, 0.2 + lvl * 0.48), (0.01, 0.1, 0.045), YEL if k % 3 == 0 else WHITE)
    text("Regalschild", ["SNACKS", "GETRÄNKE"][gx > 0], (gx, -1.2, 1.85), 0.16, WHITE, rot=(math.radians(90), 0, math.radians(90)))
    box("Schildträger", (gx, -1.2, 1.85), (0.02, 1.2, 0.26), RED)
# Sicherheitsspiegel in der Ecke über dem Eingang
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(-3.75, 2.75, 2.55), segments=32, ring_count=16)
mirror = bpy.context.object
mirror.scale = (0.45, 0.45, 1.0)
mirror.data.materials.append(mat("Spiegel", (0.9, 0.9, 0.9), 0.02, 1.0))
bpy.ops.object.shade_smooth()
# Kaffeeautomat an der Rückwand rechts
box("Kaffeeautomat", (2.2, D0 + 0.35, 0.95), (0.7, 0.6, 1.9), mat("Automat", (0.12, 0.12, 0.13), 0.35, 0.6))
box("Automat Display", (2.2, D0 + 0.66, 1.45), (0.4, 0.01, 0.25), mat("Display blau", (1, 1, 1), 0.4, emit=(0.3, 0.6, 1.0), strength=4))
box("Automat Front", (2.2, D0 + 0.66, 1.05), (0.5, 0.01, 0.35), mat("Kaffeebild", (0.35, 0.2, 0.1), 0.5))
for k in range(6):
    cyl("Becher", (2.75, D0 + 0.35, 1.0 + k * 0.012), 0.04, 0.012, WHITE)
# Theke: Zigarettenregal mit Packungen, Kaugummi, Lotto, kleiner Überwachungsmonitor, Kaffeebecher
for row in range(4):
    for k in range(14):
        c = R.choice([(0.7, 0.7, 0.7), (0.6, 0.05, 0.05), (0.05, 0.1, 0.35), (0.7, 0.6, 0.1), (0.1, 0.1, 0.1)])
        box("Packung", (3.69, -0.5 + k * 0.16, 1.45 + row * 0.24), (0.04, 0.12, 0.17), mat("Pk", c, 0.5))
box("Monitor", (2.45, 1.45, 1.25), (0.35, 0.32, 0.4), mat("Monitorgehäuse", (0.08, 0.08, 0.08), 0.5))
box("Monitorbild", (2.27, 1.45, 1.27), (0.01, 0.27, 0.22), mat("Monitorbild", (1, 1, 1), 0.4, emit=(0.55, 0.65, 0.6), strength=1.6))
cyl("Kaffeebecher", (2.55, -0.3, 1.1), 0.045, 0.12, WHITE)
box("Lotto", (2.25, 1.85, 1.28), (0.02, 0.32, 0.42), mat("Lotto", (0.8, 0.75, 0.1), 0.5))
text("Lotto Text", "LOTTO", (2.235, 1.85, 1.38), 0.08, RED, rot=(math.radians(90), 0, math.radians(-90)))
box("Kaugummi", (2.2, 0.75, 1.1), (0.18, 0.5, 0.12), mat("Kaugummi", (0.1, 0.5, 0.6), 0.4))
# Fußmatte und Pfütze vor der Tür
box("Fußmatte", (0.1, D1 - 0.6, 0.006), (1.3, 0.8, 0.012), mat("Matte", (0.05, 0.05, 0.05), 0.95))
bpy.ops.mesh.primitive_circle_add(vertices=48, radius=0.55, fill_type="NGON", location=(-0.4, D1 - 1.5, 0.003))
pf = bpy.context.object
pf.scale = (1.4, 0.7, 1)
pf.data.materials.append(mat("Pfütze", (0.02, 0.02, 0.02), 0.02, spec=1.0))
# Draußen: Bordstein, Parkmarkierungen, Mülleimer, Preissäule, Luftstation
box("Bordstein", (0, D1 + 1.62, 0.06), (12, 0.12, 0.14), mat("Bordstein", (0.35, 0.35, 0.34), 0.8))
for x in (-5.5, -2.8, -0.1, 2.6, 5.3):
    box("Markierung", (x, 4.9, -0.005), (0.1, 1.6, 0.01), mat("Farbe weiß", (0.7, 0.7, 0.68), 0.6))
cyl("Mülleimer", (2.0, D1 + 0.9, 0.45), 0.24, 0.9, mat("Mülleimer", (0.15, 0.2, 0.15), 0.6))
box("Preissäule", (-5.2, 13.5, 2.5), (1.4, 0.4, 5.0), mat("Säule", (0.15, 0.15, 0.17), 0.5))
for k, (lab, pr) in enumerate((("SUPER E10", "1,79"), ("DIESEL", "1,65"))):
    text("Preis Label", lab, (-5.65, 13.28, 3.9 - k * 0.8), 0.22, WHITE, align="LEFT")
    text("Preis LED", pr, (-4.6, 13.28, 3.9 - k * 0.8), 0.36, mat("LED", (1, 1, 1), 0.4, emit=(1.0, 0.35, 0.05), strength=12), align="RIGHT")
box("Luftstation", (4.6, 6.2, 0.7), (0.4, 0.4, 1.4), mat("Luft", (0.1, 0.25, 0.55), 0.5))


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


def figure(name, pos, tilt=0.0, hand_on_glass=False):
    """Großer, hagerer Mensch im langen dunklen Mantel mit Kapuze. Gesicht im Schatten, nur schwacher Augenglanz."""
    x, y = pos
    parts = [
        cyl(name + " Bein L", (x - 0.09, y, 0.3), 0.06, 0.6, M["cloth"]),
        cyl(name + " Bein R", (x + 0.09, y, 0.3), 0.06, 0.6, M["cloth"]),
        cone(name + " Mantel", (x, y, 1.12), 0.3, 0.2, 1.15, M["cloth"], scale=(1.0, 0.62, 1.0)),
        sphere(name + " Schultern", (x, y, 1.68), 0.25, M["cloth"], scale=(1.0, 0.55, 0.42)),
        cyl(name + " Arm L", (x - 0.27, y + 0.02, 1.22), 0.05, 0.92, M["cloth"], rot=(0, math.radians(-5), 0)),
        sphere(name + " Hand L", (x - 0.31, y + 0.02, 0.72), 0.05, M["skin"], scale=(0.7, 0.7, 1.7)),
        cyl(name + " Hals", (x, y, 1.82), 0.055, 0.16, M["cloth"]),
        sphere(name + " Kapuze", (x, y + 0.02, 2.0), 0.155, M["cloth"], scale=(1.0, 1.05, 1.22)),
        sphere(name + " Gesicht", (x, y - 0.075, 1.97), 0.1, mat("Gesicht", (0.05, 0.045, 0.04), 0.8), scale=(0.85, 0.6, 1.15)),
    ]
    for dx in (-0.038, 0.038):
        parts.append(sphere(name + " Auge", (x + dx, y - 0.13, 2.0), 0.011, EYESHINE))
    if hand_on_glass:
        # rechter Arm nach vorn gehoben, flache Hand liegt an der Glasscheibe
        sh, hd = Vector((x + 0.26, y, 1.62)), Vector((x + 0.34, D1 + 0.035, 1.8))
        mid = (sh + hd) / 2
        arm = cyl(name + " Arm R", tuple(mid), 0.05, (hd - sh).length, M["cloth"])
        arm.rotation_euler = (hd - sh).to_track_quat("Z", "Y").to_euler()
        parts.append(arm)
        palm = sphere(name + " Hand R", (hd.x, hd.y + 0.012, hd.z), 0.075, M["skin"], scale=(0.75, 0.22, 1.05))
        parts.append(palm)
        for k in range(4):
            parts.append(cyl(name + " Finger", (hd.x - 0.04 + k * 0.027, hd.y + 0.01, hd.z + 0.1), 0.011, 0.11, M["skin"], verts=8))
    else:
        parts.append(cyl(name + " Arm R", (x + 0.27, y + 0.02, 1.22), 0.05, 0.92, M["cloth"], rot=(0, math.radians(5), 0)))
        parts.append(sphere(name + " Hand R", (x + 0.31, y + 0.02, 0.72), 0.05, M["skin"], scale=(0.7, 0.7, 1.7)))
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


# ================================================================ Ab hier: Folge 1 (Außen-Details, Zettel, Einstellungen)
FONT_TYPE = bpy.data.fonts.load(os.path.join(HERE, "fonts", "SpecialElite-Regular.ttf"))
FONT_MARK = bpy.data.fonts.load(os.path.join(HERE, "fonts", "PermanentMarker-Regular.ttf"))

# Pfütze im Laden wirkte wie ein Loch im Boden: raus
if bpy.data.objects.get("Circle"):
    bpy.data.objects.remove(bpy.data.objects["Circle"], do_unlink=True)

# ---------------------------------------------------------------- Fassade, Dach, Vordach-Licht
FAC = mat("Fassade", (0.16, 0.16, 0.17), 0.7)
box("Dach Laden", (0, (D0 + D1) / 2, H + 0.35), (W1 - W0 + 0.6, D1 - D0 + 0.6, 0.5), FAC)
box("Blende", (0, D1 + 0.25, H + 0.35), (W1 - W0 + 0.6, 0.1, 0.62), FAC)
SIGN = mat("Leuchtschrift", (1, 1, 1), 0.4, emit=(0.92, 0.95, 1.0), strength=7)
text("Fassadenschrift", "SHOP  ·  BISTRO  ·  24 H", (0, D1 + 0.31, H + 0.33), 0.26, SIGN, rot=(math.radians(90), 0, math.radians(180)))
for x in (-3.0, -1.0, 1.0, 3.0):
    cyl("Downlight", (x, D1 + 0.2, H + 0.09), 0.07, 0.01, mat("Downlight", (1, 1, 1), 0.4, emit=(1.0, 0.9, 0.75), strength=20))
    bpy.ops.object.light_add(type="SPOT", location=(x, D1 + 0.2, H + 0.05))
    s_ = bpy.context.object
    s_.data.energy, s_.data.spot_size, s_.data.color = 70, math.radians(80), (1.0, 0.88, 0.7)
# Leuchtband rund um das Tankdach
BAND = mat("Dachband", (1, 1, 1), 0.4, emit=(0.75, 0.85, 1.0), strength=5)
for (cx, cy, sx, sy) in ((0, 6.0, 14.02, 0.02), (0, 13.0, 14.02, 0.02), (-7.0, 9.5, 0.02, 7.02), (7.0, 9.5, 0.02, 7.02)):
    box("Dachband", (cx, cy, 4.62), (sx, sy, 0.14), BAND)

# ---------------------------------------------------------------- Zapfsäulen-Details, Poller, Pfützen, Straße, Bäume
RUBBER = mat("Gummi", (0.015, 0.015, 0.015), 0.6)


def hose(name, pts):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.018
    sp_ = cu.splines.new("BEZIER")
    sp_.bezier_points.add(len(pts) - 1)
    for bp_, p in zip(sp_.bezier_points, pts):
        bp_.co = p
        bp_.handle_left_type = bp_.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    sc.collection.objects.link(o)
    o.data.materials.append(RUBBER)
    return o


for k, x in enumerate((-3, 3)):
    box("Säulenkopf", (x, 9.5, 2.05), (0.72, 1.0, 0.32), mat("Kopf", (0.2, 0.2, 0.22), 0.5))
    for yy in (8.99, 10.01):
        box("Preisband", (x, yy, 2.05), (0.6, 0.01, 0.14), mat("Preisband", (1, 1, 1), 0.4, emit=(1.0, 0.45, 0.08), strength=6))
        box("Display", (x, yy, 1.38), (0.34, 0.01, 0.22), mat("Display Säule", (1, 1, 1), 0.4, emit=(0.5, 0.8, 1.0), strength=3))
    text("Säulennummer", str(k + 1), (x, 10.0, 0.75), 0.3, mat("Weiß matt", (0.85, 0.85, 0.85), 0.6), rot=(math.radians(90), 0, math.radians(180)))
    for side in (-1, 1):
        hx = x + side * 0.31
        hose("Schlauch", [(hx, 9.5, 1.75), (hx + side * 0.18, 9.62, 1.0), (hx + side * 0.07, 9.7, 0.55), (hx, 9.62, 1.15)])
        box("Zapfpistole", (hx + side * 0.02, 9.62, 1.2), (0.05, 0.14, 0.2), RUBBER)
    for yy in (7.65, 11.35):
        cyl("Poller", (x, yy, 0.5), 0.09, 0.8, mat("Poller gelb", (0.75, 0.6, 0.05), 0.5))
        cyl("Poller Band", (x, yy, 0.62), 0.092, 0.12, mat("Poller schwarz", (0.02, 0.02, 0.02), 0.5))
PUDDLE = mat("Pfütze außen", (0.01, 0.01, 0.012), 0.03, spec=1.0)
for (px, py, rx, ry) in ((-0.5, 4.75, 0.9, 0.45), (1.9, 5.3, 0.7, 0.3), (-2.6, 4.4, 0.6, 0.35), (0.8, 7.2, 1.1, 0.5)):
    bpy.ops.mesh.primitive_circle_add(vertices=40, radius=1, fill_type="NGON", location=(px, py, 0.004))
    o = bpy.context.object
    o.scale = (rx, ry, 1)
    o.data.materials.append(PUDDLE)
for x in range(-28, 30, 5):
    box("Mittellinie", (x, 18.0, -0.004), (2.4, 0.12, 0.01), mat("Linie", (0.55, 0.55, 0.5), 0.7))
def slab_mat():
    m = bpy.data.materials.new("Betonplatten")
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Scale"].default_value = 0.8
    br.inputs["Color1"].default_value = (0.06, 0.06, 0.057, 1)
    br.inputs["Color2"].default_value = (0.05, 0.05, 0.048, 1)
    br.inputs["Mortar"].default_value = (0.015, 0.015, 0.015, 1)
    br.inputs["Mortar Size"].default_value = 0.01
    br.inputs["Brick Width"].default_value = 1.0
    br.inputs["Row Height"].default_value = 1.0
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 0.9
    nz.inputs["Detail"].default_value = 6
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.42
    cr.color_ramp.elements[0].color = (0.16, 0.15, 0.14, 1)
    cr.color_ramp.elements[1].position = 0.62
    cr.color_ramp.elements[1].color = (1, 1, 1, 1)
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.inputs["Factor"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(br.outputs["Color"], mix.inputs["A"])
    nt.links.new(cr.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.7
    return m


box("Betonplatten", (0, 9.5, 0.001), (14, 7, 0.01), slab_mat())
am = bpy.data.materials["Asphalt"].node_tree
am.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.012, 0.012, 0.014, 1)
ramp = [n for n in am.nodes if n.type == "VALTORGB"][0].color_ramp
ramp.elements[0].color = (0.04, 0.04, 0.04, 1)
ramp.elements[1].color = (0.22, 0.22, 0.22, 1)
TREE = mat("Baum", (0.006, 0.01, 0.007), 0.9)
RT = random.Random(99)
for i in range(26):
    x = RT.uniform(-26, 26)
    y = RT.uniform(-16, -9) if abs(x) < 14 else RT.uniform(-12, 26)
    h = RT.uniform(6, 11)
    cone("Baum", (x, y, h / 2), RT.uniform(1.4, 2.6), 0.05, h, TREE, verts=10)

# ---------------------------------------------------------------- Regel-Zettel auf der Theke
paper_m = bpy.data.materials.new("Papier laminiert")
paper_m.use_nodes = True
pn = paper_m.node_tree
pb = pn.nodes["Principled BSDF"]
nz = pn.nodes.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 40
cr = pn.nodes.new("ShaderNodeValToRGB")
cr.color_ramp.elements[0].color = (0.74, 0.72, 0.66, 1)
cr.color_ramp.elements[1].color = (0.86, 0.85, 0.8, 1)
pn.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
pn.links.new(cr.outputs["Color"], pb.inputs["Base Color"])
pb.inputs["Roughness"].default_value = 0.28
bpy.ops.object.empty_add(location=(3.05, 0.98, 1.048))
NOTE = bpy.context.object
NOTE.name = "Zettel"
NOTE.rotation_euler = (0, 0, math.radians(90 + 4))
NOTE_PARTS = {}


def on_note(o, lx, ly, lz=0.0, rz=0.0):
    o.parent = NOTE
    o.location = (lx, ly, lz)
    o.rotation_euler = (0, 0, math.radians(rz))
    return o


bpy.ops.mesh.primitive_plane_add(size=1)
paper = bpy.context.object
paper.name = "Papier"
paper.scale = (0.21, 0.297, 1)
paper.data.materials.append(paper_m)
on_note(paper, 0, 0)
INK = mat("Tinte", (0.008, 0.008, 0.01), 0.7)
REDINK = mat("Rotstift", (0.55, 0.02, 0.02), 0.5)


def note_text(key, body, ly, size, font, material, lx=-0.088, rz=0.0, align="LEFT"):
    bpy.ops.object.text_add()
    o = bpy.context.object
    o.name = key
    o.data.body = body
    o.data.font = font
    o.data.size = size
    o.data.align_x = align
    o.data.materials.append(material)
    on_note(o, lx, ly, 0.0006, rz)
    NOTE_PARTS[key] = o
    return o


note_text("Titel", "NACHTSCHICHT - REGELN", 0.115, 0.0145, FONT_TYPE, INK, lx=0.0, align="CENTER")
note_text("Strich", "_______________________", 0.105, 0.012, FONT_TYPE, INK, lx=0.0, align="CENTER")
note_text("Regel 1", "1. Ab 2:00 Uhr bleibt die Tür ZU.", 0.072, 0.0102, FONT_TYPE, INK)
note_text("Regel 2", "2. Flackert das Licht:\n    Schau auf Kamera 3.", 0.04, 0.0102, FONT_TYPE, INK)
note_text("Regel 3", "3. Steht draußen jemand still\n    im Regen: NICHT ansprechen.", -0.006, 0.0102, FONT_TYPE, INK)
note_text("Regel 4", "4. Er klopft dreimal.\n    Mach NIEMALS auf.", -0.052, 0.0102, FONT_TYPE, INK)
note_text("Rot", "Egal, wer es sagt!", -0.1, 0.0165, FONT_MARK, REDINK, lx=-0.075, rz=5)
note_text("Gruss", "- M.", -0.128, 0.011, FONT_TYPE, INK, lx=0.045)
# Unterstreichung mit Rotstift, Kaffeerand, Klebestreifen, Kugelschreiber
bpy.ops.mesh.primitive_plane_add(size=1)
ul = bpy.context.object
ul.scale = (0.105, 0.0016, 1)
ul.data.materials.append(REDINK)
on_note(ul, -0.02, -0.111, 0.0007, 4)
bpy.ops.mesh.primitive_torus_add(major_radius=0.034, minor_radius=0.0022, location=(0, 0, 0))
ring = bpy.context.object
ring.scale = (1, 1, 0.08)
ring.data.materials.append(mat("Kaffeerand", (0.25, 0.13, 0.05), 0.6, alpha=0.55))
on_note(ring, 0.118, 0.17, 0.0004)
TAPE = mat("Klebeband", (0.9, 0.88, 0.7), 0.25, alpha=0.45)
for (lx, ly, rz) in ((-0.1, 0.143, 40), (0.1, 0.143, -40), (-0.1, -0.143, -40), (0.1, -0.143, 40)):
    bpy.ops.mesh.primitive_plane_add(size=1)
    tp = bpy.context.object
    tp.scale = (0.05, 0.018, 1)
    tp.data.materials.append(TAPE)
    on_note(tp, lx, ly, 0.0009, rz)
pen = cyl("Kuli", (0, 0, 0), 0.0045, 0.14, mat("Kuli", (0.05, 0.12, 0.45), 0.3), rot=(0, math.radians(90), 0), verts=12)
on_note(pen, 0.14, -0.03, 0.005, 75)
pen.rotation_euler = (0, math.radians(90), math.radians(75))

# ---------------------------------------------------------------- Gestalten
fig_out = figure("Gestalt Regen", (-0.6, 5.35))
fig_out.rotation_euler = (0, 0, math.pi)          # schaut zur Außenkamera
fig_door = figure("Gestalt Tür", (0.25, D1 + 0.3), tilt=-7, hand_on_glass=True)


# ---------------------------------------------------------------- Regen nur unter freiem Himmel, Tropfkante am Tankdach
def rain_zone(name, zones, count, z0, lmin=0.25, lmax=0.45, ztop=5.0):
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rr = random.Random(sum(map(ord, name)))
    areas = [(x1 - x0) * (y1 - y0) for (x0, x1, y0, y1) in zones]
    for _ in range(count):
        x0, x1, y0, y1 = rr.choices(zones, weights=areas)[0]
        x, y, z = rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(0, ztop)
        ln, w = rr.uniform(lmin, lmax), 0.006
        v = [bm.verts.new((x - w, y, z)), bm.verts.new((x + w, y, z)), bm.verts.new((x + w + 0.02, y, z + ln)), bm.verts.new((x - w + 0.02, y, z + ln))]
        bm.faces.new(v)
    bm.to_mesh(me)
    o = bpy.data.objects.new(name, me)
    sc.collection.objects.link(o)
    o.data.materials.append(M["rain"])
    o.location.z = z0
    fc = o.driver_add("location", 2)
    fc.driver.expression = f"{z0} - ((frame * 0.8) % {ztop})"
    return o


OPEN = [(-10, 10, D1 + 0.35, 5.95), (-14, -7.1, 6.0, 13.0), (7.1, 14, 6.0, 13.0), (-16, 16, 13.05, 24)]
for zz in (0.0, 5.0):
    rain_zone(f"Regen {zz}", OPEN, 1500, zz)
DRIP = [(-7.0, 7.0, 5.97, 6.04), (-7.0, 7.0, 12.96, 13.03)]
for zz in (0.0, 4.4):
    rain_zone(f"Tropfkante {zz}", DRIP, 260, zz, 0.15, 0.3, ztop=4.4)

# ---------------------------------------------------------------- Lichter (werden pro Einstellung animiert)
LAMPS = []
for i, t in tubes:
    bpy.ops.object.light_add(type="AREA", location=(t.location.x, t.location.y, H - 0.15))
    L = bpy.context.object
    L.data.shape, L.data.size, L.data.size_y = "RECTANGLE", 1.3, 0.3
    L.data.color = (0.86, 0.93, 1.0)
    LAMPS.append((i, L))
CANOPY_LIGHTS = []
for x in (-4.5, 0, 4.5):
    for y in (7.5, 11.5):
        bpy.ops.object.light_add(type="AREA", location=(x, y, 4.3))
        L = bpy.context.object
        L.data.size = 1.2
        L.data.color = (1.0, 0.9, 0.75)
        CANOPY_LIGHTS.append(L)
bpy.ops.object.light_add(type="SPOT", location=(1.0, 8.0, 4.2), rotation=(math.radians(-55), 0, math.radians(180)))
sp = bpy.context.object
sp.data.energy, sp.data.spot_size, sp.data.color = 300, math.radians(45), (1.0, 0.88, 0.7)

w = bpy.data.worlds.new("Nacht")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.010, 0.012, 0.02, 1)
sc.world = w

# ---------------------------------------------------------------- Einstellung wählen
import json  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
SHOT = args[args.index("--shot") + 1] if "--shot" in args else "r1"


def _arg(name, default, typ=float):
    return typ(args[args.index(name) + 1]) if name in args else default


PROFIL_RES = _arg("--res", 1080, int)
PROFIL_SAMPLES = _arg("--samples", 128, int)
PROFIL_INNEN = _arg("--innen", 0.3)
PROFIL_AUGEN = _arg("--augen", 3.0)
PROFIL_DACH = _arg("--dach", 0.15)    # Tankdach-Licht (1 = wie in der Folge)
DEFAULTS = {
    "r1": {"frames": 95, "dips": [78, 79], "blackout": None, "jump": None, "flick5": list(range(70, 95, 3)), "canopy_off": [], "fig_out": 0},
    "r2": {"frames": 95, "dips": [], "blackout": None, "jump": None, "flick5": [], "canopy_off": [66, 67, 68, 70], "fig_out": 68},
    "r3": {"frames": 70, "dips": [6, 9], "blackout": [11, 15], "jump": 16, "flick5": [25, 26, 40, 52, 53, 61], "canopy_off": [], "fig_out": 0},
    "note": {"frames": 1, "dips": [], "blackout": None, "jump": None, "flick5": [], "canopy_off": [], "fig_out": 0},
    "profil": {"frames": 1, "dips": [], "blackout": None, "jump": None, "flick5": [], "canopy_off": [], "fig_out": 0},
}
sp_path = os.path.join(BUILD, "shots.json")
CFG = dict(DEFAULTS[SHOT])
if os.path.exists(sp_path):
    CFG.update(json.load(open(sp_path, encoding="utf-8")).get(SHOT, {}))
N = CFG["frames"]


def interior(f):
    if SHOT == "profil":
        return PROFIL_INNEN   # Laden fast dunkel: Gestalt hebt sich als Umriss vor dem hellen Tankdach ab
    b = CFG.get("blackout")
    if b and b[0] <= f <= b[1]:
        return 0.0
    if f in CFG["dips"] or f == CFG.get("jump"):
        return 0.15
    return 1.0


FLV = random.Random(5)
FLICK = {f: FLV.choice([0.05, 0.2, 0.45]) for f in CFG["flick5"]}


def key_strength(material, base, level):
    sock = material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for f in range(1, N + 1):
        sock.default_value = base * level(f)
        sock.keyframe_insert("default_value", frame=f)


key_strength(TUBE, 4.0, interior)
key_strength(TUBE_FLICK, 4.0, lambda f: interior(f) * FLICK.get(f, 1.0))
key_strength(FRIDGE, 1.6, interior)
key_strength(NEON, 14.0, interior)
for name, base in (("Display blau", 4.0), ("Monitorbild", 1.6), ("Bildschirm", 2.0)):
    m_ = bpy.data.materials.get(name)
    if m_:
        key_strength(m_, base, interior)
canopy = lambda f: PROFIL_DACH if SHOT == "profil" else (0.04 if f in CFG["canopy_off"] else 1.0)  # noqa: E731
key_strength(CANOPY_L, 30.0, canopy)
key_strength(BAND, 5.0, canopy)
for f in range(1, N + 1):
    for i, L in LAMPS:
        L.data.energy = 38 * interior(f) * (FLICK.get(f, 1.0) if i == 5 else 1.0)
        L.data.keyframe_insert("energy", frame=f)
    nl.data.energy = 25 * interior(f)
    nl.data.keyframe_insert("energy", frame=f)
    for L in CANOPY_LIGHTS:
        L.data.energy = (380 if SHOT == "r2" else 1300) * canopy(f)
        L.data.keyframe_insert("energy", frame=f)
    fig_out.hide_render = not (SHOT == "r2" and f < CFG["fig_out"])
    fig_out.keyframe_insert("hide_render", frame=f)
    fig_door.hide_render = not ((SHOT == "r3" and CFG.get("jump") and f >= CFG["jump"]) or (SHOT == "profil" and "--puppe" in args))
    fig_door.keyframe_insert("hide_render", frame=f)
# Gestalt im Regen schwankt kaum merklich
for f in range(1, N + 1, 4):
    fig_out.rotation_euler = (0, math.radians(0.7 * math.sin(f * 0.37)), math.pi)
    fig_out.keyframe_insert("rotation_euler", frame=f)
NOTE.hide_render = SHOT != "note"
for o in NOTE.children:
    o.hide_render = SHOT != "note"

# ---------------------------------------------------------------- Profilbild: Tropfen auf der Glastür
if SHOT == "profil":
    import bmesh
    from mathutils import Matrix
    WATER = bpy.data.materials.new("Wassertropfen")
    WATER.use_nodes = True
    wb = WATER.node_tree.nodes["Principled BSDF"]
    wb.inputs["Base Color"].default_value = (1, 1, 1, 1)
    wb.inputs["Roughness"].default_value = 0.03
    wb.inputs["IOR"].default_value = 1.33
    wb.inputs["Transmission Weight" if "Transmission Weight" in wb.inputs else "Transmission"].default_value = 1.0
    me = bpy.data.meshes.new("Tropfen")
    bm = bmesh.new()
    rr = random.Random(23)
    for _ in range(520):
        r_ = rr.uniform(0.0015, 0.0045) * (1.6 if rr.random() < 0.08 else 1.0)
        streak = rr.uniform(1.0, 3.2) if rr.random() < 0.3 else rr.uniform(0.8, 1.25)
        x_, z_ = rr.uniform(-0.78, 0.78), rr.uniform(0.45, 2.55)
        mtx = Matrix.Translation((x_, D1 + 0.0035, z_)) @ Matrix.Diagonal((1.0, 0.4, streak, 1.0))
        bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=7, radius=r_, matrix=mtx)
    bm.to_mesh(me)
    # Gestalt fürs Profilbild: langer Umhang mit spitzer Kapuze (der runde Kopf der Folgen-Gestalt wirkt aus der Nähe wie eine Puppe)
    gx_, gy_ = _arg("--gx", 0.12), D1 + _arg("--gy", 0.2)
    M["cloth"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*([_arg("--stoff", 0.03)] * 3), 1)
    cl = [
        cone("Umhang", (gx_, gy_, 0.9), 0.42, 0.24, 1.8, M["cloth"], scale=(1.0, 0.62, 1.0)),
        sphere("Schultern", (gx_, gy_, 1.55), 0.26, M["cloth"], scale=(1.0, 0.62, 0.75)),
        cone("Kapuzenfall", (gx_, gy_ + 0.02, 1.73), 0.25, 0.15, 0.32, M["cloth"], scale=(1.0, 0.78, 1.0)),   # Stoff fällt von der Kapuze auf die Schultern
        sphere("Kapuze", (gx_, gy_ + 0.06, 1.97), 0.17, M["cloth"], scale=(1.0, 1.1, 1.15)),
        cone("Kapuzenspitze", (gx_, gy_ + 0.13, 2.1), 0.12, 0.03, 0.2, M["cloth"], rot=(math.radians(-35), 0, 0)),
        sphere("Gesicht", (gx_, gy_ - 0.08, 1.95), 0.105, mat("Leere", (0.0, 0.0, 0.0), 1.0), scale=(0.85, 0.5, 1.1)),
    ]
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.026, location=(gx_, gy_ - 0.12, 1.955), rotation=(math.radians(90), 0, 0))
    rim_ = bpy.context.object
    rim_.scale = (0.92, 1.18, 1.0)      # nach der Drehung: x breit, y (lokal) = Höhe
    rim_.data.materials.append(M["cloth"])
    bpy.ops.object.shade_smooth()
    cl.append(rim_)
    bpy.ops.object.select_all(action="DESELECT")
    for p_ in cl:
        p_.select_set(True)
    bpy.context.view_layer.objects.active = cl[0]
    bpy.ops.object.join()
    cloak = bpy.context.object
    sc.cursor.location = (gx_, gy_, 0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    # Stoff statt glatter Grundkörper: feiner unterteilen und leicht unregelmäßig verbeulen
    sub_ = cloak.modifiers.new("Unterteilung", "SUBSURF")
    sub_.levels = sub_.render_levels = 2
    tex_ = bpy.data.textures.new("Stofffalten", "CLOUDS")
    tex_.noise_scale = 0.14
    dis_ = cloak.modifiers.new("Falten", "DISPLACE")
    dis_.texture = tex_
    dis_.strength = _arg("--falten", 0.018)
    dis_.mid_level = 0.5
    eyes_ = []
    for dx in (-0.034, 0.034):
        e_ = sphere("Auge", (gx_ + dx, gy_ - 0.14, 1.975), 0.0062, EYESHINE, scale=(1.35, 1.0, 0.8))
        e_.parent = cloak
        e_.matrix_parent_inverse = cloak.matrix_world.inverted()
        eyes_.append(e_)
    cloak.rotation_euler = (0, math.radians(_arg("--tilt", -4.0)), 0)
    # ein Licht genau über der Gestalt (draußen, leicht dahinter): Kapuze und Schultern bekommen eine Kante, das Gesicht bleibt schwarz
    bpy.ops.object.light_add(type="SPOT", location=(gx_, gy_ + 0.3, 3.0))
    top_ = bpy.context.object
    top_.data.energy, top_.data.spot_size, top_.data.color = _arg("--oben", 45.0), math.radians(55), (0.85, 0.9, 1.0)
    top_.data.shadow_soft_size = 0.15
    for o_ in list(sc.objects):   # Fassaden-Strahler über dem Gehweg abschwächen (sie hellen sonst den Umhang von vorn auf)
        if o_.type == "LIGHT" and o_.data.type == "SPOT" and abs(o_.location.z - (H + 0.05)) < 0.01:
            o_.data.energy *= _arg("--fassade", 0.3)
    if bpy.data.objects.get("Ziehen"):
        bpy.data.objects["Ziehen"].hide_render = True   # „DRÜCKEN“ läge sonst mitten auf der Brust
    drops = bpy.data.objects.new("Tropfen", me)
    sc.collection.objects.link(drops)
    drops.data.materials.append(WATER)
    for poly in me.polygons:
        poly.use_smooth = True

# ---------------------------------------------------------------- Kamera
CAMS = {
    "cam01": ((3.55, -2.2, 2.75), (-0.2, 3.0, 0.95), 17),
    "cam03": ((2.0, 12.4, 3.9), (-0.5, 5.0, 1.45), 23),
    "note": ((3.6, 0.98, 1.47), (3.04, 0.99, 1.048), 40),
    # von innen frontal auf die Glastür: Türpfosten links/rechts, Gestalt als Umriss vor dem hellen Tankdach
    "profil": (lambda v: (tuple(v[0:3]), tuple(v[3:6]), v[6]))([float(x) for x in args[args.index("--cam") + 1].split(",")])
    if "--cam" in args else ((0.12, 1.3, 1.62), (0.12, D1 + 0.25, 1.9), 35),
}
cam_key = {"r1": "cam01", "r2": "cam03", "r3": "cam01", "note": "note", "profil": "profil"}[SHOT]
loc, tgt, lens = CAMS[cam_key]
bpy.ops.object.camera_add(location=loc)
cam = bpy.context.object
cam.data.lens = lens
cam.data.sensor_width = 36
cam.data.sensor_fit = "VERTICAL"
cam.rotation_euler = (Vector(tgt) - cam.location).to_track_quat("-Z", "Y").to_euler()
sc.camera = cam
if SHOT == "note":
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector(tgt) - cam.location).length
    cam.data.dof.aperture_fstop = 6.0
if SHOT == "profil":
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = (Vector((0.25, D1 + 0.2, 1.97)) - cam.location).length   # scharf auf die Kapuze
    cam.data.dof.aperture_fstop = _arg("--fstop", 4.0)
    EYESHINE.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = PROFIL_AUGEN

sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = {"note": 64, "profil": PROFIL_SAMPLES}.get(SHOT, 24)
sc.cycles.adaptive_threshold = 0.02
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.cycles.diffuse_bounces = 2
sc.cycles.glossy_bounces = 2
sc.cycles.transparent_max_bounces = 4
sc.cycles.blur_glossy = 1.0
sc.cycles.sample_clamp_indirect = 3.0
sc.render.use_persistent_data = True
sc.render.resolution_x, sc.render.resolution_y = {"note": (720, 1280), "profil": (PROFIL_RES, PROFIL_RES)}.get(SHOT, RES)
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, N
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "None"
sc.view_settings.exposure = -0.75 if SHOT == "r2" else -0.3
sp.hide_render = SHOT == "r2"
sc.render.image_settings.file_format = "PNG"

outdir = os.path.join(BUILD, SHOT)
os.makedirs(outdir, exist_ok=True)
if SHOT == "r2":
    from bpy_extras.object_utils import world_to_camera_view
    sc.frame_set(1)
    pr = world_to_camera_view(sc, cam, Vector((fig_out.location.x, fig_out.location.y, 1.45)))
    json.dump({"x": round(pr.x * RES[0], 1), "y": round((1 - pr.y) * RES[1], 1)}, open(os.path.join(outdir, "figure.json"), "w"))
if "--save" in args:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BUILD, f"{SHOT}.blend"))
if SHOT == "profil":
    sc.frame_set(1)
    sc.render.filepath = os.path.join(outdir, f"profil_{PROFIL_RES}.png")
    bpy.ops.render.render(write_still=True)
    print("Profilbild fertig:", sc.render.filepath)
elif SHOT == "note":
    sc.frame_set(1)
    sc.render.filepath = os.path.join(outdir, "zettel.png")
    bpy.ops.render.render(write_still=True)
    # Lage der Regeln im Bild (Pixel), für die Markierungen im Schnitt
    from bpy_extras.object_utils import world_to_camera_view
    dg = bpy.context.evaluated_depsgraph_get()
    W_, H_ = sc.render.resolution_x, sc.render.resolution_y
    boxes = {}
    for key, o in NOTE_PARTS.items():
        oe = o.evaluated_get(dg)
        pts = [world_to_camera_view(sc, cam, oe.matrix_world @ Vector(c)) for c in oe.bound_box]
        xs, ys = [p.x * W_ for p in pts], [(1 - p.y) * H_ for p in pts]
        boxes[key] = [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))]
    json.dump(boxes, open(os.path.join(outdir, "boxes.json"), "w"), indent=1)
    print("Zettel fertig:", boxes)
elif "--still" in args:
    for f in args[args.index("--still") + 1].split(","):
        sc.frame_set(int(f))
        sc.render.filepath = os.path.join(BUILD, f"still_{SHOT}_{int(f):04d}.png")
        bpy.ops.render.render(write_still=True)
elif "--frames" in args:
    rng_ = args[args.index("--frames") + 1]
    a, b = (1, N) if rng_ == "all" else (int(v) for v in rng_.split("-"))
    for f in range(a, b + 1):
        out = os.path.join(outdir, f"{f:04d}.png")
        if os.path.exists(out):
            continue
        sc.frame_set(f)
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
        print(f"{SHOT}: Bild {f}/{b} fertig", flush=True)

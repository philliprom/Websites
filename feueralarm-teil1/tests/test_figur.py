import math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy
import toon as T
from figur import figur

out = sys.argv[-1]
T.reset()
T.setup(res=(540, 960), aa="8", bg="#cfe3f2")
floor = T.mat("Boden", "#c9b79c"); wall = T.mat("Wand", "#efe6d2"); board = T.mat("Tafel", "#2f5b46")
desk = T.mat("Tisch", "#d8b98c"); metal = T.mat("Metall", "#6f7680"); chair = T.mat("Stuhl", "#3d6fb0")
T.box("boden", (12, 14, 0.1), floor, loc=(0, 4, -0.05), line=0)
T.box("wand_vorn", (12, 0.2, 3.2), wall, loc=(0, 6.2, 1.6), line=0.0)
T.box("tafel", (3.6, 0.06, 1.2), board, loc=(0, 6.08, 1.55), line=0.012)
def tisch(x, y):
    T.box(f"platte_{x}_{y}", (1.3, 0.55, 0.04), desk, loc=(x, y, 0.72), line=0.008, bevel=0.01)
    for dx in (-0.6, 0.6):
        for dy in (-0.22, 0.22):
            T.cylinder(f"bein_{x}_{y}_{dx}_{dy}", 0.018, 0.70, metal, loc=(x + dx, y + dy, 0.35), line=0.005, segs=10)
def stuhl(x, y, rot=0):
    e = T.empty(f"stuhl_{x}_{y}", (x, y, 0)); e.rotation_euler[2] = math.radians(rot)
    T.box(f"sitz_{x}_{y}", (0.42, 0.40, 0.03), chair, loc=(0, 0, 0.45), parent=e, line=0.007, bevel=0.01)
    T.box(f"lehne_{x}_{y}", (0.42, 0.03, 0.28), chair, loc=(0, 0.2, 0.72), parent=e, line=0.007, bevel=0.01)
    for dx in (-0.18, 0.18):
        for dy in (-0.17, 0.17):
            T.cylinder(f"sb_{x}_{y}_{dx}_{dy}", 0.012, 0.45, metal, loc=(dx, dy, 0.225), parent=e, line=0.004, segs=8)
tisch(0.3, 0.55); stuhl(0.62, 0.05); stuhl(0.0, 0.05)
tisch(0.3, 2.0); stuhl(0.0, 1.55); stuhl(0.62, 1.55)
t0 = time.time()
ben = figur("Ben", dict(skin="#f3cfb1", hair="#7a4a22", hair_style="stachel", top="#e8862f", top_style="hoodie",
                        pants="#33415c"), pose="sitzen", loc=(0.62, 0.05, 0), rot=180)
ben["kopf"].rotation_euler[2] = math.radians(-50)
ben["hals"].rotation_euler[2] = math.radians(-15)
ben["mund"].scale[2] = 1.4
ben["brauen"][0].rotation_euler[1] = math.radians(-14); ben["brauen"][1].rotation_euler[1] = math.radians(14)
lina = figur("Lina", dict(skin="#b07a55", hair="#1d1a1a", hair_style="zopf", top="#2a9d8f", top_style="jacke",
                          pants="#2b2d42", lashes=True), pose="sitzen", loc=(0.0, 1.55, 0), rot=180)
lina["torso"].rotation_euler[2] = math.radians(150)
lina["kopf"].rotation_euler[2] = math.radians(25)
sander = figur("Sander", dict(skin="#f5d9c6", hair="#5b2a1f", hair_style="dutt", top="#3a3d44", top_style="blazer",
                              pants="#2a2c31", shoes="#151515", h=1.1, glasses="#151515", lips="#a8484c", lashes=True),
               pose="stehen", loc=(-0.6, 4.6, 0), rot=0)
sander["schulter_r"].rotation_euler[0] = math.radians(-40); sander["ellbogen_r"].rotation_euler[0] = math.radians(-60)
print("Figuren gebaut", round(time.time() - t0, 1), "s,", len(bpy.data.objects), "Objekte")
cam = T.camera(loc=(0.0, -0.05, 1.12), lens=15)
T.look_at(cam, (0.25, 3.0, 1.05))
bpy.context.scene.render.filepath = out
t0 = time.time()
bpy.ops.render.render(write_still=True)
print("Render", round(time.time() - t0, 1), "s")

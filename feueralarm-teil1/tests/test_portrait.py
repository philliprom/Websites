import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C
out = sys.argv[-1]
T.reset(); sc = T.setup(res=(1600, 900), aa="FXAA", bg="#d9e6ef", shadow=0.35, light=(-0.5, -0.6, 0.65))
who = ["ben", "lina", "sander", "pohl"]
for i, w in enumerate(who):
    R = C.baue(w, w, loc=(-1.5 + i * 1.0, 0, 0), rot=-20)
    R["mund"].scale[2] = 1.0 if i % 2 else 0.32
    R["kopf"].rotation_euler[2] = math.radians(10)
cam = T.camera(loc=(0, -4.2, 1.55), lens=40); T.look_at(cam, (0, 0, 1.4))
sc.render.filepath = out; bpy.ops.render.render(write_still=True)

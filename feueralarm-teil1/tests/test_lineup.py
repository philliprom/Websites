import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C
out = sys.argv[-1]
T.reset(); sc = T.setup(res=(1080, 1080), aa="FXAA", bg="#d9e6ef", shadow=0.35, light=(-0.5, -0.6, 0.65))
T.box("boden", (14, 8, 0.1), T.mat("b", "#cdbfa8"), loc=(0, 2, -0.05), line=0)
who = ["ben", "lina", "sander", "pohl", "kid1", "kid2", "kid3", "kid4"]
for i, w in enumerate(who):
    R = C.baue(w, w, loc=(-3.15 + i * 0.9, 0, 0), rot=(0 if i % 2 == 0 else 25))
    R["mund"].scale[2] = 0.32 if i % 3 else 1.0
cam = T.camera(loc=(0, -4.6, 1.45), lens=30); T.look_at(cam, (0, 0, 1.0))
sc.render.filepath = out; bpy.ops.render.render(write_still=True)

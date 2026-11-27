import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C
out = sys.argv[-1]
T.reset(); sc = T.setup(res=(1200, 900), aa="FXAA", bg="#d9e6ef", shadow=0.3, light=(-0.5, -0.6, 0.65))
R = C.baue("Fahrer", "fahrer", loc=(-0.7, 0, 0), rot=-15)
R["mund"].scale[2] = 0.9
B = C.baue("Ben", "ben", loc=(0.8, 0, 0), rot=15)
cam = T.camera(loc=(0, -3.4, 1.55), lens=38); T.look_at(cam, (0, 0, 1.45))
sc.render.filepath = out; bpy.ops.render.render(write_still=True)

import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C, anim as AN
out = sys.argv[-1]
T.reset(); sc = T.setup(res=(1600, 700), aa="FXAA", bg="#d9e6ef", shadow=0.3, light=(-0.5, -0.6, 0.65))
poses = ["verschraenkt", "liste", "telefon", "bauch", "zeigen", "kabel", "greifen", "abwehr"]
for i, p in enumerate(poses):
    R = C.baue(f"s{i}", "sander", loc=(-3.5 + i * 1.0, 0, 0), rot=-25)
    for s, sx in (("l", 1), ("r", -1)):
        a = AN.ARM[p]
        R[f"schulter_{s}"].rotation_euler = (math.radians(a[0]), math.radians(-sx * a[1]), math.radians(sx * a[2]))
        R[f"ellbogen_{s}"].rotation_euler = (math.radians(a[3]), 0, 0)
cam = T.camera(loc=(0, -6.5, 1.5), lens=28); T.look_at(cam, (0, 0, 1.4))
sc.render.filepath = out; bpy.ops.render.render(write_still=True)

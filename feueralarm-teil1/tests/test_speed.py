import math, os, sys, time
sys.argv = sys.argv[:sys.argv.index("--")] + ["--"] + sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv
here = os.path.dirname(os.path.abspath(__file__))
aa, res, outdir = sys.argv[-3], int(sys.argv[-2]), sys.argv[-1]
sys.argv = [sys.argv[0], os.path.join(outdir, "dummy.png")]
exec(open(os.path.join(here, "test_figur.py")).read().split("cam = T.camera")[0])
import bpy, toon as T
sc = bpy.context.scene
sc.render.resolution_x, sc.render.resolution_y = res, res * 16 // 9
sc.display.render_aa = aa
cam = T.camera(loc=(0.0, -0.05, 1.12), lens=15); T.look_at(cam, (0.25, 3.0, 1.05))
sc.frame_start, sc.frame_end = 1, 6
for f in (1, 6):
    lina["kopf"].rotation_euler[2] = math.radians(25 if f == 1 else -10)
    lina["kopf"].keyframe_insert("rotation_euler", frame=f)
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = os.path.join(outdir, f"spd_{aa}_{res}_")
t0 = time.time()
bpy.ops.render.render(animation=True)
print("AA", aa, "RES", res, "per frame", round((time.time() - t0) / 6, 2), "s")

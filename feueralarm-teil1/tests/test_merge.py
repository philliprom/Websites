import math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_klasse.py")).read().split("cam = T.camera")[0])
t0 = time.time()
rigs = [ben, lina, sander]
for R in rigs:
    T.merge_rig(R)
for o in [o for o in bpy.data.objects if o.name.endswith("_root") and o.name.startswith("kid")]:
    T.merge_children(o, recursive=True)
T.merge_children(None, name="set_statisch")
print("Zusammengefasst", round(time.time() - t0, 1), "s", len(bpy.data.objects), "Objekte")
cam = T.camera(loc=(K.NOAH[0], K.NOAH[1] - 0.02, 1.16), lens=14); T.look_at(cam, (2.2, 5.5, 1.3))
sc.frame_start, sc.frame_end = 1, 4
for f in (1, 4):
    ben["kopf"].rotation_euler[2] = math.radians(0 if f == 1 else -40); ben["kopf"].keyframe_insert("rotation_euler", frame=f)
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out + "_merged_"
t1 = time.time(); bpy.ops.render.render(animation=True); print("pro Bild", round((time.time() - t1) / 4, 2), "s")

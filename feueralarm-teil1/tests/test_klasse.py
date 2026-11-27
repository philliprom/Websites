import math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C, set_klasse as K
out = sys.argv[-1]
t0 = time.time()
T.reset(); sc = T.setup(res=(540, 960), aa="FXAA", bg="#bcd9ee", shadow=0.32, light=(-0.75, -0.25, 0.62))
K.build()
ben = C.baue("Ben", "ben", pose="sitzen", loc=(K.BEN[0], K.BEN[1], 0), rot=180)
lina = C.baue("Lina", "lina", pose="sitzen", loc=(K.LINA[0], K.LINA[1], 0), rot=180)
sander = C.baue("Sander", "sander", pose="stehen", loc=(3.3, 4.4, 0), rot=60)
k = 0
for cx in K.COLS:
    for ry in K.ROWS:
        for sx in (-1, 1):
            x = cx + sx * K.SEAT_DX
            if (abs(x - K.NOAH[0]) < 0.01 and ry == K.NOAH[1]) or (abs(x - K.BEN[0]) < .01 and ry == K.BEN[1]) or (abs(x - K.LINA[0]) < .01 and ry == K.LINA[1]):
                continue
            k += 1
            if k in (3, 9, 14, 19):
                continue
            C.baue(f"kid{k}", f"kid{k}", pose="sitzen", loc=(x, ry, 0), rot=180, detail=False)
print("Aufbau", round(time.time() - t0, 1), "s", len(bpy.data.objects), "Objekte")
cam = T.camera(loc=(K.NOAH[0], K.NOAH[1] - 0.02, 1.16), lens=14)
views = {"vorn": (2.2, 5.5, 1.3), "ben": (-3.6, 0.6, 1.25), "fenster": None}
for v, tgt in views.items():
    if v == "fenster":
        cam.location = (-3.45, 0.1, 1.42); T.look_at(cam, (-14, 0.0, -5.2))
    else:
        cam.location = (K.NOAH[0], K.NOAH[1] - 0.02, 1.16); T.look_at(cam, tgt)
    sc.render.filepath = f"{out}_{v}.png"
    t1 = time.time(); bpy.ops.render.render(write_still=True); print(v, round(time.time() - t1, 1), "s")

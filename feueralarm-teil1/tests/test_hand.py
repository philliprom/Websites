import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C
out = sys.argv[-1]
T.reset(); sc = T.setup(res=(720, 1280), aa="FXAA", bg="#cfe3f2", shadow=0.3, light=(-0.75, -0.25, 0.62))
T.box("tisch", (1.3, 0.55, 0.035), T.mat("Tischplatte", "#dcc196"), loc=(0, 0.45, 0.73), line=0.007, bevel=0.008)
T.box("boden", (6, 6, 0.1), T.mat("Linoleum", "#b9ad97"), loc=(0, 1, -0.05), line=0)
T.box("stuhl", (0.42, 0.4, 0.03), T.mat("Stuhl", "#3d6fb0"), loc=(0, -0.05, 0.45), line=0.006)
cam = T.camera(loc=(0, -0.02, 1.2), lens=22)
H = C.pov_haende(cam, phone_tex=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "handy_r1.png"))
T.look_at(cam, (0.05, 0.55, 0.3))
for k, lens in enumerate((22, 17)):
    cam.data.lens = lens
    sc.render.filepath = f"{out}_{lens}.png"; bpy.ops.render.render(write_still=True)

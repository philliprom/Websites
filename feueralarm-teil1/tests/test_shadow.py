import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T
out = sys.argv[-1]
for i, light in enumerate(["MATCAP", "STUDIO", "FLAT"]):
    T.reset(); sc = T.setup(res=(360, 640), aa="FXAA", bg="#cfe3f2", shadow=0.6, light=(0.4, 0.3, 0.8))
    sc.display.shading.light = light
    T.box("boden", (6, 6, 0.1), T.mat("b", "#c9b79c"), loc=(0, 2, -0.05), line=0)
    T.ellipsoid("kugel", (0.6, 0.6, 0.6), T.mat("k", "#d04040"), loc=(0, 2, 0.6), line=0.01)
    T.box("kiste", (0.5, 0.5, 0.8), T.mat("c", "#4060d0"), loc=(1.0, 2.6, 0.4), line=0.01)
    cam = T.camera(loc=(0, -1.5, 1.6), lens=24); T.look_at(cam, (0.3, 2, 0.4))
    sc.render.filepath = f"{out}_{light}.png"; bpy.ops.render.render(write_still=True)

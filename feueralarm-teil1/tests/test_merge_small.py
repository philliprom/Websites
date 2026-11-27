import faulthandler, os, sys
faulthandler.enable()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy, toon as T, cast as C
T.reset(); T.setup(res=(200, 200), aa="FXAA")
T.box("a", (1, 1, 1), T.mat("x", "#ff0000"), loc=(0, 3, 0))
T.box("b", (1, 1, 1), T.mat("y", "#00ff00"), loc=(2, 3, 0))
print("merge static", flush=True)
o = T.merge_children(None, name="set")
print("ok", o.name, len(o.data.polygons), flush=True)
R = C.baue("Ben", "ben")
print("merge rig", flush=True)
T.merge_rig(R)
print("ok rig", len(bpy.data.objects), flush=True)

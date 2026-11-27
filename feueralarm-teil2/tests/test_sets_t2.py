import math, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bpy
base, out = sys.argv[-2], sys.argv[-1]
import toon as T, set_hof as H
views = {
    "hof": [((0.3, 1.2, 1.55), (3.2, 13.0, 1.0), 18), ((0.3, 1.2, 1.55), (14, 24, 3.0), 16)],
    "auto": [((H.SPUR_X + H.NOAH_AUGE[0], H.NOAH_AUGE[1], H.NOAH_AUGE[2]), (H.SPUR_X - 0.2, 10, 1.0), 17),
             ((H.SPUR_X + H.NOAH_AUGE[0], H.NOAH_AUGE[1], H.NOAH_AUGE[2]), (H.SPUR_X - 1.5, -0.45, 1.12), 16)],
}
for setname, vs in views.items():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(base, f"{setname}.blend"))
    names = json.load(open(os.path.join(base, f"{setname}.json")))
    T.setup(res=(540, 960), aa="FXAA", bg="#8c96a3", shadow=0.3, light=(-0.4, -0.5, 0.8))
    O = bpy.data.objects
    for nm, rn in names.items():
        if nm.startswith("_"):
            continue
        O[rn["root"]].location = (0, -80, -40)
    if setname == "auto":
        for o in O:
            if "_glas_" in o.name:
                o.hide_render = True
        O[names["Fahrer"]["root"]].location = (H.SPUR_X + H.FAHRER_SITZ[0], H.FAHRER_SITZ[1], 0.12)
        O[names["Fahrer"]["root"]].rotation_euler[2] = math.radians(180)
        O[names["Ben"]["root"]].location = (H.SPUR_X + H.BEN_SITZ[0], H.BEN_SITZ[1], 0.1)
        O[names["Ben"]["root"]].rotation_euler[2] = math.radians(180)
    else:
        O[names["Fahrer"]["root"]].location = (3.2 - 1.2, 12.2, 0)
        O[names["Fahrer"]["root"]].rotation_euler[2] = math.radians(180)
        O[names["Ben"]["root"]].location = (1.2, 2.0, 0)
        O[names["Ben"]["root"]].rotation_euler[2] = math.radians(200)
    O["pov_rig"].location = (0, -0.6, 0)
    cam = bpy.context.scene.camera
    for k, (p, t, lens) in enumerate(vs):
        cam.location = p; T.look_at(cam, t); cam.data.lens = lens
        bpy.context.scene.render.filepath = f"{out}_{setname}_{k}.png"
        bpy.ops.render.render(write_still=True)

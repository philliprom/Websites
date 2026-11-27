"""Besetzung: Aussehen aller Figuren, POV-Hände mit Handy."""
import math

import toon as T
from figur import figur, _hash

BEN = dict(skin="#f3cfb1", hair="#8a5426", hair_style="stachel", head=1.12, top="#ec8a2f", top_style="hoodie", pants="#34415e",
           brow="#5e3818", shoes="#f4f4f4")
LINA = dict(skin="#a8704c", hair="#1c1716", hair_style="lang", head=1.12, shoulder=0.44, width=0.94, top="#2a9d8f", top_style="jacke", shirt="#f6f1e7",
            pants="#2b2d42", lashes=True, brow="#1c1716", band="#f2c230", shoes="#fafafa")
SANDER = dict(skin="#f2d7c6", hair="#3b1a14", hair_style="bob", head=1.04, top="#34373e", top_style="blazer", pants="#2a2c31",
              shoes="#151515", sole="#151515", h=1.1, glasses="#141414", lips="#a3434a", lashes=True, brow="#4a1f15",
              head_w=0.93, width=0.92, shoulder=0.44)
POHL = dict(skin="#e8b998", hair="#b9b5ad", hair_style="grau", head=1.06, top="#35618f", top_style="arbeit", pants="#2e4058",
            shoes="#4a3424", sole="#2a1e14", h=1.08, brow="#9c978e", brow_h=1.5, beard="#aaa59c", cap="#24344d",
            width=1.12, mouth="#5d2a24")

KIDS_SKIN = ["#f3d2b6", "#e8b48f", "#c68a62", "#8d5a3b", "#f6d9c4", "#d7a27c", "#5e3a28"]
KIDS_HAIR = ["#2a1d16", "#6b4423", "#d4a55a", "#151212", "#8c3b1f", "#3d2b20", "#b78a4c"]
KIDS_TOP = ["#d94f4f", "#4f7fd9", "#5bbf72", "#9b6bd1", "#f0c64a", "#e07ab5", "#4ab3c4", "#e8e8e8", "#545b66",
            "#c96a3a"]
KIDS_STYLE = ["kurz", "stachel", "lang", "zopf", "locken", "kurz", "lang"]


def kid_spec(i):
    def pick(lst, k):
        return lst[int(_hash(f"kid{i}", k) * len(lst)) % len(lst)]
    st = pick(KIDS_STYLE, 3)
    return dict(skin=pick(KIDS_SKIN, 1), hair=pick(KIDS_HAIR, 2), hair_style=st, top=pick(KIDS_TOP, 4),
                top_style="hoodie" if _hash(f"kid{i}", 5) < 0.5 else "jacke", pants=pick(["#2d3443", "#3b4a6b", "#2f2f2f",
                                                                                         "#5a5040"], 6),
                lashes=st in ("lang", "zopf"), brow=pick(KIDS_HAIR, 2), band=pick(KIDS_TOP, 7), head=1.1)


def pov_haende(cam, phone_tex=None, line=0.004, sleeve="#27365c", skin="#efc4a2"):
    """Unterarme und Hände von Noah mit Handy, an der Kamera befestigt (Kamera-Raum: -Z nach vorn, Y nach oben)."""
    R = {}
    rig = T.empty("pov_rig", (0, 0, 0), cam)
    sl = T.mat("Noah_aermel", sleeve)
    sk = T.mat("Noah_haut", skin)
    # Handy vor der Kamera, unten Mitte
    hp = T.empty("pov_handy", (0.0, -0.075, -0.27), rig, rot=(-8, 0, 0))
    R["handy"] = hp
    body = T.mat("Handy", "#17181c")
    T.box("handy_koerper", (0.074, 0.152, 0.009), body, parent=hp, line=line, bevel=0.006)
    scr = T.mat("Handy_bild", "#0d1117", tex=phone_tex)
    T.plane("handy_bild", (0.068, 0.146), scr, loc=(0, 0, 0.0047), rot=(0, 0, 0), parent=hp)
    R["bild"] = scr
    for side, sx in (("l", -1), ("r", 1)):
        hd = T.empty(f"pov_hand_{side}", (sx * 0.040, -0.035, -0.012), hp)
        palm = T.ellipsoid(f"pov_handfl_{side}", (0.055, 0.085, 0.032), sk, parent=hd, line=line)
        palm.rotation_euler[1] = math.radians(sx * 20)
        th = T.ellipsoid(f"pov_daumen_{side}", (0.022, 0.055, 0.02), sk, loc=(-sx * 0.012, 0.035, 0.014), parent=hd,
                         line=line)
        th.rotation_euler = (math.radians(10), 0, math.radians(sx * 25))
        for k in range(3):
            f = T.ellipsoid(f"pov_finger_{side}_{k}", (0.02, 0.05, 0.018), sk,
                            loc=(sx * 0.005, 0.03 - k * 0.022, -0.004), parent=hd, line=line * 0.8)
            f.rotation_euler[2] = math.radians(sx * 70)
            f.location.x += sx * 0.02
        arm = T.capsule(f"pov_unterarm_{side}", 0.035, 0.22, sl, loc=(sx * 0.02, -0.06, -0.02), parent=hd, line=line,
                        axis="Y")
        arm.rotation_euler = (math.radians(-30), math.radians(-sx * 15), 0)
        R[f"hand_{side}"] = hd
    return R


def baue(name, which, pose="stehen", loc=(0, 0, 0), rot=0.0, detail=True, line=0.0065):
    spec = {"ben": BEN, "lina": LINA, "sander": SANDER, "pohl": POHL}.get(which)
    if spec is None:
        spec = kid_spec(int(which.replace("kid", "")))
    return figur(name, spec, pose=pose, loc=loc, rot=rot, detail=detail, line=line)

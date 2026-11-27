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


def _glied(name, p0, p1, r, mat, parent, line, r2=None):
    """Kapsel von p0 nach p1 (im Raum des Elternteils)."""
    from mathutils import Vector
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    e = T.empty(f"{name}_achse", tuple(p0), parent)
    e.rotation_mode = "QUATERNION"
    e.rotation_quaternion = d.normalized().to_track_quat("-Z", "Y")
    T.capsule(name, r, d.length, mat, parent=e, line=line, r2=r2, segs=16)
    return e


def pov_haende(cam, phone_tex=None, line=0.0022, sleeve="#27365c", skin="#efc4a2"):
    """Noahs rechte Hand hält das Handy (wie im Vorbild): Handfläche hinter dem Gerät, Daumen am rechten Rand,
    Fingerspitzen links um die Kante, Ärmel kommt von unten rechts ins Bild. Bildschirm bleibt frei.
    Kamera-Raum: -Z nach vorn, Y nach oben, X nach rechts."""
    R = {}
    rig = T.empty("pov_rig", (0, 0, 0), cam)
    sl = T.mat("Noah_aermel", sleeve)
    sk = T.mat("Noah_haut", skin)
    hp = T.empty("pov_handy", (0.0, -0.058, -0.25), rig, rot=(-6, 0, 0))
    R["handy"] = hp
    body = T.mat("Handy", "#17181c")
    T.box("handy_koerper", (0.074, 0.152, 0.009), body, parent=hp, line=line, bevel=0.006)
    scr = T.mat("Handy_bild", "#0d1117", tex=phone_tex)
    T.plane("handy_bild", (0.067, 0.145), scr, loc=(0, 0, 0.0047), rot=(0, 0, 0), parent=hp)
    R["bild"] = scr
    hd = T.empty("pov_hand_r", (0.0, 0.0, 0.0), hp)
    # Handfläche hinter dem Gerät (unten rechts), Ballen schaut rechts hervor
    T.ellipsoid("pov_handfl", (0.078, 0.10, 0.032), sk, loc=(0.016, -0.04, -0.021), parent=hd, line=line)
    T.ellipsoid("pov_ballen", (0.03, 0.05, 0.028), sk, loc=(0.042, -0.052, -0.006), parent=hd, line=line)
    # Daumen vorn am rechten Rand, nach oben-innen
    _glied("pov_daumen_grund", (0.046, -0.062, -0.002), (0.043, -0.03, 0.006), 0.0115, sk, hd, line)
    _glied("pov_daumen_spitze", (0.043, -0.03, 0.006), (0.034, -0.006, 0.008), 0.0105, sk, hd, line, r2=0.0095)
    # Fingerspitzen links um die Kante
    for k, y in enumerate((-0.058, -0.037, -0.016, 0.004)):
        ln = 0.011 if k in (1, 2) else 0.008
        _glied(f"pov_finger_{k}", (-0.045, y, -0.006), (-0.045 + ln, y + 0.002, 0.002), 0.0074, sk, hd, line,
               r2=0.0068)
        _glied(f"pov_fingerruecken_{k}", (-0.02, y - 0.003, -0.012), (-0.047, y, -0.006), 0.0085, sk, hd, line)
    # Handgelenk und Ärmel nach unten rechts aus dem Bild
    _glied("pov_gelenk", (0.028, -0.085, -0.024), (0.07, -0.16, -0.05), 0.026, sk, hd, line, r2=0.028)
    _glied("pov_aermel", (0.06, -0.14, -0.045), (0.16, -0.36, -0.1), 0.036, sl, hd, line, r2=0.042)
    R["hand_r"] = hd
    return R


def baue(name, which, pose="stehen", loc=(0, 0, 0), rot=0.0, detail=True, line=0.0065):
    spec = {"ben": BEN, "lina": LINA, "sander": SANDER, "pohl": POHL}.get(which)
    if spec is None:
        spec = kid_spec(int(which.replace("kid", "")))
    return figur(name, spec, pose=pose, loc=loc, rot=rot, detail=detail, line=line)

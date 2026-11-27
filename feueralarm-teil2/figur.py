"""Toon-Figuren aus einfachen Formen: großer Kopf, große Augen, Gelenk-Puppe (starre Teile an Drehpunkten).

figur(name, spec, pose) baut die Figur mit Blick nach -Y und gibt ein Dict mit allen Drehpunkten zurück,
die animiert werden (kopf, hals, torso, arme, beine, mund, augen, brauen).
"""
import math

from mathutils import Vector

import toon as T


def _hash(name, k):
    h = 2166136261
    for ch in f"{name}:{k}":
        h = (h ^ ord(ch)) * 16777619 & 0xFFFFFFFF
    return (h % 10000) / 10000.0


def smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


SPEC_DEFAULT = dict(
    skin="#f1c7a5", hair="#4a3426", hair_style="kurz", top="#3b5ba5", top_style="hoodie", pants="#2d3443",
    shoes="#f2f2f2", h=1.0, head=1.0, brow="#3a2a20", eyes="#1b1b1b", glasses=None, beard=None, mouth="#6b2a2a",
    width=1.0, cap=None, lips=None, lashes=False, sole="#d9d9d9",
)


def figur(name, spec=None, pose="stehen", loc=(0, 0, 0), rot=0.0, line=0.0065, detail=True):
    s = dict(SPEC_DEFAULT)
    s.update(spec or {})
    h = s["h"]
    W = s["width"]
    M = {k: T.mat(f"{name}_{k}", s[k]) for k in ("skin", "hair", "top", "pants", "shoes", "brow", "eyes", "mouth", "sole")}
    white = T.mat("Augenweiss", "#fbfbf8")
    R = {}
    root = T.empty(f"{name}_root", loc)
    root.rotation_euler[2] = math.radians(rot)
    R["root"] = root
    sit = pose == "sitzen"
    hip_z = (0.50 if sit else 0.86) * h
    becken = T.empty(f"{name}_becken", (0, 0, hip_z), root)
    R["becken"] = becken

    # ---------------- Beine
    for side, sx in (("l", 1), ("r", -1)):
        hj = T.empty(f"{name}_huefte_{side}", (sx * 0.095 * W, 0, -0.03), becken)
        T.capsule(f"{name}_ober_{side}", 0.078 * W, 0.36 * h, M["pants"], parent=hj, line=line)
        knie = T.empty(f"{name}_knie_{side}", (0, 0, -0.40 * h), hj)
        T.capsule(f"{name}_unter_{side}", 0.066 * W, 0.34 * h, M["pants"], parent=knie, line=line, r2=0.06 * W)
        fuss = T.empty(f"{name}_fuss_{side}", (0, 0, -0.39 * h), knie)
        T.ellipsoid(f"{name}_schuh_{side}", (0.115, 0.25, 0.10), M["shoes"], loc=(0, -0.05, -0.02), parent=fuss, line=line)
        if detail:
            T.ellipsoid(f"{name}_sohle_{side}", (0.12, 0.255, 0.04), M["sole"], loc=(0, -0.05, -0.055), parent=fuss,
                        line=line * 0.8)
        if sit:
            hj.rotation_euler[0] = math.radians(-88)
            knie.rotation_euler[0] = math.radians(88)
        R[f"huefte_{side}"] = hj
        R[f"knie_{side}"] = knie

    # ---------------- Rumpf
    T.ellipsoid(f"{name}_hose", (0.36 * W, 0.24, 0.24), M["pants"], loc=(0, 0, 0.0), parent=becken, line=line)
    torso = T.empty(f"{name}_torso", (0, 0, 0.02), becken)
    R["torso"] = torso
    style = s["top_style"]
    T.ellipsoid(f"{name}_rumpf", (0.43 * W, 0.26, 0.64 * h), M["top"], loc=(0, 0, 0.27 * h), parent=torso, line=line,
                cut=None)
    # Schultern runder
    T.ellipsoid(f"{name}_schultern", (s.get("shoulder", 0.50) * W, 0.25, 0.20), M["top"], loc=(0, 0, 0.47 * h), parent=torso, line=line)
    if style == "hoodie":
        T.ellipsoid(f"{name}_kapuze", (0.30, 0.16, 0.16), M["top"], loc=(0, 0.11, 0.57 * h), parent=torso, line=line)
        if detail:
            dark = T.mat(f"{name}_top_dunkel", _shade(s["top"], 0.82))
            T.box(f"{name}_tasche", (0.26 * W, 0.03, 0.12), dark, loc=(0, -0.122, 0.12 * h), parent=torso, line=line * 0.7,
                  bevel=0.01)
            band = T.mat("Kordel", "#f4f1ea")
            for sx in (1, -1):
                T.cylinder(f"{name}_kordel_{sx}", 0.006, 0.13, band, loc=(sx * 0.04, -0.128, 0.40 * h), parent=torso,
                           line=0.0, segs=8)
    elif style == "blazer":
        bl = T.mat("Bluse", "#f5f3ee")
        T.ellipsoid(f"{name}_bluse", (0.13, 0.06, 0.22), bl, loc=(0, -0.11, 0.47 * h), parent=torso, line=line * 0.8)
        lap = T.mat(f"{name}_revers", _shade(s["top"], 0.75))
        for sx in (1, -1):
            o = T.box(f"{name}_revers_{sx}", (0.07, 0.02, 0.22), lap, loc=(sx * 0.07, -0.125, 0.43 * h), parent=torso,
                      line=line * 0.7, bevel=0.008)
            o.rotation_euler[1] = math.radians(-sx * 18)
        btn = T.mat("Knopf", "#202020")
        for k in range(2):
            T.ellipsoid(f"{name}_knopf_{k}", (0.022, 0.012, 0.022), btn, loc=(0, -0.13, (0.25 - 0.1 * k) * h),
                        parent=torso, line=0)
    elif style == "jacke":
        inner = T.mat(f"{name}_shirt", s.get("shirt", "#f2efe8"))
        T.ellipsoid(f"{name}_kragen", (0.20, 0.17, 0.08), T.mat(f"{name}_kragenfarbe", _shade(s["top"], 0.88)),
                    loc=(0, 0.0, 0.565 * h), parent=torso, line=line * 0.8)
        zip_m = T.mat("Reissverschluss", "#d9d9d9")
        T.cylinder(f"{name}_zip", 0.0055, 0.46 * h, zip_m, loc=(0, -0.127, 0.29 * h), parent=torso, line=0, segs=6)
    elif style == "arbeit":
        stripe = T.mat("Reflex", "#d8d8c8")
        T.cylinder(f"{name}_reflex", 0.222 * W, 0.04, stripe, loc=(0, 0, 0.12 * h), parent=torso, line=line * 0.7, segs=32)
        pock = T.mat(f"{name}_tasche", _shade(s["top"], 0.85))
        for sx in (1, -1):
            T.box(f"{name}_brusttasche_{sx}", (0.10, 0.02, 0.09), pock, loc=(sx * 0.09, -0.125, 0.38 * h), parent=torso,
                  line=line * 0.7, bevel=0.008)
        pen = T.mat("Stift", "#e2b21c")
        T.cylinder(f"{name}_stift", 0.006, 0.07, pen, loc=(0.11, -0.13, 0.43 * h), parent=torso, line=0, segs=8)
        T.box(f"{name}_guertel", (0.37 * W, 0.25, 0.05), T.mat("Guertel", "#3a2a1e"), loc=(0, 0, 0.02), parent=becken,
              line=line * 0.7, bevel=0.01)

    # ---------------- Arme
    for side, sx in (("l", 1), ("r", -1)):
        sh = T.empty(f"{name}_schulter_{side}", (sx * 0.225 * W, 0, 0.47 * h), torso)
        T.capsule(f"{name}_oberarm_{side}", 0.062, 0.24 * h, M["top"], parent=sh, line=line)
        el = T.empty(f"{name}_ellbogen_{side}", (0, 0, -0.27 * h), sh)
        T.capsule(f"{name}_unterarm_{side}", 0.056, 0.20 * h, M["top"], parent=el, line=line, r2=0.05)
        hd = T.empty(f"{name}_hand_{side}", (0, 0, -0.25 * h), el)
        T.ellipsoid(f"{name}_handfl_{side}", (0.055, 0.085, 0.10), M["skin"], loc=(0, 0, -0.04), parent=hd, line=line)
        th = T.ellipsoid(f"{name}_daumen_{side}", (0.03, 0.03, 0.06), M["skin"], loc=(0, -0.04, -0.02), parent=hd,
                         line=line)
        th.rotation_euler[0] = math.radians(25)
        sh.rotation_euler[1] = math.radians(sx * 8)  # Arme leicht vom Körper weg
        sh.rotation_euler[0] = math.radians(-6)
        el.rotation_euler[0] = math.radians(-14)
        if sit:
            sh.rotation_euler[0] = math.radians(-30)
            el.rotation_euler[0] = math.radians(-55)
        R[f"schulter_{side}"] = sh
        R[f"ellbogen_{side}"] = el
        R[f"hand_{side}"] = hd

    # ---------------- Hals und Kopf
    hals = T.empty(f"{name}_hals", (0, 0.0, 0.55 * h), torso)
    R["hals"] = hals
    T.cylinder(f"{name}_halsform", 0.064, 0.11, M["skin"], loc=(0, 0.005, 0.03), parent=hals, line=line, segs=16)
    kopf = T.empty(f"{name}_kopf", (0, 0, 0.05), hals)
    R["kopf"] = kopf
    hs = s["head"]
    HW, HD, HH = 0.27 * hs * s.get("head_w", 1.0), 0.265 * hs, 0.31 * hs
    cz = 0.15 * hs
    T.ellipsoid(f"{name}_kopfform", (HW, HD, HH), M["skin"], loc=(0, 0, cz), parent=kopf, line=line * 1.1)
    # Kinn/Kiefer etwas schmaler: zweite Form unten
    T.ellipsoid(f"{name}_kiefer", (HW * 0.82, HD * 0.85, HH * 0.55), M["skin"], loc=(0, -0.01, cz - HH * 0.22),
                parent=kopf, line=line * 1.1)
    for sx in (1, -1):
        T.ellipsoid(f"{name}_ohr_{sx}", (0.035, 0.05, 0.075), M["skin"], loc=(sx * HW * 0.5, 0.0, cz - 0.005), parent=kopf,
                    line=line)
    # Augen
    R["augen"], R["pupillen"], R["brauen"] = [], [], []
    ey = -HD * 0.43
    for side, sx in (("l", 1), ("r", -1)):
        ep = T.empty(f"{name}_auge_{side}", (sx * 0.055 * hs, ey, cz + 0.018 * hs), kopf)
        T.ellipsoid(f"{name}_augapfel_{side}", (0.066 * hs, 0.035, 0.084 * hs), white, parent=ep, line=line * 0.8)
        pp = T.empty(f"{name}_pupille_{side}", (0, -0.016, -0.004), ep)
        T.ellipsoid(f"{name}_pupillenform_{side}", (0.034 * hs, 0.016, 0.044 * hs), M["eyes"], parent=pp, line=0)
        T.ellipsoid(f"{name}_glanz_{side}", (0.012, 0.008, 0.012), white, loc=(-0.008 * hs, -0.007, 0.011 * hs), parent=pp,
                    line=0, segs=10, rings=6)
        R["augen"].append(ep)
        R["pupillen"].append(pp)
        bp = T.empty(f"{name}_braue_{side}", (sx * 0.058 * hs, ey - 0.008, cz + 0.074 * hs), kopf)
        T.box(f"{name}_braueform_{side}", (0.07 * hs, 0.02, 0.021 * s.get("brow_h", 1.0)), M["brow"], parent=bp, line=0,
              bevel=0.008)
        R["brauen"].append(bp)
        if s["lashes"]:
            lash = T.box(f"{name}_wimper_{side}", (0.03, 0.012, 0.008), M["brow"], loc=(sx * 0.03 * hs, 0.0, 0.035 * hs),
                         parent=ep, line=0, bevel=0.003)
            lash.rotation_euler[1] = math.radians(-sx * 30)
    # Nase, Mund
    T.ellipsoid(f"{name}_nase", (0.036 * hs, 0.04, 0.046 * hs), M["skin"], loc=(0, -HD * 0.5, cz - 0.028 * hs), parent=kopf,
                line=line * 0.8)
    mund = T.empty(f"{name}_mund", (0, -HD * (0.5 if s.get("vollbart") else 0.455), cz - 0.078 * hs), kopf)
    T.ellipsoid(f"{name}_mundform", (0.074 * hs, 0.032, 0.03 * hs), M["mouth"], parent=mund, line=line * 0.6)
    mund.scale = (1, 1, 0.32)
    R["mund"] = mund
    if s["lips"]:
        T.ellipsoid(f"{name}_lippen", (0.066 * hs, 0.024, 0.014 * hs), T.mat(f"{name}_lip", s["lips"]),
                    loc=(0, -HD * 0.46, cz - 0.07 * hs), parent=kopf, line=0)

    # ---------------- Haare
    _hair(name, s, M, kopf, HW, HD, HH, cz, line)
    if s["glasses"]:
        gm = T.mat(f"{name}_brille", s["glasses"])
        for sx in (1, -1):
            ring = T.torus(f"{name}_glas_{sx}", 0.045 * hs, 0.0055, gm, loc=(sx * 0.058 * hs, ey - 0.032, cz + 0.016 * hs),
                           parent=kopf, line=0)
            ring.scale = (1, 1, 0.80)
            arm = T.box(f"{name}_buegel_{sx}", (0.006, 0.13, 0.006), gm, loc=(sx * 0.103 * hs, ey + 0.035, cz + 0.022 * hs),
                        parent=kopf, line=0)
        T.box(f"{name}_steg", (0.03, 0.007, 0.007), gm, loc=(0, ey - 0.036, cz + 0.024 * hs), parent=kopf, line=0)
        if s.get("lenses"):  # Sonnenbrille: dunkle Gläser verdecken die Augen
            lm = T.mat(f"{name}_glaeser", s["lenses"])
            for sx in (1, -1):
                g = T.ellipsoid(f"{name}_sonnenglas_{sx}", (0.094 * hs, 0.012, 0.074 * hs), lm,
                                loc=(sx * 0.058 * hs, ey - 0.031, cz + 0.016 * hs), parent=kopf, line=line * 0.5)
    if s.get("vollbart"):  # Vollbart um Kinn und Wangen, Mund liegt davor
        vb = T.mat(f"{name}_vollbart", s["vollbart"])
        T.ellipsoid(f"{name}_vollbartform", (HW * 0.9, HD * 0.86, HH * 0.5), vb, loc=(0, -0.012, cz - HH * 0.25),
                    parent=kopf, line=line, cut=lambda v: v.z > HH * 0.1)
        T.ellipsoid(f"{name}_oberlippenbart", (0.1 * hs, 0.035, 0.026 * hs), vb, loc=(0, -HD * 0.47, cz - 0.05 * hs),
                    parent=kopf, line=line * 0.7)
    if s["beard"]:
        bm_ = T.mat(f"{name}_bart", s["beard"])
        T.ellipsoid(f"{name}_schnurrbart", (0.11 * hs, 0.04, 0.03 * hs), bm_, loc=(0, -HD * 0.47, cz - 0.052 * hs),
                    parent=kopf, line=line * 0.7)
    return R


def _shade(hexc, f):
    c = hexc.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def _hair(name, s, M, kopf, HW, HD, HH, cz, line):
    st = s["hair_style"]
    hm = M["hair"]
    if st == "glatze":
        return
    front = {"kurz": 0.42, "stachel": 0.40, "zopf": 0.34, "dutt": 0.40, "grau": 0.50, "lang": 0.34,
             "locken": 0.30, "bob": 0.36}.get(st, 0.4)
    back = {"lang": -0.95, "zopf": -0.55, "locken": -0.7, "grau": -0.45, "bob": -0.7}.get(st, -0.6)
    sx_, sy_, sz_ = HW * 1.05, HD * 1.07, HH * 1.07

    fdeg = {"kurz": 62, "stachel": 64, "zopf": 68, "dutt": 64, "grau": 58, "lang": 68, "locken": 72, "bob": 66}.get(st, 64)
    bdeg = {"lang": 150, "zopf": 125, "locken": 132, "grau": 112, "bob": 132}.get(st, 122)

    def theta_max(phi):
        # phi=-90 vorn, 90 hinten, 0/180 Seiten; Schläfen etwas tiefer, Nacken tief
        t = (math.sin(math.radians(phi)) + 1) / 2          # 0 vorn … 1 hinten
        base = fdeg + (bdeg - fdeg) * smoothstep(0.15, 0.85, t)
        side = abs(math.cos(math.radians(phi)))
        return base + 14 * side * (1 - smoothstep(0.35, 0.75, t))
    T.cap(f"{name}_haarkappe", (sx_, sy_, sz_), hm, theta_max, loc=(0, 0.008, cz + 0.016), parent=kopf, line=line)
    if st == "stachel":
        for k in range(10):
            a = (k / 10) * 2 * math.pi + 0.3
            r = 0.05 + 0.04 * _hash(name, k)
            x, y = math.cos(a) * r, math.sin(a) * r * 0.9 + 0.015
            o = T.ellipsoid(f"{name}_straehne_{k}", (0.075, 0.075, 0.12 + 0.05 * _hash(name, k + 20)), hm,
                            loc=(x, y, cz + HH * 0.44), parent=kopf, line=line, segs=12, rings=8)
            o.rotation_euler = (math.radians(-y * 300 - 15), math.radians(x * 300), 0)
        for k, x in enumerate((-0.07, -0.02, 0.035, 0.08)):
            o = T.ellipsoid(f"{name}_ponyspitze_{k}", (0.06, 0.05, 0.11), hm, loc=(x, -HD * 0.40, cz + HH * 0.34),
                            parent=kopf, line=line, segs=12, rings=8)
            o.rotation_euler = (math.radians(-35), math.radians(-20 + 12 * k), 0)
    elif st == "kurz":
        for k, (x, ang) in enumerate(((-0.06, 20), (0.0, 5), (0.06, -10))):
            o = T.ellipsoid(f"{name}_pony_{k}", (0.11, 0.06, 0.08), hm, loc=(x, -HD * 0.40, cz + HH * 0.36), parent=kopf,
                            line=line, segs=16, rings=8)
            o.rotation_euler = (math.radians(-20), math.radians(ang), 0)
    elif st == "locken":
        for k in range(16):
            a = (k / 16) * 2 * math.pi
            x = math.cos(a) * HW * 0.46
            y = math.sin(a) * HD * 0.46 + 0.02
            z = cz + HH * (0.28 + 0.12 * _hash(name, k))
            T.ellipsoid(f"{name}_locke_{k}", (0.095, 0.095, 0.095), hm, loc=(x, y, z), parent=kopf, line=line, segs=12,
                        rings=8)
        T.ellipsoid(f"{name}_lockentop", (HW * 0.9, HD * 0.9, 0.13), hm, loc=(0, 0.01, cz + HH * 0.46), parent=kopf,
                    line=line)
    elif st == "zopf":
        o = T.ellipsoid(f"{name}_pony", (HW * 0.70, 0.045, 0.085), hm, loc=(0.035, -HD * 0.395, cz + HH * 0.335),
                        parent=kopf, line=line)
        o.rotation_euler = (math.radians(-18), math.radians(-16), 0)
        band = T.mat("Haargummi", s.get("band", "#e04848"))
        piv = T.empty(f"{name}_zopfpunkt", (0, HD * 0.50, cz + HH * 0.28), kopf)
        T.ellipsoid(f"{name}_gummi", (0.055, 0.05, 0.05), band, parent=piv, line=line * 0.8)
        z1 = T.ellipsoid(f"{name}_zopf", (0.10, 0.11, 0.30), hm, loc=(0, 0.07, -0.12), parent=piv, line=line)
        z1.rotation_euler[0] = math.radians(22)
        T.ellipsoid(f"{name}_zopfspitze", (0.07, 0.07, 0.14), hm, loc=(0, 0.11, -0.27), parent=piv, line=line)
    elif st == "dutt":
        T.ellipsoid(f"{name}_dutt", (0.14, 0.13, 0.13), hm, loc=(0, HD * 0.40, cz + HH * 0.36), parent=kopf, line=line)
        T.ellipsoid(f"{name}_seitenscheitel", (HW * 0.55, HD * 0.55, 0.06), hm, loc=(0.05, -HD * 0.22, cz + HH * 0.42),
                    parent=kopf, line=line * 0.7, rot=("Y", -14))
    elif st == "lang":
        T.ellipsoid(f"{name}_langhaar", (HW * 1.14, HD * 0.72, HH * 1.30), hm, loc=(0, HD * 0.26, cz - HH * 0.34),
                    parent=kopf, line=line)
        o = T.ellipsoid(f"{name}_pony", (HW * 0.70, 0.045, 0.085), hm, loc=(-0.03, -HD * 0.395, cz + HH * 0.335),
                        parent=kopf, line=line)
        o.rotation_euler = (math.radians(-18), math.radians(16), 0)
    elif st == "bob":
        for sx in (1, -1):
            o = T.ellipsoid(f"{name}_bobseite_{sx}", (HW * 0.30, HD * 0.85, HH * 0.80), hm,
                            loc=(sx * HW * 0.43, 0.012, cz - HH * 0.16), parent=kopf, line=line)
            o.rotation_euler[1] = math.radians(sx * 6)
        T.ellipsoid(f"{name}_bobhinten", (HW * 1.06, HD * 0.55, HH * 0.78), hm, loc=(0, HD * 0.28, cz - HH * 0.14),
                    parent=kopf, line=line)
        o = T.ellipsoid(f"{name}_bobpony", (HW * 0.78, 0.05, 0.10), hm, loc=(-0.035, -HD * 0.395, cz + HH * 0.335),
                        parent=kopf, line=line)
        o.rotation_euler = (math.radians(-10), math.radians(22), 0)
    elif st == "grau":
        for sx in (1, -1):
            T.ellipsoid(f"{name}_koteletten_{sx}", (0.03, 0.06, 0.09), hm, loc=(sx * HW * 0.49, -0.02, cz - 0.0),
                        parent=kopf, line=line * 0.7)
    if s["cap"]:
        cm = T.mat(f"{name}_muetze", s["cap"])
        T.ellipsoid(f"{name}_muetzenform", (HW * 1.10, HD * 1.12, HH * 0.80), cm, loc=(0, 0.004, cz + HH * 0.22),
                    parent=kopf, line=line, cut=lambda v: v.z < -0.01)
        o = T.box(f"{name}_schirm", (HW * 0.78, 0.14, 0.018), cm, loc=(0, -HD * 0.60, cz + HH * 0.235), parent=kopf,
                  line=line, bevel=0.007)
        o.rotation_euler[0] = math.radians(-8)

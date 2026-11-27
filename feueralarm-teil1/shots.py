"""Einstellungen (Kamera, Figuren, Gesten) für DER FEUERALARM · Teil 1.

Jede Einstellung: (id, set, start-Ausdruck, Funktion). Das Ende ist der Start der nächsten Einstellung.
Zeiten kommen aus timeline.json: S('l05') = Beginn, E('l05') = Ende einer Zeile.
"""
import math

from mathutils import Vector

import set_klasse as K

NOAH = Vector(K.NOAH_EYE)
BEN_SITZ = (K.BEN[0], K.BEN[1], 0)
LINA_SITZ = (K.LINA[0], K.LINA[1], 0)
BEN_KOPF = Vector((K.BEN[0], K.BEN[1], 1.31))
LINA_KOPF = Vector((K.LINA[0], K.LINA[1], 1.31))
TUER = Vector((3.95, 4.45, 1.15))
VORB = Vector((-3.0, 5.98, 1.0))
SPRECHER = Vector(K.LAUTSPRECHER)
REGLER = Vector((K.LAUTSPRECHER[0] + 0.5, K.LAUTSPRECHER[1], 2.0))


def heading(frm, to):
    """Drehwinkel (Grad), damit eine Figur bei frm nach to schaut (Figuren schauen lokal nach -Y)."""
    d = Vector(to) - Vector(frm)
    return math.degrees(math.atan2(d.x, -d.y))


SHOTS = []


def shot(sid, set_, start):
    def deco(fn):
        SHOTS.append(dict(id=sid, set=set_, start=start, fn=fn))
        return fn
    return deco


# ============================================================ KLASSENZIMMER
@shot("01_abschliessen", "klasse", lambda c: 0.0)
def s01(c):
    ben, sander = c.a["Ben"], c.a["Sander"]
    ben.place(BEN_SITZ, 180)
    sander.place((3.45, 4.42, 0), 90)
    sander.arm(0, "r", "schluessel", 0.01)
    sander.arm(0, "l", "stehen", 0.01)
    sander.look(0, TUER + Vector((0.0, 0.0, -0.2)), 0.01)
    t_pan = c.S("l01") + 0.85
    sander.look(t_pan + 0.2, "cam", 0.5)
    ben.look(0, TUER, 0.01)
    ben.look(t_pan - 0.1, "cam", 0.35)
    ben.brow(0, "schreck", 0.01)
    ben.bend(0, (6, -18), 0.01)
    ben.say(c.S("l01"), c.env("l01"))
    c.pov.at(0, pos=NOAH, target=(3.35, 4.42, 1.38), dur=0.01, lens=46)
    c.pov.at(t_pan, target=BEN_KOPF + Vector((0.12, 0.05, -0.08)), dur=0.38, lens=16)
    c.phone(None)


@shot("02_uebung", "klasse", lambda c: c.S("l02") - 0.15)
def s02(c):
    sander, ben, lina = c.a["Sander"], c.a["Ben"], c.a["Lina"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    p0 = (3.35, 4.4, 0)
    sander.place(p0, heading(p0, NOAH))
    sander.look(c.t0, "cam", 0.01)
    sander.arm(c.t0, "r", "huefte", 0.5)
    sander.move(c.t0 + 0.4, c.t0 + 2.2, (2.55, 4.25, 0), walk=True, rot=heading((2.55, 4.25, 0), NOAH))
    sander.say(c.S("l02"), c.env("l02"))
    lina.look(c.t0, (2.6, 4.3, 1.7), 0.4)
    ben.look(c.t0, (2.6, 4.3, 1.7), 0.4)
    c.pov.at(c.t0, pos=NOAH, target=(3.0, 4.35, 1.5), dur=0.01, lens=36)
    c.pov.at(c.t0 + 0.4, target=(2.55, 4.25, 1.55), dur=1.8)
    c.phone(None)


@shot("03_lina_protest", "klasse", lambda c: c.S("l03") - 0.1)
def s03(c):
    sander, ben, lina = c.a["Sander"], c.a["Ben"], c.a["Lina"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    sander.place((2.55, 4.25, 0), heading((2.55, 4.25, 0), LINA_KOPF))
    sander.look(c.t0, LINA_KOPF, 0.3)
    lina.look(c.t0, (2.55, 4.25, 1.75), 0.2)
    lina.bend(c.t0, (-4, 35), 0.3)
    lina.arm(c.t0 + 0.2, "r", "abwehr", 0.3)
    lina.brow(c.t0, "boese", 0.2)
    lina.say(c.S("l03"), c.env("l03"))
    ben.look(c.t0, LINA_KOPF, 0.3)
    c.pov.at(c.t0, pos=NOAH, target=(-2.15, 2.6, 1.38), dur=0.01, lens=15)


@shot("04_hinsetzen", "klasse", lambda c: c.S("l04") - 0.05)
def s04(c):
    sander, lina = c.a["Sander"], c.a["Lina"]
    lina.place(LINA_SITZ, 180)
    sp = (1.6, 4.0, 0)
    sander.place(sp, heading(sp, LINA_KOPF))
    sander.look(c.t0, LINA_KOPF, 0.01)
    sander.arm(c.t0, "r", "zeigen", 0.25)
    sander.brow(c.t0, "boese", 0.2)
    sander.say(c.S("l04"), c.env("l04"))
    c.pov.at(c.t0, pos=NOAH, target=(1.6, 4.0, 1.6), dur=0.01, lens=40)
    c.pov.at(c.t0 + 0.1, target=(1.55, 4.0, 1.65), dur=1.2, lens=46)


def handy_einstellung(c, n, nach_oben=None, seitlich=None):
    ben = c.a.get("Ben")
    if ben is not None and c.set == "klasse":
        ben.place(BEN_SITZ, 180)
        ben.look(c.t0, NOAH + Vector((0.0, 0.25, -0.45)), 0.3)
        ben.bend(c.t0, (10, -22), 0.4)
        ben.brow(c.t0, "sorge", 0.3)
    c.pov.at(c.t0, pos=NOAH + Vector((0, 0.02, -0.04)), target=NOAH + Vector((0.05, 0.55, -0.95)), dur=0.01, lens=17)
    c.pov.at(c.t0 + 0.2, target=NOAH + Vector((0.02, 0.6, -0.9)), dur=1.5)
    c.phone(f"r{n}", raise_at=c.t0, lower_at=None)
    c.pov.shake = 0.7
    if nach_oben is not None:
        t, tgt, lens = nach_oben
        c.pov.at(t, target=tgt, dur=0.5, lens=lens)
        c.phone(f"r{n}", raise_at=c.t0, lower_at=t)


@shot("05_regel1", "klasse", lambda c: c.S("r1") - 0.65)
def s05(c):
    c.a["Sander"].place((1.6, 4.0, 0), heading((1.6, 4.0, 0), NOAH))
    c.a["Sander"].look(c.t0, LINA_KOPF, 0.01)
    handy_einstellung(c, 1)


@shot("06_wer_schreibt", "klasse", lambda c: c.S("l05") - 0.2)
def s06(c):
    ben = c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    ben.look(c.t0, "cam", 0.3)
    ben.bend(c.t0, (4, -25), 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.look(c.S("l06") + 0.3, NOAH + Vector((0.02, 0.28, -0.35)), 0.35)
    ben.brow(c.S("l06") + 0.4, "schreck", 0.2)
    ben.look(c.E("l06") - 0.4, "cam", 0.3)
    ben.say(c.S("l06"), c.env("l06"))
    c.pov.at(c.t0, pos=NOAH, target=BEN_KOPF + Vector((0.15, 0.1, -0.12)), dur=0.01, lens=16)
    c.phone("r1", raise_at=None, lower_at=None, low=True)


@shot("07_sander_kommt", "klasse", lambda c: c.S("l07") - 0.25)
def s07(c):
    sander, ben, lina = c.a["Sander"], c.a["Ben"], c.a["Lina"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    p0 = (-0.9, 4.1, 0)
    p1 = (-1.48, 1.15, 0)
    sander.place(p0, heading(p0, NOAH))
    sander.move(c.t0, c.t0 + 2.3, p1, walk=True, rot=heading(p1, NOAH))
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "skeptisch", 0.3)
    sander.say(c.S("l07"), c.env("l07"))
    lina.look(c.t0, (-1.2, 2.5, 1.7), 0.4)
    c.pov.at(c.t0, pos=NOAH, target=(-1.0, 3.6, 1.6), dur=0.01, lens=18)
    c.pov.at(c.t0 + 0.3, target=(-1.45, 1.4, 1.62), dur=2.0)
    c.phone(None, lower_at=c.t0)


@shot("08_nichts", "klasse", lambda c: c.S("l08") - 0.1)
def s08(c):
    sander, ben = c.a["Sander"], c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    sp = (-1.5, 0.95, 0)
    sander.place(sp, heading(sp, NOAH))
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "skeptisch", 0.01)
    sander.arm(c.t0, "beide", "verschraenkt", 0.4)
    ben.look(c.t0, (-1.5, 0.95, 1.75), 0.3)
    c.pov.at(c.t0, pos=NOAH, target=(-1.5, 0.95, 1.72), dur=0.01, lens=16)


@shot("09_passiert_nichts", "klasse", lambda c: c.S("l09") - 0.1)
def s09(c):
    sander, ben = c.a["Sander"], c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    sp = (-1.5, 0.95, 0)
    sander.place(sp, heading(sp, NOAH))
    sander.arm(c.t0, "beide", "verschraenkt", 0.01)
    sander.bend(c.t0, (16, 0), 0.6)
    sander.look(c.t0, BEN_KOPF, 0.3)
    sander.look(c.S("l09") + 1.0, "cam", 0.4)
    sander.say(c.S("l09"), c.env("l09"))
    sander.mouth_closed = 0.45
    ben.look(c.t0, (-1.5, 0.95, 1.6), 0.2)
    ben.brow(c.t0, "sorge", 0.2)
    c.pov.at(c.t0, pos=NOAH, target=(-1.5, 0.95, 1.62), dur=0.01, lens=18)
    c.pov.at(c.t0 + 0.5, target=(-1.55, 0.9, 1.52), dur=1.5, lens=20)


@shot("10_alle_draussen", "klasse", lambda c: c.S("l10") - 0.3)
def s10(c):
    lina, ben, sander = c.a["Lina"], c.a["Ben"], c.a["Sander"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    sander.place((-1.2, 5.05, 0), heading((-1.2, 5.05, 0), NOAH))
    lina.look(c.t0, (-8, 1.2, -1.0), 0.3)
    lina.bend(c.t0, (0, -40), 0.4)
    lina.look(c.S("l10") + 0.6, "cam", 0.35)
    lina.brow(c.t0, "sorge", 0.3)
    lina.say(c.S("l10"), c.env("l10"))
    ben.look(c.t0, (-8, 0.4, -1.0), 0.4)
    c.pov.at(c.t0, pos=NOAH, target=LINA_KOPF + Vector((-0.2, 0.2, -0.05)), dur=0.01, lens=16)


@shot("10b_hof", "klasse", lambda c: c.S("l10") + 1.7)
def s10b(c):
    lina, ben = c.a["Lina"], c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    lina.look(c.t0, (-10, 2, -3), 0.01)
    ben.look(c.t0, (-10, 0, -3), 0.01)
    lina.say(c.S("l10"), c.env("l10"))
    c.pov.at(c.t0, pos=(-3.15, 0.6, 1.62), target=(-12.0, -1.5, -5.6), dur=0.01, lens=21)
    c.pov.at(c.t0 + 0.1, pos=(-3.3, 0.62, 1.66), target=(-13.0, 1.5, -6.2), dur=2.2, lens=24)


@shot("11_warum_wir", "klasse", lambda c: c.S("l11") - 0.05)
def s11(c):
    ben, lina = c.a["Ben"], c.a["Lina"]
    ben.place(BEN_SITZ, 180)
    lina.place(LINA_SITZ, 180)
    ben.look(c.t0, "cam", 0.2)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("l11"), c.env("l11"))
    lina.look(c.t0, "cam", 0.3)
    c.pov.at(c.t0, pos=NOAH, target=BEN_KOPF + Vector((0.15, 0.1, -0.12)), dur=0.01, lens=16)


@shot("12_anwesenheit", "klasse", lambda c: c.S("l12") - 0.3)
def s12(c):
    sander, lina = c.a["Sander"], c.a["Lina"]
    lina.place(LINA_SITZ, 180)
    sp = (-1.45, 5.3, 0)
    sander.place(sp, heading(sp, NOAH) * 0.5)
    sander.arm(c.t0, "beide", "liste", 0.3)
    sander.look(c.t0, "cam", 0.01)
    sander.say(c.S("l12"), c.env("l12"))
    c.list_prop = True
    c.pov.at(c.t0, pos=NOAH, target=(-1.45, 5.3, 1.5), dur=0.01, lens=34)


@shot("13_regel2", "klasse", lambda c: c.S("r2") - 0.65)
def s13(c):
    c.a["Sander"].place((-1.45, 5.3, 0), 0)
    handy_einstellung(c, 2)


@shot("14_noah_berger", "klasse", lambda c: c.S("l13") - 0.3)
def s14(c):
    sander, lina = c.a["Sander"], c.a["Lina"]
    lina.place(LINA_SITZ, 180)
    sp = (-1.45, 5.3, 0)
    sander.place(sp, heading(sp, NOAH) * 0.5)
    sander.arm(c.t0, "beide", "liste", 0.01)
    c.list_prop = True
    sander.look(c.t0, (-1.45, 4.7, 0.9), 0.01)
    sander.look(c.E("l13") + 0.15, (2.5, 1.0, 1.2), 0.5)
    sander.look(c.E("l13") + 0.75, (-2.3, 0.3, 1.25), 0.6)
    sander.look(c.S("l14") + 0.5, "cam", 0.5)
    sander.brow(c.E("l13"), "skeptisch", 0.4)
    sander.say(c.S("l13"), c.env("l13"))
    sander.say(c.S("l14"), c.env("l14"))
    c.pov.at(c.t0, pos=NOAH, target=(-1.45, 5.3, 1.6), dur=0.01, lens=32)
    c.pov.at(c.t0 + 0.2, target=(-1.45, 5.3, 1.76), dur=c.t1 - c.t0 - 0.2, lens=58)


@shot("15_krank", "klasse", lambda c: c.S("l15") - 0.1)
def s15(c):
    ben = c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    ben.look(c.t0, (-1.45, 5.3, 1.7), 0.15)
    ben.arm(c.t0, "r", "hand_hoch", 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("l15"), c.env("l15"))
    c.pov.at(c.t0, pos=NOAH, target=BEN_KOPF + Vector((0.12, 0.12, 0.0)), dur=0.01, lens=16)


@shot("16_soso", "klasse", lambda c: c.S("l16") - 0.15)
def s16(c):
    sander = c.a["Sander"]
    sp = (-1.45, 5.3, 0)
    sander.place(sp, heading(sp, NOAH))
    sander.arm(c.t0, "beide", "liste", 0.01)
    c.list_prop = True
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "boese", 0.6)
    sander.say(c.S("l16"), c.env("l16"))
    sander.idle = 0.3
    c.pov.at(c.t0, pos=NOAH, target=(-1.45, 5.3, 1.8), dur=0.01, lens=70)
    c.pov.at(c.t0 + 0.1, target=(-1.45, 5.3, 1.82), dur=1.5, lens=80)
    c.pov.shake = 0.5


@shot("17_durchsage", "klasse", lambda c: c.S("l17") - 1.1)
def s17(c):
    sander = c.a["Sander"]
    sp = (-1.45, 5.3, 0)
    sander.place(sp, heading(sp, NOAH))
    sander.look(c.t0 + 0.2, SPRECHER, 0.4)
    sander.move(c.t0 + 1.0, c.t0 + 3.6, (3.0, 5.45, 0), walk=True, rot=180)
    sander.look(c.t0 + 3.3, REGLER, 0.3)
    sander.arm(c.t0 + 3.4, "r", "kabel", 0.4)
    sander.brow(c.t0 + 0.4, "boese", 0.3)
    c.pov.at(c.t0, pos=NOAH, target=(0.4, 5.6, 2.0), dur=0.01, lens=20)
    c.pov.at(c.t0 + 0.4, target=SPRECHER + Vector((0.2, 0, -0.5)), dur=0.7, lens=44)


@shot("18_abgedreht", "klasse", lambda c: c.S("l18") - 0.4)
def s18(c):
    lina, sander, ben = c.a["Lina"], c.a["Sander"], c.a["Ben"]
    lina.place(LINA_SITZ, 180)
    ben.place(BEN_SITZ, 180)
    sander.place((3.0, 5.45, 0), 180)
    sander.arm(c.t0, "r", "kabel", 0.01)
    sander.arm(c.t0 + 0.5, "r", "stehen", 0.6)
    sander.look(c.t0, REGLER, 0.01)
    sander.look(c.t0 + 0.7, "cam", 0.5)
    lina.look(c.t0, "cam", 0.25)
    lina.bend(c.t0, (0, -35), 0.3)
    lina.brow(c.t0, "schreck", 0.2)
    lina.say(c.S("l18"), c.env("l18"))
    ben.look(c.t0, (3.0, 5.45, 1.8), 0.3)
    c.pov.at(c.t0, pos=NOAH, target=(-2.15, 2.6, 1.4), dur=0.01, lens=15)


@shot("19_regel3", "klasse", lambda c: c.S("r3") - 0.65)
def s19(c):
    c.a["Sander"].place((3.0, 5.45, 0), 0)
    handy_einstellung(c, 3, nach_oben=(c.E("r3") - 1.2, VORB + Vector((0.2, 0, 0.1)), 22))


@shot("20_welcher", "klasse", lambda c: c.S("l19") - 0.5)
def s20(c):
    sander, lina, ben = c.a["Sander"], c.a["Lina"], c.a["Ben"]
    lina.place(LINA_SITZ, 180)
    ben.place(BEN_SITZ, 180)
    sp = (3.55, 4.1, 0)
    sander.place(sp, 75)
    sander.arm(c.t0, "r", "telefon", 0.01)
    sander.look(c.t0, (8, 5.0, 1.0), 0.01)
    sander.say(c.S("l19"), c.env("l19"))
    c.phone_prop = "Sander"
    lina.look(c.t0, (3.55, 4.1, 1.8), 0.4)
    ben.look(c.t0, (3.55, 4.1, 1.8), 0.4)
    c.pov.at(c.t0, pos=NOAH, target=(3.45, 4.1, 1.6), dur=0.01, lens=42)


@shot("21_wie_du_aussiehst", "klasse", lambda c: c.S("l20") - 0.1)
def s21(c):
    ben = c.a["Ben"]
    ben.place(BEN_SITZ, 180)
    ben.look(c.t0, "cam", 0.15)
    ben.bend(c.t0, (6, -28), 0.25)
    ben.brow(c.t0, "schreck", 0.15)
    ben.say(c.S("l20"), c.env("l20"))
    ben.look(c.S("l21") + 0.1, (-3.0, 5.98, 0.8), 0.3)
    c.pov.at(c.t0, pos=NOAH, target=BEN_KOPF + Vector((0.1, 0.08, -0.1)), dur=0.01, lens=16)
    c.pov.at(c.S("l21"), target=VORB + Vector((0.5, 0, -0.2)), dur=0.45, lens=16)


@shot("22_mir_ist_schlecht", "klasse", lambda c: c.S("l22") - 0.25)
def s22(c):
    lina, sander = c.a["Lina"], c.a["Sander"]
    lina.place(LINA_SITZ, 180)
    sp = (3.55, 4.1, 0)
    sander.place(sp, 75)
    sander.arm(c.t0, "r", "telefon", 0.01)
    sander.look(c.t0, (8, 5.0, 1.0), 0.01)
    c.phone_prop = "Sander"
    sander.look(c.S("l22") + 0.4, LINA_KOPF, 0.3)
    sander.move(c.S("l22") + 0.5, c.S("l22") + 1.2, sp, walk=False, rot=heading(sp, LINA_KOPF))
    sander.arm(c.S("l22") + 0.6, "r", "stehen", 0.4)
    lina.look(c.t0, (3.55, 4.1, 1.8), 0.2)
    lina.bend(c.t0, (12, 20), 0.3)
    lina.arm(c.t0, "beide", "bauch", 0.3)
    lina.brow(c.t0, "sorge", 0.2)
    lina.say(c.S("l22"), c.env("l22"))
    c.pov.at(c.t0, pos=(-1.55, 0.9, 0.78), target=(-1.75, 5.2, 0.9), dur=0.01, lens=15)
    c.pov.at(c.t0 + 0.1, pos=(-1.62, 3.9, 0.74), target=(-2.6, 6.2, 0.95), dur=c.t1 - c.t0 - 0.1)
    c.pov.run.append((c.t0, c.t1))


# ============================================================ FLUR
FLUR_V = 2.9      # Laufgeschwindigkeit m/s
FLUR_Y0 = 1.0


def flur_y(c, t):
    """Kamera-y im Flur zur Zeit t: läuft in 23/24, bleibt in 25 stehen, läuft in 26 weiter."""
    s23, s25, s26 = c.shot_start("23_regel4_flur"), c.shot_start("25_ich_weiss"), c.shot_start("26_lauf")
    if t <= s25:
        return FLUR_Y0 + FLUR_V * (t - s23)
    y25 = FLUR_Y0 + FLUR_V * (s25 - s23) + 0.6
    if t <= s26:
        return y25 - 0.6 + 0.6 * min(1.0, (t - s25) / 0.5)
    return y25 + (FLUR_V + 0.4) * (t - s26)


def run_cam(c, look_dx=0.0, look_z=1.05, ahead=9.0, x=-0.3):
    y0, y1 = flur_y(c, c.t0), flur_y(c, c.t1)
    c.pov.linear = True
    c.pov.at(c.t0 - 0.01, pos=(x, y0, 1.55), target=(x + look_dx, y0 + ahead, look_z), dur=0.01, lens=16)
    c.pov.at(c.t0, pos=(x, y1, 1.55), target=(x + look_dx, y1 + ahead, look_z), dur=c.t1 - c.t0)
    c.pov.run.append((c.t0 - 0.5, c.t1 + 0.5))
    return y0, y1


@shot("23_regel4_flur", "flur", lambda c: c.S("r4") - 0.7)
def s23(c):
    ben = c.a["Ben"]
    y0, y1 = run_cam(c, look_dx=0.1, look_z=0.85, ahead=6.0)
    ben.place((0.55, y0 + 1.6, 0), 180)
    ben.move(c.t0, c.t1, (0.55, y1 + 1.6, 0), walk=True, rot=180)
    ben.look(c.t0, (0.5, 40, 1.3), 0.01)
    c.a["Sander"].place((0, -50, -20), 0)
    c.phone("r4", raise_at=c.t0, lower_at=c.t1 - 0.3, low=False)


@shot("24_keller_niemand", "flur", lambda c: c.S("l23") - 0.1)
def s24(c):
    ben = c.a["Ben"]
    y0, y1 = run_cam(c, look_dx=0.75, look_z=1.25, ahead=2.6)
    ben.place((0.5, y0 + 1.15, 0), 180)
    ben.move(c.t0, c.t1, (0.5, y1 + 1.15, 0), walk=True, rot=180)
    ben.look(c.t0, "cam", 0.3)
    ben.brow(c.t0, "schreck", 0.2)
    ben.say(c.S("l23"), c.env("l23"))
    c.a["Sander"].place((0, -50, -20), 0)
    c.phone(None)


@shot("25_ich_weiss", "flur", lambda c: c.S("l24") - 0.15)
def s25(c):
    sander, ben = c.a["Sander"], c.a["Ben"]
    y = flur_y(c, c.t0)
    sy = y - 12.0
    sp = (0.35, sy, 0)
    sander.place(sp, 180)
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "boese", 0.01)
    sander.arm(c.t0 + 0.2, "r", "zeigen", 0.3)
    sander.say(c.S("l24"), c.env("l24"))
    sander.arm(c.E("l24") - 0.1, "r", "stehen", 0.3)
    sander.move(c.E("l24") - 0.1, c.t1 + 0.6, (0.35, sy + 2.2, 0), walk=True, rot=180)
    ben.place((0.55, y + 1.3, 0), 180)
    ben.look(c.t0 + 0.3, (0.35, sy, 1.7), 0.4)
    c.pov.at(c.t0, pos=(-0.3, y, 1.55), target=(-0.2, y + 6, 1.3), dur=0.01, lens=16)
    c.pov.at(c.t0 + 0.05, pos=(-0.3, flur_y(c, c.t1), 1.55), target=(0.35, sy, 1.62), dur=0.5, lens=58)
    c.pov.shake = 1.3


@shot("26_lauf", "flur", lambda c: c.S("l25") - 0.05)
def s26(c):
    ben = c.a["Ben"]
    y0 = flur_y(c, c.t0)
    ben.place((0.5, y0 + 1.0, 0), 180)
    ben.look(c.t0, "cam", 0.01)
    ben.brow(c.t0, "schreck", 0.01)
    ben.say(c.S("l25"), c.env("l25"))
    ben.look(c.S("l25") + 0.35, (0.0, 38, 1.2), 0.25)
    ben.move(c.S("l25") + 0.2, c.t1, (0.3, flur_y(c, c.t1) + 1.6, 0), walk=True, rot=180)
    c.a["Sander"].place((0, -50, -20), 0)
    c.pov.at(c.t0, pos=(-0.3, y0, 1.55), target=(0.35, y0 + 1.0, 1.3), dur=0.01, lens=16)
    c.pov.at(c.t0 + 0.3, pos=(-0.25, flur_y(c, c.t1), 1.55), target=(0.0, 38, 1.1), dur=c.t1 - c.t0 - 0.3)
    c.pov.run.append((c.t0 + 0.2, c.t1 + 0.3))


# ============================================================ KELLER
@shot("27_was_macht_ihr", "keller", lambda c: c.S("l26") - 1.1)
def s27(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pp = (-2.05, 2.4, 0)
    pohl.place(pp, -90)
    pohl.arm(c.t0, "beide", "tisch", 0.01)
    pohl.look(c.t0, (-3.0, 3.0, 0.9), 0.01)
    t_turn = c.t0 + 0.55
    pohl.move(t_turn, t_turn + 0.5, pp, walk=False, rot=heading(pp, (-2.3, -0.5, 0)))
    pohl.look(t_turn, "cam", 0.4)
    pohl.arm(t_turn, "beide", "stehen", 0.4)
    pohl.brow(t_turn, "schreck", 0.2)
    pohl.say(c.S("l26"), c.env("l26"))
    ben.place((-1.5, -0.3, 0), 0)
    ben.move(c.t0 + 0.3, c.t0 + 1.4, (-1.45, 0.55, 0), walk=True, rot=-20)
    ben.look(c.t0, (-2.05, 2.4, 1.7), 0.3)
    c.pov.at(c.t0, pos=(-2.55, -0.85, 1.58), target=(-2.2, 3.0, 1.4), dur=0.01, lens=16)
    c.pov.at(c.t0 + 0.1, pos=(-2.35, -0.25, 1.56), target=(-2.05, 2.4, 1.6), dur=1.0, lens=20)


@shot("28_sie_sucht_mich", "keller", lambda c: c.S("l27") - 0.1)
def s28(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pp = (-2.05, 2.4, 0)
    pohl.place(pp, heading(pp, (-2.3, -0.5, 0)))
    pohl.look(c.t0, "cam", 0.01)
    pohl.brow(c.t0, "sorge", 0.4)
    ben.place((-1.45, 0.55, 0), -20)
    ben.look(c.t0, (-2.05, 2.4, 1.7), 0.01)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.56), target=(-2.05, 2.4, 1.62), dur=0.01, lens=22)
    c.pov.shake = 1.3


@shot("29_zeig_mal", "keller", lambda c: c.S("l28") - 0.1)
def s29(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pp = (-2.05, 2.4, 0)
    pohl.place(pp, heading(pp, (-2.3, -0.5, 0)))
    pohl.look(c.t0, "cam", 0.01)
    pohl.brow(c.t0, "sorge", 0.01)
    pohl.say(c.S("l28"), c.env("l28"))
    pohl.move(c.S("l28") + 1.2, c.S("l28") + 2.4, (-2.15, 1.25, 0), walk=True, rot=heading((-2.15, 1.25, 0),
                                                                                         (-2.35, -0.25, 0)))
    pohl.arm(c.E("l28") - 0.9, "r", "greifen", 0.5)
    ben.place((-1.45, 0.55, 0), -20)
    ben.look(c.t0, (-2.05, 2.4, 1.7), 0.01)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.56), target=(-2.05, 2.4, 1.66), dur=0.01, lens=22)
    c.pov.at(c.S("l28") + 1.3, target=(-2.15, 1.3, 1.6), dur=1.2, lens=18)


@shot("30_regel5", "keller", lambda c: c.S("r5") - 0.7)
def s30(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pp = (-2.15, 0.95, 0)
    pohl.place(pp, heading(pp, (-2.35, -0.25, 0)))
    pohl.bend(c.t0, (22, 0), 0.4)
    pohl.look(c.t0, (-2.3, 0.1, 0.95), 0.3)
    pohl.arm(c.t0, "r", "greifen", 0.01)
    pohl.arm(c.t0 + 0.6, "r", "stehen", 0.6)
    pohl.brow(c.t0 + 2.0, "schreck", 0.4)
    ben.place((-1.6, 0.45, 0), -40)
    ben.look(c.t0, (-2.3, 0.1, 0.95), 0.3)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.52), target=(-2.25, 0.6, 1.0), dur=0.01, lens=17)
    c.pov.shake = 0.8
    c.phone("r5", raise_at=c.t0, lower_at=None)


@shot("31_papa", "keller", lambda c: c.S("l29") - 0.3)
def s31(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pp = (-2.15, 0.95, 0)
    pohl.place(pp, heading(pp, (-2.35, -0.25, 0)))
    pohl.bend(c.t0, (22, 0), 0.01)
    pohl.bend(c.t0 + 0.3, (4, 0), 0.8)
    pohl.look(c.t0, (-2.3, 0.1, 0.95), 0.01)
    pohl.look(c.t0 + 0.5, "cam", 0.5)
    pohl.brow(c.t0, "schreck", 0.01)
    ben.place((-1.6, 0.45, 0), -40)
    ben.look(c.t0, "cam", 0.4)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.52), target=(-2.3, 0.3, 0.6), dur=0.01, lens=17)
    c.pov.at(c.t0 + 0.4, target=(-2.15, 0.95, 1.7), dur=1.0, lens=22)
    c.phone("r5", raise_at=None, lower_at=c.t0 + 0.4)


@shot("32_beerdigung", "keller", lambda c: c.S("l30") - 0.2)
def s32(c):
    pohl = c.a["Pohl"]
    pp = (-2.15, 0.95, 0)
    pohl.place(pp, heading(pp, (-2.35, -0.25, 0)))
    pohl.look(c.t0, "cam", 0.01)
    pohl.brow(c.t0, "sorge", 0.3)
    pohl.say(c.S("l30"), c.env("l30"))
    pohl.idle = 0.6
    c.a["Ben"].place((-1.6, 0.45, 0), -40)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.52), target=(-2.15, 0.95, 1.78), dur=0.01, lens=30)
    c.pov.at(c.t0 + 0.2, target=(-2.15, 0.95, 1.8), dur=c.t1 - c.t0 - 0.2, lens=38)
    c.pov.shake = 0.6


@shot("33_wem_glaubst_du", "keller", lambda c: c.S("l31") - 0.2)
def s33(c):
    ben = c.a["Ben"]
    bp = (-1.6, 0.45, 0)
    ben.place(bp, heading(bp, (-2.35, -0.25, 0)))
    ben.look(c.t0, "cam", 0.01)
    ben.brow(c.t0, "sorge", 0.01)
    ben.say(c.S("l31"), c.env("l31"))
    c.a["Pohl"].place((-2.15, 0.95, 0), heading((-2.15, 0.95, 0), (-2.35, -0.25, 0)))
    c.a["Pohl"].look(c.t0, "cam", 0.01)
    c.pov.at(c.t0, pos=(-2.35, -0.25, 1.52), target=(-1.6, 0.45, 1.5), dur=0.01, lens=20)
    c.pov.at(c.t0 + 0.3, target=(-1.62, 0.45, 1.55), dur=2.0, lens=24)
    c.pov.shake = 0.6

"""Einstellungen für DER FEUERALARM · Teil 2 (AUTO).

Sets: keller (Rückblick, Pohl ruft), hof (Hinterhof, blaues Auto, Fahrer, Sander an der Tür),
auto (Rückbank, Fahrt durch die Stadt bis zur roten Ampel). Im Auto sind alle Positionen relativ zum Auto
(c.im_auto: Kamera und Figuren fahren mit).
"""
import math

from mathutils import Vector

import set_hof as H

SHOTS = []


def shot(sid, set_, start):
    def deco(fn):
        SHOTS.append(dict(id=sid, set=set_, start=start, fn=fn))
        return fn
    return deco


def heading(frm, to):
    d = Vector(to) - Vector(frm)
    return math.degrees(math.atan2(d.x, -d.y))


# ============================================================ KELLER (wie Ende Teil 1)
K_NOAH = Vector((-2.35, -0.25, 1.52))
K_POHL = (-1.75, 0.95, 0)
K_BEN = (-2.9, 0.5, 0)


@shot("01_rueckblick", "keller", lambda c: 0.0)
def s01(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pohl.place(K_POHL, heading(K_POHL, (-2.35, -0.25, 0)))
    pohl.look(c.t0, (-2.3, 0.3, 1.0), 0.01)
    pohl.brow(c.t0, "sorge", 0.01)
    ben.place(K_BEN, 40)
    ben.look(c.t0, (-2.3, 0.3, 1.0), 0.01)
    c.pov.at(c.t0, pos=K_NOAH, target=(-2.3, 0.55, 0.62), dur=0.01, lens=22)
    c.pov.at(c.t0 + 0.3, target=(-2.31, 0.5, 0.66), dur=c.t1 - c.t0, lens=26)
    c.phone("r5", raise_at=None, lower_at=c.t1 - 0.25)


@shot("02_pohl_ruft", "keller", lambda c: c.S("k01") - 0.15)
def s02(c):
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    pohl.place(K_POHL, heading(K_POHL, (-2.35, -0.25, 0)))
    pohl.look(c.t0, "cam", 0.2)
    pohl.brow(c.t0, "schreck", 0.2)
    pohl.arm(c.t0 + 0.1, "r", "zeigen", 0.3)
    pohl.move(c.t0 + 0.4, c.t1 + 0.4, (-2.05, 0.1, 0), walk=True, rot=heading((-2.05, 0.1, 0), (-2.4, -1.0, 0)))
    pohl.say(c.S("k01"), c.env("k01"))
    ben.place(K_BEN, 40)
    ben.look(c.t0, (-2.6, -1.0, 1.3), 0.3)
    ben.move(c.t0 + 0.3, c.t1, (-2.7, -0.35, 0), walk=True, rot=heading((-2.9, 0.5, 0), (-2.6, -1.2, 0)))
    # Noah ist schon an der Tür und schaut zurück
    c.pov.at(c.t0, pos=(-2.55, -0.75, 1.55), target=(-1.75, 0.95, 1.7), dur=0.01, lens=20)
    c.pov.shake = 1.4


# ============================================================ HINTERHOF
TUER = Vector((0.0, 0.6, 1.55))
AUTO_TUER_HINTEN = Vector((3.72, 12.05, 0))
FAHRER_START = (2.6, 11.5, 0)
FAHRER_WINK = (3.2, 11.35, 0)


def hof_basis(c, fahrer_bei=FAHRER_START):
    c.glas_aus = False
    f = c.a["Fahrer"]
    f.place(fahrer_bei, heading(fahrer_bei, (0.4, 3.0, 0)))
    f.look(c.t0, "cam", 0.01)
    return f


@shot("03_raus", "hof", lambda c: c.S("k02") - 0.25)
def s03(c):
    ben = c.a["Ben"]
    f = hof_basis(c)
    f.place((2.6, 12.3, 0), 0)            # noch im Auto (sitzend unsichtbar hinter der Tür)
    f.look(c.t0, (0.3, 2.0, 1.5), 0.01)
    ben.place((-0.4, 0.4, 0), 180)
    ben.move(c.t0 + 0.2, c.t1, (-0.6, 3.2, 0), walk=True, rot=200)
    ben.look(c.t0, "cam", 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("k02"), c.env("k02"))
    c.a["Sander"].place((0, -60, -30), 0)
    c.pov.linear = True
    c.pov.at(c.t0 - 0.01, pos=(0.2, 0.3, 1.55), target=(0.8, 6.0, 1.3), dur=0.01, lens=16)
    c.pov.at(c.t0, pos=(0.5, 3.6, 1.55), target=(2.6, 12.0, 1.1), dur=c.t1 - c.t0)
    c.pov.run.append((c.t0, c.t1 + 0.3))


@shot("04_blaues_auto", "hof", lambda c: c.S("k04") - 0.15)
def s04(c):
    ben = c.a["Ben"]
    f = hof_basis(c)
    f.place((2.55, 12.25, 0), 0)
    f.look(c.t0, (0.3, 4.0, 1.5), 0.01)
    ben.place((-0.6, 3.2, 0), 200)
    ben.look(c.t0, (3.2, 13.0, 1.0), 0.2)
    ben.arm(c.t0 + 0.1, "r", "zeigen", 0.3)
    ben.brow(c.t0, "schreck", 0.2)
    ben.say(c.S("k04"), c.env("k04"))
    c.a["Sander"].place((0, -60, -30), 0)
    c.pov.at(c.t0, pos=(0.5, 3.6, 1.55), target=(3.0, 12.8, 1.0), dur=0.01, lens=24)
    c.pov.at(c.t0 + 0.2, target=(3.1, 12.9, 1.05), dur=c.t1 - c.t0, lens=30)


@shot("05_fahrer", "hof", lambda c: c.S("k05") - 0.6)
def s05(c):
    ben = c.a["Ben"]
    f = hof_basis(c)
    f.place(FAHRER_START, 0)
    f.move(c.t0, c.t0 + 0.9, FAHRER_START, walk=False, rot=heading(FAHRER_START, (1.0, 6.4, 0)))
    f.move(c.t0 + 0.9, c.t0 + 2.2, FAHRER_WINK, walk=True, rot=heading(FAHRER_WINK, (1.0, 6.4, 0)))
    f.look(c.t0 + 0.3, "cam", 0.4)
    f.arm(c.S("k05") + 1.4, "l", "zeigen", 0.4)
    f.say(c.S("k05"), c.env("k05"))
    ben.place((-0.3, 5.6, 0), 200)
    ben.look(c.t0, (2.6, 11.5, 1.8), 0.3)
    c.a["Sander"].place((0, -60, -30), 0)
    c.pov.at(c.t0, pos=(0.9, 6.0, 1.55), target=(2.6, 11.4, 1.6), dur=0.01, lens=22)
    c.pov.at(c.t0 + 0.4, pos=(1.0, 6.4, 1.55), target=(3.1, 11.3, 1.75), dur=1.5, lens=28)


@shot("06_namen", "hof", lambda c: c.S("k06") - 0.1)
def s06(c):
    ben = c.a["Ben"]
    f = hof_basis(c, FAHRER_WINK)
    ben.place((0.35, 6.2, 0), heading((0.35, 6.2, 0), (1.0, 6.4, 0)) + 40)
    ben.look(c.t0, "cam", 0.2)
    ben.brow(c.t0, "skeptisch", 0.2)
    ben.bend(c.t0, (6, -18), 0.3)
    ben.say(c.S("k06"), c.env("k06"))
    c.a["Sander"].place((0, -60, -30), 0)
    c.pov.at(c.t0, pos=(1.0, 6.4, 1.55), target=(0.35, 6.25, 1.6), dur=0.01, lens=18)


@shot("07_vater", "hof", lambda c: c.S("k07") - 0.1)
def s07(c):
    ben = c.a["Ben"]
    f = hof_basis(c, FAHRER_WINK)
    f.look(c.t0, "cam", 0.01)
    f.say(c.S("k08"), c.env("k08"))
    f.arm(c.S("k08") + 0.3, "r", "abwehr", 0.4)
    ben.place((0.35, 6.2, 0), heading((0.35, 6.2, 0), FAHRER_WINK))
    ben.look(c.t0, (3.2, 11.35, 1.9), 0.01)
    c.a["Sander"].place((0, -60, -30), 0)
    c.pov.at(c.t0, pos=(1.0, 6.4, 1.55), target=(3.15, 11.3, 1.85), dur=0.01, lens=32)
    c.pov.at(c.S("k08"), target=(3.18, 11.32, 1.88), dur=c.t1 - c.S("k08"), lens=40)


@shot("08_sander_tuer", "hof", lambda c: c.S("k09") - 0.35)
def s08(c):
    sander = c.a["Sander"]
    hof_basis(c, FAHRER_WINK)
    sander.place((0.0, 0.7, 0), 180)
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "boese", 0.01)
    sander.arm(c.t0 + 0.15, "r", "zeigen", 0.3)
    sander.say(c.S("k09"), c.env("k09"))
    sander.move(c.E("k09"), c.t1 + 0.5, (0.2, 2.0, 0), walk=True, rot=180)
    c.a["Ben"].place((0.35, 6.2, 0), 160)
    c.pov.at(c.t0, pos=(1.0, 6.4, 1.55), target=(2.0, 10.0, 1.4), dur=0.01, lens=20)
    c.pov.at(c.t0 + 0.05, target=(0.0, 0.7, 1.7), dur=0.35, lens=46)
    c.pov.shake = 1.3


@shot("09_rein", "hof", lambda c: c.S("k10") - 0.1)
def s09(c):
    ben = c.a["Ben"]
    hof_basis(c, (4.4, 11.2, 0))
    ben.place((0.35, 6.2, 0), 180)
    ben.look(c.t0, "cam", 0.01)
    ben.brow(c.t0, "schreck", 0.01)
    ben.say(c.S("k10"), c.env("k10"))
    ben.move(c.S("k10") + 0.4, c.t1, (3.4, 11.2, 0), walk=True, rot=heading((0.35, 6.2, 0), (3.4, 11.2, 0)))
    c.a["Sander"].place((0.2, 2.0, 0), 180)
    c.pov.linear = True
    c.pov.at(c.t0 - 0.01, pos=(1.0, 6.4, 1.55), target=(0.4, 6.3, 1.5), dur=0.01, lens=18)
    c.pov.at(c.S("k10") + 0.35, pos=(2.9, 10.2, 1.5), target=(3.72, 12.4, 1.1), dur=c.t1 - c.S("k10") - 0.35, lens=18)
    c.pov.run.append((c.S("k10") + 0.3, c.t1 + 0.2))


# ============================================================ IM AUTO
CAM = Vector(H.NOAH_AUGE)
CAM_MITTE = Vector((0.1, -0.48, 1.16))     # Noah duckt sich und lehnt zur Mitte („Kopf runter“)
FAHRER = (H.FAHRER_SITZ[0], H.FAHRER_SITZ[1], H.SITZ_Z["Fahrer"])
BEN = (H.BEN_SITZ[0], H.BEN_SITZ[1], H.SITZ_Z["Ben"])
FAHRER_KOPF = Vector((H.FAHRER_SITZ[0], H.FAHRER_SITZ[1] - 0.03, 1.44))
BEN_KOPF = Vector((H.BEN_SITZ[0], H.BEN_SITZ[1], 1.32))
HANDYHALTER = Vector(H.HANDYHALTER)
STRASSE = (H.FAHRER_SITZ[0], 14.0, 1.35)          # Fahrer schaut auf die Straße
FENSTERKNOPF = Vector((0.77, -0.55, 0.92))
# rote Ampel relativ zum haltenden Auto
AMPEL_REL = Vector((4.4 - H.SPUR_X, H.AMPEL_Y - 0.36 - H.STOP_Y, 3.6))


def auto_basis(c):
    """Gemeinsamer Aufbau im Auto. Positionen relativ zum Auto, das bei x=SPUR_X fährt."""
    c.glas_aus = True
    c.im_auto = True
    f, ben = c.a["Fahrer"], c.a["Ben"]
    f.place(FAHRER, 180)
    f.look(c.t0, STRASSE, 0.01)
    f.arm(c.t0, "beide", "tisch", 0.01)
    ben.place(BEN, 180)
    ben.look(c.t0, FAHRER_KOPF, 0.01)
    return f, ben


def umdrehen(f, t, dur=0.45, zurueck=None):
    """Fahrer dreht Kopf und Schultern nach hinten rechts (zu Noah); optional wieder nach vorn."""
    f.look(t, "cam", dur)
    f.bend(t, (0, -32), dur)
    if zurueck is not None:
        f.look(zurueck, STRASSE, 0.5)
        f.bend(zurueck, (0, 0), 0.5)


@shot("10_anschnallen", "auto", lambda c: c.S("k11") - 1.1)
def s10(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.S("k11") - 0.35, 0.4, zurueck=c.E("k11") + 0.25)
    f.brow(c.t0, "skeptisch", 0.3)
    f.say(c.S("k11"), c.env("k11"))
    ben.brow(c.t0, "sorge", 0.3)
    c.pov.at(c.t0, pos=CAM, target=(-0.05, 3.0, 1.2), dur=0.01, lens=16)
    c.pov.at(c.S("k11") - 0.35, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.4, lens=22)
    c.pov.shake = 0.5


@shot("11_lina", "auto", lambda c: c.S("k12") - 0.15)
def s11(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, "cam", 0.2)
    ben.bend(c.t0, (8, -20), 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("k12"), c.env("k12"))
    ben.look(c.E("k12") + 0.2, FAHRER_KOPF, 0.4)
    c.pov.at(c.t0, pos=CAM, target=BEN_KOPF + Vector((0.2, 0.15, -0.1)), dur=0.01, lens=17)
    c.pov.shake = 0.4


@shot("12_regel6", "auto", lambda c: c.S("r6") - 0.7)
def s12(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, CAM + Vector((0.0, 0.35, -0.5)), 0.3)
    ben.bend(c.t0, (10, -22), 0.4)
    c.pov.at(c.t0, pos=CAM + Vector((0, 0.02, -0.04)), target=CAM + Vector((0.0, 0.55, -0.95)), dur=0.01, lens=22)
    c.pov.at(c.t0 + 0.2, target=CAM + Vector((-0.02, 0.6, -0.9)), dur=1.5)
    c.pov.shake = 0.6
    c.phone("r6", raise_at=c.t0, lower_at=None)


@shot("13_anruf", "auto", lambda c: c.S("k15") - 1.0)
def s13(c):
    f, ben = auto_basis(c)
    c.fahrerhandy = "anruf_sander.png"
    f.arm(c.t0 + 0.5, "r", "greifen", 0.35)
    f.arm(c.S("k15") + 0.4, "r", "tisch", 0.35)
    ben.look(c.t0, HANDYHALTER, 0.2)
    ben.look(c.S("k15"), "cam", 0.25)
    ben.brow(c.t0, "schreck", 0.2)
    ben.bend(c.S("k15"), (8, -22), 0.3)
    ben.say(c.S("k15"), c.env("k15"))
    # Großaufnahme: Handy des Fahrers im Halter, eingehender Anruf „SANDER“
    c.pov.at(c.t0, pos=CAM, target=HANDYHALTER + Vector((0, 0, 0.005)), dur=0.01, lens=95)
    c.pov.at(c.t0 + 0.05, target=HANDYHALTER + Vector((0, 0, 0.0)), dur=c.S("k15") - c.t0 - 0.2, lens=105)
    c.pov.at(c.S("k15") - 0.12, target=BEN_KOPF + Vector((0.25, 0.22, -0.08)), dur=0.01, lens=17)


@shot("14_problem", "auto", lambda c: c.S("k16") - 0.2)
def s14(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.t0, 0.45, zurueck=c.E("k17") - 0.1)
    f.brow(c.t0, "skeptisch", 0.2)
    f.say(c.S("k16"), c.env("k16"))
    ben.look(c.t0, FAHRER_KOPF, 0.2)
    c.pov.at(c.t0, pos=CAM, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.01, lens=24)
    c.pov.at(c.t0 + 0.4, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.03)), dur=c.t1 - c.t0 - 0.4, lens=28)


@shot("15_regel7", "auto", lambda c: c.S("r7") - 0.7)
def s15(c):
    f, ben = auto_basis(c)
    f.look(c.t0, STRASSE, 0.01)
    ben.look(c.t0, CAM + Vector((0.0, 0.35, -0.5)), 0.3)
    c.pov.at(c.t0, pos=CAM + Vector((0, 0.02, -0.04)), target=CAM + Vector((0.0, 0.55, -0.95)), dur=0.01, lens=22)
    # Noah duckt sich und schaut zwischen den Sitzen nach vorn: rote Ampel
    c.pov.at(c.E("r7") - 1.0, pos=CAM_MITTE, target=AMPEL_REL + Vector((0, 0, -0.3)), dur=0.6, lens=40)
    c.pov.shake = 0.6
    c.phone("r7", raise_at=c.t0, lower_at=c.E("r7") - 1.0)


@shot("16_finger_weg", "auto", lambda c: c.S("k18") - 0.75)
def s16(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.S("k18") - 0.3, 0.35)
    f.brow(c.S("k18") - 0.3, "boese", 0.3)
    f.say(c.S("k18"), c.env("k18"))
    ben.look(c.t0, FENSTERKNOPF, 0.3)
    # Noah schaut auf den Fensterheber neben sich … dann dreht sich der Fahrer um
    c.pov.at(c.t0, pos=CAM, target=FENSTERKNOPF + Vector((0, 0.1, 0.05)), dur=0.01, lens=24)
    c.pov.at(c.S("k18") - 0.3, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.3, lens=26)
    c.pov.at(c.S("k18") + 0.1, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.03)), dur=c.t1 - c.S("k18"), lens=32)


@shot("17_was_machen_wir", "auto", lambda c: c.S("k19") - 0.15)
def s17(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.t0, 0.01, zurueck=c.t0 + 0.3)
    ben.look(c.t0, "cam", 0.2)
    ben.bend(c.t0, (6, -24), 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("k19"), c.env("k19"))
    c.pov.at(c.t0, pos=CAM, target=BEN_KOPF + Vector((0.15, 0.1, -0.08)), dur=0.01, lens=17)
    c.pov.at(c.t0 + 0.3, target=BEN_KOPF + Vector((0.13, 0.1, -0.06)), dur=2.0, lens=20)
    c.pov.shake = 0.5


@shot("18_ampel_gelb", "auto", lambda c: c.E("k19") + 0.2)
def s18(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, AMPEL_REL, 0.3)
    c.ampel = [(c.t0, "rot"), (c.t0 + 0.45, "rotgelb")]
    c.pov.at(c.t0, pos=CAM_MITTE, target=AMPEL_REL + Vector((0, 0, -0.25)), dur=0.01, lens=34)
    c.pov.at(c.t0 + 0.4, target=AMPEL_REL + Vector((0, 0, -0.1)), dur=1.2, lens=48)

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


# ============================================================ HINTERHOF (Start mitten in der Flucht)
TUER = Vector((0.0, 0.6, 1.55))
P0 = Vector((0.15, 0.75, 1.55))              # gerade aus der Kellertür gestürmt
P1 = Vector((0.95, 3.0, 1.55))               # hier dreht sich Noah zu Pohl um
STOP = Vector((2.0, 5.2, 1.55))              # hier bleibt Noah vor dem Fahrer stehen
FAHRER_HOF = H.hof_welt(-1.3, 0.3)           # neben der offenen Hintertür, außerhalb des Autos
FAHRER_HOF_KOPF = Vector((FAHRER_HOF[0], FAHRER_HOF[1], 1.95))
AUTO_BLICK = Vector(H.hof_welt(-0.6, 0.6, 1.0))
TUER_OFFEN = Vector(H.hof_welt(-1.35, -0.75, 1.1))   # Einstieg hinter der offenen Tür
BEN_HOF = (1.2, 5.3, 0)
POHL_TUER = (0.1, 0.8, 0)


def hof_basis(c):
    c.glas_aus = False
    f = c.a["Fahrer"]
    f.place(FAHRER_HOF, heading(FAHRER_HOF, (STOP.x, STOP.y, 0)))
    f.look(c.t0, "cam", 0.01)
    f.arm(c.t0, "l", "greifen", 0.01)        # Hand an der offenen Tür
    for nm in ("Pohl", "Sander"):
        c.a[nm].place((0, -60, -30), 0)
    return f


@shot("01_raus", "hof", lambda c: 0.0)
def s01(c):
    f = hof_basis(c)
    c.lichthupe = [(0.12, 0.3), (0.48, 0.66), (c.E("k01") + 0.05, c.E("k01") + 0.22)]
    pohl, ben = c.a["Pohl"], c.a["Ben"]
    # Pohl kommt erst aus der Tür, wenn Noah schon losgerannt ist (am Anfang steht die Kamera in der Tür)
    drinnen = (POHL_TUER[0], -1.3, 0)
    pohl.place(drinnen, heading(POHL_TUER, (P1.x, P1.y, 0)))
    pohl.move(c.S("k01") - 1.1, c.S("k01") - 0.45, POHL_TUER, walk=True, rot=heading(POHL_TUER, (P1.x, P1.y, 0)))
    pohl.look(c.t0, "cam", 0.01)
    pohl.brow(c.t0, "schreck", 0.01)
    pohl.arm(c.S("k01") - 0.2, "r", "zeigen", 0.3)
    pohl.say(c.S("k01"), c.env("k01"))
    # Ben stürmt hinter Pohl aus der Tür und rennt links an Noah vorbei
    b0, b1 = (-0.55, 0.75, 0), (-0.35, 3.3, 0)
    ben.place((-0.55, -1.3, 0), heading(b0, b1))
    ben.move(c.S("k01") - 0.6, c.S("k01") + 0.1, b0, walk=True, rot=heading(b0, b1))
    ben.move(c.S("k01") + 0.1, c.E("k01") + 0.25, b1, walk=True, rot=heading(b0, b1))
    ben.move(c.E("k01") + 0.25, c.E("k01") + 1.3, BEN_HOF, walk=True, rot=heading(b1, BEN_HOF))
    ben.look(c.t0, "cam", 0.3)
    ben.brow(c.t0, "schreck", 0.2)
    # Kamera: losrennen → umdrehen (Pohl brüllt) → weiter zum Auto
    c.pov.linear = True
    c.pov.at(c.t0, pos=P0, target=AUTO_BLICK + Vector((0, 0, 0.3)), dur=0.01, lens=30)
    c.pov.at(c.t0 + 0.45, pos=P1, dur=c.S("k01") - 0.25 - (c.t0 + 0.45))
    c.pov.at(c.t0 + 0.45, target=FAHRER_HOF_KOPF + Vector((0, 0, -0.3)), dur=1.8, lens=26)
    c.pov.at(c.S("k01") - 0.25, target=Vector((0.1, 0.8, 1.75)), dur=0.28, lens=24)        # Blick zurück
    c.pov.at(c.E("k01") - 0.05, target=FAHRER_HOF_KOPF + Vector((0, 0, -0.2)), dur=0.28, lens=26)
    c.pov.at(c.E("k01") + 0.1, pos=STOP, dur=c.t1 - c.E("k01") - 0.15)
    c.pov.run.append((c.t0 + 0.4, c.S("k01") - 0.1))
    c.pov.run.append((c.E("k01") + 0.05, c.t1))
    c.pov.shake = 1.5


@shot("02_fahrer", "hof", lambda c: c.S("k05") - 0.45)
def s02(c):
    f = hof_basis(c)
    f.say(c.S("k05"), c.env("k05"))
    f.arm(c.S("k05") + 1.5, "r", "zeigen", 0.35)          # „Steig ein“: zeigt auf die offene Tür
    f.look(c.S("k05") + 1.45, TUER_OFFEN, 0.25)
    f.look(c.S("k05") + 2.1, "cam", 0.3)
    c.a["Ben"].place(BEN_HOF, heading(BEN_HOF, FAHRER_HOF))
    c.a["Ben"].look(c.t0, FAHRER_HOF_KOPF, 0.2)
    c.pov.at(c.t0, pos=STOP, target=FAHRER_HOF_KOPF + Vector((0.0, 0.0, -0.45)), dur=0.01, lens=28)
    c.pov.at(c.t0 + 0.2, target=FAHRER_HOF_KOPF + Vector((0.0, 0.0, -0.35)), dur=c.t1 - c.t0 - 0.2, lens=36)
    c.pov.shake = 1.1


@shot("03_namen", "hof", lambda c: c.S("k06") - 0.1)
def s03(c):
    hof_basis(c)
    ben = c.a["Ben"]
    ben.place(BEN_HOF, heading(BEN_HOF, (STOP.x, STOP.y, 0)) + 25)
    ben.look(c.t0, "cam", 0.2)
    ben.brow(c.t0, "skeptisch", 0.2)
    ben.bend(c.t0, (6, -18), 0.3)
    ben.say(c.S("k06"), c.env("k06"))
    c.pov.at(c.t0, pos=STOP, target=Vector((BEN_HOF[0] + 0.05, BEN_HOF[1] + 0.05, 1.62)), dur=0.01, lens=19)


@shot("04_vater", "hof", lambda c: c.S("k07") - 0.1)
def s04(c):
    f = hof_basis(c)
    f.say(c.S("k08"), c.env("k08"))
    f.arm(c.S("k08") + 0.3, "r", "abwehr", 0.4)
    f.brow(c.S("k08"), "skeptisch", 0.3)
    c.a["Ben"].place(BEN_HOF, heading(BEN_HOF, FAHRER_HOF))
    c.a["Ben"].look(c.t0, FAHRER_HOF_KOPF, 0.01)
    c.pov.at(c.t0, pos=STOP, target=FAHRER_HOF_KOPF + Vector((0, 0, -0.25)), dur=0.01, lens=40)
    c.pov.at(c.S("k08"), target=FAHRER_HOF_KOPF + Vector((0, 0, -0.18)), dur=c.t1 - c.S("k08"), lens=50)


@shot("05_sander_tuer", "hof", lambda c: c.S("k09") - 0.35)
def s05(c):
    hof_basis(c)
    sander = c.a["Sander"]
    sander.place((0.0, 0.7, 0), heading((0.0, 0.7, 0), (STOP.x, STOP.y, 0)))
    sander.look(c.t0, "cam", 0.01)
    sander.brow(c.t0, "boese", 0.01)
    sander.arm(c.t0 + 0.15, "r", "zeigen", 0.3)
    sander.say(c.S("k09"), c.env("k09"))
    ziel = (0.9, 2.9, 0)
    sander.move(c.E("k09") - 0.2, c.t1 + 0.8, ziel, walk=True, rot=heading((0.0, 0.7, 0), ziel))
    c.a["Ben"].place(BEN_HOF, 160)
    c.pov.at(c.t0, pos=STOP, target=FAHRER_HOF_KOPF + Vector((0, 0, -0.25)), dur=0.01, lens=30)
    c.pov.at(c.t0 + 0.04, target=Vector((0.0, 0.7, 1.72)), dur=0.3, lens=42)
    c.pov.shake = 1.4


@shot("06_rein", "hof", lambda c: c.S("k10") - 0.1)
def s06(c):
    hof_basis(c)
    ben = c.a["Ben"]
    ben.place(BEN_HOF, heading(BEN_HOF, (STOP.x, STOP.y, 0)))
    ben.look(c.t0, "cam", 0.01)
    ben.brow(c.t0, "schreck", 0.01)
    ben.say(c.S("k10"), c.env("k10"))
    # Ben rennt hinten ums Auto zur anderen Tür
    um = H.hof_welt(-1.2, -2.9)
    ben.move(c.S("k10") + 0.5, c.t1 + 0.4, um, walk=True, rot=heading(BEN_HOF, um))
    c.a["Sander"].place((0.9, 2.9, 0), heading((0.9, 2.9, 0), (STOP.x, STOP.y, 0)))
    c.pov.linear = True
    c.pov.at(c.t0 - 0.01, pos=STOP, target=Vector((BEN_HOF[0], BEN_HOF[1] + 0.05, 1.6)), dur=0.01, lens=19)
    c.pov.at(c.S("k10") + 0.6, target=TUER_OFFEN, dur=0.3, lens=20)
    c.pov.at(c.S("k10") + 0.75, pos=Vector((4.2, 6.55, 1.3)), dur=c.t1 - c.S("k10") - 0.75)   # rechts am Fahrer vorbei
    c.pov.run.append((c.S("k10") + 0.6, c.t1 + 0.2))
    c.pov.shake = 1.5


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
INNENGRIFF = Vector((0.765, -0.3, 0.95))
FENSTER_HR = Vector((0.83, -0.57, 1.3))
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


@shot("07_anschnallen", "auto", lambda c: c.S("k11") - 1.6)
def s07(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.S("k11") - 0.3, 0.35, zurueck=c.E("k11") + 0.25)
    f.brow(c.t0, "skeptisch", 0.3)
    f.say(c.S("k11"), c.env("k11"))
    ben.brow(c.t0, "schreck", 0.3)
    c.pov.at(c.t0, pos=CAM, target=(-0.05, 3.0, 1.2), dur=0.01, lens=16)
    c.pov.at(c.t0 + 0.9, target=(-0.05, 3.0, 1.55), dur=0.18)          # Ruck beim Losrasen
    c.pov.at(c.t0 + 1.08, target=(-0.05, 3.0, 1.22), dur=0.25)
    c.pov.at(c.S("k11") - 0.3, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.35, lens=22)
    c.pov.shake = 1.0


@shot("08_lina", "auto", lambda c: c.S("k12") - 0.15)
def s08(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, "cam", 0.2)
    ben.bend(c.t0, (8, -20), 0.3)
    ben.brow(c.t0, "sorge", 0.2)
    ben.say(c.S("k12"), c.env("k12"))
    ben.look(c.E("k12") + 0.2, FAHRER_KOPF, 0.4)
    c.pov.at(c.t0, pos=CAM, target=BEN_KOPF + Vector((0.2, 0.15, -0.1)), dur=0.01, lens=17)
    c.pov.shake = 0.4


@shot("09_regel6", "auto", lambda c: c.S("r6") - 0.7)
def s09(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, CAM + Vector((0.0, 0.35, -0.5)), 0.3)
    ben.bend(c.t0, (10, -22), 0.4)
    c.pov.at(c.t0, pos=CAM + Vector((0, 0.02, -0.04)), target=CAM + Vector((0.0, 0.55, -0.95)), dur=0.01, lens=22)
    c.pov.at(c.t0 + 0.2, target=CAM + Vector((-0.02, 0.6, -0.9)), dur=1.5)
    c.pov.shake = 0.6
    c.phone("r6", raise_at=c.t0, lower_at=None)


@shot("10_tuer_zu", "auto", lambda c: c.S("k14") - 0.15)
def s10(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, "cam", 0.3)
    ben.brow(c.t0, "schreck", 0.2)
    t_tuer = c.W("k14", 2) - 0.25          # „Die Tür geht nicht auf!“
    c.pov.at(c.t0, pos=CAM + Vector((0, 0.02, -0.04)), target=CAM + Vector((-0.02, 0.6, -0.9)), dur=0.01, lens=22)
    c.pov.at(t_tuer, pos=CAM + Vector((0.08, 0.0, -0.05)), target=INNENGRIFF, dur=0.25, lens=24)
    c.pov.shake = 0.7
    c.pov.tilt(c.t0, 0, 0.01)              # Rütteln am Türgriff
    c.pov.tilt(t_tuer + 0.3, 4, 0.12)
    c.pov.tilt(t_tuer + 0.45, -3, 0.12)
    c.pov.tilt(t_tuer + 0.62, 3, 0.12)
    c.pov.tilt(t_tuer + 0.8, 0, 0.2)
    c.phone("r6", raise_at=None, lower_at=t_tuer - 0.1)


@shot("11_anruf", "auto", lambda c: c.S("k15a") - 1.15)
def s11(c):
    f, ben = auto_basis(c)
    c.fahrerhandy = "anruf_sander.png"
    f.look(c.t0 + 0.3, HANDYHALTER, 0.3)
    f.arm(c.S("k15a") - 0.55, "r", "greifen", 0.3)       # nimmt ab
    f.arm(c.S("k15a") + 0.3, "r", "tisch", 0.4)
    f.say(c.S("k15a"), c.env("k15a"))
    f.look(c.S("k15a") + 0.4, STRASSE, 0.4)
    f.look(c.E("k15a") - 0.9, "cam", 0.4)                 # „Wir sind gleich da.“ – Blick nach hinten
    f.bend(c.E("k15a") - 0.9, (0, -20), 0.4)
    f.brow(c.S("k15a"), "boese", 0.4)
    ben.look(c.t0, HANDYHALTER, 0.2)
    ben.look(c.S("k15") - 0.25, "cam", 0.25)
    ben.brow(c.t0, "schreck", 0.2)
    ben.bend(c.S("k15") - 0.2, (8, -22), 0.3)
    ben.say(c.S("k15"), c.env("k15"))
    # Großaufnahme: Anruf „SANDER“ → Fahrer nimmt ab → Schnitt auf Ben
    c.pov.at(c.t0, pos=CAM, target=HANDYHALTER + Vector((0, 0, 0.005)), dur=0.01, lens=95)
    c.pov.at(c.t0 + 0.05, target=HANDYHALTER, dur=0.9, lens=105)
    c.pov.at(c.S("k15a") - 0.3, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.35, lens=24)
    c.pov.at(c.E("k15a") - 0.9, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.03)), dur=0.9, lens=30)
    c.pov.at(c.S("k15") - 0.12, target=BEN_KOPF + Vector((0.25, 0.22, -0.08)), dur=0.01, lens=17)


@shot("12_problem", "auto", lambda c: c.S("k16") - 0.2)
def s12(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.t0, 0.45, zurueck=c.E("k17") - 0.1)
    f.brow(c.t0, "skeptisch", 0.2)
    f.say(c.S("k16"), c.env("k16"))
    ben.look(c.t0, FAHRER_KOPF, 0.2)
    c.pov.at(c.t0, pos=CAM, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.01, lens=24)
    c.pov.at(c.t0 + 0.4, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.03)), dur=c.t1 - c.t0 - 0.4, lens=28)


@shot("13_regel7", "auto", lambda c: c.S("r7") - 0.7)
def s13(c):
    f, ben = auto_basis(c)
    ben.look(c.t0, CAM + Vector((0.0, 0.35, -0.5)), 0.3)
    c.pov.at(c.t0, pos=CAM + Vector((0, 0.02, -0.04)), target=CAM + Vector((0.0, 0.55, -0.95)), dur=0.01, lens=22)
    # Noah duckt sich und schaut zwischen den Sitzen nach vorn: rote Ampel
    c.pov.at(c.E("r7") - 1.0, pos=CAM_MITTE, target=AMPEL_REL + Vector((0, 0, -0.3)), dur=0.6, lens=40)
    c.pov.shake = 0.6
    c.phone("r7", raise_at=c.t0, lower_at=c.E("r7") - 1.0)


@shot("14_finger_weg", "auto", lambda c: c.S("k18") - 0.75)
def s14(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.S("k18") - 0.3, 0.35)
    f.brow(c.S("k18") - 0.3, "boese", 0.3)
    f.say(c.S("k18"), c.env("k18"))
    ben.look(c.t0, FENSTERKNOPF, 0.3)
    # Noah schaut auf den Fensterheber neben sich … dann dreht sich der Fahrer um
    c.pov.at(c.t0, pos=CAM, target=FENSTERKNOPF + Vector((0, 0.1, 0.05)), dur=0.01, lens=24)
    c.pov.at(c.S("k18") - 0.3, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.3, lens=26)
    c.pov.at(c.S("k18") + 0.1, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.03)), dur=c.t1 - c.S("k18"), lens=32)


@shot("15_fenster", "auto", lambda c: c.E("k18") + 0.15)
def s15(c):
    f, ben = auto_basis(c)
    umdrehen(f, c.t0, 0.01, zurueck=c.t0 + 0.15)            # schaut wieder nach vorn …
    c.fenster = (c.t0 + 0.2, c.t0 + 1.35)                   # … da fährt die Scheibe von selbst herunter
    umdrehen(f, c.t0 + 1.0, 0.3)                            # … und er fährt herum
    f.brow(c.t0 + 1.0, "boese", 0.2)
    ben.look(c.t0 + 0.2, FENSTER_HR, 0.3)
    ben.brow(c.t0 + 0.2, "schreck", 0.2)
    c.pov.at(c.t0, pos=CAM, target=FENSTER_HR + Vector((0, 0.05, -0.05)), dur=0.01, lens=22)
    c.pov.at(c.t0 + 1.35, target=FAHRER_KOPF + Vector((0.12, -0.05, -0.04)), dur=0.22, lens=26)
    c.pov.shake = 1.2


@shot("16_was_machen_wir", "auto", lambda c: c.S("k19") - 0.15)
def s16(c):
    f, ben = auto_basis(c)
    c.fenster = (-2.0, -1.0)
    umdrehen(f, c.t0, 0.01)
    f.brow(c.t0, "boese", 0.01)
    ben.look(c.t0, "cam", 0.2)
    ben.bend(c.t0, (6, -24), 0.3)
    ben.brow(c.t0, "schreck", 0.2)
    ben.say(c.S("k19"), c.env("k19"))
    c.pov.at(c.t0, pos=CAM, target=BEN_KOPF + Vector((0.15, 0.1, -0.08)), dur=0.01, lens=17)
    c.pov.at(c.t0 + 0.3, target=BEN_KOPF + Vector((0.13, 0.1, -0.06)), dur=2.0, lens=20)
    c.pov.shake = 0.8


@shot("17_ampel_gelb", "auto", lambda c: c.E("k19") + 0.2)
def s17(c):
    f, ben = auto_basis(c)
    c.fenster = (-2.0, -1.0)
    ben.look(c.t0, AMPEL_REL, 0.3)
    c.ampel = [(c.t0, "rot"), (c.t0 + 0.45, "rotgelb")]
    c.pov.at(c.t0, pos=CAM_MITTE, target=AMPEL_REL + Vector((0, 0, -0.25)), dur=0.01, lens=34)
    c.pov.at(c.t0 + 0.4, target=AMPEL_REL + Vector((0, 0, -0.1)), dur=1.2, lens=48)

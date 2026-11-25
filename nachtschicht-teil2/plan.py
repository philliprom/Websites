"""Schnittplan für Nachtschicht Teil 2 aus den Sprechzeiten (nach emotion.py).
  python3 nachtschicht-teil2/plan.py a|b
schreibt <zweig>/build/edl.json (Einstellungen mit Start/Ende, Quelle, Uhrzeit, Ereignisse) und für A zusätzlich
build/shots.json (Bildzahl und Türbeginn der Ich-Sicht „tuer“ für scene.py).
Quellen: t1r1/t1r2/t1r3 = Bildfolgen aus Teil 1 (CAM 01 leer, CAM 03, CAM 01 mit Gestalt an der Tür), tuer/lager = neu.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
Z = sys.argv[1]
B = os.path.join(HERE, Z, "build")
tl = json.load(open(os.path.join(B, "timeline.json"), encoding="utf-8"))
SEG = {s["id"]: s for s in tl["segments"]}
D = tl["duration"]
st = lambda i: SEG[i]["start"]           # noqa: E731
en = lambda i: SEG[i]["speechEnd"]       # noqa: E731


def capt(i, k):
    c = SEG[i]["caps"]
    return c[k]["start"] if k < len(c) else st(i)


r = lambda x: round(x, 3)  # noqa: E731
T1 = json.load(open(os.path.join(HERE, "..", "nachtschicht-teil1", "build", "shots.json"), encoding="utf-8"))
JUMP = T1["r3"]["jump"]                  # ab hier steht die Gestalt in Teil 1 an der Tür
FIG_GONE = T1["r2"]["fig_out"]           # ab hier ist CAM 03 leer
C = lambda h, m, s=0: h * 3600 + m * 60 + s  # noqa: E731
shots, ev = [], {}


def add(id_, a, b, kind, **kw):
    shots.append(dict(id=id_, t=[r(a), r(b)], kind=kind, **kw))


if Z == "a":
    t1 = st("a02") - 0.35
    t2 = st("a04") - 0.25
    t3 = en("a06") + 0.55
    t4 = st("a09") - 0.2
    t5 = st("a11") - 0.25
    t6 = st("a16") - 0.1
    t7 = st("a17") - 0.6
    t8 = en("a17") + 0.7
    add("SH0", 0, t1, "prints", src="t1r1", frm=1, loop=True, cam="CAM 01  EINGANG", clock=C(2, 51, 3), reveal="all",
        zoom=[0.0, t1, 1.0, 1.35], title=True)
    add("SH1", t1, t2, "vote", src="t1r3", frm=JUMP + 6, loop=True, cam="CAM 01  EINGANG", clock=C(2, 47, 40), dim=0.45, card="vote_a")
    add("SH2", t2, t3, "pov", src="tuer", frm=1)
    add("SH3", t3, t4, "phone", lock="lock_a", notifs=[["notif_a1", st("a08") - 0.35, 700]], buzz=[capt("a07", 1) - 0.1, capt("a07", 1) + 0.3])
    add("SH4", t4, t5, "chat", img="chat_a", scroll=[capt("a09", 0) + 0.3, capt("a09", 1) + 0.2])
    # Spuren erscheinen nacheinander von der Tür bis zur Kasse (ab „nasse Fußspuren“ bis zum Ende von „wo du stehst“)
    add("SH5", t5, t6, "prints", src="t1r1", frm=1, loop=True, cam="CAM 01  EINGANG", clock=C(2, 50, 12), reveal=[capt("a12", 1), en("a15") - 0.2],
        zoom=[st("a14"), en("a15"), 1.0, 1.3])
    ev["flicker"] = [capt("a16", 1) - 0.25, en("a16") + 0.1]      # „GEHT AUS“: Flackern, dann schwarz
    add("SH6", t6, t7, "prints", src="t1r1", frm=40, loop=True, cam="CAM 01  EINGANG", clock=C(2, 50, 31), reveal="all", out=ev["flicker"])
    add("SH7", t7, t8, "ir", cam="CAM 01  EINGANG", clock=C(2, 50, 36), zoom=[t7, t8, 1.0, 1.18])
    add("SH8", t8, D, "decision", base="ir", cam="CAM 01  EINGANG", clock=C(2, 50, 39), cards=["card_a_A", "card_a_B"],
        card_t=[st("a18"), capt("a18", 1)], end=en("a19") + 0.45)
    ev["door_open"] = capt("a04", 2) - 0.1     # „DIE TÜR GEHT AUF“
    ev["unlock"] = capt("a04", 1) - 0.2        # Schlüssel
    ev["door_close"] = st("a07") + 0.1         # „Du schließt wieder ab“
    ev["breath"] = [t7 + 0.1, D - 0.5]
    ev["final"] = en("a19") + 0.45
    # Ich-Sicht: Bildzahl und Türbeginn für Blender
    n_tuer = int(round((t3 - t2) * 10)) + 2
    door_start = int((ev["door_open"] - t2) * 10) + 1
    sp = os.path.join(HERE, "build", "shots.json")
    cfg = json.load(open(sp)) if os.path.exists(sp) else {}
    cfg["tuer"] = {"frames": n_tuer, "door_start": door_start}
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    json.dump(cfg, open(sp, "w"), indent=1)
    print(f"Ich-Sicht „tuer“: {n_tuer} Bilder, Tür geht ab Bild {door_start} auf")
else:
    t1 = st("b02") - 0.35
    t2 = st("b04") - 0.25
    t3 = st("b06") - 0.3
    t4 = st("b08") - 0.25
    t4b = capt("b09", 2) - 0.1             # „ER IST WEG“
    t5 = st("b10") - 0.2
    t6 = st("b11") - 0.2
    t7 = st("b14") - 0.25
    t8 = st("b17") - 0.3
    add("SH0", 0, t1, "cctv", src="lager", frm=30, loop=True, cam="CAM 02  LAGER", clock=C(2, 51, 47), zoom=[0.0, t1, 1.0, 1.3], title=True)
    add("SH1", t1, t2, "vote", src="t1r3", frm=JUMP + 6, loop=True, cam="CAM 01  EINGANG", clock=C(2, 47, 40), dim=0.45, card="vote_b")
    add("SH2", t2, t3, "cctv", src="t1r3", frm=JUMP + 10, loop=True, cam="CAM 01  EINGANG", clock=C(2, 47, 46))
    add("SH3", t3, t4, "phone", lock="lock_b", notifs=[["notif_b1", st("b07") - 0.25, 700], ["notif_b2", capt("b07", 1) - 0.2, 940]],
        buzz=[st("b06") + 0.05, st("b06") + 0.45])
    add("SH4", t4, t4b, "cctv", src="t1r3", frm=JUMP + 30, loop=True, cam="CAM 01  EINGANG", clock=C(2, 48, 31))
    add("SH4b", t4b, t5, "cctv", src="t1r1", frm=1, loop=True, cam="CAM 01  EINGANG", clock=C(2, 48, 37))
    add("SH5", t5, t6, "cctv", src="t1r2", frm=FIG_GONE + 3, loop=True, cam="CAM 03  ZAPFSÄULEN", clock=C(2, 48, 41))
    add("SH6", t6, t7, "cctv", src="lager", frm=1, loop=True, cam="CAM 02  LAGER", clock=C(2, 48, 45), zoom=[st("b12"), st("b13"), 1.0, 1.45])
    add("SH7", t7, t8, "note", keys=[[r(st("b14")), "all"], [r(st("b15")), "Regel 5a"], [r(capt("b15", 2)), "Regel 5b"], [r(st("b16")), "Versteck"]])
    add("SH8", t8, D, "decision", base="lager", src="lager", frm=50, loop=True, cam="CAM 02  LAGER", clock=C(2, 49, 20), dim=0.5,
        cards=["card_b_A", "card_b_B"], card_t=[st("b17"), capt("b17", 2)], end=en("b18") + 0.45)
    ev["knocks"] = [en("b05") + 0.35, en("b05") + 0.65, en("b05") + 0.95]
    ev["knock_stop"] = st("b08")
    ev["final"] = en("b18") + 0.45
json.dump({"zweig": Z, "duration": r(D), "fps_src": 10, "events": ev, "shots": shots}, open(os.path.join(B, "edl.json"), "w"),
          indent=1, ensure_ascii=False)
print(f"Fassung {Z.upper()}: {D:.1f} s")
for s in shots:
    print(f"  {s['id']:5s} {s['t'][0]:6.2f} – {s['t'][1]:6.2f}  {s['kind']}")

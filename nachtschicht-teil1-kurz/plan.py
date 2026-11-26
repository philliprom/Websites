"""Schnittplan für Teil 1 (kurz) aus den Sprechzeiten nach emotion.py → build/edl.json.
Alle Bilder aus Teil 1: t1r1 = CAM 01 leer, t1r2 = CAM 03 (Gestalt im Regen, verschwindet), t1r3 = CAM 01 Stromausfall/Sprung/
Gestalt an der Tür, Zettel = nachtschicht-teil1/build/note/zettel.png.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
tl = json.load(open(os.path.join(B, "timeline.json"), encoding="utf-8"))
SEG = {s["id"]: s for s in tl["segments"]}
D = tl["duration"]
st = lambda i: SEG[i]["start"]      # noqa: E731
en = lambda i: SEG[i]["speechEnd"]  # noqa: E731


def capt(i, k):
    c = SEG[i]["caps"]
    return c[k]["start"] if k < len(c) else st(i)


r = lambda x: round(x, 3)  # noqa: E731
T1 = json.load(open(os.path.join(HERE, "..", "nachtschicht-teil1", "build", "shots.json"), encoding="utf-8"))
JUMP, FIG_GONE = T1["r3"]["jump"], T1["r2"]["fig_out"]
FIG2 = json.load(open(os.path.join(HERE, "..", "nachtschicht-teil1", "build", "r2", "figure.json")))
DOOR = [250, 360]                       # Gestalt an der Glastür im CAM-01-Bild (Quelle 432×768)
C = lambda h, m, s=0: h * 3600 + m * 60 + s  # noqa: E731
shots, ev = [], {}


def add(id_, a, b, kind, **kw):
    shots.append(dict(id=id_, t=[r(a), r(b)], kind=kind, **kw))


t1 = st("k02") - 0.15
t2 = st("k04") - 0.12
t3 = st("k06") - 0.12
t4 = st("k07") - 0.1
t5 = st("k08") - 0.15
# Haken: aus dem Dunkeln (Stromausfall) springt das Bild auf die Gestalt an der Tür, dreimal Klopfen
add("SH0", 0, t1, "cctv", src="t1r3", frm=JUMP - 2, cam="CAM 01  EINGANG", clock=C(2, 47, 3), focus=DOOR,
    zoom=[0.0, t1, 1.35, 1.7], hook=True)
add("SH1", t1, t2, "note", keys=[[r(st("k02")), "Regel 4"], [r(st("k03")), "Rot"]])
# CAM 03: Gestalt steht im Regen und ist bei „Dann war er weg“ verschwunden
gone_at = st("k05") + 0.35
frm2 = max(1, FIG_GONE - int((gone_at - t2) * 10))
add("SH2", t2, t3, "cctv", src="t1r2", frm=frm2, cam="CAM 03  ZAPFSÄULEN", clock=C(2, 42, 11), focus=[FIG2["x"], FIG2["y"]],
    zoom=[t2, gone_at, 1.25, 1.7])
add("SH3", t3, t4, "cctv", src="t1r3", frm=JUMP + 12, loop=True, cam="CAM 01  EINGANG", clock=C(2, 47, 12), focus=DOOR,
    zoom=[t3, t4, 1.3, 1.85])
add("SH4", t4, t5, "phone", lock="phone_bg", notifs=[["notif1", capt("k07", 1) - 0.15, 700]], buzz=[st("k07") + 0.05])
add("SH5", t5, D, "decision", base="cctv", src="t1r3", frm=JUMP + 20, loop=True, cam="CAM 01  EINGANG", clock=C(2, 47, 20),
    dim=0.5, cards=["cardA", "cardB"], card_t=[st("k08") + 0.15, st("k08") + 0.55], end=en("k09") + 1.0, end_text="TEIL 2 FOLGT")
ev["hook_knocks"] = [0.3, 0.58, 0.86]
ev["jump"] = 0.2
ev["gone"] = gone_at
ev["door_knocks"] = [t3 + 0.25, t3 + 0.53, t3 + 0.81]
ev["final_knock"] = en("k09") + 1.0
json.dump({"duration": r(D), "fps_src": 10, "events": ev, "shots": shots}, open(os.path.join(B, "edl.json"), "w"), indent=1, ensure_ascii=False)
print(f"Kurz: {D:.1f} s")
for s in shots:
    print(f"  {s['id']}  {s['t'][0]:5.2f} – {s['t'][1]:5.2f}  {s['kind']}")

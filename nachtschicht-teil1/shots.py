"""Plant den Schnitt aus den Sprechzeiten (build/timeline.json) und schreibt
  build/shots.json  – Bildzahl und Ereignisse je Blender-Einstellung (r1, r2, r3) für scene.py
  build/edl.json    – Einstellungen im fertigen Video (Start/Ende in Sekunden, Quelle, Uhrzeit der Kamera, Ereignisse)
Aufruf: python3 nachtschicht-teil1/shots.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
FPS = 10  # Überwachungskamera: 10 Bilder pro Sekunde
tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
SEG = {s["id"]: s for s in tl["segments"]}
D = tl["duration"]


def st(i):
    return SEG[i]["start"]


def en(i):
    return SEG[i]["speechEnd"]


def capt(i, k):
    c = SEG[i]["caps"]
    return c[k]["start"] if k < len(c) else st(i)


r = lambda x: round(x, 3)  # noqa: E731
# ---------------------------------------------------------------- Einstellungen im Video
sh = {}
sh["SH0"] = (0.0, st("s02") - 0.3)                       # Haken: Gestalt an der Tür
sh["SH1"] = (sh["SH0"][1], st("s03") - 0.15)             # Schwarz „02:39“
sh["SH2"] = (sh["SH1"][1], st("s05") - 0.2)              # CAM 01 leer
sh["SH3"] = (sh["SH2"][1], st("s11") - 0.25)             # Regel-Zettel
sh["SH4"] = (sh["SH3"][1], capt("s12", 1) - 0.05)        # CAM 01 Licht flackert (Wechsel bei „Kamera drei“)
sh["SH5"] = (sh["SH4"][1], en("s15") + 0.6)             # CAM 03 Gestalt, Flackern, weg
sh["SH6"] = (sh["SH5"][1], st("s17") - 0.2)              # CAM 01 Stromausfall, Sprung, Klopfen
sh["SH7"] = (sh["SH6"][1], st("s19") - 0.3)              # Handy
sh["SH8"] = (sh["SH7"][1], D)                            # Entscheidung

T6 = sh["SH6"][0]
EV = {
    "hook_knocks": [0.08, 0.36, 0.64],
    "flicker_sh4": capt("s11", 1) - 0.1,                  # „Das Licht flackert“
    "cam3_flicker": st("s14") + 0.35,                     # „Das Licht flackert wieder“
    "dips": [T6 + 0.5, T6 + 0.8],
    "blackout": [T6 + 1.0, T6 + 1.6],
    "jump": T6 + 1.6,
    "knocks": [T6 + 2.45, T6 + 2.72, T6 + 2.99],
    "phone_buzz": [sh["SH7"][0] + 0.15, sh["SH7"][0] + 0.55],
    "msg1": capt("s17", 1) - 0.1,
    "msg2": min(st("s18") + 0.9, st("s19") - 1.0),
    "cards": [capt("s19", 0), capt("s19", 1)],
    "final_knock": D - 1.0,
}
assert EV["knocks"][-1] + 0.3 < st("s16"), "Klopfen muss vor „Er klopft dreimal“ liegen"

# ---------------------------------------------------------------- Blender-Einstellungen
def frames(a, b):
    return int(round((b - a) * FPS)) + 2


n2 = frames(*sh["SH2"])
n4 = frames(*sh["SH4"])
fl0 = n2 + int((EV["flicker_sh4"] - sh["SH4"][0]) * FPS)     # erstes Flackerbild in r1
r1 = {"frames": n2 + n4, "dips": [fl0 + 3, fl0 + 4], "blackout": None, "jump": None,
      "flick5": [fl0, fl0 + 1, fl0 + 2, fl0 + 5, fl0 + 7, fl0 + 8, fl0 + 12, fl0 + 15, fl0 + 16], "canopy_off": [], "fig_out": 0}
n5 = frames(*sh["SH5"])
c0 = int((EV["cam3_flicker"] - sh["SH5"][0]) * FPS) + 1
r2 = {"frames": n5, "dips": [], "blackout": None, "jump": None, "flick5": [],
      "canopy_off": [c0, c0 + 1, c0 + 3, c0 + 4, c0 + 5], "fig_out": c0 + 4}
n6 = frames(*sh["SH6"])
f6 = lambda t: int((t - T6) * FPS) + 1  # noqa: E731
r3 = {"frames": n6, "dips": [f6(x) for x in EV["dips"]], "blackout": [f6(EV["blackout"][0]), f6(EV["blackout"][1]) - 1],
      "jump": f6(EV["jump"]), "flick5": [f6(EV["jump"]) + k for k in (9, 10, 24, 25, 26, 38, 51)], "canopy_off": [], "fig_out": 0}
json.dump({"r1": r1, "r2": r2, "r3": r3}, open(os.path.join(BUILD, "shots.json"), "w"), indent=1)

# ---------------------------------------------------------------- Schnittliste
CLOCK = {  # Uhrzeit der Kamera beim Start der Einstellung (Sekunden nach Mitternacht)
    "SH0": 2 * 3600 + 47 * 60 + 31, "SH2": 2 * 3600 + 39 * 60 + 31, "SH4": 2 * 3600 + 44 * 60 + 6,
    "SH5": 2 * 3600 + 44 * 60 + 11, "SH6": 2 * 3600 + 46 * 60 + 58, "SH8": 2 * 3600 + 47 * 60 + 20,
}
jump_frame = r3["jump"]
edl = {
    "duration": r(D), "fps_src": FPS, "events": {k: ([r(x) for x in v] if isinstance(v, list) else r(v)) for k, v in EV.items()},
    "shots": [
        {"id": "SH0", "t": [r(x) for x in sh["SH0"]], "kind": "cctv", "src": "r3", "from": jump_frame + 4, "cam": "CAM 01  EINGANG", "clock": CLOCK["SH0"], "title": True},
        {"id": "SH1", "t": [r(x) for x in sh["SH1"]], "kind": "black", "text": "02:39"},
        {"id": "SH2", "t": [r(x) for x in sh["SH2"]], "kind": "cctv", "src": "r1", "from": 1, "cam": "CAM 01  EINGANG", "clock": CLOCK["SH2"]},
        {"id": "SH3", "t": [r(x) for x in sh["SH3"]], "kind": "note",
         "keys": [[r(st("s05")), "all"], [r(st("s06")), "Regel 1"], [r(st("s07")), "Regel 2"], [r(st("s08")), "Regel 3"],
                  [r(st("s09")), "Regel 4"], [r(st("s10")), "Rot"]],
         # Zwischenschnitt bei Regel 3 („steht draußen jemand still im Regen“): der leere Platz auf Kamera 3
         "cuts": [{"t": [r(capt("s08", 1) - 0.05), r(capt("s08", 3) - 0.1)], "src": "r2", "from": r2["fig_out"] + 2, "loop": True,
                   "cam": "CAM 03  ZAPFSÄULEN", "clock": 2 * 3600 + 41 * 60 + 2},
                  # bei Regel 4 („Er klopft dreimal“): die leere Eingangstür, leises Klopfen – niemand da
                  {"t": [r(capt("s09", 1) - 0.05), r(capt("s09", 2) - 0.1)], "src": "r1", "from": 20, "loop": True,
                   "cam": "CAM 01  EINGANG", "clock": 2 * 3600 + 41 * 60 + 40, "knock": True}]},
        {"id": "SH4", "t": [r(x) for x in sh["SH4"]], "kind": "cctv", "src": "r1", "from": n2 + 1, "cam": "CAM 01  EINGANG", "clock": CLOCK["SH4"]},
        {"id": "SH5", "t": [r(x) for x in sh["SH5"]], "kind": "cctv", "src": "r2", "from": 1, "cam": "CAM 03  ZAPFSÄULEN", "clock": CLOCK["SH5"],
         "zoom": [r(capt("s13", 0)), r(capt("s13", 0) + 2.2), 1.75]},
        {"id": "SH6", "t": [r(x) for x in sh["SH6"]], "kind": "cctv", "src": "r3", "from": 1, "cam": "CAM 01  EINGANG", "clock": CLOCK["SH6"]},
        {"id": "SH7", "t": [r(x) for x in sh["SH7"]], "kind": "phone"},
        {"id": "SH8", "t": [r(x) for x in sh["SH8"]], "kind": "cctv", "src": "r3", "from": jump_frame + 8, "loop": True, "dim": 0.5,
         "cam": "CAM 01  EINGANG", "clock": CLOCK["SH8"], "cards": True},
    ],
}
json.dump(edl, open(os.path.join(BUILD, "edl.json"), "w"), indent=1, ensure_ascii=False)
tot = r1["frames"] + r2["frames"] + r3["frames"]
print(f"Dauer {D:.1f} s · Bilder r1 {r1['frames']} · r2 {r2['frames']} · r3 {r3['frames']} · zusammen {tot}")
for s_ in edl["shots"]:
    print(f"  {s_['id']}  {s_['t'][0]:6.2f} – {s_['t'][1]:6.2f}  {s_['kind']}")

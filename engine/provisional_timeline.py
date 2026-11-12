#!/usr/bin/env python3
"""Vorläufige Zeitleiste ohne Sprachausgabe, um Szenen schon zu prüfen, während die Stimme noch eingesprochen wird.

  python3 engine/provisional_timeline.py <projekt>
  node engine/render.cjs <projekt> --stills 1.0,5.5,12

Schätzt die Satzlängen (0,06 s pro Zeichen) und schreibt build/timeline.json und build/timeline.js.
build_timeline.py überschreibt beide Dateien später mit den echten Zeiten.
"""
import json
import os
import sys

P = sys.argv[1]
sc = json.load(open(os.path.join(P, "script.json"), encoding="utf-8"))


def caption_chunks(caps, start, dur):
    weights = [len(c.replace("^", "").replace("!", "").replace("~", "")) + 3 for c in caps]
    total, out, t = sum(weights), [], start
    for c, w in zip(caps, weights):
        words = []
        for raw in c.split(" "):
            style = "w"
            if raw.startswith("^"):
                style, raw = "g", raw[1:]
            elif raw.startswith("!"):
                style, raw = "r", raw[1:]
            elif raw.startswith("~"):
                style, raw = "y", raw[1:]
            words.append([raw, style])
        out.append({"start": round(t, 3), "words": words})
        t += dur * w / total
    return out


t, segs = sc["lead_in"], []
for i, s in enumerate(sc["segments"]):
    if i:
        t += s.get("gap", sc["default_gap"])
    dur = max(0.8, len(s["say"]) * 0.06)
    segs.append({"id": s["id"], "say": s["say"], "start": round(t, 3), "speechEnd": round(t + dur, 3), "caps": caption_chunks(s["caps"], t, dur),
                 "sfx": [[n, round((t + dur + float(o[1:])) if isinstance(o, str) else (t + o), 3)] for n, o in s.get("sfx", [])]})
    t += dur
total = t + sc["tail"]
for i, s in enumerate(segs):
    s["end"] = segs[i + 1]["start"] if i + 1 < len(segs) else round(total, 3)
tl = {"fps": 30, "duration": round(total, 3), "segments": segs, "env": [0.0] * int(total * 30 + 1)}
os.makedirs(os.path.join(P, "build"), exist_ok=True)
open(os.path.join(P, "build", "timeline.js"), "w", encoding="utf-8").write("window.TL = " + json.dumps(tl, ensure_ascii=False) + ";\n")
json.dump(tl, open(os.path.join(P, "build", "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("vorläufig", round(total, 1), "s")

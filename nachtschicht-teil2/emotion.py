"""Mehr Gefühl in der Erzählerstimme (Wunsch nach Hörprobe 3: „geht in die richtige Richtung, wenn es spannend wird gern
noch ein Ticken mehr“). Jeder Satz wird nach seiner Spannungsstufe (script.json „spannung“ 0–3) per PSOLA (Praat)
angehoben: höher, etwas schneller, lebendigere Satzmelodie, ab Stufe 2 zum Satzende hin steigend. Die Klangfarbe bleibt.
Weil die Sätze dabei kürzer werden, wird die Zeitleiste neu gesetzt (Pausen zwischen den Sätzen bleiben gleich).
  <vx>/bin/python nachtschicht-teil2/emotion.py a|b
Liest <zweig>/build/vo.wav + timeline.json (beim ersten Lauf als vo_roh.wav / timeline_roh.json gesichert, danach immer
davon ausgehend) und schreibt vo.wav + timeline.json neu.
"""
import json
import os
import shutil
import sys

import numpy as np
import parselmouth
import soundfile as sf
from parselmouth.praat import call

HERE = os.path.dirname(os.path.abspath(__file__))
# Stufe -> (Halbtöne, Dauerfaktor, Tonumfang, Anstieg zum Satzende in Halbtönen). Hörprobe 3 hatte 1/2/3 Halbtöne,
# 0,97/0,93/0,90, Umfang 1,08/1,15/1,25, Anstieg 0/0,5/1,5 – hier „ein Ticken mehr“.
STUFE = {0: (0.0, 1.0, 1.0, 0.0), 1: (1.5, 0.96, 1.1, 0.0), 2: (2.8, 0.92, 1.2, 0.6), 3: (4.0, 0.88, 1.32, 1.5)}


def psola(wav, sr, semitones=0.0, dur=1.0, range_=1.0, rise=0.0):
    snd = parselmouth.Sound(np.asarray(wav, dtype=np.float64), sampling_frequency=sr)
    T = snd.get_total_duration()
    man = call(snd, "To Manipulation", 0.01, 60, 300)
    pt = call(man, "Extract pitch tier")
    n = call(pt, "Get number of points")
    if n > 2 and (semitones or range_ != 1 or rise):
        ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
        fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
        lm = np.median(np.log2(fs))
        new = 2 ** (lm + (np.log2(fs) - lm) * range_ + (semitones + rise * ts / T) / 12)
        call(pt, "Remove points between", 0, T)
        for t_, f_ in zip(ts, new):
            call(pt, "Add point", float(t_), float(f_))
        call([man, pt], "Replace pitch tier")
    if abs(dur - 1) > 1e-3:
        dt = call("Create DurationTier", "d", 0, T)
        call(dt, "Add point", 0, dur)
        call([man, dt], "Replace duration tier")
    return np.asarray(call(man, "Get resynthesis (overlap-add)").values[0], dtype=np.float32)


def main(zweig):
    P = os.path.join(HERE, zweig)
    B = os.path.join(P, "build")
    for a, b in (("vo.wav", "vo_roh.wav"), ("timeline.json", "timeline_roh.json")):
        if not os.path.exists(os.path.join(B, b)):
            shutil.copy(os.path.join(B, a), os.path.join(B, b))
    vo, sr = sf.read(os.path.join(B, "vo_roh.wav"), dtype="float32")
    tl = json.load(open(os.path.join(B, "timeline_roh.json"), encoding="utf-8"))
    sp = {s["id"]: s.get("spannung", 0) for s in json.load(open(os.path.join(P, "script.json"), encoding="utf-8"))["segments"]}
    segs = tl["segments"]
    tail = tl["duration"] - segs[-1]["speechEnd"]
    parts, out = [], []
    t = segs[0]["start"]
    for i, s in enumerate(segs):
        if i > 0:
            t += s["start"] - segs[i - 1]["speechEnd"]   # Pause wie vorher
        a = vo[int(s["start"] * sr):int(s["speechEnd"] * sr)]
        lvl = sp.get(s["id"], 0)
        b = psola(a, sr, *STUFE[lvl]) if lvl else a
        k = (len(b) / sr) / max(1e-6, s["speechEnd"] - s["start"])
        ns = dict(s, start=round(t, 3), speechEnd=round(t + len(b) / sr, 3), spannung=lvl,
                  caps=[dict(c, start=round(t + (c["start"] - s["start"]) * k, 3)) for c in s["caps"]])
        out.append(ns)
        parts.append((t, b))
        t += len(b) / sr
    total = t + tail
    for i, s in enumerate(out):
        s["end"] = out[i + 1]["start"] if i + 1 < len(out) else round(total, 3)
    y = np.zeros(int(total * sr) + sr, np.float32)
    for t0, b in parts:
        y[int(t0 * sr):int(t0 * sr) + len(b)] += b
    y = y[:int(total * sr)]
    y = y / max(1e-6, np.abs(y).max()) * 0.9
    sf.write(os.path.join(B, "vo.wav"), y, sr, subtype="PCM_16")
    tl.update(duration=round(total, 3), segments=out)
    tl.pop("env", None)
    json.dump(tl, open(os.path.join(B, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Zweig {zweig}: {tl_dur(tl)} · vorher {json.load(open(os.path.join(B, 'timeline_roh.json')))['duration']:.1f} s")
    for s in out:
        print(f"  {s['id']} St.{s['spannung']} {s['start']:6.2f}–{s['speechEnd']:6.2f}  {s['say']}")


def tl_dur(tl):
    return f"{tl['duration']:.1f} s"


if __name__ == "__main__":
    main(sys.argv[1])

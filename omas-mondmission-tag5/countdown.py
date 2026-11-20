"""Misst in build/vo.wav, wann Oma im Satz s06 „Drei! Zwei! Eins! Los!“ die vier Wörter beginnt (Lautstärke-Einsätze).
Schreibt build/countdown.json (Zeiten relativ zum Satzanfang). Danach make_script.py noch einmal ausführen: Piepser und
Countdown-Zahlen liegen dann genau auf den Wörtern.
Aufruf: python3 omas-mondmission-tag5/countdown.py
"""
import json
import os
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(os.path.join(HERE, "build", "timeline.json"), encoding="utf-8"))
seg = next(s for s in tl["segments"] if s["id"] == "s06")
with wave.open(os.path.join(HERE, "build", "vo.wav"), "rb") as w:
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1:
        a = a.reshape(-1, w.getnchannels()).mean(axis=1)
i0, i1 = int(seg["start"] * sr), int(seg["speechEnd"] * sr)
x = a[i0:i1]
hop = int(sr * 0.01)
rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-12) for i in range(0, len(x) - hop, hop)])
db = 20 * np.log10(rms + 1e-9)
thr = db.max() - 28
voiced = db > thr
# Einsätze: Übergang leise -> laut nach mindestens 60 ms Pause, kurze Lücken schließen
onsets, quiet = [], 99
for i, v in enumerate(voiced):
    if v and quiet >= 6:
        onsets.append(i * 0.01)
    quiet = 0 if v else quiet + 1
print("Einsätze (s):", onsets)
if len(onsets) < 4:
    raise SystemExit("Weniger als 4 Wörter erkannt, Countdown bleibt bei den Untertitel-Zeiten.")
if len(onsets) > 4:
    # die vier längsten Pausen davor behalten: erstes Wort plus die drei Einsätze nach den längsten Lücken
    gaps = sorted(range(1, len(onsets)), key=lambda k: onsets[k] - onsets[k - 1], reverse=True)[:3]
    onsets = [onsets[0]] + [onsets[k] for k in sorted(gaps)]
json.dump([round(v, 3) for v in onsets], open(os.path.join(HERE, "build", "countdown.json"), "w"))
print("Countdown:", onsets)

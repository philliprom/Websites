"""Endkontrolle: jede Zeile im fertigen Video (mit Alarm, Musik, Effekten) per Whisper prüfen.

  QA_WHISPER=<whisper-medium> <vx>/bin/python aussprache_endmix.py <folgen-ordner> [video.mp4]

Gibt jede Abweichung vom Sprechtext aus. Ziel: alle Zeilen exakt (Schreibweisen wie Pohl/Pol zählen nicht).
Typische Ursachen und Abhilfe stehen in references/stimmen.md.
"""
import json
import os
import subprocess
import sys
import tempfile

import soundfile as sf

ordner = os.path.abspath(sys.argv[1])
sys.path.insert(0, ordner)
import asr  # noqa: E402
from story import LINES  # noqa: E402

if len(sys.argv) > 2:
    video = sys.argv[2]
else:
    vids = sorted(f for f in os.listdir(os.path.join(ordner, "out")) if f.endswith(".mp4") and not f.startswith("probe"))
    video = os.path.join(ordner, "out", vids[0])
tmp = os.path.join(tempfile.mkdtemp(), "a16.wav")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-ac", "1", "-ar", "16000", tmp],
               check=True)
w, sr = sf.read(tmp, dtype="float32")
tl = json.load(open(os.path.join(ordner, "timeline.json"), encoding="utf-8"))
say = {l["id"]: l["say"] for l in LINES}
bad = 0
for l in tl["lines"]:
    seg = w[int(max(0, l["start"] - 0.1) * sr):int((l["end"] + 0.15) * sr)]
    hyp = asr.asr(seg, sr)
    if asr.norm(hyp) != asr.norm(say[l["id"]]):
        bad += 1
        print(f'Abweichung {l["id"]:5} {l["who"]:9} | gehört: {hyp} | soll: {say[l["id"]]}')
print(f'{len(tl["lines"]) - bad} von {len(tl["lines"])} Zeilen exakt erkannt')

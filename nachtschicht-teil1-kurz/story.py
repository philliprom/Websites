"""Nachtschicht – Teil 1, KURZE Fassung (ca. 30 s). Die lange Fassung (79 s) lief schwach: 61 bzw. 275 Aufrufe,
2–8 % Likes, kaum Kommentare – der Anfang war zu ruhig, das Klopfen kam erst nach ~45 s.
Neu: Sekunde 0 die Gestalt an der Tür + dreimal Klopfen, dann in schnellen Schnitten die Geschichte, am Ende A/B.
Bilder komplett aus Teil 1 (keine neuen Renderings), Stimme neu (kurze Sätze), schneller und mit Gefühl (emotion.py).
Erzeugt script.json für engine/build_timeline.py.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# (id, Text, Untertitel, Pause davor, Spannung)
S = [
    ("k01", "Er klopft dreimal.", ["ER KLOPFT ^DREIMAL."], 0.0, 2),
    ("k02", "Regel vier vom Chef: Mach niemals auf.", ["REGEL 4 VOM CHEF:", "MACH ^NIEMALS AUF."], 0.35, 2),
    ("k03", "Egal, wer es sagt.", ["„^EGAL, ^WER ^ES ^SAGT.“"], 0.2, 3),
    ("k04", "Vor fünf Minuten stand er noch draußen. Im Regen.", ["VOR FÜNF MINUTEN", "STAND ER NOCH ^DRAUSSEN.", "IM REGEN."], 0.35, 1),
    ("k05", "Dann war er weg.", ["DANN WAR ER ^WEG."], 0.2, 2),
    ("k06", "Jetzt steht er an deiner Tür.", ["JETZT STEHT ER", "AN ^DEINER ^TÜR."], 0.3, 3),
    ("k07", "Und dein Chef schreibt: Mach die Tür auf. Sofort.", ["UND DEIN CHEF SCHREIBT:", "„MACH DIE TÜR AUF.", "^SOFORT.“"], 0.45, 2),
    ("k08", "Machst du auf?", ["MACHST DU ^AUF?"], 0.35, 2),
    ("k09", "Schreib A oder B.", ["SCHREIB ^A ODER ^B."], 0.25, 0),
]
segments = [{"id": i, "say": say, "caps": caps, "gap": gap, "sfx": [], "spannung": sp} for i, say, caps, gap, sp in S]
script = {"title": "Nachtschicht – Teil 1 (kurz)", "lead_in": 0.35, "tail": 1.6, "default_gap": 0.25,
          "tts": {"engine": "qwen", "voice": "../nachtschicht-teil1/voice/horror.wav", "voice_text": "../nachtschicht-teil1/voice/horror.txt",
                  "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.7, "max_pause": 0.22},
          "segments": segments}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
print(f"script.json: {len(segments)} Sätze, {sum(len(s['say']) for s in segments)} Zeichen")

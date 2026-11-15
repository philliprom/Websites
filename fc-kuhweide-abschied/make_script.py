"""Abschied: FC Kuhweide geht in die Winterpause. Erzeugt script.json, kader.js und out/beschreibung.txt.
Aufruf: python3 fc-kuhweide-abschied/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))
n = len(K["namen"])
segments = [
    {"id": "s01", "say": "Danke an alle, die beim FC Kuhweide mitgespielt haben!", "caps": ["DANKE AN ALLE,", "DIE BEIM FC KUHWEIDE", "^MITGESPIELT HABEN!"], "gap": 0.0,
     "sfx": [["cheer", 0.1], ["drum", 0.6]]},
    {"id": "s02", "say": "Und an die drei, die gestern gefehlt haben:", "caps": ["UND AN DIE DREI,", "DIE GESTERN ^GEFEHLT HABEN:"], "gap": 2.6,
     "sfx": [["whoosh", -0.05], ["blip", 0.3], ["blip", 0.7], ["blip", 1.1]]},
    {"id": "s03", "say": "Jamie, Noel und Kilian: Ihr seid im Ehrenkader!", "caps": ["^JAMIE, ^NOEL UND ^KILIAN:", "IHR SEID IM ^EHRENKADER!"], "gap": 0.1,
     "sfx": [["stamp", "e-0.9"], ["stamp", "e-0.6"], ["stamp", "e-0.3"], ["cheer", "e-0.2"]]},
    {"id": "s04", "say": "Jetzt geht der FC Kuhweide in die Winterpause.", "caps": ["JETZT GEHT DER FC KUHWEIDE", "IN DIE ^WINTERPAUSE."], "gap": 1.0,
     "sfx": [["whoosh", -0.05], ["sparkle", 0.3]]},
    {"id": "s05", "say": "Berta passt so lange auf das Tor auf.", "caps": ["^BERTA PASST SO LANGE", "AUF DAS TOR AUF."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["moo", "e+0.1"]]},
    {"id": "s06", "say": f"Danke für hundertzweiundzwanzig Fans!", "caps": ["DANKE FÜR", f"^{K['fans']} FANS!"], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["pop", 0.1], ["confetti", 0.15], ["ding", "e+0.2"]]},
]
script = {
    "title": "FC Kuhweide – Winterpause", "voice": "voxcpm2", "lead_in": 0.1, "tail": 2.2, "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt", "cfg": 2.0, "steps": 10},
    "music": {"bpm": 96, "inst": "vibes", "clap": 0.6, "ambience": 0.2,
              "chords": [[60, 64, 67, 72], [57, 60, 64, 69], [65, 69, 72, 77], [67, 71, 74, 79]], "roots": [48, 45, 41, 43], "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = (f"Danke für {K['fans']} Fans ❤️ Der FC Kuhweide geht in die Winterpause ❄️ Ist dein Name im Abspann? 👀 "
       "#fckuhweide #danke #winterpause #fußball #kreisliga")
pin = "📌 Danke an alle, die mitgespielt haben ❤️ Berta passt aufs Tor auf, bis wir wiederkommen 🐄❄️"
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – ABSCHIED „WINTERPAUSE“ · TEXTE ZUM POSTEN
=========================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTZEIT
Heute, wann es passt. Im Abspann stehen alle {n} Namen aus den Kommentaren.
""")
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(K, ensure_ascii=False) + ";\n")
print(f"Abschied: {len(segments)} Sätze, {n} Namen")

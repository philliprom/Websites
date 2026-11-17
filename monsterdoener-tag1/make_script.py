"""Monsterdöner – Tag 1: Ich habe eine Dönerbude für Monster eröffnet. Erzeugt script.json und out/beschreibung.txt.
Mehrere Sprecher: jedes Segment hat "voice" (leo, vampir, geist, werwolf, zombie), Stimmen in voice/<name>.wav + .txt.
Aufruf: python3 monsterdoener-tag1/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {v: {"voice": f"voice/{v}.wav", "voice_text": f"voice/{v}.txt"} for v in ("leo", "vampir", "geist", "werwolf", "zombie")}
VOICES["geist"]["fx"] = "aecho=0.8:0.7:90|160:0.35|0.22"
VOICES["werwolf"]["fx"] = "rubberband=pitch=0.78:formant=shifted,volume=1.4"
segments = [
    {"id": "s01", "voice": "leo", "say": "Hilfe! Mein erster Kunde will mich beißen!",
     "caps": ["!HILFE!", "MEIN ERSTER KUNDE", "WILL MICH !BEISSEN! 😱"], "gap": 0.0,
     "sfx": [["hiss", -0.1], ["sting", 0.05], ["hiss", "e-0.6"], ["whoosh", "e-0.75"]]},
    {"id": "s02", "voice": "vampir", "say": "Einen Döner. Ohne Knoblauch.",
     "caps": ["EINEN DÖNER.", "!OHNE !KNOBLAUCH."], "gap": 0.5, "sfx": [["scratch", -0.5], ["ding", -0.2]]},
    {"id": "s03", "voice": "leo", "say": "Kommt sofort!",
     "caps": ["KOMMT ^SOFORT!"], "gap": 0.2, "sfx": [["whoosh", -0.05], ["pop", "e+0.05"], ["boing", "e+0.5"]]},
    {"id": "s04", "voice": "vampir", "say": "Hm. Das schmeckt komisch.",
     "caps": ["HM. DAS SCHMECKT …", "!KOMISCH."], "gap": 1.4, "sfx": [["card", -0.6], ["crunch", -0.25]]},
    {"id": "s05", "voice": "leo", "say": "Oh. Knoblauch-Fladenbrot.",
     "caps": ["OH.", "^KNOBLAUCH-", "^FLADENBROT. 😬"], "gap": 0.2, "sfx": [["whoosh", -0.05], ["sting", 0.4]]},
    {"id": "s06", "voice": "vampir", "say": "Neeeein!",
     "caps": ["!NEEEEIN!"], "gap": 0.15,
     "sfx": [["poof", "e+0.05"], ["flap", "e+0.15"], ["flap", "e+0.35"], ["klong", "e+0.55"], ["flap", "e+0.65"], ["crunch", "e+0.9"], ["flap", "e+1.1"]]},
    {"id": "s07", "voice": "leo", "say": "Okay. Ab morgen kein Knoblauch mehr.",
     "caps": ["OKAY. AB MORGEN", "!KEIN KNOBLAUCH MEHR."], "gap": 1.45, "sfx": [["whoosh", -0.05]]},
    {"id": "s08", "voice": "leo", "say": "Und ihr entscheidet, wer als Nächstes kommt!",
     "caps": ["UND IHR ENTSCHEIDET,", "WER ALS ^NÄCHSTES KOMMT!"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 1.2], ["pop", 1.4], ["pop", 1.6], ["ding", "e+0.3"]]},
]
script = {
    "title": "Monsterdöner – Tag 1", "voice": "qwen3-tts (5 Stimmen)", "lead_in": 0.05, "tail": 2.3, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/leo.wav", "voice_text": "voice/leo.txt", "voices": VOICES,
            "tries": 3, "max_wer": 0.08, "candidates": 3, "temperature": 0.7},
    "music": {"bpm": 120, "inst": "pluck", "clap": 0.6, "ambience": 0.15,
              "chords": [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [52, 56, 59, 64]], "roots": [45, 41, 48, 40],
              "arp": [0, 2, 1, 3, 2, 1, 0, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Tag 1 in meiner Dönerbude für Monster: Mein erster Kunde ist ein Vampir 🧛 und ich hab den Knoblauch vergessen 😬 "
       "1 Follower = 1 Kunde. Wer kommt morgen? A Werwolf, B Geist, C Zombie 👇 #döner #monster #tag1 #comedy #fyp")
pin = ("📌 Abstimmung: Wer kommt morgen in den Laden? A 🐺 Werwolf · B 👻 Geist · C 🧟 Zombie. "
       "Schreib den Buchstaben! Wir zählen ehrlich (eine Stimme pro Person), morgen kommt der Sieger.")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Monsterdöner (neues Konto)
MONSTERDÖNER – TAG 1 · TEXTE ZUM POSTEN
=======================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

PROFIL (neues Konto)
Name: Monsterdöner 🧛🥙
Nutzername (Vorschlag, falls frei): @monsterdoener oder @monster.doener
Profilbild: profilbild_logo.png (Alternative: profilbild_leo.png)
Bio: Ich hab eine Dönerbude für Monster eröffnet 🧛🥙 1 Follower = 1 Kunde. Ihr entscheidet, wer kommt!
""")
print(f"Tag 1: {len(segments)} Sätze")

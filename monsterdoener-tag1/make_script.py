"""Monsterdöner – Tag 1: Ich habe eine Dönerbude für Monster eröffnet. Erzeugt script.json und out/beschreibung.txt.
Mehrere Sprecher: jedes Segment hat "voice" (leo, vampir, geist, werwolf, zombie), Stimmen in voice/<name>.wav + .txt.
Aufruf: python3 monsterdoener-tag1/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {v: {"voice": f"voice/{v}.wav", "voice_text": f"voice/{v}.txt"} for v in ("leo", "vampir", "geist", "werwolf", "zombie")}
VOICES["geist"]["fx"] = "aecho=0.8:0.7:90|160:0.35|0.22"
segments = [
    {"id": "s01", "voice": "leo", "say": "Tag eins: Ich habe eine Dönerbude für Monster eröffnet.",
     "caps": ["TAG 1: ICH HABE EINE", "^DÖNERBUDE FÜR ^MONSTER", "ERÖFFNET! 🧛"], "gap": 0.0, "sfx": [["title", -0.1]]},
    {"id": "s02", "voice": "vampir", "say": "Einmal Döner. Aber ohne Knoblauch!",
     "caps": ["EINMAL DÖNER.", "ABER !OHNE !KNOBLAUCH!"], "gap": 0.2, "sfx": [["whoosh", -0.05]]},
    {"id": "s03", "voice": "leo", "say": "Oh. Die Soße ist schon drauf.",
     "caps": ["OH. DIE SOSSE", "IST SCHON ^DRAUF. 😬"], "gap": 0.15, "sfx": [["whoosh", -0.05], ["pop", 0.4]]},
    {"id": "s04", "voice": "vampir", "say": "Neeeein!",
     "caps": ["!NEEEEIN!"], "gap": 0.1, "sfx": [["poof", "e+0.05"], ["flap", "e+0.3"], ["flap", "e+0.6"], ["flap", "e+0.9"]]},
    {"id": "s05", "voice": "geist", "say": "Einmal mit alles, bitte.",
     "caps": ["EINMAL MIT ALLES, BITTE. 👻"], "gap": 1.0, "sfx": [["ding", -0.5], ["whoosh", -0.05]]},
    {"id": "s06", "voice": "geist", "say": "Schon wieder durchgefallen.",
     "caps": ["SCHON WIEDER", "^DURCHGEFALLEN."], "gap": 1.3, "sfx": [["card", -1.25], ["whoosh", -0.85], ["splash", -0.45]]},
    {"id": "s07", "voice": "werwolf", "say": "Döner mit extra Fleisch!",
     "caps": ["DÖNER MIT", "^EXTRA FLEISCH!"], "gap": 0.7, "sfx": [["ding", -0.5], ["whoosh", -0.05], ["riser", "e+0.1"], ["poof", "e+0.75"], ["howl", "e+0.85"]]},
    {"id": "s08", "voice": "zombie", "say": "Mit … alles …",
     "caps": ["MIT … ALLES … 🧟"], "gap": 2.9, "sfx": [["crunch", -1.0], ["ding", -0.5], ["whoosh", -0.05], ["crunch", "e+0.3"]]},
    {"id": "s09", "voice": "leo", "say": "Passt so.",
     "caps": ["PASST SO. 😅"], "gap": 0.75, "sfx": [["whoosh", -0.05]]},
    {"id": "s10", "voice": "leo", "say": "Ein Follower ist ein Kunde. Und ihr entscheidet: Wer kommt morgen?",
     "caps": ["^1 FOLLOWER = ^1 KUNDE.", "UND IHR ENTSCHEIDET:", "WER KOMMT ^MORGEN?"], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["pop", 2.4], ["pop", 2.6], ["pop", 2.8]]},
    {"id": "s11", "voice": "leo", "say": "Oh nein. Die Lebensmittelkontrolle!",
     "caps": ["OH NEIN …", "DIE !LEBENSMITTEL-", "!KONTROLLE!"], "gap": 0.95, "sfx": [["knock", -0.85], ["sting", "e+0.05"]]},
]
script = {
    "title": "Monsterdöner – Tag 1", "voice": "qwen3-tts (5 Stimmen)", "lead_in": 0.15, "tail": 2.2, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/leo.wav", "voice_text": "voice/leo.txt", "voices": VOICES,
            "tries": 3, "max_wer": 0.08, "candidates": 3, "temperature": 0.7},
    "music": {"bpm": 120, "inst": "pluck", "clap": 0.6, "ambience": 0.15,
              "chords": [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [52, 56, 59, 64]], "roots": [45, 41, 48, 40],
              "arp": [0, 2, 1, 3, 2, 1, 0, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Tag 1: Ich habe eine Dönerbude für Monster eröffnet 🧛🥙 1 Follower = 1 Kunde. Ihr entscheidet: Wer kommt morgen? "
       "A Mumie, B Hexe, C Alien 👇 #döner #monster #tag1 #comedy #fyp")
pin = ("📌 Abstimmung: Wer kommt morgen in den Laden? A 🧻 Mumie · B 🧙‍♀️ Hexe · C 👽 Alien. "
       "Schreib den Buchstaben! Wir zählen ehrlich, morgen kommt der Sieger. Und: Was sagt die Lebensmittelkontrolle? 😬")
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

"""Omas Mondmission – Tag 1. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 omas-mondmission-tag1/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Ich bin achtundsiebzig und fliege mit meiner Kuh zum Mond.",
     "caps": ["ICH BIN ^78", "UND FLIEGE MIT MEINER ^KUH", "ZUM ^MOND! 🚀"], "gap": 0.0,
     "sfx": [["title", 0.0], ["sparkle", 0.5]]},
    {"id": "s02", "say": "Die Rakete habe ich aus meinem alten Heizöl-Tank gebaut.",
     "caps": ["DIE RAKETE HABE ICH AUS", "MEINEM ALTEN ^HEIZÖLTANK", "GEBAUT."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.7], ["pop", 1.5], ["pop", 2.3]]},
    {"id": "s03", "say": "Nur Herr Krause vom Gartenverein ist dagegen.",
     "caps": ["NUR ^HERR ^KRAUSE", "VOM GARTENVEREIN", "IST !DAGEGEN."], "gap": 1.0,
     "sfx": [["moo", -0.95], ["scratch", -0.05], ["boing", 0.35]]},
    {"id": "s04", "say": "Der kann mir mal den Buckel runterrutschen!",
     "caps": ["DER KANN MIR MAL", "DEN ^BUCKEL RUNTERRUTSCHEN!"], "gap": 0.35,
     "sfx": [["whoosh", -0.05], ["squeak", "e+0.05"]]},
    {"id": "s05", "say": "Aber der Tank ist noch leer.",
     "caps": ["ABER DER ^TANK", "IST NOCH !LEER."], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["klong", "e+0.05"], ["klong", "e+0.35"]]},
    {"id": "s06", "say": "Jeder Kommentar ist ein Liter Treibstoff.",
     "caps": ["JEDER ^KOMMENTAR", "IST ^1 LITER TREIBSTOFF! ⛽"], "gap": 0.6,
     "sfx": [["card", 0.15], ["gulp", 1.0], ["ding", 1.25]]},
    {"id": "s07", "say": "Bei hundert Litern heben wir ab!",
     "caps": ["BEI ^100 LITERN", "HEBEN WIR ^AB! 🚀"], "gap": 0.2,
     "sfx": [["riser", -0.2], ["rocket", 0.25], ["cheer", "e+0.1"]]},
    {"id": "s08", "say": "Und jeder, der tankt, kommt mit Namen auf die Rakete.",
     "caps": ["UND JEDER, DER TANKT,", "KOMMT MIT ^NAMEN", "AUF DIE ^RAKETE!"], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["brush", 0.45], ["brush", 1.1], ["sparkle", 1.6]]},
    {"id": "s09", "say": "Also: Schreib Tanken!",
     "caps": ["ALSO: SCHREIB", "^„TANKEN“! ⛽"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", "e+0.0"], ["moo", "e+0.6"]]},
]
script = {
    "title": "Omas Mondmission – Tag 1", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.1, "tail": 2.4, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/oma_ref.wav", "voice_text": "voice/oma_ref.txt", "tries": 3, "max_wer": 0.08},
    "music": {"bpm": 104, "inst": "pluck", "clap": 0.5, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")

cap = ("Oma (78) fliegt mit ihrer Kuh zum Mond 🚀🐄 Jeder Kommentar = 1 Liter Treibstoff. Bei 100 Litern heben wir ab! "
       "Schreib TANKEN ⛽ #oma #mondmission #tag1 #kuh #fyp")
pin = ("📌 So geht's: Jeder Kommentar = 1 Liter ⛽ Wir zählen ehrlich. Bei 100 Litern startet die Rakete, "
       "und jeder, der tankt, kommt mit Namen auf die Rakete 🚀 Tank: 0 / 100")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""OMAS MONDMISSION – TAG 1 · TEXTE ZUM POSTEN
============================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

PROFIL UMSTELLEN (direkt vor dem Posten)
Name: Omas Mondmission 🚀
Profilbild: profilbild_duo.png (Oma + Berta, die bisherigen Fans erkennen Berta; Alternative: profilbild_oma.png)
Bio: Oma Gisela (78) & Kuh Berta fliegen zum Mond 🚀 Jeder Kommentar = 1 Liter Treibstoff. Start bei 100!
Danach dieses Video oben anpinnen. Die alten FC-Kuhweide-Videos bleiben online.
""")
print(f"Tag 1: {len(segments)} Sätze")

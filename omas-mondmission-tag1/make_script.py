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
    {"id": "s02", "say": "Mein Heinz ist neunzehnhundertvierundsiebzig zum Mond geflogen. Jetzt hole ich ihn zurück!",
     "caps": ["MEIN ^HEINZ IST ^1974", "ZUM MOND GEFLOGEN.", "JETZT HOLE ICH", "IHN ^ZURÜCK!"], "gap": 0.15,
     "sfx": [["card", -0.05], ["whoosh", 2.6]]},
    {"id": "s03", "say": "Die Rakete habe ich aus seinem alten Heizöl-Tank gebaut.",
     "caps": ["DIE RAKETE HABE ICH AUS", "SEINEM ALTEN ^HEIZÖLTANK", "GEBAUT."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.7], ["pop", 1.5], ["pop", 2.3]]},
    {"id": "s04", "say": "Nur Herr Krause vom Gartenverein ist dagegen.",
     "caps": ["NUR ^HERR ^KRAUSE", "VOM GARTENVEREIN", "IST !DAGEGEN."], "gap": 1.0,
     "sfx": [["moo", -0.95], ["scratch", -0.05], ["boing", 0.35]]},
    {"id": "s05", "say": "Der kann mir mal den Buckel runterrutschen!",
     "caps": ["DER KANN MIR MAL", "DEN ^BUCKEL RUNTERRUTSCHEN!"], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["squeak", "e+0.05"]]},
    {"id": "s06", "say": "Aber der Tank ist noch leer.",
     "caps": ["ABER DER ^TANK", "IST NOCH !LEER."], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["klong", "e+0.05"], ["klong", "e+0.35"]]},
    {"id": "s07", "say": "Jeder Kommentar ist ein Liter Treibstoff.",
     "caps": ["JEDER ^KOMMENTAR", "IST ^1 LITER TREIBSTOFF! ⛽"], "gap": 0.6,
     "sfx": [["card", 0.15], ["gulp", 1.0], ["ding", 1.25]]},
    {"id": "s08", "say": "Bei hundert Litern heben wir ab!",
     "caps": ["BEI ^100 LITERN", "HEBEN WIR ^AB! 🚀"], "gap": 0.2,
     "sfx": [["riser", -0.2], ["rocket", 0.25], ["cheer", "e+0.1"]]},
    {"id": "s09", "say": "Und jeder, der tankt, kommt in meine Bodenkontrolle.",
     "caps": ["UND JEDER, DER TANKT,", "KOMMT IN MEINE", "^BODENKONTROLLE!"], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["brush", 0.6], ["brush", 1.2], ["sparkle", 1.9]]},
    {"id": "s10", "say": "Und ganz unten steht: Vorsicht vor den … was?!",
     "caps": ["UND GANZ UNTEN STEHT:", "!VORSICHT VOR DEN …", "^WAS?!"], "gap": 0.4,
     "sfx": [["card", -0.1], ["sting", "e-0.6"], ["moo", "e+0.15"]]},
    {"id": "s11", "say": "Egal! Schreib Tanken!",
     "caps": ["EGAL!", "SCHREIB ^„TANKEN“! ⛽"], "gap": 0.55,
     "sfx": [["whoosh", -0.05], ["ding", "e+0.0"]]},
]
script = {
    "title": "Omas Mondmission – Tag 1", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.1, "tail": 2.4, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/oma_ref.wav", "voice_text": "voice/oma_ref.txt", "tries": 3, "max_wer": 0.08,
            "candidates": 4, "temperature": 0.7},
    "music": {"bpm": 104, "inst": "pluck", "clap": 0.5, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")

cap = ("Oma (78) holt Opa Heinz vom Mond 🚀🐄 Er ist 1974 hingeflogen und nie zurückgekommen. Jeder Kommentar = 1 Liter Treibstoff, "
       "bei 100 Litern heben wir ab! Schreib TANKEN ⛽ Und was meint Heinz mit „Vorsicht vor den M…“? 👀 #oma #mondmission #tag1 #kuh #fyp")
pin = ("📌 So geht's: Jeder Kommentar = 1 Liter ⛽ Wir zählen ehrlich. Bei 100 Litern startet die Rakete 🚀 "
       "Jeder, der tankt, kommt mit Namen in Omas Bodenkontrolle (die Tafel im Garten). Tank: 0 / 100")
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
Bio: Oma Gisela (78) holt Opa Heinz vom Mond 🚀🐄 Jeder Kommentar = 1 Liter Treibstoff. Start bei 100!
Danach dieses Video oben anpinnen. Die alten FC-Kuhweide-Videos bleiben online.
""")
print(f"Tag 1: {len(segments)} Sätze")

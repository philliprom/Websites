"""Omas Mondmission – Tag 6: Krause wird abgeschüttelt (Abstimmung Tag 5: A 5:0), landet in seiner Hecke, Chris ist zurück,
neue Regel: Jeder Follower bringt Oma näher an den Mond, Landung bei 300 (Zwischenziele 175/200/250).
Erzeugt script.json, tank.js und out/beschreibung.txt aus tank.json. Vor dem Posten "follower" in tank.json auf den
aktuellen Stand setzen und neu bauen (nur Sätze mit der Zahl werden neu gesprochen).
Aufruf: python3 omas-mondmission-tag6/make_script.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "tank.json"), encoding="utf-8"))
F, Z = T["follower"], T["ziel"]
EINS = ["null", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf", "dreizehn",
        "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
ZEHN = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]


def zahl(n):
    if n >= 100:
        h, r = divmod(n, 100)
        return ("hundert" if h == 1 else EINS[h] + "hundert") + (zahl(r) if r else "")
    if n < 20:
        return EINS[n]
    z, e = divmod(n, 10)
    return ZEHN[z] if e == 0 else f"{EINS[e]}und{ZEHN[z]}"


M1 = T["meilensteine"][0][0]
segments = [
    {"id": "s01", "say": "Ihr habt entschieden: Krause wird abgeschüttelt!",
     "caps": ["IHR HABT ENTSCHIEDEN:", "KRAUSE WIRD", "!ABGESCHÜTTELT! 🫨"], "gap": 0.0,
     "sfx": [["boing", -0.3], ["whoosh", 0.4], ["boing", 1.2], ["squeak", 1.9]]},
    {"id": "s02", "say": "Fünf zu null! Jan schreibt sogar: A, sonst Anzeige!",
     "caps": ["^5 : 0 FÜR A!", "JAN SCHREIBT SOGAR:", "„A, SONST ^ANZEIGE!“ 😂"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", 0.3], ["pop", "e-1.6"]]},
    {"id": "s03", "say": "Festhalten, Berta! Tschüss, Herr Krause!",
     "caps": ["FESTHALTEN, ^BERTA!", "TSCHÜSS, HERR ^KRAUSE! 👋"], "gap": 0.15,
     "sfx": [["boing", 0.0], ["boing", 0.4], ["moo", 0.6], ["whistle", "e-0.9"], ["whoosh", "e-0.8"]]},
    {"id": "s04", "say": "Keine Sorge, er ist weich gelandet.",
     "caps": ["KEINE SORGE,", "ER IST ^WEICH GELANDET. 🌳"], "gap": 0.2,
     "sfx": [["crunch", -0.2], ["poof", -0.15], ["boing", 1.2]]},
    {"id": "s05", "say": "Und Chris ist wieder da! Hallo Chris!",
     "caps": ["UND ^CHRIS IST WIEDER DA!", "HALLO ^CHRIS! 👋"], "gap": 0.2,
     "sfx": [["pop", 0.1], ["hearts", "e-0.8"]]},
    {"id": "s06", "say": "Jetzt geht es zum Mond. Aber nur mit euch!",
     "caps": ["JETZT GEHT ES ZUM ^MOND. 🌕", "ABER NUR MIT ^EUCH!"], "gap": 0.2,
     "sfx": [["riser", -0.1], ["whoosh", 0.2], ["sparkle", 0.9]]},
    {"id": "s07", "say": f"Bei dreihundert Followern landen wir. Wir sind schon bei {zahl(F)}!",
     "caps": [f"BEI ^{Z} FOLLOWERN", "LANDEN WIR. 🌕", "WIR SIND SCHON", f"BEI ^{F}! 🚀"], "gap": 0.15,
     "sfx": [["pop", 0.5], ["pop", 0.8], ["pop", 1.1], ["pop", 1.4], ["ding", "e-0.6"]]},
    {"id": "s08", "say": f"Folg mir, damit wir ankommen! Bei {zahl(M1)} wird es gefährlich!",
     "caps": ["^FOLG MIR, DAMIT", "WIR ANKOMMEN! ❤️", f"BEI ^{M1} WIRD ES", "!GEFÄHRLICH! ⚠️"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["tap", 1.0], ["kaching", 1.05], ["sting", "e-1.2"]]},
]
script = {
    "title": "Omas Mondmission – Tag 6", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.35, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "../omas-mondmission-tag1/voice/oma_ref.wav", "voice_text": "../omas-mondmission-tag1/voice/oma_ref.txt",
            "tries": 3, "max_wer": 0.08, "candidates": 4, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "pluck", "clap": 0.55, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
open(os.path.join(HERE, "tank.js"), "w", encoding="utf-8").write("window.TANK = " + json.dumps(T, ensure_ascii=False) + ";\n")

ms = " · ".join(f"{n}: {name.capitalize()} {emo}" for n, name, emo in T["meilensteine"])
cap = (f"Tag 6: Ihr habt entschieden, Krause wird abgeschüttelt 🫨 (keine Sorge, er ist weich gelandet 🌳). "
       f"Jetzt geht's zum Mond: Bei {Z} Followern landet Oma! 🌕 Folgst du schon? 🚀 #oma #mondmission #tag6 #kuh #fyp")
pin = (f"📌 NEUE REGEL: Jeder Follower bringt Oma näher an den Mond 🚀 Stand: {F} / {Z}. Unterwegs: {ms}. "
       "Kommentare = Funksprüche an Oma 📻, die besten liest sie vor! Ergebnis Tag 5: A (abschütteln) gewinnt 5:0.")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Omas Mondmission (@gruselwahl.de)
OMAS MONDMISSION – TAG 6 · TEXTE ZUM POSTEN
============================================
Stand: {T['stand']} · {F} Follower · Ziel {Z} · {len(T['namen'])} Namen auf der Tafel

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

PROFIL (vor dem Posten ändern):
Anzeigename: Omas Mondmission 🚀
Bio: Oma Gisela (78) fliegt zum Mond 🚀🐄 Bei {Z} Followern landet sie! Kommentare = Funksprüche 📻

TITELBILD
Datei: titelbild.png
""")
cp = os.path.join(HERE, "cover.html")
cov = open(cp, encoding="utf-8").read()
open(cp, "w", encoding="utf-8").write(re.sub(r"\d+ / \d+ FOLLOWER", f"{F} / {Z} FOLLOWER", cov))
print(f"Tag 6: {len(segments)} Sätze, {F}/{Z} Follower, {len(T['namen'])} Namen")

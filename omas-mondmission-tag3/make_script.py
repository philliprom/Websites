"""Omas Mondmission – Tag 3: Krause bohrt ein Loch in den Tank, Abstimmung A/B. Erzeugt script.json, tank.js und out/beschreibung.txt aus tank.json.
Vor dem Posten Liter und Namen in tank.json aktualisieren (Kommentare unter allen Folgen zählen), dann neu bauen.
Aufruf: python3 omas-mondmission-tag3/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "tank.json"), encoding="utf-8"))
L = T["liter"]
EINS = ["null", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf", "dreizehn",
        "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
ZEHN = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig", "achtzig", "neunzig"]


def zahl(n):
    if n < 20:
        return EINS[n]
    if n == 100:
        return "hundert"
    z, e = divmod(n, 10)
    return ZEHN[z] if e == 0 else f"{EINS[e]}und{ZEHN[z]}"


Lw = zahl(L).capitalize()
segments = [
    {"id": "s01", "say": "Krause hat ein Loch in meinen Tank gebohrt!",
     "caps": ["^KRAUSE HAT EIN !LOCH", "IN MEINEN TANK GEBOHRT!"], "gap": 0.0,
     "sfx": [["hiss", -0.35], ["splash", 0.1], ["splash", 1.1]]},
    {"id": "s02", "say": "Zum Glück habe ich es mit Kaugummi zugeklebt.",
     "caps": ["ZUM GLÜCK MIT", "^KAUGUMMI ZUGEKLEBT!"], "gap": 0.2,
     "sfx": [["squeak", "e-0.75"], ["pop", "e-0.6"]]},
    {"id": "s03", "say": f"Dank euch sind jetzt {zahl(L)} Liter drin!",
     "caps": ["DANK EUCH SIND JETZT", f"^{L} LITER DRIN! ⛽"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.1"]]},
    {"id": "s04", "say": f"Und {zahl(len(T['namen']))} Namen stehen schon auf meiner Tafel.",
     "caps": [f"UND ^{len(T['namen'])} NAMEN STEHEN", "SCHON AUF DER TAFEL! ❤️"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["sparkle", 0.4], ["blip", 0.6], ["blip", 0.9], ["blip", 1.2]]},
    {"id": "s05", "say": "Aber Krause gibt nicht auf. Am Sonntag kommt das Ordnungsamt!",
     "caps": ["ABER ^KRAUSE GIBT NICHT AUF.", "AM !SONNTAG KOMMT", "DAS !ORDNUNGSAMT!"], "gap": 0.2,
     "sfx": [["scratch", -0.05], ["boing", 0.3], ["stamp", "e-1.2"]]},
    {"id": "s06", "say": "Wie schützen wir die Rakete? A, Berta hält Wache. B, wir tarnen sie als Gartenhaus.",
     "caps": ["WIE SCHÜTZEN WIR DIE RAKETE?", "^A: BERTA HÄLT WACHE 🐄", "^B: TARNEN ALS GARTENHAUS 🏡"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 2.2], ["moo", 2.9], ["pop", 3.9]]},
    {"id": "s07", "say": "Schreib A oder B. Jeder Kommentar ist ein Liter!",
     "caps": ["SCHREIB ^A ODER ^B! 👇", "JEDER KOMMENTAR = ^1 LITER ⛽"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["ding", "e+0.0"]]},
]
script = {
    "title": "Omas Mondmission – Tag 3", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.35, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "../omas-mondmission-tag1/voice/oma_ref.wav", "voice_text": "../omas-mondmission-tag1/voice/oma_ref.txt",
            "tries": 3, "max_wer": 0.08, "candidates": 4, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "pluck", "clap": 0.55, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
open(os.path.join(HERE, "tank.js"), "w", encoding="utf-8").write("window.TANK = " + json.dumps(T, ensure_ascii=False) + ";\n")

cap = (f"Tag 3: Krause hat ein Loch in Omas Tank gebohrt 😱 Zum Glück gibt es Kaugummi. {L} Liter sind drin! "
       "Wie schützen wir die Rakete bis Sonntag? A 🐄 Berta hält Wache · B 🏡 als Gartenhaus tarnen 👇 #oma #mondmission #tag3 #kuh #fyp")
pin = (f"📌 Abstimmung: A 🐄 Berta hält Wache oder B 🏡 Rakete als Gartenhaus tarnen? Schreib A oder B! "
       f"Jeder Kommentar = 1 Liter ⛽ Tank: {L} / 100. Wir zählen ehrlich, eine Stimme pro Person.")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Omas Mondmission (@gruselwahl.de)
OMAS MONDMISSION – TAG 3 · TEXTE ZUM POSTEN
============================================
Stand Tank: {T['stand']} · {L} Liter · {len(T['namen'])} Namen auf der Tafel

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png
""")
import re
cp = os.path.join(HERE, "cover.html")
cov = open(cp, encoding="utf-8").read()
open(cp, "w", encoding="utf-8").write(re.sub(r"TANK: \d+ / 100 LITER", f"TANK: {L} / 100 LITER", cov))
print(f"Tag 3: {len(segments)} Sätze, {L} Liter, {len(T['namen'])} Namen")

"""Omas Mondmission – Tag 4: Die Rakete wird zum Gartenhaus (Abstimmung Tag 3: B), Abstimmung Ja/Nein. Erzeugt script.json, tank.js und out/beschreibung.txt aus tank.json.
Vor dem Posten Liter und Namen in tank.json aktualisieren (Kommentare unter allen Folgen zählen), dann neu bauen.
Aufruf: python3 omas-mondmission-tag4/make_script.py
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
    {"id": "s01", "say": "Ihr habt entschieden: Meine Rakete ist jetzt ein Gartenhaus!",
     "caps": ["IHR HABT ENTSCHIEDEN:", "MEINE RAKETE IST JETZT", "EIN !GARTENHAUS! 🏡"], "gap": 0.0,
     "sfx": [["knock", -0.3], ["knock", -0.15], ["sparkle", 0.3], ["ding", "e-0.4"]]},
    {"id": "s02", "say": "Nur die Spitze guckt ein bisschen raus.",
     "caps": ["NUR DIE ^SPITZE GUCKT", "EIN BISSCHEN RAUS. 🚀"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["boing", "e-0.5"]]},
    {"id": "s03", "say": f"Und dank euch sind schon {zahl(L)} Liter im Tank!",
     "caps": ["UND DANK EUCH SIND SCHON", f"^{L} LITER IM TANK! ⛽"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.1"]]},
    {"id": "s04", "say": "Einer hat sogar Buchstabe für Buchstabe getankt. Hi, wie geht es euch? Uns geht es prima!",
     "caps": ["EINER HAT ^BUCHSTABE FÜR", "^BUCHSTABE GETANKT:", "„HI, WIE GEHT ES EUCH?“", "UNS GEHT ES ^PRIMA! ❤️"], "gap": 0.2,
     "sfx": [["whoosh", -0.05]] + [["blip", 0.5 + i * 0.13] for i in range(13)]},
    {"id": "s05", "say": "Meine Tafel ist voll. Neue Namen kommen jetzt an die Gartenhaus-Wand!",
     "caps": ["MEINE TAFEL IST !VOLL.", "NEUE NAMEN KOMMEN AN", "DIE ^GARTENHAUS-WAND! ✍️"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["stamp", 1.0], ["brush", "e-1.7"]]},
    {"id": "s06", "say": "Aber am Sonntag kommt das Ordnungsamt.",
     "caps": ["ABER AM ^SONNTAG KOMMT", "DAS !ORDNUNGSAMT."], "gap": 0.2,
     "sfx": [["scratch", -0.05], ["boing", 0.3], ["stamp", "e-0.6"]]},
    {"id": "s07", "say": "Fällt es auf mein Gartenhaus rein? Schreib Ja oder Nein!",
     "caps": ["FÄLLT ES AUF MEIN", "GARTENHAUS REIN?", "SCHREIB ^JA ODER ^NEIN! 👇"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 1.6], ["pop", 2.0]]},
    {"id": "s08", "say": "Jeder Kommentar ist ein Liter!",
     "caps": ["JEDER KOMMENTAR = ^1 LITER ⛽"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", "e+0.0"], ["moo", "e+0.4"]]},
]
script = {
    "title": "Omas Mondmission – Tag 4", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.35, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "../omas-mondmission-tag1/voice/oma_ref.wav", "voice_text": "../omas-mondmission-tag1/voice/oma_ref.txt",
            "tries": 3, "max_wer": 0.08, "candidates": 4, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "pluck", "clap": 0.55, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
open(os.path.join(HERE, "tank.js"), "w", encoding="utf-8").write("window.TANK = " + json.dumps(T, ensure_ascii=False) + ";\n")

cap = (f"Tag 4: Ihr habt abgestimmt, Omas Rakete ist jetzt ein Gartenhaus 🏡 (nur die Spitze guckt raus 🚀). {L} Liter sind drin! "
       "Am Sonntag kommt das Ordnungsamt. Fällt es drauf rein? Ja oder Nein 👇 #oma #mondmission #tag4 #kuh #fyp")
pin = (f"📌 Abstimmung: Fällt das Ordnungsamt auf das Gartenhaus rein? Schreib JA oder NEIN! "
       f"Jeder Kommentar = 1 Liter ⛽ Tank: {L} / 100. Ergebnis Tag 3: B (Gartenhaus) gewinnt 3:1. Danke fürs Tanken!")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Omas Mondmission (@gruselwahl.de)
OMAS MONDMISSION – TAG 4 · TEXTE ZUM POSTEN
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
print(f"Tag 4: {len(segments)} Sätze, {L} Liter, {len(T['namen'])} Namen")

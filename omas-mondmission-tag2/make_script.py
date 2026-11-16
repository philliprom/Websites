"""Omas Mondmission – Tag 2: Die Testzündung geht schief. Erzeugt script.json, tank.js und out/beschreibung.txt aus tank.json.
Vor dem Posten Liter und Namen in tank.json aktualisieren (Kommentare unter allen Folgen zählen), dann neu bauen.
Aufruf: python3 omas-mondmission-tag2/make_script.py
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
    {"id": "s01", "say": "Ich bin achtundsiebzig und habe gerade meinen Garten in die Luft gesprengt.",
     "caps": ["ICH BIN ^78 UND HABE", "GERADE MEINEN GARTEN", "IN DIE !LUFT GESPRENGT."], "gap": 0.0,
     "sfx": [["boom", -0.85], ["crunch", -0.55], ["poof", -0.3]]},
    {"id": "s02", "say": f"{Lw} Liter waren wohl doch zu wenig.",
     "caps": [f"^{L} LITER WAREN WOHL", "DOCH ZU !WENIG."], "gap": 0.25,
     "sfx": [["whoosh", -0.05], ["klong", "e+0.05"]]},
    {"id": "s03", "say": "Dabei wartet mein Heinz doch auf dem Mond!",
     "caps": ["DABEI WARTET MEIN ^HEINZ", "DOCH AUF DEM ^MOND!"], "gap": 0.2,
     "sfx": [["card", -0.05]]},
    {"id": "s04", "say": f"Danke an meine ersten {zahl(len(T['namen']))} Tanker!",
     "caps": ["DANKE AN MEINE", f"ERSTEN ^{len(T['namen'])} TANKER! ❤️"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["sparkle", 0.4], ["blip", 0.6], ["blip", 0.9], ["blip", 1.2]]},
    {"id": "s05", "say": "Aber Krause will die Rakete bis Sonntag abreißen lassen.",
     "caps": ["ABER ^KRAUSE WILL DIE RAKETE", "BIS !SONNTAG ABREISSEN LASSEN."], "gap": 1.1,
     "sfx": [["scratch", -0.05], ["boing", 0.3], ["stamp", 0.6]]},
    {"id": "s06", "say": "Also: Schreib Tanken! Jeder Kommentar ist ein Liter.",
     "caps": ["ALSO: SCHREIB ^„TANKEN“! ⛽", "JEDER KOMMENTAR = ^1 LITER"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["ding", "e+0.0"], ["moo", "e+0.5"]]},
]
script = {
    "title": "Omas Mondmission – Tag 2", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.95, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "../omas-mondmission-tag1/voice/oma_ref.wav", "voice_text": "../omas-mondmission-tag1/voice/oma_ref.txt",
            "tries": 3, "max_wer": 0.08, "candidates": 4, "temperature": 0.7},
    "music": {"bpm": 112, "inst": "pluck", "clap": 0.55, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
open(os.path.join(HERE, "tank.js"), "w", encoding="utf-8").write("window.TANK = " + json.dumps(T, ensure_ascii=False) + ";\n")

cap = (f"Tag 2: Testzündung 💥 Oma (78) will zu Opa Heinz auf den Mond, aber {L} Liter reichen nicht. Krause gibt ihr bis Sonntag! "
       "Jeder Kommentar = 1 Liter ⛽ Schreib TANKEN #oma #mondmission #tag2 #kuh #fyp")
pin = (f"📌 Tank: {L} / 100 Liter ⛽ Jeder Kommentar = 1 Liter, wir zählen ehrlich. Wer tankt, kommt auf die Bodenkontrolle-Tafel. "
       "Und was meint Heinz mit „Vorsicht vor den M…“? Ratet mal 👀")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Omas Mondmission (@gruselwahl.de)
OMAS MONDMISSION – TAG 2 · TEXTE ZUM POSTEN
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
print(f"Tag 2: {len(segments)} Sätze, {L} Liter, {len(T['namen'])} Namen")

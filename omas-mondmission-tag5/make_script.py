"""Omas Mondmission – Tag 5: Tank voll (Buchstaben-Tanker), Grüße, Start, Krause hängt an der Rakete, Abstimmung A/B. Erzeugt script.json, tank.js und out/beschreibung.txt aus tank.json.
Vor dem Posten Liter und Namen in tank.json aktualisieren (Kommentare unter allen Folgen zählen), dann neu bauen.
Aufruf: python3 omas-mondmission-tag5/make_script.py (nach dem ersten TTS-Lauf noch einmal, für die Countdown-Piepser)
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
    if n > 100:
        return "hundert" + zahl(n - 100)
    if n < 20:
        return EINS[n]
    if n == 100:
        return "hundert"
    z, e = divmod(n, 10)
    return ZEHN[z] if e == 0 else f"{EINS[e]}und{ZEHN[z]}"


CHRIS = T["brief_chris"].replace(" ", "")
segments = [
    {"id": "s01", "say": "Ihr Verrückten! Der Tank ist voll!",
     "caps": ["IHR VERRÜCKTEN!", "DER TANK IST !VOLL! ⛽"], "gap": 0.0,
     "sfx": [["splash", -0.3], ["hiss", -0.25], ["splash", 0.6], ["sparkle", "e-0.5"]]},
    {"id": "s02", "say": f"{zahl(L).capitalize()} Liter! Und alles Buchstabe für Buchstabe.",
     "caps": [f"^{L} LITER! 🤯", "UND ALLES BUCHSTABE", "FÜR ^BUCHSTABE!"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", 0.9], ["ding", 1.2]]},
    {"id": "s03", "say": "Chris hat sogar einen ganzen Brief getankt. Liebe Grüße zurück, Chris!",
     "caps": ["^CHRIS HAT SOGAR EINEN", "GANZEN ^BRIEF GETANKT:", "LIEBE GRÜSSE ZURÜCK,", "^CHRIS! 👋"], "gap": 0.2,
     "sfx": [["whoosh", -0.05]] + [["blip", 0.25 + i * 0.15] for i in range(16)] + [["hearts", "e-0.6"]]},
    {"id": "s04", "say": "Hallo David! Und Noel: Dein Trikot fliegt mit!",
     "caps": ["HALLO ^DAVID! 👋", "UND ^NOEL: DEIN TRIKOT", "FLIEGT MIT! ⚽"], "gap": 0.2,
     "sfx": [["whoosh", -0.05]] + [["blip", 0.1 + i * 0.07] for i in range(9)] + [["whistle", "e-1.3"], ["pop", "e-1.2"]]},
    {"id": "s05", "say": "Ordnungsamt hin oder her: Wir starten jetzt!",
     "caps": ["ORDNUNGSAMT HIN ODER HER:", "WIR ^STARTEN JETZT! 🚀"], "gap": 0.15,
     "sfx": [["scratch", -0.05], ["crunch", "e-0.7"], ["poof", "e-0.62"], ["whoosh", "e-0.55"]]},
    {"id": "s06", "say": "Drei! Zwei! Eins! Los!",
     "caps": ["^3 …", "^2 …", "^1 …", "!LOS! 🚀"], "gap": 0.25,
     "sfx": [["riser", -0.1]], "countdown": True},
    # „Moment mal. Herr Krause hängt dran!“ kam in 14 Fassungen nie in Omas Stimmfarbe (zu tief, Ähnlichkeit ≤ 0,965).
    # „Ach du Schreck!“ passt: Ähnlichkeit 0,987, 257 Hz (Probe im Satz-Cache)
    {"id": "s07", "say": "Ach du Schreck! Herr Krause hängt dran!",
     "caps": ["ACH DU SCHRECK!", "HERR ^KRAUSE HÄNGT DRAN! 😱"], "gap": 0.5,
     "sfx": [["boing", 0.0], ["squeak", "e-1.0"]]},
    {"id": "s08", "say": "Abschütteln oder mitnehmen? Schreib A oder B!",
     "caps": ["^ABSCHÜTTELN ODER", "^MITNEHMEN?", "SCHREIB ^A ODER ^B! 👇"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.2], ["pop", 1.2], ["moo", "e+0.3"]]},
]
# Zweiter Durchlauf nach der Vertonung: Countdown-Piepser genau auf die gesprochenen Zahlen (build/countdown.json aus
# countdown.py) und Trikot-Geräusche auf „Und Noel“ (Untertitel-Zeit, so wie die Szene sie benutzt)
cdp, tlp = os.path.join(HERE, "build", "countdown.json"), os.path.join(HERE, "build", "timeline.json")
if os.path.exists(cdp):
    rel = json.load(open(cdp))
    T["countdown"] = rel
    seg6 = next(x for x in segments if x["id"] == "s06")
    seg6["sfx"] = [["riser", -0.1], ["beep", rel[0]], ["beep", rel[1]], ["beep", rel[2]], ["bigbeep", rel[3]],
                   ["boom", rel[3] + 0.2], ["rocket", rel[3] + 0.25]]
if os.path.exists(tlp):
    tl = json.load(open(tlp, encoding="utf-8"))
    sg4 = next((x for x in tl["segments"] if x["id"] == "s04"), None)
    if sg4 and len(sg4.get("caps", [])) == 3:
        r1 = round(sg4["caps"][1]["start"] - sg4["start"], 3)
        r2 = round(sg4["caps"][2]["start"] - sg4["start"], 3)
        seg4 = next(x for x in segments if x["id"] == "s04")
        seg4["sfx"] = [x for x in seg4["sfx"] if x[0] not in ("whistle", "pop")] + [["whistle", r1], ["pop", r1 + 0.05], ["whoosh", r2 + 0.1]]
for sg in segments:
    sg.pop("countdown", None)
script = {
    "title": "Omas Mondmission – Tag 5", "voice": "qwen3-tts (Oma_Qwen_1)", "lead_in": 0.35, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "../omas-mondmission-tag1/voice/oma_ref.wav", "voice_text": "../omas-mondmission-tag1/voice/oma_ref.txt",
            "tries": 3, "max_wer": 0.08, "candidates": 4, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "pluck", "clap": 0.55, "ambience": 0.25,
              "chords": [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]], "roots": [48, 43, 45, 41],
              "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
open(os.path.join(HERE, "tank.js"), "w", encoding="utf-8").write("window.TANK = " + json.dumps(T, ensure_ascii=False) + ";\n")

cap = (f"Tag 5: {L} Liter! 🤯 Ihr habt Buchstabe für Buchstabe getankt, jetzt fliegt Oma los 🚀🐄 … aber wer hängt da unten dran? 😱 "
       "Abschütteln oder mitnehmen? A oder B 👇 #oma #mondmission #tag5 #rakete #fyp")
pin = (f"📌 Abstimmung: Herr Krause hängt an der Rakete! A = abschütteln 🫨 B = mitnehmen 🚀 "
       f"Tank: {L} / 100 ⛽ VOLL! Danke an alle {len(T['namen'])} Tanker, besonders an die Buchstaben-Tanker Chris, Jonas und David. "
       "Ab jetzt: Schreib Oma einen Funkspruch ins All 📻, die besten liest sie vor!")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Omas Mondmission (@gruselwahl.de)
OMAS MONDMISSION – TAG 5 · TEXTE ZUM POSTEN
============================================
Stand Tank: {T['stand']} · {L} Liter · {len(T['namen'])} Namen
Rechnung: {T['liter_rechnung']}

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
print(f"Tag 5: {len(segments)} Sätze, {L} Liter, {len(T['namen'])} Namen")

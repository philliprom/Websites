"""Tag 4: Berta ist weg. Erzeugt script.json, kader.js und out/beschreibung.txt aus kader.json.
Aufruf: python3 fc-kuhweide-tag4/make_script.py
Ziel: höchstens 30 s, ein Erzählstrang, in Sekunde 1 ohne Vorwissen verständlich.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))
yg, mia = K["kapitaen"]["wahl"]
zw = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn"]

segments = [
    {"id": "s01", "say": "Unsere Kuh ist weg.", "caps": ["UNSERE ^KUH", "IST !WEG."], "gap": 0.0,
     "sfx": [["stamp", 0.0]]},
    {"id": "s02", "say": "Und Samstag spielen wir um sie!", "caps": ["UND ^SAMSTAG", "SPIELEN WIR ^UM SIE!"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.35]]},
    {"id": "s03", "say": "Schuld ist der hier:", "caps": ["SCHULD IST", "^DER HIER:"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["drum", 0.05]]},
    {"id": "s04", "say": "Metzger-Manni! Der Ex-Profi von Matschbach.", "caps": ["!METZGER-MANNI!", "DER ^EX-PROFI", "VON MATSCHBACH."], "gap": 0.05,
     "sfx": [["stamp", 0.0], ["horn", 0.12], ["card", 1.1]]},
    {"id": "s05", "say": "Er hat gesagt, er freut sich auf Berta.", "caps": ["ER HAT GESAGT,", "ER ^FREUT SICH", "AUF !BERTA."], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["blip", 0.9], ["sting", "e-0.35"]]},
    {"id": "s06", "say": "Berta hat's gehört … und ist abgehauen!", "caps": ["BERTA HAT'S ^GEHÖRT …", "UND IST !ABGEHAUEN!"], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["boing", 0.45], ["moo", "e-1.1"], ["whoosh", "e-0.7"]]},
    {"id": "s07", "say": "Ausgerechnet Richtung Matschbach!", "caps": ["AUSGERECHNET", "RICHTUNG !MATSCHBACH!"], "gap": 0.35,
     "sfx": [["whoosh", -0.05], ["pop", 0.2]]},
    {"id": "s08", "say": "Schreibt Berta in die Kommentare!", "caps": ["SCHREIBT ~BERTA", "IN DIE ^KOMMENTARE!"], "gap": 0.45,
     "sfx": [["whoosh", -0.05], ["blip", 0.1], ["pop", 0.9]]},
    {"id": "s09", "say": "Jeder Kommentar holt sie einen Schritt zurück.", "caps": ["JEDER KOMMENTAR", "HOLT SIE EINEN", "^SCHRITT ZURÜCK."], "gap": 0.05,
     "sfx": [["tap", 0.7], ["tap", 1.1], ["tap", 1.5]]},
    {"id": "s10", "say": f"Kapitänswahl: {zw[yg['stimmen']]} zu {zw[mia['stimmen']]}! {mia['sprich']} und {yg['sprich']} führen den Suchtrupp gemeinsam an.",
     "caps": ["KAPITÄNSWAHL:", f"^{yg['stimmen']} : {mia['stimmen']}!", f"^{mia['name'].upper()} UND ^{yg['name'].upper()} FÜHREN", "DEN SUCHTRUPP ^GEMEINSAM AN!"], "gap": 0.45,
     "sfx": [["whoosh", -0.05], ["card", 0.15], ["card", 0.45], ["stamp", 1.25], ["confetti", 1.3], ["cheer", 1.35], ["pop", 2.2]]},
    {"id": "s11", "say": "Finden wir sie bis Samstag?", "caps": ["FINDEN WIR SIE", "BIS ^SAMSTAG?"], "gap": 0.5,
     "sfx": [["whoosh", -0.05], ["pop", 0.05], ["tap", "e+0.3"], ["ding", "e+0.35"]]},
]
script = {
    "title": "FC Kuhweide – Tag 4: Berta ist weg",
    "voice": "voxcpm2", "lead_in": 0.1, "tail": 1.5, "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt",
            "cfg": 2.0, "steps": 10},
    "music": {"bpm": 118, "inst": "pluck", "clap": 1.5, "ambience": 0.2,
              "chords": [[69, 72, 76, 81], [65, 69, 72, 77], [60, 64, 67, 72], [67, 71, 74, 79]],
              "roots": [45, 41, 48, 43], "arp": [0, 1, 2, 1, 3, 2, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Tag 4: Berta ist weg 😱 Samstag spielen wir um sie – und Metzger-Manni freut sich schon 🌭 "
       "Schreibt BERTA 👇 Jeder Kommentar holt sie einen Schritt zurück! #fckuhweide #tag4 #freeberta #fußball #kreisliga")
pin = (f"📌 Schreib BERTA 🐄 – jeder Kommentar = 1 Schritt zurück nach Kuhweide! Morgen zählen wir nach 👣 "
       f"Kapitänswahl {yg['stimmen']}:{mia['stimmen']} – {mia['name'].upper()} & {yg['name']} führen gemeinsam 👑")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – TAG 4 · TEXTE ZUM POSTEN
=======================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTZEIT
Gegen 12:00 Uhr. In der ersten Stunde jeden Kommentar beantworten und liken.
Morgen früh zählen wir alle Kommentare mit „BERTA“ – das ist Bertas Schrittzahl in Folge 5.
""")
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(K, ensure_ascii=False) + ";\n")
print("Tag 4: Skript mit", len(segments), "Sätzen")

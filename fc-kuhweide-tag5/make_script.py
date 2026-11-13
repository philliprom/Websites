"""Tag 5: Unsere Torhüterin ist eine Kuh. Erzeugt script.json, kader.js und out/beschreibung.txt aus kader.json.
Aufruf: python3 fc-kuhweide-tag5/make_script.py
Neu: Einstieg für Fremde (Zeitlupen-Parade, „Unsere Torhüterin ist eine Kuh“), Mitmach-Versprechen statt reiner Geschichte.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))
zw = {7: "siebenmal", 8: "achtmal", 9: "neunmal", 10: "zehnmal", 11: "elfmal", 12: "zwölfmal"}
n = K["berta_rufe"]
nb, nn = len(K["kommentare"]["berta"]), len(K["kommentare"]["neu"])

segments = [
    {"id": "s01", "say": "Unsere Torhüterin ist eine Kuh.", "caps": ["UNSERE TORHÜTERIN", "IST EINE ^KUH."], "gap": 0.0,
     "sfx": [["kick_ball", 0.0], ["boing", 0.12], ["cheer", 0.3]]},
    {"id": "s02", "say": "Und morgen spielt sie gegen den Metzger.", "caps": ["UND MORGEN SPIELT SIE", "GEGEN DEN !METZGER."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["blip", 1.0], ["sting", "e-0.25"]]},
    {"id": "s03", "say": "Gestern ist sie noch abgehauen.", "caps": ["GESTERN IST SIE", "NOCH !ABGEHAUEN."], "gap": 0.55,
     "sfx": [["whoosh", -0.05], ["stamp", 0.05]]},
    {"id": "s04", "say": f"Aber ihr habt {zw.get(n, str(n) + ' Mal')} Berta gerufen …", "caps": ["ABER IHR HABT", f"^{n}× BERTA GERUFEN …"], "gap": 0.2,
     "sfx": [["whoosh", -0.05]] + [["blip", round(0.1 + 0.2 * i, 2)] for i in range(nb)]},
    {"id": "s05", "say": "… und sie ist zurück!", "caps": ["… UND SIE IST ^ZURÜCK!"], "gap": 0.05,
     "sfx": [["whoosh", 0.0], ["cheer", 0.35], ["confetti", 0.4], ["moo", "e+0.1"]]},
    {"id": "s06", "say": "Für morgen brauchen wir noch Verstärkung.", "caps": ["FÜR MORGEN BRAUCHEN WIR", "NOCH ^VERSTÄRKUNG."], "gap": 0.8,
     "sfx": [["whoosh", -0.05], ["pop", 0.2]]},
    {"id": "s07", "say": "Wer heute seine Position kommentiert, spielt morgen mit!", "caps": ["WER HEUTE SEINE ^POSITION", "KOMMENTIERT,", "SPIELT ^MORGEN MIT!"], "gap": 0.1,
     "sfx": [["whoosh", -0.05]] + [["blip", round(0.1 + 0.17 * i, 2)] for i in range(nn)]},
    {"id": "s08", "say": "Morgen um drei ist Anpfiff: Kuh gegen Metzger!", "caps": ["MORGEN UM 3 IST ^ANPFIFF:", "^KUH GEGEN !METZGER!"], "gap": 1.1,
     "sfx": [["whistle", -0.1], ["whoosh", -0.05], ["pop", "e+0.15"], ["tap", "e+0.6"], ["ding", "e+0.65"]]},
]
script = {
    "title": "FC Kuhweide – Tag 5: Unsere Torhüterin ist eine Kuh",
    "voice": "voxcpm2", "lead_in": 0.1, "tail": 1.6, "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt",
            "cfg": 2.0, "steps": 10},
    "music": {"bpm": 128, "inst": "pluck", "clap": 1.8, "ambience": 0.25,
              "chords": [[67, 71, 74, 79], [64, 67, 71, 76], [60, 64, 67, 72], [62, 66, 69, 74]],
              "roots": [43, 40, 48, 50], "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Unsere Torhüterin ist eine Kuh 🐄🧤 Und morgen spielt sie gegen den Metzger 😳 Wer heute seine Position kommentiert, spielt morgen mit! 👇 "
       "#fckuhweide #tag5 #fußball #kreisliga #kuh")
pin = (f"📌 Kommentier deine Position (Torwart, Abwehr, Mittelfeld, Sturm …) – morgen stehst du in der Aufstellung gegen Matschbach ⚽ "
       f"Anpfiff: morgen {K['anpfiff']} 🐄")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – TAG 5 · TEXTE ZUM POSTEN
=======================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTZEIT
Heute gegen 12:00 Uhr. Das Spiel kommt morgen um {K['anpfiff']} („Anpfiff“ im Video).

KOMMENTARE (max. 5 Minuten)
Alle liken. Antworten nur auf Fragen und Lustiges. Sammelantwort unter der ersten Bewerbung:
„Alle Bewerbungen sind notiert – morgen steht ihr in der Aufstellung ✅“
""")
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(K, ensure_ascii=False) + ";\n")
print(f"Tag 5: {len(segments)} Sätze, {nb} Berta-Karten, {nn} Bewerbungen")

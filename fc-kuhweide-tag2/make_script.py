"""Erzeugt script.json und kader.js für Tag 2 aus kader.json.

Aufruf: python3 fc-kuhweide-tag2/make_script.py
Danach: Stimme (engine/build_timeline.py), Ton (engine/audio.py), Bild (engine/render.cjs).
Nur Sätze, deren Text sich ändert (z. B. Fanzahl), werden dank Satz-Cache neu gesprochen.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))

spieler = sum(1 for p in K["aufstellung"] for n in p["names"] if not n.startswith("Berta")) + sum(1 for s in K["staff"] if s.get("spielt"))
fans = K["fans"]
rest = K["kasse_start"] - K["netz_preis"]
flo = K["torwart_herausforderer"]["name"]
jul = K["dauerkarte_001"]["name"]

ultra = K["ultra"]["name"]
segments = [
    {"id": "s01", "say": "Gestern: null Fans.", "caps": ["GESTERN: !0 FANS."], "gap": 0.0,
     "sfx": [["whistle", 0.0], ["pop", 0.05]]},
    {"id": "s02", "say": f"Heute: {fans}!", "caps": [f"HEUTE: ^{fans}!"], "gap": 0.05,
     "sfx": [["cheer", 0.0], ["confetti", 0.1], ["flap", "e-0.1"]]},
    {"id": "s03", "say": f"Und {spieler} von euch wollen bei uns spielen.", "caps": [f"UND ^{spieler} VON EUCH", "WOLLEN BEI UNS ^SPIELEN."], "gap": 0.1,
     "sfx": [["blip", 0.05], ["blip", 0.27], ["blip", 0.49], ["blip", 0.71], ["blip", 0.93], ["blip", 1.15], ["blip", 1.37]]},
    {"id": "s04", "say": f"{K['netz_waehler']} wollte ein Netz.", "caps": [f"^{K['netz_waehler'].upper()} WOLLTE", "EIN ^NETZ."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["blip", 0.05]]},
    {"id": "s05", "say": "Gekauft!", "caps": ["^GEKAUFT!"], "gap": 0.05,
     "sfx": [["pop", 0.0], ["kaching", 0.15]]},
    {"id": "s06", "say": f"{ultra} wollte Ultra werden.", "caps": [f"^{ultra.upper()} WOLLTE", "^ULTRA WERDEN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["blip", 0.05]]},
    {"id": "s07", "say": "Bitte sehr: unser Ultra-Block.", "caps": ["BITTE SEHR:", "UNSER ^ULTRA-BLOCK."], "gap": 0.05,
     "sfx": [["drum", 0.05], ["drum", "e-0.5"], ["cheer", "e-0.4"]]},
    {"id": "s08", "say": f"Und {flo} will ins Tor.", "caps": [f"UND ^{flo.upper()}", "WILL INS ^TOR."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["blip", 0.05]]},
    {"id": "s09", "say": "Aber Berta gibt ihren Platz nicht her.", "caps": ["ABER ^BERTA GIBT", "IHREN PLATZ", "!NICHT HER."], "gap": 0.05,
     "sfx": [["moo", "e-0.3"]]},
    {"id": "s10", "say": "Also: Elfmeter-Test! Unser Neuner schießt …", "caps": ["ALSO:", "^ELFMETER-TEST!", "UNSER ^NEUNER", "SCHIESST …"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["whistle", 0.05], ["kick_ball", "e-0.05"]]},
    {"id": "s11", "say": "… und Berta hält. Mal wieder aus Versehen.", "caps": ["… UND BERTA ^HÄLT.", "MAL WIEDER", "AUS !VERSEHEN."], "gap": 0.05,
     "sfx": [["boing", 0.05], ["cheer", 0.3]]},
    {"id": "s12", "say": "Und hier ist euer Kader!", "caps": ["UND HIER IST", "EUER ^KADER!"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pins", 0.25]]},
    {"id": "s13", "say": f"Mit Sturm-Duo, zwei Co-Trainern und einem Duell rechts hinten.", "caps": ["MIT ^STURM-DUO,", "ZWEI ^CO-TRAINERN", "UND EINEM !DUELL", "RECHTS HINTEN."], "gap": 0.05,
     "sfx": [["pop", 0.05], ["pop", "e-2.3"], ["boing", "e-1.0"]]},
    {"id": "s14", "say": f"Die Dauerkarte Nummer eins geht an: {jul}!", "caps": ["DIE DAUERKARTE", "NR. 1 GEHT AN:", f"^{jul.upper()}!"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.05], ["stamp", "e-0.35"], ["confetti", "e-0.3"]]},
    {"id": "s15", "say": f"Und jetzt ihr: Wer geht ins Tor? Berta oder {flo}?", "caps": ["UND JETZT IHR:", "WER GEHT INS ~TOR?", f"^BERTA ODER ^{flo.upper()}?"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["card", "e-1.5"], ["card", "e-0.8"]]},
    {"id": "s16", "say": "Schreibt's in die Kommentare!", "caps": ["SCHREIBT'S IN DIE", "^KOMMENTARE!"], "gap": 0.05,
     "sfx": [["pop", 0.05], ["hearts", 0.2]]},
    {"id": "s17", "say": "Und morgen schicken wir Post. An den größten Kreisligaverein der Welt.", "caps": ["UND MORGEN", "SCHICKEN WIR ^POST.", "AN DEN !GRÖSSTEN", "KREISLIGAVEREIN DER WELT."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["blip", 0.6], ["pop", 0.65], ["riser", "e-1.2"]]},
]

script = {
    "title": "FC Kuhweide – Tag 2: Der Kader",
    "voice": "voxcpm2",
    "lead_in": 0.1,
    "tail": 1.0,
    "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt",
            "cfg": 2.0, "steps": 10},
    "music": {"bpm": 126, "inst": "pluck", "clap": 1.7, "ambience": 0.2,
              "chords": [[67, 71, 74, 79], [66, 69, 74, 78], [64, 67, 71, 76], [64, 67, 72, 76]],
              "roots": [43, 50, 40, 48], "arp": [0, 1, 2, 1, 3, 2, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = (f"Tag 2: Gestern 0 Fans, heute {fans} ⚽🐄 {spieler} von euch wollen bei uns spielen – ist dein Name im Kader? 👀 "
       f"Wer geht ins Tor: BERTA oder {flo.upper()}? Schreibt's in die Kommentare 👇 #fckuhweide #tag2 #fußball #kreisliga #amateurfußball")
pin = (f"📌 TORWART-DUELL: Schreibt BERTA 🐄 oder {flo.upper()} 🧤! Und wer noch in den Kader will: Position in die Kommentare ✍️ "
       f"Morgen geht unsere Post raus – an den größten Kreisligaverein der Welt 👀✉️")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – TAG 2 · TEXTE ZUM POSTEN
=======================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png – beim Posten unter „Titelbild bearbeiten“ hochladen.

POSTZEIT
Gegen 12:00 Uhr. In der ersten Stunde jeden Kommentar beantworten und liken.
""")
kjs = dict(K, spieler=spieler, kasse_rest=rest)
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(kjs, ensure_ascii=False) + ";\n")
print(f"script.json + kader.js erzeugt: {spieler} Spieler-Wünsche, {fans} Fans, Kasse {K['kasse_start']} → {rest} €")

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

segments = [
    {"id": "s01", "say": f"{spieler} von euch wollen bei uns spielen.", "caps": [f"^{spieler} VON EUCH", "WOLLEN BEI UNS ^SPIELEN."], "gap": 0.0,
     "sfx": [["whistle", 0.0], ["pop", 0.1]]},
    {"id": "s02", "say": "Ist dein Name dabei?", "caps": ["IST ^DEIN ^NAME DABEI?"], "gap": 0.08,
     "sfx": [["blip", 0.05]]},
    {"id": "s03", "say": "Aber erst: Berta gibt ihr Tor nicht her.", "caps": ["ABER ERST:", "^BERTA GIBT IHR", "TOR !NICHT HER."], "gap": 0.1,
     "sfx": [["whoosh", -0.05], ["pop", 0.1], ["moo", "e-0.2"]]},
    {"id": "s04", "say": f"{fans} Fans – und immer noch eine Bierbank.", "caps": [f"^{fans} ^FANS –", "UND IMMER NOCH", "EINE !BIERBANK."], "gap": 0.1,
     "sfx": [["whoosh", -0.05], ["cheer", 0.0], ["coo", "e-0.6"], ["flap", "e-0.5"]]},
    {"id": "s05", "say": f"Abgestimmt hat übrigens nur {K['netz_waehler']}.", "caps": ["ABGESTIMMT HAT", f"ÜBRIGENS NUR ^{K['netz_waehler'].upper()}."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.1]]},
    {"id": "s06", "say": "Also: Netz gekauft!", "caps": ["ALSO: ^NETZ ^GEKAUFT!"], "gap": 0.08,
     "sfx": [["whoosh", -0.05], ["pop", 0.15], ["kaching", 0.5]]},
    {"id": "s07", "say": "Und hier ist euer Kader!", "caps": ["UND HIER IST", "EUER ^KADER!"], "gap": 0.12,
     "sfx": [["whoosh", -0.05], ["pins", 0.25]]},
    {"id": "s08", "say": "Mit Sturm-Duo, zwei Co-Trainern und unserem ersten Ultra.", "caps": ["MIT ^STURM-DUO,", "ZWEI ^CO-TRAINERN", "UND UNSEREM ERSTEN ^ULTRA."], "gap": 0.05,
     "sfx": [["pop", 0.05], ["pop", "e-1.4"], ["pop", "e-0.6"]]},
    {"id": "s09", "say": f"Rechts hinten gibt's ein Duell: {K['rv_duell']['namen']}.", "caps": ["RECHTS HINTEN", "GIBT'S EIN !DUELL:", f"^{K['rv_duell']['namen'].upper()}."], "gap": 0.1,
     "sfx": [["pop", 0.1], ["boing", "e-1.0"]]},
    {"id": "s10", "say": f"Und die Dauerkarte Nummer eins geht an: {jul}!", "caps": ["UND DIE DAUERKARTE", "NR. 1 GEHT AN:", f"^{jul.upper()}!"], "gap": 0.12,
     "sfx": [["whoosh", -0.05], ["pop", 0.05], ["stamp", "e-0.35"], ["confetti", "e-0.3"]]},
    {"id": "s11", "say": "Bleibt nur eine Frage: Wer geht ins Tor?", "caps": ["BLEIBT NUR", "EINE FRAGE:", "WER GEHT INS ~TOR?"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.1]]},
    {"id": "s12", "say": f"Berta oder {flo}? Schreibt's in die Kommentare!", "caps": [f"^BERTA ODER ^{flo.upper()}?", "SCHREIBT'S IN DIE", "^KOMMENTARE!"], "gap": 0.1,
     "sfx": [["card", 0.05], ["card", 0.45], ["pop", "e-1.0"]]},
    {"id": "s13", "say": "Und markiert den Kumpel, der bei uns auf die Bank muss.", "caps": ["UND MARKIERT DEN", "^KUMPEL, DER BEI UNS", "AUF DIE ^BANK MUSS."], "gap": 0.12,
     "sfx": [["pop", 0.1], ["hearts", 0.4], ["whistle", "e-0.1"]]},
]

script = {
    "title": "FC Kuhweide – Tag 2: Der Kader",
    "voice": "voxcpm2",
    "lead_in": 0.15,
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
kjs = dict(K, spieler=spieler, kasse_rest=rest)
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(kjs, ensure_ascii=False) + ";\n")
print(f"script.json + kader.js erzeugt: {spieler} Spieler-Wünsche, {fans} Fans, Kasse {K['kasse_start']} → {rest} €")

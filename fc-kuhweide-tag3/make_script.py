"""Tag 3: Der Brief. Erzeugt script.json, kader.js und out/beschreibung.txt aus kader.json.
Aufruf: python3 fc-kuhweide-tag3/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))
n_ultra = len(K["ultras"])
zahl = {6: "sechs", 7: "sieben", 8: "acht", 9: "neun", 10: "zehn", 11: "elf", 12: "zwölf"}.get(n_ultra, str(n_ultra))
y, m = K["kapitaen"][0]["name"], K["kapitaen"][1]["name"]
LESEN = 0.9  # kurze Lesepause nach Kommentar-Karten

segments = [
    {"id": "s01", "say": "Der Brief ist von …", "caps": ["DER BRIEF", "IST VON …"], "gap": 0.0,
     "sfx": [["whoosh", 0.0], ["drum", 0.2]]},
    {"id": "s02", "say": f"… dem {K['gegner']}!", "caps": [f"… DEM ^{K['gegner'].upper()}!"], "gap": 0.05,
     "sfx": [["stamp", 0.05], ["horn", 0.25]]},
    {"id": "s03", "say": "Unserem Erzrivalen. Die Taube hat sich verflogen.", "caps": ["UNSEREM !ERZRIVALEN.", "DIE TAUBE HAT", "SICH ^VERFLOGEN."], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["coo", "e-0.6"]]},
    {"id": "s04", "say": "Samstag um drei ist das Spiel.", "caps": ["^SAMSTAG UM 3", "IST DAS ^SPIEL."], "gap": 0.35,
     "sfx": [["whoosh", -0.05], ["pop", 0.05]]},
    {"id": "s05", "say": "Und wenn wir verlieren, muss Berta nach Matschbach.", "caps": ["UND WENN WIR !VERLIEREN,", "MUSS ^BERTA", "NACH MATSCHBACH."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["scratch", "e-1.0"], ["mstop", "e-0.95"], ["sting", "e-0.9"]]},
    {"id": "s06", "say": "Niemals! Wir brauchen Verstärkung.", "caps": ["^NIEMALS!", "WIR BRAUCHEN", "^VERSTÄRKUNG."], "gap": 0.9,
     "sfx": [["mgo", -0.1], ["whoosh", -0.05], ["pop", 0.05]]},
    {"id": "s07", "say": f"Gestern: {K['fans_gestern']} Fans. Heute: {K['fans']}!", "caps": [f"GESTERN: {K['fans_gestern']} FANS.", f"HEUTE: ^{K['fans']}!"], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["cheer", "e-0.6"], ["confetti", "e-0.5"]]},
    {"id": "s08", "say": f"{K['capo']['name']} wird Capo. Und der Ultra-Block hat jetzt {zahl} Mann!", "caps": [f"^{K['capo']['name'].upper()} WIRD ^CAPO.", "DER ULTRA-BLOCK HAT", f"JETZT ^{n_ultra} MANN!"], "gap": 0.35,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["blip", 1.3], ["blip", 1.65], ["blip", 2.0], ["blip", 2.35], ["drum", "e-0.4"]]},
    {"id": "s09", "say": f"{K['bus']['name']} fährt den Mannschaftsbus.", "caps": [f"^{K['bus']['name'].upper()} FÄHRT DEN", "^MANNSCHAFTSBUS."], "gap": 0.2 + LESEN,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["horn", "e-0.2"]]},
    {"id": "s10", "say": "Okay … es ist ein Traktor.", "caps": ["OKAY …", "ES IST EIN ^TRAKTOR."], "gap": 0.4,
     "sfx": [["boing", "e+0.05"]]},
    {"id": "s11", "say": f"{K['physio']['name']} wird Physio, {K['sprecher']['name']} Stadionsprecher und {K['maskottchen']['name']} unser Maskottchen.",
     "caps": [f"^{K['physio']['name'].upper()} WIRD ^PHYSIO,", f"^{K['sprecher']['name'].upper()} ^STADIONSPRECHER", f"UND ^{K['maskottchen']['name'].upper()} UNSER ^MASKOTTCHEN."], "gap": 0.5,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["blip", 1.3], ["blip", 2.6]]},
    {"id": "s12", "say": f"Im Tor steht Berta. {K['torwart']['ersatz']} ist ihr Ersatz.", "caps": ["IM TOR STEHT ^BERTA.", f"^{K['torwart']['ersatz'].upper()} IST IHR ERSATZ."], "gap": 0.2 + LESEN,
     "sfx": [["whoosh", -0.05], ["moo", 0.9]]},
    {"id": "s13", "say": f"Und wer wird Kapitän? {y} oder {m}?", "caps": ["UND WER WIRD ~KAPITÄN?", f"^{y.upper()} ODER ^{m.upper()}?"], "gap": 0.4,
     "sfx": [["whoosh", -0.05], ["card", "e-1.3"], ["card", "e-0.7"]]},
    {"id": "s14", "say": "Schreibt's in die Kommentare!", "caps": ["SCHREIBT'S IN DIE", "^KOMMENTARE!"], "gap": 0.2,
     "sfx": [["pop", 0.05], ["hearts", 0.2]]},
    {"id": "s15", "say": "Ach ja … auf der Rückseite steht noch was.", "caps": ["ACH JA …", "AUF DER ^RÜCKSEITE", "STEHT NOCH WAS."], "gap": 0.5,
     "sfx": [["whoosh", -0.05], ["card", "e-0.5"]]},
    {"id": "s16", "say": "„Wir haben einen neuen Stürmer. Er war mal Profi.“", "caps": ["„WIR HABEN EINEN", "NEUEN ^STÜRMER.", "ER WAR MAL !PROFI.“"], "gap": 0.6,
     "sfx": [["mstop", -0.1], ["sting", 0.0]]},
    {"id": "s17", "say": "Wer das ist? Morgen um zwölf.", "caps": ["WER DAS IST?", "MORGEN UM ^12."], "gap": 1.0,
     "sfx": [["mgo", -0.1], ["whoosh", -0.05], ["pop", 0.05], ["tap", "e+0.3"], ["ding", "e+0.35"], ["confetti", "e+0.35"]]},
]
script = {
    "title": "FC Kuhweide – Tag 3: Der Brief",
    "voice": "voxcpm2", "lead_in": 0.1, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt",
            "cfg": 2.0, "steps": 10},
    "music": {"bpm": 124, "inst": "pluck", "clap": 1.7, "ambience": 0.2,
              "chords": [[64, 67, 71, 76], [65, 69, 72, 77], [67, 71, 74, 79], [64, 67, 72, 76]],
              "roots": [40, 41, 43, 48], "arp": [0, 1, 2, 1, 3, 2, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = (f"Tag 3: Der Brief ist vom {K['gegner']} 😱 Samstag geht's um BERTA 🐄 Wer wird Kapitän: {y} oder {m.upper()}? "
       f"Schreibt's in die Kommentare 👇 #fckuhweide #tag3 #fußball #kreisliga #amateurfußball")
pin = (f"📌 KAPITÄNSWAHL: Schreibt {y} {K['kapitaen'][0]['emo']} oder {m.upper()} {K['kapitaen'][1]['emo']}! "
       f"Und: Wer ist der Ex-Profi von Matschbach? 👀 Tippt mit – Auflösung morgen um 12")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – TAG 3 · TEXTE ZUM POSTEN
=======================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTZEIT
Gegen 12:00 Uhr. In der ersten Stunde jeden Kommentar beantworten und liken.
""")
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(K, ensure_ascii=False) + ";\n")
print(f"Tag 3: {K['fans']} Fans, {n_ultra} Ultras")

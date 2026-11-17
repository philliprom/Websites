"""Tech-Lupe – Testvideo: Warum 0,1 + 0,2 nicht 0,3 ergibt. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 techlupe-test/make_script.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Dein Computer kann nicht mal null Komma eins plus null Komma zwei rechnen.",
     "caps": ["DEIN COMPUTER KANN", "NICHT MAL ^0,1 ^+ ^0,2", "!RECHNEN."], "gap": 0.0,
     "sfx": [["blip", 0.0], ["sting", 1.0]]},
    {"id": "s02", "say": "Raus kommt null Komma drei. Dann fünfzehn Nullen. Und dann eine Vier.",
     "caps": ["RAUS KOMMT 0,3 …", "DANN ^15 ^NULLEN …", "UND DANN EINE !4."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["tick", 1.2], ["tick", 1.35], ["tick", 1.5], ["tick", 1.65], ["tick", 1.8], ["pop", "e-0.2"]]},
    {"id": "s03", "say": "Schuld ist das Binärsystem. Computer kennen nur Nullen und Einsen.",
     "caps": ["SCHULD IST DAS", "^BINÄRSYSTEM.", "NUR ^NULLEN UND ^EINSEN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05]]},
    {"id": "s04", "say": "Kennst du das von einem Drittel? Als Kommazahl hört das nie auf.",
     "caps": ["KENNST DU DAS", "VON ^1/3?", "DAS HÖRT !NIE AUF."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["blip", 1.3]]},
    {"id": "s05", "say": "Genau so geht es dem Computer mit null Komma eins.",
     "caps": ["GENAU SO GEHT ES", "DEM COMPUTER MIT ^0,1."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["riser", 0.6]]},
    {"id": "s06", "say": "Aber er hat nur vierundsechzig Bit Platz. Also schneidet er einfach ab.",
     "caps": ["ER HAT NUR", "^64 ^BIT PLATZ.", "ALSO !SCHNEIDET ER AB."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["scratch", "e-0.9"], ["card", "e-0.6"]]},
    {"id": "s07", "say": "Diese winzigen Reste landen am Ende im Ergebnis.",
     "caps": ["DIESE ^WINZIGEN ^RESTE", "LANDEN IM !ERGEBNIS."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 1.0], ["ding", "e-0.1"]]},
    {"id": "s08", "say": "Darum rechnen Bank-Programme oft mit ganzen Cent.",
     "caps": ["DARUM RECHNEN BANKEN", "OFT MIT ^GANZEN ^CENT. 🏦"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["kaching", "e-0.2"]]},
    {"id": "s09", "say": "Folge für mehr Informatik in dreißig Sekunden!",
     "caps": ["FOLGE FÜR MEHR", "^INFORMATIK IN 30 SEK! 🔍"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.9], ["ding", "e+0.2"]]},
]
script = {
    "title": "Tech-Lupe – 0,1 + 0,2", "voice": "qwen3-tts (Erzähler)", "lead_in": 0.05, "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/erzaehler.wav", "voice_text": "voice/erzaehler.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 2, "temperature": 0.7},
    "music": {"bpm": 112, "inst": "vibes", "clap": 0.35, "ambience": 0.05,
              "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [48, 52, 55, 60], [45, 48, 52, 57]], "roots": [38, 34, 36, 33],
              "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Warum rechnet dein Computer 0,1 + 0,2 = 0,30000000000000004? 🤯 Informatik in 30 Sekunden erklärt. "
       "Welches Thema soll ich als Nächstes erklären? 👇 #informatik #programmieren #lernen #techtok #fyp")
pin = "📌 Welches Informatik-Thema als Nächstes? Schreib es in die Kommentare, das meistgelikte erkläre ich als Nächstes 👇"
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Tech-Lupe (dein bestehender Kanal)
TECH-LUPE – TESTVIDEO 0,1 + 0,2 · TEXTE ZUM POSTEN
==================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

HINWEIS
Stimme ist KI (Qwen3-TTS). Beim Posten „KI-generierte Inhalte“ einschalten. Mit deiner eigenen Stimme wäre es glaubwürdiger.
""")
print(f"{len(segments)} Sätze")

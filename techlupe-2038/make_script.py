"""Tech-Lupe – Folge 2: Das Jahr-2038-Problem. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 techlupe-2038/make_script.py
Fakten (geprüft): 2^31−1 = 2.147.483.647 s nach 1.1.1970 = 19.01.2038 03:14:07 UTC (04:14:07 deutsche Zeit);
eine Sekunde später −2^31 = 13.12.1901 20:45:52 UTC (21:45:52 deutsche Zeit); 2^63 s ≈ 292 Mrd. Jahre;
Stand 17.11.2026 ≈ 1,795 Mrd. Sekunden.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Am neunzehnten Januar zweitausendachtunddreißig springt bei manchen Computern die Uhr ins Jahr neunzehnhunderteins.",
     "caps": ["AM ^19. ^JANUAR ^2038", "SPRINGT BEI MANCHEN", "COMPUTERN DIE UHR", "INS JAHR !1901."], "gap": 0.0,
     "sfx": [["tick", 0.0], ["tick", 0.5], ["tick", 1.0], ["boom", "e-1.4"]]},
    {"id": "s02", "say": "Denn viele Computer zählen die Sekunden seit dem ersten Januar neunzehnhundertsiebzig.",
     "caps": ["DENN VIELE COMPUTER", "ZÄHLEN ^SEKUNDEN", "SEIT DEM ^1. ^JANUAR ^1970."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["riser", 1.0]]},
    {"id": "s03", "say": "Heute fast eins Komma acht Milliarden.",
     "caps": ["HEUTE FAST", "^1,8 ^MILLIARDEN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.2"]]},
    {"id": "s04", "say": "Alte Systeme speichern das in zweiunddreißig Bit. Da passen nur zwei Komma eins Milliarden rein.",
     "caps": ["ALTE SYSTEME:", "^32 ^BIT.", "DA PASSEN NUR", "^2,1 ^MILLIARDEN REIN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["card", 0.4]]},
    {"id": "s05", "say": "Eine Sekunde später kippt die Zahl ins Minus.",
     "caps": ["EINE SEKUNDE SPÄTER", "KIPPT SIE INS !MINUS."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["sting", "e-0.9"]]},
    {"id": "s06", "say": "Und das heißt für den Computer: Dezember neunzehnhunderteins.",
     "caps": ["UND DAS HEISST", "FÜR DEN COMPUTER:", "!DEZEMBER !1901."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["riser", 0.3], ["boing", "e-0.3"]]},
    {"id": "s07", "say": "Die Lösung: vierundsechzig Bit. Das reicht für zweihundertzweiundneunzig Milliarden Jahre.",
     "caps": ["DIE LÖSUNG: ^64 ^BIT.", "DAS REICHT FÜR", "^292 ^MILLIARDEN JAHRE."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["kaching", "e-0.3"]]},
    {"id": "s08", "say": "Fast alles ist schon umgestellt. Aber nicht jedes alte Gerät.",
     "caps": ["FAST ALLES IST", "SCHON ^UMGESTELLT.", "ABER NICHT JEDES", "!ALTE GERÄT."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 1.2]]},
    {"id": "s09", "say": "Folge für mehr Informatik in dreißig Sekunden!",
     "caps": ["FOLGE FÜR MEHR", "^INFORMATIK IN 30 SEK! 🔍"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.9], ["ding", "e+0.2"]]},
]
script = {
    "title": "Tech-Lupe – Jahr 2038", "voice": "qwen3-tts (Klon Thorsten-Voice, CC0, Variante A ruhig)", "lead_in": 0.05,
    "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/thorsten.wav", "voice_text": "voice/thorsten.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 2, "temperature": 0.7},
    "music": {"bpm": 112, "inst": "vibes", "clap": 0.35, "ambience": 0.05,
              "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [48, 52, 55, 60], [45, 48, 52, 57]], "roots": [38, 34, 36, 33],
              "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Am 19.01.2038 um 04:14:07 Uhr springt bei manchen Computern die Uhr auf 1901 🤯 Das Jahr-2038-Problem in 30 Sekunden erklärt. "
       "Welches Thema als Nächstes? 👇 #informatik #programmieren #2038 #techtok #fyp")
pin = "📌 Wusstest du das schon? Und welches Informatik-Thema soll ich als Nächstes erklären? Das meistgelikte kommt als Nächstes 👇"
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Tech-Lupe (dein bestehender Kanal)
TECH-LUPE – FOLGE 2: DAS JAHR-2038-PROBLEM · TEXTE ZUM POSTEN
=============================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTEN
Beim Posten „KI-generierte Inhalte“ einschalten (die Stimme ist ein KI-Klon der freien Thorsten-Voice-Stimme).
Nicht am selben Tag wie Folge 1 posten, mindestens 1 Tag Abstand.

FAKTEN ZUM NACHPRÜFEN
2^31 − 1 = 2.147.483.647 Sekunden nach dem 01.01.1970 = 19.01.2038, 03:14:07 UTC (04:14:07 deutsche Zeit).
Eine Sekunde später: −2^31 = 13.12.1901, 20:45:52 UTC. 64 Bit (2^63 s) reichen für rund 292 Milliarden Jahre.
""")
print(f"{len(segments)} Sätze")

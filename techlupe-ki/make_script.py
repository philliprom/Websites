"""Tech-Lupe – Folge 3: So funktioniert ChatGPT wirklich. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 techlupe-ki/make_script.py
Inhalt (bewusst vereinfacht, aber richtig): Sprachmodelle berechnen für das nächste Textstück (Token) eine
Wahrscheinlichkeitsverteilung, wählen eins aus, hängen es an und wiederholen das. Gelernt aus sehr großen Textmengen,
gespeichert in Milliarden Parametern. Ziel ist „plausibel“, nicht „wahr“ → überzeugend klingende Fehler möglich.
Balkenwerte im Video sind Beispielwerte (so gekennzeichnet).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Wenn du ChatGPT etwas fragst, macht es im Kern nur eins: Es rät das nächste Wort.",
     "caps": ["WENN DU ^CHATGPT FRAGST,", "MACHT ES NUR EINS:", "ES !RÄT DAS !NÄCHSTE !WORT."], "gap": 0.0,
     "sfx": [["blip", 0.05], ["blip", 0.35], ["sting", "e-0.9"]]},
    {"id": "s02", "say": "Für jedes mögliche Wort berechnet es, wie wahrscheinlich es als Nächstes kommt.",
     "caps": ["FÜR JEDES MÖGLICHE WORT:", "WIE ^WAHRSCHEINLICH", "KOMMT ES ALS NÄCHSTES?"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["tick", 0.9], ["tick", 1.1], ["tick", 1.3], ["tick", 1.5]]},
    {"id": "s03", "say": "Dann nimmt es eins davon, hängt es an, und alles beginnt von vorn.",
     "caps": ["DANN NIMMT ES EINS,", "HÄNGT ES AN,", "UND ALLES ^VON ^VORN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 1.35], ["blip", "e-0.6"]]},
    {"id": "s04", "say": "Gelernt hat es das aus riesigen Mengen Text. Gespeichert in Milliarden von Zahlen.",
     "caps": ["GELERNT AUS", "^RIESIGEN ^MENGEN ^TEXT.", "GESPEICHERT IN", "^MILLIARDEN VON ^ZAHLEN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["riser", 0.5]]},
    {"id": "s05", "say": "Es sucht also das passendste Wort. Nicht unbedingt das wahre.",
     "caps": ["ES SUCHT DAS", "^PASSENDSTE WORT.", "NICHT UNBEDINGT", "DAS !WAHRE."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["card", "e-0.8"]]},
    {"id": "s06", "say": "Darum klingt eine Antwort auch dann überzeugend, wenn sie falsch ist.",
     "caps": ["DARUM KLINGT ES", "^ÜBERZEUGEND,", "AUCH WENN ES !FALSCH IST."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["stamp", "e-0.5"]]},
    {"id": "s07", "say": "Wichtige Fakten also immer selbst prüfen.",
     "caps": ["WICHTIGE FAKTEN", "IMMER ^SELBST ^PRÜFEN. ✅"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.2"]]},
    {"id": "s08", "say": "Folge für mehr Informatik in dreißig Sekunden!",
     "caps": ["FOLGE FÜR MEHR", "^INFORMATIK IN 30 SEK! 🔍"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.9], ["ding", "e+0.2"]]},
]
script = {
    "title": "Tech-Lupe – So funktioniert ChatGPT", "voice": "qwen3-tts (Klon Thorsten-Voice, CC0, Variante A ruhig)",
    "lead_in": 0.05, "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/thorsten.wav", "voice_text": "voice/thorsten.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 2, "temperature": 0.7},
    "music": {"bpm": 112, "inst": "vibes", "clap": 0.35, "ambience": 0.05,
              "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [48, 52, 55, 60], [45, 48, 52, 57]], "roots": [38, 34, 36, 33],
              "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("So funktioniert ChatGPT wirklich 🤖 Es rät Wort für Wort, was am besten passt, nicht was stimmt. "
       "Darum: wichtige Fakten selbst prüfen! Welches Thema als Nächstes? 👇 #informatik #ki #chatgpt #techtok #fyp")
pin = "📌 Hat dir eine KI auch schon mal etwas Falsches total überzeugt erzählt? Schreib's in die Kommentare 👇"
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Tech-Lupe (dein bestehender Kanal)
TECH-LUPE – FOLGE 3: SO FUNKTIONIERT CHATGPT WIRKLICH · TEXTE ZUM POSTEN
=======================================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTEN
Beim Posten „KI-generierte Inhalte“ einschalten (die Stimme ist ein KI-Klon der freien Thorsten-Voice-Stimme).
Mindestens 1 Tag Abstand zur vorigen Folge.

INHALT ZUM NACHPRÜFEN (bewusst vereinfacht)
Sprachmodelle wie ChatGPT berechnen für das nächste Textstück (genauer: Token, oft ein Wortstück) eine Wahrscheinlichkeit,
wählen eins aus, hängen es an und wiederholen das. Gelernt aus sehr großen Textmengen, gespeichert in Milliarden
Parametern; danach zusätzlich darauf trainiert, hilfreich zu antworten. Die Prozentwerte im Video sind Beispielwerte.
Das Australien-Beispiel ist zur Veranschaulichung (Hauptstadt ist Canberra).
""")
print(f"{len(segments)} Sätze")

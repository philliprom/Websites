"""Tech-Lupe – Folge 6: Wie Websites dein Passwort speichern (Hashing) und warum ein Datenleck trotzdem gefährlich ist.
Erste Folge mit HyperFrames (HeyGen, HTML → Video) statt der eigenen Engine; Stimme wie immer (Qwen3-TTS-Klon Thorsten A).
Erzeugt script.json und out/beschreibung.txt.  Aufruf: python3 techlupe-passwort/make_script.py
Fakten (geprüft 26.11.2026):
- Seriöse Dienste speichern nicht das Passwort, sondern einen Hash (Einwegfunktion, z. B. SHA-256; besser: langsame
  Passwort-Hashes mit Salt wie bcrypt/Argon2). Beim Login wird die Eingabe gehasht und mit dem gespeicherten Wert verglichen.
- SHA-256("passwort123") = 55789e79eca2f9a1e0786388b869f34f28a64ccbc37eb85ceeb031fd9677e06e (selbst berechnet).
- Zurückrechnen ist praktisch unmöglich; Angreifer raten stattdessen: Kandidaten (Wortlisten aus alten Leaks) hashen und
  vergleichen. Bei schnellen Verfahren schafft eine einzelne Spiele-Grafikkarte Milliarden Versuche pro Sekunde
  (hashcat-Benchmark RTX 4090: MD5 ≈ 164 Mrd./s, SHA-256 ≈ 22 Mrd./s; bcrypt Kosten 5 nur ≈ 184.000/s).
- Kurze/bekannte Passwörter fallen dadurch sofort; wer dasselbe Passwort überall nutzt, öffnet mit einem Leak alle Konten
  (Credential Stuffing). Empfehlung (BSI): lange Passwörter bzw. Passphrasen, für jeden Dienst ein eigenes,
  Passwort-Manager, Zwei-Faktor-Anmeldung.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Diese Website kennt dein Passwort gar nicht.",
     "caps": ["DIESE WEBSITE KENNT", "DEIN ^PASSWORT", "!GAR NICHT."], "gap": 0.0,
     "sfx": [["tick", 0.05], ["tick", 0.2], ["tick", 0.35], ["stamp", "e-0.5"]]},
    {"id": "s02", "say": "Gespeichert wird nur ein Fingerabdruck davon: ein sogenannter Hash.",
     "caps": ["GESPEICHERT WIRD NUR", "EIN ^FINGERABDRUCK:", "EIN ^HASH."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.4"]]},
    {"id": "s03", "say": "Aus passwort eins zwei drei wird immer dieselbe lange Zeichenkette.",
     "caps": ["AUS ^passwort123", "WIRD IMMER DIESELBE", "LANGE ^ZEICHENKETTE."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["tick", 1.2], ["tick", 1.4], ["tick", 1.6], ["tick", 1.8], ["ding", "e-0.3"]]},
    {"id": "s04", "say": "Zurückrechnen geht nicht. Das ist eine Einbahnstraße.",
     "caps": ["ZURÜCKRECHNEN?", "!GEHT NICHT.", "EINE ^EINBAHNSTRASSE."], "gap": 0.15,
     "sfx": [["poof", 0.9], ["stamp", "e-1.2"]]},
    {"id": "s05", "say": "Beim Login wird deine Eingabe wieder gehasht und verglichen. Gleicher Hash: Du bist drin.",
     "caps": ["BEIM LOGIN: WIEDER HASHEN", "UND ^VERGLEICHEN.", "GLEICHER HASH:", "^DU BIST DRIN. ✅"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["tick", 1.4], ["tick", 1.6], ["ding", "e-0.4"]]},
    {"id": "s06", "say": "Gefährlich wird es bei einem Datenleck. Angreifer hashen einfach Millionen bekannter Passwörter und vergleichen.",
     "caps": ["GEFÄHRLICH WIRD'S", "BEI EINEM !DATENLECK.", "ANGREIFER HASHEN", "^MILLIONEN BEKANNTE", "PASSWÖRTER UND VERGLEICHEN."], "gap": 0.25,
     "sfx": [["sting", -0.05], ["riser", 2.0], ["tick", 3.0], ["tick", 3.2], ["tick", 3.4], ["tick", 3.6], ["tick", 3.8]]},
    {"id": "s07", "say": "Bei schnellen Verfahren schafft eine einzige Grafikkarte Milliarden Versuche pro Sekunde.",
     "caps": ["EINE EINZIGE GRAFIKKARTE:", "!MILLIARDEN VERSUCHE", "PRO SEKUNDE."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["stamp", "e-0.6"], ["sting", "e-0.55"]]},
    {"id": "s08", "say": "Kurze Passwörter sind sofort geknackt. Und wer überall dasselbe nutzt, verliert alle Konten auf einmal.",
     "caps": ["KURZE PASSWÖRTER:", "!SOFORT GEKNACKT.", "ÜBERALL DASSELBE?", "!ALLE KONTEN OFFEN."], "gap": 0.2,
     "sfx": [["stamp", 1.3], ["pop", 2.6], ["pop", 2.8], ["pop", 3.0], ["pop", 3.2], ["sting", "e-0.5"]]},
    {"id": "s09", "say": "Also: lange Passwörter, für jede Seite ein eigenes. Ein Passwort-Manager merkt sie sich für dich.",
     "caps": ["LANGE PASSWÖRTER,", "FÜR JEDE SEITE ^EIN ^EIGENES.", "EIN ^PASSWORT-MANAGER", "MERKT SIE SICH. 🔐"], "gap": 0.25,
     "sfx": [["whoosh", -0.05], ["ding", 2.2], ["sparkle", "e-0.6"]]},
    {"id": "s10", "say": "Folge für mehr Informatik, einfach erklärt!",
     "caps": ["FOLGE FÜR MEHR", "^INFORMATIK,", "EINFACH ERKLÄRT! 🔍"], "gap": 0.2,
     "sfx": [["title", -0.05]]},
]
script = {
    "title": "Tech-Lupe – Wie Websites dein Passwort speichern",
    "voice": "qwen3-tts (Klon Thorsten-Voice, CC0, Variante A ruhig)",
    "lead_in": 0.05, "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/thorsten.wav", "voice_text": "voice/thorsten.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "vibes", "clap": 0.35, "ambience": 0.05,
              "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [48, 52, 55, 60], [45, 48, 52, 57]],
              "roots": [38, 34, 36, 33], "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(
    """TECH-LUPE – WIE WEBSITES DEIN PASSWORT SPEICHERN · TEXTE ZUM POSTEN
=================================================================

BESCHREIBUNG (Caption):
Die Website kennt dein Passwort gar nicht 🤯 Sie speichert nur einen Hash – und warum ein Datenleck trotzdem gefährlich ist. 🔐 #informatik #passwort #itsicherheit #lernenmittiktok #techlupe

ERSTER KOMMENTAR:
Welches Thema soll die Tech-Lupe als Nächstes erklären? 👇

FAKTEN (für Rückfragen in den Kommentaren):
- Seriöse Dienste speichern einen Hash (Einwegfunktion), keine Passwörter. Beim Login wird verglichen.
- SHA-256 von „passwort123“ = 55789e79eca2f9a1e0786388b869f34f28a64ccbc37eb85ceeb031fd9677e06e
- Schnelle Verfahren: eine RTX 4090 schafft laut hashcat-Benchmark ca. 22 Mrd. SHA-256-Versuche pro Sekunde.
  Gute Dienste nutzen langsame Verfahren mit Salt (bcrypt, Argon2): dort nur Tausende pro Sekunde.
- Empfehlung (BSI): lang, für jeden Dienst ein eigenes Passwort, Passwort-Manager, Zwei-Faktor-Anmeldung.

POSTEN
- „KI-generierte Inhalte“ einschalten (Stimme ist ein KI-Klon).
""")
print(f"script.json: {len(segments)} Sätze, {sum(len(s['say']) for s in segments)} Zeichen")

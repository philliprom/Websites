"""Wo geht dein Geld hin? – Folge 1: Der 8-Euro-Döner. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 geld-doener/make_script.py

Belegte Zahlen (Recherche 18.11.2026):
- Typischer Dönerpreis 2026: etwa 7,50–8,50 € (Preisvergleiche 2026); wir rechnen mit 8,00 €.
- Mehrwertsteuer auf Speisen in der Gastronomie seit 01.01.2026 dauerhaft 7 % (Steueränderungsgesetz 2025, Bundesrat 19.12.2025),
  gleich ob im Laden oder zum Mitnehmen. 8,00 € brutto → 0,52 € Mehrwertsteuer.
- Zutaten laut Verband der Dönerproduzenten (via Hürriyet/Jacobin): Fleisch 125 g 2,00 €, Brot 245 g 0,38 €, Salat/Gemüse 135 g 0,39 €,
  Soße 25 g 0,15 €, Gewürze 10 g 0,08 € = 3,00 €.
Beispielrechnung (Annahmen, so gekennzeichnet): Fixkosten 12.000 €/Monat = Miete 3.000 € + 2 Vollzeitkräfte zum Mindestlohn
13,90 €/h (2026) inkl. Arbeitgeberanteil ≈ 5.800 € + Strom/Gas/Wasser 900 € + Sonstiges (Versicherung, Kasse, Kartengebühren,
Geräte, Buchhaltung) 2.300 €; Verpackung 0,10 €/Döner; 30 Tage.
150 Döner/Tag → Fixkosten 2,67 €/Döner → Gewinn vor Steuern 1,71 €/Döner. 60 Döner/Tag → 6,67 €/Döner → −2,29 €/Döner.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Du zahlst acht Euro für einen Döner. Aber was bleibt davon eigentlich beim Laden?",
     "caps": ["DU ZAHLST ^8 ^EURO", "FÜR EINEN DÖNER.", "ABER WAS BLEIBT", "DAVON !BEIM !LADEN?"], "gap": 0.0,
     "sfx": [["kaching", 0.1], ["sting", "e-1.0"]]},
    {"id": "s02", "say": "Zweiundfünfzig Cent bekommt das Finanzamt. Das ist die Mehrwertsteuer.",
     "caps": ["!52 !CENT BEKOMMT", "DAS ^FINANZAMT.", "DIE ^MEHRWERTSTEUER."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["stamp", 0.5]]},
    {"id": "s03", "say": "Drei Euro kosten die Zutaten. Allein das Fleisch kostet zwei Euro.",
     "caps": ["^3 ^EURO FÜR", "DIE ZUTATEN.", "ALLEIN DAS FLEISCH:", "!2 !EURO."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", 0.5], ["pop", 0.7], ["pop", 0.9], ["pop", 1.1], ["pop", 1.3]]},
    {"id": "s04", "say": "Bleiben vier Euro achtundvierzig. Davon zahlt der Laden Miete, Personal und Strom.",
     "caps": ["BLEIBEN ^4,48 ^EURO.", "DAVON ZAHLT DER LADEN", "MIETE, PERSONAL", "UND STROM."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["pop", "e-1.6"], ["pop", "e-1.0"], ["pop", "e-0.4"]]},
    {"id": "s05", "say": "Verkauft ein Laden hundertfünfzig Döner am Tag, sind das rund zwei Euro siebzig pro Döner.",
     "caps": ["VERKAUFT EIN LADEN", "^150 DÖNER AM TAG,", "SIND DAS RUND", "!2,70 !EURO PRO DÖNER."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["card", 0.6]]},
    {"id": "s06", "say": "Dann bleiben etwa ein Euro siebzig. Vor Steuern. Und davon muss der Inhaber leben.",
     "caps": ["DANN BLEIBEN ETWA", "^1,70 ^EURO.", "VOR STEUERN.", "DAVON LEBT DER INHABER."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["kaching", 0.9]]},
    {"id": "s07", "say": "Verkauft der Laden aber nur sechzig Döner am Tag, macht er mit jedem über zwei Euro Verlust.",
     "caps": ["NUR ^60 DÖNER AM TAG?", "DANN MACHT ER", "MIT JEDEM !ÜBER !2 !EURO", "!VERLUST."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["boing", "e-0.8"]]},
    {"id": "s08", "say": "Darum kann der volle Laden oft günstiger sein als der leere.",
     "caps": ["DARUM KANN DER", "^VOLLE LADEN OFT", "^GÜNSTIGER SEIN", "ALS DER LEERE."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", "e-0.2"]]},
    {"id": "s09", "say": "Was kostet der Döner bei dir? Schreib es in die Kommentare!",
     "caps": ["WAS KOSTET DER", "^DÖNER BEI DIR?", "SCHREIB ES IN DIE", "^KOMMENTARE! 👇"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.8], ["ding", "e+0.2"]]},
]
script = {
    "title": "Wo geht dein Geld hin? – Döner", "voice": "qwen3-tts (Klon Thorsten-Voice, CC0, Variante A ruhig)",
    "lead_in": 0.05, "tail": 2.0, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/thorsten.wav", "voice_text": "voice/thorsten.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.6, "max_pause": 0.45},
    "music": {"bpm": 104, "inst": "marimba", "clap": 0.4, "ambience": 0.05,
              "chords": [[57, 60, 64, 67], [53, 57, 60, 64], [50, 53, 57, 60], [52, 55, 59, 64]], "roots": [45, 41, 38, 40],
              "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Du zahlst 8 € für deinen Döner. Aber was bleibt davon beim Laden? 🥙💸 52 Cent Steuer, 3 € Zutaten und der Rest … "
       "Was kostet der Döner bei dir? 👇 #döner #preise #geld #wirtschaft #fyp")
pin = ("📌 Beispielrechnung: Zutaten laut Verband der Dönerproduzenten, Mehrwertsteuer 7 % (seit 2026), "
       "Miete/Personal/Strom angenommen für einen Laden mit 150 Dönern am Tag. Wie viel zahlst du in deiner Stadt? 👇")
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Wo geht dein Geld hin? (zweites Konto, vorher @monsterdoener – bitte umbenennen)
FOLGE 1: DER 8-EURO-DÖNER · TEXTE ZUM POSTEN
============================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

PROFIL
Profilbild: profilbild_logo.png (Euro-Münze im Ringdiagramm, empfohlen) · Alternative: profilbild_tag.png (Preisschild „€?“)
Name: Wo geht dein Geld hin? 💸
Nutzername (falls frei, der Reihe nach probieren): @wogehtdeingeld · @wo.geht.dein.geld · @geldroentgen
Bio (65 Zeichen, TikTok erlaubt 80): Alltagspreise auseinandergenommen 💸 Was steckt wirklich im Preis?

POSTEN
Beim Posten „KI-generierte Inhalte“ einschalten (die Stimme ist ein KI-Klon der freien Thorsten-Voice-Stimme).

ZAHLEN UND QUELLEN (falls jemand fragt)
- Preis: typischer Dönerpreis 2026 etwa 7,50–8,50 €, gerechnet mit 8,00 €.
- Mehrwertsteuer: seit 01.01.2026 dauerhaft 7 % auf Speisen in der Gastronomie (auch im Laden), 8,00 € → 0,52 €.
- Zutaten (Verband der Dönerproduzenten): Fleisch 2,00 €, Brot 0,38 €, Salat 0,39 €, Soße 0,15 €, Gewürze 0,08 € = 3,00 €.
- Beispielrechnung (Annahmen): Fixkosten 12.000 € im Monat (Miete 3.000 €, 2 Vollzeitkräfte zum Mindestlohn ≈ 5.800 €,
  Strom/Gas/Wasser 900 €, Sonstiges 2.300 €), Verpackung 0,10 € pro Döner, 30 Tage.
  150 Döner/Tag → 2,67 € Fixkosten pro Döner → 1,71 € Gewinn vor Steuern.
  60 Döner/Tag → 6,67 € Fixkosten pro Döner → 2,29 € Verlust pro Döner.
""")
print(f"{len(segments)} Sätze")

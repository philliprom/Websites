"""Tech-Lupe – Folge 5: IPv4 vs. IPv6. Erzeugt script.json und out/beschreibung.txt.
Aufruf: python3 techlupe-ipv6/make_script.py
Fakten (geprüft 24.11.2026):
- IPv4: 32 Bit → 2^32 = 4.294.967.296 Adressen, geschrieben als 4 Zahlen 0–255 (Beispiel 203.0.113.42 aus dem
  Dokumentationsbereich TEST-NET-3, RFC 5737).
- RIPE NCC (Europa, Naher Osten, Teile Zentralasiens) hat am 25.11.2019 die letzten freien IPv4-Adressen vergeben
  (danach nur noch Warteliste mit zurückgegebenen Adressen). IANA-Vorrat war schon 2011 leer.
- Notlösung NAT: Router hat eine öffentliche Adresse, Geräte zu Hause private Adressen (z. B. 192.168.178.x).
- IPv6: 128 Bit → 2^128 = 340.282.366.920.938.463.463.374.607.431.768.211.456 ≈ 3,4·10^38 = 340 Sextillionen.
  Geschrieben als 8 Blöcke à 4 Hex-Ziffern (Beispiel 2001:db8:… aus dem Dokumentationsbereich, RFC 3849).
- Sandkörner der Erde (Schätzung ≈ 7,5·10^18): 3,4·10^38 / 7,5·10^18 ≈ 4,5·10^19 Adressen pro Sandkorn → „billionenfach“ stimmt.
- Google-Statistik: Anteil der Nutzer, die Google über IPv6 erreichen, 2026 um 50 % (erstmals über 50 % am 28.03.2026,
  danach wieder knapp darunter). Daher „rund die Hälfte der Zugriffe auf Google“.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
segments = [
    {"id": "s01", "say": "Europa hat keine freien Internet-Adressen mehr. Die letzten wurden zweitausendneunzehn vergeben.",
     "caps": ["EUROPA HAT KEINE FREIEN", "!INTERNET-ADRESSEN MEHR.", "DIE LETZTEN GINGEN", "^2019 WEG."], "gap": 0.0,
     "sfx": [["tick", 0.05], ["tick", 0.25], ["tick", 0.45], ["stamp", 1.6], ["sting", 1.65]]},
    {"id": "s02", "say": "Jedes Gerät im Internet braucht eine IP-Adresse. Wie eine Hausnummer, damit die Datenpakete ankommen.",
     "caps": ["JEDES GERÄT BRAUCHT", "EINE ^IP-ADRESSE.", "WIE EINE ^HAUSNUMMER,", "DAMIT PAKETE ANKOMMEN. 📨"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.6], ["whoosh", "e-1.6"], ["ding", "e-0.3"]]},
    {"id": "s03", "say": "Die alte Version heißt I P V vier. Vier Zahlen, jede von null bis zweihundertfünfundfünfzig.",
     "caps": ["DIE ALTE VERSION:", "^IPv4", "4 ZAHLEN, JEDE", "VON ^0 BIS ^255."], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 1.4], ["pop", 1.6], ["pop", 1.8], ["pop", 2.0]]},
    {"id": "s04", "say": "Das sind zweiunddreißig Bit. Also nur gut vier Komma drei Milliarden Adressen.",
     "caps": ["DAS SIND ^32 ^BIT.", "ALSO NUR GUT", "^4,3 MILLIARDEN ADRESSEN."], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["tick", 0.4], ["tick", 0.6], ["tick", 0.8], ["tick", 1.0], ["ding", "e-0.4"]]},
    {"id": "s05", "say": "Klingt viel. Aber es gibt längst mehr Geräte als Adressen.",
     "caps": ["KLINGT VIEL.", "ABER ES GIBT LÄNGST", "!MEHR GERÄTE ALS ADRESSEN."], "gap": 0.15,
     "sfx": [["pop", 0.3], ["pop", 0.5], ["pop", 0.7], ["pop", 0.9], ["sting", "e-0.8"]]},
    {"id": "s06", "say": "Die Notlösung: Dein Router teilt sich eine einzige Adresse mit allen Geräten bei dir zu Hause.",
     "caps": ["DIE NOTLÖSUNG:", "DEIN ^ROUTER TEILT", "^EINE ADRESSE MIT", "ALLEN GERÄTEN ZU HAUSE. 🏠"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 1.3], ["pop", 1.5], ["pop", 1.7], ["ding", "e-0.5"]]},
    {"id": "s07", "say": "Die echte Lösung heißt I P V sechs. Mit hundertachtundzwanzig Bit statt zweiunddreißig.",
     "caps": ["DIE ECHTE LÖSUNG:", "^IPv6", "^128 BIT", "STATT 32."], "gap": 0.25,
     "sfx": [["riser", -0.2], ["whoosh", 0.0], ["ding", 1.6]]},
    {"id": "s08", "say": "Das sind dreihundertvierzig Sextillionen Adressen. Genug für jedes Sandkorn der Erde, und zwar billionenfach.",
     "caps": ["DAS SIND ^340", "!SEXTILLIONEN ADRESSEN.", "GENUG FÜR JEDES", "^SANDKORN DER ERDE,", "UND ZWAR BILLIONENFACH. 🏖️"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["kaching", 0.9], ["sparkle", "e-1.5"]]},
    {"id": "s09", "say": "Schon rund die Hälfte der Zugriffe auf Google läuft über I P V sechs. Dein Handy kann meistens beides.",
     "caps": ["SCHON RUND ^DIE ^HÄLFTE", "DER ZUGRIFFE AUF GOOGLE", "LÄUFT ÜBER ^IPv6.", "DEIN HANDY KANN", "MEISTENS ^BEIDES. 📱"], "gap": 0.15,
     "sfx": [["whoosh", -0.05], ["ding", 1.4], ["pop", "e-1.0"], ["pop", "e-0.8"]]},
    {"id": "s10", "say": "Folge für mehr Informatik, einfach erklärt!",
     "caps": ["FOLGE FÜR MEHR", "^INFORMATIK, EINFACH ERKLÄRT! 🔍"], "gap": 0.2,
     "sfx": [["whoosh", -0.05], ["pop", 0.9], ["ding", "e+0.2"]]},
]
script = {
    "title": "Tech-Lupe – IPv4 vs. IPv6", "voice": "qwen3-tts (Klon Thorsten-Voice, CC0, Variante A ruhig)",
    "lead_in": 0.05, "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "qwen", "voice": "voice/thorsten.wav", "voice_text": "voice/thorsten.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.7, "max_pause": 0.45},
    "music": {"bpm": 112, "inst": "vibes", "clap": 0.35, "ambience": 0.05,
              "chords": [[50, 53, 57, 62], [46, 50, 53, 58], [48, 52, 55, 60], [45, 48, 52, 57]], "roots": [38, 34, 36, 33],
              "arp": [0, 2, 1, 3, 2, 3, 1, 2]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
cap = ("Europa hat seit 2019 keine freien IPv4-Adressen mehr 😳 Warum das Internet umzieht und was IPv6 damit zu tun hat, "
       "einfach erklärt. Welches Thema als Nächstes? 👇 #informatik #netzwerk #ipv6 #itausbildung #techtok #fyp")
pin = "📌 Fun Fact: IPv5 gab es auch, aber nur als Experiment fürs Streaming. Welches Netzwerk-Thema soll ich als Nächstes erklären? 👇"
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""KANAL: Tech-Lupe (dein bestehender Kanal)
TECH-LUPE – FOLGE 5: IPv4 VS. IPv6 · TEXTE ZUM POSTEN
=====================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTEN
Beim Posten „KI-generierte Inhalte“ einschalten (die Stimme ist ein KI-Klon der freien Thorsten-Voice-Stimme).
Mindestens 1 Tag Abstand zur vorigen Folge.

INHALT ZUM NACHPRÜFEN
IPv4: 32 Bit, 2^32 = 4.294.967.296 Adressen, 4 Zahlen 0–255. RIPE NCC (Europa) hat am 25.11.2019 die letzten freien
IPv4-Adressen vergeben (IANA-Vorrat schon 2011 leer). Notlösung NAT: eine öffentliche Adresse am Router, private Adressen
(192.168.x.x) zu Hause. IPv6: 128 Bit, 2^128 ≈ 3,4·10^38 = 340 Sextillionen Adressen, 8 Blöcke Hex. Sandkörner der Erde
(Schätzung ≈ 7,5·10^18) → ≈ 4,5·10^19 Adressen pro Sandkorn. Google: rund 50 % der Nutzer erreichen Google über IPv6 (2026).
Beispieladressen im Video stammen aus den Dokumentationsbereichen (203.0.113.0/24, 2001:db8::/32), sind also keine echten Geräte.
""")
print(f"{len(segments)} Sätze")

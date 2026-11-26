# Tech-Lupe – Serien-Gedächtnis

Bestehender TikTok-Kanal des Kanalinhabers (selbst Informatiker), wird zu „Informatik in 30 Sekunden“ umgebaut.
Machart: reine Bewegtgrafik (Engine-Ebene `alt`, dunkles Tech-Design, JetBrains Mono, Cyan/Gelb/Rot), Erzählerstimme
Qwen3-TTS-Klon von Thorsten-Voice (CC0), Variante A „ruhig“ (`stimmproben/README.md`). Beim Posten „KI-generierte Inhalte“ an.

## Regeln
- Sichere Zonen: `node engine/safe_check.cjs <projekt>` muss „alles frei ✓“ melden (18.11.: Kanalname oben und
  Untertitel-Enden rechts waren von TikTok verdeckt).
- Erstes Bild = das überraschende Ergebnis (Terminal mit falscher Rechnung, Uhr springt auf 1901 …), kein Vorspann.
- Ein Thema, ein Aha, Zahlen vorher nachrechnen (Faktenblock in `make_script.py` und `beschreibung.txt`).
- Zahlen in `say` als Wörter schreiben („zweiunddreißig Bit“), in `caps` als Ziffern. Whisper liest Zahlen als Ziffern,
  deshalb wirkt die WER bei Zahlensätzen hoch, obwohl der Ton stimmt.
- Schluss: „Folge für mehr Informatik in dreißig Sekunden!“ (bis 30 s) bzw. „Folge für mehr Informatik, einfach erklärt!“
  (längere Folgen bis 60 s, vom Kanalinhaber erlaubt) + Themenfrage in den Kommentaren.

## Themenwahl
Kanalinhaber 17.11.: lieber **relevante, wichtige** Informatik statt Kuriositäten (0,1 + 0,2 und 2038 waren ihm zu speziell).
Also Themen, die jeden betreffen: KI, Passwörter/Sicherheit, Internet, Datenschutz, wie Apps Daten sammeln.

## Folgen
| Nr. | Ordner | Thema | Länge | Stand |
|---|---|---|---|---|
| 1 | `techlupe-test/` | Warum 0,1 + 0,2 = 0,30000000000000004 | 34,1 s | fertig, noch nicht gepostet |
| 2 | `techlupe-2038/` | Das Jahr-2038-Problem (Unix-Zeit, 32 Bit → 1901, Lösung 64 Bit) | 37,1 s | fertig 17.11. |
| 3 | `techlupe-ki/` | So funktioniert ChatGPT wirklich (nächstes Wort, Wahrscheinlichkeiten, passend ≠ wahr, selbst prüfen) | 29,6 s | fertig 17.11. |
| 4 | `techlupe-switch/` | Hub vs. Switch (Hub kopiert an alle, Kollision, Switch lernt MAC-Adressen, gezielt + gleichzeitig, Router) | 52,9 s | fertig 18.11. (Wunsch des Kanalinhabers, bis 60 s erlaubt) |
| 5 | `techlupe-ipv6/` | IPv4 vs. IPv6 (Europa seit 25.11.2019 ohne freie IPv4-Adressen, Hausnummer, 4 Zahlen 0–255, 32 Bit = 4,3 Mrd, mehr Geräte als Adressen, NAT im Router, IPv6 128 Bit = 340 Sextillionen, Sandkörner, rund 50 % der Google-Zugriffe) | 52,1 s | fertig 24.11. (Wunsch des Kanalinhabers), −14,4 LUFS, sichere Zonen frei |

Themen-Ideen (relevant): Wie Passwörter gespeichert werden und warum Leaks gefährlich sind (Hashing) · Was HTTPS/das Schloss
wirklich schützt · Was passiert, wenn du google.de eintippst (DNS, IP, Pakete) · Wie Phishing-Links tricksen ·
Was Cookies über dich wissen · Warum KI-Bilder erkennbar sind (oder nicht) · Was ein Algorithmus ist (TikTok-Feed).

## ElevenLabs (Stand 26.11.2026)
- Stimme laut Kanalinhaber: **George** (Voice-ID `JBFqnCBsd6RMkjVDRZzb`), Modell `eleven_multilingual_v2`, speed 1,1.
- Schlüssel liegen NICHT im Repository; sie werden über das sichere Formular als Netzwerk-Geheimnis der Umgebung
  gespeichert (Header `xi-api-key` für api.elevenlabs.io).
- 26.11.: Konto „neu“ (kostenlos, 2.866 Zeichen frei) lehnt jede Erzeugung ab: „Unusual activity … Free Tier access
  has been disabled“ (laut ElevenLabs ausgelöst durch Proxy/VPN oder mehrere kostenlose Konten). Nutzbar nur mit
  bezahltem Tarif. Ohnehin gilt im kostenlosen Tarif: keine kommerzielle Nutzung, „elevenlabs.io“ muss im Titel stehen.

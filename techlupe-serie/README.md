# Tech-Lupe – Serien-Gedächtnis

Bestehender TikTok-Kanal des Kanalinhabers (selbst Informatiker), wird zu „Informatik in 30 Sekunden“ umgebaut.
Machart: reine Bewegtgrafik (Engine-Ebene `alt`, dunkles Tech-Design, JetBrains Mono, Cyan/Gelb/Rot), Erzählerstimme
Qwen3-TTS-Klon von Thorsten-Voice (CC0), Variante A „ruhig“ (`stimmproben/README.md`). Beim Posten „KI-generierte Inhalte“ an.

## Regeln
- Erstes Bild = das überraschende Ergebnis (Terminal mit falscher Rechnung, Uhr springt auf 1901 …), kein Vorspann.
- Ein Thema, ein Aha, Zahlen vorher nachrechnen (Faktenblock in `make_script.py` und `beschreibung.txt`).
- Zahlen in `say` als Wörter schreiben („zweiunddreißig Bit“), in `caps` als Ziffern. Whisper liest Zahlen als Ziffern,
  deshalb wirkt die WER bei Zahlensätzen hoch, obwohl der Ton stimmt.
- Schluss immer: „Folge für mehr Informatik in dreißig Sekunden!“ + Themenfrage in den Kommentaren.

## Folgen
| Nr. | Ordner | Thema | Länge | Stand |
|---|---|---|---|---|
| 1 | `techlupe-test/` | Warum 0,1 + 0,2 = 0,30000000000000004 | 34,1 s | fertig, noch nicht gepostet |
| 2 | `techlupe-2038/` | Das Jahr-2038-Problem (Unix-Zeit, 32 Bit → 1901, Lösung 64 Bit) | 37,1 s | fertig 17.11. |

Themen-Ideen: Warum Passwörter mit 8 Zeichen schnell geknackt sind · Was passiert, wenn du google.de eintippst (DNS) ·
Warum Computer keinen echten Zufall können · Wie ein QR-Code trotz Kratzer funktioniert (Fehlerkorrektur) ·
Warum 1 KB manchmal 1024 Byte ist.

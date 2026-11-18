# „Wo geht dein Geld hin?“ – Serien-Gedächtnis

Zweiter Kanal (Konto vorher @monsterdoener, umbenennen). Alltagspreise auseinandergenommen: Preisschild zerfällt in seine
Teile. Bewegtgrafik (Engine-Ebene `alt`), dunkelgrün/gold, Preisbalken oben (Gesamtpreis = volle Breite), Kassenbon,
Preisschilder. Stimme: Qwen3-TTS-Klon Thorsten-Voice (CC0), Variante A, 3 Fassungen pro Satz, `max_pause` 0,45 s.

## Regeln
- Zahlen vorher recherchieren, Quellen in `make_script.py` und `beschreibung.txt`; was angenommen ist, im Bild als
  „Beispiel“ kennzeichnen.
- Aussprache prüfen: `build/tts_qa.txt` lesen. Wörter, die Whisper anders hört, umformulieren statt hoffen
  (17.11.: „an den Staat“ wurde als „Start“ gehört → „bekommt das Finanzamt“; „Dönern“ → „Döhnen“ → Satz mit „Döner“).
- Zahlen als Wörter in `say`, keine Abkürzungen (MwSt → Mehrwertsteuer), kein €-Zeichen in `say`.
- Schluss: Frage, die jeder beantworten kann („Was kostet der Döner bei dir?“).

## Folgen
| Nr. | Ordner | Thema | Länge | Stand |
|---|---|---|---|---|
| 1 | `geld-doener/` | Der 8-Euro-Döner: 0,52 € Mehrwertsteuer, 3,00 € Zutaten, Rest, Beispiel-Laden 150 vs. 60 Döner am Tag | 42,0 s | fertig 18.11. |

Ideen: Tankfüllung (Energiesteuer, CO2-Preis, Mehrwertsteuer) · Kinoticket · Konzertkarte · Spotify-Stream ·
Handyvertrag · Pfandflasche · Coffee to go · Deutschlandticket.

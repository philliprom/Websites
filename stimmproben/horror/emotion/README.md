# Stimmtest „mehr Gefühl“ (25.11.2026)

Wunsch des Kanalinhabers für Teil 2: mehr Emotion, an spannenden Stellen soll die Stimme etwas höher gehen,
aber natürlich klingen. Testtext (7 Sätze, Spannung steigt von Stufe 0 bis 3):

> Das Klopfen hört auf. Einfach so. · Du hältst die Luft an. Und dann hörst du es. · Schritte. Nicht draußen. ·
> Sondern hinter dir, im Lager!

| Hörprobe | Wie entstanden |
|---|---|
| `1_wie_teil1.m4a` | Klon mit der normalen Referenz, Einstellungen wie in Teil 1 (zum Vergleich) |
| `2_mehr_gefuehl_gesprochen.m4a` | Sätze ab Stufe 1 mit einer Referenz derselben Stimme, die per PSOLA 1,5 bzw. 3 Halbtöne höher und 5–10 % schneller ist. Das Modell spricht dann selbst höher, Betonung bleibt seine eigene |
| `3_mehr_gefuehl_nachbearbeitet.m4a` | Fassung 1, jeder Satz nach Stufe angehoben (Praat-PSOLA, Klangfarbe bleibt): +1/+2/+3 Halbtöne, etwas schneller, größerer Tonumfang, im letzten Satz zusätzlich steigend |
| `4_mehr_gefuehl_ausgewaehlt.m4a` | Normale Referenz, aber für spannende Sätze 6 Fassungen mit etwas mehr Zufall (Temperatur 0,85) und davon die genommen, die von sich aus 1,5/2,5/3,5 Halbtöne höher liegt (Engine-Option `pitch_up`). Nichts nachbearbeitet |

In 2, 3 und 4 werden spannende Sätze außerdem 1–3 dB lauter (in Teil 1 wurden alle Sätze gleich laut gemacht).

Befund beim Bau: Die Auswahl in Teil 1 nahm immer die Fassung nahe der Referenztonhöhe (96 Hz). Lebhaftere Fassungen,
die das Modell von sich aus höher sprach (109 Hz bei „Du hältst die Luft an“ und beim letzten Satz), wurden dadurch
verworfen. Das hat die Stimme mit flach gemacht. Daraus entstand Fassung 4.
Aufruf und Ablauf: `gefuehl.py` (Kopf der Datei).

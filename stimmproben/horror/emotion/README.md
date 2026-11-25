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

## Ergebnis (Messung, Tonhöhe je Satz in Hz)

| Fassung | Stufe 0 | 0 | 1 | 1 | 2 | 2 | 3 | Sprechzeit | Tonumfang spannende Sätze |
|---|---|---|---|---|---|---|---|---|---|
| 1 wie Teil 1 | 78 | 76 | 91 | 92 | 78 | 85 | 99 | 8,9 s | 8,8 Halbtöne |
| 2 Vorlage höher | 78 | 76 | 94 | 96 | 78 | 72 | 112 | 8,9 s | 8,9 |
| 3 nachbearbeitet | 78 | 75 | 98 | 98 | 89 | 97 | 125 | 8,5 s | 12,3 |
| 4 ausgewählt | 78 | 76 | 96 | 95 | 70 | 77 | 99 | 9,1 s | 7,8 |

- 3 hebt wie geplant stufenweise an (+1 bis +4 Halbtöne, lebendigere Satzmelodie), Stimmqualität gleich
  (HNR 10,9 dB gegenüber 10,8 dB bei Fassung 1, keine Knackser). 2 wirkt vor allem im letzten Satz (+2 Halbtöne).
- 4 hat nicht funktioniert: Mit der ruhigen Vorlage spricht das Modell auch unter 6 Fassungen kaum von sich aus höher
  (Ziel 105–118 Hz, erreicht 86–101 Hz). „Schritte.“ kam dabei geflüstert heraus und wurde nur gewählt, weil eine
  nicht messbare Tonhöhe bisher keine Strafpunkte bekam (in `engine/build_timeline.py` behoben). Fassung 4 wird deshalb
  nicht verschickt. Die Option `pitch_up` bleibt in der Engine, hilft aber nur zusammen mit einer lebhafteren Vorlage.
- Verschickt an den Kanalinhaber: 1, 2 und 3. Er entscheidet nach Gehör, ob 2 oder 3 für Teil 2 genommen wird.

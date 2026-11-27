# DER FEUERALARM · TEIL 2

Folge im Format „Unbekannte Nummer“ (Skill `unbekannte-nummer`). Fortsetzung von `feueralarm-teil1/`.
Die Zuschauer haben in den Kommentaren **AUTO** gewählt (der Nummer glauben).

## Geschichte (68,6 s inkl. 4 s Endkarte)

1. **Rückblick (≤ 2,5 s):** Handy mit Regel 5 in Papas Stimme: „Hinterhof. Blaues Auto.“ Darunter „TEIL 2 · Ihr habt gewählt: AUTO“.
2. **Keller:** Pohl ruft „Das ist eine Falle!“, Noah rennt los, Ben hinterher.
3. **Hinterhof im Regen:** blaues Auto mit laufendem Motor. Ein Mann mit Sonnenbrille steigt aus: „Dein Vater schickt mich.“
   Ben: „Woher kennt der Typ deinen Namen?“ Frau Sander reißt die Tür auf: „Bleib stehen!“ – rein ins Auto.
4. **Im Auto:** Türen zu, Zentralverriegelung klackt. „Anschnallen. Und Kopf runter.“
5. **Regel 6 (Papa):** „Falsches Auto. Ich warte hinter der Turnhalle. Steig AUS.“
6. **Wendung:** Das Handy des Fahrers klingelt – auf dem Bildschirm steht **SANDER**.
7. **Regel 7 (Papa):** „An der Ampel. Fenster hinten rechts geht auf. Raus, wenn es grün wird.“
8. Rote Ampel, Noah tastet nach dem Fensterheber: „Finger weg vom Fenster, Noah.“ Ben: „Was machen wir?“
9. **Cliffhanger:** Die Ampel springt auf Rot-Gelb. Endkarte: **FENSTER** (Regel 7 folgen) oder **SITZEN BLEIBEN**.

Lehren aus Teil 1 (9.000 Aufrufe, Ø 51 s geschaut, 17,5 % bis zum Ende, 101 neue Follower) umgesetzt:
kürzer, Rückblick nur 2 Sekunden, Bedrohung ab der ersten Sekunde, alle paar Sekunden etwas Neues.

## Neu gegenüber Teil 1

| Datei | Neu |
|---|---|
| `set_hof.py` | Hinterhof (Regen, Turnhalle, Notausgang), Straße mit Häusern, Bäumen, Laternen, geparkten Autos, Ampel; Auto mit Innenraum (hoher Fahrgastraum, damit die großen Toon-Köpfe unters Dach passen) |
| `cast.py`, `figur.py` | Fahrer (Mütze, Sonnenbrille, Vollbart, schwarze Jacke) |
| `anim.py` | `follow`: Figuren und Kamera fahren mit dem Auto mit (Positionen im Auto relativ zum Auto) |
| `render_shot.py` | Autofahrt (`car_y_fn`: anfahren, Stadttempo, bremsen hinter einem wartenden Auto), Ampelphasen als Schlüsselbilder (`c.ampel`), Scheiben im Auto ausblenden (Glanzstreifen bleiben sichtbar), Bildschirm des Fahrer-Handys |
| `sound.py` | Regen, Alarm aus dem Gebäude, Motor nach Drehzahl, Fahrgeräusch nach Tempo, Autotüren, Zentralverriegelung, Klingelton, Fensterheber-Klicks |
| `assemble.py` | Hinweis „Ihr habt gewählt“, Regen im Hof, Farbe je Ort (Hof, Auto), Endkarte mit Fenster- und Sitz-Symbol |

## Befehle

Siehe `.claude/skills/unbekannte-nummer/references/produktion.md`. Sets: `keller` (aus Teil 1), `hof`, `auto`.

## Prüfung (fertiges Video)

- 1080×1920, 68,6 s, −14,6 LUFS, Spitze −1,3 dBFS
- Aussprache im Endmix (`aussprache_endmix.py`): 21 von 22 Zeilen exakt; die eine Abweichung ist nur die Schreibweise
  („dahinten“ statt „da hinten“), gesprochen identisch
- Stimme überall ≥ 12 dB über Hintergrund (knappste Zeile: Rückblick r5 mit 12,7 dB)
- Kontaktbogen alle 3 s geprüft: Banner, Hinweis „Ihr habt gewählt“, Untertitel, Regen nur im Hof, Endkarte

## Ausgabe

- `out/feueralarm_teil2_tiktok.mp4` (nicht im Repo), `out/titelbild.png`
- `out/beschreibung.txt`, `out/kommentar.txt` (angepinnter Kommentar mit der Abstimmung für Teil 3)

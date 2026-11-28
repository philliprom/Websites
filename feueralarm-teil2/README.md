# DER FEUERALARM · TEIL 2

Folge im Format „Unbekannte Nummer“ (Skill `unbekannte-nummer`). Fortsetzung von `feueralarm-teil1/`.
Die Zuschauer haben in den Kommentaren **AUTO** gewählt (der Nummer glauben).

## Geschichte (66 s inkl. 4 s Endkarte), Fassung 2

1. **Start mitten in der Flucht:** Noah stürmt aus der Kellertür in den Regen. Das blaue Auto steht da, gibt Lichthupe,
   der Fahrer (Sonnenbrille, Bart) wartet an der offenen Hintertür. Regel 5 in Papas Stimme: „Hinterhof. Blaues Auto.“
   Darunter „TEIL 2 · Ihr habt gewählt: AUTO“.
2. Noah dreht sich um: Pohl brüllt aus der Tür „Das ist eine Falle!“, Ben stürmt hinterher.
3. **Am Auto (ab Sekunde 6):** „Dein Vater schickt mich. Steig ein.“ – Ben: „Woher kennt der Typ deinen Namen?“ –
   Sander reißt die Tür auf: „Bleib stehen!“ – „Los, rein da!“
4. **Im Auto:** Türen knallen, Zentralverriegelung, Reifen quietschen. „Anschnallen. Und Kopf runter.“
5. **Regel 6 (Papa):** „Falsches Auto. Ich warte hinter der Turnhalle. Steig AUS.“ – Noah: „Die Tür geht nicht auf!“
6. **Wendung:** Das Handy des Fahrers klingelt: **SANDER**. Er nimmt ab: „Ja. Ich hab beide. Wir sind gleich da.“ –
   Ben: „Der arbeitet für Sander!“
7. **Regel 7 (Papa):** „An der Ampel. Fenster hinten rechts geht auf. Raus, wenn es grün wird.“
8. Rote Ampel. „Finger weg vom Fenster, Noah.“ – dann fährt die Scheibe **von selbst** herunter, der Fahrer fährt herum.
   Ben: „Noah… was machen wir?“ – die Ampel springt auf Rot-Gelb. Endkarte: **FENSTER** oder **SITZEN BLEIBEN**.

Fassung 2 nach Rückmeldung: Anfang war zu ruhig (Handy im Keller), der Weg zum Auto zog sich (ca. 15 s), der Fahrer
stand im Auto (Figur innerhalb der Karosserie). Jetzt: Start in Bewegung, Auto 8 m statt 13 m entfernt, Fahrer steht
außerhalb neben der offenen Tür, drei Zeilen gestrichen, drei spannendere neu (verriegelte Tür, Telefonat, Fenster).

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

- 1080×1920, 66,0 s, −14,7 LUFS, Spitze −0,7 dBTP (Limiter nach loudnorm, sonst Übersteuerung am Anfang)
- Aussprache im Endmix (`aussprache_endmix.py`): 19 von 20 Zeilen exakt; die eine Abweichung ist nur die Schreibweise
  („dahinten“ statt „da hinten“), gesprochen identisch
- Stimme überall ≥ 12 dB über Hintergrund (knappste Zeilen: r5 12,4 dB, k18/k19 12,5 dB)
- Kontaktbogen alle 3 s geprüft: Banner, Hinweis „Ihr habt gewählt“, Untertitel, Regen nur im Hof, Endkarte

## Ausgabe

- `out/feueralarm_teil2_tiktok.mp4` (nicht im Repo), `out/titelbild.png`
- `out/beschreibung.txt`, `out/kommentar.txt` (angepinnter Kommentar mit der Abstimmung für Teil 3)

# FC Kuhweide – Tag 2: Der Kader

Folge 2 der Serie (siehe [`../fc-kuhweide-serie/README.md`](../fc-kuhweide-serie/README.md)). Neue Fassung nach dem Vergleich mit
FC Asche, FC Kaiser 09 und Rekrut Schulz (ca. 49 s: dicht erzählt, aber mit Lesepausen für die Kommentare, Ultra-Block und Taktiktafel):

1. Haken: „Gestern: 0 Fans. Heute: X!“, die Bank füllt sich, Konfetti
2. Echte Kommentare fliegen als Karten ins Bild („X von euch wollen spielen“)
3. Kommentar wird umgesetzt: Luca wollte ein Netz → gekauft (Kasse 500 → 411 €). Joel wollte Ultra werden → Ultra-Block
   mit Megafon und Trommel.
4. Flo will ins Tor, Berta weigert sich → Elfmeter-Test: der Neuner schießt, Berta hält aus Versehen
5. Taktiktafel mit dem Kader, Dauerkarte Nr. 001 für Julius
6. Abstimmung „BERTA oder FLO?“ und die Aufforderung, Kumpels zu markieren
7. Cliffhanger: „Morgen kommt Post. Vom größten Kreisligaverein der Welt.“

**Ausgabe:** `out/fc-kuhweide_tag2.mp4` · `out/titelbild.png` · `out/beschreibung.txt`

## Alles Veränderliche steht in `kader.json`

Fanzahl, Kasse und Netzpreis, Aufstellung (Position, Nummer, @-Namen, Duell/Duo), Staff/Ehrenrollen, Dauerkarte Nr. 001 und der
Torwart-Herausforderer. `make_script.py` erzeugt daraus `script.json` (Sprechertext mit den Zahlen) und `kader.js` (Daten für die
Taktiktafel im Bild).

## Morgens vor dem Posten (ca. 30–45 min)

1. Kommentare von Tag 1 neu abrufen und Nachzügler, YG-Benutzername und offene Antworten (Lilly, Florian) in `kader.json` eintragen.
   Aktuelle Follower-Zahl als `fans` eintragen.
2. `python3 fc-kuhweide-tag2/make_script.py`
3. Stimme: `QA_WHISPER=<ziel>/models/whisper-medium HF_HUB_OFFLINE=1 <ziel>/vx/bin/python engine/build_timeline.py fc-kuhweide-tag2 <ziel>/models/VoxCPM2`.
   Nur Sätze mit geänderten Zahlen oder Namen werden neu gesprochen, der Rest kommt aus `tts_cache/`. Ist die Umgebung weg:
   `bash engine/setup_voxcpm.sh <ziel>`.
4. `python3 engine/audio.py fc-kuhweide-tag2` und `node engine/render.cjs fc-kuhweide-tag2`, danach mit ffmpeg zusammenführen
   (siehe [`../engine/README.md`](../engine/README.md)).
5. `node engine/render_cover.cjs fc-kuhweide-tag2` für das Titelbild. Texte stehen in `out/beschreibung.txt`.

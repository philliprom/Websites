# FC Kuhweide – Tag 2: Der Kader

Folge 2 der Serie (siehe [`../fc-kuhweide-serie/README.md`](../fc-kuhweide-serie/README.md)). Ziel: Die Leute aus den Tag-1-Kommentaren
landen auf der Taktiktafel. Dazu kommen das Torwart-Duell Berta gegen Flo und eine Aufforderung zum Teilen. Nach den Studio-Daten
von Tag 1 ist das Video kürzer (~30 s) und beginnt sofort mit dem Haken („15 von euch wollen bei uns spielen. Ist dein Name dabei?“).

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

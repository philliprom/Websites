# Nachtschicht – Teil 1 (interaktive Horror-Folge)

Erste Folge des Horror-Formats „Du entscheidest“ (Idee: Kanal @playmalo.com als Vorbild für das Format, Geschichte eigen).
Überwachungskamera-Look, Erzähler in der Du-Form (Thorsten-Klon, Variante A), Abstimmung A/B per Kommentar.

## Geschichte
Nachtschicht an einer Tankstelle an der Landstraße, 02:39 Uhr, Regen. Der Chef hat einen laminierten Zettel mit vier Regeln
dagelassen (1. ab 2 Uhr Tür zu, 2. flackert das Licht → Kamera 3, 3. steht jemand still im Regen → nicht ansprechen,
4. er klopft dreimal → niemals aufmachen), darunter mit rotem Stift „Egal, wer es sagt!“. Auf Kamera 3 steht eine Gestalt
zwischen Zapfsäulen und Laden im Regen, das Tankdach-Licht flackert, sie ist weg. Stromausfall im Laden – danach steht sie
mit der Hand an der Glastür und klopft dreimal. Dann schreibt der Chef: „Mach die Tür auf. Sofort.“ („Er friert.“)
**A: Aufmachen (Chef) · B: Nicht aufmachen (Regel 4).** Die Mehrheit entscheidet über Teil 2.

## Ablauf (Skripte, in dieser Reihenfolge)
1. `story.py` → `script.json` (21 Sätze, Pausen) und `out/beschreibung.txt`
2. `engine/build_timeline.py nachtschicht-teil1 <Qwen3-TTS-Base>` (qw-Umgebung) → `build/vo.wav`, `build/timeline.json`
3. `shots.py` → `build/shots.json` (Bildzahl + Ereignisse je Blender-Einstellung) und `build/edl.json` (Schnittliste)
4. `scene.py --shot r1|r2|r3 --frames all` und `--shot note` (bl-Umgebung, Blender 5.3/Cycles CPU, 432×768, 10 fps)
5. `node assets.cjs` → Handy-Sperrbildschirm, Nachrichten, Entscheidungskarten (Playwright)
6. `sound.py` (vx-Umgebung) → `build/mix.wav` (Sounddesign + Stimme mit Ducking)
7. `assemble.py` (vx-Umgebung) → `out/nachtschicht_teil1.mp4`; `assemble.py --cover` → `out/titelbild.png`;
   `assemble.py --stills 1,14` → Prüfbilder

## Einstellungen
SH0 Haken (CAM 01, Gestalt an der Tür, Titel) · SH1 Schwarz „02:39“ · SH2 CAM 01 leer · SH3 Zettel mit Zoom und
Textmarker, Zwischenschnitt auf CAM 03 bei Regel 3 · SH4 CAM 01 Flackern · SH5 CAM 03 Gestalt, digitaler Zoom, Flackern,
weg · SH6 CAM 01 Dippen, Stromausfall, Sprung, Klopfen · SH7 Handy · SH8 Entscheidung (Karten A/B), Schlussklopfen,
„TEIL 2 FOLGT“.

## Schriften (`fonts/`)
Special Elite (Schreibmaschine, Apache 2.0), Permanent Marker (Filzstift, Apache 2.0), Oswald (Untertitel, OFL),
von npm (@fontsource) geladen und mit fontTools nach TTF umgewandelt.

## Ergebnis (24.11.2026, 20:05)
- `out/nachtschicht_teil1_tiktok.mp4` (66,4 s, 45 MB, 5,5 Mbit/s, −14,7 LUFS) – zum Hochladen.
  `out/nachtschicht_teil1.mp4` ist die Fassung mit hoher Bitrate (100 MB). Beide nicht im Repository (GitHub-Grenze),
  neu erzeugen mit `assemble.py` (ca. 6 min) bzw. ffmpeg (crf 23, maxrate 6M).
- `out/titelbild.png`, `out/beschreibung.txt` (Caption, angepinnter Kommentar, Kanal-Vorschlag).
- Rechenzeit Blender: r2 17 s/Bild (90 Bilder), r3 20 s/Bild (71), r1 20 s/Bild (113), Zettel ca. 3 min.
  Mit `use_persistent_data` bleibt die Szene zwischen den Bildern im Speicher – fast 3× schneller als im Test.
- Stimme: 21 Sätze, Ähnlichkeit 0,963–0,989, Tonhöhe 109–127 Hz (Referenz 120), je Satz lautheitsangeglichen.
- Nachbesserungen nach dem ersten Schnitt: Stromausfall im Schnitt verstärkt (Bild ×0,33 + Rauschen, wie eine
  nachregelnde Kamera), Entscheidungskarten kleiner und tiefer (Gestalt an der Tür bleibt sichtbar), Zettel mit
  weniger Tiefenunschärfe (Blende 6) gerendert, Rauschen etwas schwächer, Bitrate begrenzt.

## Ideen für Teil 2
- A (aufmachen): Tür öffnet sich, Gestalt ist weg – auf dem Boden eine nasse Spur bis zum Lager; das Handy vibriert:
  „Wer hat dir gesagt, dass du aufmachen sollst? – Chef“ (der Chef hat nie geschrieben).
- B (nicht aufmachen): Klopfen hört auf, Kamera 2 (Lager) zeigt eine offene Hintertür … Regel 5 auf der Rückseite des Zettels.

## Neue Fassung (25.11.2026): Horror-Erzähler
Kanalinhaber: Thorsten A klingt zu fröhlich. Vier Proben (`stimmproben/horror/`), gewählt **Stimme 3 „tief, langsam“**
(Qwen3-TTS VoiceDesign), Wunsch: „ein ganz kleines bisschen flüstern, weniger lange Pausen“.
- Referenz `voice/horror.wav`: Entwurf 3 mit gekürzten Pausen (15,3 → 11,8 s), Klon mit dem Base-Modell, `max_pause` 0,32.
- 21 Sätze: Ähnlichkeit 0,974–0,991, Tonhöhe 84–101 Hz (Referenz 96), keine Aussprachefehler.
- Im Mix (`sound.py`): leichter Flüster-Hauch (Rauschen 1,8–7,5 kHz mit der Hüllkurve der Stimme, −15 dB), Bass
  +2,5 dB, Präsenz −1,5 dB, kurzer dunkler Raum.
- Folge jetzt **79,6 s** (langsamere Stimme). Neue Zeitplanung, aber nur geänderte Bilder neu gerendert (`reuse.py`:
  147 von 314 Bildern behalten, 167 neu, ca. 50 min).
- Zusätzlich zweiter Zwischenschnitt im Zettel-Teil: bei „Er klopft dreimal“ die leere Eingangstür (CAM 01) mit leisem
  dreimaligem Klopfen.
- `out/nachtschicht_teil1_tiktok.mp4`: 79,6 s, 55 MB, −13,9 LUFS.

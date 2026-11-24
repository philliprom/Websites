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

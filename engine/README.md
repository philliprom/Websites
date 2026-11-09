# Engine für die „Tag 1“-Videos

Gemeinsame Bausteine für `mondmission-tag1/` und `fc-kuhweide-tag1/`. `fietland-tag1/` ist eigenständig und nutzt die
gleiche Technik in einer früheren, nicht ausgelagerten Fassung.

| Datei | Aufgabe |
|---|---|
| `engine.js` | Kamera, Untertitel, Figuren-Rig (Arme, Augen, Mund mit Lippensync), UI-Bausteine (Chips, Profil-Karte, Kommentar, Ticket, Kasse, Countdown, Abstimmungskarten), Konfetti und Glitzer |
| `engine.css` | Stil der UI-Bausteine, Farben per CSS-Variablen pro Projekt (`--badge-bg`, `--banner-bg`, `--ticket-accent` …) |
| `build_timeline.py` | Sprachausgabe (Piper TTS) pro Satz. Erzeugt `build/vo.wav`, `timeline.json` und die Hüllkurve für die Mundbewegung. Effekt-Cues: Zahl = Sekunden ab Satzanfang, `"e-0.3"` = 0,3 s vor Satzende. |
| `audio.py` | Synthetische Musik (Preset im `music`-Block der `script.json`: `bpm`, `inst` = marimba/vibes/pluck, Akkorde) und Soundeffekte, Mix mit Ducking auf −14 LUFS |
| `render.cjs` | rendert mit Chromium/Playwright Frame für Frame zu H.264 |

Ein Projekt besteht aus `script.json` (Text, Untertitel, Cues, Musik), `index.html` (Theme-Farben) und `scene.js`
(Welt-Grafik, Figuren, eine Funktion pro Schnitt).

```bash
cd engine && npm install && cd ..
pip install piper-tts numpy
P=mondmission-tag1
python3 engine/build_timeline.py $P <pfad>/de_DE-thorsten-high.onnx
python3 engine/audio.py $P
node engine/render.cjs $P                 # oder: --sheet / --stills 1.5,10
ffmpeg -i $P/build/video_noaudio.mp4 -i $P/build/mix.wav -c:v libx264 -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart $P/out/video.mp4
```

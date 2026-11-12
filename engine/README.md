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

## Stimmen

Zwei Sprach-Engines sind eingebaut. Welche genutzt wird, steht in `script.json` unter `tts`:

| Engine | Klang | Lizenz | Einsatz |
|---|---|---|---|
| **VoxCPM2** (`"tts": {"engine": "voxcpm", ...}`) | sehr natürlich, 48 kHz, Stimm-Design und Klonen | Apache-2.0 (kommerziell nutzbar) | FC Kuhweide |
| Piper „Thorsten“ (Standard ohne `tts`-Block) | robuster, aber hörbar synthetisch | Stimme CC0 | Fietland, Mondmission |

VoxCPM2 ist eine der Engines, die auch [VoiceStudio](https://github.com/debpalash/VoiceStudio) anbietet. Die dortige Standard-Engine
OmniVoice wird hier bewusst nicht genutzt, weil ihre Gewichte nur nicht-kommerziell lizenziert sind (CC-BY-NC).

**So bleibt die Stimme in jeder Folge gleich:** Die Figur bekommt einmalig eine Referenzaufnahme (`voice/kalle_ref.wav` und
`voice/kalle_ref.txt`), die per Stimm-Design entworfen wurde (`engine/voxcpm_tts.py design …`). Jede Folge klont dann genau
diese Referenz. Erzeugt wird jeweils ein ganzer Satz am Stück, damit die Betonung natürlich bleibt. Danach schneidet das Skript
den Satz über Whisper-Wort-Zeitstempel in die Bild-Segmente. Jeder Satz wird per Whisper zurückgehört. Weicht er vom Skript ab
(Wortfehlerrate > 8 %), wird er neu erzeugt. Das Protokoll steht in `build/tts_qa.txt`.

```bash
python -m venv vx && vx/bin/pip install "voxcpm>=2.0.3" soundfile faster-whisper
# Modelle: openbmb/VoxCPM2 (~5 GB), Systran/faster-whisper-small (~0,5 GB) von Hugging Face
QA_WHISPER=<pfad>/whisper-small vx/bin/python engine/build_timeline.py fc-kuhweide-tag1 <pfad>/VoxCPM2
```
Auf einer CPU mit 4 Kernen dauert ein 45-Sekunden-Video etwa 20 Minuten Sprachsynthese, mit GPU wenige Sekunden.

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

## Neuere Bausteine (Stand 12.11.2026, FC Kuhweide Tag 4)

| Datei / Option | Zweck |
|---|---|
| `setup_voxcpm.sh <ziel>` | Sprachumgebung in neuem Container aufsetzen. Platzbedarf ca. 14 GB (venv 7,3 GB, VoxCPM2 4,7 GB, Whisper medium 1,5 GB, small 0,5 GB). |
| `provisional_timeline.py <projekt>` | Vorläufige Zeitleiste ohne Stimme, um Standbilder zu prüfen, während die Stimme noch läuft |
| `render_cover.cjs <projekt>` | Titelbild aus `shots.cover` + `<projekt>/cover.html` → `out/titelbild.png` |
| `render_avatar.cjs <projekt> <variante>` | Profilbild aus `<projekt>/avatar.js` (Beispiel: `fc-kuhweide-tag1/avatar.js`) |
| `tiktok.py profil <nutzer>` / `tiktok.py kommentare <nutzer> <video_id>` | Kanal-Zahlen und Kommentare ohne Login (Grenzen im Dateikopf) |
| `Engine.start({ whip: true \| { skip: ['s09'] } })` | Wisch-Übergang bei jedem Schnitt, für einzelne Schnitte abschaltbar |
| `Engine.start({ punch: 0.07 })` | kurzer Zoom-Stoß bei jedem Schnitt |
| `Engine.start({ karaoke: true })` | Untertitel Wort für Wort (noch nicht gesprochene Wörter blass) |
| `S.noCap = true` (im Schnitt) | Untertitel für Zwischentitel ausblenden |
| Effekt-Marken `mstop` / `mgo` | Musik an dieser Stelle aus- bzw. wieder einblenden (kein Klang) |

**Klänge in `sfx`:** pop whoosh ding title stamp confetti sparkle splash waves flap squawk gulp poof riser pins horn squeak tap
blip tick card kaching hearts bark moo whistle rocket boing kick_ball coo cheer beep bigbeep crunch crickets drum sting scratch

**Sprachausgabe (VoxCPM2):** Jeder Satz liegt danach im Satz-Cache `<projekt>/tts_cache/` (mit einchecken). Das Modell wird nur
geladen, wenn ein Satz neu gesprochen werden muss. Großgeschriebene Wörter („BERTA“) buchstabiert die Stimme: im `say` normal
schreiben, nur in `caps` groß. Bindestrich-Wörter, die Whisper getrennt schreibt („Metzger Manni“), werden für die Schnittpunkte
trotzdem gefunden. Zahlen im `say` ausschreiben. Abweichungen wie „Mike“ statt „Maik“ oder „12“ statt „zwölf“ in `build/tts_qa.txt`
sind nur Schreibweisen der Spracherkennung.

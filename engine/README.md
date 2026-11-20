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
blip tick card kaching hearts bark moo whistle rocket boing kick_ball coo cheer beep bigbeep crunch crickets drum sting scratch klong brush

**Sprachausgabe (VoxCPM2):** Jeder Satz liegt danach im Satz-Cache `<projekt>/tts_cache/` (mit einchecken). Das Modell wird nur
geladen, wenn ein Satz neu gesprochen werden muss. Großgeschriebene Wörter („BERTA“) buchstabiert die Stimme: im `say` normal
schreiben, nur in `caps` groß. Bindestrich-Wörter, die Whisper getrennt schreibt („Metzger Manni“), werden für die Schnittpunkte
trotzdem gefunden. Zahlen im `say` ausschreiben. Abweichungen wie „Mike“ statt „Maik“ oder „12“ statt „zwölf“ in `build/tts_qa.txt`
sind nur Schreibweisen der Spracherkennung.

## Qwen3-TTS (Stand 15.11.2026, Omas Mondmission)

Natürlicher klingende Stimmen als VoxCPM2-Stimmentwürfe. Qwen3-TTS ist eine der Engines aus VoiceStudio, Lizenz Apache-2.0,
kann Deutsch. Zwei Modelle: **VoiceDesign** (Stimme aus einer Beschreibung entwerfen) und **Base** (Stimme klonen, damit die
Figur in jedem Satz gleich klingt). Die Standard-Engine von VoiceStudio (OmniVoice) ist nur nicht-kommerziell freigegeben.

```bash
# eigene Umgebung, nutzt torch und faster-whisper aus der VoxCPM-Umgebung vx mit (qwen-tts braucht transformers 4.57)
python3 -m venv qw && echo "$(vx/bin/python -c 'import site;print(site.getsitepackages()[0])')" > "$(qw/bin/python -c 'import site;print(site.getsitepackages()[0])')/zz_vx_torch.pth"
qw/bin/pip install qwen-tts
# Download ohne Xet-Protokoll: der Xet-Server (cas-server.xethub.hf.co) ist in der Umgebung gesperrt, normales HTTP geht
HF_HUB_DISABLE_XET=1 qw/bin/python -c "from huggingface_hub import snapshot_download as d; d('Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign', local_dir='models/Qwen3-TTS-VoiceDesign')"
# Stimmen entwerfen (mit Whisper-Prüfung)
QA_WHISPER=models/whisper-medium qw/bin/python engine/qwen3_engine.py design models/Qwen3-TTS-VoiceDesign <ausgabe> "<Beschreibung>||<Beschreibung>" "<Text>"
```

Vertonung: in `script.json` `"tts": {"engine": "qwen", "voice": "voice/<ref>.wav", "voice_text": "voice/<ref>.txt"}` und
`build_timeline.py` mit `qw/bin/python` und dem **Base**-Modell als letztem Argument starten. Satz-Cache und Whisper-Prüfung wie bei VoxCPM2.

### Option `max_pause` (18.11.2026)
`"tts": {"max_pause": 0.45}` kürzt lange Atempausen innerhalb eines Satzes auf höchstens 0,45 s (Cache bleibt roh,
Wortzeiten werden danach neu per Whisper bestimmt). Standardmäßig aus.

### Einzelnen Satz neu aufnehmen: `take`, `candidates`, `pitch_tol` (20.11.2026)
Klingt ein Satz anders als die übrigen (andere Stimmfarbe, zu hoch oder zu tief), nur diesen Satz neu erzeugen, im Segment:
`"take": 1, "candidates": 10, "pitch_tol": 0.06`. `take` gibt dem Satz einen eigenen Cache-Eintrag und andere Zufallswerte
(die anderen Sätze kommen weiter aus dem Cache), `candidates` überschreibt die Zahl der Fassungen, `pitch_tol` die erlaubte
Tonhöhen-Abweichung von der Referenz in Oktaven, bevor Strafpunkte anfallen (Standard 0,15 ≈ ±11 %, 0,06 ≈ ±4 %).
Im Log stehen je Fassung Ähnlichkeit und F0. Gute Werte für Oma: Ähnlichkeit ≥ 0,975, F0 235–270 Hz (Referenz 252 Hz).

## Sichere Zonen für TikTok (18.11.2026)

TikTok legt eigene Oberfläche über das Video (Screenshot des Kanalinhabers vom Döner-Video): oben Suche/Tabs, rechts die
Knöpfe (Profilbild, Like, Kommentar, Speichern, Teilen), unten Name und Beschreibung. Text dort ist teilweise verdeckt.
Zonen (1080×1920): **oben bis y 260**, **rechts ab x 920 zwischen y 800 und 1700**, **unten ab y 1660**.

- Prüfen vor jedem Rendern: `node engine/safe_check.cjs <projekt>` (alle 0,5 s, listet Text in den Zonen, Exit-Code 1 bei
  Verstößen). Mit `--bild 1.0,5.0` entstehen Standbilder mit eingezeichneten Zonen (`build/safe_<t>.png`).
  „Hinweis … Kulisse“ betrifft Schrift in der gezeichneten Szene (z. B. Aufschrift auf der Rakete) und ist meist egal.
- Engine-Untertitel sind jetzt höchstens 740 px breit (`capWidth` in `Engine.start` änderbar). Dabei behoben: Die
  Schriftgröße wurde per Attribut gesetzt und von der CSS-Regel `#caps text` überstimmt, zu lange Untertitel wurden also nie
  verkleinert. Jetzt per `style.fontSize`.
- Gilt ab 18.11. für neue Videos. Die schon fertigen Videos (Tech-Lupe 1–4, Döner, Oma Tag 3) bleiben bewusst wie
  verschickt (Wunsch des Kanalinhabers: „nur für die Zukunft merken“); ihre `scene.js` sind schon angepasst und würden
  beim nächsten Neubau sicher.
- Engine-Elemente tiefer gesetzt: `#badge` 290 px, `.chip` mindestens 300 px, `#banner`/`#kasse` 300 px, `.card` 300 px,
  `#votePill` 720 px. Herzchen fliegen nicht mehr in die untere Ecke.

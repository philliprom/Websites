# Produktion: vom Skript zum fertigen Video

Pfade: `F` = Folgenordner (mit `scripts/neue_folge.py` angelegt), `Z` = Umgebungsordner aus `scripts/setup.sh`
(Blender `Z/bl`, Ton/Whisper `Z/vx`, Qwen `Z/qw`, Modelle `Z/models`). Blender immer mit `EGL_PLATFORM=surfaceless`.

## Inhalt
1. Dateien im Folgenordner und was je Folge anzupassen ist
2. Ablauf mit Befehlen
3. Einstellungen schreiben (`shots.py`)
4. Rendern
5. Ton und Schnitt
6. Prüfen und abliefern
7. Stolperfallen (schon gelöst, nicht wieder einbauen)

## 1. Dateien

| Datei | Inhalt | Je Folge anpassen? |
|---|---|---|
| `story.py` | `TITLE`, `PART`, `VOICES` (Figur → Stimmbeschreibung), `LINES` (id, who, sub, say, rot, emo, kind regel/zeile/durchsage, n), `ENDKARTE` | **immer** |
| `cast.py` | Aussehen der Figuren (Ben, Lina, Sander, Pohl, Mitschüler), POV-Hand mit Handy | neue Figuren ergänzen |
| `figur.py` | Figurenbaukasten (Kopf, Augen, Frisuren: kurz, stachel, lang, zopf, locken, dutt, bob, grau; Kleidung: hoodie, jacke, blazer, arbeit) | selten |
| `set_klasse.py`, `set_flur.py`, `tex.py` | Sets (Klassenzimmer + Schulhof, Flur, Keller) und deren Texturen (Tafel, Uhr, Schilder) | neue Orte als neue `set_*.py` |
| `build_base.py` | baut je Set eine `.blend` (Raum + eingefrorene Mitschüler zu einer Mesh, Hauptfiguren je Gelenk) | Set-Liste und welche Figuren je Set |
| `shots.py` | alle Einstellungen: Kamera, Figuren, Blicke, Gesten, Sprechen, Handy | **immer** |
| `render_shot.py` | rendert Einstellungen (`liste`, `alle`, `<id,id>`, `test`, `standbild`), Farbe/Licht je Set (`SETLOOK`) | `SETLOOK` für neue Sets |
| `anim.py` | Figuren-Animation (Blick, Lippen, Blinzeln, Gesten `ARM`, Brauen `BRAUE`, Gehen) und POV-Kamera | neue Gesten |
| `voices.py`, `voices2.py`, `qwen3_engine.py`, `asr.py` | Stimmen (siehe `stimmen.md`) | `REFS` in `voices2.py` |
| `timeline.py` | Pausen vor jeder Zeile (`GAP`), Ereignisse (Vibration, Gong, Türen) | **immer** (`GAP`, Ereignisse) |
| `phone.py` | Sperrbildschirm-Texturen mit Regel-Mitteilungen (`TIMES` = Uhrzeiten) | Uhrzeiten |
| `sound.py` | Ton: Stimmen je Ort, Alarm, Ereignisse, Musik-Akzente, Herzschlag | **immer** (Ereignis-Abschnitt) |
| `assemble.py` | Schnitt: Hochskalieren, Farbe je Set (`grade`), Untertitel, Banner, Endkarte | Farbe neuer Sets |
| `make_cover.py`, `make_matcap.py` | Titelbild, Toon-Lichtkugel | nein |

## 2. Ablauf mit Befehlen

```bash
cd F
python3 tex.py && python3 phone.py && python3 make_matcap.py
# Stimmen (Hintergrund, ~1 h; siehe stimmen.md)
QWEN_DTYPE=bf16 QA_WHISPER=Z/models/whisper-medium Z/qw/bin/python voices.py gen Z/models/Qwen3-TTS-VoiceDesign 2
Z/qw/bin/python voices2.py refs            # vorher REFS anpassen
QWEN_DTYPE=bf16 Z/qw/bin/python voices2.py klon Z/models/Qwen3-TTS-Base 2
QWEN_DTYPE=bf16 Z/qw/bin/python voices2.py wahl Z/models/Qwen3-TTS-Base Z/models/whisper-medium
QA_WHISPER=Z/models/whisper-medium Z/qw/bin/python timeline.py
# Szenen
EGL_PLATFORM=surfaceless Z/bl/bin/python build_base.py klasse <base>/klasse.blend   # je Set
EGL_PLATFORM=surfaceless Z/bl/bin/python render_shot.py liste <base> <frames>        # schreibt build/shots.json
EGL_PLATFORM=surfaceless Z/bl/bin/python render_shot.py alle <base> <test> test      # 3 Bilder je Einstellung, halbe Größe
# Vollrendern (2 Prozesse, je 2 Threads; ~1 Bild/s gesamt)
LP_NUM_THREADS=2 EGL_PLATFORM=surfaceless nohup Z/bl/bin/python render_shot.py <ids_a> <base> <frames> &
LP_NUM_THREADS=2 EGL_PLATFORM=surfaceless nohup Z/bl/bin/python render_shot.py <ids_b> <base> <frames> &
# Ton, Schnitt, Titelbild
Z/vx/bin/python sound.py
python3 assemble.py <frames>                     # ~15 min; Probe: python3 assemble.py <frames> teil 6
EGL_PLATFORM=surfaceless Z/bl/bin/python render_shot.py standbild <shot>:<sekunde> <base> <bild.png>
python3 make_cover.py <bild.png>
```

Die Stimmen laufen auf der CPU und blockieren die Kerne. Währenddessen nur leichte Arbeit erledigen (Sets bauen,
Testbilder mit `nice -n 10`). Die beiden Renderprozesse teilt man nach Länge auf: längste Einstellung zuerst, immer
dem Prozess mit weniger Gesamtzeit zuteilen.

## 3. Einstellungen schreiben (`shots.py`)

Jede Einstellung ist eine Funktion mit `@shot(id, set, start)`. Der Start ist ein Ausdruck über die Zeitleiste:
`c.S('l05')` = Beginn, `c.E('l05')` = Ende einer Zeile. Das Ende einer Einstellung ist der Start der nächsten.

```python
@shot("07_sander_kommt", "klasse", lambda c: c.S("l07") - 0.25)
def s07(c):
    sander = c.a["Sander"]                         # Figuren aus der Grund-Szene
    sander.place((-0.9, 4.1, 0), heading((-0.9, 4.1, 0), NOAH))
    sander.move(c.t0, c.t0 + 2.3, (-1.48, 1.15, 0), walk=True, rot=...)
    sander.look(c.t0, "cam", 0.01)                 # Weltpunkt, "cam" oder None
    sander.brow(c.t0, "skeptisch", 0.3)            # neutral, boese, sorge, schreck, skeptisch
    sander.arm(c.t0, "beide", "verschraenkt", 0.4) # Gesten in anim.ARM
    sander.say(c.S("l07"), c.env("l07"))           # Lippen nach Lautstärke
    c.pov.at(c.t0, pos=NOAH, target=(-1.0, 3.6, 1.6), dur=0.01, lens=18)
    c.phone(None, lower_at=c.t0)                   # Handy: state "r1".."r5", raise_at, lower_at, low
```

Figuren schauen lokal nach −Y. `heading(von, nach)` liefert den Drehwinkel. Arme: Euler ZXY (drehen, heben, abspreizen),
neue Posen in `anim.ARM` erst numerisch prüfen (Handposition ausgeben), dann rendern.
Nicht platzierte Figuren werden automatisch weggeräumt. Requisiten: `c.list_prop = True` (Liste in Sanders Hand),
`c.phone_prop = "Sander"` (Handy am Ohr).

Vor dem Vollrendern **immer** `render_shot.py alle … test` und den Kontaktbogen ansehen: Ist die sprechende Figur zu sehen?
Verdeckt jemand die Sicht? Ist der Täter groß genug?

## 4. Rendern

- Blender Workbench (Matcap-Toon, Konturen per Geometry Nodes, Schatten). EEVEE läuft auf Mesa nicht sauber.
- 720×1280, FXAA, JPEG 95; `assemble.py` skaliert auf 1080×1920 (das Vorbild war selbst nur 576×1024).
- Grund-Szenen einmal bauen (`build_base.py`): Raum und Mitschüler werden zu einer Mesh verschmolzen, das spart den Großteil
  der Renderzeit (7–9 s → ~1,9 s je Bild). Hauptfiguren bleiben je Gelenk getrennt.
- Bei einem Neustart des Containers laufen Hintergrundprozesse nicht weiter: Fortschritt prüfen und neu starten
  (`voices2.py klon` überspringt Vorhandenes, beim Rendern nur fehlende Einstellungen neu).

## 5. Ton und Schnitt

- `sound.py`: Abschnitt „Ereignisse“ an die Folge anpassen (Schlüssel, Schritte mit Zeiten aus `build/shots.json`,
  Türen, Rennen, Akzente bei Wendungen). Die Seitenketten-Absenkung hält den Hintergrund ≥ 12 dB unter der Stimme;
  danach ausgeben lassen, welche Zeilen am knappsten sind.
- Lautheit: `assemble.py` normalisiert auf −14 LUFS (TikTok).
- Nur Ton geändert? Nicht neu schneiden, nur neu verbinden:
  `ffmpeg -i build/video_ohne_ton.mp4 -i build/mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy -c:a aac -b:a 192k -shortest out/<name>.mp4`

## 6. Prüfen und abliefern

1. Kontaktbogen alle 3 s (`scripts/kontaktbogen.sh`): Banner, Untertitel, Hand, Ende.
2. Lautheit (`ffmpeg … -af ebur128`): etwa −14 LUFS, Spitze ≤ −1 dBFS.
3. `scripts/aussprache_endmix.py`: jede Zeile im Endmix.
4. Abliefern: Video (SendUserFile), `out/titelbild.png`, `out/beschreibung.txt`, `out/kommentar.txt`, README der Folge.
   Commit und Push, das Video selbst nicht ins Repo (zu groß).

## 7. Stolperfallen (gelöst, nicht wieder einbauen)

- `look_at` braucht vorher `view_layer.update()`, sonst zielt die Kamera vom Ursprung aus.
- Meshes per eigenem bmesh-Code zusammenführen → Depsgraph-Absturz. Blender-Befehle `object.convert` + `object.join`
  verwenden (`toon.merge_children`).
- Beim Verbinden gehen UVs verloren: texturierte Flächen (Tafel, Uhr, Schilder, Handy-Bildschirm) bleiben einzeln.
- Nach `open_mainfile` ist das zwischengespeicherte Kontur-Material ungültig (`toon.black()` fängt das ab).
- Schulter-Euler XYZ ließ verschränkte Arme nach außen zeigen → ZXY.
- Sichtlinie zur Tür war durch sitzende Schüler verdeckt → Plätze in `FREI`.
- Alte Handhaltung (zwei Fäustlinge über dem Bildschirm) sah seltsam aus → eine Hand, Bildschirm frei.
- Kamera-Schwenk über Pohls Bauch wirkte wirr → harter Schnitt aufs Gesicht.
- Toon-Figuren haben große Köpfe: Im Auto ragten Fahrer und Ben durchs Dach. Kopfhöhen vor dem Rendern messen
  (Bounding Box der Kopf-Meshes) und Innenräume danach bauen (Auto: Himmel innen ≥ 1,7 m, Sitze tief).
- Dunkle Sitze + Fahrer in Schwarz = nicht lesbar → Innenraum hell (Sitze #77716a).
- Von der Rückbank sieht man den Fahrer nur von hinten → er dreht Kopf **und** Schultern (`look("cam")` + `bend((0, -32))`).
- Texturierte Flächen an beweglichen Teilen (Nummernschilder) brauchen `parent=` und müssen beim Verbinden in `keep`,
  sonst schweben sie am Ursprung bzw. werden weiß.
- Handy-Bildschirm eines anderen (z. B. Anruf „SANDER“) nur mit Teleobjektiv lesbar: Brennweite ~100 statt 30.
- Ampel von innen nicht sichtbar, wenn das Auto direkt an der Haltelinie steht → wartendes Auto davor, eigenes Auto
  hält ~12 m vor der Ampel, Noah duckt sich (Kamera tiefer).

## 8. Fortsetzungen (Teil 2, 3 …)

- Kommentare entscheiden: `scripts/tiktok_stats.py` liest nur öffentliche Zahlen. Die Kommentare selbst liest der
  Nutzer und nennt das Ergebnis (nicht über inoffizielle Schnittstellen abrufen).
- Rückblick ≤ 2,5 s (Regel-Banner der letzten Regel + Pille „TEIL n · Ihr habt gewählt: …“ unter dem Banner),
  dann sofort Bedrohung. Teil 1 hatte Ø 51 s Wiedergabe bei 130 s Länge → Teil 2 auf ~80 s gekürzt.
- Vorlage für Fahrzeuge und Außen-Sets: `feueralarm-teil2/` (`set_hof.py`: Hof, Straße, Auto mit Innenraum;
  `anim.py` `follow`; `render_shot.py` `car_y_fn`, `c.ampel`, `c.glas_aus`, `c.fahrerhandy`).
- Während die Stimmen laufen, mit einer **vorläufigen Zeitleiste** (geschätzte Zeilenlängen, Platzhalter-Hüllkurven)
  Testbilder aller Einstellungen rendern; die echte `timeline.py` überschreibt später alles.
- Cliffhanger-Einstellung nach der letzten Zeile (z. B. Ampel springt auf Rot-Gelb): `END_PAUSE` entsprechend verlängern.

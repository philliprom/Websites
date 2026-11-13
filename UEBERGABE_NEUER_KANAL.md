# Übergabe: Zweiter TikTok-Kanal im „1 Follower = 1 …“-Format

Stand: 12.11.2026. Diese Datei fasst alles zusammen, was ein neuer Chat braucht, um parallel zu **FC Kuhweide** einen zweiten
Kanal in derselben Nische aufzubauen: Format, Zahlen, Erkenntnisse, Regeln, Technik und Arbeitsablauf.

---

## 0. So startest du den neuen Chat

1. **Repo:** `philliprom/Websites`. **Alles liegt auf dem Branch `claude/gracious-hamilton-5kohce`.** Der Standard-Branch `techlab`
   enthält nur das Techlab-Projekt, dort fehlen Engine und alle Vorlagen. Der neue Chat setzt seinen Arbeitsbranch deshalb darauf auf:
   ```bash
   git fetch origin claude/gracious-hamilton-5kohce
   git checkout -B <arbeitsbranch-des-neuen-chats> origin/claude/gracious-hamilton-5kohce
   ```
2. **Cloud-Umgebung „TikTok-Recherche“** wählen. Nur dort sind TikTok-Seiten und Hugging Face (Sprachmodelle) erreichbar.
3. **Erste Nachricht (Vorschlag zum Kopieren):**
   > Lies bitte `UEBERGABE_NEUER_KANAL.md` im Repo (Branch `claude/gracious-hamilton-5kohce`) und arbeite danach. Wir bauen einen
   > zweiten Kanal in derselben Nische wie FC Kuhweide. Richte zuerst die Technik ein und schlag mir dann 3 Konzepte vor.
4. **Nicht anfassen:** die Ordner `fc-kuhweide-*` (laufender Kanal, eigener Chat) und `techlab/` (anderes Projekt). Die Engine
   (`engine/`) wird geteilt, Änderungen dort nur rückwärtskompatibel (neue Optionen standardmäßig aus).

**Rollen:** Der Kanalinhaber postet selbst, antwortet selbst auf Kommentare und schickt Screenshots (Sticker-Kommentare, TikTok Studio).
Claude baut Videos, Titelbilder, Texte, Antwortvorschläge und wertet Zahlen aus. Claude loggt sich nie bei TikTok ein und nimmt
keine Zugangsdaten an, auch nicht im Chat.

---

## 1. Das Format (die Nische)

- **Ursprung:** viraler Trend „Tag 1: Ich habe eine Dönerbude eröffnet. 1 Follower = 1 Kunde. Ihr entscheidet.“ (@marlons.doenerbude_).
- **Mechanik:** Tag-Zähler („TAG 1“-Badge), jeder Follower wird Teil der Geschichte (Fan, Kunde, Einwohner …), die Community
  entscheidet per Kommentar, echte Kommentare werden sichtbar umgesetzt, Fortschritt in Zahlen, tägliche Folgen.
- **Unser Unterschied:** Bei uns stehen echte Kommentierende mit @-Namen im Bild (Kader, Rollen, Stempel). Andere Kanäle erfinden
  ihre Figuren.

### Vorbilder (Stand 09.11.)

| Kanal | Zahlen | Was wir daraus gelernt haben |
|---|---|---|
| **FC Asche** (@asche348) | seit 01.11., 57.000 Follower; Tag 1–3 je ca. 300.000 Aufrufe, ab Tag 6 deutlich weniger (Tag 7: 63.000) | Fast dasselbe Konzept wie FC Kuhweide. Figuren-Comedy (Opa im Tor), Kassenstand, Dauerkarte 001. Format nutzt sich ab. |
| **Rekrut Schulz** (@vyral696) | 10.500 Follower; erstes Konzept floppte nach 2 Videos, neues Konzept sofort 82.000 Aufrufe | Schnell wechseln ist normal. Ein-Wort-Aufruf („Schreib ‚Marke‘“). Bis zu 3 Videos am Tag. Steigerung mit Cliffhanger. |
| **FC Kaiser 09** (@fckaiser09) | 4.300 Follower, Spitze 58.000 Aufrufe | Ganze Spiele mit Anzeigetafel, Spielminute und Toren = Spannung. |

**Gemeinsam bei den erfolgreichen Videos:** Action mit Spannung, Kommentar → sichtbare Umsetzung, Fortschritt in Zahlen gleich zu
Beginn („Gestern 0 → heute 90“), viele Schauplätze, kurze Etiketten, dichte Erzählung. 2D oder 3D ist nicht entscheidend.

---

## 2. Was FC Kuhweide gezeigt hat (echte Zahlen)

Kanal @gruselwahl.de „FC Kuhweide“: Trainer Kalle, Torhüterin Kuh Berta, Taube als Running Gag. Follower: 35 → 45 → 75 → 101 (12.11.).

| Folge | Länge | Aufrufe | Ø Wiedergabe | Anteil | ganz angesehen | neue Follower |
|---|---|---|---|---|---|---|
| Tag 1 | 45 s | 1.553 | 8,5 s | 19 % | 3,9 % | 36 (nach 5 h) |
| Tag 2 | 57 s | 1.548 | 11,4 s | 20 % | 2,8 % | 34 |
| Tag 3 | 56 s | 1.042 | 14,1 s | 25 % | 5,6 % | 26 |

**Haltekurve Tag 2:** nach 1 s noch 72 %, nach 4 s ca. 37 %, nach 8 s ca. 24 %, danach flach (26 s: ca. 14 %).
**Herkunft:** 90 % „Für dich“, 89 % neue Zuschauer und Nicht-Follower, 2,3 % über Direktnachrichten (geteilt). 51 % Frauen.

**Folgerungen:**
1. **TikTok verteilt uns, aber die ersten 4 Sekunden entscheiden.** Fast zwei Drittel wischen weg, bevor die Geschichte anfängt.
2. Jedes Video wird ca. 1.000–1.500 Leuten gezeigt (Spitze in Stunde 1–3) und dann nicht weiter ausgespielt, weil im Schnitt nur
   20–25 % des Videos geschaut werden. Faustregel (keine offizielle Zahl): deutlich über 50 % nötig.
3. **Wer bleibt, wird Fan:** 2–3,6 % der Zuschauer folgen, über 20 echte Kommentare pro Folge. Das Konzept trägt.
4. Fast jeder Zuschauer sieht nur ein Video → jede Folge muss **ohne Vorwissen** funktionieren.
5. Die Ø-Wiedergabe liegt fast unabhängig von der Länge bei 11–14 s → **kurze Folgen** (≤ 30 s) kommen auf über 50 %.
6. Kommentare sind fast nur Rollen- und Positionswünsche. Abstimmungen bekommen wenige Stimmen (1–3 pro Option).

Ausführliches Gedächtnis von FC Kuhweide (Zusagen, Regeln, alle Auswertungen): `fc-kuhweide-serie/README.md`.

---

## 3. Regeln für jede Folge (Checkliste)

**Einstieg (wichtigster Teil)**
- [ ] Bild 0 ist sofort stark und ohne Vorwissen verständlich (Beispiel Tag 4: Plakat „VERMISST: BERTA“, das mit Stempel-Ton ins Bild knallt).
- [ ] Stimme beginnt bei 0,1 s, erster Satz nennt Konflikt oder Einsatz („Unsere Kuh ist weg. Und Samstag spielen wir um sie!“).
- [ ] Spätestens alle 1,5–3 s ein Schnitt oder ein neues Element.

**Aufbau**
- [ ] **Hauptfolge höchstens 30 s**, ein Erzählstrang. Namenslisten gehören ins zweite Video.
- [ ] **Zwei Videos pro Tag:** Hauptfolge gegen 12:00, „Neuzugänge“ (alle neuen Rollen mit Karte und Stempel) frühestens 4 h später.
- [ ] Echte Kommentare als Karte mit @-Namen + grüner Stempel „✓ ROLLE“. Wer eine Rolle bekommt, wird auch im Ton **genannt**.
- [ ] Lesepause: Karten im Abstand von ca. 0,4 s, letzte Karte ca. 1–2 s stehen lassen.
- [ ] Mitmachen mit niedriger Hürde: Ein-Wort-Aufruf („Schreibt BERTA“), Abstimmung mit genau 2 Optionen, „Markier deinen Kumpel“.
- [ ] Schluss: Ereignis im Bild + Bedrohung für eine beliebte Figur + Frage zum Mitraten, dann Abschlusskarte „TEIL X · MORGEN 12 UHR“
      mit Folgen-Knopf. Eine reine Ankündigung reicht nicht.

**Fairness und Sicherheit**
- [ ] Abstimmungen ehrlich zählen: eine Stimme pro Person, Selbststimmen zählen, Likes zählen nicht (der Kanal liked beim Antworten mit).
      Vor dem Auswerten Screenshots holen (Sticker-Kommentare und Antworten unter dem angepinnten Kommentar sind per Abruf unsichtbar).
- [ ] Was in Antworten zugesagt wird, kommt in die nächste Folge.
- [ ] Nur öffentliche @-Namen zeigen, keine Profilbilder, keine Klarnamen. Ungeprüfte Markennamen nicht ins Video.
- [ ] Familienfreundlich: Bedrohungen nur andeuten, Gefährliches nicht verherrlichen (Pyro-Wunsch → Wunderkerze).
- [ ] Konkurrenz nie im Video nennen, kein Spam unter fremden Videos.
- [ ] Kommentare: alle liken, aber nur wenige beantworten (Fragen, Top-Kommentar, Story-Potenzial, eine Sammelantwort für alle
      Bewerbungen). Die eigentliche Antwort ist der Auftritt im nächsten Video. Antworten immer etwas anders formulieren.
- [ ] **Wechselregel:** Zündet ein Konzept nach ca. 5 Folgen nicht (Ø-Wiedergabe unter 50 %, Aufrufe nicht über ca. 2.000), neues Konzept testen.

**Bildaufbau (1080 × 1920):** Unten ca. 350 px und rechts ca. 150 px verdeckt die TikTok-Oberfläche. Wichtiges zwischen y 200 und
1500 halten. Untertitel stehen bei y 1350–1480. Das „TAG X“-Badge sitzt oben links.

---

## 4. Tagesablauf

| Zeit | Wer | Was |
|---|---|---|
| morgens | Kanalinhaber | meldet sich, schickt Screenshots: Sticker-Kommentare, TikTok Studio (Übersicht, Haltekurve, Traffic-Quellen) |
| morgens | Claude | Kommentare abrufen (`engine/tiktok.py`), auswerten, Antworten-Datei schreiben, `kader.json` aktualisieren, beide Videos bauen (ca. 1–2 h) |
| 17–19 Uhr | Kanalinhaber | Hauptfolge posten (Titelbild, Caption, ersten Kommentar anpinnen), alle Kommentare liken, nur die wichtigsten beantworten (max. 5 min) |
| optional | Kanalinhaber | zweites Video (z. B. Neuzugänge) mindestens 4 h versetzt; bei FC Kuhweide brachte es mehr Follower als die Hauptfolge |
| abends | Kanalinhaber | Studio-Zahlen schicken; Claude plant daraus die nächste Folge |

**Pro Folge liefern:** `out/<name>.mp4`, `out/titelbild.png`, `out/beschreibung.txt` (Caption + angepinnter Kommentar + Postzeit),
`out/antworten_<vorfolge>.txt` (Antwortvorschläge). Alles committen, pushen und per Datei an den Kanalinhaber schicken.

---

## 5. Ideen für den neuen Kanal (Entscheidung beim Kanalinhaber)

**Was ein Konzept braucht** (aus FC Kuhweide gelernt):
- Eine sympathische Hauptfigur mit Stimme und ein **Tier-Sidekick** als Publikumsliebling (Berta-Effekt).
- Ein **messbares Ziel** mit sichtbarem Fortschritt (Fans, Meter, Einwohner).
- **Viele Rollen**, die Kommentierende bekommen können (wie Kader, Ultras, Trainerstab).
- Einen **Gegenspieler** für Spannung und Cliffhanger (wie SV Matschbach und Metzger-Manni).
- **Bewusst anders als Fußball**, damit sich die beiden Kanäle nicht gegenseitig Zuschauer wegnehmen.

**Schon vorhanden (je ein fertiges „Tag 1“, noch nach alten Regeln, 44–48 s, ältere Piper-Stimme):**
- `mondmission-tag1/` – **Omas Mondmission:** Oma Gisela (78) baut im Schrebergarten eine Rakete, Dackel Waldi ist Kopilot,
  1 Follower = 1 Meter höher. Rollen: Funker, Raketenbauer, Bodenkontrolle … Gegenspieler denkbar: Kleingartenvorstand.
- `fietland-tag1/` – **Fietland:** Fiete gründet auf einer Sandbank sein eigenes Land, Möwe Jürgen ist Finanzminister,
  1 Follower = 1 Einwohner. Rollen: Minister, Botschafter, Leuchtturmwärter … Gegenspieler denkbar: Nachbarinsel.

Weitere Richtungen zum Ausarbeiten: eigene Burg (1 Follower = 1 Untertan, Ritter/Hofnarr/Koch, Gans als Wachhund, Raubritter von
nebenan), Wanderzirkus (1 Follower = 1 Zuschauer, Clown/Dompteur, Alpaka, Konkurrenzzirkus). Vor dem Bauen 2–3 Konzepte als kurze
Steckbriefe vorschlagen und den Kanalinhaber wählen lassen.

**Kanal-Paket für den Start:** Name und @-Name (keine fremden Marken, keine echten Personen), Bio mit Mechanik und Ziel
(Vorbild: „Vom Bolzplatz ins Stadion – mit euch ⚽ 1 Follower = 1 Fan. Ihr entscheidet!“), Profilbild (`render_avatar.cjs`),
Tag 1 (≤ 30 s), Titelbild, Caption, angepinnter Kommentar, Serien-Gedächtnis `<kanal>-serie/README.md`.

---

## 6. Technik

### Ordner im Repo

| Ordner | Inhalt |
|---|---|
| `engine/` | gemeinsame Engine: Kamera, Figuren-Rig mit Lippensync, Untertitel, UI-Bausteine, Musik, Effekte, Render. Doku: `engine/README.md` |
| `fc-kuhweide-tag4/` | **beste Vorlage für eine Hauptfolge** (Plakat, Spielerkarte, Wegweiser, Anzeige „Heimweg“, Abschlusskarte) |
| `fc-kuhweide-tag4b/` | **Vorlage für das Neuzugänge-Video** (Kommentarkarten mit Stempel, Kommentarfeld, Werbebande) |
| `fc-kuhweide-tag1/` | Stimm-Referenz (`voice/`), Stimm-Kandidaten, Profilbild (`avatar.js`) |
| `fc-kuhweide-serie/README.md` | Gedächtnis von FC Kuhweide (Vorbild für `<kanal>-serie/README.md`) |
| `mondmission-tag1/`, `fietland-tag1/` | frühe Tag-1-Prototypen (siehe oben) |
| `techlab/` | anderes Projekt, nicht anfassen |

Neuer Kanal: eigene Ordner `<kanal>-serie/` (Gedächtnis) und `<kanal>-tag1/`, `<kanal>-tag2/` … (je Folge ein Ordner, durch Kopieren der
letzten Folge).

### Einrichtung (einmal pro Container)

```bash
cd engine && npm install && cd ..                 # Schriften Fredoka und Nunito (node_modules ist nicht eingecheckt)
bash engine/setup_voxcpm.sh <scratchpad>/tts      # Sprachmodelle, 20–40 min, ca. 14 GB
```
Playwright und Chromium sind im Container vorinstalliert (nicht neu installieren), ffmpeg ist vorhanden. Bei Platzmangel große
Zwischendateien (`build/`, Pip-Cache, `whisper-small`) löschen.

### Aufbau einer Folge

- `kader.json` – alles Veränderliche (Zahlen, Namen, Kommentare, Abstimmung).
- `make_script.py` – erzeugt daraus `script.json` (Sätze `say`, Untertitel `caps` mit `^` grün, `!` rot, `~` blau, Pausen `gap`,
  Effekte `sfx` mit Sekunden ab Satzanfang oder `"e-0.3"` = vor Satzende), `kader.js` und `out/beschreibung.txt`.
- `scene.js` – Welt und Figuren als SVG, eine Funktion pro Schnitt (`shots.s01 …`), dazu `shots.cover` fürs Titelbild.
  Zeitpunkte immer über `cue('s05', 'stamp')` an die Effekte koppeln, nie fest eintragen.
- `index.html` – Farben und Stile, `cover.html` – Texte fürs Titelbild.

### Bauen

```bash
P=<kanal>-tag1
python3 $P/make_script.py
python3 engine/provisional_timeline.py $P          # optional: Szenen schon prüfen, bevor die Stimme fertig ist
node engine/render.cjs $P --stills 0,2.5,6         # Standbilder in $P/build/stills/ – vor jedem Komplett-Render anschauen
QA_WHISPER=<tts>/models/whisper-medium HF_HUB_OFFLINE=1 <tts>/vx/bin/python engine/build_timeline.py $P <tts>/models/VoxCPM2
python3 engine/audio.py $P
node engine/render.cjs $P
ffmpeg -v error -y -i $P/build/video_noaudio.mp4 -i $P/build/mix.wav -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
  -profile:v high -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart $P/out/<name>.mp4
node engine/render_cover.cjs $P                    # Titelbild
```
Dauer auf der CPU: Stimme ca. 3 min Laden + ca. 1 min pro Satz (lange Läufe im Hintergrund starten), Render eines 30-s-Videos ca. 5–8 min.
Ziel-Lautheit −14 LUFS (macht `audio.py`), Format 1080 × 1920, 30 fps.

### Stimme für die neue Hauptfigur

1. Kandidaten entwerfen:
   `<tts>/vx/bin/python engine/voxcpm_tts.py design <tts>/models/VoxCPM2 <ordner> "<Beschreibung der Stimme>" "<Beispieltext>" 3`
   (mehrere Beschreibungen mit `||` trennen). Die Ausgabe zeigt Tonhöhe (F0) und Verständlichkeit (WER) je Kandidat.
2. Tonhöhe prüfen (Stimm-Design lieferte bei Männerstimmen anfangs zu hohe Stimmen), 3 Kandidaten als m4a an den Kanalinhaber
   schicken und auswählen lassen. Die Stimme soll sich klar von Kalle unterscheiden.
3. Gewählte Datei als `<kanal>-tag1/voice/<figur>_ref.wav`, den gesprochenen Text als `<figur>_ref.txt` ablegen und in
   `make_script.py` unter `tts.voice` / `tts.voice_text` eintragen. Jede Folge klont dann genau diese Referenz.

**Fallen bei der Sprachausgabe:** Großbuchstaben werden buchstabiert (im `say` „Berta“, nur in `caps` „BERTA“). Zahlen ausschreiben.
Ein Satz endet bei `.`, `!` oder `?`; Segmente ohne Satzende werden mit dem nächsten zusammen gesprochen und per Whisper geschnitten.
Gesprochene Sätze liegen in `<projekt>/tts_cache/` und werden mit eingecheckt, dann wird nur Geändertes neu gesprochen.

### TikTok-Daten

```bash
python3 -I engine/tiktok.py profil <nutzer>                        # Follower, Likes, alle Videos mit Zahlen
python3 -I engine/tiktok.py kommentare <nutzer> <video_id> --json <scratchpad>/k.json
```
Grenzen ohne Login: Sticker-, GIF- und Bild-Kommentare fehlen oft, eigene Kommentare des Kanals auf oberster Ebene (der angepinnte)
und Antworten darunter fehlen ganz → Screenshots vom Kanalinhaber. Die TikTok-Web-App selbst lässt sich im Container nicht öffnen.
**TikTok-Studio-Zahlen gibt es nur per Screenshot.** Nützlich: Übersicht (Ø Wiedergabe, ganz angesehen, neue Follower, Aufrufkurve),
Haltekurve („Zuschauerbindung“), Traffic-Quellen, Reiter „Zuschauer*innen“.

---

## 7. Stand FC Kuhweide (nur zur Info)

- Gepostet: Tag 1–3. Am 12.11. gebaut: Tag 4 „Berta ist weg“ (26 s) und Tag 4b „Die Neuzugänge“ (34 s).
- Offene Zusagen dort: BERTA-Kommentare zählen (Bertas Heimweg, Folge 5), Spiel am Samstag 14.11. um 15 Uhr gegen den SV Matschbach
  um Berta, Fynns Bratwurst und neuer Mannschaftsbus, Luca als Abwehrchef, Doppelspitze Mia und YG.
- Wird im bisherigen Chat weitergeführt. Der neue Chat ändert dort nichts, kann aber Code und Szenen als Vorlage kopieren.

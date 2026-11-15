# Omas Mondmission – Serien-Gedächtnis

Läuft seit 15.11.2026 auf dem bisherigen Kanal (@gruselwahl.de, vorher „FC Kuhweide“, 122 Follower). Entscheidung und Gründe:
`fc-kuhweide-serie/README.md`, Abschnitt „15.11. abends – Kanal wird weitergenutzt“.

## Idee in einem Satz

Oma Gisela (78) aus Kuhweide hat im Schrebergarten aus ihrem alten Heizöltank eine Rakete gebaut und will mit ihrer Kuh Berta
zum Mond. **Jeder Kommentar = 1 Liter Treibstoff. Bei 100 Litern heben sie ab.** Wer tankt, kommt mit Namen auf die Rakete.

## Roter Faden (seit 15.11. abends, vom Kanalinhaber gewünscht: „mehr Story“)

**Oma holt Opa Heinz vom Mond zurück.** Heinz ist 1974 mit einer selbstgebauten Rakete gestartet und nie zurückgekommen
(im Dorf heißt es: „Der ist nur Brötchen holen gegangen“). Oma findet in seinem alten Heizöltank (Bj. 1974, auf dem Tank ein
eingeritztes Herz „H+G 1974“) eine Postkarte vom Mond: Vorderseite „Grüße vom Mond“ mit Heinz im Goldfischglas-Helm, orangem
Overall, Koteletten, Brille, Schnurrbart, neben einer rot-weißen 70er-Rakete und einem Gartenzwerg. Rückseite: „Liebe Gisela,
komm nach! Dein Heinz ♥ PS: Bring Kuchen mit. PPS: Vorsicht vor den M…“ (Rest abgerissen). Was meint Heinz? (Auflösung später:
Mondkühe.)

| Phase | Inhalt | Mitmachen |
|---|---|---|
| 1 Der Start | Tank füllen, Krause sabotiert, Testzündung geht schief, Start bei 100 Litern | Kommentar = 1 Liter, Namen auf die Tafel „Bodenkontrolle“ |
| 2 Die Reise | Krause als blinder Passagier entdeckt (zu dritt), Meteoriten, Weltraumschrott, Tankleck | Funksprüche an Oma (die besten liest sie vor), Abstimmungen mit 2 Optionen |
| 3 Der Mond | Heinz' Spuren (Brötchentüte 1974, Gartenzwerg im Krater), Mondkühe (Berta verliebt sich), Heinz finden mit Überraschung | Rätsel mitraten, Abstimmungen |
| danach | Rückflug, Mars oder Heinz' nächstes Geheimnis | |

Jede Folge endet mit einer offenen Frage. Namen stehen auf der Kreidetafel **„Bodenkontrolle · Kuhweide · Mission Mond“** im Garten
(Entwurf: 94 Namen passen lesbar in 3 Spalten, bei Bedarf zweite Tafel), nicht mehr auf der Rakete.

## Figuren

| Figur | Aussehen | Rolle |
|---|---|---|
| **Oma Gisela (78)** | weißer Dutt mit Stricknadel, Fliegerbrille auf der Stirn, rote Strickjacke, blaue Schürze mit Punkten, rosa Puschen | Erzählerin (eigene Stimme), frech: „Der kann mir mal den Buckel runterrutschen!“ |
| **Berta** | die Kuh aus FC Kuhweide, jetzt mit Goldfischglas-Raumhelm und Antenne | Kopilotin; muht in den Helm, die Scheibe beschlägt (Running Gag) |
| **Herr Krause** | Vorstand Gartenverein, Weste, Halbglatze mit Strähnen, Schnurrbart, Klemmbrett „§17“ | Gegenspieler hinter der Hecke: „Raketen sind verboten! §17“, Frist bis Sonntag |
| Gartenzwerg | rote Mütze, Fernglas | einziger Zuschauer, verliert beim Start seine Mütze |

**Rakete:** Heizöltank (Bj. 1974), Spitze = roter Trichter mit Punkten, Bullauge = alte Waschmaschine, Flügel = Backbleche,
Düse = Blumentopf, Lichterkette am oberen Rand, Leiter, Gartenschlauch, Tankanzeige „LEER“, Namensfeld „Hier kommen eure Namen hin“.
**Ort:** Parzelle 17 im Schrebergarten neben der Kuhweide (hinten: Wiese mit kleinem Fußballtor, Dorf mit Kirche), Abendlicht.

## Mitmach-Regeln (ehrlich zählen)

- **Liter = angezeigte Kommentarzahl unter allen Folgen minus Kommentare des Kanals selbst.** So kann jeder nachzählen.
- **Namen auf der Rakete:** jeder Account, der kommentiert hat (einmal pro Person). Sticker-Kommentare sind über die
  Abfrage unsichtbar, dafür braucht es Screenshots.
- Kommen weniger Liter zusammen, wird es trotzdem lustig (Rakete hüpft nur bis aufs Laubendach).

## Namen auf der Rakete (Platzfrage, 15.11.)

- Test mit den 94 Namen aus dem FC-Kuhweide-Abspann: Auf den Tank passen nur **61 Namen, und das nur in Schrift 12** (zu klein).
  Das kleine Namensfeld aus dem ersten Entwurf ist deshalb raus. Folge 1 zeigt jetzt „UNTERSCHRIFTEN ERWÜNSCHT!“ quer über den
  Tank, und der Pinsel malt „DEIN NAME?“ groß darüber.
- **Plan ab Tag 2:** Namen wie Unterschriften auf einem Gips über die ganze Rakete (Tank, Trichter, Backbleche, Blumentopf).
  Im Video fährt die Kamera langsam daran entlang, damit jeder seinen Namen findet (Pause drücken).
- **Wenn es voll wird:** Oma schnallt Booster an (Regentonne, Milchkanne, alter Boiler). Jeder Booster bringt mehr Treibstoff
  und neuen Platz für Namen, und die Rakete wächst sichtbar mit der Gemeinschaft. Notfalls kommen Namen auch auf Bertas Helm
  oder Krauses Hecke (Ärger mit Krause). Im All werden die Namen später zu Sternen.
- Technik: `packNames()` in `omas-mondmission-tag1/scene.js` (Zonen + Aussparungen, Schrift 26 → 12), Probeschnitte
  `namesTest` / `namesClose`. Offen für Tag 2: Namen auf dem Trichter liegen noch unter der Trichter-Grafik (eigene Ebene
  nach `rkNose` nötig), Backbleche als schräge Zonen.

## Folgenplan (Entwurf)

| Folge | Inhalt |
|---|---|
| Tag 1 | Vorstellung, Krause dagegen, Tank 0/100, Regel, Vorschau auf den Start, Namensfeld, „Schreib TANKEN!“ |
| Tag 2 | echter Tankstand + erste Namen auf der Rakete, Testzündung geht schief (Oma voller Ruß, Berta-Helm beschlagen), Krause: „Frist bis Sonntag!“ |
| Tag 3 | Krause sabotiert (Schlauch, Ordnungsamt), Abstimmung mit 2 Optionen, wie die Rakete geschützt wird |
| Start | bei 100 Litern: großes Startvideo, danach Folgen im All (Mond, Raumstation, Sternschnuppen) |

## Technik

- Projekt `omas-mondmission-tag1/`: `make_script.py` → `script.json` + `out/beschreibung.txt`; Szene `scene.js` (eigene Grafik,
  Engine-Rig für Oma), Overlay-Elemente in `index.html` (#hook, #tankHud, #demo, #cta, KLONG), `cover.html`, `avatar.js`.
- Neue Geräusche in `engine/audio.py`: `klong` (leerer Tank), `brush` (Pinsel).
- Stimme: VoxCPM2-Entwürfe (Runde 1 A–C: 250–430 Hz, zu jung; Runde 2 D–G: 180–265 Hz) klangen dem Kanalinhaber alle
  unnatürlich. Deshalb Qwen3-TTS (ebenfalls aus VoiceStudio, Apache-2.0): Entwurf mit dem VoiceDesign-Modell (Proben Qwen 1–4,
  saubere Aufnahmen, 207–333 Hz), danach Klonen mit dem Base-Modell. Die gewählte Probe wird `voice/oma_ref.wav` + `oma_ref.txt`,
  in `script.json` `"engine": "qwen"`. Einrichtung: `engine/README.md`, Abschnitt „Qwen3-TTS“.

## Stand

- 15.11.: Folge 1 gebaut (Grafik, Titelbild, Profilbilder `out/profilbild_oma.png` / `profilbild_duo.png`). Bilder vom
  Kanalinhaber gelobt. Stimme: **Oma_Qwen_1** gewählt („warm, leicht rau, frech und verschmitzt“), Referenz `voice/oma_ref.wav`.
  Endfassung `omas-mondmission-tag1/out/omas-mondmission_tag1.mp4` (ca. 27 s). Satz 2 sagt „Heizöl-Tank“ (mit Bindestrich
  spricht Qwen das Ö sauber, ohne kam „Heizhültank“); Qwen sagt „habe“ statt „hab“, Untertitel angepasst.
- Tipp Vertonung: Zahlen im `say` ausschreiben; „100“ statt „hundert“ in `tts_qa.txt` ist nur Schreibweise der Erkennung.

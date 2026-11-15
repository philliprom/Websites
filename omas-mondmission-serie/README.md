# Omas Mondmission – Serien-Gedächtnis

Läuft seit 15.11.2026 auf dem bisherigen Kanal (@gruselwahl.de, vorher „FC Kuhweide“, 122 Follower). Entscheidung und Gründe:
`fc-kuhweide-serie/README.md`, Abschnitt „15.11. abends – Kanal wird weitergenutzt“.

## Idee in einem Satz

Oma Gisela (78) aus Kuhweide hat im Schrebergarten aus ihrem alten Heizöltank eine Rakete gebaut und will mit ihrer Kuh Berta
zum Mond. **Jeder Kommentar = 1 Liter Treibstoff. Bei 100 Litern heben sie ab.** Wer tankt, kommt mit Namen auf die Rakete.

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

- 15.11.: Folge 1 gebaut (Grafik, Titelbild, Profilbilder `out/profilbild_oma.png` / `profilbild_duo.png`), stumme Vorschau.
  Warten auf die Stimmwahl (D, E, F oder G), danach Vertonung und Endfassung.

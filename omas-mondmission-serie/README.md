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

## Zahlen

| Video | gepostet | Länge | Stand | Aufrufe | Likes | Komm. | Shares | Gesp. |
|---|---|---|---|---|---|---|---|---|
| Abschied FC Kuhweide | 15.11. 13:49 | 20 s | 16.11. früh | 824 | 18 | 7 | 2 | 2 |
| Mondmission Tag 1 | 15.11. 18:52 | 36 s | 16.11. früh | 743 | 26 | 11 | 0 | 1 |
| Mondmission Tag 1 | 15.11. 18:52 | 36 s | 16.11. 22 Uhr | 796 | 28 | 12 | 0 | 1 |
| Mondmission Tag 2 | 16.11. 13:01 | 23 s | 16.11. 22 Uhr (nach 9 h) | 766 | 9 | 11 | 0 | 1 |
| Mondmission Tag 1 | 15.11. 18:52 | 36 s | 18.11. abends | 806 | 27 | 12 | 0 | 1 |
| Mondmission Tag 2 | 16.11. 13:01 | 23 s | 18.11. abends | 777 | 10 | 11 | 0 | 1 |
| Mondmission Tag 3 | 18.11. 21:33 | 28 s | 19.11. mittags (ca. 15 h) | 647 | 14 | 17 | 0 | 0 |

**Studio Tag 1 (16.11. 07:14):** 746 Aufrufe, Ø Wiedergabe **9,1 s von 37 s (25 %)**, ganz angesehen 5,3 %, 12 neue Follower,
Gesamtwiedergabe 1:54 h, 96,9 % „Für dich“. Kurve: Absturz in der ersten Sekunde (laut TikTok hören die meisten bei 0:01 auf),
bei ca. 3 s nur noch rund 40 %, danach langsam fallend. Aufrufe kamen in zwei Testwellen von je rund 200 pro Stunde in den
ersten ca. 6 h, danach Stillstand. Zum Vergleich FC Kuhweide Tag 2: 72 % bei 1 s, ca. 37 % bei 4 s.
**Folgerung:** Das erste Bild hält nicht (ruhige Totale, langer Textkasten, ruhiger erster Satz). Tag 2 mit Action im ersten
Bild (kalter Einstieg), kürzer (≤ 25 s).

Tag 2 trotz Explosion im ersten Bild wieder bei rund 770 Aufrufen, Likes nur 1,2 % (Tag 1: 3,5 %). Kanal 16.11. abends:
139 Follower. Alle 10 Videos des Kontos liegen bei 750–1.600 Aufrufen, egal welches Konzept, welche Länge, welcher Einstieg.
Offene Frage: liegt es am Inhalt oder am Konto (Publikum aus FC-Kuhweide-Zeiten)? Vorschlag: dieselbe Folge auf dem neuen
Konto B testen.

Kanal 16.11. früh: 137 Follower (15.11.: 122). Anzeigename noch „FC Kuhweide“, Bio schon umgestellt.
**Tank nach Tag 1: 11 Liter** (11 Kommentare von 11 verschiedenen Leuten, alle „Tanken“, keine Sticker): leif244, mxik.1965,
ljl1407, ka_digga60, flo49472, hannes.mp, 2022lennie, nellly1946, lennox.hager, azad_.051, ryersonmotion1909.
Niemand hat auf „Vorsicht vor den M…“ geraten.

## Tag 2 (gebaut 16.11. vormittags, `omas-mondmission-tag2/`)

23 s, −14,0 LUFS. Kalter Einstieg: Testzündung explodiert im ersten Bild (Feuerball, Scherben, „KABUMM!“, Rakete hüpft und
bleibt schief stehen, Oma voller Ruß mit zerzausten Haaren, Bertas Helm beschlagen). Danach Tank 11/100, Postkarte kurz, Tafel mit
den 11 Namen, Krause mit Schild „FRIST: SONNTAG!“, Aufruf. Liter und Namen stehen in `tank.json` (vor dem Posten aktualisieren,
dann `make_script.py` und neu bauen; nur Sätze mit der Zahl werden neu gesprochen). Neues Geräusch `boom` in `engine/audio.py`.

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
- 15.11. abends: Folge 1 mit Heinz-Geschichte neu gebaut (11 Sätze, **37 s**, −14,2 LUFS): Postkarte vom Mond (Vorder- und
  Rückseite), Herz „H+G 1974“ auf dem Tank, Kreidetafel „Bodenkontrolle“ mit „DEIN NAME?“, offenes Ende „PPS: Vorsicht vor den M…“
  → „Egal! Schreib Tanken!“. Titelbild und Einstieg: „OMA (78) HOLT OPA VOM MOND“.
- 15.11. später: Kanalinhaber hörte eine „dauernd veränderte“ Stimme. Messung: Stimmfarbe ähnlich (0,93–0,99), aber Tonhöhe
  je Satz 137–298 Hz (Referenz 252 Hz). Lösung in der Engine: `"candidates": 4, "temperature": 0.7` – je Satz 4 Fassungen,
  Auswahl nach Sprecher-Ähnlichkeit, Tonhöhe nah an der Referenz und WER. Danach 224–282 Hz, Ähnlichkeit 0,96–0,99.
  Endfassung 36,7 s, −14,2 LUFS. Messskript: Sprecher-Einbettung von Qwen (`qwen3_engine.speaker_similarity`).
- Tipp Vertonung: Zahlen im `say` ausschreiben; „100“ statt „hundert“ in `tts_qa.txt` ist nur Schreibweise der Erkennung.

## Tag 3 (gebaut 18.11. abends, `omas-mondmission-tag3/`)

Kanalinhaber will es „nochmal probieren“. **Tank: 23 Liter** (Tag 1: 12 Kommentare, Tag 2: 11). **20 Namen** auf der Tafel
(einmal pro Person; neu: .al1n4aa, wer.hat.dich.gefr, 2.takt.lennox.de, hassi7333, finni111, jan.priv068, tayler_235,
kersy58 (Antwort), luki02235). Ablauf: kalter Einstieg mit Heizöl-Fontäne aus einem Loch im Tank („Krause hat ein Loch in
meinen Tank gebohrt!“) → Kaugummi-Flicken („PFLOPP!“) → Tankanzeige zählt 11 → 23 → Tafel mit 20 Namen → Krause mit
Bohrmaschine, dann Schild „FRIST: SONNTAG!“ („Am Sonntag kommt das Ordnungsamt!“) → **Abstimmung A 🐄 Berta hält Wache /
B 🏡 als Gartenhaus tarnen** → „Schreib A oder B. Jeder Kommentar ist ein Liter!“. Tag 4 zeigt das Ergebnis der Abstimmung.
Stimme Oma_Qwen_1 mit 4 Fassungen pro Satz, neu `max_pause` 0,45 s.

## Auswertung Tag 3 (19.11. mittags)

- 647 Aufrufe nach rund 15 h, 14 Likes (2,2 %), 17 Kommentare, 0 Shares, 0 gespeichert. Gepostet 21:33 statt wie geplant
  12–13 Uhr. Reichweite bleibt im Bereich aller Folgen (650–820), wächst nicht.
- Abstimmung (eine Stimme pro Person): **B 3** (@l_eg7430, @1234567891011cwjs, @jonas_hptn) : **A 1** (@lenni.gehres21)
  → Rakete wird als Gartenhaus getarnt.
- @jonas_hptn hat nach seinem „B“ 13 einzelne Buchstaben kommentiert: H I W I G E T E S E U C H („Hi, wie geht's euch“).
  Nach Regel (jeder Kommentar = 1 Liter) zählt alles: **Tank 23 + 17 = 40 Liter**.
- @ka_digga60 heißt jetzt @anonym13142 (gleiche Person, Name auf der Tafel angepasst). **24 Namen**, Tafel damit voll.
- Studio-Daten (Wiedergabedauer, Kurve) fehlen noch, beim Kanalinhaber erfragen.

## Tag 4 (gebaut 19.11., `omas-mondmission-tag4/`)

28,3 s, −14,3 LUFS. Kalter Einstieg: Rakete steht als Gartenhaus da (Bretterwand, Fenster mit Vorhängen ums Bullauge,
Blumenkasten, Schild „GARTENHAUS“, Tür mit Herz, rotes Dach, nur die Raketenspitze guckt raus), Oma präsentiert, „TADAA!“ →
Zoom auf die Spitze → Tank 23 → 40 → Buchstaben-Tanker @jonas_hptn: Buchstaben-Kacheln „HI WIGETES EUCH“ = „Hi, wie geht's
euch?“, Oma: „Uns geht es prima!“ → Tafel mit 24 Namen, Stempel „VOLL!“ → neues Feld „DEIN NAME HIER ✍️“ an der
Gartenhaus-Wand → Krause mit Schild „SONNTAG: ORDNUNGSAMT!“ → **Abstimmung Ja 🏡 fällt drauf rein / Nein 🚨 fliegt auf** →
„Jeder Kommentar ist ein Liter!“. Sichere Zonen geprüft (nur Kulissen-Schrift). Alle 8 Sätze ohne Aussprachefehler.
Tag 5 (Sonntag): Ordnungsamt kommt, Ergebnis der Abstimmung.

## Auswertung Tag 4 (20.11. mittags)

- Gepostet 19.11. 11:52. **658 Aufrufe, 13 Likes (2,0 %), 76 Kommentare**, 0 Shares, 0 gespeichert. Reichweite wie immer
  (650–870), die Kommentarzahl ist ein Rekord, kommt aber von nur **4 Personen**.
- Buchstaben-Tanken ist zum Spiel der Stammzuschauer geworden (Tag 4 hatte @jonas_hptn dafür gelobt):
  - @1234567891011cwjs (Chris): **64 Buchstaben** = „halo wie gehtes euch ofe gut bis morgen tschau könt ihr mich grüßen
    heiße chri(s)“ → er will **gegrüßt werden**.
  - @david69056: 9 Buchstaben „DEHALOHLO“ (vermutlich „Hallo“).
  - @lol_111.4: „hoffe euch geht's gutttt“ (Antwort auf „Uns geht es prima“).
- **Abstimmung Ja/Nein: 0 Stimmen.** Niemand hat abgestimmt, alle haben getankt.
- Unter Tag 1 neu: @noel63501 „Wieso keine Fußballmannschaft mehr“ + „Ich vermisse sie“ (war im FC-Kuhweide-Ehrenkader, Nr. 77).
- **Tank: 14 + 11 + 17 + 74 = 116 Liter → VOLL.** (2 Kommentare unter Tag 4 sind unsichtbar, Sticker oder eigener
  Kommentar, nicht gezählt.) **27 Namen** (neu: @noel63501, @david69056, @lol_111.4).
- Lehre: Wer erwähnt oder gegrüßt wird, kommentiert weiter. Persönliche Grüße im Video sind der stärkste Hebel für
  Kommentare, aber nicht für Reichweite (Aufrufe bleiben gleich, Shares 0). Studio-Daten (Wiedergabedauer) fehlen noch.

## Tag 5 (gebaut 20.11., `omas-mondmission-tag5/`) – DER START

Kalter Einstieg: Heizöl schießt oben aus der Raketenspitze (Gartenhaus-Tarnung steht noch), „Ihr Verrückten! Der Tank ist
voll!“ → Tankanzeige 40 → 116 („VOLL!“), Buchstaben regnen in die Spitze → **Chris' Brief** als Buchstaben-Kacheln (64),
„Liebe Grüße zurück, Chris!“ → „Hallo David!“ (Kacheln) → **Noel: rotes FC-Kuhweide-Trikot Nr. 77** fliegt an den
Fahnenmast der Rakete → Oma und Berta im Bullauge: „Ordnungsamt hin oder her: Wir starten jetzt!“, die Gartenhaus-Wand
kracht um, das Dach fliegt weg → Countdown 3-2-1-LOS, Start mit Rauchfahne, Zwerg verliert die Mütze → „Ach du Schreck! Herr
Krause hängt dran!“: Krause baumelt am Gartenschlauch unter der Rakete, Schild „HALT! §17“, strampelt →
**Abstimmung A 🫨 abschütteln / B 🚀 mitnehmen**. Ab jetzt neue Mitmach-Regel: Funksprüche an Oma (im angepinnten Kommentar).
Countdown-Piepser per `countdown.py` genau auf die gesprochenen Zahlen gelegt (zweiter Lauf von `make_script.py`).
**Endfassung 28,5 s, −14,1 LUFS**, alle 8 Sätze ohne Aussprachefehler, sichere Zonen geprüft (nur Kulisse: Tafel, Trikot am Mast).
Nachbesserung 20.11.: Kanalinhaber hörte bei Satz 7 („Moment mal. Herr Krause hängt dran!“) eine andere Stimmfarbe. Messung:
gewählt war 217 Hz / Ähnlichkeit 0,965 (übrige Sätze 229–276 Hz, 0,966–0,987). 10 weitere Fassungen derselben Worte blieben
zu tief oder fremd (118–328 Hz, ≤ 0,976). Neue Formulierung **„Ach du Schreck! Herr Krause hängt dran!“**: 257 Hz, 0,987.
Lehre: Wenn ein Satz in vielen Fassungen nicht passt, liegt es an der Formulierung, nicht am Zufall. Umformulieren.
Tag 6: Ergebnis der Abstimmung (Krause abschütteln oder als blinder Passagier mit), erste Funksprüche.

## Plan Tag 6: Follower gewinnen (21.11., Wunsch des Kanalinhabers)

Befund: Seit Start der Mondmission (15.11.) nur 122 → 140 Follower (+18 in 6 Tagen). „1 Kommentar = 1 Liter“ bringt
Kommentare, aber keinen Grund zu folgen. Bei FC Kuhweide brachte jede Folge 26–36 Follower (Follow-Rate 2,2–3,6 %), weil
**Folgen selbst Teil des Spiels war** („1 Follower = 1 Fan“, „ich nehme euch in den Verein auf“).

- **Neue Regel ab Tag 6: „Jeder Follower bringt Oma näher an den Mond. Bei 200 Followern landet sie.“** Öffentlich nachprüfbar
  (Followerzahl im Profil), wie die Liter. Im Video: Flugbahn Erde → Mond, Rakete steht beim aktuellen Stand (z. B. 140/200),
  am Ende die Profilkarte der Engine mit animiertem „Folgen“-Knopf (`ui.profile.followAt`). Kommentare bleiben Funksprüche.
- Inhalt Tag 6: Ergebnis der Abstimmung (Krause abschütteln/mitnehmen), erste Funksprüche vorlesen, Follower-Ziel.
- Sofort im Profil (Kanalinhaber): Anzeigename von „FC Kuhweide“ auf „Omas Mondmission 🚀“, Bio aktualisieren
  („Start bei 100“ ist erledigt), Tag 1 und Tag 5 im Profil anpinnen.
- Erwartung ehrlich: Reichweite liegt bei ca. 650 Aufrufen. Mit 2–3 % Follow-Rate sind das 13–20 Follower je Folge, also
  200 in etwa 3–4 Folgen, wenn die Reichweite nicht steigt.

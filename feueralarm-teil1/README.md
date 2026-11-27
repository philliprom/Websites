# DER FEUERALARM · Teil 1 (POV-Schuldrama, 3D-Toon)

Video im Format des Vorbilds „Perspektive in Dramen“ (POV, Dialog statt Erzähler, Regeln einer unbekannten Nummer als
Handy-Einblendung, Entscheidungskarte am Ende). **Geschichte, Figuren, Sets und Wendung sind eigene**, nichts ist 1:1
übernommen.

- Video: `out/feueralarm_teil1_tiktok.mp4` (1080×1920, 30 fps, Version 2: 2:10 min, −14 LUFS);
  wegen der Größe nicht im Repo (`.gitignore`), lässt sich mit dem Ablauf unten neu erzeugen
- Titelbild: `out/titelbild.png`
- Beschreibung: `out/beschreibung.txt`, angepinnter Kommentar: `out/kommentar.txt`

## Geschichte

Feueralarm in der 8c. Die Vertretungslehrerin Frau Sander schließt die Tür ab: „Das ist nur eine Übung.“ Eine unbekannte
Nummer schreibt Noah (du, POV) Regeln: Sie ist keine Lehrerin, sie sucht **dich**. Sie macht „Anwesenheit“, dreht die
Durchsage des Schulleiters ab und telefoniert („Ich weiß nur noch nicht, welcher“). Lina lenkt sie ab, Noah und Ben fliehen
über den Vorbereitungsraum, durch den Flur in den Keller (Raum K3). Dort ist Hausmeister Pohl, der den Alarm gedrückt hat.
Regel 5: „Ich bin's. Papa. Geh NICHT mit Pohl. Hinterhof. Blaues Auto.“ Pohl: „Ich war auf der Beerdigung deines Vaters.“

**Entscheidung für Teil 2:** AUTO (der Nummer glauben) oder POHL (beim Hausmeister bleiben).

Figuren: Noah (du, nur Hände/Stimme), Ben (Freund, orange Hoodie), Lina (Klassenkameradin), Frau Sander (Bob, Brille,
Blazer), Hausmeister Pohl (Mütze, Schnurrbart), Schulleiter (nur Durchsage).

## Version 2 (Rückmeldung: Aussprache, Hände, Ende)

- **Aussprache:** Jede Zeile wurde mit Whisper Wort für Wort geprüft. Vorher gab es Fehler wie „Crank. Sozo.“, „Rige drei“,
  „Ruben ist eine Frau“, und „unten“ war kaum verständlich. Jetzt ist jede Figur ein **Klon einer festen Referenz** aus ihren
  deutlichsten Aufnahmen (`voices2.py`, `tts_cache/refs/`). Je Zeile gibt es 2 bis 4 Varianten, gewählt wird nach
  Wort-Sicherheit, Textgleichheit und Stimmähnlichkeit (`tts_cache/wahl2.json`). Alle 37 Zeilen werden jetzt fehlerfrei erkannt.
  Ein paar Texte sind für die Sprachausgabe umgeschrieben: „So, so.“, „Raum Ka drei“, „Lauf, lauf!“, „Da oben ist eine Frau“.
  Die künstliche Beschleunigung der Regeln ist entfernt, sie klang unnatürlich.
- **Regel 5:** Noah liest nur „Regel fünf.“, der Rest kommt in der **Stimme des Vaters** (tief, warm, leiser Hall). So denkt
  niemand, Noah sagt „Ich bin's. Papa.“
- **Hände:** Eine rechte Hand hält das Handy wie im Vorbild (Daumen rechts, Fingerspitzen links, Ärmel von unten rechts),
  der Bildschirm bleibt frei.
- **Ende:** ruhige Handy-Einstellung für Regel 5, dann Pohls Gesicht ohne Schwenk, dann Ben. Die Endkarte ist aufgeräumt
  (kein Zusatztext, ruhiger dunkler Hintergrund), der Ton am Ende ruhiger (ein Schlag bei „Papa“, leiser Herzschlag).
- Die Durchsage hat eine tiefere Schulleiter-Stimme, Pohls erster Satz ist in seiner normalen Stimmlage.
- Die Untertitel folgen den echten Wortzeiten (Whisper), nicht mehr der Zeichenzahl.

## Herstellung (alles lokal, kostenlos)

| Schritt | Werkzeug | Datei |
|---|---|---|
| Skript, Emotionen je Zeile | Python | `story.py` |
| 7 Stimmen | Qwen3-TTS: Stimmentwurf (VoiceDesign), dann Klon je Figur (Base); Auswahl nach Whisper-Wortsicherheit | `voices.py`, `voices2.py`, `tts_cache/auswahl2.json` |
| Zeitleiste | Stille schneiden, Pausen kürzen, Regeln 14 % schneller (Praat) | `timeline.py` → `timeline.json` |
| 3D-Toon-Look | Blender Workbench (ohne Grafikkarte, Mesa/EGL), eigene Toon-Matcap, schwarze Konturen per Geometry Nodes, Schlagschatten | `toon.py`, `make_matcap.py` |
| Figuren | Gelenkpuppen aus Grundformen (große Köpfe/Augen, Frisuren, Kleidung) | `figur.py`, `cast.py` |
| Sets | Klassenzimmer 204 mit Blick auf den Schulhof (Sammelplatz, Feuerwehr), Flur, Keller K3 | `set_klasse.py`, `set_flur.py`, `tex.py` |
| Animation | Lippen nach Lautstärke, Blinzeln, Blickrichtung, Gesten, Gehen/Rennen, POV-Handkamera | `anim.py`, `shots.py` (34 Einstellungen) |
| Rendern | Grundszenen einmal bauen und zusammenfassen, dann je Einstellung 720×1280 | `build_base.py`, `render_shot.py` |
| Ton | Feueralarm-Klingel, Gong + Durchsage (Lautsprecher-Filter), Vibration, Schritte, Türen, Keller, Spannungsmusik, Herzschlag; Sprache immer ≥ 12 dB über Hintergrund | `sound.py` |
| Schnitt | Hochskalieren auf 1080×1920, Farbstimmung je Ort (Flur: rotes Alarmlicht), Untertitel weiß mit roten Schlüsselwörtern, Regel-Banner, Entscheidungskarte | `assemble.py` |
| Titelbild | Standbild in voller Auflösung + Schlagzeile | `make_cover.py` |

Ablauf (Pfade anpassen; `bl` = Blender-Python, `qw` = Qwen-Umgebung, `vx` = Ton):

```bash
python3 tex.py && python3 phone.py && python3 make_matcap.py
qw/bin/python voices.py gen <Qwen3-TTS-VoiceDesign> 2      # Stimmentwürfe (~8x Echtzeit auf CPU, QWEN_DTYPE=bf16)
qw/bin/python voices2.py refs                               # Referenz je Figur
qw/bin/python voices2.py klon <Qwen3-TTS-Base> 2            # Klon-Varianten (~5x Echtzeit)
qw/bin/python voices2.py wahl <Qwen3-TTS-Base> <whisper-medium>
QA_WHISPER=<whisper-medium> qw/bin/python timeline.py       # mit Wortzeiten für die Untertitel
EGL_PLATFORM=surfaceless bl/bin/python build_base.py klasse <base>/klasse.blend   # dito flur, keller
EGL_PLATFORM=surfaceless bl/bin/python render_shot.py liste <base> <frames>       # schreibt build/shots.json
EGL_PLATFORM=surfaceless bl/bin/python render_shot.py alle <base> <frames>        # ~1 Bild/s bei 2 Prozessen
vx/bin/python sound.py
python3 assemble.py <frames>
EGL_PLATFORM=surfaceless bl/bin/python render_shot.py standbild 16_soso:60.45 <base> <bild.png> && python3 make_cover.py <bild.png>
```

Hinweise:
- Workbench braucht `libegl1 libegl-mesa0 libgl1-mesa-dri libgbm1` (apt). EEVEE läuft auf Mesa nicht sauber.
- Beim Zusammenfügen in Blender gingen Texturkoordinaten verloren: texturierte Flächen (Tafel, Uhr, Schilder) bleiben deshalb
  einzeln (`toon.merge_children`).
- Schulter-Gelenke drehen in der Reihenfolge ZXY (erst um den Oberarm, dann heben, dann abspreizen), sonst zeigen
  verschränkte Arme nach außen.

## Ideen für Teil 2 (je nach Abstimmung)

- **AUTO gewinnt:** Hinterhof, das blaue Auto läuft schon. Am Steuer ein Mann mit Kappe und Sonnenbrille, die Stimme vom
  Telefon: „Steig ein, Noah.“ Ben weigert sich. Regel 6: „Wenn er die Brille abnimmt, renn.“ Frau Sander taucht am
  Schultor auf. Entscheidung: einsteigen oder zurück zu Lina?
- **POHL gewinnt:** Pohl führt die beiden durch den Heizungsgang zur Turnhalle. Pohls Handy vibriert, Absender: dieselbe
  unbekannte Nummer: „Du hattest einen Auftrag.“ Was weiß Pohl? Entscheidung: Pohl das Handy wegnehmen oder weglaufen?
- In beiden Fällen kommt Lina zurück (sie hat Frau Sander abgelenkt und weiß jetzt etwas über sie).

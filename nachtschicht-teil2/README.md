# Nachtschicht – Teil 2 (beide Fassungen)

Die Abstimmung unter Teil 1 entscheidet, welche Fassung gepostet wird. Damit Teil 2 sofort nach der Abstimmung online
gehen kann, werden **beide** fertig produziert.

## Geschichte
- **A – aufgemacht** (`a/`): Du drehst den Schlüssel um, die Tür geht auf: Regen, niemand. Du schließt wieder ab. Der
  Chef schreibt: „Wer hat dir gesagt, dass du aufmachen sollst?“ – im Chat fehlt seine Nachricht von 02:47, er hat nie
  geschrieben. Auf Kamera 1 erscheinen nasse Fußspuren von der Tür an der Theke vorbei bis hinter die Kasse („Du warst
  nicht draußen“). Das Licht geht aus, die Kamera schaltet auf Nachtsicht: die Kapuzengestalt steht am Ende der Spuren.
  „Und direkt hinter dir atmet jemand.“ Teil 3: **A Umdrehen · B Rausrennen**.
- **B – nicht aufgemacht** (`b/`): Du bleibst hinter der Theke, er klopft noch einmal dreimal. Der Chef: „Er friert.“ –
  „Warum machst du nicht auf?“ Das Klopfen hört auf, Kamera 1 leer, Kamera 3 leer – aber auf Kamera 2 (Lager) steht die
  Hintertür offen, nasse Spuren führen herein. Auf der Rückseite des Zettels: „5. Steht die Hintertür offen, ist er
  schon drin. VERSTECK DICH!“ Am Ende fällt hinten eine Tür ins Schloss. Teil 3: **A Verstecken · B Rausrennen**.

## Mehr Gefühl in der Stimme
Wunsch nach Hörprobe 3 (`stimmproben/horror/emotion/`): „geht in die richtige Richtung, wenn es spannend wird gern
noch ein Ticken mehr“. Jeder Satz hat eine Spannungsstufe 0–3 (`story.py`); `emotion.py` hebt ihn per PSOLA an
(+1,5 / +2,8 / +4 Halbtöne, 4–12 % schneller, lebendigere Melodie, ab Stufe 2 zum Satzende steigend), `sound.py` macht
ihn 1 / 2 / 3,5 dB lauter. Messung Fassung A: Stufe 3 von 85–94 Hz auf 113–125 Hz, Stufe 2 von 84–97 auf 102–117 Hz.

## Ablauf
1. `story.py` → `a/script.json`, `b/script.json`
2. `engine/build_timeline.py nachtschicht-teil2/a|b <Qwen3-TTS-Base>` (qw) → `<zweig>/build/vo.wav`, `timeline.json`
3. `emotion.py a|b` (vx) → Stimme angehoben, Zeitleiste neu (Original als `vo_roh.wav` / `timeline_roh.json`)
4. `plan.py a|b` → `<zweig>/build/edl.json`; für A auch `build/shots.json` (Bildzahl und Türbeginn der Ich-Sicht)
5. `scene.py --shot …` (bl, Blender) → neue Bilder in `build/`: `tuer` (Ich-Sicht, Bildfolge), `spuren` +
   `spuren_leer` (Standbilder; die Differenz sind nur die Spuren, `spuren.json` = Lage jeder Spur im Bild), `ir`
   (Nachtsicht), `lager` (CAM 02, Bildfolge), `zettel_rueck`. Kamera 1 leer, Kamera 3 und die Gestalt an der Tür
   kommen aus den Bildfolgen von Teil 1 (`nachtschicht-teil1/build/r1–r3`).
6. `node assets.cjs` → Sperrbildschirm, Benachrichtigungen, Chat, Abstimmungskarte, Entscheidungskarten
7. `sound.py a|b` (vx) → `<zweig>/build/mix.wav`
8. `assemble.py a|b` (vx) → `out/nachtschicht_teil2_<a|b>.mp4`; `--cover` → `out/titelbild_<a|b>.png`

## Dinge, die beim Bauen aufgefallen sind
- Die Bäume aus Teil 1 stehen teils direkt hinter dem Laden: durch die offene Hintertür sah man nur einen Baum.
  Für das Lager werden sie entfernt.
- Die Theke verdeckt von CAM 01 aus den Boden direkt daneben: die Spuren laufen deshalb mit etwas Abstand zur Theke
  (per Strahl geprüft: alle sichtbar außer der ersten auf der Fußmatte).
- Die runde Folgen-Gestalt wirkt aus der Nähe albern: in der Nachtsicht steht die Kapuzengestalt vom Profilbild.

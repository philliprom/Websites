# Horror-Test „Nachtschicht“ (24.11.2026)

Idee: interaktive Horror-Serie im Überwachungskamera-Stil („Du entscheidest“), angeregt von @playmalo.com (Format ja,
deren Geschichten/Figuren nein). Test, ob Blender in der Cloud realistisch genug aussieht.

- `scene.py`: Blender 5.3 als Python-Modul (`pip install bpy==5.3.0` in eigener venv, ca. 1,1 GB), Cycles auf der CPU.
  Alles prozedural: Tankstellen-Shop (Glasfront, Theke mit Kasse, Regale, Kühltüren, 2 kaputte Röhren, eine flackert),
  draußen Tankdach mit Zapfsäulen, nasser Asphalt, Regen (Streifen per Treiber animiert), Gestalt im Mantel mit Kapuze
  (Gesicht im Schatten, schwacher Augenglanz). Ablauf 5 s / 15 fps: Gestalt steht draußen im Regen → Bild 47–50 Licht
  aus → ab Bild 51 steht sie direkt an der Glastür, Kopf schief.
- Kamera wie echte Überwachungskamera: oben hinter der Theke, Blick auf die Eingangstür.
- `post.py`: Ton (Regen, Röhrenbrummen, Klick beim Stromausfall, Schlag + Sting beim Sprung, dreimal Klopfen) und Look
  (450×800 → 1080×1920, Unschärfe, Rauschen, ausgeblichene Farben, Vignette, „CAM 03 EINGANG“, Datum/Uhrzeit läuft,
  blinkendes „● REC“, Farbversatz beim Sprung). `--test <png>` macht ein Vorschaubild.
- Rechenzeit: ca. 35 s pro Bild bei 450×800, 40 Samples, 4 CPU-Kerne → 5 s Video ≈ 45 min.

## Ergebnis Test 1
`out/nachtschicht_test.mp4` (5 s) und `out/standbild_tuer.png`. Stimmung und Kamera-Look funktionieren (Zeitstempel,
REC, Rauschen, Stromausfall mit hell bleibendem Tankdach draußen, Sprung an die Tür mit Bildstörung und Klopfen).
Schwächen: Die Gestalt wirkt noch wie eine Schaufensterpuppe (aus Grundformen gebaut), Waren und Regale sind einfache
Klötze. Nächste Stufe: echte Texturen/HDRI von Poly Haven (CC0, Host muss freigegeben werden), Figur aus MakeHuman (CC0),
mehr Details (Preisschilder, Plakate, Schmutz), Kamerabewegung leicht (Rauschen/Zittern statt starr).

## Test 2 (24.11. abends): mehr Details, neuer Ton
Wunsch des Kanalinhabers nach Test 1: „ein paar mehr Details und bessere Soundeffekte“.
- Szene: Fliesen mit Fugen und Schmutz, Rasterdecke, Fußmatte und Pfütze am Eingang, rotes „OFFEN“-Neonschild im
  Fenster (von innen spiegelverkehrt, rotes Licht), „24/7“-Aufkleber, Öffnungszeiten, Sicherheitsspiegel in der Ecke,
  Kühlregale mit Glastüren, Böden und Flaschen im Gegenlicht, Preisleisten und Preisschilder an den Regalen,
  Regalschilder, Plakate („KAFFEE 1,50 €“, „2 FÜR 1“), Kaffeeautomat mit Display, Zigarettenregal mit Packungen,
  Monitor, Kaffeebecher, Lotto-Schild, draußen Bordstein, Parkmarkierungen, Mülleimer, Preissäule mit LED-Preisen,
  Luftstation. Gestalt an der Tür: rechte Hand flach an der Scheibe auf Gesichtshöhe.
- Ton (Stereo, `post.py`, mit der vx-Umgebung wegen SciPy): siehe Kopf von `post.py`. Lautheitsverlauf: Grundpegel
  um −23 dB, beim Stromausfall leiser (−27), Schock −8 dB, Klopfen −11/−12 dB.
- Rechenzeit: ca. 60 s pro Bild (32 Samples, 450×800), 75 Bilder ≈ 75 min.

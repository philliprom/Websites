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

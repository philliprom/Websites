# Stimmen und Aussprache

Die wichtigste Rückmeldung zur ersten Fassung war: „Wörter falsch ausgesprochen, klingt unnatürlich.“ Die Ursachen
und das Verfahren, das sie behoben hat:

## Verfahren (Qwen3-TTS, alles lokal auf CPU, `QWEN_DTYPE=bf16`)

1. **Stimmentwurf** (`voices.py gen <VoiceDesign> 2`): je Zeile 2 Varianten aus Figurenbeschreibung (`VOICES` in
   `story.py`, Englisch) + Emotion (`emo`). Etwa 8-fache Echtzeit.
2. **Referenz je Figur** (`voices2.py refs`): 1–3 der deutlichsten Entwurfs-Aufnahmen einer Figur (Whisper-Mindestsicherheit
   ≥ 0,8) aneinandergehängt, 5–10 s. Welche, steht in `REFS` in `voices2.py`: nach Runde 1 anhand der Werte anpassen.
3. **Klon** (`voices2.py klon <Base> 2`): jede Zeile 2-mal als Klon der Referenz. Etwa 5-fache Echtzeit. Gleiche Stimme
   in jeder Zeile und stabilere Aussprache als reine Entwürfe.
4. **Auswahl** (`voices2.py wahl <Base> <whisper-medium>`): alle Varianten (Entwürfe + Klone) mit Whisper prüfen.
   Punkte = mittlere Wortsicherheit + 0,8 × schwächstes Wort − 2 × Wortfehlerrate + Stimmähnlichkeit. Bericht:
   `tts_cache/wahl2.json`, Auswahl: `tts_cache/auswahl2.json`.
5. **Nachbessern**: Zeilen mit schwächstem Wort < 0,7 → 2 weitere Klone (`klon … 4 <id,id>`) und `wahl … <id,id>`.
6. **Stimmlage prüfen** (Praat-Median je Zeile): weicht eine Zeile weit von der Figur ab (z. B. 203 Hz statt 90 Hz beim
   Hausmeister), die passendere Variante von Hand in `auswahl2.json` eintragen und nach `tts_cache/<id>.wav` kopieren.
7. **Zeitleiste** (`QA_WHISPER=… timeline.py`): schneidet Stille, kürzt nur sehr lange Pausen (> 0,45 s), holt
   Wortzeiten für die Untertitel. **Kein Tempo-Stretching** (machte die Regeln unnatürlich).
8. **Endmix prüfen** (`scripts/aussprache_endmix.py`): jede Zeile im fertigen Video mit allen Effekten. Ziel: alle exakt.

## Was schiefging und was half

| Problem | Ursache | Lösung |
|---|---|---|
| „Crank. Sozo.“ statt „Krank. Soso.“ | Entwurfsmodell, seltenes Wort | Sprechtext „Krank. So, so.“ + Klone + Auswahl |
| „Rige drei“, „Ruben ist eine Frau“ (Oben…), „unten“ unverständlich | Entwürfe mit Emotion (Flüstern/Panik) instabil | Klone einer klaren Referenz, Whisper-Auswahl; Satzanfang „Da oben …“ |
| „Lauf!“ als „Ui, huuuh“ / „WAUF! FÜLF!“ | Einwortruf | „Lauf! Lauf!“ |
| Regeln klangen gepresst | Praat-Tempo 0,86 | entfernt |
| Noah liest „Ich bin's. Papa.“ → klingt, als wäre Noah der Papa | Regeln immer in Noahs Stimme | Noah liest nur „Regel fünf.“, Rest in eigener **Vater-Stimme** (tief, warm, wenig Hall) |
| Durchsage klang wie ein Kind (360 Hz) | Entwurf „loud, urgent“ | Beschreibung „deep, low pitch … without shouting“, Variante mit 209 Hz |
| Im Endmix: „Warum“ → „Baron“ | Lautsprecher-Filter zu hart | Band 260–4800 Hz, wenig Verzerrung, Hall 0,18 |
| „Noah?!“ aus der Ferne → „Norbert“ | Flur-Hall 0,55 | Hall 0,28, Tiefpass 5,5 kHz |
| „Papa…?“ → „Baba“ | kurz, unter Herzschlag, mit Hall | trocken, +3 dB, Herzschlag setzt dort aus |
| Sprache zu leise neben der Alarmklingel | Klingel mit hohen Anteilen | Seitenketten-Absenkung: Hintergrund ≥ 12 dB unter der Stimme; Klingel tiefpassgefiltert |

Zahlen nach dem Verfahren (Feueralarm): alle 37 Zeilen trocken exakt erkannt; im Endmix 36 von 37 (verbliebener Rest:
„dem/den“ beim Rennen).

## Stimmen der Feueralarm-Besetzung (Referenzen liegen im Folgenordner `tts_cache/refs/`)

| Figur | Beschreibung (Kurz) | Tonhöhe |
|---|---|---|
| Noah (POV) | 15, Stimme gerade gebrochen, leicht rau | ~135 Hz |
| Ben (Freund) | 14, hell, schnell, frech | ~280 Hz |
| Lina | 15, klar, selbstbewusst | ~345 Hz |
| Frau Sander (Täterin) | Mitte 40, tief, glatt, kalt-höflich | ~170 Hz |
| Hausmeister Pohl | ~60, tief, rau, warm | ~90 Hz |
| Schulleiter (Durchsage) | Ende 50, tief, bestimmt | ~210 Hz |
| Vater (Regel 5) | Mitte 40, warm, tief, leise | ~88 Hz |

Für eine Fortsetzung dieselben Referenzen nehmen (Ordner kopieren), dann klingen die Figuren gleich.

## Rechenzeit (4 CPU-Kerne)

Entwurf ~8×, Klon ~5× Echtzeit. 37 Zeilen: Entwürfe ~35 min, Klone ~25 min, Auswahl ~10 min. Währenddessen
können Szenen gebaut und Testbilder gerendert werden (mit `nice`).

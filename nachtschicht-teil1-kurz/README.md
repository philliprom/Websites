# Nachtschicht – Teil 1, kurze Fassung (21 s)

Warum: Die lange Fassung (79 s) lief auf zwei Konten schwach – @monsterdoener 61 Aufrufe in 4,5 h, @gruselwahl.de
275 Aufrufe in 8 h (7 Likes, 1 Kommentar, 0 geteilt). Der Anfang war zu ruhig („Würdest du aufmachen?“ über einem
dunklen Bild, dann „Acht Minuten vorher“ und 30 s Regeln), das Klopfen kam erst nach ~45 s.

Neu: Sekunde 0 springt das Bild aus dem Dunkeln auf die Gestalt an der Tür, dreimal Klopfen, großer Text
„ER KLOPFT DREIMAL.“ Dann in schnellen Schnitten: Regel 4 mit Textmarker → „Egal, wer es sagt“ → CAM 03 (Gestalt im
Regen, verschwindet) → Gestalt an deiner Tür → Nachricht vom Chef → A/B. Bilder komplett aus Teil 1, Stimme neu
(9 kurze Sätze), mit Gefühl (wie Teil 2) und 10 % schneller.

Ablauf: `story.py` → `engine/build_timeline.py nachtschicht-teil1-kurz <Qwen3-TTS-Base>` → `emotion.py` → `plan.py`
→ `sound.py` → `assemble.py` (`--cover` für das Titelbild). Ergebnis: `out/nachtschicht_teil1_kurz_tiktok.mp4`
(21,3 s, 18 MB, −14,4 LUFS), `out/titelbild_kurz.png`, `out/beschreibung_kurz.txt`.

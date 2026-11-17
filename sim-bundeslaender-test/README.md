# Testvideo: Simulation „16 Bundesländer – nur eins überlebt“ (17.11.2026)

Idee: Physik-Simulation statt Zeichentrick + KI-Stimme. Bälle (Bundesländer mit Flaggenfarben) in einem drehenden Ring mit
Lücke. Wer durch die Lücke fällt, ist raus. Tabelle unten zeigt Platzierungen, am Ende Sieger mit Krone und Aufruf
„Schreib dein Bundesland“. Keine Stimme, nur Musik und Töne (jeder Wandkontakt spielt den nächsten Ton einer Melodie).

- `sim.py`: Physik (deterministisch, 600 Schritte/s), Seed-Suche nach Tempo, Ton (Engine-Klangbausteine aus `engine/audio.py`).
  `python3 sim-bundeslaender-test/sim.py suche 240` → passende Seeds, `… bau <seed>` → `build/sim.js`, `timeline.json`, `mix.wav`.
- `index.html`: Darstellung (SVG), `window.renderAt(t)`; gerendert mit `node engine/render.cjs sim-bundeslaender-test`.
- Ton: `ffmpeg … -af loudnorm=I=-14:TP=-1.5:LRA=11` beim Zusammenfügen.
- Einstellungen: g 900, Ring r 410, Ball r 46, Drehung 0,9 rad/s, Lücke halbe Breite 0,15 rad + 0,01 je Ausgeschiedenem.
- Seed 166: erster raus nach 1,7 s, alle ≤ 4 s einer, Finale 3,9 s, Sieger Saarland, Video 35,2 s, −15,3 LUFS.
- Ehrlich bleiben: Seed nur nach Tempo auswählen, nie nach Sieger.

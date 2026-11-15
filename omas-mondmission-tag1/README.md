# Omas Mondmission – Tag 1 🚀

Erste Folge der neuen Serie auf dem bisherigen FC-Kuhweide-Kanal. Serien-Gedächtnis: [`../omas-mondmission-serie/README.md`](../omas-mondmission-serie/README.md).

**Ablauf (ca. 28 s):** Oma Gisela (78) vor ihrer Heizöltank-Rakete, Berta mit Raumhelm („Ich bin 78 und fliege mit meiner Kuh zum Mond.“)
→ Kamerafahrt an der Rakete mit Beschriftungen (Blumentopf, Backbleche, Waschmaschine, Trichter) → Berta muht, der Helm beschlägt
→ Herr Krause taucht hinter der Hecke auf („Raketen sind verboten! §17“) → „Der kann mir mal den Buckel runterrutschen!“
→ KLONG: Tank leer → Tankanzeige 0/100 L, Beispiel-Kommentar „TANKEN“ fliegt hinein (+1 L) → Vorschau auf den Start bei 100 Litern
→ Pinsel malt „DEIN NAME?“ aufs Namensfeld → Aufruf „Schreib TANKEN!“.

**Dateien:** `out/titelbild.png`, `out/profilbild_oma.png` / `out/profilbild_duo.png` (Vorschau: `out/profilbild_vorschau.png`),
`out/beschreibung.txt` (Caption, angepinnter Kommentar, Profiltexte).

## Bauen

```bash
python3 omas-mondmission-tag1/make_script.py
# Stimme: voice/oma_ref.wav + voice/oma_ref.txt (gewählte Probe), dann
HF_HUB_OFFLINE=1 QA_WHISPER=<modelle>/whisper-medium <vx>/bin/python engine/build_timeline.py omas-mondmission-tag1 <modelle>/VoxCPM2
python3 engine/audio.py omas-mondmission-tag1
node engine/render.cjs omas-mondmission-tag1
ffmpeg -i omas-mondmission-tag1/build/video_noaudio.mp4 -i omas-mondmission-tag1/build/mix.wav -c:v copy -c:a aac -b:a 192k -shortest omas-mondmission-tag1/out/omas-mondmission_tag1.mp4
node engine/render_cover.cjs omas-mondmission-tag1
node engine/render_avatar.cjs omas-mondmission-tag1 oma duo
```
Ohne Stimme (Bilder prüfen): `python3 engine/provisional_timeline.py omas-mondmission-tag1`, dann `node engine/render.cjs omas-mondmission-tag1 --stills 1,5,9`.

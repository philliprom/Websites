# GTA-6-Highlight-Kanal (Idee vom 19.11.2026)

Clips bekannter deutscher Streamer als TikTok-Highlights, **nur von Streamern, die das öffentlich erlauben**
(`streamers.json`, mit Regeln und Quelle). Stand 19.11.: **Papaplatte** (Content Guidelines über leakshield: TikTok/Shorts
frei nutzbar, nicht für Werbung, nicht aus dem Zusammenhang, nichts Schädigendes, frühestens 12 h nach dem Stream,
möglichst Material, das er selbst nicht nutzt). Für andere deutsche Streamer keine öffentlichen Regeln gefunden.

## Ablauf
1. **Top-Clips finden:** `python3 clips/twitch_top.py` → `out/topclips_<datum>.md` (offizielle Twitch-Schnittstelle,
   meistgesehene Clips des Spiels „Grand Theft Auto VI“, mindestens 12 h alt). Braucht `TWITCH_CLIENT_ID` und einen
   App-Token (Netzwerk-Geheimnis für api.twitch.tv oder `TWITCH_TOKEN`), und api.twitch.tv muss in der Umgebung erlaubt sein.
2. **Clip-Dateien:** lädt der Kanalinhaber selbst herunter (diese Umgebung erreicht Twitch nicht) und schickt sie.
3. **Schnitt:** `<vx>/bin/python clips/make_short.py <clip.mp4> --streamer papaplatte --titel "…"` →
   1080×1920, Facecam oben + Spiel darunter (Facecam-Bereich in `streamers.json`) oder Spiel groß, Untertitel per Whisper
   (Nunito Black, gesprochenes Wort gelb, max. 740 px breit), Titel ab y 290, „▶ twitch.tv/…“ unten links, −14 LUFS.
   Alles in den sicheren Zonen (engine/README.md).
4. **Prüfen vor dem Posten:** Regeln des Streamers (12 h, Zusammenhang, keine Werbung), Titel ehrlich, Streamer in der
   Beschreibung nennen und verlinken.

## Test
`test/testclip.mp4` ist ein künstlicher Testclip (Testbild, „FACECAM“-Kasten, Sprache aus unserer Stimme), kein echter
Stream. `test/test_mit_facecam.mp4` und `test/test_ohne_facecam.mp4` zeigen die beiden Layouts.

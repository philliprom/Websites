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
   Upload im Chat geht nur bis 30 MB: Clips in **720p** laden (60 s ≈ 20–28 MB, 30 s ≈ 10–15 MB), 1080p nur bei
   Clips bis etwa 30 s. Für TikTok reicht 720p, der Schnitt rechnet den Facecam-Bereich automatisch um.
3. **Schnitt:** `<vx>/bin/python clips/make_short.py <clip.mp4> --streamer papaplatte --titel "…"` →
   1080×1920, Facecam oben + Spiel darunter (Facecam-Bereich in `streamers.json`) oder Spiel groß, Untertitel per Whisper
   (Nunito Black, gesprochenes Wort gelb, max. 740 px breit), Titel ab y 290, „▶ twitch.tv/…“ unten links, −14 LUFS.
   Alles in den sicheren Zonen (engine/README.md).
4. **Prüfen vor dem Posten:** Regeln des Streamers (12 h, Zusammenhang, keine Werbung), Titel ehrlich, Streamer in der
   Beschreibung nennen und verlinken.

## Test
`test/testclip.mp4` ist ein künstlicher Testclip (Testbild, „FACECAM“-Kasten, Sprache aus unserer Stimme), kein echter
Stream. `test/test_mit_facecam.mp4` und `test/test_ohne_facecam.mp4` zeigen die beiden Layouts.

## Regel (19.11.2026)
Nur Streamer mit Erlaubnis kommen in `streamers.json` und damit in Liste und Schnitt: öffentliche Regeln (wie Papaplatte),
die Twitch-Einstellung „Zuschauer dürfen Clips in sozialen Netzwerken hochladen“ (Teilen-Menü unter einem Clip zeigt
TikTok/YouTube/Instagram) oder eine schriftliche Zusage. Clips ohne Erlaubnis werden nicht automatisiert (Wunsch des
Kanalinhabers vom 19.11. abgelehnt: Risiko von Meldungen und Kontosperre liegt bei seinem Konto).

## Schritte für den Kanalinhaber
Einmalig: neues TikTok-Konto (neutraler Name), Erlaubnisse sammeln (Teilen-Menü prüfen oder Anfrage, Vorlage unten),
Twitch-Entwickler-App (dev.twitch.tv/console → Register Your Application, Redirect `http://localhost`, Client-ID +
Secret), Token per `curl.exe -X POST "https://id.twitch.tv/oauth2/token" -d "client_id=…&client_secret=…&grant_type=client_credentials"`
(gilt ca. 60 Tage), Token ins sichere Formular (api.twitch.tv), Client-ID in den Chat (nicht geheim).
Täglich automatisch: geplante Aufgabe erstellt morgens die Top-Clip-Liste. Täglich von Hand (ca. 5 min): 3–5 Clips
auswählen und herunterladen, in den Chat schicken; Schnitt automatisch; posten oder in TikTok Studio planen.

## Anfrage-Vorlage
„Hi <Name>! Ich möchte einen kleinen TikTok-Kanal mit GTA-6-Highlights deutscher Streamer starten. Darf ich Clips aus
deinen Streams verwenden? Ich nenne und verlinke dich in jedem Video, poste frühestens am Tag danach, schneide nichts aus dem
Zusammenhang und nutze nichts für Werbung. Wenn du etwas nicht drin haben willst, nehme ich es sofort raus. Danke dir!“

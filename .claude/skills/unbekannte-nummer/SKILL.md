---
name: unbekannte-nummer
description: >-
  Produziert komplette animierte TikTok-POV-Dramen im Format „Unbekannte Nummer“: Du (POV) bekommst Regeln von einer
  unbekannten Nummer, eine falsche Autoritätsperson bedroht die Klasse, Flucht, Wendung, Entscheidungskarte „Teil 2
  entscheidet ihr“. 3D-Toon-Look in Blender, 6–7 KI-Stimmen mit Aussprache-Prüfung, Regel-Banner, Untertitel mit roten
  Schlüsselwörtern, Ton, Titelbild, Beschreibung, angepinnter Kommentar. Benutze diesen Skill immer, wenn eine neue Folge,
  ein Teil 2, eine Fortsetzung oder eine neue Geschichte im POV-/Regel-/Entscheidungsformat gewünscht ist (z. B. „mach Teil 2
  vom Feueralarm“, „neue Folge für Unbekannte Nummer“, „so ein POV-Video wie das letzte“, „AUTO hat gewonnen, weiter geht's“),
  auch wenn das Wort Skill nicht fällt, und wenn Zahlen dieser Videos ausgewertet werden sollen.
---

# Unbekannte Nummer: POV-Dramen produzieren

Erste Folge: **Der Feueralarm, Teil 1** (Repo-Ordner `feueralarm-teil1/`). Auf @gruselwahl.de hatte sie nach 1,3 h
1.629 Aufrufe und 4,8 % Likes, später 9.000 Aufrufe, Ø 50,9 s Wiedergabe (bei 130 s Länge), 17,5 % bis zum Ende,
101 neue Follower. Die Folgen davor im anderen Stil kamen insgesamt auf ca. 275. Fortsetzung: **Teil 2**
(`feueralarm-teil2/`, 68 s, Auto/Straße/Ampel). Dieser Skill enthält den kompletten, erprobten Ablauf als Vorlage und
alles, was beim ersten Mal schiefging.

Sprache mit dem Nutzer: **Deutsch**, ehrlich (nichts schönreden), kurze Zwischenstände bei langen Schritten.

## Wann welche Datei lesen

- `references/format.md`: Bausteine, Geschichte in 14 Takten, Texte, Endkarte, Titelbild, Beschreibung. **Vor dem Schreiben
  der Geschichte lesen.**
- `references/stimmen.md`: Stimmen und Aussprache-Prüfung, Liste bekannter Fehler und ihre Lösung. **Vor dem Vertonen lesen.**
  Die Aussprache war der Hauptkritikpunkt der ersten Fassung.
- `references/produktion.md`: alle Befehle, welche Datei je Folge anzupassen ist, wie `shots.py` geschrieben wird,
  Rendern, Ton, Schnitt, Stolperfallen.

## Ablauf

1. **Umgebung prüfen**: Gibt es Blender-Python, Qwen-Modelle und Whisper? Wenn nicht: `bash scripts/setup.sh <ordner>`
   (ca. 16 GB, braucht PyPI und Hugging Face). Ist der Container neu gestartet, fehlen eventuell Mesa-EGL-Pakete;
   `setup.sh` installiert sie nach.
2. **Folge anlegen**: `python3 scripts/neue_folge.py <repo>/<ordner> --titel "TITEL" --teil "TEIL 1"`. Das kopiert die
   funktionierende Vorlage (Feueralarm) mit allen Skripten. Für einen Teil 2 dieselben Sets, Figuren und Stimm-Referenzen
   weiterverwenden: `tts_cache/refs/` aus dem Vorgängerordner kopieren.
3. **Geschichte** in `story.py` (eigene Geschichte, nie ein fremdes Video nacherzählen): 14 Takte aus `format.md`, 5 Regeln,
   ca. 35–40 Zeilen, Sprechtext (`say`) aussprachefreundlich. Dem Nutzer Kurzfassung und Entscheidung kurz zeigen, wenn die
   Richtung unklar ist. Sonst direkt weiterarbeiten.
4. **Stimmen** im Hintergrund starten (Entwurf → Referenz → Klon → Auswahl, siehe `stimmen.md`). Während das läuft:
5. **Sets, Figuren, Einstellungen**: Sets anpassen oder neu bauen, `build_base.py`, `shots.py` schreiben, Testbilder aller
   Einstellungen als Kontaktbogen prüfen (Sprecher sichtbar? Sicht frei? Hand natürlich?).
6. **Zeitleiste** mit Wortzeiten (`timeline.py`), dann **Vollrendern** in zwei Prozessen (~1 Bild/s; 2 min Video ≈ 65 min).
7. **Ton** (`sound.py`, Ereignisse der Folge eintragen), **Schnitt** (`assemble.py`).
8. **Prüfen**: Kontaktbogen (`scripts/kontaktbogen.sh`), Lautheit −14 LUFS, `scripts/aussprache_endmix.py` (Ziel: jede Zeile
   exakt erkannt). Abweichungen nach der Tabelle in `stimmen.md` beheben, dann nur den Ton neu anlegen.
9. **Abliefern**: Video und Titelbild per SendUserFile, Beschreibung und angepinnter Kommentar zum Kopieren in die Antwort,
   README im Folgenordner, Commit und Push (Video selbst nicht ins Repo).
10. **Auswerten**, wenn der Nutzer einen Link schickt: `python3 scripts/tiktok_stats.py <link>`. Das liest nur öffentliche
    Seiten, nie einloggen oder Zugangsdaten annehmen. Kommentare entscheiden über Teil 2.

## Feste Regeln

- TikTok-Sicherheitszonen: Inhalte zwischen y 288 und 1248 (bei 1080×1920), Untertitel-Unterkante ≤ 1248, rechts unten Platz
  für die Knöpfe.
- Format und Stil anderer Kanäle sind erlaubt, deren Geschichten, Figuren und Bilder nicht.
- Keine Login-Daten für TikTok annehmen oder anfordern; die E-Mail des Nutzers nie in externen Anfragen verwenden.
- Alle Werkzeuge lokal und kostenlos (Blender, Qwen3-TTS Apache-2.0, Whisper, ffmpeg). ElevenLabs ist für diesen Account gesperrt.

## Skripte

| Skript | Zweck |
|---|---|
| `scripts/setup.sh <ziel>` | Umgebung im frischen Container (EGL, Blender-Python, Ton, Qwen, Modelle) |
| `scripts/neue_folge.py <ordner>` | neue Folge aus der Vorlage `assets/vorlage/` |
| `scripts/tiktok_stats.py <link oder @handle>` | öffentliche Zahlen eines Videos, oder ob ein Handle frei ist |
| `scripts/aussprache_endmix.py <folge> [video]` | Endkontrolle jeder Zeile im fertigen Video |
| `scripts/kontaktbogen.sh <video> <bild> [s]` | Kontaktbogen alle N Sekunden |

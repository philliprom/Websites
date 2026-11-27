# Neuer Kanal: POV-Dramen „Unbekannte Nummer“

Kanal für die animierten POV-Schuldramen (erste Folge: `feueralarm-teil1/`). Format: Du (POV) bekommst Regeln von einer
unbekannten Nummer, jede Folge endet mit einer Entscheidung, die Kommentare bestimmen Teil 2.

## Name

**Empfehlung:** Anzeigename **Unbekannte Nummer**, Handle **@die.unbekannte.nummer**

Warum: Der Name ist zugleich das Versprechen jeder Folge (Regeln von unbekannt) und macht neugierig. Er passt zu Banner,
Profilbild und Endkarte.

Handle-Prüfung über die öffentlichen Profilseiten (27.11.2026, ohne Login; kann sich jederzeit ändern):

| Handle | Status |
|---|---|
| @die.unbekannte.nummer | frei (Empfehlung) |
| @unbekanntenummer.pov | frei |
| @unbekannte.nummer.de | frei |
| @klasse8c.pov | frei (Alternative mit Fokus auf die Figuren: „Klasse 8c“) |
| @pov.entscheidungen | frei (Alternative „POV: Du entscheidest“) |
| @wem.glaubst.du | frei, aber @wemglaubstdu existiert (1.260 Follower), Verwechslungsgefahr |
| @unbekannte.nummer, @unbekanntenummer, @klasse8c, @du.entscheidest | vergeben (kleine Konten) |

## Beschreibung (Bio, max. 80 Zeichen)

Empfehlung (70 Zeichen):

```
📱 Eine unbekannte Nummer schreibt dir Regeln. Teil 2 entscheidet ihr 👇
```

Alternativen:

```
POV-Dramen 📱 Regeln von einer unbekannten Nummer. Ihr entscheidet 👇
Du bekommst Regeln von einer unbekannten Nummer. Befolgst du sie? 📱
```

## Profilbild

`out/profilbild.png` (1080×1080, TikTok zeigt es rund), Vorschau in drei Größen: `out/profilbild_vorschau.png`.
Toon-Hand mit Handy wie im Video, auf dem Bildschirm das gelbe „?“ der unbekannten Nummer und „REGEL 1“, dunkler Grund
mit gelbem Ring (gleiche Farben wie die Regel-Banner).

```bash
python3 profilbild.py textur
EGL_PLATFORM=surfaceless <blender-python> profilbild.py render   # nutzt toon.py und cast.py aus feueralarm-teil1
python3 profilbild.py bild
```

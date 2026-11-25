# Kanal „Nachtschicht – Du entscheidest“

Neuer TikTok-Kanal für interaktive Horror-Geschichten (ab 25.11.2026). Format wie @playmalo.com (Du-Perspektive,
Abstimmung A/B per Kommentar), Geschichten und Bilder eigen. Idee für später: Jede Geschichte ist eine andere
Nachtschicht (Tankstelle, Krankenhaus, Wachdienst, Leitstelle …), so passt der Name zu jeder neuen Serie.

## Profil
TikTok-Grenzen: Name 30 Zeichen, Benutzername 24 Zeichen (Buchstaben, Zahlen, Punkt, Unterstrich), Bio 80 Zeichen.
Die App zählt beim Tippen mit. Emojis können doppelt zählen, deshalb ist unten mit 2 Zeichen pro Emoji gerechnet.

- **Name:** `Nachtschicht – Du entscheidest` (30)
- **Benutzername** (ob frei, zeigt nur die App): `nachtschicht.horror` (19) · `nachtschicht.du` (15) · `nachtschicht_ab` (15)
- **Bio**
  1. empfohlen: `Horror zum Mitentscheiden 🚪 Du bist allein. Es klopft. A oder B? 👇` (68)
  2. `Interaktive Horror-Serie 🚪 Du entscheidest in den Kommentaren: A oder B 👇` (75)
  3. `Jede Folge eine Nachtschicht. Es klopft. Du entscheidest: A oder B? 👇` (70)
- **Profilbild:** `out/profilbild.png` (empfohlen, ohne Schrift) oder `out/profilbild_rec.png` (Kamera-Look mit „● REC“).
  So sieht es rund aus: `out/profilbild_vorschau.png` (groß im Profil, klein neben Kommentaren, dunkler/heller Modus).
- Bei jedem Video „KI-generierte Inhalte“ einschalten (Stimme Qwen3-TTS, Bilder am Computer erzeugt).
- Posten abends/nachts (20–23 Uhr).

## Profilbild: so entsteht es
Blender-Szene aus Teil 1 (`nachtschicht-teil1/scene.py`, Einstellung `--shot profil`): von innen frontal auf die
Glastür, Laden dunkel, Tankdach-Licht gedimmt, ein Licht genau über der Gestalt. Fürs Profilbild eine eigene
Kapuzengestalt (Umhang, Kapuze mit Saum, Stofffalten über Displace-Modifier, kleine leuchtende Augen), Regentropfen
auf der Scheibe, Schärfe auf den Augen (Blende 2,8). Der runde Kopf der Folgen-Gestalt wirkte aus der Nähe wie eine
Spielfigur. Befehl mit allen Werten: `nachtschicht-teil1/build/profil/befehl.txt` (1080 × 1080, 80 Samples).
Danach `profilbild.py` (vx-Umgebung): Leuchten um die Augen, kühle Farbe, Vignette, Korn, Variante mit „● REC“,
Vorschau.

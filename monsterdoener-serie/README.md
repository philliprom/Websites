# Monsterdöner – Serien-Gedächtnis

Kanal B (neues, aufgewärmtes Konto). Start 16./17.11.2026. Idee vom Kanalinhaber: „sowas wie die Dönerbude vom Anfang, nur
ausgefallener“ (Vorbild @marlons.doenerbude_: „Tag 1: Ich habe eine Dönerbude eröffnet … 1 Follower = 1 Kunde, ihr entscheidet“).

## Idee

Leo (Anfang 20) hat eine Dönerbude für Monster eröffnet. **1 Follower = 1 Kunde. Ihr entscheidet, welches Monster als Nächstes
kommt** (Abstimmung A/B/C in den Kommentaren, ehrlich gezählt). Jede Folge: viele kurze Szenen, mehrere Figuren mit eigenen
Stimmen, ein Gag pro Kunde, Cliffhanger am Ende.

## Figuren und Stimmen (Qwen3-TTS, je Figur eigene Referenz in `monsterdoener-tag1/voice/`)

| Figur | Aussehen | Gag |
|---|---|---|
| **Leo** (Ladenbesitzer) | braune Haare, weiße Döner-Mütze, schwarzes Shirt, rote Schürze „MD“ | macht alles mit, „Passt so.“ |
| **Graf Vladi** (Vampir) | blasslila Haut, Umhang rot/schwarz, Zähne | „Aber ohne Knoblauch!“ – Soße schon drauf → Puff, Fledermaus |
| **Geist** | weißes Laken, große Augen | Döner fällt durch ihn durch („Schon wieder durchgefallen.“), Stimme mit Hall |
| **Werwolf Wolfgang** | Holzfällerhemd, Bart; bei Vollmond Wolfskopf | „Extra Fleisch!“ → Vollmond → frisst den ganzen Spieß |
| **Zombie Günther** | grün, zerrissenes Hemd | „Mit … alles …“, Arm fällt auf die Theke |
| **Lebensmittelkontrolle** | Schatten hinter der Glastür mit Geister-Staubsauger | Reserve für eine spätere Folge (Szene ist schon gezeichnet) |

**Laden:** Seitenansicht, Fliesenwand, Neonschild „MONSTER DÖNER“, Speisekarte (Vampir-Teller ohne Knoblauch, Hirn-Box),
Dönerspieß vor Grillwand, Kühlschrank „Blutorangen-Limo“, Theke mit Knoblauch-/Scharf-Flasche und Trinkgeldglas
„keine Seelen“, Glastür mit Nachthimmel und Vollmond.

## Mitmachen

- Abstimmung „Wer kommt morgen?“ Tag 1: A 🐺 Werwolf · B 👻 Geist · C 🧟 Zombie (alle drei schon gezeichnet und vertont).
  Gewinner = meiste Kommentare mit dem Buchstaben, eine Stimme pro Person.
- Kunden-Zähler = echte Followerzahl.

## Technik

- Projekt `monsterdoener-tag1/`: `make_script.py` (Segmente mit `"voice"`), `scene.js`, `cover.html`, `avatar.js` (`logo`, `leo`).
- Engine: Stimme pro Segment (`tts.voices`, optional `fx` als ffmpeg-Filter, z. B. Hall beim Geist), neue Geräusche `howl`, `knock`.
- Achtung IDs: Szene darf keine IDs der Engine-Oberfläche benutzen (z. B. `counter`, `title`, `stamp`, `big`) – sonst verschwindet
  das Szenen-Element und der Engine-Kasten erscheint (passiert mit der Theke, jetzt `shopCounter`).

## Stand

- 17.11. nachts: erste Fassung von Tag 1 (verworfen, 34,5 s, −14,6 LUFS, 11 Sätze, 5 Stimmen,
  rund 20 Szenen). Stimmen: Leo 154 Hz, Vampir 161 Hz (zweiter Entwurf, „Male, about 50, very low deep bass“), Geist 273 Hz + Hall,
  Werwolf 214 Hz → per `rubberband` tiefer, Zombie 105 Hz. Ähnlichkeit zur jeweiligen Vorlage 0,93–0,995.
- Profilbilder: `profilbild_logo.png` (Döner mit Vampirzähnen, empfohlen), `profilbild_leo.png`.
- 17.11. Umbau nach Feedback des Kanalinhabers („hektisch, dann wieder lange Pausen, am Anfang passiert nichts Wildes“):
  Tag 1 (`monsterdoener-tag1/out/monsterdoener_tag1.mp4`) ist jetzt **eine durchgehende Vampir-Geschichte**, 24,1 s, 8 Sätze, Pausen höchstens 0,5 s (außer wenn im Bild etwas
  passiert). Ablauf: kalter Einstieg „Mein erster Kunde will mich beißen!“ (Vampir zischt, Nahaufnahme) → „⏪ 30 Sekunden
  vorher“ → „Einen Döner. Ohne Knoblauch.“ → Leo greift zur Knoblauch-Flasche („KNOBLAUCH?!“), tauscht gegen Scharf („PUH …“)
  → Vampir beißt, wird grün → das Brot ist Knoblauch-Fladenbrot → „Neeeein!“ → Puff, Fledermaus-Schwarm, Flaschen fallen →
  Leo mit Besen und Strubbelhaaren „Ab morgen kein Knoblauch mehr.“ → Abstimmung Werwolf/Geist/Zombie.
  Geist, Werwolf, Zombie und Lebensmittelkontrolle sind aus Tag 1 raus und bleiben für spätere Folgen.
- Lehre daraus für alle Folgen: **eine Figur, ein Problem, eine Pointe pro Folge**, das wildeste Bild zuerst (danach Rückblende),
  keine Pausen ohne Handlung, ≤ 25 s.
- Nächste Folge: Abstimmung A/B/C auswerten (eine Stimme pro Person), das Sieger-Monster bekommt seine eigene Geschichte.

## Zahlen

| Folge | gepostet | Stand | Aufrufe | Likes | Komm. | Follower Kanal |
|---|---|---|---|---|---|---|
| Tag 1 (Vampir) | Di 17.11. 08:22 (geplant war 16–17 Uhr) | 17.11. 12:14 (knapp 4 h) | 85 | 2 | 0 | 0 |

- Konto: @monsterdoener. Der angezeigte Name ist noch „DayOnd“ (nicht „Monsterdöner 🧛🥙“). Dazu gibt es ein nicht
  öffentliches Video vom 11.11. (Aufwärmphase).
- Kanalinhaber: „so schlecht hat noch nie ein Video performt“. Zum Vergleich: Auf @gruselwahl.de (älteres Konto mit Verlauf)
  hatten alle Videos 750–1.600 Aufrufe. Ein neues Konto ohne Follower bekommt zuerst nur eine kleine Testgruppe.
- Studio 17.11. 15:32 (7 h): 85 Aufrufe, Gesamtzeit 14:40, **Ø 8,4 s von 24 s (35 %)**, **9,52 % ganz angesehen**, 0 neue
  Follower. Aufrufe fast alle in der ersten Stunde (~90), danach praktisch 0 → TikTok hat nach der ersten Testgruppe
  aufgehört zu verteilen. Zuschauerquellen erst ab 100 Aufrufen sichtbar.
- Kurve (abgelesen): 1 s ≈ 78 %, **3 s ≈ 48 %**, 5 s ≈ 33 %, 8 s ≈ 22 %, danach fast flach bis 21 s (≈ 16 %), Ende ≈ 9 %.
  → Wer 8 s schafft, schaut die Geschichte meist zu Ende. Verloren gehen die Leute in den ersten 3 s.
- Ursache, die wir selbst gebaut haben: Der Satz, der neugierig macht („… will mich beißen!“), kam erst bei **3,5 s**.
  Davor: „Tag eins in meiner Dönerbude für Monster“ (Erklärung) und eine ruhige Totale mit großem weißem Textkasten.
- Vergleich Mondmission Tag 1 (altes Konto): Ø 9,1 von 37 s (25 %), 5,28 % ganz. Haltekraft in % also besser, aber dasselbe Muster:
  die meisten weg bei 0:01. Gilt für alle bisherigen Videos → **die ersten 2 Sekunden sind das Hauptproblem**, nicht die Geschichte.
- Gegenmaßnahme (17.11. nachmittags): neuer Einstieg „Hilfe! Mein erster Kunde will mich beißen!“, Vampir springt ab Bild 1
  fauchend auf die Kamera zu, „beißen“ schon bei ~1,6 s, kein großer Textkasten mehr (nur kleiner Chip „TAG 1 · DÖNERBUDE FÜR MONSTER“).
  Messgröße für den Test: Anteil nach 3 s (vorher ≈ 48 %).
- Neue Fassung Tag 1 (17.11. nachmittags): 22,4 s, −14,6 LUFS. Bild 1 = Vampir in Großaufnahme (springt auf die Kamera zu),
  0,05 s „Hilfe!“, 0,5 s Leo (Hände am Kopf, Schreck-Mund), 1,6 s „will mich beißen!“ mit beiden im Bild, 3,4 s „⏪ 30 Sekunden vorher“.
  Engine: neue Option `talkO` am Figuren-Rig (Schreck-Mund bewegt sich beim Sprechen), standardmäßig aus.
  Empfehlung: altes Video auf „Nur ich“ stellen (nicht löschen), neue Fassung 16–17 Uhr posten, nach 24 h Kurve vergleichen.

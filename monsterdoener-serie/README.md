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

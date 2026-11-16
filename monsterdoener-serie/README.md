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
| **Lebensmittelkontrolle** | Schatten hinter der Glastür mit Geister-Staubsauger | Cliffhanger Tag 1 |

**Laden:** Seitenansicht, Fliesenwand, Neonschild „MONSTER DÖNER“, Speisekarte (Vampir-Teller ohne Knoblauch, Hirn-Box),
Dönerspieß vor Grillwand, Kühlschrank „Blutorangen-Limo“, Theke mit Knoblauch-/Scharf-Flasche und Trinkgeldglas
„keine Seelen“, Glastür mit Nachthimmel und Vollmond.

## Mitmachen

- Abstimmung „Wer kommt morgen?“ Tag 1: A Mumie · B Hexe · C Alien. Gewinner = meiste Kommentare mit dem Buchstaben, eine Stimme pro Person.
- Kunden-Zähler = echte Followerzahl.

## Technik

- Projekt `monsterdoener-tag1/`: `make_script.py` (Segmente mit `"voice"`), `scene.js`, `cover.html`, `avatar.js` (`logo`, `leo`).
- Engine: Stimme pro Segment (`tts.voices`, optional `fx` als ffmpeg-Filter, z. B. Hall beim Geist), neue Geräusche `howl`, `knock`.
- Achtung IDs: Szene darf keine IDs der Engine-Oberfläche benutzen (z. B. `counter`, `title`, `stamp`, `big`) – sonst verschwindet
  das Szenen-Element und der Engine-Kasten erscheint (passiert mit der Theke, jetzt `shopCounter`).

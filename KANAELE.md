# Kanäle – Überblick und Ablauf (Stand 16.11.2026)

**Stand 16.11. abends:** Mondmission pausiert (alle Folgen ~800 Aufrufe, Kanalinhaber: „zu langweilig, nicht aufwendig genug“). Kanal B startet mit **Monsterdöner** (aufwendiger: 5 Figuren, 5 Stimmen, viele Szenen).

Ziel: bis zu 3 TikTok-Kanäle gleichzeitig, ohne durcheinanderzukommen. Grundidee: **3 Kanäle = 3 Versuche.** Jeder Kanal
testet ein eigenes Konzept. Nach etwa 5 Folgen bekommt das Konzept mit den besten Zahlen die meiste Energie.

## Die Kanäle

| | Kanal A | Kanal B | Kanal C |
|---|---|---|---|
| Konto | @gruselwahl.de | neues Konto (aufgewärmt) | noch anlegen |
| Name im Profil | Omas Mondmission 🚀 (pausiert) | Monsterdöner 🧛🥙 | offen |
| Konzept | Oma Gisela holt Opa Heinz vom Mond, Kommentar = 1 Liter | Dönerbude für Monster, 1 Follower = 1 Kunde, Abstimmung wer kommt | eigenes, siehe unten |
| Projektordner | `omas-mondmission-*` | `monsterdoener-*` | eigenes Kürzel |
| Serien-Notizen | `omas-mondmission-serie/README.md` | `monsterdoener-serie/README.md` | `<kürzel>-serie/README.md` |
| Chat | dieser Chat | dieser Chat | eigener Chat |
| Postzeit | 12–13 Uhr | 16–17 Uhr | 19–20 Uhr |

## Regeln gegen Durcheinander

1. **Ein Chat pro Kanal.** Jeder Chat kennt nur seinen Kanal und arbeitet nur in seinen Ordnern. Bei Fragen zu einem Kanal
   immer im passenden Chat schreiben.
2. **Jede Datei zum Posten trägt den Kanal im Namen und in der ersten Zeile:** Video `out/<kürzel>_tagN.mp4`, in
   `beschreibung.txt` steht ganz oben `KANAL: … (@konto)`. Vor dem Posten kurz prüfen: richtiges Konto in der App?
3. **Feste Postzeiten** (Tabelle oben), damit sich die Kanäle nicht gegenseitig Zuschauer wegnehmen und der Tag planbar ist.
   TikTok kann Videos auch zeitgesteuert veröffentlichen (TikTok Studio im Browser), dann reicht einmal am Tag hochladen.
4. **Zahlen und Kommentare** jeden Morgen pro Kanal in den passenden Chat: Studio-Screenshots von gestern und
   Screenshots von Sticker-Kommentaren. Der Chat zählt dann selbst (Liter, Namen usw.).
5. **Kommentare beantworten, schlank:** alle liken, eine Sammelantwort pro Video, nur Fragen einzeln beantworten.
6. **Technik:** Die Engine (`engine/`) ist geteilt. Änderungen nur rückwärtskompatibel (neue Optionen standardmäßig aus).
   Jeder Chat arbeitet auf seinem eigenen Branch. Neue Engine-Bausteine aus diesem Branch holt ein anderer Chat mit
   `git fetch origin claude/gracious-hamilton-5kohce && git checkout origin/claude/gracious-hamilton-5kohce -- engine/`.
7. **Sichere Zonen:** Vor jedem Rendern `node engine/safe_check.cjs <projekt>` laufen lassen, bis „alles frei ✓“ kommt.
   Oben bis 260 px, rechts ab x 920 (y 800–1700) und unten ab 1660 px liegt TikTok-Oberfläche (siehe `engine/README.md`).
8. **Stimmen:** jede Hauptfigur bekommt eine eigene Qwen3-TTS-Stimme (Entwurf + Klon mit `"candidates": 4`), damit
   kein Kanal wie ein anderer klingt. Anleitung: `engine/README.md`, Abschnitt „Qwen3-TTS“.

## Was jeder neue Kanal aus Kanal A lernen sollte

- **Das erste Bild entscheidet.** Mondmission Tag 1: die meisten Zuschauer weg bei 0:01, Ø 9 von 37 s. Deshalb: Action im
  ersten Bild (kalter Einstieg), kurzer Text, starker erster Satz.
- **Kurz:** Hauptfolge höchstens 25 s, pro Satz eine Szene.
- **Geschichte mit offener Frage** (Rätsel, Gegenspieler, Frist) statt nur Namen und Zahlen. Wer dranbleibt, folgt
  (Tag 1: 12 neue Follower bei 746 Aufrufen).
- **Mitmachen mit sichtbarem Ziel** (Tank, Meter, Einwohner …), ehrlich zählen, Namen auf einer Tafel.

- **Stand 17.11.: Der Look selbst ist vermutlich die Grenze.** 13 Videos auf zwei Konten, vier Themen, immer dasselbe Bild:
  die meisten weg bei 0:01. Gezeichnete SVG-Figuren + KI-Stimme wirken neben dem, was sonst auf TikTok läuft, billig.
  Die Cloud-Umgebung hat keine Grafikkarte, deshalb geht hier nur dieser Stil. Besprochen: Produktion auf dem eigenen Rechner,
  falls dort eine NVIDIA-Grafikkarte steckt (freie Bild-/Video-Modelle wie Wan oder FLUX schnell, kostenlos, aber Rechenzeit).

- **17.11.: zwei Testvideos statt Zeichentrick-Geschichten:** `sim-bundeslaender-test/` (Physik-Simulation, keine Stimme,
  Mitmachen über Kommentare) und `techlupe-test/` (Informatik animiert erklärt, für den bestehenden Kanal Tech-Lupe des
  Kanalinhabers, der selbst Informatiker ist).

## Konzept-Ideen für B und C (müssen sich von A und voneinander unterscheiden)

| Idee | Haken im ersten Bild | Mitmachen | Rätsel/Gegenspieler |
|---|---|---|---|
| **Fietland** – Fiete gründet sein eigenes Land auf einer Sandbank | Welle schwappt über die Sandbank, Fiete klammert sich an den Fahnenmast | 1 Kommentar = 1 Sandsack gegen die Flut | Flaschenpost mit Schatzkarte, Nachbarinsel will die Sandbank |
| **Ritterburg aus Pappe** – Kurt (12) baut eine Burg im Hinterhof | Burgmauer kippt auf den Ritter | 1 Kommentar = 1 Stein | Raubritter vom Nachbarhof, geheimer Tunnel |
| **Wanderzirkus** – Zirkus Fiasko ist pleite | Elefant fällt durchs Zelt | 1 Kommentar = 1 Zuschauer | Konkurrenzzirkus, verschwundener Zauberer |

Vorschlag zur Reihenfolge: B startet, sobald das Konto aufgewärmt ist. C erst, wenn A oder B nach einer Woche zeigt,
welche Machart besser läuft. Drei Kanäle täglich kosten viel Nutzungs-Limit, für B und C reicht anfangs jeden zweiten Tag.

## Zweiter Kanal: neue Ideen (18.11.2026)

Kugel-Simulation verworfen (Kanalinhaber: „gibt es zu oft, zu eintönig“). Gezeichnete Geschichten mit KI-Stimme ebenfalls
gefloppt. Neue Richtung: Bewegtgrafik + echte Referenzstimme (wie Tech-Lupe), aber Themen für alle.

1. **Wo geht dein Geld hin? (gewählt 18.11., Folge 1 Döner fertig, siehe `geld-serie/README.md`)** – Alltagspreise aufgeschlüsselt: Döner, Tankfüllung, Kinoticket, Handyvertrag,
   Konzertkarte, Spotify-Stream. Preisschild zerfällt in Teile (Steuer, Miete, Personal, Gewinn …). Zahlen vorher
   recherchieren, als Beispielrechnung kennzeichnen. Diskussionen in den Kommentaren („bei uns kostet er 9 €“).
2. **Rätsel der Geschichte** – echte, gut belegte historische Rätsel (z. B. Kaspar Hauser), mehrteilig mit Cliffhanger.
   Karten, Zeitstrahl, gemeinfreie Bilder. Keine Fälle mit lebenden Beteiligten.
3. **Quiz zum Mitraten** – z. B. Bundesland am Umriss erkennen, Punkte in die Kommentare. Leicht zu machen, aber verbreitet.

# Format „Unbekannte Nummer“: was die Folgen ausmacht

## Inhalt
1. Warum das Format funktioniert (Zahlen)
2. Bausteine jeder Folge
3. Geschichte schreiben: Ablauf in Takten
4. Dialog und Texte für die Sprachausgabe
5. Bild: Einstellungen, die wirken
6. Endkarte, Titelbild, Beschreibung, angepinnter Kommentar
7. Teil 2 und Serien

## 1. Warum das Format funktioniert

- Vorbild: animierte POV-Dramen auf TikTok (eine unbekannte Nummer schickt Regeln, die Klasse ist in Gefahr,
  Entscheidung am Ende). Ein solches Video hatte 2 Mio. Aufrufe bei 160 s Länge. Lange Videos tragen hier, weil alle 5–10 s
  etwas Neues passiert (Regel, Bedrohung, Entdeckung).
- **Der Feueralarm, Teil 1** (27.11.2026, @gruselwahl.de, 157 Follower): **1.629 Aufrufe nach 1,3 h**, Like-Rate 4,8 %,
  13-mal gespeichert, 7 Kommentare. Zum Vergleich: die Folge davor im Überwachungskamera-Stil mit Erzähler hatte insgesamt
  275 Aufrufe. Der Unterschied kam vom Format, nicht vom Kanal.
- Inhalte anderer Kanäle nie 1:1 nachbauen: Format und Stil übernehmen, aber Geschichte, Figuren, Sets und Wendung sind immer
  eigene.

## 2. Bausteine jeder Folge (alle Pflicht)

| Baustein | Umsetzung |
|---|---|
| POV | Kamera = Augen der Hauptfigur (Noah). Sie spricht selbst, man sieht nur ihre Hand mit dem Handy. |
| Dialog statt Erzähler | 5–7 Sprecher mit klar unterschiedlichen Stimmen. |
| Regeln von unbekannter Nummer | 5 Regeln; je Regel: Vibration + „Pling“, Banner oben (dunkel, gelber Rand, „UNBEKANNTE NUMMER“, Uhrzeit, gelb „REGEL n“, weißer Text, GROSSGESCHRIEBENES gelb), Handy in der Hand mit Sperrbildschirm. Noah liest vor. |
| Untertitel | weiß mit dunkler Kontur, Schlüsselwörter rot, ein Satz zur Zeit, unteres Drittel (Unterkante ≤ y 1248 bei 1080×1920). |
| Bedrohung durch Erwachsenen | jemand mit scheinbarer Autorität (Vertretungslehrerin, Busfahrer, Hausmeister, Herbergsvater …) ist nicht, wer er vorgibt. |
| Verbündete | bester Freund (immer dabei) + eine Mitschülerin, die etwas riskiert (Ablenkung). |
| Wendung | Regel 5 stellt alles infrage (Absender-Identität oder Widerspruch zu einem Helfer). |
| Entscheidung | „WEM GLAUBST DU?“ (oder „WAS TUST DU?“) mit zwei Kacheln (Symbol + 1–3 Wörter + kurzer Untertitel), „Teil 2 entscheidet ihr.“ |
| Länge | 2:00–2:30 (Feueralarm 2:10, 37 Zeilen, ca. 280 Wörter). |

## 3. Geschichte schreiben: Ablauf in Takten

Ziel: in den ersten 2 s eine konkrete Bedrohung, danach alle 5–10 s eine Steigerung.

1. **Haken (0–3 s):** Freund flüstert die Bedrohung („Noah… sie hat uns eingeschlossen.“), Bild zeigt sie sofort.
2. **Autorität lügt (3–10 s):** Täter beruhigt falsch („Das ist nur eine Übung.“), jemand widerspricht, wird zurechtgewiesen.
3. **Regel 1 (~11 s):** benennt die Lüge („Sie ist keine Lehrerin“) + eine Verhaltensregel. Noah: „Wer schreibt mir das?“
4. **Kontrolle (20–35 s):** Täter kommt nah, verdächtigt, Noah lügt glaubwürdig; Täter droht unterschwellig.
5. **Beweis von außen (35–40 s):** etwas zeigt, dass alles falsch ist (ganze Schule draußen, Durchsage des Schulleiters).
6. **Regel 2 (~45 s):** macht es persönlich („Sie sucht DICH.“). Täter sucht nach Namen, Freund deckt Noah.
7. **Täter schaltet Hilfe aus (~60 s):** Durchsage abdrehen, Handy wegnehmen, Tür blockieren.
8. **Regel 3 (~70 s):** Fluchtweg + Zeitpunkt („wenn sie telefoniert“). Täter verrät sich am Telefon („Ich weiß nur noch nicht, welcher.“).
9. **Flucht (~80 s):** Mitschülerin lenkt ab, Noah + Freund schleichen raus.
10. **Regel 4 (~85 s):** neues Ziel (Keller K3), Ortswechsel, Rennen, Täter entdeckt die Flucht und ruft hinterher.
11. **Ankunft (~100 s):** scheinbar sicherer Ort, ein Helfer (Hausmeister), der etwas weiß.
12. **Regel 5 (~110 s):** Wendung: „Ich bin's. Papa. Geh NICHT mit Pohl.“ – gesprochen in der **Stimme des Absenders**, nicht von Noah.
13. **Gegenbeweis (~120 s):** Helfer widerspricht hart („Ich war auf der Beerdigung deines Vaters.“).
14. **Frage (~125 s):** Freund: „Noah… wem glaubst du?“ → Endkarte.

Ton: spannend, realistisch, keine Gewalt und kein Blut (Publikum: Jugendliche). Logik muss halten: jede Regel muss sich im
Nachhinein erklären lassen (wer weiß was woher), Teil 2 löst auf.

## 4. Dialog und Texte für die Sprachausgabe

- Kurze Sätze, Jugendsprache sparsam („Alter…“), echte Namen, die gut auszusprechen sind (Noah, Ben, Lina, Pohl, Sander).
- In `story.py` steht `sub` (Untertitel) und `say` (Sprechtext). Im Sprechtext Zahlen ausschreiben („Raum zwei null vier“,
  „Raum Ka drei“) und schwierige Stellen umformulieren. Was nachweislich schiefging, steht in `stimmen.md`.
- Einwortrufe vermeiden (die Stimme verschluckt sie): „Lauf! Lauf!“ statt „Lauf!“.
- Jede Zeile bekommt eine englische Emotionsangabe (`emo`), die nur der Stimmentwurf nutzt.

## 5. Bild: Einstellungen, die wirken

- Weitwinkel (15–17 mm) für Nähe; für Personen in mehr als 3 m Entfernung enger (30–60 mm), sonst sind sie zu klein.
- Handy-Einstellungen: Blick nach unten, 22 mm, eine Hand hält das Handy (Daumen rechts, Fingerspitzen links).
- Freund nah im Profil oder frontal, wenn er spricht; Täter frontal und leicht von unten, wenn er droht.
- Sichtlinien freihalten: Plätze zwischen Kamera und wichtigen Orten leer lassen (`FREI` in `set_klasse.py`).
- Keine Kameraschwenks über Körper (wirkt unruhig); lieber harter Schnitt auf das Gesicht.
- Ortswechsel mit Farbstimmung: Flur mit rotem Alarm-Pulsieren, Keller dunkel mit Vignette.

## 6. Endkarte, Titelbild, Beschreibung, Kommentar

- Endkarte: dunkler, kaum unscharfer Hintergrund, Frage oben, zwei Kacheln, gelbe Pille „Teil 2 entscheidet ihr.“,
  kleiner Titel „DER FEUERALARM · TEIL 1“. Kein weiterer Text (das wirkte durcheinander).
- Titelbild: Standbild des Täters in voller Auflösung (`render_shot.py standbild`), Gesicht unten-mittig, oben gelbe Pille
  „POV: …“ + 3 Zeilen Schlagzeile (zwei weiß, eine rot), „TEIL 1“-Badge. Schrift nie über dem Gesicht.
- Beschreibung: `POV: <Haken>… aber <Wendung> 🔒 und eine unbekannte Nummer schreibt dir, was du tun sollst 📱 (Teil 1)` +
  5 Hashtags (`#pov #storytime #schule #animation #<thema>`).
- Angepinnter Kommentar: Frage + beide Optionen mit Emoji + „Die meisten Stimmen entscheiden Teil 2 👇“.

## 7. Teil 2 und Serien

- Kommentare zählen (AUTO vs. POHL o. ä.), Mehrheit bestimmt die Fortsetzung; im Video kurz sagen, wie abgestimmt wurde.
- Gleiche Figuren, Stimmen (Referenzen in `tts_cache/refs/`) und Sets weiterverwenden: Wiedererkennung.
- Teil 2 beginnt mit 1–2 s Rückblende (letzte Regel als Banner) und dann sofort neuer Bedrohung.

# FC Kuhweide – Tag 1 ⚽

Idee 3 für das „Tag 1 / 1 Follower = 1 X / ihr entscheidet“-Format. Das Video ist vertikal (1080×1920, 30 fps, ca. 43 s).

**Fertiges Video:** [`out/fc-kuhweide_tag1.mp4`](out/fc-kuhweide_tag1.mp4) · **Cover:** [`out/cover.png`](out/cover.png)

## Die Idee

**Trainer Kalle** gründet einen Fußballverein. Das Stadion ist eine Kuhweide mit Maulwurfshügeln, das Tor hat kein Netz,
und die Tribüne ist eine einzelne Bierbank. **Jeder Follower wird ein Fan und bekommt einen Platz auf der Tribüne.**

| Figur | Rolle | Running Gag |
|---|---|---|
| **Kalle** | Trainer mit Schnauzer, Trainingsanzug, Pfeife | Träumt vom ausverkauften Stadion |
| **Berta** | Kuh, Torwart mit Handschuhen | Gehalt: 1 Eimer Gras pro Spiel. Hält nur aus Versehen. |
| **Die Taube** | einziger Fan bisher | sitzt auf der Bierbank |

**Warum es funktionieren kann:**
- Fußball ist in Deutschland das größte Gemeinschaftsthema.
- Die Tribüne füllt sich sichtbar mit jedem Follower.
- Fans identifizieren sich stark mit „ihrem“ Verein, und die Dauerkarte Nr. 001 ist ein starker Kommentar-Anreiz.
- Später möglich: echte Spieltage, Trikot-Abstimmungen, Gegner aus den Kommentaren.

## Stimme

Kalle spricht mit einer KI-Stimme aus **VoxCPM2** (Apache-2.0, kommerziell nutzbar). Die Stimme wurde per Stimm-Design entworfen:
„Mann in den Vierzigern, tiefe, leicht raue Stimme, lebhaft und humorvoll“. Gespeichert ist sie in `voice/kalle_ref.wav`,
damit sie in jeder Folge gleich klingt. Hörproben von drei Kandidaten liegen in `voice/kandidaten/` (A ist die aktuelle).
Soll Kalle anders klingen, tausche einfach `voice/kalle_ref.wav` und `voice/kalle_ref.txt` aus und baue neu.

## Posting-Text

```
Tag 1: Ich habe einen Fußballverein gegründet ⚽ Jeder Follower = 1 Fan auf der Tribüne. Flutlicht, Netz fürs Tor oder was ganz anderes? Ihr entscheidet 👇 #fckuhweide #tag1 #fußball #kreisliga #fyp
```

## Serien-Ideen
- **Tag 2:** Abstimmungsergebnis umsetzen. Die ersten Fan-Namen stehen auf der Bierbank.
- **Tag 3:** Erstes Spiel gegen den SV Matschbach. Berta frisst den Elfmeterpunkt.
- **Tag 4:** Vereinshymne aus den Kommentaren. Trikotfarbe per Abstimmung.
- **Meilensteine:** 100 Fans = zweite Bierbank, 1.000 = Stehplatz-Tribüne, 10.000 = Flutlicht für alle.

## Bauen
Siehe [`../engine/README.md`](../engine/README.md). Kurz:
`python3 engine/build_timeline.py fc-kuhweide-tag1 <stimme.onnx>`, `python3 engine/audio.py fc-kuhweide-tag1`,
`node engine/render.cjs fc-kuhweide-tag1`, danach mit ffmpeg zusammenführen.

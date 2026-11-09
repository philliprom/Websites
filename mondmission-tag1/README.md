# Omas Mondmission – Tag 1 🚀

Idee 2 für das „Tag 1 / 1 Follower = 1 X / ihr entscheidet“-Format. Das Video ist vertikal (1080×1920, 30 fps, ca. 44 s).

**Fertiges Video:** [`out/mondmission_tag1.mp4`](out/mondmission_tag1.mp4) · **Cover:** [`out/cover.png`](out/cover.png)

## Die Idee

**Oma Gisela (78)** will zum Mond. Ihre Rakete hat sie im Schrebergarten aus einer Regentonne gebaut. Die Spitze ist ein
Küchentrichter, der Treibstoff ist Sprudel (Medium). **Jeder Follower bringt die Rakete einen Meter höher.**
Erzählt wird aus Sicht des Enkels („Das ist meine Oma …“). Das ist ein sehr TikTok-typischer Blickwinkel.

| Figur | Rolle | Running Gag |
|---|---|---|
| **Oma Gisela** | Kommandantin, 78, Fliegerbrille, Kittelschürze | Plant den Mondflug im Schrebergarten, Parzelle 17 |
| **Waldi** | Dackel, Kopilot mit Nudelsieb als Helm | Gehalt: 1 Leberwurst am Tag. Bellt bei jedem Countdown. |
| **Gartenzwerg** | einziger Zuschauer | schaut mit Fernglas zu, sagt nie etwas |

**Warum es funktionieren kann:**
- Ein messbares Ziel: 384.400.000 m bis zum Mond.
- Jede Folge zeigt sichtbaren Fortschritt (Höhenmeter).
- Omas sind auf TikTok Sympathieträger.
- Der Dackel ist ein Meme-Garant.

## Posting-Text

```
Tag 1: Meine Oma (78) fliegt zum Mond 🚀 Jeder Follower = 1 Meter höher. Fallschirm, Raumhelm für Waldi oder was ganz anderes? Ihr entscheidet 👇 #omasmondmission #tag1 #oma #dackel #fyp
```

## Serien-Ideen
- **Tag 2:** Abstimmungsergebnis (z. B. Waldis Raumhelm). Erster echter Countdown, und Waldi bellt bei „3“.
- **Tag 3:** Testflug: 1 Meter (= erster Follower), Oma schwebt über dem Kohlbeet.
- **Tag 4:** Der Nachbar aus Parzelle 18 beschwert sich über Sprudel-Abgase.
- **Meilensteine:** 100 m = über der Laube, 1 km = über den Wolken, 10 km = Flughöhe eines Fliegers.

## Bauen
Siehe [`../engine/README.md`](../engine/README.md). Kurz:
`python3 engine/build_timeline.py mondmission-tag1 <stimme.onnx>`, `python3 engine/audio.py mondmission-tag1`,
`node engine/render.cjs mondmission-tag1`, danach mit ffmpeg zusammenführen.

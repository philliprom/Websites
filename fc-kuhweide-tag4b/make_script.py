"""Tag 4b: Die Neuzugänge (zweites Video des Tages). Erzeugt script.json, kader.js und out/beschreibung.txt.
Aufruf: python3 fc-kuhweide-tag4b/make_script.py
Zweck: Neue Zuschauer verstehen in Sekunde 1 das Prinzip („Kommentar = Aufnahme“), Kommentierende finden ihren Namen.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, "kader.json"), encoding="utf-8"))
G = K["gruppen"]
st, ve, sp, ul, pl = G["stab"], G["verein"], G["sponsor"][0], G["ultras"], G["spieler"]
zw = {5: "fünf", 6: "sechs", 7: "sieben", 8: "acht", 9: "neun", 10: "zehn"}
n_sp = zw.get(len(pl), str(len(pl)))
blips = lambda n, a=0.1, step=0.45: [["blip", round(a + i * step, 2)] for i in range(n)]

segments = [
    {"id": "s01", "say": "Ihr kommentiert, ich nehme euch in den Verein auf.", "caps": ["IHR ^KOMMENTIERT,", "ICH NEHME EUCH", "IN DEN ^VEREIN AUF."], "gap": 0.0,
     "sfx": [["stamp", 0.3], ["stamp", 0.75], ["stamp", 1.2]]},
    {"id": "s02", "say": "Das sind die Neuzugänge von heute!", "caps": ["DAS SIND DIE", "^NEUZUGÄNGE VON HEUTE!"], "gap": 0.3,
     "sfx": [["whoosh", -0.05], ["pop", 0.1], ["confetti", 0.2]]},
    {"id": "s03", "say": f"{st[0]['name']} wird Mannschaftsarzt, {st[1]['name']} Torwarttrainer und {st[2]['name']} Standard-Trainer.",
     "caps": [f"^{st[0]['name'].upper()} WIRD ^MANNSCHAFTSARZT,", f"^{st[1]['name'].upper()} ^TORWARTTRAINER", f"UND ^{st[2]['name'].upper()} ^STANDARD-TRAINER."], "gap": 0.35,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["blip", 1.5], ["blip", 2.6]]},
    {"id": "s04", "say": f"{ve[0]['name']} verwaltet die Kasse, {ve[1]['name']} die Eckfahnen. Und wir haben einen Transferberater!",
     "caps": [f"^{ve[0]['name'].upper()} VERWALTET DIE ^KASSE,", f"^{ve[1]['name'].upper()} DIE ^ECKFAHNEN.", "UND WIR HABEN EINEN", "^TRANSFERBERATER!"], "gap": 1.3,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["blip", 1.4], ["blip", 2.6], ["blip", 3.0], ["blip", 3.4], ["blip", 3.8]]},
    {"id": "s05", "say": f"{sp['name']} kriegt endlich seine Bande!", "caps": [f"^{sp['name'].upper()} KRIEGT ENDLICH", "SEINE ^BANDE!"], "gap": 1.6,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["stamp", "e-0.4"], ["cheer", "e-0.3"]]},
    {"id": "s06", "say": f"{ul[0]['name']} wollte Pyro. Er kriegt eine Wunderkerze.", "caps": [f"^{ul[0]['name'].upper()} WOLLTE !PYRO.", "ER KRIEGT EINE", "^WUNDERKERZE."], "gap": 0.6,
     "sfx": [["whoosh", -0.05], ["blip", 0.05], ["blip", 0.5], ["blip", 0.95], ["sparkle", "e-1.0"], ["drum", "e-0.2"]]},
    {"id": "s07", "say": f"Und {n_sp} neue Spieler!", "caps": [f"UND ^{len(pl)} NEUE", "^SPIELER!"], "gap": 1.0,
     "sfx": [["whoosh", -0.05]] + blips(len(pl), 0.05, 0.3)},
    {"id": "s08", "say": "Du willst auch rein? Schreib deine Position in die Kommentare!", "caps": ["DU WILLST AUCH ~REIN?", "SCHREIB DEINE ^POSITION", "IN DIE ^KOMMENTARE!"], "gap": 2.0,
     "sfx": [["whoosh", -0.05], ["pop", 1.0], ["tap", 1.3], ["tap", 1.45], ["tap", 1.6], ["tap", 1.75], ["tap", 1.9], ["ding", "e-0.2"]]},
    {"id": "s09", "say": "Und was mit unserer Kuh los ist, siehst du im letzten Video.", "caps": ["UND WAS MIT UNSERER", "^KUH LOS IST,", "SIEHST DU IM", "^LETZTEN VIDEO."], "gap": 1.3,
     "sfx": [["whoosh", -0.05], ["stamp", 0.4], ["pop", "e+0.2"], ["tap", "e+0.6"], ["ding", "e+0.65"]]},
]
script = {
    "title": "FC Kuhweide – Tag 4: Die Neuzugänge",
    "voice": "voxcpm2", "lead_in": 0.1, "tail": 1.8, "default_gap": 0.1,
    "tts": {"engine": "voxcpm", "voice": "../fc-kuhweide-tag1/voice/kalle_ref.wav", "voice_text": "../fc-kuhweide-tag1/voice/kalle_ref.txt",
            "cfg": 2.0, "steps": 10},
    "music": {"bpm": 128, "inst": "marimba", "clap": 1.8, "ambience": 0.2,
              "chords": [[67, 71, 74, 79], [64, 67, 71, 76], [65, 69, 72, 77], [62, 67, 71, 74]],
              "roots": [43, 40, 41, 43], "arp": [0, 1, 2, 3, 2, 1, 2, 3]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
alle = [x["handle"] for grp in (st, ve, [sp], ul, pl) for x in grp if x["handle"].startswith("@")]
cap = (f"Tag 4, Teil 2: Die Neuzugänge ⚽ Mannschaftsarzt, Torwarttrainer, Sponsor und {len(pl)} neue Spieler – ist dein Name dabei? 👀 "
       f"Du willst auch rein? Schreib deine Position in die Kommentare 👇 #fckuhweide #tag4 #neuzugänge #fußball #kreisliga")
pin = ("📌 So kommst du in den Verein: Schreib deine Wunschposition oder Wunschrolle in die Kommentare ✍️ Die Neuen stehen im nächsten Video 🤝 "
       "Und: Jedes BERTA (hier oder unter Teil 1) holt unsere Kuh einen Schritt zurück 🐄")
gruppen = [" ".join(alle[i:i + 5]) for i in range(0, len(alle), 5)]
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""FC KUHWEIDE – TAG 4b „DIE NEUZUGÄNGE“ · TEXTE ZUM POSTEN
==========================================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTZEIT
Frühestens 4 Stunden nach Teil 1 („Berta ist weg“), z. B. gegen 17:30 Uhr.

OPTIONAL: NEUZUGÄNGE MARKIEREN (TikTok benachrichtigt sie, viele schauen dann rein)
Höchstens 5 Namen pro Kommentar, damit es nicht wie Spam wirkt. Einfach nacheinander als eigene Kommentare posten:
{chr(10).join(gruppen)}
""")
open(os.path.join(HERE, "kader.js"), "w", encoding="utf-8").write("window.KADER = " + json.dumps(K, ensure_ascii=False) + ";\n")
print(f"Tag 4b: {len(segments)} Sätze, {len(alle)} markierbare Neuzugänge")

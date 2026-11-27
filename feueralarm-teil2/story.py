"""DER FEUERALARM · Teil 2 (Zuschauer haben AUTO gewählt).

Noah rennt vor Pohl weg in den Hinterhof, steigt mit Ben in das blaue Auto. Regel 6 (Papas Stimme): falsches Auto.
Auf dem Handy des Fahrers steht „SANDER“. Regel 7: an der Ampel durchs Fenster. Entscheidung: FENSTER oder SITZEN BLEIBEN.

Lehren aus Teil 1 (9.000 Aufrufe, Ø 51 s geschaut, 17,5 % bis zum Ende): kürzer (~90 s), Rückblick ≤ 2,5 s,
Bedrohung ab der ersten Sekunde, alle 5–8 s etwas Neues.
"""

TITLE = "DER FEUERALARM"
PART = "TEIL 2"
INTRO = "TEIL 2 · Ihr habt gewählt: AUTO"

VOICES = {
    "noah": "A 15-year-old German teenage boy, voice recently broken but still young and light, medium pitch, slightly husky, "
            "natural and unpolished.",
    "ben": "A 14-year-old German boy with a bright, high, youthful voice, fast and expressive, a bit cheeky.",
    "sander": "A woman in her mid-forties with a low, smooth, controlled voice, polite on the surface but cold and menacing, "
              "speaking slowly and precisely like a strict teacher.",
    "pohl": "A man around sixty, the school caretaker, with a deep, raspy, warm and worn voice.",
    "papa": "A German man in his mid-forties with a warm, deep, slightly husky voice. He speaks quietly, slowly and "
            "urgently, like a father leaving a secret message for his son.",
    "fahrer": "A German man in his late thirties with a calm, deep, smooth voice. He sounds friendly and reassuring at first, "
              "but there is something cold and controlled underneath.",
}

LINES = [
    # Rückblick: Regel 5 als Banner, Papas Stimme
    dict(id="r5", who="papa", kind="regel", n=5,
         sub="Ich bin's. Papa. Geh NICHT mit Pohl. Hinterhof. Blaues Auto.",
         say="Hinterhof. Blaues Auto.", rot=[], emo="He speaks quietly and urgently."),
    # Keller: Noah rennt los
    dict(id="k01", who="pohl", sub="Noah! Bleib hier! Das ist eine Falle!", rot=["Falle"],
         emo="He shouts after him, desperate and worried."),
    dict(id="k02", who="ben", sub="Noah, warte! Wo willst du hin?", rot=[],
         emo="He calls out, out of breath, running after him."),
    dict(id="k03", who="noah", sub="Zum Auto. Wenn das wirklich Papa ist…", rot=["Papa"],
         emo="He answers determined but shaky, out of breath."),
    # Hinterhof, Regen, blaues Auto mit laufendem Motor
    dict(id="k04", who="ben", sub="Da! Ein blaues Auto. Der Motor läuft.", rot=["blaues Auto"],
         emo="He whispers tensely."),
    dict(id="k05", who="fahrer", sub="Noah? Dein Vater schickt mich. Steig ein. Schnell.", rot=["Dein Vater"],
         emo="He speaks calmly and friendly, but in a hurry."),
    dict(id="k06", who="ben", sub="Woher kennt der Typ deinen Namen?", rot=["deinen Namen"],
         emo="He whispers suspiciously."),
    dict(id="k07", who="noah", sub="Wo ist mein Vater?", rot=[],
         emo="He asks tense and hopeful."),
    dict(id="k08", who="fahrer", sub="Er wartet auf dich. Ich bring dich hin.", rot=[],
         emo="He answers smoothly and reassuring."),
    dict(id="k09", who="sander", sub="Noah?! Bleib stehen!", rot=["Bleib stehen"],
         emo="She shouts from far away, angry and sharp."),
    dict(id="k10", who="ben", sub="Sie kommt! Los, rein da!", rot=["Sie kommt"],
         emo="He shouts in panic."),
    # Im Auto (Rückbank), Fahrt durch die Stadt
    dict(id="k11", who="fahrer", sub="Anschnallen. Und Kopf runter.", rot=[],
         emo="He gives a calm, firm order."),
    dict(id="k12", who="ben", sub="Und Lina? Die ist noch bei ihr!", rot=["Lina"],
         emo="He whispers, worried."),
    dict(id="k13", who="noah", sub="Papa holt sie. Ganz sicher.", rot=[],
         emo="He whispers, trying to sound sure."),
    dict(id="r6", who="papa", kind="regel", n=6,
         sub="Falsches Auto. Ich warte hinter der Turnhalle. Steig AUS.",
         say="Falsches Auto. Ich warte hinter der Turnhalle. Steig aus.", rot=["Falsches Auto"],
         emo="He speaks quietly, alarmed and urgent."),
    dict(id="k14", who="noah", sub="Falsches Auto…?", rot=["Falsches Auto"],
         emo="He whispers in shock."),
    dict(id="k15", who="ben", sub="Noah… auf seinem Handy steht Sander!", rot=["Sander"],
         emo="He whispers in panic."),
    dict(id="k16", who="fahrer", sub="Gibt's ein Problem da hinten?", rot=[],
         emo="He asks coldly and suspiciously."),
    dict(id="k17", who="noah", sub="Nein. Mir ist nur schlecht.", rot=[],
         emo="He tries hard to sound calm."),
    dict(id="r7", who="papa", kind="regel", n=7,
         sub="An der Ampel. Fenster hinten rechts geht auf. Raus, wenn es grün wird.",
         say="An der Ampel. Fenster hinten rechts geht auf. Raus, wenn es grün wird.", rot=["Ampel"],
         emo="He speaks quietly and urgently, very clearly."),
    dict(id="k18", who="fahrer", sub="Finger weg vom Fenster, Noah.", rot=["Finger weg"],
         emo="He says it slowly and menacingly."),
    dict(id="k19", who="ben", sub="Noah… was machen wir?", rot=["was machen wir"],
         emo="He whispers, scared."),
]

for _l in LINES:
    _l.setdefault("kind", "zeile")
    _l.setdefault("say", _l["sub"].replace("…?", "?").replace("…!", "!").replace("… ", ", ").replace("…", ","))

ENDKARTE = dict(frage="WAS TUST DU?",
                a=("FENSTER", "Regel 7 folgen"),
                b=("SITZEN BLEIBEN", "abwarten, wohin er fährt"),
                teil2="Teil 3 entscheidet ihr.")

if __name__ == "__main__":
    for l in LINES:
        print(f'{l["id"]:4} {l["who"]:8} {l["say"]}')
    print(len(LINES), "Zeilen,", sum(len(l["say"].split()) for l in LINES), "Wörter")

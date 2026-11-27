"""DER FEUERALARM · Teil 1 – eigenes POV-Schuldrama im Format „unbekannte Nummer schickt Regeln“.

Format wie im Vorbild (POV, Dialog statt Erzähler, Regeln als Handy-Einblendung, Entscheidungskarte am Ende),
Geschichte, Figuren und Wendung sind eigene.

Jede Zeile: id, Sprecher, Untertitel (sub), Sprechtext (say, Zahlen ausgeschrieben), Emotion (Englisch für Qwen VoiceDesign),
rot = Schlüsselwörter, die im Untertitel rot erscheinen.
"""

TITLE = "DER FEUERALARM"
PART = "TEIL 1"

# Stimmen: Grundbeschreibung je Figur (Qwen3-TTS VoiceDesign versteht Englisch am besten)
VOICES = {
    "noah": "A 15-year-old German teenage boy, voice recently broken but still young and light, medium pitch, slightly husky, "
            "natural and unpolished.",
    "ben": "A 14-year-old German boy with a bright, high, youthful voice, fast and expressive, a bit cheeky.",
    "lina": "A 15-year-old German teenage girl with a clear, confident, slightly sassy voice.",
    "sander": "A woman in her mid-forties with a low, smooth, controlled voice, polite on the surface but cold and menacing, "
              "speaking slowly and precisely like a strict teacher.",
    "pohl": "A man around sixty, the school caretaker, with a deep, raspy, warm and worn voice.",
    "durchsage": "A middle-aged male headmaster with an authoritative, loud voice making an urgent announcement.",
    "papa": "A German man in his mid-forties with a warm, deep, slightly husky voice. He speaks quietly, slowly and "
            "urgently, like a father leaving a secret message for his son.",
}

LINES = [
    # Szene 1: Klassenzimmer 204, Feueralarm klingelt, Frau Sander schließt ab
    dict(id="l01", who="ben", sub="Noah… sie hat uns eingeschlossen.", rot=["eingeschlossen"],
         emo="He whispers urgently in panic, voice trembling, barely audible."),
    dict(id="l02", who="sander", sub="Alle bleiben sitzen. Das ist nur eine Übung.", rot=["Übung"],
         emo="She speaks calmly and coldly, in full control, no emotion."),
    dict(id="l03", who="lina", sub="Bei Feueralarm müssen wir raus! Das weiß jeder!", rot=["raus"],
         emo="She protests loudly, indignant and upset."),
    dict(id="l04", who="sander", sub="Hinsetzen, Lina.", rot=[],
         emo="She gives a sharp, quiet, threatening command."),
    dict(id="r1", who="noah", kind="regel", n=1,
         sub="Das ist keine Übung. Und sie ist keine Lehrerin. Tu so, als glaubst du ihr.",
         say="Regel eins. Das ist keine Übung. Und sie ist keine Lehrerin. Tu so, als glaubst du ihr.",
         rot=["keine Lehrerin"], emo="He reads a text message quietly to himself, tense and hushed."),
    dict(id="l05", who="noah", sub="Wer schreibt mir das?", rot=[],
         emo="He whispers, confused and scared."),
    dict(id="l06", who="ben", sub="Unbekannte Nummer? Alter… zeig her.", rot=["Unbekannte Nummer"],
         emo="He whispers fast, nervous and curious."),
    dict(id="l07", who="sander", sub="Was gibt's da hinten zu flüstern?", rot=[],
         emo="She asks slowly and suspiciously, coming closer, cold and sharp."),
    dict(id="l08", who="noah", sub="Nichts. Ben hat nur Angst vor dem Alarm.", rot=[],
         emo="He tries hard to sound calm and casual, but he is nervous."),
    dict(id="l09", who="sander", sub="Musst du nicht, Ben. Hier drin passiert euch nichts.", rot=["Hier drin"],
         emo="She speaks with fake friendliness, sweet but creepy, a cold smile in her voice."),
    # Blick aus dem Fenster: ganze Schule auf dem Hof
    dict(id="l10", who="lina", sub="Guckt mal raus. Die ganze Schule steht draußen. Nur wir nicht.", rot=["Nur wir nicht"],
         emo="She whispers, worried and suspicious."),
    dict(id="l11", who="ben", sub="Warum nur wir?", rot=[],
         emo="He whispers, scared."),
    dict(id="l12", who="sander", sub="Ich mache kurz Anwesenheit. Wer aufgerufen wird, steht auf.", rot=["Anwesenheit"],
         emo="She speaks in a businesslike, cool, controlled tone."),
    dict(id="r2", who="noah", kind="regel", n=2,
         sub="Wenn sie deinen Namen sagt: Bleib sitzen. Sie sucht DICH.",
         say="Regel zwei. Wenn sie deinen Namen sagt: Bleib sitzen. Sie sucht dich.",
         rot=["DICH"], emo="He reads a text message quietly to himself, his voice getting scared."),
    dict(id="l13", who="sander", sub="Noah Berger?", rot=["Noah Berger"],
         emo="She calls out a name slowly, cold, lurking."),
    dict(id="l14", who="sander", sub="Noah Berger. Ist der heute nicht da?", rot=[],
         emo="She repeats the name louder, impatient and suspicious."),
    dict(id="l15", who="ben", sub="Der ist krank. Seit Montag.", rot=["krank"],
         emo="He answers quickly, nervous, trying to lie convincingly."),
    dict(id="l16", who="sander", sub="Krank. Soso.", say="Krank. So, so.", rot=[],
         emo="She says it slowly and drawn out, deeply suspicious, menacing."),
    # Durchsage, Sander dreht den Lautsprecher ab
    dict(id="l17", who="durchsage", kind="durchsage", sub="Raum 204! Warum ist eure Tür zu? Sofort raus zum Sammelplatz!",
         say="Raum zwei null vier! Warum ist eure Tür zu? Sofort raus zum Sammelplatz!", rot=["Sofort raus"],
         emo="He shouts urgently and angrily into a microphone."),
    dict(id="l18", who="lina", sub="Sie hat die Durchsage abgedreht!", rot=["abgedreht"],
         emo="She gasps in shock and disbelief, whispering loudly."),
    dict(id="r3", who="noah", kind="regel", n=3,
         sub="Die Tür hinter dem Pult ist offen. Geh, wenn sie telefoniert.",
         say="Regel drei. Die Tür hinter dem Pult ist offen. Geh, wenn sie telefoniert.",
         rot=["Tür hinter dem Pult"], emo="He reads a text message in a hushed, tense whisper."),
    dict(id="l19", who="sander", sub="Er ist hier. Ich weiß nur noch nicht, welcher. … Fünf Minuten.", rot=["welcher"],
         say="Er ist hier. Ich weiß nur noch nicht, welcher. Fünf Minuten.",
         emo="She speaks quietly into a phone, cold and secretive."),
    dict(id="l20", who="ben", sub="Welcher?! Die weiß gar nicht, wie du aussiehst!", rot=["wie du aussiehst"],
         emo="He whispers in shock and panic, fast."),
    dict(id="l21", who="noah", sub="Komm. Jetzt.", rot=[],
         emo="He whispers, determined and urgent."),
    dict(id="l22", who="lina", sub="Frau Sander! Mir ist voll schlecht!", rot=[],
         emo="She calls out loudly, acting dramatically sick to create a distraction."),
    # Flur, Alarmlicht
    dict(id="r4", who="noah", kind="regel", n=4,
         sub="Nicht die Haupttreppe. Keller, Raum K3. Schließ hinter dir ab.",
         say="Regel vier. Nicht die Haupttreppe. Keller, Raum Ka drei. Schließ hinter dir ab.",
         rot=["Keller, Raum K3"], emo="He reads a text message out of breath, while running, tense."),
    dict(id="l23", who="ben", sub="In den Keller? Da unten ist doch niemand!", rot=[],
         emo="He is out of breath and panicking while running."),
    dict(id="l24", who="sander", sub="Noah?! Ich weiß, dass du das bist!", rot=["Ich weiß"],
         emo="She shouts angrily from far away, sharp and threatening."),
    dict(id="l25", who="ben", sub="Lauf! Lauf!", say="Lauf, lauf!", rot=["Lauf"],
         emo="He shouts one single word loudly and urgently, clearly articulated."),
    # Keller K3
    dict(id="l26", who="pohl", sub="Ihr? Was macht ihr denn hier unten?", rot=[],
         emo="He is startled and surprised, gruff."),
    dict(id="l27", who="noah", sub="Da oben ist eine Frau. Die sucht mich. Und jemand schreibt mir, was ich tun soll.",
         rot=["sucht mich"], emo="He is out of breath and desperate, speaking fast."),
    dict(id="l28", who="pohl", sub="Ich weiß. Ich hab den Alarm gedrückt, als sie reinkam. Zeig mal her.", rot=["Alarm gedrückt"],
         emo="He speaks quietly and seriously, calm and protective."),
    dict(id="r5", who="noah", kind="regel", n=5,
         sub="Ich bin's. Papa. Geh NICHT mit Pohl. Hinterhof. Blaues Auto.",
         say="Regel fünf.", rot=["Papa", "NICHT"], emo="He reads quietly and slowly, tense, almost whispering."),
    dict(id="r5b", who="papa", kind="regel", n=5,
         sub="Ich bin's. Papa. Geh NICHT mit Pohl. Hinterhof. Blaues Auto.",
         say="Ich bin's. Papa. Geh nicht mit Pohl. Hinterhof. Blaues Auto.", rot=[],
         emo="He speaks quietly and urgently, warm but serious, pausing briefly between the short sentences."),
    dict(id="l29", who="noah", sub="Papa…?", rot=["Papa"],
         emo="He whispers, stunned, his voice breaking, close to tears."),
    dict(id="l30", who="pohl", sub="Noah… das kann nicht sein. Ich war auf der Beerdigung deines Vaters.",
         rot=["Beerdigung"], emo="He speaks quietly and sadly, gently, shaken."),
    dict(id="l31", who="ben", sub="Noah… wem glaubst du?", rot=["wem glaubst du"],
         emo="He whispers, scared and serious."),
]

for _l in LINES:
    _l.setdefault("kind", "zeile")
    _l.setdefault("say", _l["sub"].replace("…?", "?").replace("…!", "!").replace("… ", ", ").replace("…", ","))

ENDKARTE = dict(frage="WEM GLAUBST DU?",
                a=("BLAUES AUTO", "der Nummer glauben"),
                b=("BEI POHL BLEIBEN", "dem Hausmeister glauben"),
                teil2="Teil 2 entscheidet ihr.")

if __name__ == "__main__":
    import json
    for l in LINES:
        print(f'{l["id"]:4} {l["who"]:9} {l["say"]}')
    print(len(LINES), "Zeilen,", sum(len(l["say"].split()) for l in LINES), "Wörter")

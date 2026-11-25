"""Nachtschicht – Teil 2, beide Fassungen (die Abstimmung unter Teil 1 entscheidet, welche gepostet wird).
  A  „aufgemacht“:       draußen niemand, der Chef hat nie geschrieben, nasse Fußspuren bis hinter die Kasse, Licht aus.
  B  „nicht aufgemacht“: Klopfen hört auf, Kamera 2 (Lager): die Hintertür steht offen, Regel 5 auf der Rückseite.
Erzeugt a/script.json und b/script.json (Projektordner für engine/build_timeline.py) und out/beschreibung_<a|b>.txt.
Jeder Satz hat eine Spannungsstufe 0–3 („spannung“): emotion.py hebt die Stimme danach an (wie Hörprobe 3, etwas mehr),
sound.py macht spannende Sätze lauter.
Captions: ^ = rot hervorgehoben.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# (id, Text, Untertitel-Zeilen, Pause davor, Spannung)
A = [
    ("a01", "Die Spuren enden direkt hinter dir.", ["DIE SPUREN ENDEN", "DIREKT ^HINTER ^DIR."], 0.0, 2),
    ("a02", "Ihr habt entschieden.", ["IHR HABT ^ENTSCHIEDEN."], 0.9, 0),
    ("a03", "Du machst auf.", ["DU MACHST ^AUF."], 0.3, 0),
    ("a04", "Du drehst den Schlüssel um. Die Tür geht auf.", ["DU DREHST DEN", "^SCHLÜSSEL UM.", "DIE TÜR GEHT ^AUF."], 0.6, 1),
    ("a05", "Kalte Luft. Regen. Und draußen ist niemand.", ["KALTE LUFT. REGEN.", "UND DRAUSSEN", "IST ^NIEMAND."], 0.7, 1),
    ("a06", "Er stand doch eben noch hier.", ["ER STAND DOCH", "EBEN NOCH ^HIER."], 0.5, 1),
    ("a07", "Du schließt wieder ab. Dein Handy vibriert.", ["DU SCHLIESST WIEDER AB.", "DEIN ^HANDY VIBRIERT."], 0.8, 1),
    ("a08", "Wer hat dir gesagt, dass du aufmachen sollst?", ["„WER HAT DIR GESAGT,", "DASS DU ^AUFMACHEN", "^SOLLST?“"], 0.5, 2),
    ("a09", "Du scrollst nach oben. Seine Nachricht von vorhin ist weg.",
     ["DU SCROLLST NACH OBEN.", "SEINE NACHRICHT", "VON VORHIN IST ^WEG."], 0.7, 2),
    ("a10", "Dein Chef hat dir nie geschrieben.", ["DEIN CHEF HAT DIR", "^NIE GESCHRIEBEN."], 0.5, 2),
    ("a11", "Du schaust auf Kamera eins.", ["DU SCHAUST", "AUF ^KAMERA ^1."], 0.9, 1),
    ("a12", "Auf dem Boden sind nasse Fußspuren. Sie kommen von der Tür.",
     ["AUF DEM BODEN:", "NASSE ^FUSSSPUREN.", "SIE KOMMEN VON DER ^TÜR."], 0.4, 2),
    ("a13", "Du warst nicht draußen.", ["DU WARST", "^NICHT DRAUSSEN."], 0.5, 2),
    ("a14", "Sie gehen an der Theke vorbei. Bis hinter die Kasse.", ["SIE GEHEN AN DER", "THEKE VORBEI.", "BIS HINTER DIE ^KASSE."], 0.4, 3),
    ("a15", "Genau dorthin, wo du stehst.", ["GENAU DORTHIN,", "WO ^DU ^STEHST."], 0.4, 3),
    ("a16", "Das Licht geht aus.", ["DAS LICHT", "GEHT ^AUS."], 0.7, 2),
    ("a17", "Und direkt hinter dir atmet jemand.", ["UND DIREKT ^HINTER ^DIR", "ATMET ^JEMAND."], 2.2, 3),
    ("a18", "Drehst du dich um? Oder rennst du raus in den Regen?",
     ["DREHST DU DICH ^UM?", "ODER RENNST DU", "RAUS IN DEN ^REGEN?"], 1.0, 1),
    ("a19", "Schreib A oder B. Die Mehrheit entscheidet über Teil drei.",
     ["SCHREIB ^A ODER ^B.", "DIE MEHRHEIT ENTSCHEIDET", "ÜBER ^TEIL ^3."], 0.4, 0),
]
B = [
    ("b01", "Die Hintertür war abgeschlossen. Da bist du dir ganz sicher.",
     ["DIE HINTERTÜR WAR", "^ABGESCHLOSSEN.", "DA BIST DU DIR", "GANZ ^SICHER."], 0.0, 2),
    ("b02", "Ihr habt entschieden.", ["IHR HABT ^ENTSCHIEDEN."], 0.9, 0),
    ("b03", "Du machst nicht auf.", ["DU MACHST", "^NICHT AUF."], 0.3, 0),
    ("b04", "Du bleibst hinter der Theke und rührst dich nicht.", ["DU BLEIBST", "HINTER DER THEKE", "UND RÜHRST DICH ^NICHT."], 0.6, 1),
    ("b05", "Er klopft noch einmal. Dreimal.", ["ER KLOPFT NOCH EINMAL.", "^DREIMAL."], 0.6, 1),
    ("b06", "Dein Handy vibriert. Wieder dein Chef.", ["DEIN ^HANDY VIBRIERT.", "WIEDER DEIN ^CHEF."], 2.4, 1),
    ("b07", "Er friert. Warum machst du nicht auf?", ["„ER ^FRIERT.", "WARUM MACHST DU", "^NICHT AUF?“"], 0.5, 2),
    ("b08", "Dann hört das Klopfen auf.", ["DANN HÖRT DAS", "KLOPFEN ^AUF."], 0.9, 1),
    ("b09", "Du schaust auf Kamera eins. Er ist weg.", ["DU SCHAUST AUF", "^KAMERA ^1.", "ER IST ^WEG."], 0.6, 1),
    ("b10", "Kamera drei: niemand.", ["KAMERA 3:", "^NIEMAND."], 0.6, 1),
    ("b11", "Und dann siehst du Kamera zwei. Das Lager.", ["UND DANN SIEHST DU", "^KAMERA ^2.", "DAS LAGER."], 0.8, 2),
    ("b12", "Die Hintertür steht offen.", ["DIE HINTERTÜR", "STEHT ^OFFEN."], 0.5, 3),
    ("b13", "Du hast sie um Mitternacht selbst abgeschlossen.", ["DU HAST SIE UM MITTERNACHT", "^SELBST ABGESCHLOSSEN."], 0.5, 2),
    ("b14", "Du drehst den Zettel um. Auf der Rückseite steht noch eine Regel.",
     ["DU DREHST DEN ^ZETTEL UM.", "AUF DER RÜCKSEITE", "STEHT NOCH EINE ^REGEL."], 0.8, 2),
    ("b15", "Regel fünf: Steht die Hintertür offen, ist er schon drin.",
     ["REGEL 5:", "STEHT DIE HINTERTÜR OFFEN,", "IST ER ^SCHON ^DRIN."], 0.5, 3),
    ("b16", "Versteck dich.", ["^VERSTECK ^DICH."], 0.5, 3),
    ("b17", "Versteckst du dich im Kühlraum? Oder rennst du raus in den Regen?",
     ["VERSTECKST DU DICH", "IM ^KÜHLRAUM?", "ODER RENNST DU", "RAUS IN DEN ^REGEN?"], 1.0, 1),
    ("b18", "Schreib A oder B. Die Mehrheit entscheidet über Teil drei.",
     ["SCHREIB ^A ODER ^B.", "DIE MEHRHEIT ENTSCHEIDET", "ÜBER ^TEIL ^3."], 0.4, 0),
]
TTS = {"engine": "qwen", "voice": "../../nachtschicht-teil1/voice/horror.wav", "voice_text": "../../nachtschicht-teil1/voice/horror.txt",
       "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.7, "max_pause": 0.32}
for key, S, title in (("a", A, "aufgemacht"), ("b", B, "nicht aufgemacht")):
    segs = [{"id": i, "say": say, "caps": caps, "gap": gap, "sfx": [], "spannung": sp} for i, say, caps, gap, sp in S]
    script = {"title": f"Nachtschicht – Teil 2 ({title})", "lead_in": 0.6, "tail": 2.6, "default_gap": 0.3, "tts": TTS, "segments": segs}
    open(os.path.join(HERE, key, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")
    print(f"{key}/script.json: {len(segs)} Sätze, {sum(len(s['say']) for s in segs)} Zeichen")

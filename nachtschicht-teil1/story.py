"""Nachtschicht – Teil 1. Interaktive Horror-Folge im Überwachungskamera-Stil („Du entscheidest“).
Format angelehnt an interaktive Horror-Serien (Ich-/Du-Perspektive, Abstimmung per Kommentar), Geschichte eigen.

Erzeugt script.json (Erzählerstimme: entworfene Horror-Stimme 3, ab 25.11.; vorher Thorsten A) und out/beschreibung.txt.
Danach: engine/build_timeline.py (Stimme) → shots.py (Bildfolgen planen) → scene.py (Blender) → sound.py → assemble.py.

Einstellungen (SH = Einstellung im Schnitt):
  SH0 Rückblende-Haken: CAM 01, Gestalt an der Tür, Klopfen      s01
  SH1 Schwarz, Schreibmaschine „02:39“                             s02
  SH2 CAM 01 Laden leer                                            s03–s04
  SH3 Regel-Zettel (Sicht der Kassiererin)                         s05–s10
  SH4 CAM 01 Licht flackert                                        s11
  SH5 CAM 03 Zapfsäulen: Gestalt im Regen → Flackern → weg         s12–s15
  SH6 CAM 01 Stromausfall → Gestalt an der Tür → klopft dreimal    Pause + s16
  SH7 Handy: Nachricht vom Chef                                    s17–s18
  SH8 Entscheidung A/B                                             s19–s21
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = [
    ("s01", "Würdest du aufmachen?", ["WÜRDEST DU ^AUFMACHEN?"], 0.0),
    ("s02", "Acht Minuten vorher.", ["ACHT MINUTEN VORHER."], 0.7),
    ("s03", "Du hast Nachtschicht an einer Tankstelle. Irgendwo an der Landstraße. Du bist allein.",
     ["DU HAST ^NACHTSCHICHT", "AN EINER TANKSTELLE.", "IRGENDWO AN DER LANDSTRASSE.", "DU BIST ^ALLEIN."], 0.5),
    ("s04", "Draußen regnet es seit Stunden.", ["DRAUSSEN REGNET ES", "SEIT STUNDEN."], 0.2),
    ("s05", "Dein Chef hat dir einen Zettel dagelassen.", ["DEIN CHEF HAT DIR", "EINEN ^ZETTEL DAGELASSEN."], 0.5),
    ("s06", "Regel eins: Ab zwei Uhr bleibt die Tür zu.", ["REGEL 1:", "AB 2 UHR BLEIBT", "DIE TÜR ^ZU."], 0.3),
    ("s07", "Regel zwei: Flackert das Licht, schau auf Kamera drei.", ["REGEL 2:", "FLACKERT DAS LICHT,", "SCHAU AUF ^KAMERA ^3."], 0.25),
    ("s08", "Regel drei: Steht draußen jemand still im Regen, sprich ihn nicht an.",
     ["REGEL 3:", "STEHT DRAUSSEN JEMAND", "STILL IM REGEN,", "SPRICH IHN ^NICHT AN."], 0.25),
    ("s09", "Regel vier: Er klopft dreimal. Mach niemals auf.", ["REGEL 4:", "ER KLOPFT ^DREIMAL.", "MACH ^NIEMALS AUF."], 0.25),
    ("s10", "Darunter, mit rotem Stift: Egal, wer es sagt.", ["DARUNTER, MIT ROTEM STIFT:", "„^EGAL, ^WER ^ES ^SAGT.“"], 0.35),
    ("s11", "Zwei Uhr vierundvierzig. Das Licht flackert.", ["2:44 UHR.", "DAS LICHT ^FLACKERT."], 0.6),
    ("s12", "Du schaust auf Kamera drei.", ["DU SCHAUST", "AUF ^KAMERA ^3."], 0.3),
    ("s13", "Zwischen den Zapfsäulen steht jemand. Im Regen. Er bewegt sich nicht.",
     ["ZWISCHEN DEN ZAPFSÄULEN", "STEHT ^JEMAND.", "IM REGEN.", "ER BEWEGT SICH ^NICHT."], 0.5),
    ("s14", "Das Licht flackert wieder.", ["DAS LICHT", "FLACKERT WIEDER."], 0.4),
    ("s15", "Er ist weg.", ["ER IST ^WEG."], 0.7),
    ("s16", "Er klopft dreimal. Genau wie auf dem Zettel.", ["ER KLOPFT ^DREIMAL.", "GENAU WIE AUF DEM ZETTEL."], 4.5),
    ("s17", "Dann vibriert dein Handy. Eine Nachricht von deinem Chef.",
     ["DANN VIBRIERT DEIN ^HANDY.", "EINE NACHRICHT", "VON DEINEM ^CHEF."], 0.6),
    ("s18", "Mach die Tür auf. Sofort.", ["„MACH DIE TÜR AUF.", "^SOFORT.“"], 0.35),
    ("s19", "Die Regeln sagen: niemals. Dein Chef sagt: sofort.", ["DIE REGELN SAGEN: ^NIEMALS.", "DEIN CHEF SAGT: ^SOFORT."], 0.6),
    ("s20", "Was machst du? Schreib A oder B.", ["WAS MACHST DU?", "SCHREIB ^A ODER ^B."], 0.4),
    ("s21", "Die Mehrheit entscheidet über Teil zwei.", ["DIE MEHRHEIT ENTSCHEIDET", "ÜBER ^TEIL ^2."], 0.3),
]
segments = [{"id": i, "say": say, "caps": caps, "gap": gap, "sfx": []} for i, say, caps, gap in S]
script = {
    "title": "Nachtschicht – Teil 1", "voice": "qwen3-tts (Klon der entworfenen Horror-Stimme 3 „tief, langsam“, Pausen gekürzt)",
    "lead_in": 0.9, "tail": 2.4, "default_gap": 0.3,
    "tts": {"engine": "qwen", "voice": "voice/horror.wav", "voice_text": "voice/horror.txt",
            "tries": 3, "max_wer": 0.1, "candidates": 3, "temperature": 0.7, "max_pause": 0.32},
    "music": {"bpm": 60, "inst": "vibes", "clap": 0.0, "ambience": 0.0, "chords": [[45, 48, 52]], "roots": [33], "arp": [0]},
    "segments": segments,
}
open(os.path.join(HERE, "script.json"), "w", encoding="utf-8").write(json.dumps(script, ensure_ascii=False, indent=2) + "\n")

cap = ("NACHTSCHICHT · Teil 1 🌧️🚪 Allein an der Tankstelle, 4 Regeln vom Chef … und dann klopft es dreimal. "
       "Würdest du aufmachen? Du entscheidest: A oder B 👇 #horror #gruselgeschichte #creepy #nachtschicht #fyp")
pin = ("📌 DU ENTSCHEIDEST: A = Aufmachen (der Chef sagt sofort) · B = Nicht aufmachen (Regel 4: niemals). "
       "Die Mehrheit der Kommentare entscheidet, wie Teil 2 weitergeht. Folge, damit du ihn nicht verpasst.")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "beschreibung.txt"), "w", encoding="utf-8").write(f"""NACHTSCHICHT – TEIL 1 · TEXTE ZUM POSTEN
=========================================

BESCHREIBUNG (Caption):
{cap}

ERSTER KOMMENTAR (selbst posten und anpinnen):
{pin}

TITELBILD
Datei: titelbild.png

POSTEN
- Am besten abends/nachts (20–23 Uhr): Horror wird nachts geschaut (auch bei der Vorlage).
- Beim Posten „KI-generierte Inhalte“ einschalten (Erzählerstimme ist ein KI-Klon der freien Thorsten-Voice-Stimme,
  Bilder sind am Computer erzeugt).
- Kanal-Vorschlag (Monsterdöner-Konto umbauen): Name „Nachtschicht – Du entscheidest“,
  Bio: „Horror-Serie zum Mitentscheiden 🌧️🚪 Du bist allein in der Nachtschicht. Kommentiere A oder B – die Mehrheit
  bestimmt, wie es weitergeht.“
""")
print(len(segments), "Sätze")

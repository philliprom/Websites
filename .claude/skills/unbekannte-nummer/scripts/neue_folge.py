"""Neue Folge im Format „Unbekannte Nummer“ anlegen (Vorlage: Der Feueralarm, Teil 1, funktionierender Gesamtablauf).

  python3 neue_folge.py <ziel-ordner> [--titel "DIE KLASSENFAHRT"] [--teil "TEIL 1"]

Kopiert alle Skripte, Schriften und das Beispiel (Skript, Einstellungen, Sets) in den Ordner. Danach Geschichte, Sets,
Einstellungen und Ton nach references/produktion.md anpassen. Für einen Teil 2 derselben Geschichte genauso anlegen und
Figuren/Sets weiterverwenden.
"""
import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VORLAGE = os.path.join(HERE, "..", "assets", "vorlage")

README = """# {titel} · {teil}

Folge im Format „Unbekannte Nummer“ (Skill `unbekannte-nummer`). Vorlage: Der Feueralarm, Teil 1.

## Geschichte
(Kurzfassung, Figuren, Regeln 1–5, Wendung, Entscheidung A/B)

## Stand
- [ ] story.py (Zeilen, Stimmen, Endkarte)       - [ ] Sets/Texturen        - [ ] shots.py
- [ ] Stimmen + Aussprache-Prüfung (voices*.py)   - [ ] timeline.py (Pausen) - [ ] Testbilder aller Einstellungen
- [ ] Rendern                                     - [ ] sound.py            - [ ] assemble.py + Endmix-Prüfung
- [ ] Titelbild, Beschreibung, angepinnter Kommentar
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ziel")
    ap.add_argument("--titel", default=None)
    ap.add_argument("--teil", default=None)
    a = ap.parse_args()
    ziel = os.path.abspath(a.ziel)
    if os.path.exists(ziel) and os.listdir(ziel):
        sys.exit(f"{ziel} existiert schon und ist nicht leer")
    shutil.copytree(VORLAGE, ziel, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
    for d in ("out", "build", "tests"):
        os.makedirs(os.path.join(ziel, d), exist_ok=True)
    open(os.path.join(ziel, ".gitignore"), "w").write("build/\nout/*.mp4\n*.log\n__pycache__/\n")
    st = os.path.join(ziel, "story.py")
    s = open(st, encoding="utf-8").read()
    if a.titel:
        s = re.sub(r'^TITLE = ".*"$', f'TITLE = "{a.titel}"', s, flags=re.M)
    if a.teil:
        s = re.sub(r'^PART = ".*"$', f'PART = "{a.teil}"', s, flags=re.M)
    open(st, "w", encoding="utf-8").write(s)
    titel = a.titel or "NEUE FOLGE"
    open(os.path.join(ziel, "README.md"), "w", encoding="utf-8").write(README.format(titel=titel, teil=a.teil or "TEIL 1"))
    print(f"Angelegt: {ziel}")
    print("Als Nächstes: story.py neu schreiben (Beispiel ist der Feueralarm), dann references/produktion.md Schritt für Schritt.")


if __name__ == "__main__":
    main()

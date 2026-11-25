"""Behält bereits gerenderte Kamerabilder, die sich durch eine neue Zeitplanung nicht ändern, und löscht den Rest.
Ein Bild bleibt gleich, solange vor ihm in alter UND neuer Planung noch kein Ereignis liegt (Regen hängt nur von der
Bildnummer ab). Aufruf (nach shots.py):  python3 nachtschicht-teil1/reuse.py build/shots_alt.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
old = json.load(open(os.path.join(HERE, sys.argv[1]) if not os.path.isabs(sys.argv[1]) else sys.argv[1]))
new = json.load(open(os.path.join(BUILD, "shots.json")))


def first_event(c):
    ev = list(c.get("dips", [])) + list(c.get("flick5", [])) + list(c.get("canopy_off", []))
    if c.get("blackout"):
        ev.append(c["blackout"][0])
    if c.get("jump"):
        ev.append(c["jump"])
    if c.get("fig_out"):
        ev.append(c["fig_out"])
    return min(ev) if ev else c["frames"] + 1


for shot in ("r1", "r2", "r3"):
    keep = min(first_event(old[shot]), first_event(new[shot]))
    d = os.path.join(BUILD, shot)
    removed = 0
    for f in sorted(os.listdir(d)):
        if f.endswith(".png") and f[:4].isdigit() and int(f[:4]) >= keep:
            os.remove(os.path.join(d, f))
            removed += 1
    print(f"{shot}: behalte Bilder 1–{keep - 1}, gelöscht {removed}, neu zu rendern {new[shot]['frames'] - (keep - 1)}")

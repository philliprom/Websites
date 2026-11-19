#!/usr/bin/env python3
"""Top-Clips eines oder mehrerer Streamer über die offizielle Twitch-Schnittstelle (Helix „Get Clips“).

  python3 clips/twitch_top.py [--stunden 48] [--min-alter 12] [--spiel "Grand Theft Auto VI"] [--login papaplatte ...]

Ohne --login werden alle Streamer aus clips/streamers.json genommen. Ergebnis: Liste nach Aufrufen sortiert
(Titel, Aufrufe, Länge, Alter, Link) in clips/out/topclips_<datum>.md und .json.

Zugang (kostenlos): Twitch-Entwickler-App unter dev.twitch.tv/console → Client-ID (Umgebungsvariable TWITCH_CLIENT_ID)
und App-Token (Client-Credentials). Der Token kommt NICHT in den Chat: entweder als Netzwerk-Geheimnis der Umgebung für
api.twitch.tv (wird automatisch als „Authorization: Bearer …“ gesendet) oder lokal als Umgebungsvariable TWITCH_TOKEN.
Lädt nichts herunter. Clips dürfen nur nach den Regeln des Streamers verwendet werden (siehe streamers.json).
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.twitch.tv/helix"


def get(path, params):
    cid = os.environ.get("TWITCH_CLIENT_ID")
    if not cid:
        sys.exit("TWITCH_CLIENT_ID fehlt (Client-ID der Twitch-Entwickler-App).")
    url = f"{API}/{path}?{urllib.parse.urlencode(params, doseq=True)}"
    cmd = ["curl", "-sS", "--max-time", "30", "-H", f"Client-Id: {cid}", "-w", "\n%{http_code}"]
    if os.environ.get("TWITCH_TOKEN"):
        cmd += ["-H", f"Authorization: Bearer {os.environ['TWITCH_TOKEN']}"]
    r = subprocess.run(cmd + [url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    if code != "200":
        sys.exit(f"Twitch-Schnittstelle antwortet mit HTTP {code or '?'}: {body[:300] or r.stderr[:300]}")
    return json.loads(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", nargs="*")
    ap.add_argument("--stunden", type=float, default=48, help="Zeitraum, in dem die Clips erstellt wurden")
    ap.add_argument("--min-alter", type=float, default=12, help="Clips erst ab diesem Alter in Stunden (Regel Papaplatte)")
    ap.add_argument("--spiel", default="Grand Theft Auto VI")
    ap.add_argument("--anzahl", type=int, default=15)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(HERE, "streamers.json"), encoding="utf-8"))["streamer"]
    logins = a.login or [s["login"] for s in cfg]
    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(hours=a.stunden)
    end = now - dt.timedelta(hours=a.min_alter)
    game_id = None
    if a.spiel:
        g = get("games", {"name": a.spiel})["data"]
        game_id = g[0]["id"] if g else None
        if not game_id:
            print(f"Spiel „{a.spiel}“ nicht gefunden, zeige alle Spiele.")
    users = get("users", {"login": logins})["data"]
    rows = []
    for u in users:
        cur = None
        while True:
            p = {"broadcaster_id": u["id"], "started_at": start.isoformat().replace("+00:00", "Z"),
                 "ended_at": end.isoformat().replace("+00:00", "Z"), "first": 100}
            if cur:
                p["after"] = cur
            d = get("clips", p)
            for c in d["data"]:
                if game_id and c.get("game_id") != game_id:
                    continue
                rows.append(c)
            cur = d.get("pagination", {}).get("cursor")
            if not cur or len(rows) > 500:
                break
    rows.sort(key=lambda c: c["view_count"], reverse=True)
    rows = rows[: a.anzahl]
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    stamp = now.astimezone(dt.timezone(dt.timedelta(hours=1))).strftime("%Y-%m-%d_%H%M")
    lines = [f"# Top-Clips {', '.join(logins)} · {a.spiel or 'alle Spiele'} · Stand {stamp}", "",
             f"Erstellt in den letzten {a.stunden:g} h, mindestens {a.min_alter:g} h alt. Sortiert nach Aufrufen.", "",
             "| # | Aufrufe | Länge | Alter | Titel | Streamer | Link |", "|---|---|---|---|---|---|---|"]
    for i, c in enumerate(rows, 1):
        age = (now - dt.datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))).total_seconds() / 3600
        lines.append(f"| {i} | {c['view_count']:,} | {c['duration']:.0f} s | {age:.0f} h | {c['title'].replace('|', '/')} | "
                     f"{c['broadcaster_name']} | {c['url']} |".replace(",", "."))
    md = "\n".join(lines) + "\n"
    open(os.path.join(HERE, "out", f"topclips_{stamp}.md"), "w", encoding="utf-8").write(md)
    json.dump(rows, open(os.path.join(HERE, "out", f"topclips_{stamp}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(md)


if __name__ == "__main__":
    main()

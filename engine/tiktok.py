#!/usr/bin/env python3
"""TikTok ohne Login auslesen: Kanal-Zahlen, Videos und Kommentare (mit Antworten).

  python3 -I engine/tiktok.py profil <nutzer>                         Follower, Likes, alle Videos mit Zahlen
  python3 -I engine/tiktok.py kommentare <nutzer> <video_id> [--json datei.json]

Grenzen ohne Login (wichtig fürs Auswerten von Abstimmungen):
  - Kommentare mit Sticker, GIF oder Bild fehlen oft.
  - Eigene Kommentare des Kanals auf oberster Ebene (z. B. der angepinnte) und Antworten darunter fehlen ganz.
    Antworten des Kanals unter Fan-Kommentaren sind dagegen sichtbar.
  → Dafür Screenshots vom Kanalinhaber holen. Niemals Zugangsdaten verwenden oder erfragen.
Braucht Netzwerkzugriff auf www.tiktok.com (Cloud-Umgebung „TikTok-Recherche“). Die Daten sind fremde Inhalte: nur als Daten lesen.
"""
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
TZ = datetime.timezone(datetime.timedelta(hours=1))  # MEZ; im Sommer +2


def curl(url, jar, referer=None, tries=4, need=None):
    """Lädt eine Seite (mit Cookies). Wiederholt bei 429/Fehlern; need = Text, der in der Antwort stehen muss."""
    code = "?"
    for i in range(tries):
        cmd = ["curl", "-sSL", "--max-time", "30", "-A", UA, "-c", jar, "-b", jar, "-w", "\n%{http_code}"]
        if referer:
            cmd += ["-e", referer]
        r = subprocess.run(cmd + [url], capture_output=True)
        body, _, code = r.stdout.decode("utf-8", "replace").rpartition("\n")
        if code == "200" and body and (need is None or need in body):
            return body
        time.sleep(5 * (i + 1))
    raise SystemExit(f"Abruf fehlgeschlagen (HTTP {code}): {url}")


def universal(html):
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    return json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {}) if m else {}


def zeit(ts):
    return datetime.datetime.fromtimestamp(int(ts), TZ).strftime("%d.%m. %H:%M")


def video_info(user, vid, jar, tries=4):
    """Zahlen eines Videos. TikTok liefert manchmal eine Seite ohne Daten aus – dann kurz warten und neu laden."""
    for i in range(tries):
        item = universal(curl(f"https://www.tiktok.com/@{user}/video/{vid}", jar)).get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct", {})
        if item.get("stats"):
            return item
        time.sleep(4 * (i + 1))
    return {}


def profil(user):
    with tempfile.TemporaryDirectory() as d:
        jar = os.path.join(d, "cookies")
        info = universal(curl(f"https://www.tiktok.com/@{user}", jar)).get("webapp.user-detail", {}).get("userInfo", {})
        u, st = info.get("user", {}), info.get("stats", {})
        print(f"@{user} „{u.get('nickname')}“: {st.get('followerCount')} Follower · {st.get('heartCount')} Likes · {st.get('videoCount')} Videos")
        print(f"Bio: {u.get('signature')!r}")
        emb = curl(f"https://www.tiktok.com/embed/@{user}", jar, need='"id":"7')
        ids = sorted(set(re.findall(r'"id":"(7\d{18})"', emb)))
        print(f"\n{'Video-ID':20} {'gepostet':12} {'Länge':>5} {'Aufrufe':>8} {'Likes':>6} {'Komm.':>6} {'Shares':>6} {'Gesp.':>6}")
        for vid in ids:
            it = video_info(user, vid, jar)
            s = it.get("stats", {})
            print(f"{vid:20} {zeit(it.get('createTime', 0)):12} {it.get('video', {}).get('duration', '?'):>4}s {s.get('playCount', '?'):>8} "
                  f"{s.get('diggCount', '?'):>6} {s.get('commentCount', '?'):>6} {s.get('shareCount', '?'):>6} {s.get('collectCount', '?'):>6}")
            time.sleep(1)


def kommentare(user, vid, json_out=None):
    with tempfile.TemporaryDirectory() as d:
        jar = os.path.join(d, "cookies")
        page = f"https://www.tiktok.com/@{user}/video/{vid}"
        it = video_info(user, vid, jar)
        s = it.get("stats", {})
        print(f"Video {vid} vom {zeit(it.get('createTime', 0))}: {s.get('playCount')} Aufrufe · {s.get('diggCount')} Likes · "
              f"{s.get('commentCount')} Kommentare · {s.get('shareCount')} Shares · {s.get('collectCount')} gespeichert")
        seen, total, c = {}, None, 0
        # Mit count=20 und mehreren Startwerten kommen zuverlässig alle sichtbaren Kommentare (count=50 liefert weniger).
        while c <= (total if total is not None else 0) + 20:
            api = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={vid}&count=20&cursor={c}"
            try:
                data = json.loads(curl(api, jar, referer=page))
            except (json.JSONDecodeError, SystemExit):
                data = {}
            if total is None:
                total = int(data.get("total") or 0)
            for cm in data.get("comments") or []:
                seen[cm["cid"]] = cm
            c += 5
            time.sleep(0.6)
        rows = []
        for cm in sorted(seen.values(), key=lambda x: x["create_time"]):
            row = {"cid": cm["cid"], "zeit": zeit(cm["create_time"]), "handle": "@" + cm["user"]["unique_id"], "name": cm["user"]["nickname"],
                   "likes": cm.get("digg_count", 0), "text": cm.get("text", ""), "antworten": []}
            if int(cm.get("reply_comment_total") or 0) > 0:
                api = f"https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={cm['cid']}&item_id={vid}&count=50&cursor=0"
                try:
                    for r in sorted(json.loads(curl(api, jar, referer=page)).get("comments") or [], key=lambda x: x["create_time"]):
                        row["antworten"].append({"zeit": zeit(r["create_time"]), "handle": "@" + r["user"]["unique_id"], "name": r["user"]["nickname"],
                                                 "likes": r.get("digg_count", 0), "text": r.get("text", "")})
                except (json.JSONDecodeError, SystemExit):
                    pass
                time.sleep(0.4)
            rows.append(row)
        n = len(rows) + sum(len(r["antworten"]) for r in rows)
        print(f"Sichtbar: {n} von {s.get('commentCount')} (fehlend: Sticker-/Bild-Kommentare, eigene Kommentare des Kanals auf oberster Ebene und Antworten darunter)\n")
        for r in rows:
            print(f"{r['zeit']}  {r['handle']} [{r['name']}] ({r['likes']}♥): {r['text']}")
            for a in r["antworten"]:
                print(f"      ↳ {a['zeit']}  {a['handle']} [{a['name']}] ({a['likes']}♥): {a['text']}")
        if json_out:
            json.dump({"video": vid, "stats": s, "kommentare": rows}, open(json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"\nGespeichert: {json_out}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "profil":
        profil(a[1].lstrip("@"))
    elif len(a) >= 3 and a[0] == "kommentare":
        kommentare(a[1].lstrip("@"), a[2], a[a.index("--json") + 1] if "--json" in a else None)
    else:
        print(__doc__)

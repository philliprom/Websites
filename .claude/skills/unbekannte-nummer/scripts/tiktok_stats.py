"""Öffentliche Zahlen eines TikTok-Videos oder Profils (ohne Login, nur öffentliche Seiten).

  python3 tiktok_stats.py https://vm.tiktok.com/XXXX/        -> Aufrufe, Likes, Kommentare, Teilen, Speichern, Alter
  python3 tiktok_stats.py @handle                            -> Profil: vorhanden/frei, Follower, Videos
"""
import datetime
import json
import re
import subprocess
import sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(url):
    return subprocess.run(["curl", "-s", "-L", "-m", "30", "-A", UA, "-H", "Accept-Language: de-DE,de;q=0.9", url],
                          capture_output=True, text=True).stdout


def scope(html):
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    return json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {}) if m else {}


def video(url):
    if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
        url = subprocess.run(["curl", "-s", "-m", "20", "-A", UA, "-o", "/dev/null", "-w", "%{redirect_url}", url],
                             capture_output=True, text=True).stdout.split("?")[0]
    it = scope(fetch(url)).get("webapp.video-detail", {}).get("itemInfo", {}).get("itemStruct", {})
    if not it:
        sys.exit("Keine Videodaten gefunden (Seite geändert oder Video nicht öffentlich).")
    st, au, ast = it.get("stats", {}), it.get("author", {}), it.get("authorStats", {})
    t0 = datetime.datetime.fromtimestamp(int(it["createTime"]), datetime.timezone.utc)
    h = (datetime.datetime.now(datetime.timezone.utc) - t0).total_seconds() / 3600
    views = int(st.get("playCount") or 0)
    print(f"@{au.get('uniqueId')} | gepostet {t0:%d.%m. %H:%M} UTC (vor {h:.1f} h) | Länge {it.get('video', {}).get('duration')} s")
    print(f"Aufrufe {views} ({views / max(h, 0.1):.0f}/h) | Likes {st.get('diggCount')} | Kommentare {st.get('commentCount')} | "
          f"Teilen {st.get('shareCount')} | Speichern {st.get('collectCount')}")
    if views:
        print(f"Like-Rate {100 * int(st.get('diggCount') or 0) / views:.1f} % | Speicher-Rate "
              f"{100 * int(st.get('collectCount') or 0) / views:.1f} %")
    print(f"Kanal: {ast.get('followerCount')} Follower, {ast.get('videoCount')} Videos")


def profil(handle):
    d = scope(fetch(f"https://www.tiktok.com/@{handle.lstrip('@')}")).get("webapp.user-detail", {})
    if d.get("statusCode") == 10221:
        print(f"@{handle.lstrip('@')}: frei (kein Profil gefunden)")
        return
    s = d.get("userInfo", {}).get("stats", {})
    print(f"@{handle.lstrip('@')}: vergeben | {s.get('followerCount')} Follower | {s.get('videoCount')} Videos | "
          f"{s.get('heartCount')} Likes gesamt")


if __name__ == "__main__":
    arg = sys.argv[1]
    profil(arg) if arg.startswith("@") else video(arg)

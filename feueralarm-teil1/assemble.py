"""Schnitt: Bilder hochskalieren (720x1280 -> 1080x1920), Farbstimmung je Ort, Untertitel (weiß, Schlüsselwörter rot),
Regel-Banner der unbekannten Nummer, Entscheidungskarte, Ton. Ergebnis: out/feueralarm_teil1_tiktok.mp4

  python3 assemble.py <frames-ordner> [vorschau]   (vorschau: nur Standbilder an Prüfzeiten nach build/check_*.png)
"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
OUT = os.path.join(HERE, "out")
FONT = os.path.join(HERE, "assets", "fonts", "Nunito-Black.ttf")
W, H, FPS = 1080, 1920, 30
TL = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
SHOTS = json.load(open(os.path.join(BUILD, "shots.json"), encoding="utf-8"))
TOTAL = TL["total"]
ENDK = [e["t"] for e in TL["events"] if e["kind"] == "endkarte"][0]
TIMES = {1: "11:52", 2: "11:53", 3: "11:54", 4: "11:55", 5: "11:57"}
YELLOW = (255, 204, 0)
RED = (255, 59, 48)

sys.path.insert(0, HERE)
from story import ENDKARTE, TITLE, PART  # noqa: E402


def font(sz):
    return ImageFont.truetype(FONT, sz)


# ---------------------------------------------------------------- Untertitel
def chunks(line):
    """Zeile in Sätze teilen; Zeit nach Zeichenzahl verteilen."""
    text = line["sub"]
    parts = [p.strip() for p in re.split(r"(?<=[.!?…:])\s+", text) if p.strip()]
    merged = []
    for p in parts:  # kurze Stücke und klein beginnende Satzreste an das vorige hängen
        if merged and ((len(p) < 8 and not p.endswith("?")) or p[0].islower() or merged[-1].endswith("…")):
            merged[-1] += " " + p
        else:
            merged.append(p)
    total = sum(len(p) for p in merged)
    t = line["start"]
    out = []
    for p in merged:
        d = line["dur"] * len(p) / total
        out.append((t, t + d, p))
        t += d
    return out


def render_sub(text, red_words, size=54, maxw=860):
    f = font(size)
    words = text.split()
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if tmp.textlength(test, font=f) > maxw and cur:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    lh = int(size * 1.18)
    img = Image.new("RGBA", (maxw + 80, lh * len(lines) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    reds = set()
    for rw in red_words:
        for x in rw.split():
            reds.add(re.sub(r"[^\wÄÖÜäöüß]", "", x).lower())
    for k, ln in enumerate(lines):
        lw = tmp.textlength(" ".join(ln), font=f)
        x = (img.width - lw) / 2
        y = 20 + k * lh
        for w in ln:
            key = re.sub(r"[^\wÄÖÜäöüß]", "", w).lower()
            col = RED if key in reds else (255, 255, 255)
            d.text((x, y), w, font=f, fill=col, stroke_width=7, stroke_fill=(10, 10, 12))
            x += tmp.textlength(w + " ", font=f)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.5)))
    base = Image.new("RGBA", img.size, (0, 0, 0, 0))
    base.alpha_composite(shadow, (0, 4))
    base.alpha_composite(img)
    return base


SUBS = []
for l in TL["lines"]:
    if l["kind"] == "regel":
        continue
    for a, b, txt in chunks(l):
        SUBS.append(dict(t0=a - 0.05, t1=b + 0.12, img=render_sub(txt, l.get("rot", []))))


# ---------------------------------------------------------------- Regel-Banner
def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_banner(n, text):
    bw = 860
    f_h, f_r, f_t = font(30), font(64), font(46)
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = wrap(tmp, text, f_t, bw - 80)
    bh = 60 + 78 + 58 * len(lines) + 34
    img = Image.new("RGBA", (bw + 40, bh + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 26, 20 + bw, 26 + bh), 34, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 20, 20 + bw, 20 + bh), 34, fill=(18, 18, 22, 238), outline=YELLOW, width=5)
    # Kopfzeile: Symbol, Absender, Uhrzeit
    d.rounded_rectangle((50, 44, 92, 86), 10, fill=(90, 90, 100))
    d.text((62, 44), "?", font=font(34), fill=(255, 255, 255))
    d.text((108, 50), "UNBEKANNTE NUMMER", font=f_h, fill=(185, 185, 195))
    tw = d.textlength(TIMES[n], font=f_h)
    d.text((20 + bw - 34 - tw, 50), TIMES[n], font=f_h, fill=(185, 185, 195))
    d.text((50, 100), f"REGEL {n}", font=f_r, fill=YELLOW)
    for k, ln in enumerate(lines):
        y = 100 + 82 + 58 * k
        x = 50
        for w in ln.split():  # Großgeschriebenes (NICHT, DICH) gelb hervorheben
            col = YELLOW if (len(w) > 2 and re.sub(r"[^A-ZÄÖÜ]", "", w) == re.sub(r"[^\wÄÖÜäöüß]", "", w)) else (
                245, 245, 245)
            d.text((x, y), w, font=f_t, fill=col)
            x += d.textlength(w + " ", font=f_t)
    return img


BANNERS = []
for l in TL["lines"]:
    if l["kind"] == "regel":
        buzz = [e["t"] for e in TL["events"] if e["kind"] == "buzz" and e.get("regel") == l["n"]][0]
        BANNERS.append(dict(t0=buzz + 0.3, t1=l["end"] + 0.7, img=render_banner(l["n"], l["sub"])))


# ---------------------------------------------------------------- Entscheidungskarte
def icon_auto(sz, col):
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = sz / 100
    d.rounded_rectangle((8 * s, 42 * s, 92 * s, 72 * s), int(10 * s), fill=col)
    d.polygon([(24 * s, 44 * s), (34 * s, 24 * s), (68 * s, 24 * s), (80 * s, 44 * s)], fill=col)
    d.polygon([(38 * s, 42 * s), (42 * s, 30 * s), (52 * s, 30 * s), (52 * s, 42 * s)], fill=(200, 230, 255))
    d.polygon([(56 * s, 42 * s), (56 * s, 30 * s), (65 * s, 30 * s), (72 * s, 42 * s)], fill=(200, 230, 255))
    for cx in (28, 72):
        d.ellipse(((cx - 11) * s, 62 * s, (cx + 11) * s, 84 * s), fill=(25, 25, 30))
        d.ellipse(((cx - 5) * s, 68 * s, (cx + 5) * s, 78 * s), fill=(170, 170, 180))
    return im


def icon_muetze(sz, col):
    """Hausmeister-Mütze mit Schlüssel."""
    im = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = sz / 100
    d.pieslice((14 * s, 14 * s, 86 * s, 86 * s), 180, 360, fill=col)
    d.rounded_rectangle((12 * s, 46 * s, 96 * s, 58 * s), int(5 * s), fill=col)
    d.ellipse((28 * s, 66 * s, 46 * s, 84 * s), outline=(255, 255, 255), width=int(5 * s))
    d.rectangle((44 * s, 72 * s, 80 * s, 78 * s), fill=(255, 255, 255))
    d.rectangle((70 * s, 78 * s, 75 * s, 86 * s), fill=(255, 255, 255))
    return im


def endcard():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1 = 120, 960
    # Frage
    d.rounded_rectangle((x0, 330, x1, 450), 26, fill=(22, 40, 92, 245))
    q = ENDKARTE["frage"]
    f = font(76)
    d.text(((W - d.textlength(q, font=f)) / 2, 340), q, font=f, fill=(255, 255, 255))
    # zwei Kacheln
    tiles = [(ENDKARTE["a"], (36, 122, 220), icon_auto), (ENDKARTE["b"], (214, 64, 52), icon_muetze)]
    tw = (x1 - x0 - 30) // 2
    for k, ((title, sub), col, ic) in enumerate(tiles):
        tx = x0 + k * (tw + 30)
        d.rounded_rectangle((tx, 480, tx + tw, 900), 30, fill=(16, 16, 20, 238), outline=col + (255,), width=6)
        img.alpha_composite(ic(220, col + (255,)), (tx + (tw - 220) // 2, 510))
        ft = font(50 if len(title) < 12 else 40)
        words = title.split()
        lines = [title] if d.textlength(title, font=ft) < tw - 30 else [" ".join(words[:-1]), words[-1]]
        for j, ln in enumerate(lines):
            d.text((tx + (tw - d.textlength(ln, font=ft)) / 2, 745 + j * 52 - (26 if len(lines) > 1 else 0)), ln,
                   font=ft, fill=(255, 255, 255))
        fs = font(30)
        d.text((tx + (tw - d.textlength(sub, font=fs)) / 2, 845), sub, font=fs, fill=(200, 200, 210))
    # Teil 2 entscheidet ihr
    t2 = ENDKARTE["teil2"]
    f2 = font(54)
    w2 = d.textlength(t2, font=f2)
    d.rounded_rectangle(((W - w2) / 2 - 40, 940, (W + w2) / 2 + 40, 1030), 45, fill=YELLOW + (255,))
    d.text(((W - w2) / 2, 950), t2, font=f2, fill=(20, 20, 20))
    hint = "Schreib AUTO oder POHL in die Kommentare"
    fh = font(34)
    d.text(((W - d.textlength(hint, font=fh)) / 2, 1060), hint, font=fh, fill=(255, 255, 255), stroke_width=4,
           stroke_fill=(0, 0, 0))
    ttl = f"{TITLE} · {PART}"
    ft = font(32)
    d.text(((W - d.textlength(ttl, font=ft)) / 2, 1130), ttl, font=ft, fill=(220, 220, 230), stroke_width=3,
           stroke_fill=(0, 0, 0))
    return img


ENDCARD = endcard()


# ---------------------------------------------------------------- Farbe je Ort
def set_at(t):
    cur = SHOTS[0]
    for s in SHOTS:
        if s["t0"] <= t:
            cur = s
    return cur


VIG = None


def vignette(strength):
    global VIG
    if VIG is None:
        y, x = np.mgrid[0:H, 0:W]
        r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        VIG = np.clip(r - 0.55, 0, 1) ** 1.6
    return 1 - strength * VIG[..., None]


def grade(arr, t):
    s = set_at(t)
    a = arr.astype(np.float32)
    if s["set"] == "klasse":
        a = a * np.array([1.03, 1.0, 0.96]) * vignette(0.25)
    elif s["set"] == "flur":
        puls = (0.5 + 0.5 * math.sin(2 * math.pi * 1.25 * t)) ** 2
        red = np.array([255.0, 30.0, 25.0])
        a = a * (1 - 0.22 * puls) + red * 0.22 * puls
        a = a * vignette(0.45 + 0.2 * puls)
    else:  # Keller
        a = a * np.array([1.0, 0.93, 0.82]) * 0.86 * vignette(0.6)
    return np.clip(a, 0, 255).astype(np.uint8)


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def compose(frame, t):
    arr = np.asarray(frame.resize((W, H), Image.LANCZOS))
    if t >= ENDK:  # Endkarte: Bild abdunkeln und weichzeichnen
        k = ease((t - ENDK) / 0.5)
        blur = frame.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10 * k))
        arr = (np.asarray(blur).astype(np.float32) * (1 - 0.55 * k)).astype(np.uint8)
    else:
        arr = grade(arr, t)
    img = Image.fromarray(arr).convert("RGBA")
    for b in BANNERS:
        if b["t0"] <= t <= b["t1"] + 0.25:
            k_in = ease((t - b["t0"]) / 0.28)
            k_out = 1 - ease((t - b["t1"]) / 0.25) if t > b["t1"] else 1
            alpha = k_in * k_out
            y = int(290 - 50 * (1 - k_in))
            ov = b["img"].copy()
            ov.putalpha(ov.getchannel("A").point(lambda v: int(v * alpha)))
            img.alpha_composite(ov, ((W - ov.width) // 2, y))
    if t < ENDK:
        for s in SUBS:
            if s["t0"] <= t <= s["t1"]:
                k = ease((t - s["t0"]) / 0.12)
                ov = s["img"]
                y = 1225 - ov.height + int(10 * (1 - k))
                img.alpha_composite(ov, ((W - ov.width) // 2, y))
                break
    if t >= ENDK:
        k = ease((t - ENDK - 0.2) / 0.45)
        ov = ENDCARD.copy()
        ov.putalpha(ov.getchannel("A").point(lambda v: int(v * k)))
        img.alpha_composite(ov, (0, int(40 * (1 - k))))
    return img.convert("RGB")


def frame_path(fdir, f):
    p = os.path.join(fdir, f"f_{f:05d}.jpg")
    return p if os.path.exists(p) else os.path.join(fdir, f"f_{f:05d}.png")


def main():
    fdir = sys.argv[1]
    nf = int(round(TOTAL * FPS))
    if len(sys.argv) > 2 and sys.argv[2] == "vorschau":
        for tt in [float(x) for x in sys.argv[3].split(",")]:
            f = min(nf, int(tt * FPS) + 1)
            p = frame_path(fdir, f)
            if os.path.exists(p):
                compose(Image.open(p).convert("RGB"), (f - 1) / FPS).save(os.path.join(BUILD, f"check_{tt:06.2f}.png"))
        return
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(BUILD, "video_ohne_ton.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    last = None
    for f in range(1, nf + 1):
        p = frame_path(fdir, f)
        if os.path.exists(p):
            last = Image.open(p).convert("RGB")
        if last is None:
            raise SystemExit(f"Bild {f} fehlt")
        enc.stdin.write(compose(last, (f - 1) / FPS).tobytes())
        if f % 300 == 0:
            print(f"{f}/{nf}", flush=True)
    enc.stdin.close()
    enc.wait()
    out = os.path.join(OUT, "feueralarm_teil1_tiktok.mp4")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", tmp, "-i", os.path.join(BUILD, "mix.wav"),
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print("fertig:", out)


if __name__ == "__main__":
    main()

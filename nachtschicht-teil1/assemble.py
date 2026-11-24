"""Schnitt Nachtschicht Teil 1: setzt Kamerabilder (Blender), Regel-Zettel, Handy und Entscheidungskarten zum fertigen
Video zusammen, mit Überwachungskamera-Look, Untertiteln (ASS) und Ton (build/mix.wav aus sound.py).

  <vx>/bin/python nachtschicht-teil1/assemble.py                 -> out/nachtschicht_teil1.mp4
  <vx>/bin/python nachtschicht-teil1/assemble.py --stills 1,14,40 -> build/check_<t>.png (ohne Video, zum Prüfen)
"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD, OUT, FONTS = os.path.join(HERE, "build"), os.path.join(HERE, "out"), os.path.join(HERE, "fonts")
W, H, FPS = 1080, 1920, 30
edl = json.load(open(os.path.join(BUILD, "edl.json"), encoding="utf-8"))
tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
EV, SHOTS, D = edl["events"], edl["shots"], edl["duration"]
SH = {s["id"]: s for s in SHOTS}

F_OSD = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", 38)
F_TITLE = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 112)
F_SUB = ImageFont.truetype(os.path.join(FONTS, "Oswald-Bold.ttf"), 48)
F_HEAD = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 92)
F_TYPE = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 230)
F_END = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 86)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.55 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.25, 1)[..., None]
VIG_SOFT = (1 - 0.3 * (((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)).clip(0.5, 1)[..., None]
SCAN = (1 - 0.05 * (np.arange(H) % 3 == 0)).astype(np.float32)[:, None, None]
rng = np.random.default_rng(3)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out_back(x):
    x = min(1.0, max(0.0, x))
    c = 1.4
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------------------------------------------------------------- Quellen
def nframes(src):
    return len([f for f in os.listdir(os.path.join(BUILD, src)) if f.endswith(".png") and f[:4].isdigit()])


@lru_cache(maxsize=48)
def src_img(src, k):
    return Image.open(os.path.join(BUILD, src, f"{k:04d}.png")).convert("RGB")


@lru_cache(maxsize=24)
def src_up(src, k):
    """Kamerabild auf 1080×1920 hochrechnen und weichzeichnen (einmal je Quellbild)."""
    return np.asarray(src_img(src, k).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.1)), dtype=np.float32) / 255


def src_index(spec, t, t0):
    k = spec["from"] + int((t - t0) * edl["fps_src"])
    last = nframes(spec["src"])
    if spec.get("loop"):
        span = last - spec["from"] + 1
        k = spec["from"] + (k - spec["from"]) % max(1, span)
    return max(1, min(last, k))


FIG = json.load(open(os.path.join(BUILD, "r2", "figure.json"))) if os.path.exists(os.path.join(BUILD, "r2", "figure.json")) else {"x": 200, "y": 330}


def cctv_frame(spec, t, t0, dim=1.0):
    k = src_index(spec, t, t0)
    z = 1.0
    if spec.get("zoom"):
        za, zb, zmax = spec["zoom"]
        z = 1 + (zmax - 1) * ease((t - za) / max(0.1, zb - za))
    if z > 1.001:
        im = src_img(spec["src"], k)
        sw, sh_ = im.width / z, im.height / z
        cx = min(max(FIG["x"], sw / 2), im.width - sw / 2)
        cy = min(max(FIG["y"], sh_ / 2), im.height - sh_ / 2)
        a = np.asarray(im.resize((W, H), Image.BICUBIC, box=(cx - sw / 2, cy - sh_ / 2, cx + sw / 2, cy + sh_ / 2))
                       .filter(ImageFilter.GaussianBlur(1.0 + 0.6 * (z - 1))), dtype=np.float32) / 255
    else:
        a = src_up(spec["src"], k)
    y_ = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    a = y_[..., None] + 0.32 * (a - y_[..., None])
    a = np.clip((a - 0.5) * 1.12 + 0.48, 0, 1) ** 1.05
    a = a * np.array([0.95, 1.03, 0.98], dtype=np.float32)
    nz = rng.normal(0, 0.038, (H // 2, W // 2)).astype(np.float32)
    nz = np.repeat(np.repeat(nz, 2, 0), 2, 1)[..., None]
    a = (a + nz) * VIG * SCAN * dim
    return a, z


def to_img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGB")


def osd(img, spec, t, t0, z=1.0):
    d = ImageDraw.Draw(img)
    clock = spec["clock"] + int(t - t0)
    hh, mm, ss = clock // 3600, clock % 3600 // 60, clock % 60
    kw = dict(font=F_OSD, fill=(235, 235, 235), stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((70, 292), spec["cam"], **kw)
    d.text((1010, 292), f"24.11.2026  {hh:02d}:{mm:02d}:{ss:02d}", anchor="ra", **kw)
    if (t % 1.0) < 0.6:
        d.ellipse((72, 360, 98, 386), fill=(225, 30, 30))
        d.text((112, 352), "REC", font=F_OSD, fill=(225, 30, 30), stroke_width=3, stroke_fill=(0, 0, 0))
    if z > 1.05:
        d.text((1010, 352), f"ZOOM {z:.1f}×", anchor="ra", **kw)


def glitch(a, strength=1.0, seed=0):
    g = np.random.default_rng(seed)
    a = a.copy()
    sh_ = int(14 * strength)
    a[..., 0] = np.roll(a[..., 0], sh_, axis=1)
    a[..., 2] = np.roll(a[..., 2], -sh_, axis=1)
    for _ in range(int(5 * strength)):
        y0 = g.integers(250, H - 200)
        hgt = g.integers(10, 60)
        a[y0:y0 + hgt] = np.roll(a[y0:y0 + hgt], g.integers(-80, 80), axis=1)
    return a


def static_frame(seed):
    g = np.random.default_rng(seed)
    nz = g.random((H // 4, W // 4)).astype(np.float32)
    nz = np.repeat(np.repeat(nz, 4, 0), 4, 1)
    return np.stack([nz * 0.85] * 3, axis=-1) * SCAN


# ---------------------------------------------------------------- Einstellungen
def render_cctv(s, t):
    t0 = s["t"][0]
    a, z = cctv_frame(s, t, t0, s.get("dim", 1.0))
    jump = EV["jump"]
    if s["id"] == "SH6" and jump <= t < jump + 0.28:
        a = glitch(a, 1.0, int(t * 100))
        if t < jump + 0.07:
            a = np.clip(a * 1.6 + 0.12, 0, 1)
    if t - t0 < 0.1 and s["id"] != "SH0":
        k = (t - t0) / 0.1
        a = static_frame(int(t * 1000)) * (1 - k) + a * k
    img = to_img(a)
    osd(img, s, t, t0, z)
    return img


def render_black(s, t):
    a = np.zeros((H, W, 3), np.float32) + rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)
    img = to_img(np.clip(a, 0, 1))
    d = ImageDraw.Draw(img)
    a1 = s["t"][0]
    n = sum(1 for k in range(5) if t >= a1 + 0.18 + k * 0.13)
    txt = s["text"][:n]
    if txt:
        d.text((540, 860), txt, font=F_TYPE, fill=(235, 235, 230), anchor="mm")
    if (t * 2.5) % 1 < 0.6:
        bb = d.textbbox((540, 860), s["text"], font=F_TYPE, anchor="mm")
        x = bb[0] + (bb[2] - bb[0]) * n / 5 + 10
        d.rectangle((x, bb[1] + 20, x + 26, bb[3] - 10), fill=(235, 235, 230))
    d.text((540, 1010), "UHR", font=F_SUB, fill=(160, 160, 160), anchor="mm")
    return img


NOTE = Image.open(os.path.join(BUILD, "note", "zettel.png")).convert("RGB") if os.path.exists(os.path.join(BUILD, "note", "zettel.png")) else None
BOXES = json.load(open(os.path.join(BUILD, "note", "boxes.json"))) if os.path.exists(os.path.join(BUILD, "note", "boxes.json")) else {}
NOTE_A = np.asarray(NOTE, dtype=np.float32) / 255 if NOTE else None


def note_state(name):
    if name == "all":
        bs = [BOXES[k] for k in ("Titel", "Regel 1", "Regel 4", "Rot", "Gruss") if k in BOXES]
        x0, y0, x1, y1 = min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)
        return ((x0 + x1) / 2, (y0 + y1) / 2 + 20, 1.6)
    x0, y0, x1, y1 = BOXES[name]
    s_ = min(3.2, max(1.9, W * 0.9 / (x1 - x0 + 24)))
    return ((x0 + x1) / 2, (y0 + y1) / 2, s_)


def render_note(s, t):
    for c in s.get("cuts", []):
        if c["t"][0] <= t < c["t"][1]:
            return render_cctv(dict(c, id="CUT"), t)
    keys = s["keys"]
    st_ = note_state(keys[0][1])
    for i, (kt, name) in enumerate(keys):
        if t >= kt - 0.15:
            prev = st_
            nxt = note_state(name)
            p = ease((t - kt + 0.15) / 0.65)
            st_ = tuple(prev[j] + (nxt[j] - prev[j]) * p for j in range(3))
    cx, cy, sc = st_
    sc *= 1 + 0.012 * math.sin(t * 0.7)
    cx += 3 * math.sin(1.3 * t) + 2 * math.sin(2.9 * t + 1)
    cy += 3 * math.cos(1.1 * t) + 2 * math.sin(2.3 * t)
    a = NOTE_A.copy()
    for kt, name in keys:
        if name.startswith("Regel") and t >= kt + 0.25:
            p = min(1.0, (t - kt - 0.25) / 0.5)
            x0, y0, x1, y1 = BOXES[name]
            xe = int(x0 - 6 + (x1 - x0 + 12) * p)
            a[y0 - 3:y1 + 3, x0 - 6:xe] *= np.array([1.0, 0.9, 0.35], dtype=np.float32) * 0.6 + 0.4
    im = Image.fromarray((a * 255).astype(np.uint8))
    sw, sh_ = W / sc, H / sc
    cx = min(max(cx, sw / 2), im.width - sw / 2)
    cy = min(max(cy, sh_ / 2), im.height - sh_ / 2)
    b = np.asarray(im.resize((W, H), Image.BICUBIC, box=(cx - sw / 2, cy - sh_ / 2, cx + sw / 2, cy + sh_ / 2)), dtype=np.float32) / 255
    b = (b * 0.95 + rng.normal(0, 0.02, (H, W, 1)).astype(np.float32)) * VIG_SOFT
    if t - s["t"][0] < 0.1:
        k = (t - s["t"][0]) / 0.1
        b = static_frame(int(t * 1000)) * (1 - k) + b * k
    return to_img(b)


ASSET = {k: Image.open(os.path.join(BUILD, "assets", k + ".png")).convert("RGBA")
         for k in ("phone_bg", "notif1", "notif2", "cardA", "cardB") if os.path.exists(os.path.join(BUILD, "assets", k + ".png"))}


def paste_alpha(base, im, x, y, alpha=1.0):
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(x), int(y)))


def render_phone(s, t):
    dx = 0
    for b in EV["phone_buzz"] + [EV["msg2"] - 0.05]:
        if b <= t < b + 0.38:
            dx = 9 * math.sin(2 * math.pi * 38 * (t - b))
    img = Image.new("RGBA", (W, H))
    img.alpha_composite(ASSET["phone_bg"], (int(dx), 0))
    for key, at, y in (("notif1", EV["msg1"], 700), ("notif2", EV["msg2"], 940)):
        if t >= at:
            p = ease((t - at) / 0.35)
            paste_alpha(img, ASSET[key], 140 + dx, y - 120 * (1 - p), p)
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255
    a = (a + rng.normal(0, 0.015, (H, W, 1)).astype(np.float32)) * VIG_SOFT
    if t - s["t"][0] < 0.08:
        a = static_frame(int(t * 1000))
    return to_img(a)


CARD_SMALL = {k: ASSET[k].resize((int(ASSET[k].width * 0.8), int(ASSET[k].height * 0.8)), Image.LANCZOS)
              for k in ("cardA", "cardB") if k in ASSET}


def render_decision(s, t):
    t0 = s["t"][0]
    fk = EV["final_knock"]
    if t >= fk + 0.22:
        img = to_img(np.zeros((H, W, 3), np.float32) + rng.normal(0, 0.012, (H, W, 1)).astype(np.float32).clip(0, 1))
        d = ImageDraw.Draw(img)
        d.text((540, 860), "TEIL 2 FOLGT", font=F_END, fill=(230, 230, 225), anchor="mm")
        d.text((540, 980), "KOMMENTIERE  A  ODER  B", font=F_SUB, fill=(225, 40, 45), anchor="mm")
        return img
    a, _ = cctv_frame(s, t, t0, s.get("dim", 0.5))
    red = 0.06 + 0.04 * math.sin(t * 3)
    a = a * (1 - red) + np.array([0.5, 0.0, 0.02], dtype=np.float32) * red
    if fk <= t < fk + 0.22:
        a = glitch(a, 1.2, int(t * 100))
    img = to_img(a).convert("RGBA")
    d = ImageDraw.Draw(img)
    if t >= t0 + 0.2:
        d.text((540, 470), "DU ENTSCHEIDEST", font=F_HEAD, fill=(225, 40, 45), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    ca, cb = EV["cards"]
    A, B = CARD_SMALL["cardA"], CARD_SMALL["cardB"]
    x_end = (W - A.width) // 2
    if t >= ca:
        x = -A.width + (x_end + A.width) * ease_out_back((t - ca) / 0.45)
        img.alpha_composite(A, (int(x), 975))
    if t >= cb:
        x = W + (x_end - W) * ease_out_back((t - cb) / 0.45)
        img.alpha_composite(B, (int(x), 1175))
    out = img.convert("RGB")
    osd(out, s, t, t0)
    return out


def render_hook_overlay(img, t):
    d = ImageDraw.Draw(img)
    k = min(1.0, t / 0.2)
    col = (int(225 * k), int(36 * k), int(42 * k))
    d.text((540, 540), "NACHTSCHICHT", font=F_TITLE, fill=col, anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((540, 650), "TEIL 1  ·  DU ENTSCHEIDEST", font=F_SUB, fill=(240, 240, 240), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))


def frame_at(t):
    s = next((x for x in SHOTS if x["t"][0] <= t < x["t"][1]), SHOTS[-1])
    if s["kind"] == "cctv" and s.get("cards"):
        return render_decision(s, t)
    if s["kind"] == "cctv":
        img = render_cctv(s, t)
        if s.get("title"):
            render_hook_overlay(img, t)
        return img
    if s["kind"] == "black":
        return render_black(s, t)
    if s["kind"] == "note":
        return render_note(s, t)
    if s["kind"] == "phone":
        return render_phone(s, t)
    raise ValueError(s["kind"])


# ---------------------------------------------------------------- Untertitel (ASS, libass)
def ass_time(x):
    x = max(0.0, x)
    return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"


F_CAP = ImageFont.truetype(os.path.join(FONTS, "Oswald-Bold.ttf"), 100)


def build_ass():
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Oswald,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1,0,1,7,3,2,60,60,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for seg in tl["segments"]:
        caps = seg["caps"]
        for i, c in enumerate(caps):
            a = c["start"]
            b = caps[i + 1]["start"] if i + 1 < len(caps) else seg["speechEnd"] + 0.25
            plain = " ".join(w for w, _ in c["words"])
            width = F_CAP.getlength(plain) * 1.04       # Breite bei Schriftgröße 104
            fs = 104 if width <= 740 else int(104 * 740 / width)
            parts = []
            for w, style in c["words"]:
                w = w.replace("{", "(").replace("}", ")")
                parts.append("{\\c&H003030FF&}" + w + "{\\c&H00FFFFFF&}" if style in ("g", "r") else w)
            txt = "{\\fs%d\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}" % fs + " ".join(parts)
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{txt}")
    path = os.path.join(BUILD, "captions.ass")
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")
    return path


def cover():
    """Titelbild: Gestalt an der Tür (nach dem Sprung), Serientitel, Frage."""
    img = render_cctv(SH["SH6"], EV["jump"] + 1.3)
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 150)
    q = ImageFont.truetype(os.path.join(FONTS, "Oswald-Bold.ttf"), 104)
    d.text((540, 520), "NACHTSCHICHT", font=big, fill=(225, 36, 42), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
    d.text((540, 650), "TEIL 1", font=F_SUB, fill=(240, 240, 240), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((540, 1250), "WÜRDEST DU", font=q, fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((540, 1370), "AUFMACHEN?", font=q, fill=(255, 48, 48), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((540, 1480), "DU ENTSCHEIDEST · A ODER B", font=F_SUB, fill=(230, 230, 230), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, "titelbild.png"))
    print("Titelbild fertig")


def main():
    args = sys.argv[1:]
    if "--cover" in args:
        cover()
        return
    if "--stills" in args:
        for x in args[args.index("--stills") + 1].split(","):
            frame_at(float(x)).save(os.path.join(BUILD, f"check_{float(x):05.2f}.png"))
        print("Standbilder fertig")
        return
    ass = build_ass()
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, "nachtschicht_teil1.mp4")
    n = int(D * FPS)
    vf = f"ass='{ass}':fontsdir='{FONTS}'"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(BUILD, "mix.wav"), "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame_at(i / FPS).tobytes())
        if i % 150 == 0:
            print(f"Bild {i}/{n}", flush=True)
    p.stdin.close()
    p.wait()
    print("Fertig:", out)


if __name__ == "__main__":
    main()

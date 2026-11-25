"""Schnitt Nachtschicht Teil 2 (Fassung A oder B): Kamerabilder (Blender, teils aus Teil 1), Ich-Sicht, Fußspuren,
Nachtsicht, Handy, Zettel-Rückseite, Abstimmungs- und Entscheidungskarten, Überwachungskamera-Look, Untertitel (ASS)
und Ton (<zweig>/build/mix.wav aus sound.py).
  <vx>/bin/python nachtschicht-teil2/assemble.py a|b                  -> out/nachtschicht_teil2_<a|b>.mp4
  <vx>/bin/python nachtschicht-teil2/assemble.py a|b --stills 1,14,40 -> <zweig>/build/check_<t>.png
  <vx>/bin/python nachtschicht-teil2/assemble.py a|b --cover          -> out/titelbild_<a|b>.png
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
Z = sys.argv[1]
ZB, SB, OUT = os.path.join(HERE, Z, "build"), os.path.join(HERE, "build"), os.path.join(HERE, "out")
T1B, FONTS = os.path.join(HERE, "..", "nachtschicht-teil1", "build"), os.path.join(HERE, "..", "nachtschicht-teil1", "fonts")
W, H, FPS = 1080, 1920, 30
edl = json.load(open(os.path.join(ZB, "edl.json"), encoding="utf-8"))
tl = json.load(open(os.path.join(ZB, "timeline.json"), encoding="utf-8"))
EV, SHOTS, D = edl["events"], edl["shots"], edl["duration"]
SRC = {"t1r1": os.path.join(T1B, "r1"), "t1r2": os.path.join(T1B, "r2"), "t1r3": os.path.join(T1B, "r3"),
       "tuer": os.path.join(SB, "tuer"), "lager": os.path.join(SB, "lager")}
# Bildpunkte (Quelle 432×768), auf die digital gezoomt wird
FOCUS = {"t1r1": (250, 560), "lager": (250, 380), "ir": (205, 470)}

F_OSD = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", 38)
F_TITLE = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 112)
F_SUB = ImageFont.truetype(os.path.join(FONTS, "Oswald-Bold.ttf"), 48)
F_HEAD = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 92)
F_END = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 86)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.55 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)).clip(0.25, 1)[..., None]
VIG_SOFT = (1 - 0.3 * (((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)).clip(0.5, 1)[..., None]
VIG_IR = (1 - 0.9 * (((xx - W * 0.45) / (W * 0.75)) ** 2 + ((yy - H * 0.5) / (H * 0.62)) ** 2)).clip(0.08, 1)[..., None]
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
@lru_cache(maxsize=None)
def nframes(src):
    return len([f for f in os.listdir(SRC[src]) if f.endswith(".png") and f[:4].isdigit()])


@lru_cache(maxsize=64)
def src_arr(src, k):
    return np.asarray(Image.open(os.path.join(SRC[src], f"{k:04d}.png")).convert("RGB"), dtype=np.float32) / 255


def src_index(spec, t, t0):
    k = spec["frm"] + int((t - t0) * edl["fps_src"])
    last = nframes(spec["src"])
    if spec.get("loop"):
        span = last - spec["frm"] + 1
        k = spec["frm"] + (k - spec["frm"]) % max(1, span)
    return max(1, min(last, k))


def zoom_level(spec, t):
    if not spec.get("zoom"):
        return 1.0
    za, zb, z0, z1 = spec["zoom"]
    return z0 + (z1 - z0) * ease((t - za) / max(0.1, zb - za))


def upscale(a, z=1.0, focus=None, blur=1.1):
    """Quellbild (432×768) auf 1080×1920, bei z > 1 digitaler Zoom auf focus."""
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    if z > 1.001:
        fx, fy = focus or (im.width / 2, im.height / 2)
        sw, sh_ = im.width / z, im.height / z
        cx = min(max(fx, sw / 2), im.width - sw / 2)
        cy = min(max(fy, sh_ / 2), im.height - sh_ / 2)
        im = im.resize((W, H), Image.BICUBIC, box=(cx - sw / 2, cy - sh_ / 2, cx + sw / 2, cy + sh_ / 2))
        blur = blur + 0.6 * (z - 1)
    else:
        im = im.resize((W, H), Image.BICUBIC)
    return np.asarray(im.filter(ImageFilter.GaussianBlur(blur)), dtype=np.float32) / 255


def grade_cctv(a, dim=1.0, noise=0.03):
    y_ = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    a = y_[..., None] + 0.32 * (a - y_[..., None])
    a = np.clip((a - 0.5) * 1.12 + 0.48, 0, 1) ** 1.05
    a = a * np.array([0.95, 1.03, 0.98], dtype=np.float32)
    nz = rng.normal(0, noise, (H // 2, W // 2)).astype(np.float32)
    nz = np.repeat(np.repeat(nz, 2, 0), 2, 1)[..., None]
    return (a + nz) * VIG * SCAN * dim


def to_img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGB")


def osd(img, spec, t, t0, z=1.0, ir=False):
    d = ImageDraw.Draw(img)
    clock = spec["clock"] + int(t - t0)
    hh, mm, ss = clock // 3600, clock % 3600 // 60, clock % 60
    kw = dict(font=F_OSD, fill=(235, 235, 235), stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((70, 292), spec["cam"], **kw)
    d.text((1010, 292), f"24.11.2026  {hh:02d}:{mm:02d}:{ss:02d}", anchor="ra", **kw)
    if (t % 1.0) < 0.6:
        d.ellipse((72, 360, 98, 386), fill=(225, 30, 30))
        d.text((112, 352), "REC", font=F_OSD, fill=(225, 30, 30), stroke_width=3, stroke_fill=(0, 0, 0))
    if ir:
        d.text((1010, 352), "IR  NACHTSICHT", anchor="ra", **kw)
    elif z > 1.05:
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


def with_static_in(a, s, t, dur=0.1):
    if s["id"] != "SH0" and t - s["t"][0] < dur:
        k = (t - s["t"][0]) / dur
        return static_frame(int(t * 1000)) * (1 - k) + a * k
    return a


# ---------------------------------------------------------------- Fußspuren (Differenz mit/ohne Spuren, je Spur eine Maske)
PR_WITH = PR_DIFF = None
PR_MASKS = []
if os.path.exists(os.path.join(SB, "spuren", "spuren.png")) and os.path.exists(os.path.join(SB, "spuren_leer", "spuren_leer.png")):
    w_ = np.asarray(Image.open(os.path.join(SB, "spuren", "spuren.png")).convert("RGB"), dtype=np.float32) / 255
    o_ = np.asarray(Image.open(os.path.join(SB, "spuren_leer", "spuren_leer.png")).convert("RGB"), dtype=np.float32) / 255
    PR_DIFF = w_ - o_
    for poly in json.load(open(os.path.join(SB, "spuren", "spuren.json"))):
        m = Image.new("L", (w_.shape[1], w_.shape[0]), 0)
        ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
        m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
        PR_MASKS.append(np.asarray(m, dtype=np.float32)[..., None] / 255)


def prints_alpha(spec, t):
    n = len(PR_MASKS)
    if spec.get("reveal") == "all":
        return [1.0] * n
    ta, tb = spec["reveal"]
    return [min(1.0, max(0.0, (t - (ta + i * (tb - ta) / max(1, n - 1))) / 0.15)) for i in range(n)]


# ---------------------------------------------------------------- Einstellungen
def render_cctv(s, t, dim=None):
    t0 = s["t"][0]
    a = src_arr(s["src"], src_index(s, t, t0))
    if s["kind"] == "prints" and PR_DIFF is not None:
        al = prints_alpha(s, t)
        add = np.zeros_like(a)
        for m, w in zip(PR_MASKS, al):
            if w > 0:
                add += m * w
        a = np.clip(a + PR_DIFF * np.clip(add, 0, 1), 0, 1)
    z = zoom_level(s, t)
    a = grade_cctv(upscale(a, z, FOCUS.get(s["src"])), s.get("dim", 1.0) if dim is None else dim)
    if s.get("out"):                                   # „Das Licht geht aus“: Flackern, dann schwarz
        f0, f1 = s["out"]
        if f0 <= t < f1:
            g = np.random.default_rng(int(t * 10))
            a = a * (0.12 if g.random() < 0.5 else 1.0)
        elif t >= f1:
            a = rng.normal(0.02, 0.015, (H, W, 1)).astype(np.float32).repeat(3, axis=2)
            return to_img(a)
    a = with_static_in(a, s, t)
    img = to_img(a)
    osd(img, s, t, t0, z)
    return img


def render_pov(s, t):
    """Ich-Sicht: etwas mehr Farbe als die Kameras, weicher, Korn, Vignette, kein Bildschirmtext."""
    t0 = s["t"][0]
    k = min(nframes("tuer"), 1 + int((t - t0) * edl["fps_src"]))
    a = upscale(src_arr("tuer", k), 1.0, blur=0.9)
    y_ = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    a = y_[..., None] + 0.55 * (a - y_[..., None])
    a = np.clip((a - 0.5) * 1.1 + 0.47, 0, 1) * np.array([0.93, 1.0, 1.06], dtype=np.float32)
    a = (a + rng.normal(0, 0.025, (H, W, 1)).astype(np.float32)) * VIG
    return to_img(with_static_in(a, s, t))


ASSET = {}
for f_ in os.listdir(os.path.join(SB, "assets")) if os.path.isdir(os.path.join(SB, "assets")) else []:
    if f_.endswith(".png") and not f_.startswith("_"):
        ASSET[f_[:-4]] = Image.open(os.path.join(SB, "assets", f_)).convert("RGBA")


def paste_alpha(base, im, x, y, alpha=1.0):
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(im, (int(x), int(y)))


def render_phone(s, t):
    dx = 0
    for b in s.get("buzz", []) + [n_[1] - 0.05 for n_ in s["notifs"][1:]]:
        if b <= t < b + 0.38:
            dx = 9 * math.sin(2 * math.pi * 38 * (t - b))
    img = Image.new("RGBA", (W, H))
    img.alpha_composite(ASSET[s["lock"]], (int(dx), 0))
    for key, at, y in s["notifs"]:
        if t >= at:
            p = ease((t - at) / 0.35)
            paste_alpha(img, ASSET[key], 140 + dx, y - 120 * (1 - p), p)
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255
    a = (a + rng.normal(0, 0.015, (H, W, 1)).astype(np.float32)) * VIG_SOFT
    return to_img(with_static_in(a, s, t, 0.08))


def render_chat(s, t):
    im = ASSET[s["img"]]
    top_end, top_start = 0, im.height - H
    sa, sb = s["scroll"]
    y = top_start + (top_end - top_start) * ease((t - sa) / max(0.1, sb - sa))
    crop = im.crop((0, int(y), W, int(y) + H)).convert("RGB")
    a = np.asarray(crop, dtype=np.float32) / 255
    a = (a + rng.normal(0, 0.012, (H, W, 1)).astype(np.float32)) * VIG_SOFT
    return to_img(with_static_in(a, s, t, 0.06))


def render_vote(s, t):
    t0 = s["t"][0]
    a = grade_cctv(upscale(src_arr(s["src"], src_index(s, t, t0))), s.get("dim", 0.45))
    a = with_static_in(a, s, t)
    img = to_img(a).convert("RGBA")
    d = ImageDraw.Draw(img)
    if t >= t0 + 0.15:
        d.text((540, 640), "IHR HABT", font=F_HEAD, fill=(235, 235, 230), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        d.text((540, 750), "ENTSCHIEDEN", font=F_HEAD, fill=(225, 40, 45), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    card = ASSET[s["card"]]
    if t >= t0 + 0.45:
        p = ease_out_back((t - t0 - 0.45) / 0.5)
        sc_ = 0.6 + 0.4 * p
        c2 = card.resize((max(1, int(card.width * sc_)), max(1, int(card.height * sc_))), Image.LANCZOS)
        paste_alpha(img, c2, (W - c2.width) // 2, 930 + (card.height - c2.height) // 2, min(1.0, p * 1.5))
    out = img.convert("RGB")
    osd(out, s, t, t0)
    return out


@lru_cache(maxsize=1)
def ir_base():
    a = np.asarray(Image.open(os.path.join(SB, "ir", "ir.png")).convert("RGB"), dtype=np.float32) / 255
    return a


def render_ir(s, t, dim=1.0):
    t0 = s["t"][0]
    z = zoom_level(s, t)
    a = upscale(ir_base(), z, FOCUS["ir"], blur=1.3)
    y_ = a @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    y_ = np.clip((y_ - 0.06) * 1.5, 0, 1) ** 0.85                       # Nachtsicht: grau, harte Kontraste
    hi = np.clip((y_ - 0.75) / 0.25, 0, 1)                               # leuchtende Augen etwas überstrahlen
    hi = np.asarray(Image.fromarray((hi * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)), dtype=np.float32) / 255
    a = (y_ + hi * 0.8)[..., None] * np.array([0.9, 1.0, 0.94], dtype=np.float32)
    g = np.random.default_rng(int(t * 30))
    nz = g.normal(0, 0.055, (H // 3, W // 3)).astype(np.float32)
    a = a + np.repeat(np.repeat(nz, 3, 0), 3, 1)[..., None]
    if g.random() < 0.12:                                                # gelegentlich eine helle Zeile
        y0 = int(g.integers(300, H - 300))
        a[y0:y0 + 6] += 0.25
    a = a * VIG_IR * SCAN * dim
    if t - t0 < 0.3:                                                     # Umschalten auf Nachtsicht
        a = glitch(a, 1.3, int(t * 100))
        if t - t0 < 0.08:
            a = np.clip(a * 2.2 + 0.2, 0, 1)
    img = to_img(a)
    osd(img, s, t, t0, z, ir=True)
    return img


@lru_cache(maxsize=1)
def note_data():
    a = np.asarray(Image.open(os.path.join(SB, "zettel_rueck", "zettel_rueck.png")).convert("RGB"), dtype=np.float32) / 255
    return a, json.load(open(os.path.join(SB, "zettel_rueck", "boxes.json")))


def note_state(name):
    _, BOXES = note_data()
    if name == "all":
        bs = list(BOXES.values())
        x0, y0, x1, y1 = min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)
        return ((x0 + x1) / 2, (y0 + y1) / 2 + 30, 1.45)
    x0, y0, x1, y1 = BOXES[name]
    s_ = min(3.0, max(1.7, W * 0.9 / (x1 - x0 + 24)))
    return ((x0 + x1) / 2, (y0 + y1) / 2, s_)


def render_note(s, t):
    A, _ = note_data()
    keys = s["keys"]
    st_ = note_state(keys[0][1])
    for kt, name in keys:
        if t >= kt - 0.15:
            prev, nxt = st_, note_state(name)
            p = ease((t - kt + 0.15) / 0.65)
            st_ = tuple(prev[j] + (nxt[j] - prev[j]) * p for j in range(3))
    cx, cy, sc = st_
    last = keys[-1][0]
    if t >= last:                                                        # „Versteck dich“: kurzer Ruck
        sc *= 1 + 0.06 * math.exp(-(t - last) * 6)
    sc *= 1 + 0.012 * math.sin(t * 0.7)
    cx += 3 * math.sin(1.3 * t) + 2 * math.sin(2.9 * t + 1)
    cy += 3 * math.cos(1.1 * t) + 2 * math.sin(2.3 * t)
    im = Image.fromarray((A * 255).astype(np.uint8))
    sw, sh_ = W / sc, H / sc
    cx = min(max(cx, sw / 2), im.width - sw / 2)
    cy = min(max(cy, sh_ / 2), im.height - sh_ / 2)
    b = np.asarray(im.resize((W, H), Image.BICUBIC, box=(cx - sw / 2, cy - sh_ / 2, cx + sw / 2, cy + sh_ / 2)), dtype=np.float32) / 255
    b = (b * 0.95 + rng.normal(0, 0.02, (H, W, 1)).astype(np.float32)) * VIG_SOFT
    return to_img(with_static_in(b, s, t))


def render_decision(s, t):
    t0 = s["t"][0]
    if t >= s["end"]:
        img = to_img(np.zeros((H, W, 3), np.float32) + rng.normal(0, 0.012, (H, W, 1)).astype(np.float32).clip(0, 1))
        d = ImageDraw.Draw(img)
        d.text((540, 860), "TEIL 3 FOLGT", font=F_END, fill=(230, 230, 225), anchor="mm")
        d.text((540, 980), "KOMMENTIERE  A  ODER  B", font=F_SUB, fill=(225, 40, 45), anchor="mm")
        return img
    if s["base"] == "ir":
        img = render_ir(dict(s, t=[t0 - 5, s["t"][1]], zoom=None), t, dim=0.55)
    else:
        a = grade_cctv(upscale(src_arr(s["src"], src_index(s, t, t0))), s.get("dim", 0.5))
        red = 0.06 + 0.04 * math.sin(t * 3)
        a = a * (1 - red) + np.array([0.5, 0.0, 0.02], dtype=np.float32) * red
        img = to_img(with_static_in(a, s, t))
        osd(img, s, t, t0)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)
    if t >= t0 + 0.2:
        d.text((540, 470), "DU ENTSCHEIDEST", font=F_HEAD, fill=(225, 40, 45), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    A_, B_ = [ASSET[k].resize((int(ASSET[k].width * 0.8), int(ASSET[k].height * 0.8)), Image.LANCZOS) for k in s["cards"]]
    ca, cb = s["card_t"]
    x_end = (W - A_.width) // 2
    if t >= ca:
        img.alpha_composite(A_, (int(-A_.width + (x_end + A_.width) * ease_out_back((t - ca) / 0.45)), 975))
    if t >= cb:
        img.alpha_composite(B_, (int(W + (x_end - W) * ease_out_back((t - cb) / 0.45)), 1175))
    return img.convert("RGB")


def render_title(img, t):
    d = ImageDraw.Draw(img)
    k = min(1.0, t / 0.2)
    col = (int(225 * k), int(36 * k), int(42 * k))
    d.text((540, 540), "NACHTSCHICHT", font=F_TITLE, fill=col, anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((540, 650), "TEIL 2  ·  DU ENTSCHEIDEST", font=F_SUB, fill=(240, 240, 240), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))


def frame_at(t):
    s = next((x for x in SHOTS if x["t"][0] <= t < x["t"][1]), SHOTS[-1])
    k = s["kind"]
    if k in ("cctv", "prints"):
        img = render_cctv(s, t)
        if s.get("title"):
            render_title(img, t)
        return img
    return {"pov": render_pov, "phone": render_phone, "chat": render_chat, "vote": render_vote, "ir": render_ir,
            "note": render_note, "decision": render_decision}[k](s, t)


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
            width = F_CAP.getlength(plain) * 1.04
            fs = 104 if width <= 740 else int(104 * 740 / width)
            parts = []
            for w, style in c["words"]:
                w = w.replace("{", "(").replace("}", ")")
                parts.append("{\\c&H003030FF&}" + w + "{\\c&H00FFFFFF&}" if style in ("g", "r") else w)
            txt = "{\\fs%d\\fscx86\\fscy86\\t(0,90,\\fscx100\\fscy100)}" % fs + " ".join(parts)
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{txt}")
    path = os.path.join(ZB, "captions.ass")
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")
    return path


def cover():
    if Z == "a":
        img = render_ir(dict(next(s for s in SHOTS if s["kind"] == "ir"), zoom=None), next(s for s in SHOTS if s["kind"] == "ir")["t"][0] + 1.0)
        l1, l2 = "DIE SPUREN ENDEN", "HINTER DIR."
    else:
        s6 = next(s for s in SHOTS if s["id"] == "SH6")
        img = render_cctv(dict(s6, zoom=[0, 1, 1.25, 1.25]), s6["t"][0] + 2.0)
        l1, l2 = "DIE HINTERTÜR", "STEHT OFFEN."
    d = ImageDraw.Draw(img)
    big = ImageFont.truetype(os.path.join(FONTS, "SpecialElite-Regular.ttf"), 132)
    q = ImageFont.truetype(os.path.join(FONTS, "Oswald-Bold.ttf"), 104)
    d.text((540, 520), "NACHTSCHICHT", font=big, fill=(225, 36, 42), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
    d.text((540, 650), "TEIL 2", font=F_SUB, fill=(240, 240, 240), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((540, 1250), l1, font=q, fill=(255, 255, 255), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((540, 1370), l2, font=q, fill=(255, 48, 48), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    d.text((540, 1480), "DU ENTSCHEIDEST · A ODER B", font=F_SUB, fill=(230, 230, 230), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, f"titelbild_{Z}.png"))
    print("Titelbild fertig")


def main():
    args = sys.argv[2:]
    if "--cover" in args:
        cover()
        return
    if "--stills" in args:
        for x in args[args.index("--stills") + 1].split(","):
            frame_at(float(x)).save(os.path.join(ZB, f"check_{float(x):05.2f}.png"))
        print("Standbilder fertig")
        return
    ass = build_ass()
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"nachtschicht_teil2_{Z}.mp4")
    n = int(D * FPS)
    vf = f"ass='{ass}':fontsdir='{FONTS}'"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", os.path.join(ZB, "mix.wav"), "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "12M",
           "-bufsize", "24M", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-13.3:TP=-1.0:LRA=11", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", out]
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

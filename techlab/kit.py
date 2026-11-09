"""Shared detail kit for the TikTok physics videos: formulas, callouts, gauges, mini charts."""
import functools
import io
import math

import matplotlib
import numpy as np
import skia

matplotlib.use("Agg")
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

matplotlib.rcParams["mathtext.fontset"] = "cm"

FD = "/usr/share/fonts/opentype/inter/"
TF_SEMI = skia.Typeface.MakeFromFile(FD + "Inter-SemiBold.otf")
TF_MONO = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf")
TF_MONO_M = skia.Typeface.MakeFromFile("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf")
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear)


@functools.lru_cache(maxsize=64)
def font(tf_name, size):
    tf = {"mono": TF_MONO, "monom": TF_MONO_M, "semi": TF_SEMI}[tf_name]
    f = skia.Font(tf, size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def C(rgb, a=255):
    return skia.Color(int(rgb[0]), int(rgb[1]), int(rgb[2]), int(max(0, min(255, a))))


def paint(color, stroke=None, blur=None, plus=False):
    p = skia.Paint(AntiAlias=True, Color=color)
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if plus:
        p.setBlendMode(skia.BlendMode.kPlus)
    return p


def hsh(*a):
    x = math.sin(sum((i + 1) * 12.9898 * v for i, v in enumerate(a)) + 78.233) * 43758.5453
    return x - math.floor(x)


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def window(t, t0, t1, fin=0.35, fout=0.3):
    """0..1 visibility of an element shown in [t0, t1)."""
    if t < t0 or t >= t1:
        return 0.0
    return min(1.0, (t - t0) / fin, (t1 - t) / fout)


# ------------------------------------------------------------------ formulas (matplotlib mathtext -> skia image)
@functools.lru_cache(maxsize=256)
def formula(tex, size=40, color=(255, 255, 255)):
    fig = Figure(figsize=(0.01, 0.01), dpi=100)
    FigureCanvasAgg(fig)
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${tex}$", fontsize=size * 0.72, color="#%02x%02x%02x" % tuple(int(v) for v in color))
    buf = io.BytesIO()
    fig.savefig(buf, dpi=100, transparent=True, bbox_inches="tight", pad_inches=0.03, format="png")
    return skia.Image.MakeFromEncoded(skia.Data.MakeWithCopy(buf.getvalue()))


def draw_formula(c, tex, x, y, size=40, color=(255, 255, 255), alpha=1.0, anchor="left", glow=None):
    if alpha <= 0.01:
        return 0, 0
    img = formula(tex, size, tuple(int(v) for v in color))
    w, h = img.width(), img.height()
    if anchor == "center":
        x -= w / 2
    elif anchor == "right":
        x -= w
    p = skia.Paint(Alphaf=min(1.0, alpha))
    if glow is not None:
        g = skia.Paint(Alphaf=min(1.0, alpha) * 0.6)
        g.setImageFilter(skia.ImageFilters.Blur(6, 6))
        c.drawImage(formula(tex, size, tuple(int(v) for v in glow)), x, y, SAMP, g)
    c.drawImage(img, x, y, SAMP, p)
    return w, h


def formula_card(c, tex, cx, cy, size, color, alpha, accent):
    """Big centred formula on a translucent card."""
    if alpha <= 0.01:
        return
    img = formula(tex, size, tuple(int(v) for v in color))
    w, h = img.width() + 56, img.height() + 30
    sc = 0.92 + 0.08 * ease(alpha)
    c.save()
    c.translate(cx, cy)
    c.scale(sc, sc)
    rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 18, 18)
    c.drawRRect(rr, paint(C((8, 9, 22), 238 * alpha)))
    c.drawRRect(rr, paint(C(accent, 170 * alpha), stroke=2))
    p = skia.Paint(Alphaf=min(1.0, alpha))
    c.drawImage(img, -img.width() / 2, -img.height() / 2, SAMP, p)
    c.restore()


# ------------------------------------------------------------------ text helpers
def typing(text, prog):
    n = int(round(len(text) * max(0.0, min(1.0, prog))))
    return text[:n]


def label_box(c, text, x, y, color, alpha=1.0, size=24, align="left", bg=(8, 9, 22)):
    f = font("mono", size)
    w = f.measureText(text) + 20
    h = size + 14
    if align == "right":
        x -= w
    elif align == "center":
        x -= w / 2
    r = skia.Rect(x, y - h / 2, x + w, y + h / 2)
    c.drawRoundRect(r, 8, 8, paint(C(bg, 200 * alpha)))
    c.drawRoundRect(r, 8, 8, paint(C(color, 200 * alpha), stroke=1.6))
    c.drawString(text, x + 10, y + size * 0.36, f, paint(C((255, 255, 255), 255 * alpha)))
    return r


def callout(c, t, t0, t1, anchor, label_pos, text, color, size=24):
    """Leader-line callout that types itself in. anchor/label_pos: (x, y)."""
    a = window(t, t0, t1, 0.25, 0.25)
    if a <= 0.01:
        return
    prog = min(1.0, (t - t0) / 0.45)
    ax, ay = anchor
    lx, ly = label_pos
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 1.5 * (t - t0))
    c.drawCircle(ax, ay, 5, paint(C(color, 255 * a)))
    c.drawCircle(ax, ay, 9 + 5 * pulse, paint(C(color, 120 * a * (1 - pulse)), stroke=2))
    ex = lx - (20 if lx > ax else -20)
    seg = min(1.0, prog * 2)
    mx, my = ax + (ex - ax) * seg, ay + (ly - ay) * seg
    c.drawLine(ax, ay, mx, my, paint(C(color, 220 * a), stroke=2))
    if prog > 0.5:
        c.drawLine(ex, ly, lx, ly, paint(C(color, 220 * a), stroke=2))
        txt = typing(text, (prog - 0.5) * 2)
        if txt:
            label_box(c, txt, lx, ly, color, a, size, "left" if lx > ax else "right")


def readout(c, x, y, key, value, color, alpha=1.0, size=20):
    fk = font("monom", size)
    fv = font("mono", size)
    c.drawString(key, x, y, fk, paint(C((255, 255, 255), 130 * alpha)))
    c.drawString(value, x + fk.measureText(key) + 8, y, fv, paint(C(color, 255 * alpha)))


def chip(c, text, x, y, color, on, size=18):
    f = font("mono", size)
    w = f.measureText(text) + 18
    r = skia.Rect(x, y - size, x + w, y + 8)
    if on:
        c.drawRoundRect(r, 6, 6, paint(C(color, 230)))
        c.drawString(text, x + 9, y, f, paint(skia.Color(10, 10, 20)))
    else:
        c.drawRoundRect(r, 6, 6, paint(C(color, 90), stroke=1.4))
        c.drawString(text, x + 9, y, f, paint(C(color, 120)))
    return w


def timecode(c, x, y, label, t, color=(255, 80, 90), start_s=3 * 3600 + 7):
    s = int(start_s + t)
    hh, mm, ss_ = (s // 3600) % 24, (s // 60) % 60, s % 60
    f = font("mono", 20)
    if int(t * 2) % 2 == 0:
        c.drawCircle(x + 6, y - 6, 6, paint(C(color)))
    txt = f"{label}  {hh:02d}:{mm:02d}:{ss_:02d}  FR {int(t * 60) % 60:02d}"
    c.drawString(txt, x + 20, y, f, paint(skia.Color(255, 255, 255, 170)))


# ------------------------------------------------------------------ gauges & mini charts
def tach(c, cx, cy, r, value, vmax, label, color, red_from=None):
    c.drawCircle(cx, cy, r + 8, paint(skia.Color(8, 9, 22, 210)))
    c.drawCircle(cx, cy, r + 8, paint(C(color, 120), stroke=2))
    a0, a1 = 150, 390
    c.drawArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), a0, a1 - a0, False, paint(skia.Color(255, 255, 255, 50), stroke=6))
    if red_from is not None:
        ar = a0 + (a1 - a0) * red_from / vmax
        c.drawArc(skia.Rect(cx - r, cy - r, cx + r, cy + r), ar, a1 - ar, False, paint(skia.Color(255, 60, 80, 160), stroke=6))
    for k in range(11):
        a = math.radians(a0 + (a1 - a0) * k / 10)
        r0 = r - (14 if k % 5 == 0 else 8)
        c.drawLine(cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a),
                   paint(skia.Color(255, 255, 255, 140), stroke=2))
    v = max(0.0, min(vmax, value))
    a = math.radians(a0 + (a1 - a0) * v / vmax)
    c.drawLine(cx, cy, cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a), paint(C(color), stroke=4))
    c.drawCircle(cx, cy, 7, paint(C(color)))
    f = font("mono", 22)
    s = f"{value:,.0f}"
    c.drawString(s, cx - f.measureText(s) / 2, cy + r * 0.55, f, paint(skia.Color(255, 255, 255)))
    fl = font("monom", 15)
    c.drawString(label, cx - fl.measureText(label) / 2, cy + r * 0.55 + 20, fl, paint(skia.Color(255, 255, 255, 140)))


def log_x(f, lo, hi, x0, x1):
    return x0 + (x1 - x0) * (math.log(max(f, lo)) - math.log(lo)) / (math.log(hi) - math.log(lo))


def spectrum(c, x0, y0, x1, y1, partials, lo=50, hi=10000, color=(255, 176, 60), alpha=1.0):
    """partials: list of (freq, amp 0..1)."""
    c.drawLine(x0, y1, x1, y1, paint(skia.Color(255, 255, 255, int(50 * alpha)), stroke=1.2))
    fl = font("monom", 14)
    for f, lab in ((100, "100"), (1000, "1k"), (5000, "5k")):
        x = log_x(f, lo, hi, x0, x1)
        c.drawLine(x, y1, x, y1 + 5, paint(skia.Color(255, 255, 255, int(80 * alpha)), stroke=1))
        c.drawString(lab, x - fl.measureText(lab) / 2, y1 + 19, fl, paint(skia.Color(255, 255, 255, int(110 * alpha))))
    for f, a in partials:
        if f < lo or f > hi or a < 0.01:
            continue
        x = log_x(f, lo, hi, x0, x1)
        h = (y1 - y0) * min(1.0, a)
        c.drawLine(x, y1, x, y1 - h, paint(C(color, 230 * alpha), stroke=3.5))
        c.drawCircle(x, y1 - h, 3, paint(C((255, 255, 255), 230 * alpha)))


def waves(c, x0, y0, x1, y1, series, phase=0.0, alpha=1.0, mark_every=None):
    """series: list of (cycles across the width, color). Optional alignment marks every `mark_every` px fraction."""
    ym = (y0 + y1) / 2
    amp = (y1 - y0) / 2 * 0.85
    c.drawLine(x0, ym, x1, ym, paint(skia.Color(255, 255, 255, int(35 * alpha)), stroke=1))
    for cyc, col in series:
        p = skia.Path()
        n = 220
        for k in range(n + 1):
            u = k / n
            x = x0 + (x1 - x0) * u
            y = ym - amp * math.sin(2 * math.pi * cyc * u + phase * cyc)
            (p.moveTo if k == 0 else p.lineTo)(x, y)
        c.drawPath(p, paint(C(col, 230 * alpha), stroke=2.6))
    if mark_every:
        for u in mark_every:
            x = x0 + (x1 - x0) * u
            c.drawLine(x, y0 - 6, x, y1 + 6, paint(skia.Color(255, 255, 255, int(110 * alpha)), stroke=1.5))


WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11]


def keyboard(c, x0, y0, x1, y1, lo, hi, active, alpha=1.0, names=True):
    """Mini piano from MIDI lo..hi (inclusive). active: {midi: color}."""
    whites = [m for m in range(lo, hi + 1) if m % 12 in WHITE_KEYS]
    ww = (x1 - x0) / len(whites)
    pos = {}
    for i, m in enumerate(whites):
        r = skia.Rect(x0 + i * ww, y0, x0 + (i + 1) * ww - 2, y1)
        col = active.get(m)
        c.drawRoundRect(r, 4, 4, paint(C(col if col else (225, 228, 240), 255 * alpha)))
        pos[m] = (r.centerX(), y1)
        if names and m % 12 in (2, 5, 9) and col:
            nm = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][m % 12] + str(m // 12 - 1)
            f = font("mono", 14)
            c.drawString(nm, r.centerX() - f.measureText(nm) / 2, y1 - 8, f, paint(skia.Color(10, 10, 20, int(255 * alpha))))
    bh = (y1 - y0) * 0.6
    for m in range(lo, hi + 1):
        if m % 12 in WHITE_KEYS:
            continue
        left = max([w for w in whites if w < m], default=None)
        if left is None:
            continue
        i = whites.index(left)
        xc = x0 + (i + 1) * ww - 1
        r = skia.Rect(xc - ww * 0.3, y0, xc + ww * 0.3, y0 + bh)
        col = active.get(m)
        c.drawRoundRect(r, 3, 3, paint(C(col if col else (24, 26, 40), 255 * alpha)))
    return pos


def phase_circle(c, cx, cy, r, phases, colors, R, Psi, alpha=1.0, label="R"):
    c.drawCircle(cx, cy, r + 10, paint(skia.Color(8, 9, 22, int(200 * alpha))))
    c.drawCircle(cx, cy, r, paint(skia.Color(255, 255, 255, int(70 * alpha)), stroke=1.5))
    for k in range(12):
        a = 2 * math.pi * k / 12
        c.drawLine(cx + (r - 5) * math.cos(a), cy + (r - 5) * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a),
                   paint(skia.Color(255, 255, 255, int(70 * alpha)), stroke=1))
    for i, ph in enumerate(phases):
        col = colors[i] if isinstance(colors, (list, tuple)) and len(colors) == len(phases) and isinstance(colors[0], tuple) else colors
        c.drawCircle(cx + r * math.cos(ph), cy + r * math.sin(ph), 3.2, paint(C(col, 220 * alpha)))
    ex, ey = cx + r * R * math.cos(Psi), cy + r * R * math.sin(Psi)
    c.drawLine(cx, cy, ex, ey, paint(skia.Color(255, 255, 255, int(240 * alpha)), stroke=3))
    c.drawCircle(ex, ey, 5, paint(skia.Color(255, 255, 255, int(255 * alpha))))
    f = font("mono", 16)
    s = f"{label} = {R:0.2f}"
    c.drawString(s, cx - f.measureText(s) / 2, cy + r + 30, f, paint(skia.Color(255, 255, 255, int(190 * alpha))))


def dust(c, t, x0, y0, x1, y1, n, seed, color=(255, 230, 200), alpha=1.0, size=2.2):
    for k in range(n):
        u = hsh(seed, k, 1)
        v = hsh(seed, k, 2)
        sp = 6 + 14 * hsh(seed, k, 3)
        x = x0 + ((u * (x1 - x0) + sp * t + 10 * math.sin(0.7 * t + k)) % (x1 - x0))
        y = y0 + ((v * (y1 - y0) - 0.4 * sp * t + 8 * math.cos(0.5 * t + 2 * k)) % (y1 - y0))
        tw = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(2.3 * t + 7 * k))
        c.drawCircle(x, y, size * (0.6 + 0.8 * hsh(seed, k, 4)), paint(C(color, 160 * alpha * tw)))

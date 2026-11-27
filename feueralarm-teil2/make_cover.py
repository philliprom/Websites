"""Titelbild (1080x1920) aus einem Standbild in voller Auflösung + Schlagzeile.

  python3 make_cover.py <standbild.png>  ->  out/titelbild.png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "assets", "fonts", "Nunito-Black.ttf")
W, H = 1080, 1920


sys.path.insert(0, HERE)
from story import PART  # noqa: E402

SCHLAGZEILE = [("DAS IST DAS", False), ("FALSCHE", False), ("AUTO.", True)]


def font(sz):
    return ImageFont.truetype(FONT, sz)


def centered(d, y, text, f, fill, stroke=12):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=(8, 8, 10))


def main():
    src = Image.open(sys.argv[1]).convert("RGB").resize((W, H))
    # leicht hineinzoomen auf das Gesicht, Kontrast etwas hoch
    z = 1.3
    cw, ch = int(W / z), int(H / z)
    x0, y0 = (W - cw) // 2 - 10, 110   # Gesicht unten in der Mitte, Schrift oben auf Wand und Uhr
    y0 = max(0, min(H - ch, y0))
    img = src.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.1)
    # oben abdunkeln für die Schrift
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(0, 1000):
        sd.line((0, y, W, y), fill=int(185 * max(0, 1 - y / 1000) ** 1.3))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shade)
    d = ImageDraw.Draw(img)
    # Pille oben
    t = "POV: FEUERALARM"
    f = font(60)
    w = d.textlength(t, font=f)
    d.rounded_rectangle(((W - w) / 2 - 40, 250, (W + w) / 2 + 40, 342), 46, fill=(255, 204, 0))
    d.text(((W - w) / 2, 258), t, font=f, fill=(15, 15, 15))
    for k, (zeile, rot) in enumerate(SCHLAGZEILE):
        centered(d, 380 + 150 * k, zeile, font(146), (255, 59, 48) if rot else (255, 255, 255))
    # Teil
    f2 = font(46)
    d.rounded_rectangle((W / 2 - 110, 880, W / 2 + 110, 956), 22, fill=(214, 40, 40))
    d.text((W / 2 - d.textlength(PART, font=f2) / 2, 886), PART, font=f2, fill=(255, 255, 255))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    img.save(os.path.join(HERE, "out", "titelbild.png"))
    img.resize((540, 960)).save(os.path.join(HERE, "build", "titelbild_klein.png"))
    print("Titelbild fertig")


if __name__ == "__main__":
    main()

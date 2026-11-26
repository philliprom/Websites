"""Titelbild für Tech-Lupe „Passwort“ im Stil der Serie (großer Titel oben, Pille unten) über dem ersten Bild der
HyperFrames-Komposition (vor dem ersten Untertitel). Aufruf (vx): python techlupe-passwort/make_cover.py <bild.png>
"""
import os
import sys

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
tmp = os.path.join(HERE, "build", "fredoka700.ttf")
if not os.path.exists(tmp):
    f = TTFont(os.path.join(HERE, "assets", "fonts", "TLFredoka-700.woff2"))
    f.flavor = None
    f.save(tmp)
img = Image.open(sys.argv[1]).convert("RGB").resize((1080, 1920))
d = ImageDraw.Draw(img)
big = ImageFont.truetype(tmp, 132)
for y, txt, col in ((330, "SIE KENNT DEIN", (255, 255, 255)), (470, "PASSWORT NICHT!", (255, 75, 92))):
    d.text((540, y), txt, font=big, fill=col, anchor="mm", stroke_width=20, stroke_fill=(11, 16, 34))
pill = ImageFont.truetype(tmp, 52)
txt = "…NUR EINEN HASH. 🔐"
txt = "…NUR EINEN HASH."
w = d.textlength(txt, font=pill)
x0, y0 = 540 - w / 2 - 36, 1150
d.rounded_rectangle((x0, y0, x0 + w + 72, y0 + 96), radius=48, fill=(61, 220, 255))
d.text((540, y0 + 48), txt, font=pill, fill=(11, 16, 34), anchor="mm")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
img.save(os.path.join(HERE, "out", "titelbild.png"))
print("Titelbild fertig")

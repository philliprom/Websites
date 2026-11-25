"""Profilbild für den Kanal „Nachtschicht – Du entscheidest“ aus dem Blender-Render (Einstellung „profil“).
  1. Render:  <bl>/bin/python nachtschicht-teil1/scene.py --shot profil … (Befehl in nachtschicht-teil1/build/profil/befehl.txt)
  2. Nachbearbeitung:  <vx>/bin/python nachtschicht-kanal/profilbild.py
     -> out/profilbild.png        (1080×1080, ohne Schrift; TikTok schneidet rund zu)
        out/profilbild_rec.png    (Variante im Überwachungskamera-Look mit rotem „● REC“)
        out/profilbild_vorschau.png  (rund, groß und klein, auf dunklem und hellem Hintergrund)
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "nachtschicht-teil1", "build", "profil", "profil_1080.png")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(47)

a = np.asarray(Image.open(SRC).convert("RGB")).astype(np.float32) / 255
H, W = a.shape[:2]
lum = lambda x: x @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)  # noqa: E731


def blur(x, r):
    return np.asarray(Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


# Leuchten um helle Stellen (Augen, Dachlicht): zwei weiche Schichten, Augen leicht kühl-grünlich
hi = np.clip((lum(a) - 0.62) / 0.38, 0, 1)[..., None] * np.array([0.86, 1.0, 0.94], dtype=np.float32)
a = a + blur(hi, 5) * 0.55 + blur(hi, 18) * 0.45 + blur(hi, 48) * 0.25
# Augen zusätzlich weit leuchten lassen (nur im Bereich der Augen), damit sie auch im 56-px-Rundbild zu sehen sind
yy0, xx0 = np.mgrid[0:H, 0:W].astype(np.float32)
near = np.exp(-(((xx0 - 0.5 * W) / (0.13 * W)) ** 2 + ((yy0 - 0.43 * H) / (0.09 * H)) ** 2))[..., None]
eye = np.clip((lum(a) - 0.8) / 0.2, 0, 1)[..., None] * near * np.array([0.8, 1.0, 0.9], dtype=np.float32)
a = a + blur(eye, 14) * 0.9 + blur(eye, 40) * 0.8
# Farbe: Schwarz leicht blaugrün angehoben, sanfte S-Kurve
lift = np.array([0.012, 0.018, 0.026], dtype=np.float32)
a = a * (1 - lift) + lift
a = np.clip(a, 0, 1)
a = a * 0.7 + (a * a * (3 - 2 * a)) * 0.3
# Vignette (Mitte betont, das Bild wird ohnehin rund zugeschnitten)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot((xx - W / 2) / (W / 2), (yy - H * 0.45) / (H / 2))
a = a * (1 - 0.5 * np.clip((r - 0.45) / 0.7, 0, 1) ** 1.4)[..., None]


def grain(x, s):
    return x + (rng.standard_normal((H, W)).astype(np.float32) * s * (1 - 0.6 * lum(np.clip(x, 0, 1))))[..., None]


main = np.clip(grain(a, 0.016), 0, 1)
Image.fromarray((main * 255).astype(np.uint8)).save(os.path.join(OUT, "profilbild.png"), optimize=True)

# Variante Überwachungskamera: fast schwarzweiß, Zeilen, mehr Rauschen, rotes „● REC“ (liegt innerhalb des Kreises)
g = lum(a)[..., None]
cam = a * 0.25 + g * np.array([0.92, 1.0, 0.96], dtype=np.float32) * 0.75
cam = cam * (1 - 0.07 * ((np.arange(H) % 4) < 2).astype(np.float32))[:, None, None]
cam = np.clip(grain(cam, 0.03), 0, 1)
im = Image.fromarray((cam * 255).astype(np.uint8))
d = ImageDraw.Draw(im)
f = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf", 62)
x0, y0 = 250, 215
d.ellipse((x0, y0 + 14, x0 + 44, y0 + 58), fill=(235, 30, 36))
d.text((x0 + 64, y0), "REC", font=f, fill=(235, 30, 36))
im.save(os.path.join(OUT, "profilbild_rec.png"), optimize=True)


# Vorschau: so erscheint es rund im Profil (groß) und neben Kommentaren (klein), dunkel und hell
def circ(img, size):
    s = img.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    s.putalpha(m.resize((size, size), Image.LANCZOS))
    return s


imgs = [Image.open(os.path.join(OUT, n)).convert("RGB") for n in ("profilbild.png", "profilbild_rec.png")]
sheet = Image.new("RGB", (2 * 520, 2 * 400), (18, 18, 18))
ImageDraw.Draw(sheet).rectangle((0, 400, 1040, 800), fill=(255, 255, 255))
for c, img in enumerate(imgs):
    for row in range(2):
        ox, oy = c * 520 + 40, row * 400 + 40
        sheet.paste(circ(img, 320), (ox, oy), circ(img, 320))
        sheet.paste(circ(img, 56), (ox + 360, oy + 132), circ(img, 56))
sheet.save(os.path.join(OUT, "profilbild_vorschau.png"), optimize=True)
print("Profilbilder fertig:", ", ".join(sorted(os.listdir(OUT))))

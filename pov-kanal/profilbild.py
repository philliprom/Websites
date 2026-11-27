"""Profilbild für den POV-Kanal „Unbekannte Nummer“ (1080x1080, wird rund angezeigt).

1. Bildschirm-Textur (großes gelbes „?“ der unbekannten Nummer)       python3 profilbild.py textur
2. Toon-Hand mit Handy in Blender (wie im Video), freigestellt       EGL_PLATFORM=surfaceless bl/bin/python profilbild.py render
3. Zusammensetzen: dunkler Grund, gelber Ring, Leuchten             python3 profilbild.py bild
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(HERE, "..", "feueralarm-teil1")
FONT = os.path.join(FA, "assets", "fonts", "Nunito-Black.ttf")
BUILD = os.path.join(HERE, "build")
YELLOW = (255, 204, 0)


def textur():
    from PIL import Image, ImageDraw, ImageFont
    W, H = 540, 1160
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = y / H
            px[x, y] = (int(16 + 16 * t), int(18 + 10 * t), int(34 + 22 * (1 - t)))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 34)
    s = "UNBEKANNTE NUMMER"
    d.text(((W - d.textlength(s, font=f)) / 2, 250), s, font=f, fill=(200, 200, 210))
    # großes Fragezeichen in gelb umrandetem Feld
    d.rounded_rectangle((70, 330, W - 70, 330 + W - 140), 70, fill=(28, 28, 34), outline=YELLOW, width=16)
    fq = ImageFont.truetype(FONT, 330)
    q = "?"
    bb = d.textbbox((0, 0), q, font=fq)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], 330 + (W - 140 - (bb[3] - bb[1])) / 2 - bb[1]), q, font=fq, fill=YELLOW)
    fr = ImageFont.truetype(FONT, 64)
    r = "REGEL 1"
    d.text(((W - d.textlength(r, font=fr)) / 2, 790), r, font=fr, fill=YELLOW)
    d.rounded_rectangle((W / 2 - 70, H - 30, W / 2 + 70, H - 22), 4, fill=(230, 230, 235))
    os.makedirs(BUILD, exist_ok=True)
    im.save(os.path.join(BUILD, "handy_profil.png"))
    print("Textur fertig")


def render():
    sys.path.insert(0, FA)
    import bpy
    import toon as T
    import cast as C
    T.reset()
    sc = T.setup(res=(1080, 1080), aa="16", bg="#101420", shadow=0.0)
    sc.render.film_transparent = True
    cam = T.camera(loc=(0, 0, 0), rot=(90, 0, 0), lens=34)
    C.pov_haende(cam, phone_tex=os.path.join(BUILD, "handy_profil.png"), line=0.0028)
    rig = bpy.data.objects["pov_rig"]
    rig.location = (0.006, 0.064, 0.0)        # Handy in die Bildmitte
    rig.rotation_euler = (0, 0, math.radians(-7))
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.filepath = os.path.join(BUILD, "hand_handy.png")
    bpy.ops.render.render(write_still=True)


def bild():
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    N = 1080
    y, x = np.mgrid[0:N, 0:N]
    r = np.sqrt((x - N / 2) ** 2 + (y - N / 2) ** 2) / (N / 2)
    base = np.dstack([18 + 22 * (1 - r), 22 + 24 * (1 - r), 40 + 40 * (1 - r)]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(base).convert("RGBA")
    hand = Image.open(os.path.join(BUILD, "hand_handy.png")).convert("RGBA")
    # gelbes Leuchten hinter dem Handy
    glow = Image.new("L", (N, N), 0)
    ImageDraw.Draw(glow).rounded_rectangle((330, 170, 750, 880), 90, fill=210)
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.composite(Image.new("RGBA", (N, N), YELLOW + (255,)), img, glow.point(lambda v: int(v * 0.55)))
    sh = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    sh.putalpha(hand.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.45)))
    img.alpha_composite(sh, (14, 22))
    img.alpha_composite(hand)
    # gelber Ring am Rand (bleibt im runden Ausschnitt sichtbar)
    ring = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((22, 22, N - 22, N - 22), outline=YELLOW + (255,), width=26)
    img.alpha_composite(ring)
    out = os.path.join(HERE, "out", "profilbild.png")
    img.convert("RGB").save(out)
    # Vorschau rund, groß und klein
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, N, N), fill=255)
    prev = Image.new("RGB", (760, 420), (245, 245, 245))
    for sz, xx in ((380, 20), (150, 440), (64, 620)):
        c = img.convert("RGB").resize((sz, sz), Image.LANCZOS)
        prev.paste(c, (xx, (420 - sz) // 2), mask.resize((sz, sz)))
    prev.save(os.path.join(HERE, "out", "profilbild_vorschau.png"))
    print("Profilbild fertig:", out)


if __name__ == "__main__":
    {"textur": textur, "render": render, "bild": bild}[sys.argv[-1]]()

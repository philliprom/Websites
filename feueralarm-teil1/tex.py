"""Texturen für die Sets (Tafel, Uhr, Plakate, Schilder) mit PIL. Aufruf: python3 tex.py"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
F = os.path.join(A, "fonts")


def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)


def tafel():
    W, H = 2048, 680
    im = Image.new("RGB", (W, H), (44, 84, 66))
    rnd = random.Random(4)
    dust = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(dust)
    for _ in range(60):  # verwischte Kreidereste
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        d.ellipse((x - 160, y - 30, x + 160, y + 30), fill=rnd.randint(8, 22))
    dust = dust.filter(ImageFilter.GaussianBlur(28))
    im = Image.composite(Image.new("RGB", (W, H), (120, 150, 135)), im, dust)
    txt = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(txt)
    fm = font("PermanentMarker.woff", 74)
    fs = font("PermanentMarker.woff", 58)
    d.text((90, 60), "Fr, 27. November", font=fs, fill=235)
    d.text((90, 170), "Vertretung: Fr. Sander", font=fm, fill=245)
    d.text((90, 300), "Mathe  S. 112  Nr. 4 a–c", font=fs, fill=225)
    d.text((1250, 470), "Hausaufgabe:", font=fs, fill=215)
    d.text((1250, 550), "AB Prozente", font=fs, fill=215)
    d.line((90, 270, 860, 262), fill=200, width=6)
    noise = Image.effect_noise((W, H), 60).point(lambda v: 255 if v > 110 else 120)
    txt = Image.composite(txt, Image.new("L", (W, H), 0), noise.convert("L"))
    im = Image.composite(Image.new("RGB", (W, H), (236, 240, 232)), im, txt.filter(ImageFilter.GaussianBlur(0.8)))
    im.save(os.path.join(A, "tafel.png"))


def uhr(hh=11, mm=52):
    N = 512
    im = Image.new("RGB", (N, N), (43, 47, 54))  # außerhalb des Zifferblatts: Farbe des Uhrrands
    d = ImageDraw.Draw(im)
    c = N / 2
    d.ellipse((4, 4, N - 4, N - 4), fill=(250, 250, 246))
    for k in range(60):
        a = k / 60 * 2 * math.pi
        r1 = c * (0.80 if k % 5 == 0 else 0.86)
        w = 10 if k % 5 == 0 else 4
        d.line((c + math.sin(a) * r1, c - math.cos(a) * r1, c + math.sin(a) * c * 0.92, c - math.cos(a) * c * 0.92),
               fill=(25, 25, 25), width=w)
    ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    am = mm / 60 * 2 * math.pi
    d.line((c, c, c + math.sin(ah) * c * 0.5, c - math.cos(ah) * c * 0.5), fill=(20, 20, 20), width=18)
    d.line((c, c, c + math.sin(am) * c * 0.75, c - math.cos(am) * c * 0.75), fill=(20, 20, 20), width=11)
    d.line((c, c, c + math.sin(am + 2.1) * c * 0.8, c - math.cos(am + 2.1) * c * 0.8), fill=(210, 40, 40), width=5)
    d.ellipse((c - 14, c - 14, c + 14, c + 14), fill=(20, 20, 20))
    im.save(os.path.join(A, "uhr.png"))


def periodensystem():
    W, H = 900, 600
    im = Image.new("RGB", (W, H), (248, 246, 238))
    d = ImageDraw.Draw(im)
    d.text((30, 18), "PERIODENSYSTEM", font=font("Oswald-Bold.woff", 52), fill=(40, 40, 60))
    cols = [(240, 120, 120), (250, 190, 100), (250, 230, 120), (150, 210, 140), (120, 180, 230), (180, 150, 220)]
    rnd = random.Random(2)
    for r in range(7):
        for k in range(18):
            if r == 0 and 0 < k < 17:
                continue
            if r in (1, 2) and 1 < k < 12:
                continue
            x, y = 30 + k * 46, 100 + r * 64
            d.rectangle((x, y, x + 42, y + 58), fill=cols[(k // 3 + r) % len(cols)], outline=(90, 90, 90), width=2)
            d.text((x + 8, y + 14), rnd.choice("HCNOFKSPLMBA"), font=font("Nunito-Black.ttf", 26), fill=(40, 40, 40))
    im.save(os.path.join(A, "periodensystem.png"))


def regeln():
    W, H = 600, 800
    im = Image.new("RGB", (W, H), (255, 236, 160))
    d = ImageDraw.Draw(im)
    d.text((40, 30), "KLASSENREGELN 8c", font=font("Oswald-Bold.woff", 56), fill=(150, 40, 40))
    fr = font("PermanentMarker.woff", 40)
    for i, t in enumerate(["1. Wir sind leise.", "2. Handy bleibt aus.", "3. Wir helfen uns.", "4. Pünktlich sein!",
                           "5. Respekt!"]):
        d.text((50, 150 + i * 120), t, font=fr, fill=(40, 40, 70))
    im.save(os.path.join(A, "regeln.png"))


def europa():
    W, H = 900, 640
    im = Image.new("RGB", (W, H), (164, 206, 232))
    d = ImageDraw.Draw(im)
    rnd = random.Random(7)
    cols = [(236, 205, 120), (170, 210, 140), (230, 160, 150), (200, 180, 230), (240, 220, 170), (160, 200, 190)]
    for i in range(26):
        cx, cy = rnd.randint(150, 800), rnd.randint(140, 560)
        pts = []
        n = rnd.randint(6, 10)
        r0 = rnd.randint(40, 95)
        for k in range(n):
            a = k / n * 2 * math.pi
            r = r0 * (0.7 + 0.5 * rnd.random())
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.8))
        d.polygon(pts, fill=cols[i % len(cols)], outline=(110, 110, 110))
    d.rectangle((0, 0, W, 70), fill=(250, 250, 245))
    d.text((30, 6), "EUROPA", font=font("Oswald-Bold.woff", 50), fill=(30, 60, 110))
    im.save(os.path.join(A, "europa.png"))


def schild(name, text, sub=None, bg=(240, 240, 236), fg=(30, 30, 30), size=(600, 240), fs=110):
    W, H = size
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    f = font("Oswald-Bold.woff", fs)
    bb = d.textbbox((0, 0), text, font=f)
    y = (H - (bb[3] - bb[1])) / 2 - bb[1] - (22 if sub else 0)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), text, font=f, fill=fg)
    if sub:
        f2 = font("Oswald-Bold.woff", int(fs * 0.36))
        bb2 = d.textbbox((0, 0), sub, font=f2)
        d.text(((W - (bb2[2] - bb2[0])) / 2 - bb2[0], H - 66), sub, font=f2, fill=fg)
    d.rectangle((4, 4, W - 5, H - 5), outline=fg, width=6)
    im.save(os.path.join(A, f"{name}.png"))


def notausgang():
    W, H = 600, 220
    im = Image.new("RGB", (W, H), (22, 150, 80))
    d = ImageDraw.Draw(im)
    # einfaches Laufmännchen + Tür + Pfeil
    d.rectangle((40, 30, 170, 190), outline=(255, 255, 255), width=10)
    d.ellipse((240, 30, 280, 70), fill=(255, 255, 255))
    for seg in [((260, 75), (240, 135)), ((240, 135), (205, 185)), ((240, 135), (285, 170)), ((285, 170), (300, 200)),
                ((255, 90), (215, 110)), ((255, 90), (300, 115))]:
        d.line(seg, fill=(255, 255, 255), width=16)
    d.polygon([(360, 85), (480, 85), (480, 55), (560, 110), (480, 165), (480, 135), (360, 135)], fill=(255, 255, 255))
    im.save(os.path.join(A, "notausgang.png"))


def fluchtplan():
    W, H = 500, 700
    im = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 90), fill=(22, 150, 80))
    d.text((24, 14), "Flucht- und Rettungsplan", font=font("Oswald-Bold.woff", 42), fill=(255, 255, 255))
    for k in range(5):
        d.rectangle((40, 130 + k * 100, 230, 210 + k * 100), outline=(40, 40, 40), width=4)
        d.rectangle((270, 130 + k * 100, 460, 210 + k * 100), outline=(40, 40, 40), width=4)
    d.line((250, 120, 250, 640), fill=(22, 150, 80), width=14)
    d.polygon([(230, 640), (270, 640), (250, 680)], fill=(22, 150, 80))
    d.ellipse((330, 330, 360, 360), fill=(220, 40, 40))
    im.save(os.path.join(A, "fluchtplan.png"))


def lautsprecher():
    N = 256
    im = Image.new("RGB", (N, N), (226, 224, 218))
    d = ImageDraw.Draw(im)
    for y in range(30, 230, 18):
        for x in range(30, 230, 18):
            if (x - 128) ** 2 + (y - 128) ** 2 < 100 ** 2:
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(60, 60, 60))
    im.save(os.path.join(A, "lautsprecher.png"))


if __name__ == "__main__":
    tafel()
    uhr()
    periodensystem()
    regeln()
    europa()
    notausgang()
    fluchtplan()
    lautsprecher()
    schild("schild_204", "204", "Klasse 8c")
    schild("schild_vorb", "VORBEREITUNG", None, fs=80)
    schild("schild_k3", "K3", "Werkstatt / Hausmeister", fs=120)
    schild("schild_keller", "KELLER  K1–K5", "Nebentreppe", bg=(250, 250, 245), fs=70)
    schild("schild_205", "205", "Klasse 8d")
    schild("schild_203", "203", "Physik")
    print("Texturen fertig")

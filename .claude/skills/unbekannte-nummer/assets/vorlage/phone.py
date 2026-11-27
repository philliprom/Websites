"""Handy-Sperrbildschirm mit Mitteilungen der unbekannten Nummer (Textur fürs 3D-Handy).

  python3 phone.py  ->  assets/handy_leer.png, assets/handy_r1.png … handy_r5.png
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from story import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
FB = os.path.join(A, "fonts", "Nunito-Black.ttf")
W, H = 540, 1160
TIMES = {1: "11:52", 2: "11:53", 3: "11:54", 4: "11:55", 5: "11:57"}


def font(sz):
    return ImageFont.truetype(FB, sz)


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


def base(time="11:52"):
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            t = y / H
            px[x, y] = (int(18 + 30 * t + 10 * x / W), int(24 + 18 * t), int(52 + 40 * (1 - t)))
    d = ImageDraw.Draw(im)
    f_time = font(150)
    tw = d.textlength(time, font=f_time)
    d.text(((W - tw) / 2, 120), time, font=f_time, fill=(245, 245, 250))
    f_d = font(30)
    s = "Freitag, 27. November"
    d.text(((W - d.textlength(s, font=f_d)) / 2, 90), s, font=f_d, fill=(210, 214, 230))
    d.rounded_rectangle((W / 2 - 70, H - 30, W / 2 + 70, H - 22), 4, fill=(230, 230, 235))
    d.text((30, 18), "11:5x", font=font(1), fill=(0, 0, 0))
    d.text((40, 20), "LTE", font=font(22), fill=(230, 230, 235))
    d.rounded_rectangle((W - 90, 24, W - 40, 44), 5, outline=(230, 230, 235), width=2)
    d.rectangle((W - 86, 28, W - 66, 40), fill=(230, 80, 70))
    return im


def notification(im, y, n, text, time, highlight=False):
    d = ImageDraw.Draw(im, "RGBA")
    f_h = font(22)
    f_t = font(26)
    lines = wrap(d, f"Regel {n}: {text}", f_t, W - 110)
    h = 70 + 34 * len(lines)
    d.rounded_rectangle((24, y, W - 24, y + h), 26, fill=(245, 245, 248, 235) if highlight else (220, 222, 230, 200),
                        outline=(255, 205, 40) if highlight else None, width=4 if highlight else 0)
    d.ellipse((42, y + 16, 78, y + 52), fill=(120, 125, 140))
    d.text((53, y + 16), "?", font=font(26), fill=(255, 255, 255))
    d.text((92, y + 22), "UNBEKANNTE NUMMER", font=f_h, fill=(60, 60, 70))
    d.text((W - 110, y + 22), "jetzt" if highlight else time, font=f_h, fill=(100, 100, 110))
    for k, ln in enumerate(lines):
        d.text((44, y + 62 + 34 * k), ln, font=f_t, fill=(20, 20, 25))
    return y + h + 14


def main():
    base().save(os.path.join(A, "handy_leer.png"))
    regeln = {l["n"]: l["sub"] for l in LINES if l["kind"] == "regel"}
    for n in range(1, 6):
        im = base(TIMES[n])
        y = 360
        y = notification(im, y, n, regeln[n], TIMES[n], highlight=True)
        for k in range(n - 1, 0, -1):
            if y > H - 160:
                break
            y = notification(im, y, k, regeln[k], TIMES[k])
        im.save(os.path.join(A, f"handy_r{n}.png"))
    print("Handy-Bildschirme fertig")


if __name__ == "__main__":
    main()

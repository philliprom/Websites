"""Cover image for video 12: the red giant about to swallow Earth + hook."""
import importlib.util
import os
import sys

import skia
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("v12", os.path.join(HERE, "12_script.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

W, H = v.W, v.H


def line(c, text, y, size, rgb, glow, max_w=940):
    f = v.fit(v.TF_BLACK, size, text, max_w)
    v.text_c(c, text, 540, y, f, v.C(rgb), glow=v.C(glow, 200), blur=22)


def render(t_frame, out):
    v.setup_video()
    v.NO_FLASH = True
    v.caption = lambda c, t: None
    v.draw_hud = lambda *a, **k: None
    v.overlays = lambda *a, **k: None
    v.draw_tape = lambda c, t: None
    v.draw_scope = lambda *a, **k: None
    v.draw_mixer = lambda *a, **k: None
    real_text = v.text_c
    v.text_c = lambda *a, **k: None
    buf, s = v.new_surface()
    c = s.getCanvas()
    v.draw_frame(c, t_frame)
    v.text_c = real_text

    sh = skia.GradientShader.MakeLinear([(0, 1060), (0, 1560)],
                                        [skia.Color(7, 5, 14, 0), skia.Color(7, 5, 14, 238),
                                         skia.Color(7, 5, 14, 238), skia.Color(7, 5, 14, 0)],
                                        [0, 0.18, 0.82, 1])
    c.drawRect(skia.Rect(0, 1060, W, 1560), skia.Paint(Shader=sh))

    tag = "#12  END OF EARTH"
    f = v.kit.font("mono", 38)
    w = f.measureText(tag) + 60
    rr = skia.RRect.MakeRectXY(skia.Rect(540 - w / 2, 300, 540 + w / 2, 368), 34, 34)
    c.drawRRect(rr, v.paint(skia.Color(10, 12, 28, 230)))
    c.drawRRect(rr, v.paint(v.C(v.AMBER, 230), stroke=3))
    v.text_c(c, tag, 540, 348, f, skia.Color(255, 255, 255))

    line(c, "THE SUN WILL", 1200, 110, (255, 255, 255), (255, 120, 60))
    line(c, "SWALLOW EARTH", 1335, 124, (255, 120, 60), (255, 90, 40))
    line(c, "EVERY SOUND IS A FORMULA", 1440, 62, v.AMBER, v.AMBER)

    f = v.kit.font("mono", 31)
    v.text_c(c, "SOUND ON  ·  8 LAYERS, 8 FORMULAS", 540, 1612, f, skia.Color(255, 255, 255, 210))
    s.makeImageSnapshot().save(out, skia.kPNG)
    Image.open(out).convert("RGB").save(out[:-4] + ".jpg", quality=92)
    print("wrote", out)


if __name__ == "__main__":
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 48.5
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "12_cover.png")
    render(t, out)

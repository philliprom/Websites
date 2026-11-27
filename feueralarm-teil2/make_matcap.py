"""Toon-Matcap (Lichtkugel) für Blender Workbench: weiches Zwei-Ton-Cel-Shading, Licht oben links vorne."""
import numpy as np
from PIL import Image
import sys

N = 512
y, x = np.mgrid[0:N, 0:N]
nx = (x + 0.5) / N * 2 - 1
ny = 1 - (y + 0.5) / N * 2
r2 = nx ** 2 + ny ** 2
nz = np.sqrt(np.clip(1 - r2, 0, 1))
L = np.array([-0.45, 0.55, 0.70]); L /= np.linalg.norm(L)
lam = nx * L[0] + ny * L[1] + nz * L[2]


def smooth(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


lit = 1.0
shade = 0.74
v = shade + (lit - shade) * smooth(0.12, 0.24, lam)     # weiche Kante zwischen Licht und Schatten
v *= 1 - 0.10 * smooth(0.55, 0.98, np.sqrt(r2)) * (1 - smooth(0.2, 0.5, lam))  # leicht dunklerer Rand auf der Schattenseite
v += 0.05 * smooth(0.80, 0.97, lam)                        # kleiner, weicher Glanz
v = np.clip(v, 0, 1.0)
img = np.dstack([v, v, v * 0.985])                        # minimal warm
img[r2 > 1] = 0
out = sys.argv[1] if len(sys.argv) > 1 else "assets/toon_matcap.png"
Image.fromarray((img * 255).astype(np.uint8)).save(out)
print("matcap", out)

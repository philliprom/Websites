"""Nachbearbeitung „Nachtschicht“: Ton (Regen, Röhrenbrummen, Stromausfall, Schlag, Klopfen) und Überwachungskamera-Look
(Hochskalieren, Unschärfe, Rauschen, ausgeblichene Farben, Vignette, Zeitstempel, blinkendes REC, Bildstörung beim Sprung).
  python3 horror-nachtschicht/post.py      -> out/nachtschicht_test.mp4
Erwartet die Bilder aus scene.py in build/frames/0001.png … (15 Bilder pro Sekunde).
"""
import glob
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD, OUT = os.path.join(HERE, "build"), os.path.join(HERE, "out")
sys.argv_orig = list(sys.argv)
sys.argv = [sys.argv[0], HERE]  # engine/audio.py liest den Projektordner aus argv
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import audio as A  # noqa: E402

FPS = 15
TEST = sys.argv_orig[sys.argv_orig.index("--test") + 1] if "--test" in sys.argv_orig else None
N = len(glob.glob(os.path.join(BUILD, "frames", "*.png"))) if not TEST else 75
if N == 0:
    sys.exit("Keine Bilder in build/frames – erst scene.py --frames rendern.")
DUR = N / FPS
BLACK = (47 / FPS - 1 / FPS, 50 / FPS)   # Licht aus (Bilder 47–50)
JUMP = 51 / FPS - 1 / FPS                # Gestalt an der Tür
SR = A.SR
rs = np.random.RandomState(5)


def lp(x, a):
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = y[i - 1] + a * (x[i] - y[i - 1])
    return y


n = int((DUR + 1.2) * SR)
t = np.arange(n) / SR
mix = np.zeros(n)
# Regen: gefiltertes Rauschen, dazu einzelne Tropfen-Knackser
rain = lp(rs.randn(n), 0.18) * 0.22 + A.hp(rs.randn(n)) * 0.03
drops = np.zeros(n)
for i in rs.randint(0, n - 400, 260):
    k = np.arange(400) / SR
    drops[i:i + 400] += np.sin(2 * np.pi * rs.uniform(1800, 4200) * k) * np.exp(-k * 600) * rs.uniform(0.02, 0.07)
mix += rain + drops
# Brummen der Leuchtröhren (100 Hz + Obertöne), aus während des Stromausfalls
hum = (np.sin(2 * np.pi * 100 * t) * 0.05 + np.sin(2 * np.pi * 200 * t) * 0.025 + np.sin(2 * np.pi * 300 * t) * 0.012
       + A.hp(rs.randn(n)) * 0.006) * (1 + 0.15 * np.sin(2 * np.pi * 0.7 * t))
gate = np.ones(n)
gate[(t >= BLACK[0]) & (t < JUMP)] = 0.0
gate = lp(gate, 0.02)
mix += hum * gate


def put(sig, at, gain=1.0):
    i = int(at * SR)
    j = min(n, i + len(sig))
    mix[i:j] += sig[: j - i] * gain


click = A.hp(rs.randn(int(0.03 * SR))) * np.exp(-np.arange(int(0.03 * SR)) / SR * 120)
put(click, BLACK[0], 0.8)                 # Strom weg
put(click, JUMP, 0.9)                     # Strom wieder da
put(A.sfx_boom(), JUMP, 0.9)              # Schlag, wenn sie an der Tür steht
put(A.sfx_sting(), JUMP + 0.02, 0.55)
put(A.sfx_knock(), JUMP + 0.75, 0.9)      # dreimal an die Scheibe klopfen
mix = mix / max(1e-6, np.abs(mix).max()) * 0.9
wav = os.path.join(BUILD, "ton.wav")
with wave.open(wav, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------------------------------------------------------------- Bild: Überwachungskamera-Look
FONT = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
base = 1795484833  # 24.11.2026 01:47:13 UTC = 02:47:13 in Deutschland (Anzeige +3600)
txt = "fontfile=" + FONT + ":fontcolor=white@0.92:borderw=3:bordercolor=black@0.6"
vf = ",".join([
    "scale=1080:1920:flags=bicubic",
    "gblur=sigma=1.1",
    "eq=saturation=0.32:contrast=1.12:brightness=-0.02:gamma=0.95",
    "colorchannelmixer=rr=0.95:gg=1.03:bb=0.98",
    "noise=alls=24:allf=t+u",
    "vignette=angle=0.75",
    # Bildstörung beim Sprung: Farbversatz und kurzes Verrutschen
    f"rgbashift=rh=-14:bh=14:enable='between(t,{JUMP:.3f},{JUMP + 0.2:.3f})'",
    f"drawbox=x=0:y=ih*0.55:w=iw:h=26:color=white@0.25:t=fill:enable='between(t,{JUMP:.3f},{JUMP + 0.13:.3f})'",
    # Einblendungen (sichere Zonen: oben ab y 290, rechts nur oberhalb y 800)
    f"drawtext={txt}:fontsize=40:x=70:y=300:text='CAM 03  EINGANG'",
    f"drawtext={txt}:fontsize=40:x=w-tw-70:y=300:text='%{{pts\\:gmtime\\:{base + 3600}\\:%d.%m.%Y  %H\\\\\\:%M\\\\\\:%S}}'",
    f"drawtext=fontfile={FONT}:fontcolor=red@0.95:borderw=3:bordercolor=black@0.6:fontsize=40:x=70:y=360:text='● REC':enable='lt(mod(t,1),0.6)'",
])
os.makedirs(OUT, exist_ok=True)
if TEST:
    # Vorschau eines Einzelbilds mit dem Kamera-Look, als stünde es bei Sekunde 3,5 (nach dem Sprung)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", "4", "-i", TEST, "-vf", vf,
                    "-frames:v", "1", "-ss", "3.6", os.path.join(BUILD, "look_test.png")], check=True)
    sys.exit(0)
out = os.path.join(OUT, "nachtschicht_test.mp4")
cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(BUILD, "frames", "%04d.png"), "-i", wav,
       "-vf", vf, "-r", "30", "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("Fertig:", out, f"({N} Bilder, {DUR:.1f} s)")

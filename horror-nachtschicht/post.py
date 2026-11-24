"""Nachbearbeitung „Nachtschicht“: Ton und Überwachungskamera-Look.
Ton (Stereo, synthetisch): Regen in drei Schichten (Rauschen mit Böen, Prasseln auf Glas, Tropfen), ferner Donner,
Kühlregal-Kompressor, Röhrenbrummen mit Knistern genau bei den Flacker-Bildern, Strom weg (Brummen sackt ab, Relais),
Strom wieder da (Vorschaltgerät pingt), Schock (Einschlag, Sub-Ton, schiefer Streicher-Cluster), dreimal Klopfen an die
Scheibe mit Glasklang, dazu Raumhall.
Bild: Hochskalieren, Unschärfe, Rauschen, ausgeblichene Farben, Vignette, Zeitstempel, blinkendes REC, Bildstörung.
  <vx>/bin/python horror-nachtschicht/post.py      -> out/nachtschicht_test.mp4
Erwartet die Bilder aus scene.py in build/frames/0001.png … (15 Bilder pro Sekunde).
"""
import glob
import math
import os
import random
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
from scipy.signal import butter, fftconvolve, sosfilt  # noqa: E402  (mit der vx-Umgebung starten, dort gibt es SciPy)

n = int((DUR + 1.6) * SR)
t = np.arange(n) / SR


def bp(x, lo=None, hi=None, order=2):
    if lo and hi:
        sos = butter(order, [lo, hi], btype="bandpass", fs=SR, output="sos")
    elif lo:
        sos = butter(order, lo, btype="highpass", fs=SR, output="sos")
    else:
        sos = butter(order, hi, btype="lowpass", fs=SR, output="sos")
    return sosfilt(sos, x)


def env(m, a, d):
    k = np.arange(m) / SR
    return np.minimum(1, k / max(a, 1e-4)) * np.exp(-np.maximum(0, k - a) / d)


bed = np.zeros((n, 2))       # Atmosphäre (trocken)
fx = np.zeros((n, 2))        # Ereignisse (bekommen Raumhall)


def put(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= n:
        return
    j = min(n, i + len(sig))
    lg, rg = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    buf[i:j, 0] += sig[: j - i] * gain * lg * 1.414
    buf[i:j, 1] += sig[: j - i] * gain * rg * 1.414


# Lichtzustände wie in scene.py (gleicher Zufall): flackernde Röhre und Stromausfall
FLICK = []
rr = random.Random(11)
for f in range(1, N + 1):
    if rr.random() < 0.22:
        rr.choice([0.05, 0.2, 0.5])
        if not (47 <= f <= 50):
            FLICK.append((f - 1) / FPS)
FLICK += [42 / FPS, 44 / FPS]  # alle Röhren dippen kurz vor dem Ausfall (Bilder 43 und 45)
power = np.ones(n)
power[(t >= BLACK[0]) & (t < JUMP + 1 / FPS)] = 0.0
power = bp(power, hi=40, order=1)

# 1) Regen: breites Rauschen mit Böen, dichtes Prasseln auf Glas und Dach, einzelne Tropfen
gust = 1 + 0.25 * np.sin(2 * np.pi * 0.23 * t) + 0.2 * bp(rs.randn(n), hi=1.5, order=1) * 8
for c in range(2):
    bed[:, c] += bp(rs.randn(n), 400, 7000) * 0.07 * gust
for i in np.sort(rs.randint(0, n - 600, int(DUR * 230))):
    m = 260
    burst = bp(rs.randn(m), 1800, 7500) * np.exp(-np.arange(m) / SR * 900)
    put(bed, burst, i / SR, rs.uniform(0.02, 0.09), rs.uniform(-0.8, 0.8))
for i in rs.randint(0, n - 3000, int(DUR * 5)):
    m = 2400
    k = np.arange(m) / SR
    f0 = rs.uniform(900, 1700)
    drop = np.sin(2 * np.pi * (f0 * k - 2500 * k * k)) * np.exp(-k * 70)
    put(bed, drop, i / SR, rs.uniform(0.03, 0.06), rs.uniform(-0.6, 0.6))
# 2) ferner Donner am Anfang
m = int(4.0 * SR)
brown = np.cumsum(rs.randn(m))
brown = bp(brown - np.mean(brown), 18, 180) * 0.004
put(bed, brown * env(m, 0.5, 1.4), 0.1, 1.0, -0.3)
# 3) Raumton: Kühlregal-Kompressor (aus beim Stromausfall)
comp = (np.sin(2 * np.pi * 50 * t) * 0.02 + np.sin(2 * np.pi * 100 * t) * 0.012 + bp(rs.randn(n), 60, 300) * 0.02) * power
put(bed, comp, 0, 1.0, -0.5)
# 4) Brummen der Leuchtröhren (100 Hz mit Obertönen) + Knistern beim Flackern
hum = sum(np.sin(2 * np.pi * 100 * k * t + k) / k for k in range(1, 11)) * 0.018
hum = bp(hum + bp(rs.randn(n), 2000, 6000) * 0.004, 80, 4000) * power
for ft in FLICK:
    i0, i1 = int(ft * SR), int((ft + 1 / FPS) * SR)
    hum[i0:i1] *= 0.25
    m = i1 - i0
    crackle = bp(rs.randn(m), 1500, 9000) * (rs.rand(m) < 0.05) * 3.0
    put(fx, crackle, ft, 0.18, 0.4)
    k = np.arange(int(0.15 * SR)) / SR
    put(fx, np.sin(2 * np.pi * 4200 * k) * np.exp(-k * 40), ft + 1 / FPS, 0.025, 0.4)
put(bed, hum, 0, 1.0, 0.2)
# 5) Strom weg: Brummen sackt ab, Relais klackt
m = int(0.5 * SR)
k = np.arange(m) / SR
down = np.sin(2 * np.pi * np.cumsum(np.linspace(100, 30, m)) / SR) * np.exp(-k * 6)
put(fx, down, BLACK[0], 0.12)
thump = np.sin(2 * np.pi * 70 * k) * np.exp(-k * 30) + bp(rs.randn(m), 800, 5000) * np.exp(-k * 300) * 0.5
put(fx, thump, BLACK[0], 0.35, 0.3)
# 6) Strom wieder da: Vorschaltgerät „pingt“, zwei schnelle Klicks
m = int(0.8 * SR)
k = np.arange(m) / SR
ping = (np.sin(2 * np.pi * 3200 * k) + 0.6 * np.sin(2 * np.pi * 4730 * k)) * np.exp(-k * 7)
put(fx, ping, JUMP, 0.05, 0.2)
for dt in (0.0, 0.07):
    put(fx, bp(rs.randn(600), 1000, 8000) * np.exp(-np.arange(600) / SR * 400), JUMP + dt, 0.3, 0.2)
# 7) Schock: tiefer Einschlag, abfallender Sub-Ton, schriller, schiefer Streicher-Cluster
m = int(2.2 * SR)
k = np.arange(m) / SR
sub = np.sin(2 * np.pi * np.cumsum(np.linspace(58, 26, m)) / SR) * np.exp(-k * 1.6)
hit = bp(rs.randn(m), hi=260) * np.exp(-k * 9) * 6
put(fx, sub * 0.9 + hit * 0.5, JUMP, 0.9)
screech = np.zeros(m)
for fq in (880, 932, 1245, 1319, 1760):
    ph = 2 * np.pi * fq * k + 0.3 * np.sin(2 * np.pi * 5.5 * k)
    screech += sum(np.sin(h * ph) / h for h in range(1, 6))
screech = bp(screech, 500, 9000) * (0.75 + 0.25 * np.sin(2 * np.pi * 13 * k)) * env(m, 0.015, 0.9)
put(fx, screech, JUMP + 0.01, 0.055)
# 8) Dreimal mit dem Fingerknöchel an die Scheibe: Klick, dumpfer Körper, Glas klingt nach, Rahmen scheppert
for j in range(3):
    m = int(0.6 * SR)
    k = np.arange(m) / SR
    knock = (bp(rs.randn(m), 2000, 7000) * np.exp(-k * 500) * 0.8
             + np.sin(2 * np.pi * 150 * k) * np.exp(-k * 45)
             + sum(np.sin(2 * np.pi * fq * k) * np.exp(-k * dk) * am for fq, dk, am in ((2350, 18, 0.35), (3720, 25, 0.22), (5180, 32, 0.15)))
             + bp(rs.randn(m), 200, 900) * np.exp(-k * 40) * 0.6)
    put(fx, knock, JUMP + 0.8 + j * 0.27, 0.55 - j * 0.04, -0.15)

# Raumhall für die Ereignisse (synthetische Impulsantwort, ca. 0,7 s)
m = int(0.9 * SR)
k = np.arange(m) / SR
ir = np.stack([bp(rs.randn(m), hi=6000) * np.exp(-k * 8) for _ in range(2)], axis=1)
ir /= np.abs(ir).sum(axis=0) / 25
wet = np.stack([fftconvolve(fx[:, c], ir[:, c])[:n] for c in range(2)], axis=1)
mix = bed + fx + wet * 0.35
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.9
wav = os.path.join(BUILD, "ton.wav")
with wave.open(wav, "wb") as w:
    w.setnchannels(2)
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

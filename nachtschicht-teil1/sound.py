"""Sounddesign für Nachtschicht Teil 1 (Stereo, alles synthetisch) + Mischung mit der Erzählerstimme.
Liest build/edl.json, build/shots.json, build/vo.wav und schreibt build/mix.wav.
  <vx>/bin/python nachtschicht-teil1/sound.py        (braucht NumPy + SciPy)
"""
import json
import math
import os
import random
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
SR = 44100
rs = np.random.RandomState(11)
edl = json.load(open(os.path.join(BUILD, "edl.json"), encoding="utf-8"))
shots_cfg = json.load(open(os.path.join(BUILD, "shots.json"), encoding="utf-8"))
EV = edl["events"]
SH = {s["id"]: s for s in edl["shots"]}
D = edl["duration"]
n = int((D + 0.5) * SR)
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


def mask(t0, t1, fade=0.08):
    """0/1-Hüllkurve für einen Zeitbereich mit weichen Kanten."""
    m = np.clip((t - t0) / fade, 0, 1) * np.clip((t1 - t) / fade, 0, 1)
    return m


bed = np.zeros((n, 2))   # Atmosphäre: wird unter der Stimme abgesenkt
fx = np.zeros((n, 2))    # Ereignisse: bekommen Raumhall
dry = np.zeros((n, 2))   # Ereignisse ohne Hall (Handy, Rauschen beim Kamerawechsel)


def put(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= n or i + len(sig) <= 0:
        return
    s0 = max(0, -i)
    j = min(n, i + len(sig))
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    buf[max(0, i):j, 0] += sig[s0: j - i] * gain * lg
    buf[max(0, i):j, 1] += sig[s0: j - i] * gain * rg


# ---------------------------------------------------------------- Bausteine
def knock(strength=1.0):
    m = int(0.6 * SR)
    k = np.arange(m) / SR
    y = (bp(rs.randn(m), 2000, 7000) * np.exp(-k * 500) * 0.8 + np.sin(2 * np.pi * 150 * k) * np.exp(-k * 45)
         + sum(np.sin(2 * np.pi * f * k) * np.exp(-k * d) * a for f, d, a in ((2350, 18, 0.35), (3720, 25, 0.22), (5180, 32, 0.15)))
         + bp(rs.randn(m), 200, 900) * np.exp(-k * 40) * 0.6)
    return y * strength


def click(dur=0.03, lo=1000, hi=8000):
    m = int(dur * SR)
    return bp(rs.randn(m), lo, hi) * np.exp(-np.arange(m) / SR * 150)


def crackle(dur):
    m = int(dur * SR)
    return bp(rs.randn(m), 1500, 9000) * (rs.rand(m) < 0.05) * 3.0


def static(dur=0.14):
    m = int(dur * SR)
    k = np.arange(m) / SR
    return bp(rs.randn(m), 300, 9000) * np.minimum(1, k / 0.005) * np.exp(-k * 8) * 0.8


def typekey():
    m = int(0.09 * SR)
    k = np.arange(m) / SR
    return (bp(rs.randn(m), 1500, 6000) * np.exp(-k * 300) + np.sin(2 * np.pi * 220 * k) * np.exp(-k * 80) * 0.5) * 0.7


def squeak(dur=0.45):
    m = int(dur * SR)
    k = np.arange(m) / SR
    f = 1900 + 500 * np.sin(2 * np.pi * 3 * k)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + bp(rs.randn(m), 2500, 6000) * 0.5
    return s * np.minimum(1, k / 0.03) * np.minimum(1, (dur - k) / 0.08)


def rustle(dur=0.7):
    m = int(dur * SR)
    k = np.arange(m) / SR
    return bp(rs.randn(m), 800, 6000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 7 * k))) * env(m, 0.05, 0.25)


def buzz(dur=0.38):
    m = int(dur * SR)
    k = np.arange(m) / SR
    s = np.sign(np.sin(2 * np.pi * 170 * k)) * 0.5 + bp(rs.randn(m), 100, 600) * 0.6
    return bp(s, 80, 1500) * np.minimum(1, k / 0.01) * np.minimum(1, (dur - k) / 0.02)


def heartbeat():
    m = int(0.6 * SR)
    k = np.arange(m) / SR
    one = np.sin(2 * np.pi * 52 * k) * np.exp(-k * 18)
    two = np.zeros(m)
    i = int(0.22 * SR)
    two[i:] = one[: m - i] * 0.75
    return one + two


def hit():
    m = int(2.2 * SR)
    k = np.arange(m) / SR
    sub = np.sin(2 * np.pi * np.cumsum(np.linspace(58, 26, m)) / SR) * np.exp(-k * 1.6)
    noise = bp(rs.randn(m), hi=260) * np.exp(-k * 9) * 6
    return sub * 0.9 + noise * 0.5


def screech():
    m = int(1.8 * SR)
    k = np.arange(m) / SR
    s = np.zeros(m)
    for f in (880, 932, 1245, 1319, 1760):
        ph = 2 * np.pi * f * k + 0.3 * np.sin(2 * np.pi * 5.5 * k)
        s += sum(np.sin(h * ph) / h for h in range(1, 6))
    return bp(s, 500, 9000) * (0.75 + 0.25 * np.sin(2 * np.pi * 13 * k)) * env(m, 0.015, 0.8)


def riser(dur):
    m = int(dur * SR)
    k = np.arange(m) / SR
    f = np.linspace(90, 240, m)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + bp(rs.randn(m), 400, 3000) * 0.3 * (k / dur)
    return s * (k / dur) ** 2


# ---------------------------------------------------------------- Atmosphäre je Einstellung
inside = np.zeros(n)
outside = np.zeros(n)
for s in edl["shots"]:
    a, b = s["t"]
    if s["kind"] in ("cctv", "black", "note", "phone") and s.get("src") != "r2":
        inside += mask(a, b, 0.03)
    if s.get("src") == "r2":
        outside += mask(a, b, 0.03)
# Zwischenschnitt im Zettel auf Kamera 3 (draußen)
for c in SH["SH3"].get("cuts", []):
    inside -= mask(c["t"][0], c["t"][1], 0.03)
    outside += mask(c["t"][0], c["t"][1], 0.03)
inside = np.clip(inside, 0, 1)
outside = np.clip(outside, 0, 1)
power = np.ones(n)
bo = EV["blackout"]
power[(t >= bo[0]) & (t < bo[1])] = 0.0
power = bp(power, hi=40, order=1)

gust = 1 + 0.25 * np.sin(2 * np.pi * 0.23 * t) + bp(rs.randn(n), hi=1.5, order=1) * 1.6
for c in range(2):
    rain_raw = bp(rs.randn(n), 300, 8000) * gust
    bed[:, c] += bp(rain_raw, hi=1800) * 0.11 * inside               # drinnen: gedämpft durch Glas
    bed[:, c] += rain_raw * 0.075 * outside                           # draußen: hell und nah
patter = np.zeros(n)
for i in np.sort(rs.randint(0, n - 600, int(D * 200))):
    m = 260
    patter[i:i + m] += bp(rs.randn(m), 1800, 7500) * np.exp(-np.arange(m) / SR * 900) * rs.uniform(0.02, 0.08)
put(bed, patter * (0.35 * inside + 1.0 * outside), 0, 1.0, 0.1)
for i in rs.randint(0, n - 3000, int(D * 4)):
    m = 2400
    k = np.arange(m) / SR
    f0 = rs.uniform(900, 1700)
    drop = np.sin(2 * np.pi * (f0 * k - 2500 * k * k)) * np.exp(-k * 70) * rs.uniform(0.02, 0.05)
    g = outside[i] * 1.0 + inside[i] * 0.25
    put(bed, drop * g, i / SR, 1.0, rs.uniform(-0.7, 0.7))
hum = sum(np.sin(2 * np.pi * 100 * k * t + k) / k for k in range(1, 11)) * 0.016
hum = bp(hum + bp(rs.randn(n), 2000, 6000) * 0.004, 80, 4000) * power * inside
comp = (np.sin(2 * np.pi * 50 * t) * 0.016 + bp(rs.randn(n), 60, 300) * 0.016) * power * inside
canopy_hum = bp(sum(np.sin(2 * np.pi * 100 * k * t) / k for k in (1, 2, 3)), 80, 800) * 0.012 * outside
put(bed, hum + comp + canopy_hum, 0, 1.0, 0.15)
# tiefe Klangfläche (Drone) mit Schwellungen, still beim Stromausfall
drone = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 55.4 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t) + 0.3 * np.sin(2 * np.pi * 110.8 * t))
drone = drone * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t)) + bp(rs.randn(n), 40, 220) * 1.2
swell = 0.35 + 0.65 * (mask(SH["SH5"]["t"][0], SH["SH6"]["t"][1], 1.5) + mask(SH["SH8"]["t"][0], D, 1.0))
swell *= np.where((t >= bo[0]) & (t < EV["jump"]), 0.0, 1.0)
put(bed, drone * swell * 0.014, 0, 1.0)

# ---------------------------------------------------------------- Ereignisse
for k_, at in enumerate(EV["hook_knocks"]):
    put(fx, knock(0.9 - k_ * 0.05), at, 0.6, -0.15)
put(fx, hit(), 0.0, 0.35)
# Kamerawechsel: kurzes Rauschen an jeder harten Schnittstelle
for s in edl["shots"][1:]:
    put(dry, static(0.12 if s["kind"] != "cctv" else 0.16), s["t"][0] - 0.02, 0.22)
for c in SH["SH3"].get("cuts", []):
    put(dry, static(0.14), c["t"][0] - 0.02, 0.22)
    put(dry, static(0.12), c["t"][1] - 0.02, 0.18)
# Schwarzbild: Schreibmaschine „02:39“
a1 = SH["SH1"]["t"][0]
for k_ in range(5):
    put(dry, typekey(), a1 + 0.18 + k_ * 0.13, 0.5, (k_ - 2) * 0.15)
# Zettel: Papierrascheln, Filzstift bei jeder Regel, ganz leises dreifaches Klopfen bei Regel 4
put(dry, rustle(), SH["SH3"]["t"][0] + 0.05, 0.35)
for kt, name in SH["SH3"]["keys"]:
    if name.startswith("Regel"):
        put(dry, squeak(), kt + 0.15, 0.08, 0.2)
r4 = [kt for kt, nm in SH["SH3"]["keys"] if nm == "Regel 4"][0]
for k_ in range(3):
    put(fx, knock(0.5), r4 + 0.9 + k_ * 0.27, 0.12, -0.6)
put(fx, bp(np.cumsum(rs.randn(int(4 * SR))) * 0.003, 18, 160) * env(int(4 * SR), 0.6, 1.4), SH["SH2"]["t"][0] + 1.2, 1.0, -0.3)  # ferner Donner


def flick_times(cfg, shot_start, first_frame):
    return [shot_start + (f - first_frame) / edl["fps_src"] for f in cfg]


r1 = shots_cfg["r1"]
for ft in flick_times(r1["flick5"] + r1["dips"], SH["SH4"]["t"][0], SH["SH4"]["from"]):
    put(fx, crackle(0.1), ft, 0.16, 0.4)
r2 = shots_cfg["r2"]
for ft in flick_times(r2["canopy_off"], SH["SH5"]["t"][0], 1):
    put(fx, crackle(0.12), ft, 0.25, -0.2)
    put(fx, click(0.04), ft, 0.25, -0.2)
z0, z1, _ = SH["SH5"]["zoom"]
put(bed, riser(z1 - z0 + 0.8), z0, 0.06)
gone = SH["SH5"]["t"][0] + (r2["fig_out"] - 1) / edl["fps_src"]
m = int(1.2 * SR)
k = np.arange(m) / SR
put(fx, (bp(rs.randn(m), 200, 4000) * (k / 1.2) ** 3)[::-1] * 0.6, gone - 1.15, 0.25)      # rückwärts gezogenes Rauschen
put(fx, np.sin(2 * np.pi * 45 * k) * np.exp(-k * 6), gone, 0.4)
r3 = shots_cfg["r3"]
for ft in flick_times(r3["dips"], SH["SH6"]["t"][0], 1):
    put(fx, crackle(0.1), ft, 0.2, 0.4)
m = int(0.5 * SR)
k = np.arange(m) / SR
put(fx, np.sin(2 * np.pi * np.cumsum(np.linspace(100, 30, m)) / SR) * np.exp(-k * 6), bo[0], 0.15)
put(fx, np.sin(2 * np.pi * 70 * k) * np.exp(-k * 30), bo[0], 0.4, 0.3)
put(fx, click(0.05), bo[0], 0.2, 0.3)
put(fx, (np.sin(2 * np.pi * 3200 * k) + 0.6 * np.sin(2 * np.pi * 4730 * k)) * np.exp(-k * 7), EV["jump"], 0.05, 0.2)
put(fx, hit(), EV["jump"], 1.0)
put(fx, screech(), EV["jump"] + 0.01, 0.07)
for k_, at in enumerate(EV["knocks"]):
    put(fx, knock(1.0 - k_ * 0.05), at, 0.75, -0.15)
for at in EV["phone_buzz"]:
    put(dry, buzz(), at, 0.35)
put(dry, buzz(0.3), EV["msg2"] - 0.05, 0.3)
hb_t = SH["SH7"]["t"][0] + 0.8
while hb_t < D - 1.2:
    put(dry, heartbeat(), hb_t, 0.5)
    hb_t += 1.0 if hb_t < SH["SH8"]["t"][0] else 0.8
for at in EV["cards"]:
    put(fx, hit() * 0.35, at, 0.5)
put(fx, knock(1.0), EV["final_knock"], 0.9, -0.15)
put(fx, hit() * 0.6, EV["final_knock"], 0.5)

# ---------------------------------------------------------------- Mischen: Hall, Stimme, Ducking
mi = int(0.9 * SR)
k = np.arange(mi) / SR
ir = np.stack([bp(rs.randn(mi), hi=6000) * np.exp(-k * 8) for _ in range(2)], axis=1)
ir /= np.abs(ir).sum(axis=0) / 25
wet = np.stack([fftconvolve(fx[:, c], ir[:, c])[:n] for c in range(2)], axis=1)
with wave.open(os.path.join(BUILD, "vo.wav"), "rb") as w:
    vsr = w.getframerate()
    vo = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1:
        vo = vo.reshape(-1, w.getnchannels()).mean(axis=1)
if vsr != SR:
    vo = np.interp(np.arange(int(len(vo) * SR / vsr)) / SR, np.arange(len(vo)) / vsr, vo)
vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
# Stimme je Satz auf gleiche Lautheit bringen (einzelne Fassungen sind leiser/lauter), höchstens ±4 dB
tl_ = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
rms_all = [np.sqrt(np.mean(vo[int(s_["start"] * SR):int(s_["speechEnd"] * SR)] ** 2)) for s_ in tl_["segments"]]
target = float(np.median(rms_all))
for s_, r_ in zip(tl_["segments"], rms_all):
    g = float(np.clip(target / max(r_, 1e-6), 0.63, 1.58))
    i0, i1 = int((s_["start"] - 0.05) * SR), int((s_["speechEnd"] + 0.1) * SR)
    vo[i0:i1] *= g
# Erzähler-Klang (ab 25.11.): ganz leichter Flüster-Hauch (Rauschen mit der Hüllkurve der Stimme), mehr Bass,
# etwas weniger Präsenz und ein kurzer, dunkler Raum
from scipy.signal import lfilter  # noqa: E402


def peq(x, f0, gain_db, q=1.0):
    a_ = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    al = np.sin(w0) / (2 * q)
    b = [1 + al * a_, -2 * np.cos(w0), 1 - al * a_]
    a = [1 + al / a_, -2 * np.cos(w0), 1 - al / a_]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


v_env = bp(np.abs(vo), hi=35, order=1)
breath = bp(rs.randn(n), 1800, 7500) * v_env
v_rms = np.sqrt(np.mean(vo[np.abs(vo) > 0.01] ** 2)) if np.any(np.abs(vo) > 0.01) else 0.05
b_rms = np.sqrt(np.mean(breath[np.abs(vo) > 0.01] ** 2)) if np.any(np.abs(vo) > 0.01) else 1.0
vo = vo + breath * (v_rms * 10 ** (-15 / 20) / max(b_rms, 1e-9))
vo = peq(peq(vo, 130, 2.5, 0.8), 3500, -1.5, 1.2)
mi_ = int(0.45 * SR)
k_ = np.arange(mi_) / SR
ir_v = bp(rs.randn(mi_), hi=5000) * np.exp(-k_ * 11)
ir_v /= np.abs(ir_v).sum() / 6
vo = vo + fftconvolve(vo, ir_v)[:n] * 0.12
venv = bp(np.abs(vo), hi=8, order=1)
duck = 1.0 - 0.6 * np.clip(venv / 0.04, 0, 1)
mix = bed * duck[:, None] + fx + wet * 0.35 + dry
mix = mix / max(1e-6, np.abs(mix).max()) * 0.55
mix += np.stack([vo, vo], axis=1) * 0.9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
with wave.open(os.path.join(BUILD, "mix.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f"Ton fertig: {D:.1f} s → build/mix.wav")

"""Sounddesign für Nachtschicht Teil 2 (Fassung A oder B; Stereo, alles synthetisch) + Mischung mit der Erzählerstimme.
Liest <zweig>/build/edl.json, timeline.json, vo.wav und schreibt <zweig>/build/mix.wav.
  <vx>/bin/python nachtschicht-teil2/sound.py a|b
Bausteine wie in Teil 1. Spannende Sätze (Stufe 1–3 aus emotion.py) werden 1/2/3,5 dB lauter gemischt.
"""
import json
import math
import os
import random
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
Z = sys.argv[1]
BUILD = os.path.join(HERE, Z, "build")
SR = 44100
rs = np.random.RandomState(11)
edl = json.load(open(os.path.join(BUILD, "edl.json"), encoding="utf-8"))
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


# ---------------------------------------------------------------- weitere Bausteine (Teil 2)
def creak(dur=1.2, f0=95.0):
    """Türscharnier: tiefes, ruckelndes Knarzen."""
    m = int(dur * SR)
    k = np.arange(m) / SR
    f = f0 * (1 + 0.25 * np.sin(2 * np.pi * 0.7 * k)) * (1 + 0.04 * rs.randn(m).cumsum() / np.sqrt(m))
    pulses = (np.sin(2 * np.pi * np.cumsum(f) / SR) > 0.97).astype(float)
    body = bp(pulses * 3 + rs.randn(m) * 0.05, 300, 2500)
    return body * np.minimum(1, k / 0.1) * np.minimum(1, (dur - k) / 0.2)


def whoosh(dur=1.0, lo=200, hi=3000):
    m = int(dur * SR)
    k = np.arange(m) / SR
    return bp(rs.randn(m), lo, hi) * np.sin(np.pi * k / dur) ** 2


def thud(f=60.0, d=14.0):
    m = int(0.7 * SR)
    k = np.arange(m) / SR
    return np.sin(2 * np.pi * f * k) * np.exp(-k * d) + bp(rs.randn(m), 100, 800) * np.exp(-k * 40) * 0.5


def keyclick():
    return np.concatenate([click(0.02, 2000, 9000), np.zeros(int(0.07 * SR)), click(0.03, 1500, 7000) * 1.3])


def drip():
    m = int(0.25 * SR)
    k = np.arange(m) / SR
    f0 = rs.uniform(600, 1100)
    return np.sin(2 * np.pi * (f0 * k + 1800 * k * k)) * np.exp(-k * 35)


def breath(dur=2.3):
    """Atmen ganz nah: Einatmen (heller), kurze Pause, Ausatmen (tiefer, länger)."""
    m = int(dur * SR)
    k = np.arange(m) / SR
    inh = bp(rs.randn(m), 900, 4500) * np.clip(np.sin(np.pi * k / 0.8), 0, None) * (k < 0.8)
    exh = bp(rs.randn(m), 250, 2200) * np.clip(np.sin(np.pi * (k - 1.0) / 1.2), 0, None) * ((k > 1.0) & (k < 2.2))
    return inh * 0.7 + exh


def bang():
    """Metalltür fällt ins Schloss: Schlag, Nachklingen des Blechs, tiefer Stoß."""
    m = int(2.5 * SR)
    k = np.arange(m) / SR
    metal = sum(np.sin(2 * np.pi * f * k) * np.exp(-k * d) * a for f, d, a in ((180, 3, 0.6), (431, 4, 0.4), (887, 6, 0.25), (1630, 9, 0.15)))
    th = np.zeros(m)
    t_ = thud(48, 5)
    th[:len(t_)] = t_
    return metal * 0.5 + bp(rs.randn(m), 80, 3000) * np.exp(-k * 18) * 1.2 + th


# ---------------------------------------------------------------- Atmosphäre je Einstellung
inside, outside, lager = np.zeros(n), np.zeros(n), np.zeros(n)
for s in edl["shots"]:
    a, b = s["t"]
    src_ = s.get("src")
    if s["kind"] == "pov" or src_ in ("t1r1", "t1r3") or s["kind"] in ("phone", "chat", "note", "ir") or s.get("base") == "ir":
        inside += mask(a, b, 0.03)
    if src_ == "t1r2":
        outside += mask(a, b, 0.03)
    if src_ == "lager" or s.get("base") == "lager":
        lager += mask(a, b, 0.03)
if Z == "a":   # Tür steht offen: von „Tür geht auf“ bis „Du schließt wieder ab“ ist es draußen laut
    dopen = mask(EV["door_open"] + 0.2, EV["door_close"] + 0.3, 0.5)
    outside += dopen * 0.85
    inside -= dopen * 0.5
inside, outside, lager = np.clip(inside, 0, 1), np.clip(outside, 0, 1), np.clip(lager, 0, 1)
power = np.ones(n)
if Z == "a":
    power[t >= EV["flicker"][1]] = 0.0
power = bp(power, hi=40, order=1)

gust = 1 + 0.25 * np.sin(2 * np.pi * 0.23 * t) + bp(rs.randn(n), hi=1.5, order=1) * 1.6
for c in range(2):
    rain_raw = bp(rs.randn(n), 300, 8000) * gust
    bed[:, c] += bp(rain_raw, hi=1800) * 0.11 * inside
    bed[:, c] += rain_raw * 0.075 * outside
    bed[:, c] += (bp(rain_raw, hi=4500) * 0.085 + bp(rs.randn(n), 60, 400) * 0.05 * gust) * lager   # Lager: Regen + Wind durch die Tür
patter = np.zeros(n)
for i in np.sort(rs.randint(0, n - 600, int(D * 200))):
    m = 260
    patter[i:i + m] += bp(rs.randn(m), 1800, 7500) * np.exp(-np.arange(m) / SR * 900) * rs.uniform(0.02, 0.08)
put(bed, patter * (0.35 * inside + 1.0 * outside + 0.8 * lager), 0, 1.0, 0.1)
hum = sum(np.sin(2 * np.pi * 100 * k * t + k) / k for k in range(1, 11)) * 0.016
hum = bp(hum + bp(rs.randn(n), 2000, 6000) * 0.004, 80, 4000) * power * (inside + 0.6 * lager)
comp = (np.sin(2 * np.pi * 50 * t) * 0.016 + bp(rs.randn(n), 60, 300) * 0.016) * power * inside
put(bed, hum + comp, 0, 1.0, 0.15)
drone = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 55.4 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t) + 0.3 * np.sin(2 * np.pi * 110.8 * t))
drone = drone * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t)) + bp(rs.randn(n), 40, 220) * 1.2
put(bed, drone * (0.4 + 0.6 * np.clip(t / D, 0, 1) ** 1.5) * 0.016, 0, 1.0)

# ---------------------------------------------------------------- Ereignisse
put(fx, hit(), 0.0, 0.35)
for s in edl["shots"][1:]:
    put(dry, static(0.12 if s["kind"] in ("phone", "chat", "note", "pov") else 0.16), s["t"][0] - 0.02, 0.22)
SHd = {s["id"]: s for s in edl["shots"]}
vote = next(s for s in edl["shots"] if s["kind"] == "vote")
put(fx, hit() * 0.5, vote["t"][0] + 0.45, 0.5)
ph = next(s for s in edl["shots"] if s["kind"] == "phone")
for at in ph["buzz"]:
    put(dry, buzz(), at, 0.35)
for key, at, y in ph["notifs"][1:]:
    put(dry, buzz(0.3), at - 0.05, 0.3)
dec = next(s for s in edl["shots"] if s["kind"] == "decision")
for at in dec["card_t"]:
    put(fx, hit() * 0.35, at, 0.5)
hb_t = dec["t"][0] + 0.3
while hb_t < EV["final"] - 0.6:
    put(dry, heartbeat(), hb_t, 0.45)
    hb_t += 0.85
if Z == "a":
    put(dry, keyclick(), EV["unlock"], 0.35, 0.1)
    put(fx, creak(1.6, 80), EV["door_open"], 0.5, -0.2)
    put(fx, whoosh(1.4, 150, 2500), EV["door_open"] + 0.1, 0.35)
    put(fx, thud(55, 10), EV["door_close"], 0.6)
    put(dry, keyclick(), EV["door_close"] + 0.45, 0.35, 0.1)
    ch = next(s for s in edl["shots"] if s["kind"] == "chat")
    put(dry, rustle(0.35) * 0.6, ch["scroll"][0], 0.25)
    s5 = SHd["SH5"]
    ta, tb = s5["reveal"]
    nprint = len(json.load(open(os.path.join(HERE, "build", "spuren", "spuren.json"))))
    for i in range(nprint):
        put(fx, drip(), ta + i * (tb - ta) / (nprint - 1) + 0.05, 0.12, 0.3 - 0.6 * i / nprint)
    f0, f1 = EV["flicker"]
    for ft in np.arange(f0, f1, 0.09):
        if rs.rand() < 0.6:
            put(fx, crackle(0.08), ft, 0.2, 0.4)
    m = int(0.6 * SR)
    k = np.arange(m) / SR
    put(fx, np.sin(2 * np.pi * np.cumsum(np.linspace(110, 25, m)) / SR) * np.exp(-k * 4), f1, 0.25)
    put(fx, thud(70, 25), f1, 0.5, 0.3)
    s7 = SHd["SH7"]
    put(dry, click(0.04, 800, 6000), s7["t"][0] - 0.05, 0.4)                               # Nachtsicht schaltet sich ein
    m = int((D - s7["t"][0]) * SR)
    k = np.arange(m) / SR
    put(dry, np.sin(2 * np.pi * 15600 * k) * 0.02 + bp(rs.randn(m), 3000, 9000) * 0.01, s7["t"][0], 0.5)
    put(fx, hit(), s7["t"][0], 0.8)
    bt = EV["breath"][0]
    while bt < EV["breath"][1] - 2.3:
        put(dry, breath(), bt, 0.22, rs.uniform(-0.15, 0.15))
        bt += 2.6
    put(fx, hit() * 0.7, EV["final"], 0.6)
else:
    for k_, at in enumerate(EV["knocks"]):
        put(fx, knock(1.0 - k_ * 0.05), at, 0.75, -0.15)
    for s in edl["shots"]:
        if s.get("src") == "lager" or s.get("base") == "lager":
            a, b = s["t"]
            ct = a + 0.6
            while ct < b - 1.0:
                put(fx, creak(rs.uniform(0.8, 1.4), rs.uniform(70, 110)), ct, 0.25, -0.3)
                ct += rs.uniform(2.2, 3.4)
    s6 = SHd["SH6"]
    z0, z1, _, _ = s6["zoom"]
    put(bed, riser(z1 - z0 + 0.6), z0, 0.06)
    put(fx, hit(), z0 + 0.1, 0.7)
    s7 = SHd["SH7"]
    put(dry, rustle(), s7["t"][0] + 0.05, 0.35)
    for kt, name in s7["keys"][1:]:
        put(dry, squeak(), kt + 0.15, 0.08, 0.2)
    put(fx, hit() * 0.8, s7["keys"][-1][0], 0.6)
    put(fx, bang(), EV["final"] - 0.05, 0.9, -0.25)                                       # hinten fällt die Tür ins Schloss
    put(fx, hit() * 0.6, EV["final"], 0.5)

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
    # sauber umrechnen (Polyphasenfilter); lineare Interpolation hat Spiegelfrequenzen erzeugt, die als feines Zischeln mitliefen
    from math import gcd
    from scipy.signal import resample_poly
    gd = gcd(SR, vsr)
    vo = resample_poly(vo, SR // gd, vsr // gd).astype(np.float32)
vo = np.pad(vo, (0, max(0, n - len(vo))))[:n]
# Stimme je Satz auf gleiche Lautheit bringen (einzelne Fassungen sind leiser/lauter), höchstens ±4 dB
tl_ = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
rms_all = [np.sqrt(np.mean(vo[int(s_["start"] * SR):int(s_["speechEnd"] * SR)] ** 2)) for s_ in tl_["segments"]]
target = float(np.median(rms_all))
for s_, r_ in zip(tl_["segments"], rms_all):
    g = float(np.clip(target / max(r_, 1e-6), 0.63, 1.58))
    i0, i1 = int((s_["start"] - 0.05) * SR), int((s_["speechEnd"] + 0.1) * SR)
    vo[i0:i1] *= g * 10 ** ({0: 0.0, 1: 1.0, 2: 2.0, 3: 3.5}[s_.get("spannung", 0)] / 20)
# Erzähler-Klang (ab 25.11.): mehr Bass, etwas weniger Präsenz und ein kurzer, dunkler Raum (sehr leise)
from scipy.signal import lfilter  # noqa: E402


def peq(x, f0, gain_db, q=1.0):
    a_ = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    al = np.sin(w0) / (2 * q)
    b = [1 + al * a_, -2 * np.cos(w0), 1 - al * a_]
    a = [1 + al / a_, -2 * np.cos(w0), 1 - al / a_]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


# (25.11.) Künstlicher Flüster-Hauch entfernt: Kanalinhaber hörte bei jedem Satz ein Rauschen. Die Stimme selbst ist sauber.
vo = peq(peq(vo, 130, 2.5, 0.8), 3500, -1.5, 1.2)
mi_ = int(0.45 * SR)
k_ = np.arange(mi_) / SR
ir_v = bp(rs.randn(mi_), hi=5000) * np.exp(-k_ * 11)
ir_v /= np.abs(ir_v).sum() / 6
vo = vo + fftconvolve(vo, ir_v)[:n] * 0.07
# Absenkung der Atmosphäre unter der Stimme: weich und gleichmäßig über den ganzen Satz (kein Pumpen zwischen Wörtern)
speak = np.zeros(n)
for s_ in tl_["segments"]:
    speak[int((s_["start"] - 0.15) * SR):int((s_["speechEnd"] + 0.25) * SR)] = 1.0
speak = bp(speak, hi=2.0, order=1)
duck = 1.0 - 0.5 * np.clip(speak, 0, 1)
mix = bed * duck[:, None] + fx + wet * 0.35 + dry
mix = mix / max(1e-6, np.abs(mix).max()) * 0.55
# Sättigung nur für die Geräusche (Klopfen bekommt Druck); die Stimme kommt danach unverzerrt dazu
mix = np.tanh(mix * 1.2) / 1.2  # bei kleinen Pegeln unverändert, Spitzen der Geräusche ~1 dB weicher (wie bisher)
mix += np.stack([vo, vo], axis=1) * 0.9
mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
with wave.open(os.path.join(BUILD, "mix.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print(f"Ton fertig: {D:.1f} s → build/mix.wav")

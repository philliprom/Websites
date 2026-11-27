"""Ton für DER FEUERALARM: Stimmen (Raumklang je Ort), Feueralarm, Gong + Durchsage, Handy, Schritte, Türen,
Keller, Spannungsmusik, Herzschlag. Alles synthetisch.

  <vx>/bin/python sound.py   (liest timeline.json, build/shots.json; schreibt build/mix.wav)
"""
import json
import math
import os

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

from story import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
SR = 44100
TL = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
SHOTS = json.load(open(os.path.join(BUILD, "shots.json"), encoding="utf-8"))
SHOT = {s["id"]: s for s in SHOTS}
LN = {l["id"]: l for l in TL["lines"]}
EMO = {l["id"]: l["emo"] for l in LINES}
D = TL["total"]
n = int((D + 0.6) * SR)
t = np.arange(n) / SR
rs = np.random.RandomState(7)


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
    return np.clip((t - t0) / fade, 0, 1) * np.clip((t1 - t) / fade, 0, 1)


def ir(rt60, size=1.0, bright=6000):
    m = int(rt60 * SR)
    k = np.arange(m) / SR
    y = rs.randn(m) * np.exp(-6.9 * k / rt60)
    y = bp(y, 200 / size, bright)
    y[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return y / np.sqrt((y ** 2).sum())


IR = {"klasse": ir(0.55, 1.0, 7000), "flur": ir(1.3, 1.6, 6000), "keller": ir(0.7, 0.8, 4500), "hall": ir(2.2, 2, 5000)}


def reverb(x, kind, wet):
    y = fftconvolve(x, IR[kind])[:len(x)]
    return x * (1 - wet) + y * wet * 2.2


voice = np.zeros((n, 2))
bed = np.zeros((n, 2))     # Alarm, Atmosphäre (wird unter Stimmen abgesenkt)
fx = np.zeros((n, 2))      # Ereignisse
mus = np.zeros((n, 2))     # Musik


def put(buf, sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= n or i + len(sig) <= 0:
        return
    s0 = max(0, -i)
    j = min(n, i + len(sig))
    lg, rg = math.cos((pan + 1) * math.pi / 4) * 1.414, math.sin((pan + 1) * math.pi / 4) * 1.414
    buf[max(0, i):j, 0] += sig[s0:j - i] * gain * lg
    buf[max(0, i):j, 1] += sig[s0:j - i] * gain * rg


def where(time):
    """Ort (klasse/flur/keller) zur Zeit."""
    loc = "klasse"
    for s in SHOTS:
        if s["t0"] <= time:
            loc = s["set"]
    return loc


# ---------------------------------------------------------------- Stimmen
def rms_db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


PAN = {"ben": -0.35, "lina": -0.15, "sander": 0.15, "pohl": 0.05, "noah": 0.0, "durchsage": 0.25}
for l in TL["lines"]:
    w, sr = sf.read(os.path.join(HERE, "tts_cache", "trim", f'{l["id"]}.wav'), dtype="float32")
    w = resample_poly(w, SR, sr).astype(np.float64)
    e = EMO[l["id"]].lower()
    target = -20.5
    if "whisper" in e:
        target = -23.0
    if any(k in e for k in ("shout", "scream", "loud", "calls out")):
        target = -19.0
    if l["kind"] == "regel":
        target = -21.5
    w = w * 10 ** ((target - rms_db(w)) / 20)
    loc = where(l["start"] + 0.05)
    if l["id"] == "l17":   # Lautsprecher-Durchsage
        w = bp(w, 380, 3300, 3)
        w = np.tanh(w * 3.0) / 1.6
        w = reverb(w, "klasse", 0.35)
        w *= 10 ** ((-20 - rms_db(w)) / 20)
    elif l["id"] == "l24":  # Ruf vom anderen Flurende
        w = bp(w, 150, 4200)
        w = reverb(w, "flur", 0.55)
    elif l["id"] == "l19":  # leise ins Telefon, weiter weg
        w = reverb(bp(w, 120, 6000), "klasse", 0.25) * 0.85
    elif l["kind"] == "regel":
        w = reverb(w, loc, 0.06)
    else:
        w = reverb(w, loc, {"klasse": 0.12, "flur": 0.2, "keller": 0.16}[loc])
    put(voice, w, l["start"], 1.0, PAN.get(l["who"], 0) * (0.5 if l["kind"] == "regel" else 1))


# ---------------------------------------------------------------- Feueralarm (elektrische Glocke)
def bell(dur):
    m = int(dur * SR)
    k = np.arange(m) / SR
    strike = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 19 * k))
    strike = bp(strike, None, 120)
    tone = sum(a * np.sin(2 * np.pi * f * k + p) for f, a, p in ((1180, 1.0, 0), (2460, 0.55, 1), (3720, 0.3, 2),
                                                               (5300, 0.15, 3)))
    rattle = bp(rs.randn(m), 2500, 9000) * 0.25
    y = (tone + rattle) * (0.35 + 0.65 * strike)
    return y / np.abs(y).max()


t_flur = SHOT["23_regel4_flur"]["t0"]
t_keller = SHOT["27_was_macht_ihr"]["t0"]
alarm = bell(D + 0.6)[:n]
a_cls = alarm * mask(0, t_flur, 0.05)
a_flur = alarm * mask(t_flur, t_keller, 0.05)
a_kel = bp(alarm, None, 500) * mask(t_keller, D + 1, 0.3)
# Klasse: Alarm kommt gedämpft durch die Tür (am Anfang laut, dann Hintergrund)
start_boost = 1.0 + 1.6 * np.clip(1 - t / 1.2, 0, 1)
put(bed, reverb(bp(a_cls, None, 3000), "flur", 0.6) * 0.11 * start_boost, 0)
put(bed, reverb(a_flur, "flur", 0.4) * 0.2, 0)
put(bed, a_kel * 0.18, 0)

# Raumklang
room = bp(rs.randn(n), 80, 1200) * 0.012
put(bed, room * mask(0, t_flur), 0)
hum = (np.sin(2 * np.pi * 50 * t) * 0.6 + np.sin(2 * np.pi * 100 * t) * 0.3 + bp(rs.randn(n), 30, 160) * 2.5) * 0.02
put(bed, hum * mask(t_keller, D + 1, 0.4), 0)


# ---------------------------------------------------------------- Ereignisse
def click(dur=0.03, lo=1000, hi=8000, decay=150):
    m = int(dur * SR)
    return bp(rs.randn(m), lo, hi) * np.exp(-np.arange(m) / SR * decay)


def buzz():
    m = int(0.9 * SR)
    k = np.arange(m) / SR
    gate = ((k % 0.45) < 0.3).astype(float)
    gate = bp(gate, None, 60)
    y = np.sign(np.sin(2 * np.pi * 165 * k)) * 0.5 + np.sin(2 * np.pi * 165 * k)
    y = bp(y, 90, 2500) * gate
    return y * 0.5


def ping():
    m = int(0.8 * SR)
    k = np.arange(m) / SR
    return (np.sin(2 * np.pi * 1318 * k) * np.exp(-k * 6) + 0.6 * np.sin(2 * np.pi * 1976 * k) * np.exp(-k * 8)) * 0.3


def gong():
    m = int(2.2 * SR)
    k = np.arange(m) / SR
    y = np.zeros(m)
    for at, f in ((0.0, 784), (0.55, 659)):
        kk = np.clip(k - at, 0, None)
        on = (k >= at).astype(float)
        y += on * (np.sin(2 * np.pi * f * kk) + 0.4 * np.sin(2 * np.pi * 2 * f * kk) + 0.2 * np.sin(
            2 * np.pi * 3.01 * f * kk)) * np.exp(-kk * 2.2)
    y = bp(np.tanh(y * 1.5), 400, 3400)
    return reverb(y, "klasse", 0.35) * 0.35


def step(heel=True):
    m = int(0.12 * SR)
    k = np.arange(m) / SR
    if heel:
        return (bp(rs.randn(m), 1500, 7000) * np.exp(-k * 90) * 0.5 + np.sin(2 * np.pi * 220 * k) * np.exp(-k * 60) * 0.3)
    return (bp(rs.randn(m), 80, 900) * np.exp(-k * 45) * 0.9 + bp(rs.randn(m), 2000, 6000) * np.exp(-k * 120) * 0.15)


def steps(t0, t1, rate, heel, gain, loc, pan=0.0):
    tt = t0
    k = 0
    while tt < t1:
        s = step(heel) * (0.85 + 0.3 * rs.rand())
        put(fx, reverb(s, loc, 0.25), tt, gain, pan)
        tt += 1 / rate * (0.95 + 0.1 * rs.rand())
        k += 1


def creak(dur=0.9):
    m = int(dur * SR)
    k = np.arange(m) / SR
    f = 380 + 90 * np.sin(2 * np.pi * 1.3 * k) + 40 * rs.randn(m).cumsum() / SR
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sign(np.sin(ph)) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 23 * k)))
    return bp(y, 300, 3000) * env(m, 0.1, dur * 0.6) * 0.25


def thump(f=55, dur=0.35, g=1.0):
    m = int(dur * SR)
    k = np.arange(m) / SR
    return np.sin(2 * np.pi * f * k * (1 - 0.3 * k)) * np.exp(-k * 12) * g


def heart(t0, t1, bpm0=88, bpm1=112):
    tt = t0
    while tt < t1:
        bpm = bpm0 + (bpm1 - bpm0) * (tt - t0) / max(1e-3, t1 - t0)
        put(fx, thump(52, 0.3, 0.55), tt)
        put(fx, thump(46, 0.3, 0.38), tt + 0.17)
        tt += 60 / bpm


def hit(g=1.0, tail=2.5):
    m = int(tail * SR)
    k = np.arange(m) / SR
    y = np.sin(2 * np.pi * 42 * k * (1 - 0.15 * k)) * np.exp(-k * 2.2) * 1.2 + bp(rs.randn(m), 60, 2500) * np.exp(-k * 7) * 0.5
    return reverb(y, "hall", 0.4) * g


def riser(dur=1.2, g=0.5):
    m = int(dur * SR)
    k = np.arange(m) / SR
    y = bp(rs.randn(m), 800, 9000) * (k / dur) ** 2.5
    return y * g


S = lambda i: LN[i]["start"]  # noqa: E731
E = lambda i: LN[i]["end"]  # noqa: E731

# Schlüssel im Schloss (Einstellung 1)
for tt in (0.45, 0.78):
    put(fx, click(0.05, 1500, 9000, 90) * 0.7, tt, 0.9, 0.4)
put(fx, hit(0.45, 1.6), 0.0)
# Handy: Vibration + Ton, wenn die Regel erscheint
for ev in TL["events"]:
    if ev["kind"] == "buzz":
        put(fx, buzz(), ev["t"], 0.9)
        put(fx, ping(), ev["t"] + 0.35, 0.8)
    if ev["kind"] == "gong":
        put(fx, gong(), ev["t"] - 0.15, 1.0, 0.25)
    if ev["kind"] == "tuer_flur":
        put(fx, reverb(creak(0.8), "flur", 0.3), ev["t"] - 0.6, 0.8)
        put(fx, reverb(bp(rs.randn(int(0.5 * SR)), 40, 500) * env(int(0.5 * SR), 0.005, 0.12), "flur", 0.3),
            ev["t"] - 0.05, 0.9)
    if ev["kind"] == "tuer_keller":
        put(fx, reverb(creak(1.1), "keller", 0.3), ev["t"] - 0.9, 0.9)
# Durchsage wird abgedreht: Klick + kurzes Knacken
put(fx, click(0.06, 300, 5000, 60), E("l17") + 0.02, 1.2, 0.25)
put(fx, bp(rs.randn(int(0.15 * SR)), 1000, 4000) * 0.15, E("l17") - 0.05, 1, 0.25)
# Absätze von Frau Sander
s02, s07, s17, s25 = SHOT["02_uebung"], SHOT["07_sander_kommt"], SHOT["17_durchsage"], SHOT["25_ich_weiss"]
steps(s02["t0"] + 0.4, s02["t0"] + 2.2, 1.9, True, 0.5, "klasse", 0.4)
steps(s07["t0"], s07["t0"] + 2.3, 1.9, True, 0.65, "klasse", 0.1)
steps(s17["t0"] + 1.0, s17["t0"] + 3.6, 1.9, True, 0.45, "klasse", 0.3)
steps(E("l24") - 0.1, s25["t1"] + 0.6, 2.6, True, 0.4, "flur", 0.0)
# Rennen im Flur (Turnschuhe) + Atmen
for sid in ("23_regel4_flur", "24_keller_niemand", "26_lauf"):
    sh = SHOT[sid]
    steps(sh["t0"], sh["t1"], 3.0, False, 0.9, "flur", -0.1)
breath = bp(rs.randn(n), 300, 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 1.6 * t)) ** 3 * 0.05
put(fx, breath * mask(t_flur, t_keller + 1.5, 0.3), 0)
# Kriechen / Rücken (Einstellung 22)
s22 = SHOT["22_mir_ist_schlecht"]
for k in range(6):
    put(fx, bp(rs.randn(int(0.25 * SR)), 150, 1500) * env(int(0.25 * SR), 0.05, 0.08) * 0.35, s22["t0"] + 0.3 + k * 0.6)
# Keller: Tropfen
for k in range(int((D - t_keller) / 1.7)):
    put(fx, np.sin(2 * np.pi * (1400 + 300 * rs.rand()) * np.arange(int(0.15 * SR)) / SR) * np.exp(
        -np.arange(int(0.15 * SR)) / SR * 35) * 0.08, t_keller + 0.8 + k * 1.7 + 0.4 * rs.rand(), 1, 0.6)

# ---------------------------------------------------------------- Musik: Spannungsfläche + Schläge
def pad(freqs, dur, g=1.0):
    m = int(dur * SR)
    k = np.arange(m) / SR
    y = np.zeros(m)
    for f in freqs:
        for det in (-0.12, 0.0, 0.15):
            ph = rs.rand() * 6.28
            y += np.sign(np.sin(2 * np.pi * (f + det) * k + ph)) * 0.2 + np.sin(2 * np.pi * (f + det) * k + ph)
    y = bp(y, 50, 1200)
    return y / np.abs(y).max() * g


drone = pad([55.0, 82.4, 110.0], D + 0.6, 1.0)[:n]
lvl = 0.05 + 0.05 * mask(S("r2"), S("l17"), 1.5) + 0.06 * mask(t_flur, D + 1, 1.0) + 0.06 * mask(S("r5"), D + 1, 2.0)
put(mus, drone * lvl, 0)
high = pad([440.0, 466.2], D + 0.6, 1.0)[:n]
put(mus, bp(high, 300, 3000) * 0.02 * (mask(S("r2") + 2, S("l16") + 2, 1.0) + mask(S("r5"), D + 1, 1.5)), 0)
# Akzente
put(mus, riser(1.0, 0.35), S("r2") + LN["r2"]["dur"] - 1.6)
put(mus, hit(0.6), E("r2") - 0.2)
put(mus, hit(0.5), E("l16") - 0.1)
put(mus, riser(0.9, 0.3), t_flur - 0.9)
put(mus, hit(0.55), t_flur)
put(mus, hit(0.5), S("l24"))
put(mus, riser(1.6, 0.4), S("r5") + 1.0)
put(mus, hit(0.9, 3.0), S("r5") + 2.0)
put(mus, hit(0.75), S("l30") + LN["l30"]["dur"] * 0.55)
heart(S("r5"), D, 84, 118)
endk = [e["t"] for e in TL["events"] if e["kind"] == "endkarte"][0]
put(mus, hit(1.1, 3.5), endk)

# ---------------------------------------------------------------- Mischen: Hintergrund mind. 12 dB unter der Stimme
def short_db(x, win=0.1):
    k = int(win * SR)
    p = np.convolve((x ** 2).mean(1) if x.ndim > 1 else x ** 2, np.ones(k) / k, mode="same")
    return 10 * np.log10(p + 1e-10)


back = bed + mus + fx
v_db = short_db(voice)
b_db = short_db(back)
active = v_db > -45
need = np.where(active, np.minimum(0.0, (v_db - 12.0) - b_db), 0.0)
# glätten: schnell absenken, langsam zurück
g = np.zeros(n)
cur = 0.0
a_att, a_rel = math.exp(-1 / (0.02 * SR)), math.exp(-1 / (0.3 * SR))
for i in range(0, n, 64):
    tgt = need[i]
    a = a_att if tgt < cur else a_rel
    for _ in range(64):
        cur = tgt + (cur - tgt) * a
    g[i:i + 64] = cur
gain = 10 ** (g / 20)
mix = back * gain[:, None]
mix = np.tanh(mix * 1.1) / 1.1
mix = mix + voice * 0.95
peak = np.abs(mix).max()
if peak > 0.98:
    mix = mix / peak * 0.98
os.makedirs(BUILD, exist_ok=True)
sf.write(os.path.join(BUILD, "mix.wav"), mix.astype(np.float32), SR)
sf.write(os.path.join(BUILD, "voice.wav"), (voice * 0.95 * (0.98 / max(peak, 0.98))).astype(np.float32), SR)
print("Mischung fertig:", round(D, 2), "s")

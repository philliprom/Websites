"""Ton für DER FEUERALARM · Teil 2: Stimmen (Raumklang je Ort), Alarm aus der Schule, Regen, Motor, Türen,
Zentralverriegelung, Handy des Fahrers, Fahrgeräusche, Spannungsmusik, Herzschlag. Alles synthetisch.

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


IR = {"keller": ir(0.7, 0.8, 4500), "hof": ir(0.45, 1.6, 7000), "auto": ir(0.16, 0.5, 5000), "hall": ir(2.2, 2, 5000)}
WET = {"keller": 0.16, "hof": 0.1, "auto": 0.06}


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
    """Ort (keller/hof/auto) zur Zeit."""
    loc = "keller"
    for s in SHOTS:
        if s["t0"] <= time:
            loc = s["set"]
    return loc


# ---------------------------------------------------------------- Stimmen
def rms_db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)


PAN = {"ben": -0.3, "sander": 0.1, "pohl": 0.05, "noah": 0.0, "papa": 0.0, "fahrer": -0.15}
for l in TL["lines"]:
    w, sr = sf.read(os.path.join(HERE, "tts_cache", "trim", f'{l["id"]}.wav'), dtype="float32")
    w = resample_poly(w, SR, sr).astype(np.float64)
    e = EMO[l["id"]].lower()
    target = -20.5
    if "whisper" in e:
        target = -22.0
    if any(k in e for k in ("shout", "scream", "loud", "calls out")):
        target = -19.0
    if l["kind"] == "regel":
        target = -21.5
    w = w * 10 ** ((target - rms_db(w)) / 20)
    loc = where(l["start"] + 0.05)
    if l["who"] == "papa":  # Nachricht in der Stimme des Vaters: warm, etwas Hall, wie eine Erinnerung
        w = reverb(bp(w, 90, 8000), "hall", 0.1)
        w *= 10 ** ((-21.0 - rms_db(w)) / 20)
    elif l["id"] == "k09":  # Sander ruft von der Tür (ca. 6 m entfernt, Hall vom Hof, trotzdem verständlich)
        w = reverb(bp(w, 140, 6000), "hof", 0.28)
        w *= 10 ** ((-19.5 - rms_db(w)) / 20)
    else:
        w = reverb(w, loc, WET[loc])
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


def smoothstep(a, b, x):
    k = np.clip((x - a) / max(b - a, 1e-6), 0, 1)
    return k * k * (3 - 2 * k)


t_hof = SHOT["03_raus"]["t0"]
t_auto = SHOT["10_anschnallen"]["t0"]
t_go = t_auto + 0.9                      # wie render_shot.car_y_fn
t_stop = SHOT["16_finger_weg"]["t0"] - 0.4
TA, TD = 2.5, 4.5


def speed(tt):
    """relative Geschwindigkeit 0..1 (Anfahren, Stadttempo, Bremsen bis zur Ampel)."""
    u = tt - t_go
    dur = t_stop - t_go
    return np.where(u <= 0, 0.0, np.where(u < TA, u / TA, np.where(u < dur - TD, 1.0,
                    np.where(u < dur, (dur - u) / TD, 0.0))))


alarm = bell(D + 0.6)[:n]
# Keller: Alarm gedämpft durch die Decke
put(bed, bp(alarm, None, 500) * 0.16 * mask(0, t_hof + 0.3, 0.2), 0)
# Hof: Alarm aus dem Gebäude (durch Wände, Hall vom Hof), leiser, je weiter wir vom Gebäude weg sind
dist = np.interp(t, [t_hof, t_hof + 3, SHOT["05_fahrer"]["t0"], t_auto], [1.0, 0.7, 0.5, 0.45])
put(bed, reverb(bp(alarm, 300, 2500), "hof", 0.5) * 0.11 * dist * mask(t_hof, t_auto, 0.12), 0)
# im Auto: nur noch von fern, verschwindet beim Wegfahren
put(bed, bp(alarm, 400, 1500) * 0.025 * mask(t_auto, t_go + 5, 0.15) * (1 - smoothstep(t_go, t_go + 5, t)), 0)
hum = (np.sin(2 * np.pi * 50 * t) * 0.6 + np.sin(2 * np.pi * 100 * t) * 0.3 + bp(rs.randn(n), 30, 160) * 2.5) * 0.02
put(bed, hum * mask(0, t_hof, 0.2), 0)
# Regen: draußen voll, im Auto gedämpft auf dem Dach, zieht beim Fahren langsam ab
tropfen = np.zeros(n)
idx = rs.randint(0, n, int(D * 140))
tropfen[idx] = rs.randn(len(idx)) * 3
regen = bp(rs.randn(n), 400, 9000) * 0.035 + bp(rs.randn(n), 80, 400) * 0.012 + bp(tropfen, 1500, 8000) * 0.03
r_out = np.interp(t, [0, t_hof - 0.05, t_hof + 0.3, t_auto - 0.05, t_auto + 0.05], [0.0, 0.0, 1.0, 1.0, 0.0])
r_in = np.interp(t, [t_auto - 0.05, t_auto + 0.05, t_go + 2, t_go + 12], [0.0, 0.45, 0.4, 0.0])
put(bed, regen * r_out + bp(regen, None, 2200) * r_in * 1.6, 0)
# Motor des blauen Autos: im Hof Leerlauf (lauter, je näher), im Auto Drehzahl nach Tempo
spd = speed(t)
rpm = np.where(t < t_go, 820.0, 820 + 1500 * np.clip((t - t_go) / TA, 0, 1) * (spd > 0) + 0 * spd)
rpm = np.where((t >= t_go + TA) & (spd > 0), 1750 + 150 * spd, rpm)
rpm = np.where(t >= t_stop, 800.0, rpm) + 25 * np.sin(2 * np.pi * 0.7 * t)
ph = 2 * np.pi * np.cumsum(rpm / 60 * 2) / SR
motor = sum(a_ * np.sin(k * ph + p_) for k, a_, p_ in ((1, 1.0, 0), (2, 0.5, 1), (3, 0.28, 2), (4, 0.14, 0.5)))
motor = bp(motor + bp(rs.randn(n), 40, 300) * 0.6, 25, 1400)
m_hof = np.interp(t, [t_hof, t_hof + 4, SHOT["05_fahrer"]["t0"], t_auto], [0.15, 0.35, 0.6, 0.8]) * mask(t_hof, t_auto,
                                                                                                         0.1)
m_auto = (0.5 + 0.5 * np.clip((rpm - 800) / 1500, 0, 1)) * mask(t_auto, D + 1, 0.05)
put(bed, motor * 0.05 * m_hof + bp(motor, None, 600) * 0.07 * m_auto, 0)
# Fahrgeräusche (Reifen, Wind) nach Tempo
put(bed, (bp(rs.randn(n), 60, 900) * 0.05 * spd + bp(rs.randn(n), 300, 3000) * 0.012 * spd ** 2) *
    mask(t_auto, D + 1, 0.05), 0)


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
    return reverb(y, "hof", 0.35) * 0.35


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


def heart(t0, t1, bpm0=88, bpm1=112, pause=()):
    tt = t0
    while tt < t1:
        bpm = bpm0 + (bpm1 - bpm0) * (tt - t0) / max(1e-3, t1 - t0)
        if not any(a <= tt <= b for a, b in pause):
            put(fx, thump(52, 0.3, 0.4), tt)
            put(fx, thump(46, 0.3, 0.28), tt + 0.17)
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


def platsch():
    """Schritt auf nassem Asphalt."""
    m = int(0.16 * SR)
    k = np.arange(m) / SR
    return (bp(rs.randn(m), 80, 700) * np.exp(-k * 40) * 0.7 + bp(rs.randn(m), 1800, 9000) * np.exp(-k * 22) * 0.35)


def rennen(t0, t1, rate=3.2, gain=0.8):
    tt = t0
    while tt < t1:
        put(fx, reverb(platsch() * (0.85 + 0.3 * rs.rand()), "hof", 0.15), tt, gain, 0.05 * rs.randn())
        tt += 1 / rate * (0.92 + 0.16 * rs.rand())


def lay(m, sig, at):
    """sig ab Sekunde at in ein Feld der Länge m legen."""
    y = np.zeros(m)
    i = int(at * SR)
    L = max(0, min(len(sig), m - i))
    y[i:i + L] = sig[:L]
    return y


def autotuer(zu=True, g=1.0):
    m = int(0.6 * SR)
    k = np.arange(m) / SR
    if zu:   # dumpfer Schlag + Blech + Schloss
        y = np.sin(2 * np.pi * 70 * k) * np.exp(-k * 18) * 1.2 + bp(rs.randn(m), 100, 1800) * np.exp(-k * 30) * 0.8
        y += lay(m, click(0.04, 1500, 7000, 120) * 0.8, 0.025)
    else:    # Griff + Schloss auf + kurzes Quietschen
        y = lay(m, click(0.03, 1200, 6000, 150), 0.0)
        y += lay(m, click(0.05, 600, 4000, 80) * 0.7, 0.08)
        y += lay(m, creak(0.35) * 0.6, 0.12)
    return y * g


def zv():
    """Zentralverriegelung: zwei mechanische Klacks."""
    m = int(0.35 * SR)
    y = np.zeros(m)
    for at, f in ((0.0, 900), (0.09, 650)):
        i = int(at * SR)
        k = np.arange(m - i) / SR
        y[i:] += (bp(rs.randn(m - i), f, f * 5) * np.exp(-k * 90) + np.sin(2 * np.pi * f / 4 * k) * np.exp(-k * 60))
    return y * 0.8


def klingelton(dur):
    """Handy des Fahrers: einfache Marimba-Melodie, wiederholt."""
    m = int(dur * SR)
    y = np.zeros(m)
    noten = (784, 988, 1175, 988, 784, 0, 784, 988)
    tt = 0.0
    while tt < dur:
        for f in noten:
            if f:
                i = int(tt * SR)
                L = min(int(0.2 * SR), m - i)
                if L <= 0:
                    break
                k = np.arange(L) / SR
                y[i:i + L] += (np.sin(2 * np.pi * f * k) + 0.3 * np.sin(2 * np.pi * 4 * f * k) * np.exp(-k * 30)) * \
                    np.exp(-k * 14)
            tt += 0.13
        tt += 0.5
    return bp(y, 300, 6000) * 0.3


# Handy: Vibration + Ton, wenn eine Regel erscheint
for ev in TL["events"]:
    if ev["kind"] == "buzz":
        put(fx, buzz(), ev["t"], 0.9 if ev.get("regel") != 5 else 0.6)
        if ev.get("regel") != 5:   # Rückblick: Papas Stimme setzt sofort ein, kein Ton darüber
            put(fx, ping(), ev["t"] + 0.35, 0.8)
# Keller: Pohls schwere Schritte, Noah rennt los
s02 = SHOT["02_pohl_ruft"]
steps(s02["t0"] + 0.4, s02["t1"] + 0.3, 2.0, False, 0.6, "keller", 0.1)
steps(s02["t1"] - 0.6, t_hof, 3.4, False, 0.8, "keller", -0.05)
# Tür zum Hof fliegt auf: Schlag, Regen schwillt an
put(fx, reverb(thump(48, 0.5, 1.0) + bp(rs.randn(int(0.5 * SR)), 60, 900) * env(int(0.5 * SR), 0.004, 0.1) * 0.6,
               "hof", 0.35), t_hof - 0.02, 0.9)
rennen(t_hof + 0.1, SHOT["03_raus"]["t1"] + 0.2)
rennen(t_hof + 0.25, SHOT["03_raus"]["t1"], 3.0, 0.45)          # Ben hinterher
# Fahrer steigt aus: Tür auf, Stiefel
s05 = SHOT["05_fahrer"]
put(fx, reverb(autotuer(False), "hof", 0.12), s05["t0"] + 0.15, 0.8, 0.3)
steps(s05["t0"] + 0.9, s05["t0"] + 2.2, 1.8, True, 0.45, "hof", 0.25)
# Sander stößt die Tür auf
s08 = SHOT["08_sander_tuer"]
put(fx, reverb(thump(44, 0.6, 1.2) + bp(rs.randn(int(0.6 * SR)), 50, 1200) * env(int(0.6 * SR), 0.003, 0.15) * 0.8,
               "hof", 0.45), s08["t0"] - 0.05, 0.75, 0.15)
steps(E("k09") + 0.05, s08["t1"] + 0.6, 2.3, True, 0.3, "hof", 0.15)
# Rennen zum Auto, Türen, Zentralverriegelung
rennen(S("k10") + 0.35, t_auto - 0.1, 3.4, 0.85)
put(fx, reverb(autotuer(False), "hof", 0.1), t_auto - 0.55, 0.7, -0.2)
put(fx, reverb(autotuer(True), "auto", 0.1), t_auto + 0.02, 1.0, 0.3)
put(fx, reverb(autotuer(True), "auto", 0.1), t_auto + 0.3, 0.8, -0.35)
put(fx, zv(), t_auto + 0.62, 1.0, 0.0)
# Gurt (kurzes Ratschen + Klick)
put(fx, bp(rs.randn(int(0.25 * SR)), 1500, 7000) * env(int(0.25 * SR), 0.02, 0.1) * 0.25, E("k11") + 0.3, 1, 0.3)
put(fx, click(0.04, 1500, 8000, 120) * 0.8, E("k11") + 0.62, 1, 0.3)
# Handy des Fahrers klingelt bis er wegdrückt
s13 = SHOT["13_anruf"]
t_weg = S("k15") + 0.45
put(fx, bp(klingelton(t_weg - s13["t0"]), 400, 5000), s13["t0"], 0.9, -0.1)
put(fx, click(0.03, 1500, 6000, 150) * 0.6, t_weg, 1, -0.1)
# Bremsen an der Ampel
put(fx, bp(rs.randn(int(1.2 * SR)), 2500, 6000) * env(int(1.2 * SR), 0.3, 0.5) * 0.03, t_stop - 1.2, 1, 0)
# Noah drückt den Fensterheber: nichts passiert (Kindersicherung)
s16 = SHOT["16_finger_weg"]
for dt in (0.18, 0.42):
    put(fx, click(0.025, 1200, 6000, 160) * 0.9, s16["t0"] + dt, 1, 0.4)


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
s18 = SHOT["18_ampel_gelb"]
endk = [e["t"] for e in TL["events"] if e["kind"] == "endkarte"][0]
lvl = (0.06 + 0.04 * mask(SHOT["08_sander_tuer"]["t0"], t_auto + 1, 0.8) + 0.05 * mask(S("r6"), D + 1, 1.5)
       + 0.04 * mask(S("r7"), D + 1, 1.5))
put(mus, drone * lvl, 0)
high = pad([440.0, 466.2], D + 0.6, 1.0)[:n]
put(mus, bp(high, 300, 3000) * 0.02 * (mask(SHOT["08_sander_tuer"]["t0"], t_auto + 1, 0.6) + mask(S("r6"), D + 1, 1.5)),
    0)
# Akzente
put(mus, hit(0.3, 1.5), 0.0)
put(mus, riser(0.7, 0.3), SHOT["08_sander_tuer"]["t0"] - 0.7)
put(mus, hit(0.65), SHOT["08_sander_tuer"]["t0"] + 0.05)
put(mus, hit(0.55), S("r6") + 0.05)
put(mus, riser(0.8, 0.28), s13["t0"] - 0.6)
put(mus, hit(0.7), s13["t0"] + 0.1)
put(mus, riser(0.6, 0.25), S("k18") - 0.9)
put(mus, hit(0.55), S("k18") - 0.3)
put(mus, riser(1.4, 0.35), endk - 1.4)
heart(S("r7"), endk, 84, 122, pause=[])
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

"""#12 - the Sun will swallow Earth: 7.6 billion years in 65 seconds, every sound is a formula, as hard techno.

Each layer of the track is a physics formula and a hard techno element: the kick is the day (its tail grows with
tidal braking), the rolling rumble opens with the Sun's luminosity (Gough 1981), an acid line falls with the CO2 and
goes silent below 150 ppm, boiling oceans are rising-chirp bubbles, escaping hydrogen are sweeps that climb and fade,
the last life are fading blips N0 e^(-lambda t), Earth's orbit tone and the Sun's edge tone beat until they become one
(the drop), and the white dwarf is a single cooling ping.

Usage: python3 12_script.py audio | preview [t ...] | video | full
"""
import json
import math
import os
import subprocess
import sys
import time
import wave

import numpy as np
import skia

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kit  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ audio toolkit (filters, placement, basic drums)
SR = 48000
arng = np.random.default_rng(909)


def write_wav(path, st):
    pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def spec_filter(x, g):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * g(f), len(x))


def lowpass(x, fc, order=2):
    return spec_filter(x, lambda f: 1 / (1 + (f / fc) ** 2) ** (order / 2))


def highpass(x, fc, order=2):
    return spec_filter(x, lambda f: (f / fc) ** order / (1 + (f / fc) ** order))


def bandpass(x, lo, hi):
    return highpass(lowpass(x, hi, 4), lo, 4)


def convolve(x, h):
    n = len(x) + len(h) - 1
    size = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(h, size), size)[:len(x)]


def tt(d):
    return np.arange(int(d * SR)) / SR


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def place(buf, t0, sig, g=1.0):
    s = int(round(t0 * SR))
    if s >= len(buf) or s + len(sig) <= 0 or g == 0:
        return
    if s < 0:
        sig, s = sig[-s:], 0
    e = min(len(buf), s + len(sig))
    buf[s:e] += g * sig[:e - s]


def pan(p):
    a = (p + 1) * math.pi / 4
    return math.cos(a), math.sin(a)


def kick(drive, length=0.32, tail=0.18):
    t = tt(length)
    f = 46 + 240 * np.exp(-t / 0.024) + 50 * np.exp(-t / 0.1)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.001) * np.where(t < 0.03, 1, np.exp(-(t - 0.03) / tail))
    y = np.tanh(drive * (body + 0.5 * highpass(arng.standard_normal(len(t)), 2500) * np.exp(-t / 0.002)))
    y = lowpass(y, 7000, 2)
    y[-400:] *= np.linspace(1, 0, 400)
    return norm(y)


def gabber_kick():
    """drop 2: distorted kick with a long, tuned, screaming tail."""
    t = tt(0.36)
    f = 52 + 300 * np.exp(-t / 0.02) + 40 * np.exp(-t / 0.15)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.001) * np.exp(-t / 0.26)
    y = np.clip(9 * body, -1, 1) * 0.8 + 0.2 * np.sin(2.5 * np.pi * np.clip(body * 1.5, -1, 1))
    y = lowpass(y, 5500, 2)
    y[-400:] *= np.linspace(1, 0, 400)
    return norm(y)


def hat(decay, hp, d):
    t = tt(d)
    return norm(highpass(arng.standard_normal(len(t)), hp, 4) * np.exp(-t / decay))


def clap():
    t = tt(0.45)
    nz = bandpass(arng.standard_normal(len(t)), 900, 5000)
    env = np.zeros(len(t))
    for d in (0.0, 0.01, 0.021):
        env += (t >= d) * np.exp(-np.clip(t - d, 0, None) / 0.006)
    env += (t >= 0.028) * 0.7 * np.exp(-np.clip(t - 0.028, 0, None) / 0.13)
    return norm(np.tanh(2.4 * norm(nz * env)))


def metal(seed):
    r = np.random.default_rng(seed)
    t = tt(0.12)
    base = r.uniform(900, 1500)
    y = sum(np.sin(2 * np.pi * base * q * t + r.uniform(0, 6.28)) * np.exp(-t / d)
            for q, d in ((1.0, 0.045), (1.414, 0.03), (2.698, 0.02), (3.707, 0.014)))
    y = y + 0.5 * highpass(r.standard_normal(len(t)), 5000, 4) * np.exp(-t / 0.008)
    return norm(np.tanh(1.5 * norm(y)))


def tom(f0):
    t = tt(0.22)
    y = np.sin(2 * np.pi * np.cumsum(f0 + 90 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.09)
    return norm(np.tanh(2.0 * norm(y)))


def crash():
    t = tt(2.4)
    return norm(highpass(arng.standard_normal(len(t)), 3500) * np.exp(-t / 0.9))


def boom():
    t = tt(1.8)
    return norm(np.sin(2 * np.pi * np.cumsum(30 + 110 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.7) * (1 - np.exp(-t / 0.002)))


def euclid(k, n, rot=0):
    """Bjorklund / Euclidean rhythm E(k, n) as a list of 0/1."""
    pat = [1 if (i * k) % n < k else 0 for i in range(n)]
    return pat[rot:] + pat[:rot]



arng = np.random.default_rng(1213)


# ------------------------------------------------------------------ timing + story
BPM = 150
BEAT = 60.0 / BPM                 # 0.4 s
BAR = 4 * BEAT                    # 1.6 s
STEP = BEAT / 4
CHAP = 4 * BAR                    # one chapter = 4 bars = 6.4 s
T_D1, T_BRK, T_B2, T_D2, T_WD = (b * BAR for b in (16, 24, 28, 32, 36))
DUR = 41 * BAR                    # 65.6 s
GAPS = [T_D2 - BEAT]
ROOT = 43.65                      # F1
F_E = 349.23                      # F4: the tone of Earth's orbit
CHAPTERS = ["TODAY", "THE SUN GETS BRIGHTER", "THE DAYS GET LONGER", "THE FORESTS GO QUIET", "THE OCEANS BOIL",
            "EARTH TURNS INTO VENUS", "THE LAST LIFE", "THE SUN SWELLS", "THE SUN SWALLOWS EARTH", "A WHITE DWARF", "THE END"]
YK_T = [0.0, 6.4, 12.8, 19.2, 25.6, 32.0, 38.4, 44.8, 51.2, 57.6, 64.0, 65.6]
YK_Y = [1e4, 1e7, 3e8, 6e8, 1.0e9, 1.5e9, 2.5e9, 5.0e9, 7.59e9, 7.62e9, 1.0e10, 1.05e10]


def chap(t):
    return min(10, int(t / CHAP))


def in_gap(t):
    return any(g <= t < g + BEAT for g in GAPS)


def lerp_log(x, xs, ys):
    return float(10 ** np.interp(x, xs, np.log10(ys)))


def years(t):
    return lerp_log(t, YK_T, YK_Y)


def sun_L(tau):
    if tau < 5e9:
        return 1.0 / (1 - 0.4 * tau / 4.57e9)          # Gough (1981): L = L_sun / (1 + 2/5 (1 - t/t_sun))
    if tau <= 7.59e9:
        return lerp_log(tau, [5e9, 7.0e9, 7.59e9], [1.78, 30.0, 2700.0])
    return 0.01


def sun_R(tau):
    if tau < 5e9:
        return 1 + 0.6 * tau / 5e9
    if tau <= 7.59e9:
        return lerp_log(tau, [5e9, 7.0e9, 7.59e9], [1.6, 10.0, 256.0])
    return 0.0092


def earth_T(tau):
    return lerp_log(max(tau, 1.0), [1.0, 1e9, 1.5e9, 2.5e9, 5e9, 7.5e9, 7.59e9], [15.0, 50.0, 110.0, 465.0, 900.0, 1800.0, 3000.0])


def co2(tau):
    return lerp_log(max(tau, 1.0), [1.0, 6e8, 9e8, 1.5e9, 1e11], [420.0, 150.0, 10.0, 1.0, 1.0])


# ------------------------------------------------------------------ new sounds for #11
G_KERNEL = None


def spark_grain(seed):
    r = np.random.default_rng(seed)
    t = tt(0.0016)
    g = r.standard_normal(len(t)) * np.exp(-t / 0.00035) + 0.7 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.0005)
    g[0] += 2.5
    return g


def tc_note(d, f_a, f_b, acc, seed):
    """singing Tesla coil: one spark burst per period -> a buzzing pulse train at the note's pitch."""
    r = np.random.default_rng(seed)
    n = int((d + 0.004) * SR)
    t = np.arange(n) / SR
    ph = np.cumsum(f_a + (f_b - f_a) * np.clip(t / d, 0, 1)) / SR
    imp = np.zeros(n)
    idx = np.where(np.diff(np.floor(ph)) > 0)[0] + 1
    imp[0] = 1.0
    imp[idx] = r.uniform(0.75, 1.15, len(idx)) * (1.15 if acc else 1.0)
    cr = r.random(n) < 260 / SR
    imp[cr] += r.uniform(0.15, 0.4, int(cr.sum()))
    return convolve(imp, G_KERNEL) * np.minimum(1, t / 0.001) * np.clip((d + 0.004 - t) / 0.004, 0, 1)


def svf_lowpass(x, fc, k):
    """TPT state-variable lowpass (Simper/Zavalishin) with time-varying cutoff and resonance."""
    g = np.tan(np.pi * np.minimum(fc, 0.45 * SR) / SR)
    a1 = 1 / (1 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    xs, A1, A2, A3 = x.tolist(), a1.tolist(), a2.tolist(), a3.tolist()
    o = [0.0] * len(xs)
    ic1 = ic2 = 0.0
    for i in range(len(xs)):
        v3 = xs[i] - ic2
        v1 = A1[i] * ic1 + A2[i] * v3
        v2 = ic2 + A2[i] * ic1 + A3[i] * v3
        ic1 = 2 * v1 - ic1
        ic2 = 2 * v2 - ic2
        o[i] = v2
    return np.array(o)


def hard_kick(drive=9.0, tail=0.28, f_end=ROOT, click=0.6, seed=1):
    """hard techno kick: fast pitch drop into a tuned G1 tail, overdriven and clipped, mid 'knock' + click."""
    r = np.random.default_rng(seed)
    t = tt(0.55)
    f = f_end + 260 * np.exp(-t / 0.011) + 70 * np.exp(-t / 0.06)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, t / 0.0005) * np.where(t < 0.03, 1.0, np.exp(-(t - 0.03) / tail))
    y = np.clip(1.25 * np.tanh(drive * (x + 0.3 * x * x)), -1, 1)
    y = y + 0.6 * bandpass(y, 110, 420)
    tok = np.sin(2 * np.pi * 1300 * t) * np.exp(-t / 0.004)
    y = y + click * (highpass(r.standard_normal(len(t)), 3000, 2) * np.exp(-t / 0.0015) + 0.6 * tok)
    y = highpass(lowpass(y, 10000, 2), 25, 2) * np.minimum(1, (t[-1] - t) / 0.01)
    return norm(y)


def rumble_hit(f, d=0.085, seed=0):
    """one 'roll' of the rolling bass: a tuned, overdriven low hit between the kicks."""
    r = np.random.default_rng(seed)
    t = tt(d)
    x = np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t / 0.045)
    x = x + 0.3 * lowpass(r.standard_normal(len(t)), 400, 2) * np.exp(-t / 0.03)
    y = np.tanh(6.0 * x)
    y = lowpass(y, 900, 2) + 0.4 * bandpass(y, 90, 300)
    return norm(y * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.01))


def schranz_hit(seed):
    r = np.random.default_rng(seed)
    t = tt(0.07)
    y = bandpass(r.standard_normal(len(t)), 2500, 7000) * np.exp(-t / 0.018) + 0.5 * metal(seed)[:len(t)]
    return norm(np.tanh(2.5 * norm(y)))


def saw(ph):
    return 2 * (ph % 1.0) - 1


def hoover(f0, d=0.7, seed=0):
    """rave hoover: detuned pulse-ish saws with a pitch dive at the start, plus a sub octave."""
    r = np.random.default_rng(seed)
    t = tt(d)
    f = f0 * 2 ** ((5 * np.exp(-t / 0.03) - 2 * t / d) / 12)
    y = np.zeros(len(t))
    for k, det in enumerate((-0.012, -0.007, -0.003, 0.0, 0.003, 0.007, 0.012)):
        ph = np.cumsum(f * (1 + det)) / SR + r.uniform(0, 1)
        y += saw(ph) - 0.7 * saw(ph + 0.3 + 0.15 * np.sin(2 * np.pi * 0.9 * t + k)) + 0.5 * saw(ph / 2)
    env = np.minimum(1, t / 0.006) * np.clip((d - t) / 0.12, 0, 1)
    return norm(np.tanh(2.0 * norm(lowpass(y, 4000, 2))) * env)


def rave_stab(freqs, d=0.22, seed=0):
    r = np.random.default_rng(seed)
    t = tt(d)
    y = sum(saw(f0 * (1 + det) * t + r.uniform(0, 1)) for f0 in freqs for det in (-0.008, 0.0, 0.008))
    y = lowpass(y, 2800, 2) * np.minimum(1, t / 0.003) * np.exp(-t / 0.09)
    return norm(np.tanh(1.8 * norm(y)))


def siren(d):
    t = tt(d)
    u = t / d
    f = 500 * 2 ** (1.6 * u) * (1 + 0.04 * np.sin(2 * np.pi * 7 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * u ** 1.5


def pitched(x, ratio):
    return np.interp(np.arange(int(len(x) / ratio)) * ratio, np.arange(len(x)), x)


def zap_hat(seed):
    r = np.random.default_rng(seed)
    t = tt(0.05)
    y = highpass(r.standard_normal(len(t)), 7500, 4) * np.exp(-t / 0.009)
    y = y + 0.5 * np.sin(2 * np.pi * np.cumsum(2500 + 9000 * np.exp(-t / 0.004)) / SR) * np.exp(-t / 0.004)
    return norm(y)


def snare():
    t = tt(0.4)
    body = np.sin(2 * np.pi * np.cumsum(185 + 60 * np.exp(-t / 0.01)) / SR) * np.exp(-t / 0.05)
    return norm(np.tanh(2.0 * (clap()[:len(t)] + 0.7 * body)))


def crackle(seed):
    r = np.random.default_rng(seed)
    t = tt(0.06)
    y = bandpass(r.standard_normal(len(t)), 1500, 6000) * np.exp(-t / 0.01)
    y[0] += 3.0
    y = y + 0.4 * np.sin(2 * np.pi * np.cumsum(300 + 4000 * np.exp(-t / 0.003)) / SR) * np.exp(-t / 0.006)
    return norm(y)


def thunder(seed, d=4.0, crack=1.0):
    r = np.random.default_rng(seed)
    t = tt(d)
    rum = lowpass(highpass(np.cumsum(r.standard_normal(len(t))), 25, 2), 170, 4)
    env = (1 - np.exp(-t / 0.04)) * np.exp(-t / (d * 0.35)) * (1 + 0.5 * np.sin(2 * np.pi * 1.3 * t + 1))
    m = int(0.7 * SR)
    cr = np.zeros(len(t))
    hits = r.random(m) < (900 / SR) * np.exp(-np.arange(m) / SR / 0.25)
    cr[:m][hits] = r.uniform(0.3, 1.0, int(hits.sum()))
    gl = int(0.003 * SR)
    cr = bandpass(convolve(cr, r.standard_normal(gl) * np.exp(-np.arange(gl) / SR / 0.0008)), 300, 4000)
    return norm(np.tanh(1.6 * norm(norm(rum * env) + 0.8 * crack * norm(cr))))


def shout(f0, seed):
    r = np.random.default_rng(seed)
    t = tt(0.34)
    ph = 2 * np.pi * np.cumsum(f0 * (1.12 - 0.22 * t / t[-1])) / SR
    src = sum(np.sin(h * ph) / h ** 0.9 for h in range(1, 28)) + 0.25 * r.standard_normal(len(t))

    def formant(x, F):
        return spec_filter(x, lambda fr: sum(g * np.exp(-((fr - fc) / bw) ** 2) for fc, bw, g in F))
    e_ = formant(src, [(560, 90, 1.0), (1800, 130, 0.7), (2550, 180, 0.45)])
    i_ = formant(src, [(330, 70, 1.0), (2250, 140, 0.8), (2950, 200, 0.4)])
    mv = np.clip((t - 0.12) / 0.12, 0, 1)
    y = norm(e_ * (1 - mv) + i_ * mv) * np.minimum(1, t / 0.012) * np.exp(-np.clip(t - 0.16, 0, None) / 0.06)
    y = y + 0.6 * highpass(r.standard_normal(len(t)), 900, 2) * np.exp(-t / 0.03) * (t < 0.06)
    return norm(np.tanh(2.2 * norm(y)))


def crowd_hey(seed=0):
    out = np.zeros(int(0.4 * SR))
    for k, (f0, dl) in enumerate(((175, 0.0), (190, 0.006), (205, 0.011), (226, 0.017))):
        place(out, dl, shout(f0, seed * 10 + k), 1.0)
    return norm(out)


def tape_stop(x, t0, t1):
    i0, i1 = int(t0 * SR), int(t1 * SR)
    rate = np.linspace(1.0, 0.0, i1 - i0) ** 1.3
    pos = i0 + np.concatenate([[0.0], np.cumsum(rate)[:-1]])
    fade = np.linspace(1.0, 0.25, i1 - i0)
    for c_ in range(x.shape[1]):
        x[i0:i1, c_] = np.interp(pos, np.arange(i0, i1), x[i0:i1, c_]) * fade


# ------------------------------------------------------------------ sounds for #12: every layer is a formula
def bubble(f0, seed):
    """boiling ocean: one bubble = an exponential upward chirp f(t) = f0 e^(t/tau)."""
    r = np.random.default_rng(seed)
    t = tt(0.07)
    y = np.sin(2 * np.pi * np.cumsum(f0 * np.exp(t / 0.035)) / SR) * np.exp(-t / 0.02) * np.minimum(1, t / 0.002)
    return norm(y + 0.15 * highpass(r.standard_normal(len(t)), 3000, 2) * np.exp(-t / 0.004))


def escape_sweep(d=0.7):
    """hydrogen escaping: climbs and fades before it can fall back."""
    t = tt(d)
    u = t / d
    f = 280 * 12 ** u
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(2.01 * f) / SR)
    return norm(y * np.sin(np.pi * np.minimum(1, u * 1.2)) ** 1.5 * (1 - u))


def life_blip(f):
    t = tt(0.09)
    return norm(np.sin(2 * np.pi * f * t * (1 + 0.004 * np.sin(2 * np.pi * 30 * t))) * np.exp(-t / 0.025) * np.minimum(1, t / 0.001))


def dwarf_ping(f, bright=1.0):
    t = tt(1.6)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.5) + bright * 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t / 0.15)
    return norm(y * np.minimum(1, t / 0.002))


def acid_note(d, fa, fb):
    t = tt(d + 0.004)
    ph = np.cumsum(fa + (fb - fa) * np.clip(t / d, 0, 1)) / SR
    y = saw(ph) + 0.3 * np.sign(np.sin(2 * np.pi * ph))
    return y * np.minimum(1, t / 0.002) * np.clip((d + 0.004 - t) / 0.004, 0, 1)


R_ACID = [(0, 1, 0), None, (12, 1, 0), (0, 0, 0), (3, 0, 0), None, (0, 1, 0), (7, 0, 1),
          (12, 1, 0), None, (0, 0, 0), (10, 1, 0), None, (3, 0, 0), (12, 1, 1), (15, 0, 0)]
PENTA = [349.23, 415.30, 466.16, 523.25, 622.25]
LIFE_F = [1046.5, 1244.5, 1396.9, 1568.0]
GATE2 = [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1]


def make_audio(path):
    n = int(DUR * SR)
    t = np.arange(n) / SR
    names = ("kick", "rum_src", "rumb", "hat_l", "hat_r", "perc_l", "perc_r", "snare", "acid", "bubble_l", "bubble_r",
             "escape", "life", "clash", "dwarf", "pad", "fx", "boom", "post")
    ch = {k: np.zeros(n) for k in names}
    KT = [hard_kick(9.0 if c < 8 else 13.0, 0.16 + 0.02 * c, f_end=ROOT, click=0.6 if c < 8 else 0.8, seed=c + 1) for c in range(11)]
    KF = norm(lowpass(KT[6], 320, 4))
    RUMB0 = rumble_hit(ROOT, seed=61)
    FC = [220, 380, 560, 760, 1300, 1300, 300, 900, 1500, 600, 600]
    RG = [0.5, 0.65, 0.75, 0.8, 1.0, 1.0, 0.4, 0.8, 1.0, 0.6, 0.5]
    RUMB = [norm(lowpass(RUMB0, fc, 2)) for fc in FC]
    HO, SN = hat(0.06, 6500, 0.25), snare()
    ZH = [zap_hat(30 + i) for i in range(4)]
    RIDE = [metal(40 + i) for i in range(3)]
    E9, E13 = euclid(9, 16), euclid(13, 16)
    kicks, life_ev = [], []
    pl, pr = pan(-0.5), pan(0.5)

    def add_kick(tk, k, g=1.0):
        place(ch["kick"], tk, k, g)
        place(ch["rum_src"], tk, k, g)
        kicks.append(tk)

    def stereo(name, tq, sig, g, side):
        a, b = pl if side < 0 else pr
        place(ch[name + "_l"], tq, sig, g * a)
        place(ch[name + "_r"], tq, sig, g * b)

    for bi in range(int(round(DUR / BEAT))):
        bt = bi * BEAT
        q, bar = bi % 4, bi // 4
        c = chap(bt + 1e-4)
        if in_gap(bt):
            continue
        if c == 6 or (c == 9 and bar >= 38):          # the last life / the white dwarf: muffled heartbeat
            add_kick(bt, KF, 0.8 if c == 6 else 0.75 - 0.2 * (bar - 38))
        elif c == 10:
            if q == 0:
                add_kick(bt, KT[9], 0.7)
        elif bar not in (15, 31):
            add_kick(bt, KT[c])
        if bar not in (15, 31) and c < 10 and not (c == 9 and bar >= 38):   # the Sun: rolling rumble, brighter with L
            for s16, g in ((1, 0.55), (2, 0.85), (3, 0.65)):
                place(ch["rumb"], bt + s16 * STEP, RUMB[c], g * RG[c])
        if c < 10:
            stereo("hat", bt + 2 * STEP, HO, 0.3 if c in (6, 9) else 0.48, 1 if q % 2 else -1)
        if 1 <= c <= 8 and c != 6:
            stereo("hat", bt + STEP, ZH[bi % 4], 0.33, -1)
            stereo("hat", bt + 3 * STEP, ZH[(bi + 2) % 4], 0.42, 1)
        if c in (4, 5, 8):
            for s16 in range(4):
                stereo("perc", bt + s16 * STEP, RIDE[(bi + s16) % 3], 0.2 + 0.12 * (s16 == 2), 1 if s16 % 2 else -1)
        if q in (1, 3) and 1 <= c <= 8 and c != 6:
            place(ch["snare"], bt, SN, 1.0)
        if c == 6 and q == 3 and bar % 2 == 1:
            place(ch["snare"], bt, SN, 0.6)
    for rb in (15, 31):                      # kick roll + snare roll into both drops
        t0 = rb * BAR
        nb16 = 8 if rb == 15 else 4
        for k, tk in enumerate([t0 + k * BEAT / 2 for k in range(4)] + [t0 + 2 * BEAT + k * STEP for k in range(nb16)]):
            add_kick(tk, pitched(KT[3 if rb == 15 else 7], 2 ** (k / 12)), 0.8 + 0.03 * k)
        for k in range(8):
            place(ch["snare"], t0 - BAR + k * BEAT / 2, SN, 0.35 + 0.03 * k)
        for k in range(16 if rb == 15 else 12):
            place(ch["snare"], t0 + k * STEP, SN, 0.5 + 0.03 * k)
    # --- CO2 acid (bars 4-15): its pitch falls with the CO2, below 150 ppm it goes silent
    ev = []
    for bar in range(4, 16):
        for s, stp in enumerate(R_ACID):
            if stp is None:
                continue
            te = bar * BAR + s * STEP
            drop_semi = -8 * min(1.0, max(0.0, (te - 3 * CHAP) / CHAP))
            semi, acc, slide = stp
            nxt = R_ACID[(s + 1) % 16]
            sb = (nxt[0] if (slide and nxt) else semi)
            d = STEP * (1.02 if slide and nxt else 0.7)
            ev.append((te, d, semi + drop_semi, sb + drop_semi, acc))
    raw, env = np.zeros(n), np.zeros(n)
    L_env = int(0.35 * SR)
    ar = np.arange(L_env) / SR
    for (te, d, sa, sb, acc) in ev:
        place(raw, te, acid_note(d, 87.31 * 2 ** (sa / 12), 87.31 * 2 ** (sb / 12)), 1.2 if acc else 1.0)
        i0 = int(te * SR)
        e = min(n, i0 + L_env)
        env[i0:e] = np.maximum(env[i0:e], ((2.6 if acc else 1.3) * np.exp(-ar / (0.16 if acc else 0.09)))[:e - i0])
    base = np.interp(t, [0, CHAP, 2 * CHAP, 3 * CHAP, 4 * CHAP], [400, 450, 900, 1500, 500])
    acid = svf_lowpass(raw, np.clip(base * (1 + env), 60, 12000), 0.22)
    acid = np.tanh(3.5 * acid / (np.percentile(np.abs(acid[acid != 0]), 99.5) + 1e-9))
    acid *= np.interp(t, [0, CHAP, 2 * CHAP, 3 * CHAP, 4 * CHAP - BAR, 4 * CHAP], [0, 0.6, 0.85, 1.0, 1.0, 0.0])
    ch["acid"] = acid
    # --- boiling oceans: one bubble per hit, more heat = more bubbles (bars 16-23)
    for bar in list(range(16, 24)) + list(range(32, 36)):
        pat = E9 if bar < 20 else E13
        for s in range(16):
            if pat[s]:
                k = bar * 16 + s
                stereo("bubble", bar * BAR + s * STEP, bubble(PENTA[(k * 3) % 5] * (2 if s % 4 == 2 else 1), 500 + k),
                       0.55 + 0.2 * (s % 4 == 0), -1 if k % 2 else 1)
    # --- hydrogen escaping (bars 20-23): sweeps that climb and fade
    SW = escape_sweep()
    for bar in range(20, 24):
        for qq in (0, 2):
            place(ch["escape"], bar * BAR + qq * BEAT, SW, 0.6)
    # --- the last life (bars 24-27): blips that fade and drop out
    rl = np.random.default_rng(77)
    for k in range(32):
        te = T_BRK + k * BEAT / 2
        alive = math.exp(-(te - T_BRK) / 3.5)
        if rl.random() < alive:
            place(ch["life"], te, life_blip(LIFE_F[(k * 5) % 4]), alive)
            life_ev.append(te)
    # --- the clash (bars 28-31): Earth's orbit tone vs the Sun's edge, |f_E - f_S| = 8, 4, 2, 1 wobbles per bar
    seg = slice(int(T_B2 * SR), int((T_D2 - BEAT) * SR))
    ts = t[seg]
    kk = np.array([8, 4, 2, 1], float)[np.minimum(3, ((ts - T_B2) / BAR).astype(int))]
    cyc_s = np.cumsum(F_E - kk / BAR) / SR
    cyc_s += F_E * ts[0] - cyc_s[0]
    grow = (ts - T_B2) / (4 * BAR)
    tone = lowpass(saw(F_E * ts) + saw(cyc_s), 2500, 2)
    ch["clash"][seg] = np.tanh((1 + 2.5 * grow) * tone) * (0.35 + 0.65 * grow)
    # --- swallowed (bars 32-35): two tones became one, gated and screaming
    i0, i1 = int(T_D2 * SR), int(T_WD * SR)
    ts = t[i0:i1]
    uni = lowpass(np.tanh(4 * (saw(F_E * ts) + 0.7 * saw(F_E / 2 * ts))), 3000, 2)
    gate = np.zeros(i1 - i0)
    for s in range(int(round((T_WD - T_D2) / STEP))):
        if GATE2[s % 16]:
            a0, a1 = int(s * STEP * SR), int((s + 0.85) * STEP * SR)
            gate[a0:a1] = np.exp(-np.arange(a1 - a0) / SR / 0.07)
    ch["clash"][i0:i1] += 1.35 * uni * gate
    # --- the white dwarf (bars 36-40): one cold ping, cooling
    for bar in range(36, 41):
        for qq in range(4):
            if bar < 38 or (bar < 40 and qq % 2 == 0) or (bar == 40 and qq == 0):
                place(ch["dwarf"], bar * BAR + qq * BEAT, dwarf_ping(1396.9, max(0.2, 1 - 0.2 * (bar - 36))), 0.8)
    # --- pad under the last life, impacts, risers
    m = int(CHAP * SR)
    tp = np.arange(m) / SR
    pad = np.zeros(m)
    for f0 in (87.31, 103.83, 130.81, 174.61):
        for det in (-0.005, 0.005):
            for h in range(1, 14):
                if f0 * h > 2500:
                    break
                pad += np.sin(2 * np.pi * f0 * (1 + det) * h * tp + arng.uniform(0, 6.28)) / h
    place(ch["pad"], T_BRK, norm(lowpass(pad, 1000)) * np.minimum(1, tp / 0.6) * np.minimum(1, (tp[-1] - tp) / 0.4))
    for td in (T_D1, T_D2):
        place(ch["boom"], td, boom(), 1.0)
        place(ch["fx"], td, crash(), 0.6)
    place(ch["fx"], T_WD, crash(), 0.5)
    place(ch["boom"], T_WD, boom(), 0.6)
    rev = crash()[::-1]
    place(ch["post"], T_D2 - len(rev) / SR, rev * np.linspace(0, 1, len(rev)) ** 2, 0.5)
    place(ch["fx"], T_WD - len(rev) / SR, rev * np.linspace(0, 1, len(rev)) ** 2, 0.4)
    place(ch["fx"], GAPS[0] - 2 * BAR, siren(2 * BAR), 0.35)
    # --- mix + master
    last = np.full(n, -10.0)
    for kt in sorted(kicks):
        last[int(kt * SR):] = kt
    since = t - last
    duck_hard = np.clip((since - 0.02) / 0.13, 0, 1) ** 1.5
    duck_soft = 1 - 0.45 * np.exp(-since / 0.08)
    il = int(1.0 * SR)
    ti = np.arange(il) / SR
    ir = arng.standard_normal(il) * np.exp(-ti / 0.25)
    ir[:int(0.006 * SR)] = 0
    rum = np.tanh(4.0 * norm(lowpass(convolve(ch["rum_src"], ir / np.sqrt(np.sum(ir ** 2))), 170, 4) + 1e-9))
    rl_ = int(2.0 * SR)
    tr = np.arange(rl_) / SR
    irl = lowpass(arng.standard_normal(rl_), 6500) * np.exp(-tr / 0.42)
    irr = lowpass(arng.standard_normal(rl_), 6500) * np.exp(-tr / 0.42)
    for ir_ in (irl, irr):
        ir_[:int(0.02 * SR)] = 0
        ir_ /= np.sqrt(np.sum(ir_ ** 2))
    bub = ch["bubble_l"] + ch["bubble_r"]
    send = 0.55 * ch["snare"] + 0.3 * bub + 0.4 * ch["escape"] + 0.5 * ch["life"] + 0.6 * ch["dwarf"] + 0.4 * ch["pad"] + 0.2 * ch["clash"]
    wl, wr = convolve(send, irl), convolve(send, irr)
    wr *= np.sqrt(np.mean(wl ** 2) / (np.mean(wr ** 2) + 1e-12))
    common = (1.0 * ch["kick"] + 0.30 * rum * duck_hard + 0.55 * ch["rumb"] * duck_hard + 0.42 * ch["acid"] * duck_soft
              + 0.85 * ch["boom"] + (0.42 * ch["snare"] + 0.25 * ch["fx"]) * duck_soft + 0.30 * ch["escape"]
              + 0.40 * ch["life"] + 0.38 * ch["clash"] * duck_soft + 0.45 * ch["dwarf"] + 0.25 * ch["pad"])
    L = common + (0.19 * ch["hat_l"] + 0.2 * ch["perc_l"] + 0.3 * ch["bubble_l"]) * duck_soft + 0.12 * wl
    R = common + (0.19 * ch["hat_r"] + 0.2 * ch["perc_r"] + 0.3 * ch["bubble_r"]) * duck_soft + 0.12 * wr
    bus = np.stack([L, R], 1)
    bus *= np.interp(t, [0, CHAP, T_D1 - BAR, T_D1, T_BRK, T_BRK + 0.01, T_B2, T_D2 - BEAT, T_D2, T_WD, DUR],
                     [0.8, 0.85, 0.95, 1.0, 1.0, 0.8, 0.86, 1.0, 1.0, 0.95, 0.9])[:, None]
    for g in GAPS:
        i0, i1 = int(g * SR), int((g + BEAT) * SR)
        k = int(0.012 * SR)
        ramp = np.full(i1 - i0, 0.04)
        ramp[:k] = np.linspace(1, 0.04, k)
        bus[i0:i1] *= ramp[:, None]
    bus += 0.5 * ch["post"][:, None]
    bus -= 0.35 * lowpass(bus.mean(1), 45, 4)[:, None]
    low = lowpass(bus.mean(1), 120, 4)
    pk = np.percentile(np.abs(low), 99.9) + 1e-9
    bus = bus - low[:, None] + (np.tanh(1.4 * low / pk) * pk)[:, None]
    bus /= np.percentile(np.abs(bus), 99.9) / 0.95
    bus = np.tanh(1.9 * bus) / np.tanh(1.9)
    bus *= np.minimum(1, (DUR - t) / 0.8)[:, None]
    bus *= 0.9 / np.max(np.abs(bus))
    write_wav(path, bus)
    hop = SR // 30
    envs = []
    for x in (ch["kick"], ch["rumb"], ch["acid"], bub, ch["escape"], ch["life"], ch["clash"], ch["dwarf"]):
        m_ = len(x) // hop
        e = np.sqrt(np.mean(x[:m_ * hop].reshape(m_, hop) ** 2, axis=1))
        envs.append(np.clip(e / (np.percentile(e[e > 0], 99) + 1e-9), 0, 1) if (e > 0).any() else e)
    np.savez_compressed(os.path.join(OUT, "stems.npz"), kicks=np.array(sorted(kicks)), env=np.array(envs, np.float32),
                        life=np.array(life_ev))
    print("audio written")


def loudnorm(src, dst, target=-9.5):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af",
                        f"loudnorm=I={target}:TP=-1.0:LRA=20:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    gain = min(target - float(m["input_i"]), -1.0 - float(m["input_tp"]))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", f"volume={gain:.2f}dB",
                    "-ar", str(SR), dst], check=True)
    print(f"audio in: {m['input_i']} LUFS / TP {m['input_tp']} -> linear gain {gain:+.2f} dB")


# ------------------------------------------------------------------ video
W, H, FPS = 1080, 1920, 60
PINK, CYAN, AMBER, VIOLET, GREEN, RED, WHITE = (255, 80, 170), (80, 220, 255), (255, 176, 60), (160, 110, 255), (70, 240, 150), (255, 64, 84), (235, 240, 255)
LAYER = ["DAY", "SUN", "CO2", "OCEAN", "ESCAPE", "LIFE", "CLASH", "DWARF"]
LCOL = [(255, 214, 90), (255, 140, 60), (90, 220, 120), (70, 170, 255), (180, 140, 255), (120, 255, 200), (255, 70, 90), (230, 240, 255)]
CH_LAYER = [0, 1, 0, 2, 3, 4, 5, 6, 6, 7, 7]
SCOPE_TXT = ["y = sgn(sin 2πx)", "y = L(τ) · saw(x)", "y = e^(−kx) · cos 6πx,  k ↓", "y = sin(2π f x),  f ∝ log CO2",
             "y = e^(−14x) · sin(2π f0 e^(3x) x)", "y = sin(36πx²) · (1 − x)", "y = N0 e^(−λt) · blip(x)",
             "y = sin 2π f_E x + sin 2π f_S x", "y = clip(2 sin 2πfx)", "y = e^(−6x) · sin 20πx", "y = e^(−6x) · sin 20πx"]
FD = "/usr/share/fonts/opentype/inter/"
TF_BLACK = skia.Typeface.MakeFromFile(FD + "InterDisplay-Black.otf")
TF_SEMI = skia.Typeface.MakeFromFile(FD + "Inter-SemiBold.otf")
SAMP = kit.SAMP
C, paint, ease = kit.C, kit.paint, kit.ease
NO_FLASH = False


def clip01(x):
    return min(1.0, max(0.0, x))


def mixc(a, b, u):
    return tuple(a[j] + (b[j] - a[j]) * u for j in range(3))


def font(tf, size):
    f = skia.Font(tf, size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def fit(tf, size, text, max_w):
    f = font(tf, size)
    w = f.measureText(text)
    return font(tf, size * max_w / w) if w > max_w else f


TITLE1, TITLE2 = "THE SUN WILL SWALLOW EARTH", "EVERY SOUND IS A FORMULA"
F_T1 = fit(TF_BLACK, 66, TITLE1, 960)
F_T2 = fit(TF_BLACK, 52, TITLE2, 760)
TITLE_Y = (300, 366)
CAP_Y = 440


def text_c(c, s_, x, y, f, color, glow=None, blur=14):
    w = f.measureText(s_)
    if glow is not None:
        c.drawString(s_, x - w / 2, y, f, paint(glow, blur=blur))
    c.drawString(s_, x - w / 2, y, f, paint(color))


def glow_sprite(rgb, size=200):
    s_ = skia.Surface(size, size)
    c = s_.getCanvas()
    c.clear(skia.Color(0, 0, 0, 0))
    sh = skia.GradientShader.MakeRadial((size / 2, size / 2), size / 2, [C(rgb, 255), C(rgb, 90), C(rgb, 0)], [0, 0.22, 1])
    c.drawCircle(size / 2, size / 2, size / 2, skia.Paint(AntiAlias=True, Shader=sh))
    return s_.makeImageSnapshot()


GLOW = {"white": glow_sprite(WHITE), "sun": glow_sprite((255, 200, 120), 600), "red": glow_sprite((255, 90, 40), 600),
        "green": glow_sprite((120, 255, 160)), "blue": glow_sprite((150, 200, 255), 400)}


def sprite(c, img, x, y, alpha, size):
    if alpha <= 0.01:
        return
    p = skia.Paint(Alphaf=min(1.0, alpha))
    p.setBlendMode(skia.BlendMode.kPlus)
    c.drawImageRect(img, skia.Rect(x - size / 2, y - size / 2, x + size / 2, y + size / 2), SAMP, p)


VX0, VY0, VX1, VY1 = 60, 488, 1020, 1000
VIEW = skia.Rect(VX0, VY0, VX1, VY1)
SUNX, SUNY = 210.0, 744.0
EX, EY, ER = 800.0, 744.0, 66
ST, BG, VIEW_BG = None, None, None
FIELD = CLOUD = None
LAND_Q = 0.5
_n = 2 * ER + 2
_yy, _xx = np.mgrid[0:_n, 0:_n]
NX = (_xx + 0.5 - _n / 2) / ER
NY = (_yy + 0.5 - _n / 2) / ER
RR = NX ** 2 + NY ** 2
NZ = np.sqrt(np.clip(1 - RR, 0, 1))
LAT = np.arcsin(np.clip(-NY, -1, 1))
LON0 = np.arctan2(NX, NZ)
EDGE_A = np.clip((1.0 - np.sqrt(RR)) * ER + 0.5, 0, 1)
LIGHT = np.clip(-0.85 * NX + 0.45 * NZ - 0.1 * NY, 0, 1)
RIM = np.clip((np.sqrt(RR) - 0.82) / 0.18, 0, 1) * (RR <= 1)


def make_textures():
    global FIELD, CLOUD, LAND_Q
    W_, H_ = 512, 256
    lo = (np.arange(W_) + 0.5) / W_ * 2 * np.pi
    la = (np.arange(H_) + 0.5) / H_ * np.pi - np.pi / 2
    LO, LA = np.meshgrid(lo, la)
    Pp = np.stack([np.cos(LA) * np.cos(LO), np.cos(LA) * np.sin(LO), np.sin(LA)], -1)

    def field(nb, s0, s1, seed):
        rr = np.random.default_rng(seed)
        f = np.zeros(LO.shape)
        for _ in range(nb):
            cc = rr.normal(size=3)
            cc /= np.linalg.norm(cc)
            f += rr.uniform(0.5, 1.0) * np.exp(-np.sum((Pp - cc) ** 2, -1) / rr.uniform(s0, s1) ** 2)
        return (f - f.min()) / (f.max() - f.min())
    FIELD, CLOUD = field(70, 0.15, 0.45, 11), field(140, 0.05, 0.16, 12)
    LAND_Q = float(np.percentile(FIELD, 70))


def earth_image(t):
    W_, H_ = FIELD.shape[1], FIELD.shape[0]
    lon = (LON0 + 2 * np.pi * t / (8 * BEAT)) % (2 * np.pi)
    ii = (lon / (2 * np.pi) * W_).astype(int) % W_
    jj = np.clip(((LAT + np.pi / 2) / np.pi * H_).astype(int), 0, H_ - 1)
    fld = FIELD[jj, ii]
    cld = CLOUD[jj, (ii + int(t * 9)) % W_]
    brown, dry = clip01((t - 3 * CHAP) / CHAP), clip01((t - 4 * CHAP) / CHAP)
    haze, molten = clip01((t - 5 * CHAP) / CHAP), clip01((t - 6.5 * CHAP) / (1.5 * CHAP))
    land_col = np.array(mixc((50, 140, 60), (150, 115, 70), brown))
    sea = fld <= LAND_Q - 0.22 * dry
    seabed = (~sea) & (fld <= LAND_Q)
    col = np.where(sea[..., None], np.array([25.0, 75.0, 190.0]), np.where(seabed[..., None], np.array([175.0, 160.0, 140.0]), land_col))
    cov = np.clip((cld - (0.62 - 0.3 * dry - 0.4 * haze)) * 6, 0, 1)[..., None]
    col = col * (1 - cov) + 245.0 * cov
    col = col * (1 - 0.9 * haze) + np.array([228.0, 196.0, 120.0]) * 0.9 * haze
    col = col * (1 - molten) + np.array([70.0, 16.0, 8.0]) * molten
    lit = col * (0.1 + 0.9 * LIGHT[..., None])
    cracks = (np.abs((fld * 14) % 1 - 0.5) < 0.07) * molten
    lit += np.array([255.0, 120.0, 30.0]) * cracks[..., None] * 0.9
    heat = clip01((t - 7 * CHAP) / CHAP)
    lit += np.array([255.0, 90.0, 40.0]) * (0.7 * heat) * LIGHT[..., None]
    lit += np.array([80.0, 150.0, 255.0]) * (RIM * LIGHT ** 0.5 * (1 - haze) * (1 - molten))[..., None] * 0.8
    a = (EDGE_A * (RR <= 1.0))[..., None]
    rgba = np.concatenate([np.clip(lit, 0, 255) * a, 255 * a], -1).astype(np.uint8)
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)


def sun_state(t):
    if t < T_B2:
        return 46 * sun_R(years(t)) ** 0.6, mixc((255, 244, 214), (255, 214, 160), clip01(t / T_B2))
    if t < T_D2:
        u = (t - T_B2) / (T_D2 - T_B2)
        return 62 * (660 / 62) ** (u ** 1.3), mixc((255, 200, 140), (255, 110, 55), u)
    return 900.0, (255, 100, 50)


def draw_sun(c, t):
    r, col = sun_state(t)
    sprite(c, GLOW["sun"] if t < T_B2 else GLOW["red"], SUNX, SUNY, 0.75, min(2600, 6 * r))
    sh = skia.GradientShader.MakeRadial((SUNX - 0.25 * r, SUNY - 0.2 * r), r * 1.25,
                                        [C(mixc(col, (255, 255, 255), 0.6)), C(col), C(mixc(col, (90, 20, 10), 0.45))], [0, 0.55, 1])
    c.drawCircle(SUNX, SUNY, r, skia.Paint(AntiAlias=True, Shader=sh))
    for k in range(16):
        a = k * 2.399 + 0.15 * t * (1 + k % 3)
        rr_ = r * (0.25 + 0.6 * ((k * 0.618) % 1))
        c.drawCircle(SUNX + rr_ * math.cos(a), SUNY + rr_ * math.sin(a), r * 0.16, paint(C(mixc(col, (255, 255, 230), 0.4), 40), blur=r * 0.06 + 1))
    c.drawCircle(SUNX, SUNY, r, paint(C(mixc(col, (255, 255, 255), 0.3), 120), stroke=3, blur=4))


def draw_earth_scene(c, t):
    k_ = chap(t)
    mr = 105 + 45 * clip01(t / T_D2)
    ma = 2 * math.pi * t / CHAP
    mx, my = EX + mr * math.cos(ma), EY + 0.32 * mr * math.sin(ma)
    c.drawOval(skia.Rect(EX - mr, EY - 0.32 * mr, EX + mr, EY + 0.32 * mr), paint(skia.Color(255, 255, 255, 26), stroke=1))
    if math.sin(ma) < 0:
        c.drawCircle(mx, my, 8, paint(skia.Color(190, 190, 200)))
    sprite(c, GLOW["blue"], EX, EY, 0.25 * (1 - clip01((t - 5 * CHAP) / CHAP)), 260)
    c.drawImage(earth_image(t), EX - _n / 2, EY - _n / 2)
    if math.sin(ma) >= 0:
        c.drawCircle(mx, my, 8, paint(skia.Color(200, 200, 210)))
    if k_ == 5:                                      # hydrogen escaping
        for j in range(70):
            ph = (t * 0.7 + j * 0.137) % 1
            x0 = EX + 60 + ph * 280
            y0 = EY + ((j * 37) % 130 - 65) * (1 + ph * 0.6)
            c.drawLine(x0, y0, x0 + 16, y0, paint(C((190, 170, 255), 200 * (1 - ph)), stroke=2))
    if k_ == 6:                                      # the last life: signals on the night side
        lv = ST["life"]
        i = int(np.searchsorted(lv, t, side="right"))
        for j in range(max(0, i - 3), i):
            age = t - lv[j]
            if age < 0.25:
                sprite(c, GLOW["green"], EX + 20 + (j * 17) % 30, EY - 30 + (j * 29) % 60, 1 - age / 0.25, 26)
    if k_ in (7, 8):                                 # Earth's orbit vs the Sun's edge
        orb = EX - SUNX
        c.drawArc(skia.Rect(SUNX - orb, SUNY - orb, SUNX + orb, SUNY + orb), -32, 64, False,
                  paint(C(WHITE, 120), stroke=1.6))


def draw_inside(c, t):
    u = clip01((t - T_D2) / CHAP)
    c.drawRect(VIEW, skia.Paint(Shader=skia.GradientShader.MakeRadial((SUNX, SUNY), 1100,
                                [C((255, 150, 70)), C((220, 60, 30)), C((60, 10, 8))], [0, 0.5, 1])))
    for k in range(26):
        a = k * 2.399 + 0.25 * t
        rr_ = 120 + 700 * ((k * 0.618) % 1)
        c.drawCircle(SUNX + rr_ * math.cos(a), SUNY + 0.6 * rr_ * math.sin(a), 70, paint(C((255, 210, 120), 45), blur=30))
    if t < T_D2 + 2.0:                               # Earth evaporates
        g = 1 - (t - T_D2) / 2.0
        sprite(c, GLOW["white"], EX, EY, g, 160 * (1 + 2 * (1 - g)))
        for j in range(40):
            ang = j * 2.399
            d_ = (t - T_D2) * (60 + 40 * ((j * 0.37) % 1))
            c.drawCircle(EX + d_ * math.cos(ang), EY + d_ * math.sin(ang), 3, paint(C((255, 230, 180), 255 * g)))
    c.drawRect(VIEW, paint(skia.Color(0, 0, 0, int(200 * clip01((t - (T_WD - 1.2)) / 1.2)))))


def draw_dwarf(c, t):
    age = t - T_WD
    for k, col in enumerate(((80, 220, 255), (255, 80, 170), (255, 176, 60), (140, 120, 255))):
        r = (140 + 75 * k) * (1 + 0.05 * age)
        c.drawOval(skia.Rect(540 - r, 744 - 0.62 * r, 540 + r, 744 + 0.62 * r), paint(C(col, 90), stroke=16 - 2 * k, blur=14))
    sprite(c, GLOW["blue"], 540, 744, 0.9, 420)
    c.drawCircle(540, 744, ER, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial(
        (520, 724), ER * 1.3, [C((255, 255, 255)), C((200, 225, 255)), C((120, 150, 230))], [0, 0.6, 1])))
    eff = skia.DashPathEffect.Make([8, 6], 0)
    p = paint(C(WHITE, 150), stroke=2)
    p.setPathEffect(eff)
    c.drawCircle(820, 744, ER, p)
    f = kit.font("monom", 14)
    for s_, y in (("EARTH", 744 + ER + 22), ("(FOR SCALE)", 744 + ER + 40)):
        c.drawString(s_, 820 - f.measureText(s_) / 2, y, f, paint(skia.Color(255, 255, 255, 150)))


def make_view_bg():
    s_ = skia.Surface(W, H)
    c = s_.getCanvas()
    c.clear(skia.Color(0, 0, 0, 0))
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(VIEW, 22, 22), True)
    c.drawRect(VIEW, skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, VY0), (0, VY1)], [skia.Color(6, 7, 18), skia.Color(14, 10, 26)])))
    r = np.random.default_rng(3)
    for _ in range(260):
        x, y, s = r.uniform(VX0, VX1), r.uniform(VY0, VY1), r.uniform(0.5, 1.8)
        c.drawCircle(x, y, s, paint(skia.Color(255, 255, 255, int(r.uniform(40, 200)))))
    c.restore()
    return s_.makeImageSnapshot()


def make_background():
    s_ = skia.Surface(W, H)
    c = s_.getCanvas()
    c.clear(skia.Color(6, 6, 14))
    c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=skia.GradientShader.MakeRadial(
        (540, 900), 1200, [skia.Color(22, 16, 36), skia.Color(6, 6, 14)])))
    g = paint(skia.Color(255, 255, 255, 7), stroke=1)
    for x in range(0, W + 1, 46):
        c.drawLine(x, 0, x, H, g)
    for y in range(0, H + 1, 46):
        c.drawLine(0, y, W, y, g)
    return s_.makeImageSnapshot()


def setup_video():
    global ST, BG, VIEW_BG
    d = np.load(os.path.join(OUT, "stems.npz"))
    ST = {k: d[k] for k in d.files}
    make_textures()
    BG, VIEW_BG = make_background(), make_view_bg()


SEC_COL = [(255, 214, 90), (255, 160, 70), (255, 214, 90), (90, 220, 120), (70, 170, 255), (180, 140, 255), (120, 255, 200),
           (255, 120, 60), (255, 70, 90), (200, 220, 255), (200, 220, 255)]


def section_colour(t):
    return SEC_COL[chap(t)]


def draw_view(c, t):
    c.drawImage(VIEW_BG, 0, 0)
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(VIEW, 22, 22), True)
    if t < T_D2:
        draw_sun(c, t)
        draw_earth_scene(c, t)
    elif t < T_WD:
        draw_inside(c, t)
    else:
        draw_dwarf(c, t)
        if t < T_WD + 0.6:
            c.drawRect(VIEW, paint(skia.Color(255, 255, 255, int(200 * (1 - (t - T_WD) / 0.6)))))
    if in_gap(t):
        c.drawRect(VIEW, paint(skia.Color(0, 0, 0, 150)))
    c.drawRoundRect(skia.Rect(VX0 + 8, VY0 + 8, VX0 + 340, VY0 + 72), 10, 10, paint(skia.Color(0, 0, 0, 120)))
    c.drawRoundRect(skia.Rect(VX1 - 420, VY0 + 8, VX1 - 8, VY0 + 58), 10, 10, paint(skia.Color(0, 0, 0, 120)))
    f, fb = kit.font("monom", 14), kit.font("mono", 30)
    c.drawString("YEARS FROM NOW", VX0 + 18, VY0 + 26, f, paint(skia.Color(255, 255, 255, 150)))
    c.drawString(f"{years(t):,.0f}", VX0 + 18, VY0 + 60, fb, paint(C(section_colour(t))))
    lab = f"EARTH: {T_D2 - t:4.1f} s LEFT" if t < T_D2 else "EARTH: GONE"
    colr = RED if t > T_D2 - 10 else WHITE
    c.drawString(lab, VX1 - 18 - fb.measureText(lab), VY0 + 44, fb, paint(C(colr)))
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(VIEW, 22, 22), paint(C(section_colour(t), 120), stroke=2))


def scope_fn(k, t):
    u = (t % CHAP) / CHAP
    if k == 0:
        return lambda x: 0.8 * np.sign(np.sin(2 * np.pi * x))
    if k == 1:
        return lambda x: (2 * (x % 1) - 1) * (0.4 + 0.5 * u)
    if k == 2:
        return lambda x: 0.9 * np.exp(-(x % 1) * (8 - 5 * u)) * np.cos(6 * np.pi * (x % 1))
    if k == 3:
        return lambda x: 0.9 * (1 - u) * np.sin(2 * np.pi * (3.0 - 2.0 * u) * x)
    if k == 4:
        return lambda x: 0.9 * np.exp(-(x % 0.25) * 14) * np.sin(2 * np.pi * 16 * np.exp(3 * (x % 0.25)) * (x % 0.25))
    if k == 5:
        return lambda x: 0.9 * np.sin(36 * np.pi * (x % 1) ** 2) * (1 - (x % 1))
    if k == 6:
        return lambda x: 0.9 * np.exp(-(x % 0.5) * 20) * np.sin(24 * np.pi * x) * math.exp(-2.5 * u)
    if k == 7:
        dk = (8, 4, 2, 1)[min(3, int(u * 4))] / 4
        return lambda x: 0.45 * (np.sin(12 * np.pi * x) + np.sin(2 * np.pi * (6 - dk) * x))
    if k == 8:
        return lambda x: np.clip(2.2 * np.sin(12 * np.pi * x), -0.9, 0.9)
    return lambda x: 0.9 * np.exp(-(x % 1) * 6) * np.sin(20 * np.pi * x)


def draw_scope(c, t):
    x0, y0, x1, y1 = 60, 1012, 1020, 1222
    k = chap(t)
    col = LCOL[CH_LAYER[k]]
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 16, 16)
    c.drawRRect(rr, paint(skia.Color(6, 10, 14, 240)))
    c.drawRRect(rr, paint(C(col, 120), stroke=1.6))
    f = kit.font("monom", 14)
    c.drawString(f"LAYER {CH_LAYER[k] + 1}/8 · {LAYER[CH_LAYER[k]]}", x0 + 14, y0 + 22, f, paint(C(col, 230)))
    c.drawString(SCOPE_TXT[k], x1 - 14 - f.measureText(SCOPE_TXT[k]), y0 + 22, f, paint(skia.Color(255, 255, 255, 170)))
    gx0, gx1, gy0, gy1 = x0 + 14, x1 - 14, y0 + 36, y1 - 12
    ym = (gy0 + gy1) / 2
    for j in range(1, 8):
        xx = gx0 + (gx1 - gx0) * j / 8
        c.drawLine(xx, gy0, xx, gy1, paint(skia.Color(120, 255, 160, 18), stroke=1))
    c.drawLine(gx0, ym, gx1, ym, paint(skia.Color(120, 255, 160, 40), stroke=1))
    fn = scope_fn(k, t)
    xb = t / BEAT
    xs = np.linspace(xb - 2.0, xb, 480)
    ys = fn(xs) * (0.0 if in_gap(t) else 1.0)
    p = skia.Path()
    for j in range(480):
        (p.moveTo if j == 0 else p.lineTo)(gx0 + (gx1 - gx0) * j / 479, ym - (gy1 - gy0) / 2 * float(ys[j]))
    c.drawPath(p, paint(C(col, 160), stroke=5, blur=5, plus=True))
    c.drawPath(p, paint(C(col), stroke=2))


TAPE = [
    (r"y = \mathrm{sgn}(\sin 2\pi t/T_{\mathrm{day}})", "day, night, day: every kick is one day"),
    (r"L(\tau) = L_{\odot}/(1 - 0.4\,\tau/t_{\odot})", "a brighter Sun opens the rumble filter"),
    (r"\Delta T_{\mathrm{day}} \approx +2\ \mathrm{ms\ per\ century}", "the Moon brakes Earth: each kick rings longer"),
    (r"\mathrm{CO_2}(\tau) \to 150\ \mathrm{ppm}", "the acid line falls with the CO2, then silence"),
    (r"f(t) = f_0\,e^{\,t/\tau}", "one rising bubble per hit: more heat, more bubbles"),
    (r"v_{\mathrm{esc}} = \sqrt{2GM/r} = 11.2\ \mathrm{km/s}", "each sweep climbs and fades: hydrogen escaping"),
    (r"N(t) = N_0\,e^{-\lambda t}", "the last microbes fade, blip by blip"),
    (r"R_{\odot}(\tau) \to 1\ \mathrm{AU}:\ \ |f_E - f_S| \to 0", "two tones close in: the wobble slows down"),
    (r"f_E = f_S", "two tones become one"),
    (r"\rho_{\mathrm{WD}} \approx 10^9\ \mathrm{kg/m^3}", "a white dwarf: one cold ping"),
    (r"\rho_{\mathrm{WD}} \approx 10^9\ \mathrm{kg/m^3}", "which layer did you hear first?"),
]


def draw_tape(c, t):
    e = TAPE[chap(t)]
    x0, y0, x1, y1 = 90, 1236, 990, 1290
    tape = skia.Path()
    tape.moveTo(x0, y0)
    for k in range(9):
        tape.lineTo(x0 + (6 if k % 2 else 0), y0 + (y1 - y0) * k / 8)
    tape.lineTo(x1, y1)
    for k in range(9):
        tape.lineTo(x1 - (6 if k % 2 else 0), y1 - (y1 - y0) * k / 8)
    tape.close()
    c.drawPath(tape, paint(skia.Color(255, 198, 96)))
    img = kit.formula(e[0], 34, (40, 26, 8))
    sc = min(1.0, (x1 - x0 - 40) / img.width(), (y1 - y0 - 6) / img.height())
    w_, h_ = img.width() * sc, img.height() * sc
    c.drawImageRect(img, skia.Rect(540 - w_ / 2, (y0 + y1) / 2 - h_ / 2, 540 + w_ / 2, (y0 + y1) / 2 + h_ / 2), SAMP, skia.Paint())
    fs = kit.font("monom", 18)
    c.drawString(e[1], 540 - fs.measureText(e[1]) / 2, 1312, fs, paint(C(section_colour(t), 235)))


def draw_mixer(c, t):
    x0, y0, x1, y1 = 60, 1326, 1020, 1600
    rr = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 20, 20)
    c.drawRRect(rr, paint(skia.Color(8, 9, 20, 235)))
    c.drawRRect(rr, paint(C(section_colour(t), 120), stroke=2))
    fi = min(int(t * 30), ST["env"].shape[1] - 1)
    cur = CH_LAYER[chap(t)]
    fl = kit.font("monom", 12)
    for k in range(8):
        sx = 80 + 76 * k
        lv = float(ST["env"][k, fi])
        nseg = 12
        for s in range(nseg):
            ys = 1536 - s * 14
            on = s < round(lv * nseg)
            colr = LCOL[k] if s < 9 else RED
            c.drawRoundRect(skia.Rect(sx, ys - 10, sx + 52, ys), 2, 2, paint(C(colr, 235 if on else 28)))
        lab = LAYER[k]
        c.drawString(lab, sx + 26 - fl.measureText(lab) / 2, 1560, fl, paint(C(LCOL[k], 240 if k == cur else 130)))
        if k == cur:
            c.drawRoundRect(skia.Rect(sx - 6, 1356, sx + 58, 1570), 6, 6, paint(C(LCOL[k], 150), stroke=1.6))
    c.drawString("8 LAYERS = 8 FORMULAS", 80, 1590, fl, paint(skia.Color(255, 255, 255, 120)))
    tau = years(t)
    rx = 700
    c.drawLine(688, y0 + 18, 688, y1 - 18, paint(skia.Color(255, 255, 255, 30), stroke=1.2))
    wd = t >= T_WD
    gone = t >= T_D2
    rows = [("SUN L  ", f"{sun_L(tau):,.2f}x" if sun_L(tau) < 100 else f"{sun_L(tau):,.0f}x", AMBER),
            ("SUN R  ", f"{sun_R(tau):,.2f}x" if not wd else "Earth-sized", (255, 140, 60)),
            ("EARTH  ", "--" if gone else f"≈ {earth_T(tau):,.0f} °C", RED),
            ("DAY    ", "--" if gone else f"≈ {24 + 6.4 * tau / 1e9:.1f} h", (255, 214, 90)),
            ("MOON   ", "--" if gone else f"{384400 + 3.8e-5 * tau:,.0f} km", WHITE),
            ("CO2    ", "--" if gone else f"{co2(tau):,.0f} ppm", (90, 220, 120)),
            ("TEMPO  ", "150 BPM", WHITE)]
    for k, (key, v, cc) in enumerate(rows):
        kit.readout(c, rx, y0 + 40 + 33 * k, key, v, cc, 1.0, 17)


CAPS = [
    (0.0, 3.2, "today: the planet's heartbeat"), (3.2, 6.4, "every kick is one day"),
    (6.4, 9.6, "the Sun gets brighter"), (9.6, 12.8, "+10% light every billion years"),
    (12.8, 16.0, "the days get longer"), (16.0, 19.2, "the Moon is braking Earth"),
    (19.2, 22.4, "the forests go quiet"), (22.4, 25.6, "below 150 ppm CO2, plants starve"),
    (25.6, 28.8, "the oceans boil"), (28.8, 32.0, "every bubble is a note"),
    (32.0, 35.2, "Earth turns into Venus"), (35.2, 38.4, "the water escapes into space"),
    (38.4, 41.6, "the last life"), (41.6, 44.8, "microbes, deep underground"),
    (44.8, 48.0, "the Sun swells"), (48.0, 51.2, "a red giant, 250x wider"),
    (51.2, 54.4, "the Sun swallows Earth"), (54.4, 57.6, "two tones become one"),
    (57.6, 60.8, "all that's left: a white dwarf"), (60.8, 64.0, "Earth-sized, 1 ton per cm³"),
    (64.0, 99.0, "which layer did you hear first?"),
]


def caption(c, t):
    for t0, t1, s_ in CAPS:
        if t0 <= t < t1:
            age = t - t0
            a = min(1.0 if t0 == 0 else min(1.0, age / 0.1), (t1 - t) / 0.1)
            sc = 1.0 if t0 == 0 else 0.9 + 0.1 * ease(min(1.0, age / 0.15))
            f = fit(TF_SEMI, 40, s_, 900)
            w = f.measureText(s_) + 56
            c.save()
            c.translate(540, CAP_Y)
            c.scale(sc, sc)
            rr = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -36, w / 2, 36), 36, 36)
            c.drawRRect(rr, paint(C((10, 12, 28), 215 * a)))
            c.drawRRect(rr, paint(C(section_colour(t), 220 * a), stroke=2.5))
            text_c(c, s_, 0, 14, f, C((255, 255, 255), 255 * a))
            c.restore()


def co(c, t, t0, t1, anchor, lab, text, color, size=17):
    if t < t0 - 0.05 or t > t1 + 0.3:
        return
    w = kit.font("mono", size).measureText(text) + 20
    lx, ly = lab
    lx = min(lx, VX1 - 10 - w) if lx > anchor[0] else max(lx, VX0 + 10 + w)
    kit.callout(c, t, t0, t1, anchor, (lx, ly), text, color, size)


def overlays(c, t):
    co(c, t, 0.5, 3.0, (EX + 40, EY - 52), (700, 560), "EARTH: 1 KICK = 1 DAY", (120, 200, 255))
    co(c, t, 3.4, 6.0, (SUNX + 40, SUNY - 30), (330, 900), "THE SUN, 4.6 BILLION YEARS OLD", AMBER)
    mr = 105 + 45 * clip01(13.0 / T_D2)
    co(c, t, 13.2, 15.8, (EX + mr * math.cos(2 * math.pi * t / CHAP), EY + 0.32 * mr * math.sin(2 * math.pi * t / CHAP)),
       (640, 950), "THE MOON DRIFTS AWAY: 3.8 cm/YEAR", WHITE)
    co(c, t, 33.0, 35.6, (EX + 160, EY), (700, 600), "HYDROGEN ESCAPING TO SPACE", (190, 170, 255))
    if T_B2 <= t < T_D2:
        r, _ = sun_state(t)
        co(c, t, 45.6, 48.2, (SUNX + r * 0.94, SUNY - r * 0.34), (640, 560), "THE SUN'S EDGE", (255, 140, 60))
    co(c, t, 58.4, 61.0, (540 + ER * 0.7, 744 - ER * 0.7), (700, 560), "WHITE DWARF: 1 TON PER cm³", CYAN)


def draw_frame(c, t):
    c.drawImage(BG, 0, 0)
    sx = sy = 0.0
    for ts, g in ((T_D1, 1.0), (T_D2, 1.7), (T_WD, 0.8)):
        if 0 <= t - ts < 0.5:
            dd = (1 - (t - ts) / 0.5) ** 2 * 14 * g
            sx += dd * math.sin(97 * t)
            sy += dd * math.cos(71 * t)
    if T_B2 <= t < T_D2:
        tr = 3.0 * ((t - T_B2) / (T_D2 - T_B2)) ** 2
        sx += tr * math.sin(131 * t)
        sy += tr * math.cos(117 * t)
    c.save()
    c.translate(sx, sy)
    draw_view(c, t)
    draw_scope(c, t)
    draw_tape(c, t)
    draw_mixer(c, t)
    c.restore()
    if not NO_FLASH:
        for ts, col in ((T_D1, (120, 180, 255)), (T_D2, (255, 200, 150))):
            if 0 <= t - ts < 0.5:
                c.drawRect(skia.Rect(0, 0, W, H), paint(C(col, int(130 * math.exp(-(t - ts) / 0.15))), plus=True))
    overlays(c, t)
    text_c(c, TITLE1, 540, TITLE_Y[0], F_T1, skia.Color(255, 255, 255), glow=C((255, 120, 60), 150))
    text_c(c, TITLE2, 540, TITLE_Y[1], F_T2, C(AMBER), glow=C(AMBER, 150))
    caption(c, t)


def new_surface():
    buf = np.zeros((H, W, 4), dtype=np.uint8)
    return buf, skia.Surface(buf, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)


def check_formulas():
    bad = 0
    for tex in [e[0] for e in TAPE]:
        try:
            kit.formula(tex, 34, (40, 26, 8))
        except Exception as e:  # noqa: BLE001
            bad += 1
            print("BAD FORMULA:", tex, "->", str(e)[:100])
    if bad:
        raise SystemExit(f"{bad} formulas failed")
    print("formulas ok")


def preview(times):
    setup_video()
    for t in times:
        buf, s_ = new_surface()
        draw_frame(s_.getCanvas(), t)
        s_.makeImageSnapshot().save(os.path.join(OUT, f"pv_{t:05.2f}.png"), skia.kPNG)


def render(audio, out):
    setup_video()
    buf, s_ = new_surface()
    c = s_.getCanvas()
    proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                             "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                             "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "256k",
                             "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    frames = int(round(DUR * FPS))
    t0 = time.time()
    for fr in range(frames):
        draw_frame(c, fr / FPS)
        proc.stdin.write(buf.tobytes())
        if fr % 600 == 0:
            print(f"frame {fr}/{frames} {time.time() - t0:.0f}s", flush=True)
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise SystemExit(f"ffmpeg failed with {rc}")
    print("done", out, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode in ("audio", "full"):
        make_audio(os.path.join(OUT, "audio_raw.wav"))
        loudnorm(os.path.join(OUT, "audio_raw.wav"), os.path.join(OUT, "audio.wav"), -8.0)
    if mode in ("preview", "full", "check", "video"):
        check_formulas()
    if mode == "preview":
        preview([float(x) for x in sys.argv[2:]] or [0.5, 8.0, 15.0, 22.0, 27.0, 35.0, 41.0, 48.5, 52.0, 60.0])
    if mode in ("full", "video"):
        render(os.path.join(OUT, "audio.wav"), os.path.join(OUT, "12_video.mp4"))

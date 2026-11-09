"""Erzeugt Hintergrundmusik + Soundeffekte (alles synthetisch, lizenzfrei) und mischt sie mit der Stimme.

Aufruf:  python3 audio.py
Eingabe: build/timeline.json, build/vo.wav
Ausgabe: build/music.wav, build/sfx.wav, build/mix.wav
"""
import json
import os
import subprocess
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
SR = 44100
rs = np.random.RandomState(1234)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def att(t, a=0.003):
    return np.minimum(1.0, t / a)


def sweep(f0, f1, dur):
    t = tt(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR), t


def onepole_lp(x, cutoff):
    """Tiefpass mit (optional zeitvariabler) Grenzfrequenz."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def hp(x):
    return np.concatenate([[0], np.diff(x)])


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ------------------------------------------------------------------ Klangbausteine
def marimba(f, dur=0.7, amp=0.3):
    t = tt(dur)
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t * 6.5)
         + 0.32 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 20)
         + 0.1 * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * 45))
    return y * att(t) * amp


def bass(f, dur=0.5, amp=0.25):
    t = tt(dur)
    y = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) + 0.2 * np.sin(6 * np.pi * f * t)
    return y * np.exp(-t * 4.5) * att(t, 0.006) * amp


def kick(amp=0.55):
    y, t = sweep(160, 48, 0.16)
    return y * np.exp(-t * 20) * amp


def clap(amp=0.16):
    t = tt(0.18)
    n = hp(rs.randn(len(t)))
    env = np.exp(-t * 30) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 45) * (t > 0.012)
    return n * env * amp


def shaker(amp=0.05):
    t = tt(0.07)
    return hp(hp(rs.randn(len(t)))) * np.exp(-t * 70) * att(t, 0.004) * amp


def bell(f, dur=1.0, amp=0.3, partials=((1, 1, 3), (2.0, 0.5, 5), (3.01, 0.3, 8), (4.2, 0.2, 12))):
    t = tt(dur)
    y = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in partials)
    return y * att(t, 0.002) * amp


# ------------------------------------------------------------------ Soundeffekte
def sfx_pop():
    y, t = sweep(320, 980, 0.09)
    return y * np.exp(-t * 38) * att(t, 0.002) * 0.42


def sfx_whoosh():
    t = tt(0.42)
    p = t / t[-1]
    cut = 300 + 4200 * np.sin(np.pi * p) ** 2
    y = onepole_lp(rs.randn(len(t)), cut)
    return y * np.sin(np.pi * p) ** 1.5 * 0.55


def sfx_ding():
    return np.concatenate([bell(1318.5, 0.12, 0.22)[: int(0.09 * SR)], bell(1760, 0.9, 0.28)])


def sfx_title():
    y = sum(marimba(midi(m), 1.4, 0.22) for m in (65, 69, 72, 77))
    t = tt(1.4)
    cym = hp(rs.randn(len(t))) * np.exp(-t * 6) * 0.06
    return y + cym + np.pad(kick(0.6), (0, len(t) - len(kick())))


def sfx_stamp():
    t = tt(0.4)
    thump = np.sin(2 * np.pi * 65 * t) * np.exp(-t * 16) * 0.9
    n = onepole_lp(rs.randn(len(t)), 1800) * np.exp(-t * 28) * 0.8
    return (thump + n) * att(t, 0.001)


def sfx_confetti():
    t = tt(0.9)
    burst = hp(rs.randn(len(t))) * np.exp(-t * 25) * 0.25
    y = burst.copy()
    for i in range(12):
        f = 2000 + rs.rand() * 3000
        st = int((0.05 + rs.rand() * 0.6) * SR)
        b = bell(f, 0.25, 0.05 + rs.rand() * 0.04)
        y[st: st + len(b)] += b[: len(y) - st]
    return y


def sfx_sparkle():
    y = np.zeros(int(1.0 * SR))
    for i, f in enumerate([1975, 2349, 2637, 3136, 3520, 3951]):
        b = bell(f, 0.4, 0.08)
        st = int(i * 0.07 * SR)
        y[st: st + len(b)] += b[: len(y) - st]
    return y


def sfx_splash():
    t = tt(0.9)
    n = onepole_lp(rs.randn(len(t)), 900 + 2000 * np.exp(-t * 4)) * (1 - np.exp(-t * 60)) * np.exp(-t * 4) * 0.9
    for i in range(6):
        c, tc = sweep(400 + rs.rand() * 300, 1200 + rs.rand() * 600, 0.05)
        st = int((0.1 + rs.rand() * 0.5) * SR)
        n[st: st + len(c)] += c * np.exp(-tc * 40) * 0.12
    return n


def sfx_waves():
    t = tt(1.6)
    n = onepole_lp(rs.randn(len(t)), 700)
    return n * np.sin(np.pi * t / t[-1]) ** 2 * 0.7


def sfx_flap():
    y = np.zeros(int(0.6 * SR))
    for i in range(5):
        t = tt(0.07)
        b = onepole_lp(rs.randn(len(t)), 1200) * np.sin(np.pi * t / t[-1]) * 0.5
        st = int(i * 0.1 * SR)
        y[st: st + len(b)] += b
    return y


def squawk_call(dur=0.26, f0=1500, f1=880):
    t = tt(dur)
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.04 * np.sin(2 * np.pi * 28 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.tanh(3.5 * np.sin(ph)) + 0.4 * np.sin(2 * ph)
    y = onepole_lp(y, 3500)
    env = np.sin(np.pi * np.minimum(1, t / dur)) ** 0.6
    return y * env * 0.32


def sfx_squawk():
    a = squawk_call(0.24, 1600, 950)
    b = squawk_call(0.3, 1500, 820)
    return np.concatenate([a, np.zeros(int(0.06 * SR)), b])


def sfx_gulp():
    y, t = sweep(420, 110, 0.14)
    return y * np.exp(-t * 18) * 0.5


def sfx_poof():
    t = tt(0.5)
    n = onepole_lp(rs.randn(len(t)), 2500 * np.exp(-t * 6) + 200) * (1 - np.exp(-t * 200)) * np.exp(-t * 7) * 0.8
    return n


def sfx_riser():
    t = tt(0.9)
    s, _ = sweep(250, 1400, 0.9)
    n = onepole_lp(rs.randn(len(t)), 500 + 5000 * (t / t[-1]) ** 2)
    env = (t / t[-1]) ** 2
    return (s * 0.12 + n * 0.35) * env


def sfx_pins():
    y = np.zeros(int(1.6 * SR))
    for i in range(10):
        f = midi(72 + [0, 4, 7, 12, 4, 7, 12, 16, 12, 19][i])
        b = marimba(f, 0.4, 0.13)
        st = int(i * 0.11 * SR)
        y[st: st + len(b)] += b
    return y


def sfx_horn():
    t = tt(1.0)
    y = sum(np.sin(2 * np.pi * 110 * k * t * (1 + 0.002 * k)) / k for k in range(1, 8))
    y += sum(np.sin(2 * np.pi * 138.6 * k * t) / k for k in range(1, 6)) * 0.6
    y = onepole_lp(y, 900)
    env = np.minimum(1, t / 0.08) * np.minimum(1, (t[-1] - t) / 0.2)
    return y * env * 0.16


def sfx_squeak():
    t = tt(0.24)
    p = t / t[-1]
    f = 1500 + 900 * np.sin(np.pi * p) - 200 * p
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    return y * np.sin(np.pi * p) ** 0.5 * 0.3


def sfx_tap():
    t = tt(0.05)
    return (hp(rs.randn(len(t))) * 0.5 + np.sin(2 * np.pi * 1800 * t)) * np.exp(-t * 120) * 0.35


def sfx_blip():
    a = bell(880, 0.08, 0.2)[: int(0.07 * SR)]
    b = bell(1320, 0.35, 0.22)
    return np.concatenate([a, b])


def sfx_tick():
    t = tt(0.04)
    return (np.sin(2 * np.pi * 3200 * t) + hp(rs.randn(len(t))) * 0.6) * np.exp(-t * 160) * 0.35


def sfx_card():
    t = tt(0.2)
    sw = hp(rs.randn(len(t))) * np.sin(np.pi * t / t[-1]) * 0.12
    p = sfx_pop()
    y = np.zeros(max(len(t), len(p)))
    y[: len(t)] += sw
    y[: len(p)] += p
    return y


def sfx_kaching():
    y = np.zeros(int(1.3 * SR))
    d = sfx_stamp() * 0.35
    y[: len(d)] += d
    for f, st in [(2637, 0.04), (3520, 0.13)]:
        b = bell(f, 1.0, 0.22)
        i = int(st * SR)
        y[i: i + len(b)] += b[: len(y) - i]
    for i in range(28):
        f = 3000 + rs.rand() * 4000
        st = int((0.05 + rs.rand() * 0.45) * SR)
        b = bell(f, 0.06, 0.05)
        y[st: st + len(b)] += b
    return y


def sfx_hearts():
    y = np.zeros(int(0.9 * SR))
    for i in range(6):
        p = sfx_pop() * (0.4 + rs.rand() * 0.3)
        st = int(i * 0.12 * SR)
        y[st: st + len(p)] += p
    return y


SFX = {name[4:]: fn for name, fn in globals().items() if name.startswith("sfx_")}
SFX_GAIN = {"whoosh": 0.55, "waves": 0.9, "horn": 1.0, "confetti": 0.8}


# ------------------------------------------------------------------ Musik
def music(duration):
    bpm = 118
    beat = 60 / bpm
    bar = beat * 4
    n = int((duration + 2) * SR)
    L = np.zeros(n)
    R = np.zeros(n)

    def add(sig, t, pan=0.0, gain=1.0):
        i = int(t * SR)
        if i >= n:
            return
        sig = sig[: n - i] * gain
        L[i: i + len(sig)] += sig * (1 - pan) * 0.5 * 2 ** 0.5
        R[i: i + len(sig)] += sig * (1 + pan) * 0.5 * 2 ** 0.5

    chords = [[65, 69, 72, 77], [64, 67, 72, 76], [62, 65, 69, 74], [62, 65, 70, 74]]
    roots = [41, 48, 50, 46]
    arp = [0, 1, 2, 3, 2, 1, 2, 0]
    end_t = duration - 1.5
    nbars = int(np.ceil(end_t / bar))
    for b in range(nbars):
        t0 = b * bar
        ci = b % 4
        for k, idx in enumerate(arp):
            t = t0 + k * beat / 2
            if t >= end_t:
                break
            acc = 1.0 if k % 2 == 0 else 0.75
            add(marimba(midi(chords[ci][idx]), 0.6, 0.15 * acc), t, pan=0.25)
        if b == 0:
            continue
        for k in range(4):
            t = t0 + k * beat
            if t >= end_t:
                break
            if k in (0, 2):
                add(kick(), t)
                add(bass(midi(roots[ci]), 0.45, 0.24), t)
            else:
                add(clap(), t, pan=-0.1)
            add(shaker(0.035), t, pan=-0.4)
            add(shaker(0.05), t + beat / 2, pan=-0.4)
        add(bass(midi(roots[ci] + 12), 0.25, 0.12), t0 + 3.5 * beat)
    # Schlussakkord
    tend = nbars * bar
    for m in (53, 65, 69, 72, 77):
        add(marimba(midi(m), 1.8, 0.16), tend, pan=0.1)
    add(kick(0.5), tend)
    out = np.stack([L, R], axis=1)[: int(duration * SR)]
    fade = int(0.6 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return out


def ambience(duration):
    t = tt(duration)
    n = onepole_lp(rs.randn(len(t)), 500)
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * t / 5.5) ** 2
    return n * swell * 0.06


def write_wav(path, data):
    data = np.clip(data, -1, 1)
    if data.ndim == 1:
        data = data[:, None]
    with wave.open(path, "wb") as w:
        w.setnchannels(data.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((data * 32767).astype(np.int16).tobytes())


def main():
    tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
    dur = tl["duration"]

    mus = music(dur)
    amb = ambience(dur)
    mus[:, 0] += amb
    mus[:, 1] += amb
    mus /= np.max(np.abs(mus)) + 1e-9
    write_wav(os.path.join(BUILD, "music.wav"), mus * 0.8)

    fx = np.zeros(int((dur + 2) * SR))
    for seg in tl["segments"]:
        for name, t in seg["sfx"]:
            sig = SFX[name]() * SFX_GAIN.get(name, 1.0)
            i = max(0, int(t * SR))
            fx[i: i + len(sig)] += sig[: len(fx) - i]
    fx = fx[: int(dur * SR)]
    fx /= np.max(np.abs(fx)) + 1e-9
    write_wav(os.path.join(BUILD, "sfx.wav"), fx * 0.85)

    graph = (
        "[0:a]aresample=44100,aformat=channel_layouts=stereo,highpass=f=70,"
        "equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-22dB:ratio=3:attack=4:release=90:makeup=2,asplit=2[vo][key];"
        "[1:a]aformat=channel_layouts=stereo,volume=0.55[m];"
        "[m][key]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=320[mus];"
        "[2:a]aformat=channel_layouts=stereo,volume=0.5[fx];"
        "[vo][mus][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[out]"
    )
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(BUILD, "vo.wav"), "-i", os.path.join(BUILD, "music.wav"),
                    "-i", os.path.join(BUILD, "sfx.wav"), "-filter_complex", graph, "-map", "[out]", "-t", str(dur),
                    os.path.join(BUILD, "mix.wav")], check=True)
    print("Audio fertig:", os.path.join(BUILD, "mix.wav"))


if __name__ == "__main__":
    main()

"""Kommentator-Stimme für die Simulation: Sätze aus den Ereignissen des Rennens, Qwen3-TTS-Klon, Ton darunter leiser.

Aufruf (mit der Qwen-Umgebung):
  HF_HUB_OFFLINE=1 QA_WHISPER=<whisper> <qw>/bin/python sim-bundeslaender-test/kommentar.py <seed> <Qwen3-TTS-Base>
Erwartet voice/kommentator.wav + .txt. Schreibt build/mix.wav (mit Stimme), build/voice.js (Untertitel), timeline.json.
Sätze werden nach Text zwischengespeichert (voice_cache/), nur neue Sätze kosten Rechenzeit.
"""
import hashlib
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import sim  # noqa: E402

BIG = {"BY", "NRW", "BW", "NI"}
GAP = 0.18  # Pause zwischen zwei Sätzen


def names(idx):
    return [sim.STATES[i][1] for i in idx]


def join(ns):
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " und " + ns[-1]


def art(name):
    return "das Saarland" if name == "Saarland" else name


def plan(res, dur_of):
    """Wenige Ansagen, nur an den wichtigen Stellen (Kanalinhaber 17.11.: „labert permanent“):
    Start, eine Überraschung (großes Land fliegt früh), nur noch drei, Finale, Sieger, Aufruf. Mindestens 3 s Ruhe dazwischen."""
    elim = res["elim"]
    n = len(sim.STATES)
    lines = [(0.05, "Sechzehn Bundesländer. Nur eins überlebt!")]
    free = 0.05 + dur_of(lines[0][1]) + 3.0
    surprise = False
    for k, (t_ev, i) in enumerate(elim):
        left = n - (k + 1)
        ab, name = sim.STATES[i][0], sim.STATES[i][1]
        txt = None
        if left == 2:
            a, b = [j for j in range(n) if j not in [x for _, x in elim[:k + 1]]]
            txt = f"Finale! {sim.STATES[a][1]} gegen {art(sim.STATES[b][1])}!"
        elif left == 3:
            txt = "Nur noch drei!"
        elif not surprise and ab in BIG and left >= 5:
            txt = f"{name} ist raus! Damit hat keiner gerechnet!"
        if not txt or left < 2:
            continue
        start = t_ev + 0.12
        nxt_important = left == 3  # „Nur noch drei“ darf das Finale nicht blockieren
        if start < free and not (left == 2):
            continue
        start = max(start, lines[-1][0] + dur_of(lines[-1][1]) + GAP)
        lines.append((start, txt))
        surprise = surprise or "gerechnet" in txt
        free = start + dur_of(txt) + (0.3 if nxt_important else 3.0)
    w = res["winner"]
    start = max(lines[-1][0] + dur_of(lines[-1][1]) + GAP, res["t_win"] + 0.35)
    lines.append((start, f"{art(sim.STATES[w][1])[0].upper() + art(sim.STATES[w][1])[1:]} gewinnt! Wahnsinn!"))
    free = start + dur_of(lines[-1][1]) + 0.35
    lines.append((free, "Revanche morgen? Schreib dein Bundesland in die Kommentare!"))
    return lines


def main():
    seed, model = int(sys.argv[1]), sys.argv[2]
    import qwen3_engine as Q
    import voxcpm_tts as V
    import soundfile as sf
    ref = os.path.join(HERE, "voice", "kommentator.wav")
    rtxt = open(ref[:-4] + ".txt", encoding="utf-8").read().strip()
    cache = os.path.join(HERE, "voice_cache")
    os.makedirs(cache, exist_ok=True)
    res = sim.simulate(seed)
    loaded = [False]
    rh = hashlib.sha1(open(ref, "rb").read()).hexdigest()[:8]

    def wav_of(text):
        key = hashlib.sha1(f"{rh}|{text}".encode()).hexdigest()[:16]
        path = os.path.join(cache, key + ".wav")
        if os.path.exists(path):
            w, sr = sf.read(path, dtype="float32")
            return w, sr
        if not loaded[0]:
            Q.load(model)
            loaded[0] = True
        sr = Q.sample_rate()
        best = None
        fr = Q.pitch_ref(ref)
        for c in range(2):
            w = np.asarray(Q.clone(text, ref, rtxt, seed=31 + c, temperature=0.7), dtype=np.float32)
            # Stille vorn/hinten weg
            a = np.where(np.abs(w) > 0.02 * np.max(np.abs(w)))[0]
            w = w[max(0, a[0] - int(0.03 * sr)): a[-1] + int(0.08 * sr)]
            hyp = V.asr(w, sr)
            e = V.wer(text, hyp)
            simv = Q.speaker_similarity(w, sr, ref)
            f = Q.pitch(w, sr)
            dev = abs(np.log2(f / fr)) if f and fr else 0.0
            score = simv - 2 * e - 1.5 * max(0.0, dev - 0.2)
            print(f"  {text} | Fassung {c+1}: WER {e:.2f} Ähnl. {simv:.3f} F0 {f or 0:.0f} | {hyp}", flush=True)
            if best is None or score > best[0]:
                best = (score, w)
        sf.write(path, best[1], sr)
        return best[1], sr

    est = lambda tx: 0.068 * len(tx) + 0.3
    lines = plan(res, est)
    for it in range(4):  # bis der Ablauf mit echten Längen stabil ist
        real = {}
        for _, tx in lines:
            w, sr = wav_of(tx)
            real[tx] = len(w) / sr
        new = plan(res, lambda tx: real[tx] if tx in real else est(tx))
        if [x[1] for x in new] == [x[1] for x in lines]:
            lines = new
            break
        lines = new
    for _, tx in lines:
        wav_of(tx)
    out = []
    for t0, tx in lines:
        w, sr = wav_of(tx)
        out.append((t0, tx, w, sr))
        print(f"{t0:6.2f}–{t0 + len(w) / sr:6.2f}  {tx}")
    end = out[-1][0] + len(out[-1][2]) / out[-1][3]
    duration = round(max(res["t_win"] + 5.0, end + 1.2), 2)
    sim.build(seed, duration)  # sim.js, timeline.json, mix.wav (Musik + Geräusche) in passender Länge
    # Stimme einmischen, Rest darunter leiser
    import audio as A
    SR = A.SR
    with wave.open(os.path.join(BUILD, "mix.wav")) as f:
        base = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32) / 32767
    vo = np.zeros_like(base)
    duck = np.ones_like(base)
    for t0, tx, w, sr in out:
        w = np.interp(np.arange(0, len(w) * SR / sr) * sr / SR, np.arange(len(w)), w).astype(np.float32)
        w = w / (np.max(np.abs(w)) + 1e-9) * 0.95
        i = int(t0 * SR)
        j = min(len(vo), i + len(w))
        vo[i:j] += w[: j - i]
        a, b = max(0, i - int(0.08 * SR)), min(len(duck), j + int(0.15 * SR))
        duck[a:b] = 0.5
    # weiche Übergänge beim Leiserwerden
    k = int(0.06 * SR)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    mix = base * duck * 0.9 + vo
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.9
    with wave.open(os.path.join(BUILD, "mix.wav"), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((mix * 32767).astype("<i2").tobytes())
    caps = [[round(t0, 3), round(t0 + len(w) / sr, 3), tx] for t0, tx, w, sr in out]
    with open(os.path.join(BUILD, "voice.js"), "w", encoding="utf-8") as f:
        f.write("window.VOICE = " + json.dumps(caps, ensure_ascii=False) + ";\n")
    print(f"Video {duration}s, {len(out)} Sätze")


if __name__ == "__main__":
    main()

"""Erzeugt die Sprachaufnahme (Piper TTS) pro Satz und daraus die Timeline.

Aufruf:  python3 build_timeline.py <pfad/zu/de_DE-thorsten-high.onnx>
Ausgabe: build/vo.wav, build/timeline.json, build/timeline.js
"""
import json
import os
import sys
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
FPS = 30


def synth(voice, text, length_scale):
    cfg = SynthesisConfig(length_scale=length_scale, noise_scale=0.6, noise_w_scale=0.75)
    chunks = list(voice.synthesize(text, syn_config=cfg))
    sr = chunks[0].sample_rate
    audio = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
    return audio, sr


def trim(audio, sr, thresh_db=-42.0, pad=0.03):
    win = int(sr * 0.01)
    n = len(audio) // win
    rms = np.sqrt(np.mean(audio[: n * win].reshape(n, win) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms / (np.max(rms) + 1e-12))
    idx = np.where(db > thresh_db)[0]
    if len(idx) == 0:
        return audio
    a = max(0, idx[0] * win - int(pad * sr))
    b = min(len(audio), (idx[-1] + 1) * win + int(pad * sr))
    return audio[a:b]


def caption_chunks(caps, start, dur):
    weights = [len(c.replace("^", "").replace("!", "").replace("~", "")) + 3 for c in caps]
    total = sum(weights)
    out, t = [], start
    for c, w in zip(caps, weights):
        d = dur * w / total
        words = []
        for raw in c.split(" "):
            style = "w"
            if raw.startswith("^"):
                style, raw = "g", raw[1:]
            elif raw.startswith("!"):
                style, raw = "r", raw[1:]
            elif raw.startswith("~"):
                style, raw = "y", raw[1:]
            words.append([raw, style])
        out.append({"start": round(t, 3), "words": words})
        t += d
    return out


def main():
    model = sys.argv[1]
    os.makedirs(BUILD, exist_ok=True)
    script = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
    voice = PiperVoice.load(model)

    sr = None
    pieces = []
    t = script["lead_in"]
    segs = []
    for i, s in enumerate(script["segments"]):
        gap = s.get("gap", script["default_gap"]) if i > 0 else 0.0
        t += gap
        audio, sr = synth(voice, s["say"], script["length_scale"])
        audio = trim(audio, sr)
        dur = len(audio) / sr
        pieces.append((t, audio))
        segs.append({
            "id": s["id"],
            "say": s["say"],
            "start": round(t, 3),
            "speechEnd": round(t + dur, 3),
            "caps": caption_chunks(s["caps"], t, dur),
            "sfx": [[name, round(t + off, 3)] for name, off in s.get("sfx", [])],
        })
        t += dur

    total = t + script["tail"]
    for i, s in enumerate(segs):
        s["end"] = segs[i + 1]["start"] if i + 1 < len(segs) else round(total, 3)

    vo = np.zeros(int(total * sr) + sr, dtype=np.float32)
    for start, audio in pieces:
        a = int(start * sr)
        vo[a : a + len(audio)] += audio
    vo = vo[: int(total * sr)]
    peak = np.max(np.abs(vo)) + 1e-9
    vo = vo / peak * 0.9

    with wave.open(os.path.join(BUILD, "vo.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((vo * 32767).astype(np.int16).tobytes())

    # Lautstärke-Hüllkurve pro Videoframe für die Mundbewegung
    nframes = int(np.ceil(total * FPS))
    env = []
    hop = sr / FPS
    for f in range(nframes):
        a = int(f * hop)
        b = int(a + hop)
        seg = vo[a:b]
        env.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
    env = np.array(env)
    env = env / (np.percentile(env[env > 0.01], 90) if np.any(env > 0.01) else 1.0)
    env = np.clip(env, 0, 1)

    tl = {"fps": FPS, "duration": round(total, 3), "segments": segs, "env": [round(x, 3) for x in env]}
    json.dump(tl, open(os.path.join(BUILD, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(BUILD, "timeline.js"), "w", encoding="utf-8") as f:
        f.write("window.TL = " + json.dumps(tl, ensure_ascii=False) + ";\n")

    print(f"Dauer: {total:.2f}s, {len(segs)} Segmente, {nframes} Frames")
    for s in segs:
        print(f"  {s['id']} {s['start']:6.2f}-{s['speechEnd']:6.2f}  {s['say']}")


if __name__ == "__main__":
    main()

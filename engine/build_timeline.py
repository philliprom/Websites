"""Erzeugt die Sprachaufnahme (Piper TTS) pro Satz und daraus die Timeline.

Aufruf:  python3 engine/build_timeline.py <projektordner> <pfad/zu/de_DE-thorsten-high.onnx>
Ausgabe: <projekt>/build/vo.wav, build/timeline.json, build/timeline.js
"""
import json
import os
import sys
import wave

import numpy as np

HERE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
FPS = 30


def synth(voice, text, length_scale):
    from piper import SynthesisConfig
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


def cache_key(text, style, ref, tts):
    import hashlib
    h = hashlib.sha1(open(ref, "rb").read()).hexdigest()[:12]
    return hashlib.sha1(f"{text}|{style}|{h}|{tts.get('cfg', 2.0)}|{tts.get('steps', 10)}".encode()).hexdigest()[:16]


def sf_read(path):
    import soundfile as sf
    a, _ = sf.read(path, dtype="float32")
    return a


def sf_write(path, a, sr):
    import soundfile as sf
    sf.write(path, a, sr, subtype="PCM_24" if path.endswith(".flac") else "FLOAT")


def build_voxcpm(script, model_dir):
    """Erzeugt ganze Sätze mit VoxCPM2 (geklonte Projektstimme), prüft sie per Whisper und
    schneidet sie über Wort-Zeitstempel in die Segmente. Gibt (sr, pieces, timing, qa) zurück."""
    import difflib
    import re as _re
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import voxcpm_tts as V
    sr = None  # wird aus dem Cache gelesen oder nach dem Laden des Modells gesetzt (Modell nur bei Bedarf laden)
    tts = script["tts"]
    ref = os.path.join(HERE, tts["voice"])
    ref_text = open(os.path.join(HERE, tts["voice_text"]), encoding="utf-8").read().strip()
    segs = script["segments"]
    groups, cur = [], []
    for i, s in enumerate(segs):
        cur.append(i)
        if _re.search(r"[.!?]$", s["say"].strip()) or i == len(segs) - 1:
            groups.append(cur)
            cur = []
    t = script["lead_in"]
    pieces, timing, qa = [], {}, []
    for gi, g in enumerate(groups):
        if gi > 0:
            t += segs[g[0]].get("gap", script["default_gap"])
        text = " ".join(segs[i]["say"] for i in g)
        style = segs[g[0]].get("style") or tts.get("style")
        best = None
        key = cache_key(text, style, ref, tts)
        # Satz-Cache liegt im Projekt (wird mit eingecheckt), alte Ablage in build/ wird weiter gelesen
        cpath = os.path.join(HERE, "tts_cache", key + ".flac")
        old = os.path.join(BUILD, "tts_cache", key + ".wav")
        if not os.path.exists(cpath) and os.path.exists(old):
            os.makedirs(os.path.dirname(cpath), exist_ok=True)
            sf_write(cpath, sf_read(old), sr)
        if os.path.exists(cpath):
            import soundfile as _sf
            wav, sr = _sf.read(cpath, dtype="float32")
            words, hyp = V.asr_words(wav, sr)
            best = (V.wer(text, hyp), wav, words, hyp)
            print(f"  Satz {gi + 1}/{len(groups)} aus Cache: WER {best[0]:.2f} | {hyp}", flush=True)
        for attempt in range(0 if best else tts.get("tries", 4)):
            if attempt == 0:
                V.load(model_dir)
                sr = V.sample_rate()
            wav = V.clone(text, ref, ref_text, seed=tts.get("seed", 7) + 1000 * gi + attempt,
                          cfg=tts.get("cfg", 2.0), steps=tts.get("steps", 10), style=style)
            wav = trim(np.asarray(wav, dtype=np.float32), sr)
            words, hyp = V.asr_words(wav, sr)
            e = V.wer(text, hyp)
            if best is None or e < best[0]:
                best = (e, wav, words, hyp)
            print(f"  Satz {gi + 1}/{len(groups)} Versuch {attempt + 1}: WER {e:.2f} | {hyp}", flush=True)
            if e <= tts.get("max_wer", 0.08):
                break
        e, wav, words, hyp = best
        if not os.path.exists(cpath):
            os.makedirs(os.path.dirname(cpath), exist_ok=True)
            sf_write(cpath, wav, sr)
        dur = len(wav) / sr
        qa.append((text, hyp, e))
        # Schnittpunkte: Wortanfang des ersten Worts jedes Folgesegments
        ref_tok, owner = [], []
        for k, i in enumerate(g):
            toks = V._norm(segs[i]["say"])
            ref_tok += toks
            owner += [k] * len(toks)
        hyp_tok, hyp_time = [], []
        for w, ws, we in words:
            for tok in V._norm(w):
                hyp_tok.append(tok)
                hyp_time.append(ws)
        sm = difflib.SequenceMatcher(a=ref_tok, b=hyp_tok, autojunk=False)
        mapping = {}
        for blk in sm.get_matching_blocks():
            for j in range(blk.size):
                mapping[blk.a + j] = blk.b + j
        starts = [0.0]
        chars = [len(segs[i]["say"]) for i in g]
        for k in range(1, len(g)):
            first = owner.index(k) if k in owner else None
            tb = None
            if first is not None:
                for ri in range(first, len(ref_tok)):
                    if owner[ri] != k:
                        break
                    if ri in mapping:
                        tb = max(0.0, hyp_time[mapping[ri]] - 0.04)
                        break
            if tb is None or tb <= starts[-1] + 0.15:
                tb = dur * sum(chars[:k]) / sum(chars)
            starts.append(min(tb, dur - 0.1))
        for k, i in enumerate(g):
            a0 = t + starts[k]
            a1 = t + (starts[k + 1] if k + 1 < len(g) else dur)
            timing[i] = (a0, a1)
        pieces.append((t, wav))
        t += dur
    return sr, pieces, timing, qa, t


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
    model = sys.argv[-1]
    os.makedirs(BUILD, exist_ok=True)
    script = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
    segs = []
    if script.get("tts", {}).get("engine") == "voxcpm":
        sr, pieces, timing, qa, t = build_voxcpm(script, model)
        for i, s in enumerate(script["segments"]):
            a0, a1 = timing[i]
            segs.append({
                "id": s["id"], "say": s["say"], "start": round(a0, 3), "speechEnd": round(a1, 3),
                "caps": caption_chunks(s["caps"], a0, a1 - a0),
                "sfx": [[name, round((a1 + float(off[1:])) if isinstance(off, str) else (a0 + off), 3)] for name, off in s.get("sfx", [])],
            })
        with open(os.path.join(BUILD, "tts_qa.txt"), "w", encoding="utf-8") as f:
            for text, hyp, e in qa:
                f.write(f"WER {e:.2f}\n  Skript:  {text}\n  Gehört:  {hyp}\n")
        voice = None
    else:
        from piper import PiperVoice
        voice = PiperVoice.load(model)
        sr = None
        pieces = []
        t = script["lead_in"]
    for i, s in enumerate(script["segments"] if voice else []):
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
            "sfx": [[name, round((t + dur + float(off[1:])) if isinstance(off, str) else (t + off), 3)] for name, off in s.get("sfx", [])],
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

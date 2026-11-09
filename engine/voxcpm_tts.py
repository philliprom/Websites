"""VoxCPM2-Stimme (Apache-2.0) für die Tag-1-Videos: Stimm-Design, Klonen und automatische Prüfung per Whisper.

Wird von build_timeline.py genutzt, wenn script.json  "tts": {"engine": "voxcpm", ...}  enthält.
Eigenständig, um Stimm-Kandidaten zu entwerfen:
  python engine/voxcpm_tts.py design <modell_ordner> <ausgabe_ordner> "<Beschreibung>" "<Beispieltext>" [anzahl]
"""
import os
import re
import sys
import time
import unicodedata

import numpy as np
import soundfile as sf

_MODEL = None
_ASR = None


def load(model_dir):
    global _MODEL
    if _MODEL is None:
        import torch
        torch.set_num_threads(os.cpu_count() or 4)
        from voxcpm import VoxCPM
        _MODEL = VoxCPM(voxcpm_model_path=model_dir, zipenhancer_model_path=None, enable_denoiser=False, optimize=False)
    return _MODEL


def sample_rate():
    return _MODEL.tts_model.sample_rate


def _seed(seed):
    import random
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def design(text, description, seed=0, cfg=2.0, steps=10):
    _seed(seed)
    return _MODEL.generate(text=f"({description}){text}", cfg_value=cfg, inference_timesteps=steps)


def clone(text, ref_wav, ref_text, seed=0, cfg=2.0, steps=10, style=None):
    _seed(seed)
    t = f"({style}){text}" if style else text
    return _MODEL.generate(text=t, prompt_wav_path=ref_wav, prompt_text=ref_text, reference_wav_path=ref_wav,
                           cfg_value=cfg, inference_timesteps=steps)


# ------------------------------------------------------------------ Qualitätsprüfung
def asr_words(audio, sr):
    """Wie asr(), liefert zusätzlich Wörter mit Zeitstempeln [(wort, start, ende), ...]."""
    global _ASR
    if _ASR is None:
        from faster_whisper import WhisperModel
        _ASR = WhisperModel(os.environ.get("QA_WHISPER", "small"), device="cpu", compute_type="int8")
    a16 = audio
    if sr != 16000:
        n = int(len(audio) * 16000 / sr)
        a16 = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)
    segs, _ = _ASR.transcribe(a16.astype(np.float32), language="de", beam_size=5, word_timestamps=True, vad_filter=False)
    words, text = [], []
    for sg in segs:
        text.append(sg.text.strip())
        for w in sg.words or []:
            words.append((w.word.strip(), float(w.start), float(w.end)))
    return words, " ".join(text)


def asr(audio, sr):
    """Transkribiert deutsches Audio mit faster-whisper (CPU)."""
    global _ASR
    if _ASR is None:
        from faster_whisper import WhisperModel
        _ASR = WhisperModel(os.environ.get("QA_WHISPER", "small"), device="cpu", compute_type="int8")
    if sr != 16000:
        n = int(len(audio) * 16000 / sr)
        audio = np.interp(np.linspace(0, len(audio) - 1, n), np.arange(len(audio)), audio).astype(np.float32)
    segs, _ = _ASR.transcribe(audio.astype(np.float32), language="de", beam_size=5, vad_filter=False)
    return " ".join(s.text.strip() for s in segs)


_NUM = {"0": "null", "1": "eins", "500": "fünfhundert", "78": "achtundsiebzig"}


def _norm(s):
    s = s.lower().replace("ß", "ss")
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\d+", lambda m: _NUM.get(m.group(0), m.group(0)), s)
    s = re.sub(r"[^a-zäöü ]+", " ", s)
    return s.split()


def wer(ref, hyp):
    r, h = _norm(ref), _norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / max(1, len(r))


def f0_median(audio, sr):
    """Grobe Tonhöhe (Hz) per Autokorrelation – zur Plausibilitätsprüfung (Männerstimme ~ 85–160 Hz)."""
    x = audio.astype(np.float64)
    hop, win = int(sr * 0.02), int(sr * 0.05)
    out = []
    for i in range(0, len(x) - win, hop):
        f = x[i:i + win] * np.hanning(win)
        if np.sqrt(np.mean(f ** 2)) < 0.02:
            continue
        ac = np.correlate(f, f, "full")[win - 1:]
        lo, hi = int(sr / 400), int(sr / 60)
        k = lo + np.argmax(ac[lo:hi])
        if ac[k] > 0.3 * ac[0]:
            out.append(sr / k)
    return float(np.median(out)) if out else 0.0


def main():
    cmd = sys.argv[1]
    if cmd == "design":
        model_dir, out_dir, desc, text = sys.argv[2:6]
        n = int(sys.argv[6]) if len(sys.argv) > 6 else 3
        os.makedirs(out_dir, exist_ok=True)
        t0 = time.time()
        load(model_dir)
        print(f"Modell geladen in {time.time() - t0:.0f}s", flush=True)
        descs = [d.strip() for d in desc.split("||")]
        jobs = [(d, 100 + i) for d in descs for i in range(n)]
        for i, (desc, seed) in enumerate(jobs):
            t0 = time.time()
            wav = design(text, desc, seed=seed)
            sr = sample_rate()
            dur = len(wav) / sr
            path = os.path.join(out_dir, f"kandidat_{i + 1}.wav")
            sf.write(path, wav, sr)
            hyp = asr(wav, sr)
            print(f"[{i + 1}] {dur:.1f}s Audio in {time.time() - t0:.0f}s | F0 {f0_median(wav, sr):.0f} Hz | WER {wer(text, hyp):.2f} | seed {seed} | {desc} | {hyp}", flush=True)


if __name__ == "__main__":
    main()

"""Qwen3-TTS (Apache-2.0, eine der Engines aus VoiceStudio) für natürlichere Stimmen.

- Stimmentwurf mit dem VoiceDesign-Modell aus einer Beschreibung:
    python engine/qwen3_engine.py design <VoiceDesign-Modell> <ausgabe_ordner> "<Beschreibung>||<Beschreibung>" "<Beispieltext>" [seeds]
- Vertonung: build_timeline.py nutzt dieses Modul, wenn script.json "tts": {"engine": "qwen", "model": "<Base-Modell>", ...}
  enthält. Die gewählte Probe dient als Klon-Referenz (voice/voice_text), damit die Figur in jedem Satz gleich klingt.

Läuft in einer eigenen Umgebung (qwen-tts braucht transformers 4.57), die torch und faster-whisper aus der VoxCPM-Umgebung
mitbenutzt. Einrichtung: engine/README.md, Abschnitt „Qwen3-TTS“.
"""
import os
import sys
import time

import numpy as np

_MODEL = None
_PROMPTS = {}
SR = 24000  # Qwen3-TTS-Tokenizer-12Hz dekodiert mit 24 kHz


def load(model_dir):
    global _MODEL
    if _MODEL is None:
        import torch
        torch.set_num_threads(os.cpu_count() or 4)
        from qwen_tts import Qwen3TTSModel
        _MODEL = Qwen3TTSModel.from_pretrained(model_dir, device_map="cpu", dtype=torch.float32)
    return _MODEL


def sample_rate():
    return SR


def _seed(seed):
    import random
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _out(wavs, sr):
    global SR
    SR = sr
    return np.asarray(wavs[0], dtype=np.float32)


def clone(text, ref_wav, ref_text, seed=0, language="German", temperature=None, **_):
    key = (ref_wav, ref_text)
    if key not in _PROMPTS:
        _PROMPTS[key] = _MODEL.create_voice_clone_prompt(ref_audio=ref_wav, ref_text=ref_text)
    _seed(seed)
    kw = {}
    if temperature is not None:  # niedriger = gleichmäßigere Stimme von Satz zu Satz
        kw = dict(temperature=temperature, subtalker_temperature=temperature)
    wavs, sr = _MODEL.generate_voice_clone(text=text, language=language, voice_clone_prompt=_PROMPTS[key], **kw)
    return _out(wavs, sr)


_REF_EMB = {}


def _embed(wav, sr):
    import torch
    M = _MODEL.model
    target = M.speaker_encoder_sample_rate
    w = np.asarray(wav, dtype=np.float32)
    if w.ndim > 1:
        w = w.mean(1)
    if sr != target:
        import librosa
        w = librosa.resample(w, orig_sr=sr, target_sr=target)
    with torch.no_grad():
        e = M.extract_speaker_embedding(audio=w, sr=target)
    e = e.float().flatten().cpu().numpy()
    return e / (np.linalg.norm(e) + 1e-9)


_REF_F0 = {}


def pitch(wav, sr):
    """Median-Tonhöhe in Hz (Praat über parselmouth), None wenn nicht messbar."""
    try:
        import parselmouth
        from parselmouth.praat import call
    except ImportError:
        return None
    snd = parselmouth.Sound(np.asarray(wav, dtype=np.float64), sampling_frequency=sr)
    f = call(call(snd, "To Pitch", 0.0, 75, 500), "Get quantile", 0, 0, 0.5, "Hertz")
    return float(f) if f == f and f > 0 else None


def pitch_ref(ref_wav):
    if ref_wav not in _REF_F0:
        import soundfile as sf
        r, rs = sf.read(ref_wav, dtype="float32")
        _REF_F0[ref_wav] = pitch(r if r.ndim == 1 else r.mean(1), rs)
    return _REF_F0[ref_wav]


def speaker_similarity(wav, sr, ref_wav):
    """Kosinus-Ähnlichkeit der Sprecher-Einbettung eines Satzes zur Referenzstimme (1 = gleich)."""
    if ref_wav not in _REF_EMB:
        import soundfile as sf
        r, rs = sf.read(ref_wav, dtype="float32")
        _REF_EMB[ref_wav] = _embed(r, rs)
    return float(_REF_EMB[ref_wav] @ _embed(wav, sr))


def design(text, instruct, seed=0, language="German"):
    _seed(seed)
    wavs, sr = _MODEL.generate_voice_design(text=text, language=language, instruct=instruct)
    return _out(wavs, sr)


def main():
    if sys.argv[1] != "design":
        sys.exit("Aufruf: python engine/qwen3_engine.py design <modell> <ausgabe> \"<Beschreibung>||…\" \"<Text>\" [seeds]")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import soundfile as sf
    import voxcpm_tts as V  # nur für Whisper-Prüfung (asr, wer, f0_median)
    model_dir, out_dir, descs, text = sys.argv[2:6]
    n = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    load(model_dir)
    print(f"Modell geladen in {time.time() - t0:.0f}s", flush=True)
    i = 0
    for d in [x.strip() for x in descs.split("||")]:
        for k in range(n):
            i += 1
            t0 = time.time()
            wav = design(text, d, seed=100 + k)
            path = os.path.join(out_dir, f"kandidat_{i}.wav")
            sf.write(path, wav, SR)
            hyp = V.asr(wav, SR)
            print(f"[{i}] {len(wav) / SR:.1f}s Audio in {time.time() - t0:.0f}s | F0 {V.f0_median(wav, SR):.0f} Hz | "
                  f"WER {V.wer(text, hyp):.2f} | seed {100 + k} | {d} | {hyp}", flush=True)


if __name__ == "__main__":
    main()

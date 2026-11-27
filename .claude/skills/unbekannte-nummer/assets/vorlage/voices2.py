"""Stimmen, zweite Runde: klare Aussprache vor allem.

1. refs:  je Figur eine Referenz aus ihren deutlichsten bisherigen Aufnahmen (Whisper-Wortsicherheit hoch)
2. klon:  jede Zeile K-mal mit dem Base-Modell als Klon dieser Referenz (gleiche Stimme, stabilere Aussprache)
3. wahl:  alle Varianten (alte Stimmentwürfe + Klone) mit Whisper prüfen: Wort für Wort Sicherheit, Text muss stimmen;
          dazu Sprecher-Ähnlichkeit zur Referenz. Beste Variante -> tts_cache/<id>.wav, Bericht -> tts_cache/wahl2.json

  QWEN_DTYPE=bf16 qw/bin/python voices2.py refs
  QWEN_DTYPE=bf16 qw/bin/python voices2.py klon <Qwen3-TTS-Base> [K] [id,id]
  QWEN_DTYPE=bf16 qw/bin/python voices2.py wahl <Qwen3-TTS-Base> <whisper-medium>
"""
import glob
import json
import os
import re
import shutil
import sys
import time

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qwen3_engine as T  # noqa: E402
from story import LINES  # noqa: E402
from timeline import trim  # noqa: E402

CACHE = os.path.join(HERE, "tts_cache")
CAND = os.path.join(CACHE, "kandidaten")
REFDIR = os.path.join(CACHE, "refs")
SAY = {l["id"]: l["say"] for l in LINES}
WHO = {l["id"]: l["who"] for l in LINES}

# deutlichste alte Aufnahmen je Figur (Whisper-Mindestsicherheit >= 0.79)
REFS = {
    "noah": [("l05", 1), ("l08", 1), ("l21", 1)],
    "ben": [("l06", 0), ("l31", 0), ("l15", 1)],
    "lina": [("l03", 1), ("l10", 1)],
    "sander": [("l12", 1), ("l02", 1)],
    "pohl": [("l28", 0)],
    "durchsage": [("l17", 0)],
}


def refs():
    os.makedirs(REFDIR, exist_ok=True)
    for who, parts in REFS.items():
        chunks, texts, sr0 = [], [], None
        for i, j in parts:
            w, sr = sf.read(os.path.join(CAND, f"{i}_{j}.wav"), dtype="float32")
            sr0 = sr
            chunks += [trim(w, sr), np.zeros(int(0.3 * sr), dtype=np.float32)]
            texts.append(SAY[i])
        sf.write(os.path.join(REFDIR, f"{who}.wav"), np.concatenate(chunks), sr0)
        open(os.path.join(REFDIR, f"{who}.txt"), "w").write(" ".join(texts))
        print(who, round(sum(len(c) for c in chunks) / sr0, 1), "s:", " ".join(texts))


def klon(model, k, only):
    T.load(model)
    for j in range(k):
        for n, l in enumerate(LINES):
            i = l["id"]
            if (only and i not in only) or l["who"] == "papa":
                continue
            path = os.path.join(CAND, f"{i}_c{j}.wav")
            if os.path.exists(path):
                continue
            t0 = time.time()
            ref = os.path.join(REFDIR, f'{l["who"]}.wav')
            reft = open(os.path.join(REFDIR, f'{l["who"]}.txt')).read()
            temp = (0.7, 0.85, 0.6, 0.75)[j % 4]
            wav = T.clone(l["say"], ref, reft, seed=2000 + 31 * j + n, temperature=temp)
            sf.write(path, wav, T.sample_rate())
            print(json.dumps(dict(id=i, cand=f"c{j}", dur=round(len(wav) / T.sample_rate(), 2),
                                  sec=round(time.time() - t0, 1)), ensure_ascii=False), flush=True)


from asr import norm, wer  # noqa: E402  (Zahlen ausgeschrieben, stummes h ignoriert)


def wahl(model, whisper_dir, only=None):
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    T.load(model)
    asr = WhisperModel(whisper_dir, device="cpu", compute_type="int8")
    rp, cp = os.path.join(CACHE, "wahl2.json"), os.path.join(CACHE, "auswahl2.json")
    report = json.load(open(rp)) if only and os.path.exists(rp) else {}
    chosen = json.load(open(cp)) if only and os.path.exists(cp) else {}
    for l in LINES:
        i = l["id"]
        if only and i not in only:
            continue
        files = sorted(glob.glob(os.path.join(CAND, f"{i}_*.wav")))
        rows = []
        for f in files:
            w, sr = sf.read(f, dtype="float32")
            w = trim(w, sr)
            w16 = resample_poly(w, 16000, sr).astype(np.float32)
            segs, _ = asr.transcribe(w16, language="de", word_timestamps=True, beam_size=5)
            words = [x for s in segs for x in s.words]
            hyp = " ".join(x.word.strip() for x in words)
            probs = [x.probability for x in words] or [0.0]
            e = wer(l["say"], hyp)
            sim = T.speaker_similarity(w, sr, os.path.join(REFDIR, f'{l["who"]}.wav')) if l["who"] in REFS else 0.95
            dur = len(w) / sr
            cps = len(l["say"]) / max(dur, 0.1)
            score = float(np.mean(probs)) + 0.8 * min(probs) - 2.0 * e + 1.0 * (sim - 0.95)
            if cps < 7 or cps > 22:  # sehr gedehnt oder gehetzt
                score -= 0.15
            rows.append(dict(datei=os.path.basename(f), score=round(score, 3), wer=round(e, 2),
                             mean=round(float(np.mean(probs)), 2), min=round(min(probs), 2), sim=round(sim, 3),
                             dur=round(dur, 2), hyp=hyp))
        rows.sort(key=lambda r: -r["score"])
        report[i] = rows
        best = rows[0]
        chosen[i] = best["datei"]
        shutil.copy(os.path.join(CAND, best["datei"]), os.path.join(CACHE, f"{i}.wav"))
        print(f'{i:4} {l["who"]:9} -> {best["datei"]:10} score {best["score"]:.2f} min {best["min"]:.2f} '
              f'wer {best["wer"]:.2f} | {best["hyp"][:60]}', flush=True)
    json.dump(report, open(os.path.join(CACHE, "wahl2.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(chosen, open(os.path.join(CACHE, "auswahl2.json"), "w"), indent=1)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "refs":
        refs()
    elif cmd == "klon":
        klon(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2,
             set(sys.argv[4].split(",")) if len(sys.argv) > 4 else None)
    elif cmd == "wahl":
        wahl(sys.argv[2], sys.argv[3], set(sys.argv[4].split(",")) if len(sys.argv) > 4 else None)

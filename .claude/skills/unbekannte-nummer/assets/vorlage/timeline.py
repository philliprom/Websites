"""Zeitleiste aus den gewählten Stimmen: Stille abschneiden, Pausen setzen, Ereignisse (Vibration, Gong …).

  python3 timeline.py  ->  timeline.json, tts_cache/trim/<id>.wav
"""
import json
import os
import shutil

import numpy as np
import soundfile as sf

from story import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "tts_cache")
TRIM = os.path.join(CACHE, "trim")

# Pause VOR der Zeile (Sekunden); Standard 0.2
GAP = {
    "l01": 0.45, "l02": 0.35, "l03": 0.15, "l04": 0.2,
    "r1": 0.75,   # Vibration
    "l05": 0.35, "l06": 0.15, "l07": 0.45, "l08": 0.25, "l09": 0.3,
    "l10": 0.55, "l11": 0.15, "l12": 0.45,
    "r2": 0.75, "l13": 0.45, "l14": 1.0, "l15": 0.2, "l16": 0.55,
    "l17": 1.25,  # Gong vor der Durchsage
    "l18": 0.45, "r3": 0.75, "l19": 0.7, "l20": 0.25, "l21": 0.15, "l22": 0.35,
    "r4": 0.85,   # Szenenwechsel Flur
    "l23": 0.2, "l24": 0.35, "l25": 0.1,
    "l26": 1.9,   # Rennen zur Treppe + Kellertür
    "l27": 0.25, "l28": 0.3, "r5": 0.8, "r5b": 0.35, "l29": 0.6, "l30": 0.55, "l31": 0.6,
}
END_PAUSE = 0.7
END_CARD = 4.0
REGEL_TEMPO = 1.0       # keine künstliche Beschleunigung mehr (klang unnatürlich)
MAX_PAUSE = 0.45        # nur sehr lange Pausen innerhalb einer Zeile kürzen


def cap_pauses(w, sr, max_pause=MAX_PAUSE, thr_db=-40):
    win = int(0.02 * sr)
    env = np.sqrt(np.convolve(w ** 2, np.ones(win) / win, mode="same"))
    quiet = env < env.max() * 10 ** (thr_db / 20)
    out, i, n = [], 0, len(w)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            run = j - i
            keep = min(run, int(max_pause * sr))
            out.append(w[i:i + keep // 2])
            out.append(w[j - (keep - keep // 2):j])
            i = j
        else:
            j = i
            while j < n and not quiet[j]:
                j += 1
            out.append(w[i:j])
            i = j
    return np.concatenate(out) if out else w


def tempo(w, sr, factor):
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(w.astype(np.float64), sampling_frequency=sr)
    out = call(snd, "Lengthen (overlap-add)", 75, 400, factor)
    return np.asarray(out.values[0], dtype=np.float32)


def apply_manual():
    p = os.path.join(CACHE, "auswahl_manuell.json")
    if not os.path.exists(p):
        return
    for i, j in json.load(open(p)).items():
        src = os.path.join(CACHE, "kandidaten", f"{i}_{j}.wav")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(CACHE, f"{i}.wav"))


def trim(w, sr, thr_db=-38, pad=0.04):
    a = np.abs(w)
    win = int(0.01 * sr)
    env = np.convolve(a, np.ones(win) / win, mode="same")
    thr = env.max() * 10 ** (thr_db / 20)
    idx = np.where(env > thr)[0]
    if not len(idx):
        return w
    s = max(0, idx[0] - int(pad * sr))
    e = min(len(w), idx[-1] + int(pad * 1.5 * sr))
    return w[s:e]


def words_of(path):
    """Wortzeiten (Whisper) relativ zum Zeilenbeginn, für genaue Untertitel."""
    try:
        from faster_whisper import WhisperModel
        from scipy.signal import resample_poly
    except ImportError:
        return None
    global _ASR
    if "_ASR" not in globals():
        _ASR = WhisperModel(os.environ.get("QA_WHISPER", "small"), device="cpu", compute_type="int8")
    w, sr = sf.read(path, dtype="float32")
    segs, _ = _ASR.transcribe(resample_poly(w, 16000, sr).astype(np.float32), language="de", word_timestamps=True,
                              beam_size=5)
    return [[round(x.start, 3), round(x.end, 3), x.word.strip()] for s_ in segs for x in s_.words]


def main():
    os.makedirs(TRIM, exist_ok=True)
    if not os.path.exists(os.path.join(CACHE, "auswahl2.json")):
        apply_manual()  # alte Auswahl (Runde 1)
    seen_n = set()
    t = 0.0
    out = []
    events = [dict(kind="alarm_start", t=0.0)]
    for l in LINES:
        w, sr = sf.read(os.path.join(CACHE, f'{l["id"]}.wav'), dtype="float32")
        if w.ndim > 1:
            w = w.mean(1)
        w = trim(w, sr)
        w = cap_pauses(w, sr, MAX_PAUSE)
        if l["kind"] == "regel" and REGEL_TEMPO != 1.0:
            w = tempo(w, sr, REGEL_TEMPO)
        sf.write(os.path.join(TRIM, f'{l["id"]}.wav'), w, sr)
        gap = GAP.get(l["id"], 0.2)
        if l["kind"] == "regel" and l["n"] not in seen_n:
            seen_n.add(l["n"])
            events.append(dict(kind="buzz", t=round(t + 0.1, 3), regel=l["n"]))
        if l["id"] == "l17":
            events.append(dict(kind="gong", t=round(t + 0.05, 3)))
        if l["id"] == "r4":
            events.append(dict(kind="tuer_flur", t=round(t + 0.05, 3)))
        if l["id"] == "l26":
            events.append(dict(kind="tuer_keller", t=round(t + 0.1, 3)))
        t += gap
        d = len(w) / sr
        out.append(dict(id=l["id"], who=l["who"], kind=l["kind"], start=round(t, 3), end=round(t + d, 3),
                        dur=round(d, 3), sub=l["sub"], rot=l.get("rot", []), n=l.get("n"),
                        words=None if l["kind"] == "regel" else words_of(os.path.join(TRIM, f'{l["id"]}.wav'))))
        t += d
    t += END_PAUSE
    events.append(dict(kind="endkarte", t=round(t, 3)))
    total = round(t + END_CARD, 3)
    json.dump(dict(lines=out, events=events, total=total, sr=sr), open(os.path.join(HERE, "timeline.json"), "w"),
              indent=1, ensure_ascii=False)
    for o in out:
        print(f'{o["start"]:7.2f} {o["end"]:7.2f} {o["who"]:9} {o["sub"][:60]}')
    print("Gesamt", total, "s")


if __name__ == "__main__":
    main()

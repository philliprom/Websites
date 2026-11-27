"""Spracherkennung (faster-whisper) und Wortfehlerrate für die Aussprache-Prüfung.

QA_WHISPER = Pfad zum Whisper-Modell (empfohlen: medium; small ist schneller, aber ungenauer).
"""
import os
import re
import unicodedata

import numpy as np

_ASR = None
ZAHL = {"0": "null", "1": "eins", "2": "zwei", "3": "drei", "4": "vier", "5": "fünf", "6": "sechs", "7": "sieben",
        "8": "acht", "9": "neun", "10": "zehn", "204": "zwei null vier", "k3": "ka drei", "k": "ka"}


def model():
    global _ASR
    if _ASR is None:
        from faster_whisper import WhisperModel
        _ASR = WhisperModel(os.environ.get("QA_WHISPER", "medium"), device="cpu", compute_type="int8")
    return _ASR


def _16k(audio, sr):
    audio = np.asarray(audio, dtype=np.float32)
    if audio.ndim > 1:
        audio = audio.mean(1)
    if sr != 16000:
        from scipy.signal import resample_poly
        audio = resample_poly(audio, 16000, sr).astype(np.float32)
    return audio


def words(audio, sr):
    """[(wort, start, ende, sicherheit), ...] und Gesamttext."""
    segs, _ = model().transcribe(_16k(audio, sr), language="de", beam_size=5, word_timestamps=True)
    out = [(w.word.strip(), float(w.start), float(w.end), float(w.probability)) for s in segs for w in s.words]
    return out, " ".join(w[0] for w in out)


def asr(audio, sr):
    return words(audio, sr)[1]


def norm(s):
    s = unicodedata.normalize("NFKC", s.lower()).replace("ß", "ss").replace("-", " ")
    out = []
    for w in re.sub(r"[^a-zäöü0-9' ]", " ", s).split():
        w = w.replace("'", "")
        out.extend(ZAHL.get(w, w).split())
    # stummes Dehnungs-h nach Vokal ignorieren (Pohl = Pol), sonst zählen gleich klingende Wörter als Fehler
    return [re.sub(r"([aeiouäöü])h(?=[^aeiouäöü]|$)", r"\1", w) for w in out]


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(1, len(r))

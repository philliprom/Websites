"""Figurenstimmen für DER FEUERALARM mit Qwen3-TTS.

Phase 1 (gen):  VoiceDesign erzeugt je Zeile K Kandidaten aus Figurenbeschreibung + Emotion der Zeile.
Phase 2 (pick): Base-Modell liefert Sprecher-Einbettungen; je Figur wird der Stimm-Schwerpunkt aller Kandidaten
                bestimmt und je Zeile der Kandidat gewählt, der dem Schwerpunkt am nächsten ist (gleiche Stimme in allen
                Zeilen) und den Text sauber spricht (Whisper-Prüfung).

Aufruf (Umgebung qw, siehe engine/README.md):
  QA_WHISPER=<whisper-medium> qw/bin/python voices.py gen  <VoiceDesign-Modell> [K] [id,id,...]
  QA_WHISPER=<whisper-medium> qw/bin/python voices.py pick <Base-Modell>
"""
import json
import os
import sys
import time

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qwen3_engine as T  # noqa: E402
from story import LINES, VOICES  # noqa: E402

CAND = os.path.join(HERE, "tts_cache", "kandidaten")
OUT = os.path.join(HERE, "tts_cache")


def gen(model, k, only):
    import asr as V
    os.makedirs(CAND, exist_ok=True)
    T.load(model)
    for j in range(k):  # erst ein Kandidat je Zeile, dann der nächste: früh ein vollständiger Satz zum Prüfen
        for l in LINES:
            if only and l["id"] not in only:
                continue
            path = os.path.join(CAND, f'{l["id"]}_{j}.wav')
            if os.path.exists(path):
                continue
            instr = VOICES[l["who"]] + " " + l["emo"]
            t0 = time.time()
            wav = T.design(l["say"], instr, seed=1000 + 17 * j + int(l["id"][1:] if l["id"][1:].isdigit() else 0))
            sr = T.sample_rate()
            sf.write(path, wav, sr)
            hyp = V.asr(wav, sr)
            f0 = T.pitch(wav, sr) or 0
            rec = dict(id=l["id"], j=j, dur=round(len(wav) / sr, 2), f0=round(f0), wer=round(V.wer(l["say"], hyp), 2),
                       hyp=hyp, sec=round(time.time() - t0, 1))
            print(json.dumps(rec, ensure_ascii=False), flush=True)
            with open(os.path.join(CAND, "gen.jsonl"), "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def pick(model):
    T.load(model)
    recs = {}
    for line in open(os.path.join(CAND, "gen.jsonl")):
        r = json.loads(line)
        recs[(r["id"], r["j"])] = r
    emb = {}
    for (i, j), r in recs.items():
        w, sr = sf.read(os.path.join(CAND, f"{i}_{j}.wav"), dtype="float32")
        emb[(i, j)] = T._embed(w, sr)
    who = {l["id"]: l["who"] for l in LINES}
    chosen = {}
    report = []
    for ch in VOICES:
        keys = [k for k in emb if who[k[0]] == ch and recs[k]["wer"] <= 0.25]
        if not keys:
            continue
        E = np.stack([emb[k] for k in keys])
        # Schwerpunkt iterativ: Ausreißer (andere Stimmfarbe) weniger gewichten
        c = E.mean(0)
        for _ in range(3):
            c = c / np.linalg.norm(c)
            s = E @ c
            wts = np.clip(s - np.percentile(s, 30), 0, None) + 1e-3
            c = (E * wts[:, None]).sum(0)
        c = c / np.linalg.norm(c)
        for l in [l for l in LINES if l["who"] == ch]:
            cands = [k for k in emb if k[0] == l["id"]]
            def score(k):
                return float(emb[k] @ c) - 1.5 * max(0.0, recs[k]["wer"] - 0.1)
            best = max(cands, key=score)
            chosen[l["id"]] = dict(j=best[1], sim=round(float(emb[best] @ c), 3), wer=recs[best]["wer"],
                                   f0=recs[best]["f0"], dur=recs[best]["dur"],
                                   alle=[(k[1], round(float(emb[k] @ c), 3), recs[k]["wer"]) for k in sorted(cands)])
            w, sr = sf.read(os.path.join(CAND, f"{best[0]}_{best[1]}.wav"), dtype="float32")
            sf.write(os.path.join(OUT, f'{l["id"]}.wav'), w, sr)
            report.append(f'{l["id"]:4} {ch:9} j={best[1]} sim={chosen[l["id"]]["sim"]:.3f} wer={recs[best]["wer"]:.2f} '
                          f'f0={recs[best]["f0"]} {recs[best]["dur"]}s')
    json.dump(chosen, open(os.path.join(OUT, "auswahl.json"), "w"), indent=1, ensure_ascii=False)
    print("\n".join(report))


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        k = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        only = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else None
        gen(sys.argv[2], k, only)
    else:
        pick(sys.argv[2])

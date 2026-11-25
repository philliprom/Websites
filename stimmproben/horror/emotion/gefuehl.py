"""Stimmtest „mehr Gefühl“ für Nachtschicht Teil 2: an spannenden Stellen geht die Stimme natürlich etwas höher.

Drei Fassungen desselben Textes (7 Sätze, Spannung steigt von Stufe 0 bis 3):
  A  wie Teil 1: Klon mit der normalen Referenz (voice/horror.wav aus nachtschicht-teil1)
  B  mehr Gefühl beim Sprechen: Sätze ab Stufe 1 mit einer Referenz, die höher und etwas schneller gesprochen ist
     (per PSOLA aus derselben Stimme erzeugt). Das Modell spricht dann selbst höher, die Betonung bleibt seine eigene.
  C  mehr Gefühl nachträglich: Fassung A, jeder Satz je nach Stufe per PSOLA (Praat) angehoben, ab Stufe 3 steigend.
  D  mehr Gefühl durch Auswahl: normale Referenz, aber für spannende Sätze 6 Fassungen und die genommen, die von sich aus
     1,5/2,5/3,5 Halbtöne höher liegt (Engine-Option pitch_up). Nichts nachbearbeitet.
Aufrufe (vx = Python mit parselmouth/scipy, qw = Qwen3-TTS):
  vx gefuehl.py setup       -> Referenzen (voice/) und script.json für a_wie_teil1/ und b_mehr_gefuehl/
  qw engine/build_timeline.py <a|b|d> <Qwen3-TTS-Base>   (je Projekt)
  vx gefuehl.py mix         -> c_nachbearbeitet/ und die Hörproben 1_…, 2_…, 3_….m4a plus Messwerte
"""
import json
import os
import subprocess
import sys

import numpy as np
import parselmouth
import soundfile as sf
from parselmouth.praat import call

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "..", "..", "nachtschicht-teil1", "voice", "horror.wav")
REF_TXT = os.path.join(HERE, "..", "..", "..", "nachtschicht-teil1", "voice", "horror.txt")
SENTENCES = [  # (Text, Spannung 0–3, Pause davor in s)
    ("Das Klopfen hört auf.", 0, 0.0),
    ("Einfach so.", 0, 0.55),
    ("Du hältst die Luft an.", 1, 0.8),
    ("Und dann hörst du es.", 1, 0.6),
    ("Schritte.", 2, 0.9),
    ("Nicht draußen.", 2, 0.5),
    ("Sondern hinter dir, im Lager!", 3, 0.45),
]
# Stufe -> (Halbtöne, Dauerfaktor, Tonhöhenumfang, Anstieg im Satz in Halbtönen, Lautstärke in dB)
STUFE = {0: (0.0, 1.0, 1.0, 0.0, 0.0), 1: (1.0, 0.97, 1.08, 0.0, 1.0), 2: (2.0, 0.93, 1.15, 0.5, 2.0), 3: (3.0, 0.9, 1.25, 1.5, 3.0)}


def psola(wav, sr, semitones=0.0, dur=1.0, range_=1.0, rise=0.0):
    """Tonhöhe/Tempo ändern, Klangfarbe (Formanten) bleibt: Praat-Manipulation mit Overlap-Add (PSOLA)."""
    snd = parselmouth.Sound(np.asarray(wav, dtype=np.float64), sampling_frequency=sr)
    T = snd.get_total_duration()
    man = call(snd, "To Manipulation", 0.01, 60, 300)
    pt = call(man, "Extract pitch tier")
    n = call(pt, "Get number of points")
    if n > 2:
        ts = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
        fs = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
        lm = np.median(np.log2(fs))
        new = 2 ** (lm + (np.log2(fs) - lm) * range_ + (semitones + rise * ts / T) / 12)
        call(pt, "Remove points between", 0, T)
        for t_, f_ in zip(ts, new):
            call(pt, "Add point", float(t_), float(f_))
        call([man, pt], "Replace pitch tier")
    if abs(dur - 1) > 1e-3:
        dt = call("Create DurationTier", "d", 0, T)
        call(dt, "Add point", 0, dur)
        call([man, dt], "Replace duration tier")
    return np.asarray(call(man, "Get resynthesis (overlap-add)").values[0], dtype=np.float32)


def f0_median(wav, sr):
    snd = parselmouth.Sound(np.asarray(wav, dtype=np.float64), sampling_frequency=sr)
    f = call(call(snd, "To Pitch", 0.0, 60, 300), "Get quantile", 0, 0, 0.5, "Hertz")
    return float(f) if f == f else 0.0


def setup():
    r, rs = sf.read(REF, dtype="float32")
    for name, (st, du, rg) in {"horror_spannung1": (1.5, 0.95, 1.1), "horror_spannung2": (3.0, 0.9, 1.2)}.items():
        if os.path.exists(os.path.join(HERE, "voice", name + ".wav")):
            continue   # schon da (Satz-Cache hängt am Inhalt der Referenz)
        out = psola(r, rs, st, du, rg)
        sf.write(os.path.join(HERE, "voice", name + ".wav"), out / max(1e-6, np.abs(out).max()) * 0.9, rs, subtype="PCM_16")
        print(f"Referenz {name}: {f0_median(r, rs):.0f} Hz -> {f0_median(out, rs):.0f} Hz, {len(r) / rs:.1f} s -> {len(out) / rs:.1f} s")
    for proj, use_tense in (("a_wie_teil1", False), ("b_mehr_gefuehl", True), ("d_ausgewaehlt", False)):
        segs = []
        for k, (txt, lvl, gap) in enumerate(SENTENCES):
            s = {"id": f"s{k + 1:02d}", "say": txt, "caps": [txt.upper()], "gap": gap, "sfx": [], "spannung": lvl}
            if use_tense and lvl > 0:
                s["voice"] = "spannung1" if lvl == 1 else "spannung2"
            if proj == "d_ausgewaehlt" and lvl > 0:   # natürlich höhere Fassung auswählen (Engine-Option pitch_up)
                # "take": eigener Cache-Eintrag und andere Zufallswerte als in A (sonst käme A's Fassung aus dem Cache)
                s.update({"pitch_up": {1: 1.5, 2: 2.5, 3: 3.5}[lvl], "candidates": 6, "temperature": 0.85, "pitch_tol": 0.05, "take": 1})
            segs.append(s)
        tts = {"engine": "qwen", "voice": "../../../../nachtschicht-teil1/voice/horror.wav",
               "voice_text": "../../../../nachtschicht-teil1/voice/horror.txt", "tries": 3, "max_wer": 0.1,
               "candidates": 3, "temperature": 0.7, "max_pause": 0.32}
        if use_tense:
            tts["voices"] = {v: {"voice": f"../voice/horror_{v}.wav", "voice_text": "../../../../nachtschicht-teil1/voice/horror.txt"}
                             for v in ("spannung1", "spannung2")}
        os.makedirs(os.path.join(HERE, proj), exist_ok=True)
        json.dump({"lead_in": 0.4, "default_gap": 0.5, "tail": 1.0, "tts": tts, "segments": segs},
                  open(os.path.join(HERE, proj, "script.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # ruhige Sätze (Stufe 0) von D sind dieselben wie in A: nur deren Satz-Cache übernehmen
    import shutil
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "engine"))
    from build_timeline import cache_key
    tts_a = json.load(open(os.path.join(HERE, "a_wie_teil1", "script.json"), encoding="utf-8"))["tts"]
    src, dst = os.path.join(HERE, "a_wie_teil1", "tts_cache"), os.path.join(HERE, "d_ausgewaehlt", "tts_cache")
    os.makedirs(dst, exist_ok=True)
    for txt, lvl, _ in SENTENCES:
        f_ = cache_key(txt, None, os.path.join(HERE, "a_wie_teil1", tts_a["voice"]), tts_a) + ".flac"
        if lvl == 0 and os.path.exists(os.path.join(src, f_)):
            shutil.copy(os.path.join(src, f_), dst)
    print("script.json für a_wie_teil1/, b_mehr_gefuehl/ und d_ausgewaehlt/ geschrieben")


def sentences(proj):
    tl = json.load(open(os.path.join(HERE, proj, "build", "timeline.json"), encoding="utf-8"))
    vo, sr = sf.read(os.path.join(HERE, proj, "build", "vo.wav"), dtype="float32")
    return [vo[int(s["start"] * sr):int(s["speechEnd"] * sr)] for s in tl["segments"]], sr


def assemble(parts, sr, gain_db):
    rms = [np.sqrt(np.mean(p ** 2)) for p in parts]
    target = float(np.median(rms))
    out = [np.zeros(int(0.4 * sr), np.float32)]
    for p, r_, (txt, lvl, gap), g in zip(parts, rms, SENTENCES, gain_db):
        out.append(np.zeros(int(gap * sr), np.float32))
        out.append(p * float(np.clip(target / max(r_, 1e-6), 0.63, 1.58)) * 10 ** (g / 20))
    out.append(np.zeros(int(1.0 * sr), np.float32))
    return np.concatenate(out)


def mix():
    rows = {}
    a, sr = sentences("a_wie_teil1")
    b, _ = sentences("b_mehr_gefuehl")
    d, _ = sentences("d_ausgewaehlt")
    c = [psola(p, sr, *STUFE[lvl][:4]) for p, (_, lvl, _) in zip(a, SENTENCES)]
    os.makedirs(os.path.join(HERE, "c_nachbearbeitet"), exist_ok=True)
    lv = [STUFE[lvl][4] for _, lvl, _ in SENTENCES]
    for name, parts, gains in (("1_wie_teil1", a, [0] * len(a)), ("2_mehr_gefuehl_gesprochen", b, lv), ("3_mehr_gefuehl_nachbearbeitet", c, lv),
                              ("4_mehr_gefuehl_ausgewaehlt", d, lv)):
        x = assemble(parts, sr, gains)
        tmp = os.path.join(HERE, "c_nachbearbeitet", name + ".wav")
        sf.write(tmp, x / max(1e-6, np.abs(x).max()) * 0.9, sr, subtype="PCM_16")
        # gleicher Stimmklang wie in Teil 1 (Bass +2,5 dB, Präsenz −1,5 dB), Lautheit −16 LUFS
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                        "equalizer=f=130:t=q:w=0.8:g=2.5,equalizer=f=3500:t=q:w=1.2:g=-1.5,loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "44100", "-c:a", "aac", "-b:a", "160k", os.path.join(HERE, name + ".m4a")], check=True)
        rows[name] = [f0_median(p, sr) for p in parts] + [sum(len(p) for p in parts) / sr, melodie(parts, sr)]
    print("Tonhöhe je Satz (Hz), Sprechzeit gesamt, Tonumfang in den spannenden Sätzen (Halbtöne, 10.–90. Perzentil):")
    print("  Stufe:              " + " ".join(f"{lvl:>5d}" for _, lvl, _ in SENTENCES))
    for name, r_ in rows.items():
        print(f"  {name[:20]:20s} " + " ".join(f"{v:5.0f}" for v in r_[:-2]) + f"   {r_[-2]:.1f} s   {r_[-1]:.1f} HT")


def melodie(parts, sr):
    """Tonumfang (Halbtöne) aller Sätze ab Stufe 1 zusammen: wie lebendig die Satzmelodie ist."""
    fs = []
    for p, (_, lvl, _) in zip(parts, SENTENCES):
        if lvl:
            snd = parselmouth.Sound(np.asarray(p, dtype=np.float64), sampling_frequency=sr)
            f = snd.to_pitch(0.01, 60, 300).selected_array["frequency"]
            fs += list(f[f > 0])
    q = np.percentile(fs, [10, 90]) if fs else [1, 1]
    return float(12 * np.log2(q[1] / q[0]))


if __name__ == "__main__":
    {"setup": setup, "mix": mix}[sys.argv[1]]()

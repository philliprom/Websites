#!/usr/bin/env python3
"""Macht aus einem Twitch-Clip (Querformat) ein TikTok-Video (1080×1920) mit Untertiteln, Titel und Streamer-Nennung.

  <vx>/bin/python clips/make_short.py <clip.mp4> --streamer papaplatte --titel "Er hat es wirklich gemacht 😂" [--out datei.mp4]
      [--facecam x,y,b,h] [--whisper <modellordner>]

Quelle darf 1080p oder 720p sein (720p bleibt bei einem 60-s-Clip meist unter 30 MB). Der Facecam-Bereich wird immer
bezogen auf 1920×1080 angegeben und automatisch auf die echte Auflösung umgerechnet.

Layout:
  - mit Facecam (Bereich im Quellbild, aus streamers.json oder --facecam): Facecam oben, Spielbild darunter
  - ohne Facecam: Spielbild groß in der Mitte (4:3-Ausschnitt), unscharfer Hintergrund
Untertitel per Whisper (Deutsch, Wortzeiten), das gerade gesprochene Wort gelb. Titel oben ab y 290, Untertitel höchstens
740 px breit, Streamer-Name unten links über y 1660: alles in den sicheren Zonen (engine/README.md).
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-show_entries", "format=duration", "-of", "json", path], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return d["streams"][0]["width"], d["streams"][0]["height"], float(d["format"]["duration"])


def transcribe(path, model_dir):
    from faster_whisper import WhisperModel
    import numpy as np
    m = WhisperModel(model_dir, device="cpu", compute_type="int8")
    # Ton selbst per ffmpeg dekodieren (16 kHz mono), die PyAV-Version in der Umgebung kann Dateien nicht direkt öffnen
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    segs, _ = m.transcribe(audio, language="de", word_timestamps=True, vad_filter=True)
    words = []
    for s in segs:
        for w in s.words or []:
            t = w.word.strip()
            if t:
                words.append((t, w.start, w.end))
    return words


def chunks(words, max_words=3, max_chars=20, gap=0.45):
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or sum(len(x[0]) + 1 for x in cur) + len(w[0]) > max_chars or w[1] - cur[-1][2] > gap):
            out.append(cur)
            cur = []
        cur.append(w)
        if re.search(r"[.!?…]$", w[0]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def ass_time(t):
    t = max(0.0, t)
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h}:{m:02d}:{t % 60:05.2f}"


def esc(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")")


def build_ass(words, titel, credit, dur):
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Nunito Black,84,&H00FFFFFF,&H00FFFFFF,&H001E0F14,&H64000000,0,0,0,0,100,100,1,0,1,7,3,2,170,170,420,1
Style: Titel,Nunito Black,58,&H001E0F14,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,3,16,0,8,130,130,300,1
Style: Credit,Nunito ExtraBold,36,&H00FFFFFF,&H00FFFFFF,&H50000000,&H00000000,0,0,0,0,100,100,0,0,3,8,0,1,60,60,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if titel:
        ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(dur)},Titel,,0,0,0,,{esc(titel)}")
    if credit:
        ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(dur)},Credit,,0,0,0,,{esc(credit)}")
    cl = chunks(words)
    for k, ch in enumerate(cl):
        c_end = ch[-1][2] + 0.25
        if k + 1 < len(cl):  # nie mit der nächsten Zeile überlappen, sonst stapelt libass beide übereinander
            c_end = min(c_end, cl[k + 1][0][1])
        for i, (w, ws, we) in enumerate(ch):
            st = ch[0][1] if i == 0 else ws
            en = ch[i + 1][1] if i + 1 < len(ch) else c_end
            parts = []
            for j, (w2, _, _) in enumerate(ch):
                t2 = esc(w2.upper())
                parts.append("{\\c&H003BD4FF&}" + t2 + "{\\c&H00FFFFFF&}" if j == i else t2)
            pop = "{\\fscx82\\fscy82\\t(0,120,\\fscx100\\fscy100)}" if i == 0 else ""
            ev.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Cap,,0,0,0,,{pop}{' '.join(parts)}")
    return head + "\n".join(ev) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("--streamer", required=True)
    ap.add_argument("--titel", default="")
    ap.add_argument("--out")
    ap.add_argument("--facecam", help="x,y,b,h im Quellbild")
    ap.add_argument("--whisper", default=os.environ.get("QA_WHISPER", "small"))
    a = ap.parse_args()
    cfg = {s["login"]: s for s in json.load(open(os.path.join(HERE, "streamers.json"), encoding="utf-8"))["streamer"]}
    st = cfg.get(a.streamer, {"name": a.streamer, "twitch": f"twitch.tv/{a.streamer}", "facecam": None})
    fc = [int(v) for v in a.facecam.split(",")] if a.facecam else st.get("facecam")
    W, H, dur = probe(a.clip)
    if fc and (W, H) != (1920, 1080):  # Angaben gelten für 1920×1080
        fc = [int(round(fc[0] * W / 1920)), int(round(fc[1] * H / 1080)),
              int(round(fc[2] * W / 1920)), int(round(fc[3] * H / 1080))]
    out = a.out or os.path.join(HERE, "out", os.path.splitext(os.path.basename(a.clip))[0] + "_tiktok.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    print(f"Quelle {W}×{H}, {dur:.1f} s, Facecam: {fc or 'keine'}", flush=True)
    words = transcribe(a.clip, a.whisper)
    print("Gehört:", " ".join(w for w, _, _ in words), flush=True)
    ass = out[:-4] + ".ass"
    open(ass, "w", encoding="utf-8").write(build_ass(words, a.titel, f"▶ {st['twitch']}", dur))
    bg = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.18[bg]"
    if fc:
        x, y, b, h = fc
        ch = int(round(1080 * h / b / 2) * 2)
        gh = int(round(1080 * H / W / 2) * 2)
        y_cam, y_game = 395, 395 + ch + 12
        if y_game + gh > 1640:  # Spielbild darf nicht in die untere Zone ragen
            y_game = 1640 - gh
        filt = (f"{bg};[0:v]crop={b}:{h}:{x}:{y},scale=1080:{ch}:flags=lanczos[cam];[0:v]scale=1080:{gh}:flags=lanczos[game];"
                f"[bg][game]overlay=0:{y_game}[v1];[v1][cam]overlay=0:{y_cam}[v2]")
    else:
        cw = min(W, int(H * 4 / 3))
        gh = int(round(1080 * H / cw / 2) * 2)
        y_game = 470
        filt = f"{bg};[0:v]crop={cw}:{H}:{(W - cw) // 2}:0,scale=1080:{gh}:flags=lanczos[game];[bg][game]overlay=0:{y_game}[v2]"
    ass_esc = ass.replace(":", "\\:").replace("'", "\\'")
    filt += f";[v2]ass='{ass_esc}':fontsdir='{FONTS}'[v]"
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", a.clip, "-filter_complex", filt, "-map", "[v]", "-map", "0:a?",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-r", "30", "-c:v", "libx264", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("Fertig:", out)


if __name__ == "__main__":
    main()

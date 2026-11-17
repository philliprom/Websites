"""Simulation „16 Bundesländer – nur eins überlebt“: Bälle in einem drehenden Ring mit Lücke. Wer rausfällt, ist raus.

Aufruf:
  python3 sim-bundeslaender-test/sim.py suche [anzahl]   -> probiert Seeds, zeigt die mit gutem Tempo
  python3 sim-bundeslaender-test/sim.py bau <seed>       -> build/sim.js, build/timeline.json, build/mix.wav
Alles deterministisch: gleicher Seed = gleiches Rennen. Der Seed wird nach Tempo ausgesucht, nie nach Sieger.
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")

# Kürzel, Name, Flaggenstreifen (oben -> unten)
STATES = [
    ("BW", "Baden-Württemberg", ["#1B1B1B", "#F2C200"]),
    ("BY", "Bayern", ["#FFFFFF", "#2F8CEB"]),
    ("BE", "Berlin", ["#E53935", "#FFFFFF", "#E53935"]),
    ("BB", "Brandenburg", ["#E53935", "#FFFFFF"]),
    ("HB", "Bremen", ["#E53935", "#FFFFFF", "#E53935", "#FFFFFF"]),
    ("HH", "Hamburg", ["#D32F2F"]),
    ("HE", "Hessen", ["#E53935", "#FFFFFF"]),
    ("MV", "Mecklenburg-Vorpommern", ["#1565C0", "#FFFFFF", "#FDD835", "#FFFFFF", "#C62828"]),
    ("NI", "Niedersachsen", ["#1B1B1B", "#D32F2F", "#F2C200"]),
    ("NRW", "Nordrhein-Westfalen", ["#2E7D32", "#FFFFFF", "#D32F2F"]),
    ("RP", "Rheinland-Pfalz", ["#1B1B1B", "#D32F2F", "#F2C200"]),
    ("SL", "Saarland", ["#1B1B1B", "#D32F2F", "#F2C200"]),
    ("SN", "Sachsen", ["#FFFFFF", "#2E7D32"]),
    ("ST", "Sachsen-Anhalt", ["#1B1B1B", "#F2C200"]),
    ("SH", "Schleswig-Holstein", ["#1565C0", "#FFFFFF", "#D32F2F"]),
    ("TH", "Thüringen", ["#FFFFFF", "#D32F2F"]),
]

P = dict(cx=540.0, cy=1010.0, R=410.0, r=46.0, g=900.0, omega=0.9, hw0=0.15, hw_step=0.01,
         vkick=650.0, vmax=1600.0, e_ball=0.97, fps=30, sub=20, max_t=60.0, settle=0.0)


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def simulate(seed, p=P, record=False):
    rnd = random.Random(seed)
    n = len(STATES)
    cx, cy, R, r = p["cx"], p["cy"], p["R"], p["r"]
    pos = []
    while len(pos) < n:
        a, d = rnd.uniform(0, 2 * math.pi), (R - r - 30) * math.sqrt(rnd.random())
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        if all((x - qx) ** 2 + (y - qy) ** 2 > (2 * r + 8) ** 2 for qx, qy in pos):
            pos.append((x, y))
    X = [q[0] for q in pos]
    Y = [q[1] for q in pos]
    VX, VY = [], []
    for _ in range(n):
        a, s = rnd.uniform(0, 2 * math.pi), rnd.uniform(350, 700)
        VX.append(s * math.cos(a))
        VY.append(s * math.sin(a))
    state = ["in"] * n  # in | fall | gone
    phi0 = rnd.uniform(0, 2 * math.pi)
    dt = 1.0 / (p["fps"] * p["sub"])
    t = 0.0
    events, frames, elim = [], [], []
    winner, t_win = None, None
    last_wall = [-1.0] * n
    while t < p["max_t"]:
        for _ in range(p["sub"]):
            t += dt
            alive = [i for i in range(n) if state[i] == "in"]
            if len(alive) == 1 and winner is None:
                winner, t_win = alive[0], t
                events.append(["win", round(t, 4), winner])
            phi = phi0 + p["omega"] * t
            hw = p["hw0"] + p["hw_step"] * (n - len(alive))
            for i in range(n):
                if state[i] == "gone":
                    continue
                VY[i] += p["g"] * dt
                X[i] += VX[i] * dt
                Y[i] += VY[i] * dt
                if state[i] == "fall" and Y[i] > 2200:
                    state[i] = "gone"
            if winner is not None:
                continue  # nach dem Sieg nur noch Fallende weiter bewegen
            # Ball gegen Ball
            for a_ in range(len(alive)):
                i = alive[a_]
                for j in alive[a_ + 1:]:
                    dx, dy = X[j] - X[i], Y[j] - Y[i]
                    d2 = dx * dx + dy * dy
                    if d2 < (2 * r) ** 2 and d2 > 1e-9:
                        d = math.sqrt(d2)
                        nx, ny = dx / d, dy / d
                        ov = 2 * r - d
                        X[i] -= nx * ov / 2
                        Y[i] -= ny * ov / 2
                        X[j] += nx * ov / 2
                        Y[j] += ny * ov / 2
                        rv = (VX[j] - VX[i]) * nx + (VY[j] - VY[i]) * ny
                        if rv < 0:
                            jimp = -(1 + p["e_ball"]) * rv / 2
                            VX[i] -= jimp * nx
                            VY[i] -= jimp * ny
                            VX[j] += jimp * nx
                            VY[j] += jimp * ny
                            if -rv > 220:
                                events.append(["ball", round(t, 4), i, j, round(-rv)])
            # Ball gegen Ring
            ends = [(cx + R * math.cos(phi + s * hw), cy + R * math.sin(phi + s * hw)) for s in (-1, 1)]
            for i in alive:
                dx, dy = X[i] - cx, Y[i] - cy
                d = math.hypot(dx, dy)
                if d < R - r - 1:
                    continue
                th = math.atan2(dy, dx)
                dlt = abs(wrap(th - phi))
                if d > R + 4 and dlt < hw:
                    state[i] = "fall"
                    elim.append((t, i))
                    events.append(["out", round(t, 4), i, round(th, 4)])
                    continue
                half = math.asin(min(1.0, r / max(d, r)))
                if dlt + half < hw:
                    continue  # passt ganz durch die Lücke
                if dlt >= hw:  # Wand
                    if d > R - r:
                        nx, ny = dx / d, dy / d
                        vn = VX[i] * nx + VY[i] * ny
                        X[i], Y[i] = cx + nx * (R - r), cy + ny * (R - r)
                        if vn > 0:
                            out = max(vn, p["vkick"])
                            VX[i] -= (vn + out) * nx
                            VY[i] -= (vn + out) * ny
                            # winzige Störung gegen ewige Kreisbahnen
                            rot = rnd.uniform(-0.05, 0.05)
                            c, s_ = math.cos(rot), math.sin(rot)
                            VX[i], VY[i] = VX[i] * c - VY[i] * s_, VX[i] * s_ + VY[i] * c
                            if vn > 200 and t - last_wall[i] > 0.05:
                                events.append(["wall", round(t, 4), i, round(vn), round(th, 4)])
                                last_wall[i] = t
                else:  # Kante der Lücke
                    for ex, ey in ends:
                        ddx, ddy = X[i] - ex, Y[i] - ey
                        dd = math.hypot(ddx, ddy)
                        if dd < r + 8 and dd > 1e-6:
                            nx, ny = ddx / dd, ddy / dd
                            X[i], Y[i] = ex + nx * (r + 8), ey + ny * (r + 8)
                            vn = VX[i] * nx + VY[i] * ny
                            if vn < 0:
                                VX[i] -= 2 * vn * nx
                                VY[i] -= 2 * vn * ny
                                if -vn > 200:
                                    events.append(["edge", round(t, 4), i, round(-vn)])
            for i in alive:
                sp = math.hypot(VX[i], VY[i])
                if sp > p["vmax"]:
                    VX[i] *= p["vmax"] / sp
                    VY[i] *= p["vmax"] / sp
        if record:
            frames.append([round(phi0 + p["omega"] * (t_win if t_win else t), 4),
                           round(p["hw0"] + p["hw_step"] * (n - sum(1 for s in state if s == "in")), 4),
                           [[round(X[i], 1), round(Y[i], 1), {"in": 1, "fall": 2, "gone": 0}[state[i]]] for i in range(n)]])
        if winner is not None and t > t_win + 1.5:
            break
    return dict(seed=seed, elim=elim, winner=winner, t_win=t_win, events=events, frames=frames)


def pace(res):
    """Gütemaß fürs Tempo (nicht für den Sieger)."""
    if res["winner"] is None:
        return None
    ts = [t for t, _ in res["elim"]]
    if len(ts) < 15:
        return None
    gaps = [b - a for a, b in zip([0.0] + ts, ts)]
    duel = ts[-1] - ts[-2]
    burst = sum(1 for g in gaps if g < 0.25)
    return dict(first=ts[0], end=ts[-1], duel=duel, maxgap=max(gaps), burst=burst)


def search(count):
    import multiprocessing as mp
    with mp.Pool(4) as pool:
        res = pool.map(_one, range(1, count + 1))
    good = []
    for seed, q in res:
        if q and 0.8 <= q["first"] <= 3.0 and 20 <= q["end"] <= 34 and 3.0 <= q["duel"] <= 9 and q["maxgap"] < 7 and q["burst"] <= 2:
            good.append((abs(q["end"] - 28) + q["maxgap"] * 0.3, seed, q))
    good.sort()
    for _, seed, q in good[:15]:
        print(seed, {k: round(v, 2) for k, v in q.items()})
    print(f"{len(good)} von {count} Seeds passen")


def _one(seed):
    return seed, pace(simulate(seed))


# ---------------------------------------------------------------- Ton
def build_audio(res, duration):
    sys.path.insert(0, os.path.join(HERE, "..", "engine"))
    import numpy as np
    import audio as A
    SR = A.SR
    n = int(duration * SR) + SR
    fx = np.zeros(n)

    def put(sig, t, gain=1.0):
        i = int(t * SR)
        if i >= n:
            return
        sig = sig[: n - i]
        fx[i:i + len(sig)] += sig * gain

    scale = [57, 60, 62, 64, 67, 69, 72, 74, 76, 79, 81]  # a-Moll pentatonisch
    melody = [0, 2, 4, 3, 5, 4, 2, 1, 3, 5, 7, 6, 4, 5, 3, 2]
    k = 0
    last = -1.0
    for ev in res["events"]:
        kind, t = ev[0], ev[1]
        if kind == "wall" and t - last > 0.07:
            v = min(1.0, ev[3] / 1200)
            note = scale[min(len(scale) - 1, melody[k % len(melody)] + (2 if k // len(melody) % 2 else 0))]
            put(A.marimba(A.midi(note), 0.5, 0.20 + 0.16 * v), t)
            k += 1
            last = t
        elif kind == "ball" and ev[4] > 350:
            put(A.sfx_tap(), t, 0.25)
        elif kind == "out":
            put(A.sfx_pop(), t, 0.9)
            put(A.sfx_whoosh(), t + 0.02, 0.35)
        elif kind == "win":
            put(A.sfx_confetti(), t + 0.3, 0.9)
            for m_, tt in zip([69, 72, 76, 81], [0.3, 0.42, 0.54, 0.66]):
                put(A.bell(A.midi(m_), 1.4, 0.22), t + tt)
    mus = A.music(duration, {"bpm": 124, "inst": "pluck", "clap": 0.7, "ambience": 0.1,
                              "chords": [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [52, 56, 59, 64]],
                              "roots": [45, 41, 48, 40], "arp": [0, 2, 1, 3, 2, 1, 0, 2]})
    mus = np.asarray(mus, dtype=float)
    if mus.ndim > 1:
        mus = mus.mean(axis=1)
    m = np.zeros(n)
    m[: min(n, len(mus))] = mus[: min(n, len(mus))]
    mix = fx + m * 0.55
    mix = mix[: int(duration * SR)]
    peak = np.max(np.abs(mix)) or 1.0
    mix = mix / peak * 0.89
    import wave
    with wave.open(os.path.join(BUILD, "mix.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())


def build(seed, duration=None):
    os.makedirs(BUILD, exist_ok=True)
    res = simulate(seed, record=True)
    q = pace(res)
    t_win = res["t_win"]
    duration = round(duration or (t_win + 5.0), 2)
    data = dict(seed=seed, p=P, states=STATES, t_win=t_win, winner=res["winner"], frames=res["frames"],
                events=res["events"], order=[i for _, i in res["elim"]], elim=[[round(t, 3), i] for t, i in res["elim"]])
    with open(os.path.join(BUILD, "sim.js"), "w", encoding="utf-8") as f:
        f.write("window.SIM = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    with open(os.path.join(BUILD, "timeline.json"), "w") as f:
        json.dump({"fps": P["fps"], "duration": duration, "segments": []}, f)
    build_audio(res, duration)
    print(f"Seed {seed}: Sieger {STATES[res['winner']][1]}, Ende {t_win:.1f}s, Video {duration}s, Tempo {q}")
    print("Reihenfolge raus:", ", ".join(f"{STATES[i][0]} {t:.1f}s" for t, i in res["elim"]))


if __name__ == "__main__":
    if sys.argv[1] == "suche":
        search(int(sys.argv[2]) if len(sys.argv) > 2 else 60)
    else:
        build(int(sys.argv[2]))

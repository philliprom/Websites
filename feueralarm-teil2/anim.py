"""Animation: Figuren (Blickrichtung, Lippen, Blinzeln, Gesten, Gehen) und POV-Kamera (Handkamera, Blickwechsel).

Alles wird pro Bild als Schlüsselbild eingetragen (dicht, robust). Zeiten in Sekunden der Gesamtzeitleiste.
"""
import math

import bpy
import numpy as np
from mathutils import Vector

FPS = 30


def smooth(a, b, x):
    if b == a:
        return 1.0 if x >= b else 0.0
    t = min(1.0, max(0.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def noise1(t, seed, freq=0.5):
    """glattes Rauschen -1..1 (Summe von Sinus mit festen Phasen)."""
    s = 0.0
    for k, (f, a) in enumerate(((1.0, 0.55), (2.13, 0.3), (4.37, 0.15))):
        ph = (seed * 12.9898 + k * 78.233) % (2 * math.pi)
        s += a * math.sin(2 * math.pi * freq * f * t + ph)
    return s


def envelope(wav, sr, fps=FPS):
    """Lautstärke je Bild (0..1) für Lippenbewegung."""
    hop = sr / fps
    n = int(len(wav) / hop) + 1
    out = np.zeros(n)
    for i in range(n):
        a, b = int(i * hop), int((i + 1) * hop)
        seg = wav[a:b]
        if len(seg):
            out[i] = np.sqrt((seg ** 2).mean())
    if out.max() > 0:
        out = out / np.percentile(out[out > 0], 95)
    out = np.clip(out, 0, 1.2)
    # leicht glätten, Mund öffnet schneller als er schließt
    sm = np.zeros_like(out)
    v = 0.0
    for i, x in enumerate(out):
        v = v + (x - v) * (0.75 if x > v else 0.45)
        sm[i] = v
    return sm


# ---------------------------------------------------------------- Posen
# Arme (linke Seite, rechts gespiegelt): (Heben x, Abspreizen, Drehen um den Oberarm, Ellbogen) in Grad
ARM = {  # Schulter: Euler ZXY (erst Drehen um den Oberarm, dann heben, dann abspreizen)
    "stehen": (-6, 6, 0, -14),
    "sitzen": (-30, 8, -25, -60),
    "tisch": (-40, 10, -20, -65),
    "zeigen": (-80, 0, 0, -5),
    "telefon": (-20, 110, 90, -130),
    "liste": (-25, 10, -35, -95),
    "verschraenkt": (-25, 8, -75, -105),
    "bauch": (-10, 5, -70, -95),
    "abwehr": (-40, 25, -30, -100),
    "hand_hoch": (-160, 10, 0, -30),
    "schluessel": (-55, 0, -15, -35),
    "greifen": (-55, 5, -20, -35),
    "kabel": (-160, 15, 0, -20),
    "fenster": (-60, 10, -15, -40),
    "huefte": (-5, 14, 0, -30),
}
BRAUE = {  # (Neigung innen, Höhe)
    "neutral": (0, 0.0),
    "boese": (16, -0.006),
    "sorge": (-14, 0.006),
    "schreck": (-6, 0.014),
    "skeptisch": (10, 0.0),
}


class Actor:
    def __init__(self, names, seated=False, seed=1):
        O = bpy.data.objects

        def get(v):
            return [O[x] for x in v] if isinstance(v, list) else O[v]
        self.o = {k: get(v) for k, v in names.items()}
        self.brow_z0 = [bp.location.z for bp in self.o["brauen"]]
        for s_ in ("l", "r"):
            self.o[f"schulter_{s_}"].rotation_mode = "ZXY"
        self.becken_z0 = self.o["becken"].location.z
        self.seated = seated
        self.seed = seed
        self.tracks = []          # (t0, t1, fn) Ebenen
        self.looks = []           # (t, target|None, dauer)
        self.arms = {"l": [], "r": []}  # (t, pose, dauer)
        self.brows = []           # (t, name, dauer)
        self.speech = []          # (t0, env array)
        self.moves = []           # (t0, t1, p0, p1, gehen)
        self.extra = []           # (fn) beliebige Zusatzfunktionen fn(self, t)
        self.base_pos = None
        self.follow = None        # fn(t) -> Vector: Versatz (z. B. fahrendes Auto)
        self.base_rot = 0.0
        self.blink_off = False
        self.mouth_closed = 0.3
        self.idle = 1.0
        self.lean = []            # (t, (x, z) Grad, dauer) Oberkörper
        rest = "sitzen" if seated else "stehen"
        for s in ("l", "r"):
            self.arms[s].append((-1e9, rest, 0.0))
        self.brows.append((-1e9, "neutral", 0.0))
        self.lean.append((-1e9, (0.0, 0.0), 0.0))
        self.looks.append((-1e9, None, 0.0))

    # ---- Planung
    def place(self, pos, rot):
        self.base_pos = Vector(pos)
        self.base_rot = rot
        r = self.o["root"]
        r.location = self.base_pos
        r.rotation_euler = (0, 0, math.radians(rot))
        bpy.context.view_layer.update()
        self.head_local = r.matrix_world.inverted() @ self.o["kopf"].matrix_world.translation + Vector((0, 0, 0.15))

    def look(self, t, target, dur=0.35):
        """target: Weltpunkt, 'cam' oder None (geradeaus)."""
        self.looks.append((t, target, dur))

    def arm(self, t, side, pose, dur=0.4):
        for s in (("l", "r") if side == "beide" else (side,)):
            self.arms[s].append((t, pose, dur))

    def brow(self, t, name, dur=0.25):
        self.brows.append((t, name, dur))

    def say(self, t0, env):
        self.speech.append((t0, env))

    def move(self, t0, t1, p1, walk=True, rot=None):
        self.moves.append((t0, t1, None, Vector(p1), walk, rot))

    def bend(self, t, xz, dur=0.4):
        self.lean.append((t, xz, dur))

    # ---- Auswertung
    @staticmethod
    def _blend_list(lst, t, value_of, mix):
        lst = sorted(lst, key=lambda e: e[0])
        cur = value_of(lst[0])
        for e in lst[1:]:
            if t < e[0]:
                break
            w = smooth(e[0], e[0] + max(e[2], 1e-3), t)
            cur = mix(cur, value_of(e), w)
        return cur

    def pose_at(self, t, cam_pos):
        o = self.o
        # Position / Gehen
        pos = Vector(self.base_pos)
        rot = self.base_rot
        walking = 0.0
        for (t0, t1, _p0, p1, walk, r1) in sorted(self.moves, key=lambda m: m[0]):
            if t >= t0:
                w = smooth(t0, t1, t) if walk else smooth(t0, t1, t)
                p0 = pos.copy()
                pos = p0.lerp(p1, w)
                if r1 is not None:
                    rot = rot + (r1 - rot) * smooth(t0, t0 + min(0.4, t1 - t0), t)
                if walk and t0 <= t <= t1:
                    walking = min(smooth(t0, t0 + 0.25, t), 1 - smooth(t1 - 0.25, t1, t))
        if self.follow is not None:
            pos = pos + self.follow(t)
        o["root"].location = pos
        o["root"].rotation_euler = (0, 0, math.radians(rot))
        # Blick
        yaw = pitch = 0.0

        def look_val(e):
            tgt = e[1]
            if tgt is None:
                return (0.0, 0.0)
            p = Vector(cam_pos) if tgt == "cam" else Vector(tgt) + (self.follow(t) if self.follow else Vector())
            # in Wurzelraum der Figur
            ca, sa = math.cos(math.radians(-rot)), math.sin(math.radians(-rot))
            d = p - pos
            lx, ly = d.x * ca - d.y * sa, d.x * sa + d.y * ca
            v = Vector((lx, ly, d.z)) - self.head_local
            yw = math.degrees(math.atan2(v.x, -v.y))
            pt = -math.degrees(math.atan2(v.z, math.hypot(v.x, v.y)))
            return (max(-110, min(110, yw)), max(-35, min(35, pt)))
        yaw, pitch = self._blend_list(self.looks, t, look_val,
                                      lambda a, b, w: (a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w))
        # Sprechen: Mund + kleines Nicken
        talk = 0.0
        for (t0, env) in self.speech:
            i = int(round((t - t0) * FPS))
            if 0 <= i < len(env):
                talk = max(talk, float(env[i]))
        idle = self.idle
        nx = noise1(t, self.seed, 0.23) * idle
        ny = noise1(t, self.seed + 5, 0.17) * idle
        yaw += 3.0 * nx
        pitch += 2.0 * ny - 2.5 * talk * (0.5 + 0.5 * math.sin(t * 9.0 + self.seed))
        lean_x, lean_z = self._blend_list(self.lean, t, lambda e: e[1],
                                          lambda a, b, w: (a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w))
        # Verteilung: Rumpf 20 %, Hals 30 %, Kopf 50 %
        breath = 0.8 * math.sin(2 * math.pi * 0.27 * t + self.seed)
        o["torso"].rotation_euler = (math.radians(0.2 * pitch * 0.2 + breath * 0.5 + lean_x), 0,
                                     math.radians(0.2 * yaw + lean_z))
        o["hals"].rotation_euler = (math.radians(0.4 * pitch), 0, math.radians(0.3 * yaw))
        o["kopf"].rotation_euler = (math.radians(0.6 * pitch), math.radians(1.5 * nx), math.radians(0.5 * yaw))
        # Pupillen leicht in Blickrichtung
        for pp in o["pupillen"]:
            pp.location.x = max(-0.012, min(0.012, -yaw * 0.0002))
            pp.location.z = -0.004 + max(-0.008, min(0.008, -pitch * 0.0003))
        # Mund
        m = self.mouth_closed + (1.05 - self.mouth_closed) * min(1.0, talk)
        o["mund"].scale = (1.0 - 0.12 * min(1.0, talk), 1.0, m)
        # Blinzeln
        blink = 1.0
        if not self.blink_off:
            period = 2.6 + 1.7 * ((self.seed * 0.37) % 1)
            ph = (t + self.seed * 0.71) % period
            if ph < 0.13:
                blink = 0.1 + 0.9 * abs(ph - 0.065) / 0.065
        for e in o["augen"]:
            e.scale = (1, 1, blink)
        # Brauen
        bt, bz = self._blend_list(self.brows, t, lambda e: BRAUE[e[1]],
                                  lambda a, b, w: (a[0] + (b[0] - a[0]) * w, a[1] + (b[1] - a[1]) * w))
        for k, bp in enumerate(o["brauen"]):
            sx = 1 if k == 0 else -1
            bp.rotation_euler[1] = math.radians(-sx * bt)
            bp.location.z = self.brow_z0[k] + bz + 0.004 * talk
        # Arme
        for s, sx in (("l", 1), ("r", -1)):
            a = self._blend_list(self.arms[s], t, lambda e: ARM[e[1]],
                                 lambda a_, b_, w: tuple(x + (y - x) * w for x, y in zip(a_, b_)))
            sxr, ab, sz, el = a
            if walking > 0:
                ph = 2 * math.pi * 1.9 * t + (0 if s == "l" else math.pi)
                sxr += walking * 28 * math.sin(ph)
                el += walking * -25
            o[f"schulter_{s}"].rotation_euler = (math.radians(sxr), math.radians(-sx * ab), math.radians(sx * sz))
            o[f"ellbogen_{s}"].rotation_euler = (math.radians(el), 0, 0)
        # Beine beim Gehen
        if not self.seated:
            ph = 2 * math.pi * 1.9 * t
            for s, off in (("l", 0), ("r", math.pi)):
                hip = walking * 26 * math.sin(ph + off)
                knee = walking * 38 * max(0.0, math.sin(ph + off + 1.3))
                o[f"huefte_{s}"].rotation_euler = (math.radians(-hip), 0, 0)
                o[f"knie_{s}"].rotation_euler = (math.radians(knee), 0, 0)
            o["becken"].location.z = self.becken_z0 + walking * 0.025 * abs(math.sin(ph))
        for fn in self.extra:
            fn(self, t)

    def keys(self, f):
        o = self.o
        for k in ("torso", "hals", "kopf", "schulter_l", "schulter_r", "ellbogen_l", "ellbogen_r", "huefte_l", "huefte_r",
                  "knie_l", "knie_r", "root"):
            o[k].keyframe_insert("rotation_euler", frame=f)
        o["root"].keyframe_insert("location", frame=f)
        o["becken"].keyframe_insert("location", frame=f)
        o["mund"].keyframe_insert("scale", frame=f)
        for e in o["augen"]:
            e.keyframe_insert("scale", frame=f)
        for pp in o["pupillen"]:
            pp.keyframe_insert("location", frame=f)
        for bp in o["brauen"]:
            bp.keyframe_insert("rotation_euler", frame=f)
            bp.keyframe_insert("location", frame=f)


class POV:
    """Ich-Kamera: Position/Blickziel über die Zeit, Handkamera-Wackeln, Atmen, Laufen."""

    def __init__(self, cam, seed=3):
        self.cam = cam
        self.keys_pos = []   # (t, pos, dur)
        self.keys_tgt = []
        self.keys_lens = []
        self.shake = 1.0
        self.run = []        # (t0, t1)
        self.seed = seed
        self.roll = []       # (t, grad, dur)
        self.linear = False  # True: Position gleichmäßig (Laufen)
        self.follow = None   # fn(t) -> Vector: Versatz (fahrendes Auto)

    def at(self, t, pos=None, target=None, dur=0.6, lens=None):
        if pos is not None:
            self.keys_pos.append((t, Vector(pos), dur))
        if target is not None:
            self.keys_tgt.append((t, Vector(target), dur))
        if lens is not None:
            self.keys_lens.append((t, lens, dur))

    def tilt(self, t, deg, dur=0.4):
        self.roll.append((t, deg, dur))

    def _val(self, lst, t, default, linear=False):
        lst = sorted(lst, key=lambda e: e[0])
        if not lst:
            return default
        cur = lst[0][1]
        for e in lst[1:]:
            if t < e[0]:
                break
            if linear:
                w = min(1.0, max(0.0, (t - e[0]) / max(e[2], 1e-3)))
            else:
                w = smooth(e[0], e[0] + max(e[2], 1e-3), t)
            cur = cur.lerp(e[1], w) if hasattr(cur, "lerp") else cur + (e[1] - cur) * w
        return cur

    def pose_at(self, t):
        p = self._val(self.keys_pos, t, self.cam.location.copy(), self.linear)
        g = self._val(self.keys_tgt, t, p + Vector((0, 1, 0)), self.linear)
        if self.follow is not None:
            off = self.follow(t)
            p, g = p + off, g + off
        lens = self._val(self.keys_lens, t, self.cam.data.lens)
        run = 0.0
        for (t0, t1) in self.run:
            run = max(run, min(smooth(t0, t0 + 0.3, t), 1 - smooth(t1 - 0.3, t1, t)))
        sh = self.shake
        p = p + Vector((0.004 * noise1(t, self.seed, 0.4) * sh, 0.004 * noise1(t, self.seed + 2, 0.35) * sh,
                        0.003 * math.sin(2 * math.pi * 0.27 * t) * sh))
        if run > 0:
            p = p + Vector((0.025 * math.sin(2 * math.pi * 1.5 * t) * run, 0, 0.04 * abs(math.sin(2 * math.pi * 1.5 * t))
                            * run))
        d = g - p
        q = d.to_track_quat("-Z", "Y")
        e = q.to_euler()
        e.rotate_axis("X", math.radians(0.5 * noise1(t, self.seed + 7, 0.5) * sh))
        e.rotate_axis("Y", math.radians(0.6 * noise1(t, self.seed + 9, 0.45) * sh))
        roll = 0.0
        if self.roll:
            roll = self._val([(e_[0], e_[1], e_[2]) for e_ in self.roll], t, 0.0)
        e.rotate_axis("Z", math.radians(roll + 2.5 * run * math.sin(2 * math.pi * 0.75 * t)))
        self.cam.location = p
        self.cam.rotation_euler = e
        self.cam.data.lens = lens

    def keys(self, f):
        self.cam.keyframe_insert("location", frame=f)
        self.cam.keyframe_insert("rotation_euler", frame=f)
        self.cam.data.keyframe_insert("lens", frame=f)

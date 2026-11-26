"""Baut die HyperFrames-Komposition für Tech-Lupe „Passwort“ aus build/timeline.json (Stimme) und build/mix.wav.
  python3 techlupe-passwort/build_comp.py   (vx-Umgebung wegen PIL für die Untertitelbreite)
schreibt index.html (Wurzel: Hintergrund, Szenen-Hosts, Untertitel-Host, Ton) und compositions/s01…s10.html + caps.html.
Regeln aus dem HyperFrames-Vertrag: jede Szene eine Datei mit <template>, eigene pausierte Zeitleiste unter ihrer id,
fromTo statt from, keine Zufallszahlen zur Laufzeit (Rauschen/Zähler hier vorberechnet), Schriften als @font-face.
Sichere Zone 9:16: Inhalt y 300–1040, Untertitel unten bis y 1240, x 120–780 (rechts die TikTok-Leiste).
"""
import hashlib
import html
import json
import os
import random

from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
tl = json.load(open(os.path.join(B, "timeline.json"), encoding="utf-8"))
SEG = {s["id"]: s for s in tl["segments"]}
D = round(tl["duration"], 3)
LEAD = 0.15                                    # Bild wechselt kurz vor dem Satz
HASH = hashlib.sha256(b"passwort123").hexdigest()
R = random.Random(6)
HEX = "0123456789abcdef"
os.makedirs(os.path.join(HERE, "compositions"), exist_ok=True)

FONTS = """
@font-face { font-family: 'TLNunito'; src: url('assets/fonts/TLNunito-900.woff2') format('woff2'); font-weight: 900; }
@font-face { font-family: 'TLFredoka'; src: url('assets/fonts/TLFredoka-700.woff2') format('woff2'); font-weight: 700; }
@font-face { font-family: 'TLMono'; src: url('assets/fonts/TLMono-Bold.ttf') format('truetype'); font-weight: 700; }
@font-face { font-family: 'TLEmoji'; src: url('assets/fonts/TLEmoji.ttf') format('truetype'); }
"""
BASE = FONTS + """
.abs { position: absolute; }
.card { position: absolute; background: #131B36; border: 3px solid rgba(255,255,255,.10); border-radius: 34px;
  box-shadow: 0 24px 60px rgba(0,0,0,.45); }
.lbl { font-family: 'TLFredoka', sans-serif; font-weight: 700; color: #8A93B2; font-size: 34px; letter-spacing: 2px; }
.big { font-family: 'TLFredoka', sans-serif; font-weight: 700; color: #F2F5FF; }
.mono { font-family: 'TLMono', monospace; font-weight: 700; }
.cy { color: #3DDCFF; } .ye { color: #FFC83A; } .rd { color: #FF4B5C; } .gr { color: #3DFF9A; } .mu { color: #8A93B2; }
.emo { font-family: 'TLEmoji', sans-serif; }
.stamp { font-family: 'TLFredoka', sans-serif; font-weight: 700; color: #fff; background: #FF4B5C; border: 8px solid #fff;
  border-radius: 20px; padding: 6px 30px 12px; font-size: 64px; white-space: nowrap; }
"""


def st(i):
    return SEG[i]["start"]


def en(i):
    return SEG[i]["speechEnd"]


def capt(i, k):
    c = SEG[i]["caps"]
    return c[k]["start"] if k < len(c) else st(i)


ORDER = [s["id"] for s in tl["segments"]]
SCENE = {}
for k, sid in enumerate(ORDER):
    a = 0.0 if k == 0 else round(st(sid) - LEAD, 3)
    b = D if k + 1 == len(ORDER) else round(st(ORDER[k + 1]) - LEAD, 3)
    SCENE[sid] = (a, b)


def scramble(n, final, keep=0):
    """n Zwischenstände eines Hex-Strings, die sich von links nach rechts auf den Endwert einpendeln (vorberechnet)."""
    out = []
    for j in range(n):
        fixed = int(len(final) * (j + 1) / n) if j >= keep else 0
        out.append(final[:fixed] + "".join(R.choice(HEX) for _ in range(len(final) - fixed)))
    return out


def hexlines(h, per=16):
    return "<br>".join(h[i:i + per] for i in range(0, len(h), per))


class Scene:
    def __init__(self, sid):
        self.sid, (self.a, self.b) = sid, SCENE[sid]
        self.dur = round(self.b - self.a, 3)
        self.html, self.css, self.js = [], [], []
        self.tweened = set()

    def t(self, x):                         # absolute Zeit → Szenenzeit
        return round(max(0.0, x - self.a), 3)

    def el(self, id_, inner, style, cls=""):
        extra = ' data-layout-allow-occlusion data-layout-allow-overlap data-layout-allow-overflow' if cls == "stamp" else ""
        pos = "" if "position:" in style else "position:absolute;"
        self.html.append(f'<div id="{self.sid}-{id_}" class="{cls}"{extra} style="{pos}{style}">{inner}</div>')
        return f"#{self.sid}-{id_}"

    def tw(self, sel, frm, to, at):
        if sel in self.tweened:
            to = dict(to, immediateRender=False)
        self.tweened.add(sel)
        self.js.append(f'tl.fromTo("{sel}", {json.dumps(frm)}, {json.dumps(to)}, {at:.3f});')

    def setv(self, sel, vals, at):
        self.js.append(f'tl.set("{sel}", {json.dumps(vals)}, {at:.3f});')

    def pop_in(self, sel, at, dur=0.45, y=40, scale=0.9):
        self.tw(sel, {"opacity": 0, "y": y, "scale": scale, "filter": "blur(6px)"},
                {"opacity": 1, "y": 0, "scale": 1, "filter": "blur(0px)", "duration": dur, "ease": "expo.out"}, at)

    def slam(self, sel, at, rot=-8):
        self.tw(sel, {"opacity": 0, "scale": 2.2, "rotation": rot},
                {"opacity": 1, "scale": 1, "rotation": rot, "duration": 0.32, "ease": "back.out(1.6)"}, at)

    def fade_out(self, sel, at, dur=0.2):
        self.tw(sel, {"opacity": 1}, {"opacity": 0, "duration": dur, "ease": "power2.in"}, at)

    def frames(self, base_id, texts, t0, t1, style, cls="mono"):
        """Mehrere übereinanderliegende Fassungen eines Texts, nacheinander sichtbar (Rauschen, Zähler)."""
        n = len(texts)
        for j, txt in enumerate(texts):
            sel = self.el(f"{base_id}{j}", txt, style + ";opacity:0", cls)
            on = t0 + (t1 - t0) * j / n
            self.setv(sel, {"opacity": 1}, round(on, 3))
            if j + 1 < n:
                self.setv(sel, {"opacity": 0}, round(t0 + (t1 - t0) * (j + 1) / n, 3))

    def write(self):
        body = "\n    ".join(self.html)
        js = "\n    ".join(self.js)
        doc = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    {BASE}
    {''.join(self.css)}
  </style>
  <div id="root" data-composition-id="{self.sid}" data-width="1080" data-height="1920">
    <div id="{self.sid}-wrap" class="clip" data-start="0" data-duration="{self.dur}" style="position:absolute;inset:0">
    {body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    window.__timelines["{self.sid}"] = tl;
  </script>
</template>
"""
        open(os.path.join(HERE, "compositions", f"{self.sid}.html"), "w", encoding="utf-8").write(doc)


# ---------------------------------------------------------------- Szenen
CX = 450                                   # Bildmitte der sicheren Zone (x 120–780)


def card(sc, id_, x, y, w, h, inner=""):
    return sc.el(id_, inner, f"left:{x}px;top:{y}px;width:{w}px;height:{h}px", "card")


# s01 Haken: Login und Datenbank – in der Datenbank steht ein Hash, nicht das Passwort
s = Scene("s01")
c1 = card(s, "login", 150, 300, 600, 330, f"""
  <div class="lbl" style="position:absolute;left:36px;top:26px">🌐 meinshop.de · ANMELDEN</div>
  <div class="mono mu" style="position:absolute;left:36px;top:96px;font-size:30px">E-Mail</div>
  <div class="mono" style="position:absolute;left:36px;top:134px;width:528px;height:62px;border-radius:14px;background:#0B1020;color:#F2F5FF;font-size:32px;line-height:62px;padding-left:20px">lisa@mail.de</div>
  <div class="mono mu" style="position:absolute;left:36px;top:212px;font-size:30px">Passwort</div>
  <div style="position:absolute;left:36px;top:250px;width:528px;height:62px;border-radius:14px;background:#0B1020"></div>""")
for j in range(10):                          # Punkte tippen sich hinein
    sel = s.el(f"dot{j}", "•", f"left:{206 + j * 30}px;top:552px;font-size:44px;color:#F2F5FF;opacity:0", "mono")
    s.setv(sel, {"opacity": 1}, round(0.05 + j * 0.06, 3))
c2 = card(s, "db", 150, 670, 600, 330, f"""
  <div class="lbl" style="position:absolute;left:36px;top:26px">🗄️ DATENBANK</div>
  <div class="mono mu" style="position:absolute;left:36px;top:92px;font-size:28px">nutzer</div>
  <div class="mono mu" style="position:absolute;left:230px;top:92px;font-size:28px">passwort?</div>
  <div class="mono" style="position:absolute;left:36px;top:138px;font-size:34px;color:#F2F5FF">lisa</div>
  <div class="mono ye" style="position:absolute;left:230px;top:138px;font-size:27px;line-height:1.25">{hexlines(HASH[:48], 16)}…</div>""")
s.tw(c2, {"scale": 1.0}, {"scale": 1.03, "duration": 0.5, "ease": "power2.out"}, 0.0)
st1 = s.el("stamp", "KENNT ES NICHT", "left:200px;top:610px", "stamp")
s.slam(st1, s.t(capt("s01", 1)) + 0.25, -7)
s.write()

# s02 Fingerabdruck → Hash
s = Scene("s02")
fp = "".join(f'<circle cx="160" cy="180" r="{r}" fill="none" stroke="#3DDCFF" stroke-width="10" stroke-dasharray="{d}" stroke-linecap="round" opacity="{0.35 + 0.08 * k}"/>'
             for k, (r, d) in enumerate([(30, "40 20"), (55, "90 30"), (80, "120 40"), (105, "150 30"), (130, "200 45")]))
g = s.el("fp", f'<svg width="320" height="360" viewBox="0 0 320 360">{fp}</svg>', "left:290px;top:310px")
s.tw(g, {"opacity": 0, "scale": 0.6, "rotation": -20}, {"opacity": 1, "scale": 1, "rotation": 0, "duration": 0.7, "ease": "expo.out"}, 0.0)
l1 = s.el("l1", "FINGERABDRUCK", "left:120px;top:676px;width:660px;text-align:center;font-size:58px;line-height:1", "big cy")
s.pop_in(l1, s.t(capt("s02", 1)) - 0.05)
hb = card(s, "hb", 150, 800, 600, 190, f'<div class="mono ye" style="position:absolute;left:34px;top:26px;font-size:34px;line-height:1.3">{hexlines(HASH[:48], 16)}…</div>')
s.pop_in(hb, s.t(capt("s02", 2)) - 0.1, 0.45, 30)
l2 = s.el("l2", "= HASH", "left:560px;top:745px;font-size:56px", "big ye")
s.slam(l2, s.t(capt("s02", 2)) + 0.25, 6)
s.write()

# s03 Hash-Maschine: passwort123 → SHA-256 → immer derselbe Wert
s = Scene("s03")
inp = card(s, "in", 230, 300, 440, 100, '<div class="mono" style="position:absolute;inset:0;text-align:center;line-height:104px;font-size:48px;color:#F2F5FF">passwort123</div>')
s.pop_in(inp, 0.0, 0.4, 20)
ar = s.el("ar1", "↓", "left:420px;top:395px;font-size:72px;color:#8A93B2", "big")
s.pop_in(ar, 0.2, 0.3, -20, 1)
gear = '<svg width="120" height="120" viewBox="-60 -60 120 120"><g fill="#3DDCFF">' + "".join(
    f'<rect x="-9" y="-58" width="18" height="26" rx="4" transform="rotate({a})"/>' for a in range(0, 360, 45)) + \
    '<circle r="36"/><circle r="15" fill="#131B36"/></g></svg>'
mac = card(s, "mac", 200, 480, 500, 160, f'<div class="lbl" style="position:absolute;left:186px;top:30px;color:#3DDCFF">HASH-</div><div class="lbl" style="position:absolute;left:186px;top:76px;color:#3DDCFF">MASCHINE</div><div class="mono mu" style="position:absolute;left:186px;top:118px;font-size:28px">SHA-256</div>')
s.pop_in(mac, 0.15, 0.45, 30)
gr_ = s.el("gear", gear, "left:236px;top:500px")
s.tw(gr_, {"rotation": 0}, {"rotation": 540, "duration": max(1.0, s.dur - 0.3), "ease": "none"}, 0.1)
ar2 = s.el("ar2", "↓", "left:420px;top:632px;font-size:72px;color:#8A93B2", "big")
s.pop_in(ar2, 0.9, 0.3, -20, 1)
outc = card(s, "out", 150, 720, 600, 230)
s.pop_in(outc, 0.95, 0.35, 20)
t0 = 1.05
s.frames("hx", [hexlines(x, 16) for x in scramble(12, HASH)], t0, t0 + 1.0,
         "left:190px;top:744px;font-size:36px;line-height:1.3;color:#FFC83A")
again = s.el("again", "✓ JEDES MAL GLEICH", "left:120px;top:968px;width:660px;text-align:center;font-size:46px", "big gr")
s.pop_in(again, s.t(capt("s03", 2)) + 0.1)
s.write()

# s04 Einbahnstraße: zurückrechnen geht nicht
s = Scene("s04")
hb = card(s, "h", 150, 300, 600, 160, f'<div class="mono ye" style="position:absolute;left:34px;top:24px;font-size:32px;line-height:1.3">{hexlines(HASH[:32], 16)}…</div>')
s.pop_in(hb, 0.0, 0.35, 20)
back = s.el("back", "↑ ZURÜCK ZU „passwort123“?", "left:120px;top:500px;width:660px;text-align:center;font-size:40px;color:#F2F5FF", "big")
s.pop_in(back, 0.15)
x_ = s.el("x", "✕", "left:375px;top:430px;font-size:190px;color:#FF4B5C", "big")
s.slam(x_, s.t(capt("s04", 1)) - 0.05, 0)
sign = s.el("sign", '<div style="width:560px;height:200px;border-radius:24px;background:#1E5BD8;border:10px solid #fff;display:flex;align-items:center;justify-content:center;gap:24px"><span style="font-size:110px;color:#fff;line-height:1">➜</span><span class="big" style="font-size:52px;color:#fff;line-height:1.05">EINBAHN-<br>STRASSE</span></div>',
            "left:160px;top:760px")
s.tw(sign, {"opacity": 0, "x": -500}, {"opacity": 1, "x": 0, "duration": 0.55, "ease": "expo.out"}, s.t(capt("s04", 2)) - 0.1)
s.write()

# s05 Login-Vergleich: Eingabe wieder hashen und vergleichen
s = Scene("s05")
li = card(s, "li", 150, 300, 600, 120, '<div class="lbl" style="position:absolute;left:30px;top:16px">DEINE EINGABE</div><div class="mono" style="position:absolute;left:30px;top:56px;font-size:40px;color:#F2F5FF">passwort123</div>')
s.pop_in(li, 0.0, 0.35, 20)
a1 = card(s, "a1", 150, 470, 600, 150, f'<div class="lbl" style="position:absolute;left:30px;top:14px;color:#3DDCFF">NEU GEHASHT</div><div class="mono cy" style="position:absolute;left:30px;top:58px;font-size:30px;line-height:1.3">{hexlines(HASH[:32], 16)}…</div>')
s.pop_in(a1, s.t(capt("s05", 0)) + 0.7, 0.4, 20)
b1 = card(s, "b1", 150, 660, 600, 150, f'<div class="lbl" style="position:absolute;left:30px;top:14px;color:#FFC83A">GESPEICHERT</div><div class="mono ye" style="position:absolute;left:30px;top:58px;font-size:30px;line-height:1.3">{hexlines(HASH[:32], 16)}…</div>')
s.pop_in(b1, s.t(capt("s05", 1)) - 0.1, 0.4, 20)
eq = s.el("eq", "=", "left:768px;top:560px;font-size:110px;color:#3DFF9A", "big")
s.slam(eq, s.t(capt("s05", 2)) - 0.05, 0)
ok = s.el("ok", '<div style="width:600px;height:150px;border-radius:30px;background:#123D2A;border:6px solid #3DFF9A;display:flex;align-items:center;justify-content:center;gap:20px"><span class="emo" style="font-size:76px">🔓</span><span class="big gr" style="font-size:64px">DU BIST DRIN</span></div>',
          "left:150px;top:860px")
s.pop_in(ok, s.t(capt("s05", 3)) - 0.05, 0.45, 30)
s.write()

# s06 Datenleck: Hashes fliegen raus, Wortliste wird durchprobiert
s = Scene("s06")
rows = "".join(f'<div class="mono ye" style="font-size:26px;line-height:44px">{u:<6} {"".join(R.choice(HEX) for _ in range(20))}…</div>' for u in ("lisa", "tom", "ali", "mia", "ben"))
db = card(s, "db", 150, 300, 600, 330, f'<div class="lbl" style="position:absolute;left:30px;top:20px">🗄️ DATENBANK</div><div style="position:absolute;left:30px;top:70px">{rows}</div>')
s.pop_in(db, 0.0, 0.3, 10)
s.tw(db, {"x": 0, "rotation": 0}, {"x": 14, "rotation": -2, "duration": 0.06, "ease": "none", "yoyo": True, "repeat": 5}, 0.35)
leak = s.el("leak", "DATENLECK!", "left:225px;top:560px", "stamp")
s.slam(leak, s.t(capt("s06", 1)) + 0.05, -6)
s.fade_out(db, s.t(capt("s06", 2)) - 0.2, 0.25)
s.fade_out(leak, s.t(capt("s06", 2)) - 0.2, 0.25)
wl = ["123456", "hallo", "schatz", "qwertz", "passwort", "hallo123", "fussball", "passwort123"]
t_list = s.t(capt("s06", 2))
t_end = s.t(en("s06"))
step = max(0.25, (t_end - t_list - 0.4) / len(wl))
lab = s.el("wl", "WORTLISTE AUS ALTEN LECKS", "left:120px;top:320px;width:660px;text-align:center;font-size:38px", "lbl")
s.pop_in(lab, t_list, 0.3, 10)
for j, w in enumerate(wl):
    hit = w == "passwort123"
    sel = s.el(f"w{j}", f'{html.escape(w)} <span class="{"gr" if hit else "rd"}">{"✓ TREFFER" if hit else "✕"}</span>',
               f"left:170px;top:{390 + j * 74}px;font-size:40px;color:#F2F5FF;opacity:0", "mono")
    s.tw(sel, {"opacity": 0, "x": -40}, {"opacity": 1, "x": 0, "duration": 0.22, "ease": "power3.out"}, round(t_list + 0.25 + j * step, 3))
s.write()

# s07 Grafikkarte: Milliarden Versuche pro Sekunde
s = Scene("s07")
fans = "".join(f'<g transform="translate({cx},70)"><circle r="52" fill="#0B1020" stroke="#3DDCFF" stroke-width="5"/>'
               f'<g id="s07-fan{k}">' + "".join(f'<path d="M0 0 L12 -46 A46 46 0 0 1 40 -22 Z" fill="#3DDCFF" opacity=".75" transform="rotate({a})"/>' for a in (0, 90, 180, 270)) + "</g></g>"
               for k, cx in enumerate((110, 250, 390)))
gpu = s.el("gpu", f'<svg width="500" height="160" viewBox="0 0 500 160"><rect x="4" y="4" width="492" height="132" rx="20" fill="#131B36" stroke="rgba(255,255,255,.2)" stroke-width="4"/>{fans}<rect x="30" y="136" width="300" height="16" fill="#FFC83A"/></svg>',
            "left:200px;top:320px")
s.pop_in(gpu, 0.0, 0.45, 30)
for k, cx in enumerate((110, 250, 390)):
    s.tw(f"#s07-fan{k}", {"rotation": 0, "svgOrigin": f"{cx} 70"}, {"rotation": 1440, "duration": max(1.0, s.dur), "ease": "none", "svgOrigin": f"{cx} 70"}, 0.0)
vals = [int(22_000_000_000 * (j / 23) ** 3) for j in range(24)]
texts = [f"{v:,}".replace(",", ".") for v in vals]
tc = s.t(capt("s07", 1)) - 0.2
s.frames("cnt", texts, tc, tc + 1.2, "left:120px;top:560px;width:660px;text-align:center;font-size:60px;color:#FF4B5C", "mono")
per = s.el("per", "VERSUCHE PRO SEKUNDE", "left:120px;top:660px;width:660px;text-align:center;font-size:40px", "lbl")
s.pop_in(per, tc + 0.2, 0.3, 10)
mrd = s.el("mrd", "MILLIARDEN", "left:250px;top:780px", "stamp")
s.slam(mrd, s.t(capt("s07", 2)) - 0.1, -5)
s.write()

# s08 Kurz = sofort geknackt; überall gleich = alle Konten offen
s = Scene("s08")
pw = card(s, "pw", 200, 300, 500, 120, '<div class="mono" style="position:absolute;inset:0;text-align:center;line-height:114px;font-size:52px;color:#F2F5FF">hallo1</div>')
s.pop_in(pw, 0.0, 0.35, 20)
tim = s.el("tim", "⏱ GEKNACKT IN UNTER 1 SEKUNDE", "left:120px;top:450px;width:660px;text-align:center;font-size:40px", "big rd")
s.pop_in(tim, s.t(capt("s08", 1)) - 0.05, 0.3, 10)
apps = [("📧", "MAIL"), ("🛒", "SHOP"), ("💬", "CHAT"), ("🏦", "BANK")]
ta = s.t(capt("s08", 3)) - 0.1
for j, (ic, nm) in enumerate(apps):
    x0 = 130 + j * 165
    tile = s.el(f"app{j}", f'<div style="width:150px;height:190px;border-radius:28px;background:#131B36;border:3px solid rgba(255,255,255,.12);text-align:center"><div class="emo" style="font-size:66px;padding-top:18px">{ic}</div><div class="lbl" style="font-size:28px;margin-top:6px;color:#F2F5FF">{nm}</div></div>',
                f"left:{x0}px;top:600px")
    s.pop_in(tile, s.t(capt("s08", 2)) + j * 0.08, 0.35, 30)
    lk = s.el(f"lock{j}", "🔒", f"left:{x0 + 50}px;top:810px;font-size:56px", "emo")
    s.pop_in(lk, s.t(capt("s08", 2)) + 0.1 + j * 0.08, 0.3, 10)
    s.fade_out(lk, ta + j * 0.2, 0.08)
    ul = s.el(f"unl{j}", "🔓", f"left:{x0 + 50}px;top:810px;font-size:56px;opacity:0", "emo")
    s.slam(ul, ta + j * 0.2, 0)
s.write()

# s09 Lösung: lang, für jede Seite eigenes, Passwort-Manager
s = Scene("s09")
items = [("✔", "LANG", "kaffee-regen-tiger-lampe", 0), ("✔", "FÜR JEDE SEITE EIGENES", "", 1)]
y0 = 310
it1 = card(s, "i1", 150, 300, 600, 170, '<div class="big gr" style="position:absolute;left:30px;top:16px;font-size:46px">✔ LANG</div><div class="mono" style="position:absolute;left:30px;top:90px;font-size:32px;color:#F2F5FF">kaffee-regen-tiger-lampe</div>')
s.pop_in(it1, 0.0, 0.4, 20)
it2 = card(s, "i2", 150, 500, 600, 220, '<div class="big gr" style="position:absolute;left:30px;top:16px;font-size:46px">✔ JEDE SEITE EIGENES</div>'
           '<div class="mono" style="position:absolute;left:30px;top:86px;font-size:28px;line-height:1.45;color:#F2F5FF">📧 h7#Kq…  🛒 m2!Zx…<br>💬 Tr9$pa…  🏦 V4%dLw…</div>')
s.pop_in(it2, s.t(capt("s09", 1)) - 0.1, 0.4, 20)
vault = s.el("vault", '<div style="width:600px;height:200px;border-radius:30px;background:#2A2150;border:6px solid #B79CFF;display:flex;align-items:center;justify-content:center;gap:22px"><span class="emo" style="font-size:90px">🔐</span><span class="big" style="font-size:52px;color:#fff;line-height:1.05">PASSWORT-<br>MANAGER</span></div>',
             "left:150px;top:760px")
s.pop_in(vault, s.t(capt("s09", 2)) - 0.1, 0.5, 40, 0.85)
s.write()

# s10 Abschluss: Logo, folgen, Themenfrage
s = Scene("s10")
logo = s.el("logo", '<span class="emo" style="font-size:120px">🔍</span><br><span class="big" style="font-size:96px;color:#F2F5FF">TECH-<span class="cy">LUPE</span></span>',
            "left:120px;top:330px;width:660px;text-align:center;line-height:1.1")
s.pop_in(logo, 0.0, 0.5, 30, 0.8)
fol = s.el("fol", '<div style="display:inline-block;background:#FF4B5C;color:#fff;border-radius:999px;padding:18px 54px" class="big">+ FOLGEN</div>',
           "left:120px;top:690px;width:660px;text-align:center;font-size:56px")
s.slam(fol, 0.45, 0)
q = card(s, "q", 150, 840, 600, 150, '<div class="big" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;font-size:40px;color:#F2F5FF;line-height:1.15">Welches Thema als Nächstes?<br><span class="ye">Schreib’s in die Kommentare 👇</span></div>')
s.pop_in(q, 0.9, 0.45, 30)
s.write()

# ---------------------------------------------------------------- Untertitel (eine Datei, alle Gruppen)
NUN = os.environ["TL_NUNITO_TTF"]           # Nunito 900 als TTF (aus der woff2 umgewandelt) nur zum Messen der Breite
fnt = {}


def width(txt, size):
    if size not in fnt:
        fnt[size] = ImageFont.truetype(NUN, size)
    return fnt[size].getlength(txt)


def fit(words, maxw=640):
    for size in range(84, 50, -2):
        lines, cur = [], []
        for w, sty in words:
            trial = " ".join(x for x, _ in cur + [(w, sty)])
            if cur and width(trial, size) > maxw:
                lines.append(cur)
                cur = [(w, sty)]
            else:
                cur.append((w, sty))
        lines.append(cur)
        if len(lines) <= 2 and all(width(" ".join(x for x, _ in ln), size) <= maxw for ln in lines):
            return size, lines
    return 50, [words]


cap_html, cap_js = [], []
k = 0
for seg in tl["segments"]:
    caps = seg["caps"]
    for i, c in enumerate(caps):
        a = c["start"] + (0.12 if c["start"] < 0.1 else 0.0)
        b = caps[i + 1]["start"] if i + 1 < len(caps) else seg["speechEnd"] + 0.25
        size, lines = fit(c["words"])
        col = {"g": "#FFC83A", "r": "#FF4B5C", "y": "#FFC83A"}
        inner = "<br>".join(" ".join(f'<span style="color:{col[s_]}">{html.escape(w)}</span>' if s_ in col else html.escape(w)
                                     for w, s_ in ln) for ln in lines)
        cap_html.append(f'<div id="cap{k}" class="capg" style="font-size:{size}px;opacity:0">{inner}</div>')
        cap_js.append(f'tl.fromTo("#cap{k}", {{"opacity": 0, "y": 16, "scale": 0.96}}, {{"opacity": 1, "y": 0, "scale": 1, "duration": 0.12, "ease": "power3.out"}}, {a:.3f});')
        cap_js.append(f'tl.to("#cap{k}", {{"opacity": 0, "duration": 0.1, "ease": "power2.in"}}, {max(a + 0.15, b - 0.1):.3f});')
        cap_js.append(f'tl.set("#cap{k}", {{"opacity": 0, "visibility": "hidden"}}, {b:.3f});')
        k += 1
open(os.path.join(HERE, "compositions", "caps.html"), "w", encoding="utf-8").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    {FONTS}
    .capg {{ position: absolute; left: 120px; width: 660px; bottom: 680px; text-align: center; overflow: visible;
      font-family: 'TLNunito', 'TLEmoji', sans-serif; font-weight: 900; color: #fff; line-height: 1.06; letter-spacing: 1px;
      text-shadow: 0 6px 0 rgba(0,0,0,.55), 0 0 18px rgba(0,0,0,.6); -webkit-text-stroke: 3px #0B1020; paint-order: stroke fill; }}
  </style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920">
    <div id="caps-wrap" class="clip" data-start="0" data-duration="{D}" style="position:absolute;inset:0">
    {chr(10).join('    ' + h for h in cap_html)}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in cap_js)}
    window.__timelines["caps"] = tl;
  </script>
</template>
""")

# ---------------------------------------------------------------- Wurzel
hosts = []
for k, sid in enumerate(ORDER):
    a, b = SCENE[sid]
    hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{a}" '
                 f'data-duration="{round(b - a, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1920" />' for x in range(0, 1081, 90)) + \
       "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" />' for y in range(0, 1921, 90))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>
      {FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0B1020; }}
      #bg {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 35%, #16224A 0%, #0B1020 60%, #070A14 100%); }}
      #bg svg {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <div id="bg"><svg width="1080" height="1920"><g stroke="rgba(61,220,255,.06)" stroke-width="2">{grid}</g></svg></div>
      {chr(10).join('      ' + h for h in hosts)}
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{D}"
        data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{D}" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print(f"Komposition: {D:.1f} s, {len(ORDER)} Szenen, {len(cap_html)} Untertitel-Gruppen")

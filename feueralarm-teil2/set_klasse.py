"""Klassenzimmer 204 (2. Stock) mit Blick auf den Schulhof (Sammelplatz, Feuerwehr).

Koordinaten: Boden z=0, Tafel vorn bei y=+6, Fenster links (x=-4), Flurtür rechts (x=+4).
Sitzplätze: Spalten x = -2.55 / 0 / 2.55 (Doppeltische), Reihen y = 3.2 / 1.6 / 0.0 / -1.6.
Noah (Kamera) sitzt Fensterreihe, Reihe 3, Gangplatz; Ben am Fenster daneben; Lina vor Ben (Platz vor Noah frei).
"""
import math
import os

import toon as T
from figur import _hash

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")

COLS = (-2.55, 0.0, 2.55)
ROWS = (3.2, 1.6, 0.0, -1.6)
SEAT_DX = 0.33
NOAH = (COLS[0] + SEAT_DX, ROWS[2])
BEN = (COLS[0] - SEAT_DX, ROWS[2])
LINA = (COLS[0] - SEAT_DX, ROWS[1])      # vor Ben (Fensterplatz Reihe 2); Platz vor Noah bleibt frei
FREI = [(COLS[0] + SEAT_DX, ROWS[1]),                       # vor Noah
        (COLS[1] - SEAT_DX, ROWS[2]), (COLS[1] + SEAT_DX, ROWS[2]),  # Sichtlinie zur Flurtür frei
        (COLS[1] - SEAT_DX, ROWS[1]), (COLS[2] - SEAT_DX, ROWS[0])]
NOAH_EYE = (COLS[0] + SEAT_DX, ROWS[2] - 0.02, 1.24)
PULT = (-1.5, 4.75)
FLURTUER = (3.98, 4.55)
VORB_TUER = (-3.0, 5.98)
LAUTSPRECHER = (2.6, 5.93, 2.62)
GROUND = -6.8


def tex(name):
    return os.path.join(A, name)


def tisch(x, y, mats, line=0.007, name=None):
    n = name or f"tisch_{x:.2f}_{y:.2f}"
    T.box(f"{n}_platte", (1.3, 0.55, 0.035), mats["platte"], loc=(x, y, 0.73), line=line, bevel=0.008)
    T.box(f"{n}_zarge", (1.22, 0.04, 0.10), mats["metall"], loc=(x, y + 0.24, 0.66), line=line * 0.8)
    for dx in (-0.6, 0.6):
        for dy in (-0.22, 0.22):
            T.cylinder(f"{n}_bein_{dx}_{dy}", 0.017, 0.71, mats["metall"], loc=(x + dx, y + dy, 0.355), line=line * 0.7,
                       segs=8)


def stuhl(x, y, mats, rot=0, line=0.006, name=None):
    n = name or f"stuhl_{x:.2f}_{y:.2f}"
    e = T.empty(n, (x, y, 0))
    e.rotation_euler[2] = math.radians(rot)
    T.box(f"{n}_sitz", (0.42, 0.40, 0.03), mats["stuhl"], loc=(0, 0, 0.45), parent=e, line=line, bevel=0.012)
    T.box(f"{n}_lehne", (0.42, 0.03, 0.26), mats["stuhl"], loc=(0, -0.21, 0.74), parent=e, line=line, bevel=0.012)
    for dx in (-0.18, 0.18):
        for dy in (-0.17, 0.17):
            T.cylinder(f"{n}_bein_{dx}_{dy}", 0.011, 0.45, mats["metall"], loc=(dx, dy, 0.225), parent=e, line=line * 0.6,
                       segs=8)
        T.cylinder(f"{n}_holm_{dx}", 0.011, 0.30, mats["metall"], loc=(dx, -0.205, 0.6), parent=e, line=line * 0.6, segs=8)
    return e


def kram(x, y, mats, k):
    """Hefte, Federmäppchen, Flaschen auf den Tischen (deterministisch gestreut)."""
    h = _hash("kram", k)
    if h < 0.75:
        o = T.box(f"heft_{k}", (0.21, 0.29, 0.008), mats["heft"][k % len(mats["heft"])],
                  loc=(x + (h - 0.4) * 0.6, y - 0.05, 0.752), line=0.003)
        o.rotation_euler[2] = math.radians(-20 + 40 * _hash("kram", k + 7))
    if _hash("kram", k + 3) < 0.5:
        T.box(f"etui_{k}", (0.2, 0.07, 0.05), mats["etui"][k % len(mats["etui"])],
              loc=(x + 0.35 * (_hash("kram", k + 5) - 0.5), y + 0.12, 0.775), line=0.003, bevel=0.015)
    if _hash("kram", k + 9) < 0.35:
        T.cylinder(f"flasche_{k}", 0.035, 0.22, mats["flasche"], loc=(x - 0.45, y + 0.15, 0.86), line=0.003, segs=16)


def build(people=True, outside=True, line=0.009):
    M = dict(
        boden=T.mat("Linoleum", "#b9ad97"), wand=T.mat("Wand", "#f0e8d6"), wand2=T.mat("Wandsockel", "#c9d6cf"),
        decke=T.mat("Decke", "#f4f2ec"), platte=T.mat("Tischplatte", "#dcc196"), metall=T.mat("Metall", "#5d6672"),
        stuhl=T.mat("Stuhl", "#3d6fb0"), rahmen=T.mat("Fensterrahmen", "#f6f6f2"), holz=T.mat("Tuerholz", "#b98a55"),
        heizung=T.mat("Heizung", "#eeeeea"), lampe=T.mat("Lampe", "#fffdf2"), pult=T.mat("Pult", "#a8794a"),
        dunkel=T.mat("Dunkel", "#2b2f36"), regal=T.mat("Regal", "#c79c69"),
        heft=[T.mat("Heft1", "#e85d5d"), T.mat("Heft2", "#4d8fe0"), T.mat("Heft3", "#f2d14b"), T.mat("Heft4", "#5bc27a")],
        etui=[T.mat("Etui1", "#6b4fb3"), T.mat("Etui2", "#e07a2f"), T.mat("Etui3", "#2d2d2d")],
        flasche=T.mat("Flasche", "#7fc7e8"),
    )
    W0, W1, Y0, Y1, H = -4.0, 4.0, -3.0, 6.0, 3.1
    T.box("boden", (W1 - W0, Y1 - Y0, 0.1), M["boden"], loc=(0, (Y0 + Y1) / 2, -0.05), line=0)
    T.box("decke", (W1 - W0, Y1 - Y0, 0.1), M["decke"], loc=(0, (Y0 + Y1) / 2, H + 0.05), line=0)
    # Wände: vorn mit Tafel, rechts mit Tür, hinten, links mit Fenstern
    T.box("wand_vorn", (W1 - W0, 0.2, H), M["wand"], loc=(0, Y1 + 0.1, H / 2), line=0)
    T.box("wand_hinten", (W1 - W0, 0.2, H), M["wand"], loc=(0, Y0 - 0.1, H / 2), line=0)
    # rechte Wand mit Türöffnung bei y=4.55 (Breite 1.0, Höhe 2.1)
    ty = FLURTUER[1]
    T.box("wand_rechts_a", (0.2, ty - 0.5 - Y0, H), M["wand"], loc=(W1 + 0.1, (Y0 + ty - 0.5) / 2, H / 2), line=0)
    T.box("wand_rechts_b", (0.2, Y1 - ty - 0.5, H), M["wand"], loc=(W1 + 0.1, (ty + 0.5 + Y1) / 2, H / 2), line=0)
    T.box("wand_rechts_c", (0.2, 1.0, H - 2.1), M["wand"], loc=(W1 + 0.1, ty, 2.1 + (H - 2.1) / 2), line=0)
    # linke Wand: Brüstung, Sturz, Pfeiler zwischen 3 Fenstern
    wins = (-1.55, 1.15, 3.85)
    T.box("wand_links_unten", (0.2, Y1 - Y0, 0.9), M["wand"], loc=(W0 - 0.1, (Y0 + Y1) / 2, 0.45), line=0)
    T.box("wand_links_oben", (0.2, Y1 - Y0, H - 2.55), M["wand"], loc=(W0 - 0.1, (Y0 + Y1) / 2, 2.55 + (H - 2.55) / 2),
          line=0)
    edges = [Y0] + [e for c in wins for e in (c - 0.95, c + 0.95)] + [Y1]
    for k in range(0, len(edges), 2):
        a, b = edges[k], edges[k + 1]
        if b - a > 0.01:
            T.box(f"pfeiler_{k}", (0.2, b - a, 1.65), M["wand"], loc=(W0 - 0.1, (a + b) / 2, 0.9 + 0.825), line=0)
    for i, c in enumerate(wins):
        for dy in (-0.95, 0.0, 0.95):
            T.box(f"fenster_pfosten_{i}_{dy}", (0.12, 0.07, 1.65), M["rahmen"], loc=(W0 + 0.02, c + dy, 1.725), line=0.006)
        for z in (0.93, 2.52):
            T.box(f"fenster_riegel_{i}_{z}", (0.12, 1.9, 0.07), M["rahmen"], loc=(W0 + 0.02, c, z), line=0.006)
        T.box(f"fensterbank_{i}", (0.30, 1.95, 0.04), M["rahmen"], loc=(W0 + 0.1, c, 0.9), line=0.006)
        T.box(f"griff_{i}", (0.04, 0.03, 0.12), M["metall"], loc=(W0 + 0.09, c + 0.08, 1.5), line=0.003)
        # Heizkörper unter dem Fenster
        for r in range(9):
            T.box(f"heizung_{i}_{r}", (0.08, 0.08, 0.5), M["heizung"], loc=(W0 + 0.12, c - 0.6 + r * 0.15, 0.45),
                  line=0.004, bevel=0.02)
    # Sockelleiste
    T.box("sockel_hinten", (W1 - W0, 0.04, 0.1), M["wand2"], loc=(0, Y0 + 0.02, 0.05), line=0)
    # Tafel mit Rahmen und Ablage
    T.box("tafel_rahmen", (3.8, 0.06, 1.32), M["metall"], loc=(0.3, Y1 - 0.03, 1.56), line=0.008)
    T.plane("tafel", (3.66, 1.2), T.mat("Tafelbild", "#2c5442", tex=tex("tafel.png")), loc=(0.3, Y1 - 0.065, 1.56))
    T.box("kreideablage", (3.7, 0.12, 0.04), M["metall"], loc=(0.3, Y1 - 0.1, 0.92), line=0.005)
    T.box("kreide", (0.09, 0.02, 0.02), T.mat("Kreide", "#ffffff"), loc=(-0.6, Y1 - 0.12, 0.95), line=0.002)
    T.box("schwamm", (0.14, 0.07, 0.05), T.mat("Schwamm", "#e9c54a"), loc=(1.1, Y1 - 0.12, 0.965), line=0.003,
          bevel=0.01)
    # Uhr, Lautsprecher, Schilder
    uhr = T.cylinder("uhr_rand", 0.2, 0.05, M["dunkel"], loc=(-1.3, Y1 - 0.03, 2.62), axis="Y", line=0.006, segs=32)
    T.plane("uhr", (0.28, 0.28), T.mat("Uhrbild", "#ffffff", tex=tex("uhr.png")), loc=(-1.3, Y1 - 0.06, 2.62))
    lx, ly, lz = LAUTSPRECHER
    T.box("lautsprecher", (0.40, 0.14, 0.30), T.mat("Lautsprechergehaeuse", "#e3e1dc"), loc=(lx, ly - 0.02, lz),
          line=0.008, bevel=0.015)
    T.plane("lautsprecher_gitter", (0.26, 0.24), T.mat("Gitter", "#cccccc", tex=tex("lautsprecher.png")),
            loc=(lx, ly - 0.095, lz))
    # Lautstärkeregler mit Kabel (erreichbar, Frau Sander dreht ihn ab)
    T.box("regler", (0.16, 0.08, 0.2), T.mat("Regler", "#e3e1dc"), loc=(lx + 0.5, ly - 0.0, 2.0), line=0.006, bevel=0.01)
    T.cylinder("regler_knopf", 0.035, 0.04, T.mat("Knopf_rot", "#c0392b"), loc=(lx + 0.5, ly - 0.06, 2.02), axis="Y",
               line=0.003)
    k = T.cylinder("lautsprecher_kabel", 0.008, 0.7, T.mat("Kabel", "#efefef"), loc=(lx + 0.33, ly - 0.02, 2.35),
                   line=0.003, segs=8)
    k.rotation_euler[1] = math.radians(-40)
    # Vorbereitungsraum-Tür hinter dem Pult (vordere Wand, links)
    vx, vy = VORB_TUER
    T.box("vorb_zarge", (1.12, 0.08, 2.16), M["metall"], loc=(vx, Y1 - 0.02, 1.08), line=0.007)
    T.box("vorb_tuer", (1.0, 0.06, 2.08), M["holz"], loc=(vx, Y1 - 0.05, 1.04), line=0.008)
    T.cylinder("vorb_klinke", 0.012, 0.13, M["metall"], loc=(vx + 0.38, Y1 - 0.11, 1.05), axis="X", line=0.003)
    T.plane("vorb_schild", (0.42, 0.11), T.mat("Vorbschild", "#ffffff", tex=tex("schild_vorb.png")),
            loc=(vx, Y1 - 0.085, 1.72))
    # Flurtür (rechte Wand) mit Glasstreifen, drehbar am Scharnier
    fx, fy = FLURTUER
    T.box("flur_zarge_a", (0.12, 0.06, 2.12), M["metall"], loc=(fx - 0.03, fy - 0.53, 1.06), line=0.007)
    T.box("flur_zarge_b", (0.12, 0.06, 2.12), M["metall"], loc=(fx - 0.03, fy + 0.53, 1.06), line=0.007)
    T.box("flur_zarge_c", (0.12, 1.1, 0.06), M["metall"], loc=(fx - 0.03, fy, 2.13), line=0.007)
    scharnier = T.empty("flurtuer_angel", (fx - 0.04, fy + 0.5, 0))
    T.box("flurtuer_blatt_a", (0.05, 1.0, 1.25), M["holz"], loc=(0, -0.5, 0.625), parent=scharnier, line=0.008)
    T.box("flurtuer_blatt_b", (0.05, 1.0, 0.25), M["holz"], loc=(0, -0.5, 1.975), parent=scharnier, line=0.008)
    T.box("flurtuer_blatt_c", (0.05, 0.62, 0.6), M["holz"], loc=(0, -0.69, 1.55), parent=scharnier, line=0.008)
    T.box("flurtuer_blatt_d", (0.05, 0.1, 0.6), M["holz"], loc=(0, -0.05, 1.55), parent=scharnier, line=0.008)
    T.box("flurtuer_glasrahmen", (0.06, 0.3, 0.62), M["metall"], loc=(0, -0.23, 1.55), parent=scharnier, line=0.006)
    T.cylinder("flurtuer_klinke", 0.012, 0.14, M["metall"], loc=(-0.07, -0.9, 1.05), parent=scharnier, axis="Y",
               line=0.003)
    T.box("flurtuer_schloss", (0.03, 0.06, 0.12), M["metall"], loc=(-0.035, -0.9, 0.93), parent=scharnier, line=0.003)
    T.plane("notausgang", (0.55, 0.2), T.mat("Notausgangbild", "#16964f", tex=tex("notausgang.png")),
            loc=(W1 - 0.01, fy, 2.42), rot=(90, 0, -90))
    T.plane("fluchtplan", (0.42, 0.59), T.mat("Fluchtplanbild", "#ffffff", tex=tex("fluchtplan.png")),
            loc=(W1 - 0.01, fy - 1.1, 1.55), rot=(90, 0, -90))
    # Plakate rechte Wand + Pinnwand hinten
    T.plane("periodensystem", (1.5, 1.0), T.mat("PSE", "#ffffff", tex=tex("periodensystem.png")),
            loc=(W1 - 0.01, 1.2, 1.7), rot=(90, 0, -90))
    T.plane("europa", (1.4, 1.0), T.mat("Europa", "#ffffff", tex=tex("europa.png")), loc=(W1 - 0.01, -1.2, 1.7),
            rot=(90, 0, -90))
    T.plane("regeln", (0.6, 0.8), T.mat("Regeln", "#ffffff", tex=tex("regeln.png")), loc=(1.9, Y1 - 0.01, 1.7))
    T.box("pinnwand", (2.4, 0.04, 1.1), T.mat("Kork", "#c49a62"), loc=(1.4, Y0 + 0.02, 1.65), line=0.006)
    for k in range(7):
        T.box(f"zettel_{k}", (0.21, 0.01, 0.29), T.mat(f"Zettel{k % 3}", ("#ffffff", "#fff3a8", "#cfe8ff")[k % 3]),
              loc=(0.45 + k * 0.32, Y0 + 0.05, 1.5 + 0.25 * (k % 2)), line=0.002)
    # Regal hinten links
    T.box("regal", (1.6, 0.4, 1.8), M["regal"], loc=(-2.6, Y0 + 0.22, 0.9), line=0.008)
    for k, c in enumerate(("#c0392b", "#2e86c1", "#27ae60", "#f1c40f", "#8e44ad", "#e67e22")):
        T.box(f"ordner_{k}", (0.09, 0.3, 0.32), T.mat(f"Ordner{k}", c), loc=(-3.2 + k * 0.12, Y0 + 0.18, 1.3),
              line=0.003)
    # Deckenlampen
    for x in (-2.0, 0.6, 2.8):
        for y in (-1.0, 1.8, 4.4):
            T.box(f"lampe_{x}_{y}", (0.32, 1.3, 0.07), M["lampe"], loc=(x, y, H - 0.06), line=0.005)
    # Pult + Lehrerstuhl
    px, py = PULT
    T.box("pult_platte", (1.5, 0.75, 0.05), M["pult"], loc=(px, py, 0.76), line=0.008, bevel=0.01)
    T.box("pult_front", (1.48, 0.05, 0.72), M["pult"], loc=(px, py - 0.34, 0.37), line=0.008)
    T.box("pult_seite", (0.05, 0.7, 0.72), M["pult"], loc=(px + 0.72, py, 0.37), line=0.008)
    T.box("pult_seite2", (0.05, 0.7, 0.72), M["pult"], loc=(px - 0.72, py, 0.37), line=0.008)
    T.box("pult_tasche", (0.42, 0.14, 0.30), T.mat("Tasche", "#2a2a2a"), loc=(px + 0.4, py + 0.1, 0.94), line=0.006,
          bevel=0.03)
    T.box("pult_mappe", (0.32, 0.24, 0.02), T.mat("Mappe", "#c23b3b"), loc=(px - 0.35, py - 0.05, 0.795), line=0.004)
    stuhl(px, py + 0.62, M, rot=180, name="lehrerstuhl")
    # Tische, Stühle, Kram
    k = 0
    for cx in COLS:
        for ry in ROWS:
            tisch(cx, ry + 0.45, M)
            for sx in (-1, 1):
                stuhl(cx + sx * SEAT_DX, ry - 0.05, M)
            kram(cx, ry + 0.45, M, k)
            k += 1
    if outside:
        schulhof()
    return M


def schulhof():
    """Blick aus dem Fenster: Hof zwei Stockwerke tiefer, Schüler am Sammelplatz, Feuerwehr, Gegenüber-Flügel."""
    g = GROUND
    T.box("hof", (80, 90, 0.2), T.mat("Asphalt", "#9fa3a6"), loc=(-44, 2, g - 0.1), line=0)
    T.box("rasen", (30, 90, 0.2), T.mat("Rasen", "#7fb45d"), loc=(-75, 2, g - 0.05), line=0)
    T.box("fassade", (0.6, 90, 7.0), T.mat("Fassade", "#e6d3b3"), loc=(-4.4, 2, g + 3.4), line=0)
    # Gegenüberliegender Schulflügel
    T.box("fluegel", (14, 60, 13), T.mat("Fluegel", "#d9b48a"), loc=(-52, 4, g + 6.5), line=0.06)
    T.box("fluegel_dach", (15, 61, 0.8), T.mat("Dach", "#8a4b3a"), loc=(-52, 4, g + 13.2), line=0.05)
    fen = T.mat("FensterFern", "#6d8fae")
    for fl in range(3):
        for k in range(14):
            T.box(f"fern_fenster_{fl}_{k}", (0.2, 2.2, 1.6), fen, loc=(-44.9, -22 + k * 4.0, g + 2.2 + fl * 3.8), line=0.02)
    # Bäume
    for k in range(9):
        ty = -26 + k * 6.5 + 2 * _hash("baum", k)
        tx = -36 - 3 * _hash("baum", k + 3)
        T.cylinder(f"stamm_{k}", 0.35, 4.0, T.mat("Stamm", "#6b4a32"), loc=(tx, ty, g + 2.0), line=0.03)
        T.ellipsoid(f"krone_{k}", (5.0, 5.0, 5.6), T.mat("Krone", ("#5f9e4a", "#6aab52", "#558f43")[k % 3]),
                    loc=(tx, ty, g + 6.0), line=0.05, segs=16, rings=10)
    # Sammelplatz-Schild
    T.cylinder("sammel_pfosten", 0.05, 2.6, T.mat("Pfosten", "#7b7f85"), loc=(-20, -6, g + 1.3), line=0.02)
    T.box("sammel_schild", (0.05, 1.0, 0.7), T.mat("SammelGruen", "#16964f"), loc=(-20, -6, g + 2.7), line=0.02)
    # Schülergruppen in Klassenreihen
    skins = ("#f3d2b6", "#e8b48f", "#c68a62", "#8d5a3b", "#f6d9c4")
    tops = ("#d94f4f", "#4f7fd9", "#5bbf72", "#9b6bd1", "#f0c64a", "#e07ab5", "#4ab3c4", "#e8e8e8", "#545b66",
            "#c96a3a", "#2f3a4f")
    hairs = ("#2a1d16", "#6b4423", "#d4a55a", "#151212", "#8c3b1f")
    n = 0
    for grp in range(7):
        gx = -15 - (grp % 4) * 3.4
        gy = -14 + grp * 3.6
        for r in range(3):
            for c in range(4):
                n += 1
                hx = _hash("hofkind", n)
                x = gx - r * 0.75 + 0.2 * (hx - 0.5)
                y = gy + c * 0.62 + 0.2 * (_hash("hofkind", n + 99) - 0.5)
                mensch(f"hofkind_{n}", x, y, g, skins[n % 5], tops[int(hx * 11) % 11], hairs[n % 5],
                       h=1.55 + 0.15 * hx)
    for k, (x, y) in enumerate(((-13.5, -9), (-13.0, 2), (-14.0, 10))):
        mensch(f"hoflehrer_{k}", x, y, g, "#f0c8a8", ("#7a5c3e", "#3c5a7a", "#6a3c5a")[k], "#4a3b30", h=1.8,
               hand_up=True)
    feuerwehr(-27, 9, g)


def mensch(name, x, y, g, skin, top, hair, h=1.6, hand_up=False):
    """Fernfigur (wenige Teile, gut für Menschenmengen)."""
    root = T.empty(name, (x, y, g))
    root.rotation_euler[2] = math.radians(-90 + 40 * (_hash(name, 1) - 0.5))
    s = h / 1.6
    lm = T.mat("FernHose", "#2d3443")
    for sx in (-1, 1):
        T.capsule(f"{name}_bein_{sx}", 0.07 * s, 0.62 * s, lm, loc=(sx * 0.09 * s, 0, 0.78 * s), parent=root, line=0.015)
    T.capsule(f"{name}_koerper", 0.19 * s, 0.38 * s, T.mat(f"Fern_{top}", top), loc=(0, 0, 1.28 * s), parent=root,
              line=0.018)
    T.ellipsoid(f"{name}_kopf", (0.27 * s, 0.27 * s, 0.31 * s), T.mat(f"FernHaut_{skin}", skin), loc=(0, 0, 1.52 * s),
                parent=root, line=0.018, segs=16, rings=10)
    T.ellipsoid(f"{name}_haar", (0.29 * s, 0.29 * s, 0.22 * s), T.mat(f"FernHaar_{hair}", hair),
                loc=(0, 0.02, 1.6 * s), parent=root, line=0.015, segs=16, rings=8, cut=lambda v: v.z < -0.02)
    if hand_up:
        T.box(f"{name}_klemmbrett", (0.25, 0.04, 0.33), T.mat("Klemmbrett", "#c9a26b"), loc=(0.15, -0.25, 1.25 * s),
              parent=root, line=0.012)


def feuerwehr(x, y, g):
    rot = T.mat("Feuerrot", "#d1262b")
    root = T.empty("feuerwehr", (x, y, g))
    T.box("fw_aufbau", (2.5, 7.0, 2.4), rot, loc=(0, 0, 1.75), parent=root, line=0.03, bevel=0.06)
    T.box("fw_kabine", (2.5, 2.2, 2.0), rot, loc=(0, -4.4, 1.6), parent=root, line=0.03, bevel=0.08)
    T.box("fw_scheibe", (2.3, 0.08, 0.9), T.mat("Scheibe", "#9cc6e0"), loc=(0, -5.52, 2.05), parent=root, line=0.02)
    T.box("fw_streifen", (2.52, 9.2, 0.18), T.mat("Weissstreifen", "#f4f4f4"), loc=(0, -1.1, 1.05), parent=root,
          line=0.0)
    T.box("fw_leiter", (0.9, 7.6, 0.18), T.mat("Leiter", "#cfd3d6"), loc=(0, 0.3, 3.1), parent=root, line=0.02)
    for k, yy in enumerate((-4.4, -1.0, 2.2)):
        for sx in (-1, 1):
            T.cylinder(f"fw_rad_{k}_{sx}", 0.55, 0.35, T.mat("Reifen", "#1e1e1e"), loc=(sx * 1.2, yy, 0.55), parent=root,
                       axis="X", line=0.02)
    for sx in (-1, 1):
        T.box(f"fw_blaulicht_{sx}", (0.35, 0.25, 0.2), T.mat("Blaulicht", "#3d7bff"), loc=(sx * 0.8, -4.6, 2.72),
              parent=root, line=0.01, bevel=0.04)

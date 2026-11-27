"""Flur im 2. Stock (Alarmlicht rot) und Keller K3 (Hausmeister-Werkstatt).

Flur: läuft entlang +Y, x in [-1.6, 1.6]; Spinde links, Fenster/Türen rechts; Nebentreppe am Ende (y=26).
Keller: Raum x in [-3, 3], y in [0, 7], niedrige Decke, Rohre, Heizkessel, Werkbank, eine Hängelampe.
"""
import math
import os

import toon as T
from figur import _hash

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")


def tex(n):
    return os.path.join(A, n)


def flur(length=40.0):
    M = dict(boden=T.mat("FlurBoden", "#a9a094"), wand=T.mat("FlurWand", "#efe4cf"), decke=T.mat("FlurDecke", "#ecebe6"),
             spind=T.mat("Spind", "#4f7fae"), spind2=T.mat("Spind2", "#d9534f"), metall=T.mat("FlurMetall", "#5d6672"),
             holz=T.mat("FlurTuer", "#b98a55"), lampe=T.mat("FlurLampe", "#fffdf2"), rahmen=T.mat("FlurRahmen", "#f6f6f2"))
    W = 1.6
    H = 3.0
    T.box("flur_boden", (2 * W, length, 0.1), M["boden"], loc=(0, length / 2 - 2, -0.05), line=0)
    T.box("flur_decke", (2 * W, length, 0.1), M["decke"], loc=(0, length / 2 - 2, H + 0.05), line=0)
    T.box("flur_wand_l", (0.2, length, H), M["wand"], loc=(-W - 0.1, length / 2 - 2, H / 2), line=0)
    T.box("flur_wand_r", (0.2, length, H), M["wand"], loc=(W + 0.1, length / 2 - 2, H / 2), line=0)
    T.box("flur_wand_ende", (2 * W, 0.2, H), M["wand"], loc=(0, length - 2 + 0.1, H / 2), line=0)
    T.box("flur_wand_start", (2 * W, 0.2, H), M["wand"], loc=(0, -2.1, H / 2), line=0)
    # Bodenstreifen (Fliesenfugen-Look)
    fuge = T.mat("Fuge", "#968d81")
    for k in range(int(length / 1.2)):
        T.box(f"fuge_{k}", (2 * W, 0.03, 0.005), fuge, loc=(0, -2 + k * 1.2, 0.002), line=0)
    # Spinde links in Reihen
    for k in range(int((length - 6) / 0.42)):
        y = 0.5 + k * 0.42
        if 9.5 < y < 11.6:
            continue
        m = M["spind"] if (k // 6) % 2 == 0 else M["spind2"]
        T.box(f"spind_{k}", (0.45, 0.40, 1.85), m, loc=(-W + 0.23, y, 0.925), line=0.006, bevel=0.01)
        T.box(f"spind_schlitz_{k}", (0.01, 0.2, 0.02), M["metall"], loc=(-W + 0.46, y, 1.6), line=0)
        T.box(f"spind_griff_{k}", (0.02, 0.03, 0.12), M["metall"], loc=(-W + 0.47, y + 0.12, 1.05), line=0.002)
    # Türen rechts (Klassenräume) mit Schildern
    for k, (y, schild) in enumerate(((2.0, "schild_205.png"), (8.0, "schild_204.png"), (14.0, "schild_203.png"))):
        T.box(f"flurtuer_{k}", (0.06, 1.0, 2.08), M["holz"], loc=(W - 0.03, y, 1.04), line=0.008)
        T.box(f"flurtuer_zarge_{k}", (0.08, 1.12, 2.16), M["metall"], loc=(W - 0.0, y, 1.08), line=0.006)
        T.cylinder(f"flurtuer_klinke_{k}", 0.012, 0.13, M["metall"], loc=(W - 0.09, y - 0.38, 1.05), axis="X", line=0.003)
        T.plane(f"flurschild_{k}", (0.36, 0.15), T.mat(f"FlurSchild{k}", "#ffffff", tex=tex(schild)),
                loc=(W - 0.01, y + 0.75, 1.62), rot=(90, 0, -90))
    # Fenster rechts zwischen den Türen
    fen = T.mat("FlurFensterBlick", "#bcdcf0")
    for k, y in enumerate((5.0, 11.0, 17.5, 21.5)):
        T.box(f"flurfenster_{k}", (0.05, 1.8, 1.3), fen, loc=(W - 0.01, y, 1.75), line=0.008)
        T.box(f"flurfenster_rahmen_{k}", (0.07, 0.06, 1.3), M["rahmen"], loc=(W - 0.03, y, 1.75), line=0.004)
    # Feuermelder + rote Blitzleuchten
    T.box("feuermelder", (0.06, 0.16, 0.16), T.mat("Melderrot", "#d1262b"), loc=(-W + 0.03, 10.0, 1.45), line=0.006,
          bevel=0.01)
    T.box("feuermelder_glas", (0.01, 0.1, 0.1), T.mat("MelderGlas", "#f4f4f4"), loc=(-W + 0.065, 10.0, 1.46), line=0.002)
    blitz = []
    for k, y in enumerate((3.0, 10.5, 18.0, 24.5)):
        b = T.box(f"blitz_{k}", (0.12, 0.16, 0.16), T.mat(f"Blitz{k}", "#ff2a2a"), loc=(-W + 0.06, y, 2.65), line=0.006,
                  bevel=0.03)
        blitz.append(b)
    # Deckenlampen
    for k in range(int(length / 3.2)):
        T.box(f"flurlampe_{k}", (0.32, 1.2, 0.07), M["lampe"], loc=(0, k * 3.2, H - 0.06), line=0.005)
    # Notausgang + Nebentreppe am Ende
    T.plane("flur_notausgang", (0.55, 0.2), T.mat("FlurNotausgang", "#16964f", tex=tex("notausgang.png")),
            loc=(0, length - 2 - 0.01, 2.55))
    T.box("treppentuer", (1.1, 0.06, 2.1), T.mat("Treppentuer", "#7f8c99"), loc=(0, length - 2 - 0.03, 1.05),
          line=0.008)
    T.box("treppentuer_fenster", (0.4, 0.07, 0.5), T.mat("TuerGlas", "#bcdcf0"), loc=(0, length - 2 - 0.035, 1.5),
          line=0.004)
    T.plane("schild_keller", (0.6, 0.24), T.mat("Kellerschild", "#ffffff", tex=tex("schild_keller.png")),
            loc=(0.85, length - 2 - 0.01, 1.7))
    T.cylinder("treppentuer_griff", 0.015, 0.6, M["metall"], loc=(0.0, length - 2 - 0.09, 1.05), axis="X", line=0.003)
    # Schultaschen am Boden (liegen gelassen beim Alarm)
    for k, (x, y, c) in enumerate(((-0.9, 6.0, "#3b5ba5"), (0.7, 12.4, "#2d2d2d"), (-0.6, 16.0, "#c0392b"))):
        o = T.box(f"rucksack_{k}", (0.32, 0.22, 0.42), T.mat(f"Rucksack{k}", c), loc=(x, y, 0.21), line=0.006, bevel=0.06)
        o.rotation_euler[2] = math.radians(30 * (k - 1))
    return blitz


def keller():
    M = dict(boden=T.mat("KellerBoden", "#7d7a74"), wand=T.mat("KellerWand", "#b8b2a6"), decke=T.mat("KellerDecke",
                                                                                                     "#9e998f"),
             rohr=T.mat("Rohr", "#8a8f96"), rohr2=T.mat("Rohr2", "#b5523b"), kessel=T.mat("Kessel", "#c9cdd2"),
             holz=T.mat("Werkbank", "#9b7146"), regal=T.mat("KellerRegal", "#6f747b"), metall=T.mat("KellerMetall",
                                                                                                    "#4b5058"))
    X0, X1, Y0, Y1, H = -3.2, 3.2, -1.0, 7.0, 2.6
    T.box("k_boden", (X1 - X0, Y1 - Y0, 0.1), M["boden"], loc=(0, (Y0 + Y1) / 2, -0.05), line=0)
    T.box("k_decke", (X1 - X0, Y1 - Y0, 0.1), M["decke"], loc=(0, (Y0 + Y1) / 2, H + 0.05), line=0)
    T.box("k_wand_l", (0.2, Y1 - Y0, H), M["wand"], loc=(X0 - 0.1, (Y0 + Y1) / 2, H / 2), line=0)
    T.box("k_wand_r", (0.2, Y1 - Y0, H), M["wand"], loc=(X1 + 0.1, (Y0 + Y1) / 2, H / 2), line=0)
    T.box("k_wand_hinten", (X1 - X0, 0.2, H), M["wand"], loc=(0, Y1 + 0.1, H / 2), line=0)
    T.box("k_wand_vorn_a", (X1 - X0 - 1.2, 0.2, H), M["wand"], loc=(0.6 + (X0 + X1) / 2 - 0.0, Y0 - 0.1, H / 2), line=0)
    # Rohre an der Decke
    for k, (x, r, m) in enumerate(((-2.2, 0.09, "rohr"), (-1.8, 0.06, "rohr2"), (1.4, 0.11, "rohr"), (2.5, 0.07,
                                                                                                    "rohr2"))):
        T.cylinder(f"k_rohr_{k}", r, Y1 - Y0, M[m], loc=(x, (Y0 + Y1) / 2, H - 0.25 - 0.1 * (k % 2)), axis="Y", line=0.008)
        for j in range(4):
            T.box(f"k_schelle_{k}_{j}", (0.04, 0.04, 0.2), M["metall"], loc=(x, Y0 + 1 + j * 1.8, H - 0.12), line=0.003)
    T.cylinder("k_rohr_quer", 0.08, X1 - X0, M["rohr"], loc=(0, 5.6, H - 0.45), axis="X", line=0.008)
    # Heizkessel hinten rechts
    T.cylinder("k_kessel", 0.65, 1.9, M["kessel"], loc=(2.1, 5.9, 0.95), line=0.01, segs=32)
    T.cylinder("k_kessel_deckel", 0.66, 0.08, M["metall"], loc=(2.1, 5.9, 1.92), line=0.008, segs=32)
    T.cylinder("k_kessel_rohr", 0.1, 0.8, M["rohr"], loc=(2.1, 5.9, 2.3), line=0.006)
    T.cylinder("k_manometer", 0.09, 0.04, T.mat("Manometer", "#f4f4f4"), loc=(1.5, 5.45, 1.3), axis="Y", line=0.004)
    # Werkbank links mit Werkzeug
    T.box("k_werkbank", (0.8, 2.2, 0.08), M["holz"], loc=(-2.65, 3.2, 0.9), line=0.008)
    for dy in (-1.0, 1.0):
        for dx in (-0.3, 0.3):
            T.box(f"k_wb_bein_{dy}_{dx}", (0.06, 0.06, 0.88), M["metall"], loc=(-2.65 + dx, 3.2 + dy, 0.44), line=0.004)
    T.box("k_lochwand", (0.04, 2.2, 1.0), T.mat("Lochwand", "#c2a27a"), loc=(-3.08, 3.2, 1.65), line=0.006)
    for k in range(6):
        T.box(f"k_werkzeug_{k}", (0.03, 0.05, 0.3 + 0.1 * (k % 3)),
              T.mat(f"Werkzeug{k % 3}", ("#d1262b", "#3b3f46", "#e9b21c")[k % 3]),
              loc=(-3.04, 2.3 + k * 0.35, 1.65), line=0.003)
    T.box("k_werkzeugkiste", (0.5, 0.3, 0.25), T.mat("Kiste", "#d1262b"), loc=(-2.6, 2.6, 1.07), line=0.006,
          bevel=0.02)
    T.box("k_schraubstock", (0.18, 0.25, 0.15), M["metall"], loc=(-2.5, 4.0, 1.02), line=0.004)
    # Regal rechts mit Farbeimern/Kartons
    T.box("k_regal", (0.5, 2.0, 2.0), M["regal"], loc=(2.9, 2.0, 1.0), line=0.008)
    for k in range(8):
        x = 2.75
        y = 1.2 + (k % 4) * 0.45
        z = 0.5 + (k // 4) * 0.8
        if k % 3 == 0:
            T.cylinder(f"k_eimer_{k}", 0.15, 0.3, T.mat(f"Eimer{k % 2}", ("#e9e9e9", "#4f7fae")[k % 2]),
                       loc=(x, y, z + 0.15), line=0.004)
        else:
            T.box(f"k_karton_{k}", (0.35, 0.35, 0.3), T.mat("Karton", "#c49a62"), loc=(x, y, z + 0.15), line=0.004)
    # Hängelampe (Glühbirne) als Pendel
    pend = T.empty("k_lampe_pendel", (0.0, 3.0, H))
    T.cylinder("k_lampe_kabel", 0.008, 0.6, T.mat("LampeKabel", "#202020"), loc=(0, 0, -0.3), parent=pend, line=0.0)
    T.cylinder("k_lampe_schirm", 0.22, 0.12, T.mat("LampeSchirm", "#2f4f3a"), loc=(0, 0, -0.62), parent=pend,
               line=0.004, r2=0.06)
    T.ellipsoid("k_birne", (0.1, 0.1, 0.13), T.mat("Birne", "#fff4c2"), loc=(0, 0, -0.72), parent=pend, line=0.002)
    # Tür (Eingang) vorne links mit Schild K3
    T.box("k_tuer", (1.0, 0.06, 2.05), T.mat("KellerTuer", "#7f8c99"), loc=(-2.6, Y0 - 0.02, 1.02), line=0.008)
    T.plane("k_schild", (0.5, 0.2), T.mat("K3schild", "#ffffff", tex=tex("schild_k3.png")), loc=(-1.6, Y0 + 0.02, 1.8),
            rot=(90, 0, 180))
    return pend

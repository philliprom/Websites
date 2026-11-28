"""Teil 2: Hinterhof (Regen, blaues Auto, Turnhalle) und Straße (Fahrt bis zur roten Ampel), Auto mit Innenraum.

Hof: Schul-Rückwand mit Kellertür bei y=0 (Tür schaut nach +Y), Hof nach +Y, Auto bei AUTO_HOF, Turnhalle rechts hinten.
Straße: läuft entlang +Y, Auto fährt auf der rechten Spur (x=+1.6) von y=0 bis zur Ampel bei AMPEL_Y.
Auto: Front zeigt nach +Y; Fahrer vorn links (x=-0.4), Noah hinten rechts (x=+0.42), Ben hinten links (x=-0.42).
"""
import math
import os

import toon as T
from figur import _hash

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
AUTO_HOF = (3.4, 8.8, 0.0)       # Auto im Hof: nah an der Kellertür, Front schräg zum Betrachter
AUTO_HOF_ROT = 120.0
AMPEL_Y = 250.0                  # Fahrt ca. 35 s mit Stadttempo bis zur roten Ampel
SPUR_X = 1.6
FAHRER_SITZ = (-0.40, 0.30)      # relativ zum Auto
SITZ_Z = {"Fahrer": 0.02, "Ben": 0.0}   # Wurzelhöhe der sitzenden Figuren im Auto
DACH_Z = 1.74                    # Dachmitte; Himmel innen bei 1.69 (Köpfe bis ca. 1.63)
HANDYHALTER = (0.22, 0.80, 1.2)
STOP_Y = 250.0 - 11.6            # Auto hält hinter einem wartenden Auto an der roten Ampel
BEN_SITZ = (-0.42, -0.62)
NOAH_SITZ = (0.42, -0.62)
NOAH_AUGE = (0.24, -0.6, 1.22)   # Kamera: Noah lehnt sich zur Mitte, damit er zwischen den Sitzen nach vorn sieht
NOAH_AUGE_Z = 1.22


def tex(n):
    return os.path.join(A, n)


def hof_welt(lx, ly, z=0.0):
    """Weltpunkt zu einem Punkt relativ zum Hof-Auto (x rechts, y nach vorn)."""
    a = math.radians(AUTO_HOF_ROT)
    return (AUTO_HOF[0] + lx * math.cos(a) - ly * math.sin(a), AUTO_HOF[1] + lx * math.sin(a) + ly * math.cos(a), z)


def auto(name, farbe="#2a5db0", loc=(0, 0, 0), rot=0.0, innen=True, glas=True, line=0.009, tuer_hl_offen=False,
         lichter=False, fenster_hr=False):
    """Toon-Auto (Kombi-Limousine), Front nach +Y. Gibt (wurzel, glas_objekte, handyhalter-empty) zurück.
    tuer_hl_offen: Tür hinten links steht offen (Hof). lichter: Scheinwerfer-Blitze für die Lichthupe (Empties
    {name}_flare_±1, Größe wird animiert). fenster_hr: Scheibe hinten rechts als eigene Gruppe {name}_fenster_hr
    (kann herunterfahren)."""
    root = T.empty(name, loc)
    root.rotation_euler[2] = math.radians(rot)
    lack = T.mat(f"{name}_lack", farbe)
    dunkel = T.mat("AutoDunkel", "#1d1f24")
    innenm = T.mat("AutoInnen", "#565a63")
    sitz = T.mat("AutoSitz", "#77716a")
    chrom = T.mat("AutoChrom", "#c9ced6")
    glasm = T.mat("AutoGlas", "#243447")
    # Unterboden, Seiten (Türen), Motorhaube, Kofferraum, Stoßstangen
    T.box(f"{name}_boden", (1.7, 4.3, 0.16), dunkel, loc=(0, 0, 0.36), parent=root, line=line)
    scharnier = None
    for sx in (-1, 1):
        if sx == -1 and tuer_hl_offen:
            T.box(f"{name}_tuer_{sx}", (0.09, 1.1, 0.62), lack, loc=(sx * 0.87, 0.45, 0.66), parent=root, line=line,
                  bevel=0.03)
            # Hintertür links offen: Scharnier an ihrer Vorderkante, nach außen gedreht
            scharnier = T.empty(f"{name}_tuer_hl", (sx * 0.87, -0.10, 0.0), root, rot=(0, 0, -70))
            T.box(f"{name}_tuer_hl_blech", (0.09, 1.0, 0.62), lack, loc=(0, -0.5, 0.66), parent=scharnier, line=line,
                  bevel=0.03)
            T.box(f"{name}_tuer_hl_innen", (0.05, 0.95, 0.45), innenm, loc=(0.06, -0.5, 0.75), parent=scharnier,
                  line=0.004)
            T.box(f"{name}_tuer_hl_griff", (0.1, 0.14, 0.03), chrom, loc=(-0.05, -0.38, 0.86), parent=scharnier,
                  line=0.003)
            T.box(f"{name}_tuer_hl_rahmen", (0.07, 0.95, 0.06), lack, loc=(0, -0.48, 1.70), parent=scharnier,
                  line=0.005)
            T.box(f"{name}_tuer_hl_rahmen_h", (0.07, 0.06, 0.73), lack, loc=(0, -0.97, 1.33), parent=scharnier,
                  line=0.005)
        else:
            T.box(f"{name}_tuer_{sx}", (0.09, 2.1, 0.62), lack, loc=(sx * 0.87, -0.05, 0.66), parent=root, line=line,
                  bevel=0.03)
            T.box(f"{name}_tuerlinie_{sx}", (0.1, 0.02, 0.5), dunkel, loc=(sx * 0.875, -0.05, 0.68), parent=root,
                  line=0)
            T.box(f"{name}_griff_{sx}_h", (0.1, 0.14, 0.03), chrom, loc=(sx * 0.92, -0.45, 0.86), parent=root,
                  line=0.003)
        T.box(f"{name}_griff_{sx}_v", (0.1, 0.14, 0.03), chrom, loc=(sx * 0.92, 0.35, 0.86), parent=root, line=0.003)
        T.box(f"{name}_spiegel_{sx}", (0.16, 0.07, 0.1), lack, loc=(sx * 0.98, 0.98, 1.0), parent=root, line=0.004,
              bevel=0.02)
    T.box(f"{name}_haube", (1.8, 1.2, 0.36), lack, loc=(0, 1.62, 0.72), parent=root, line=line, bevel=0.1)
    T.box(f"{name}_koffer", (1.8, 1.1, 0.46), lack, loc=(0, -1.62, 0.77), parent=root, line=line, bevel=0.1)
    T.box(f"{name}_stoss_v", (1.84, 0.16, 0.22), dunkel, loc=(0, 2.24, 0.5), parent=root, line=line, bevel=0.05)
    T.box(f"{name}_stoss_h", (1.84, 0.16, 0.22), dunkel, loc=(0, -2.2, 0.5), parent=root, line=line, bevel=0.05)
    for sx in (-1, 1):
        T.box(f"{name}_licht_v_{sx}", (0.36, 0.05, 0.12), T.mat("Scheinwerfer", "#fff6c9"), loc=(sx * 0.6, 2.23, 0.78),
              parent=root, line=0.004, bevel=0.02)
        T.box(f"{name}_licht_h_{sx}", (0.34, 0.05, 0.12), T.mat("Ruecklicht", "#d8262e"), loc=(sx * 0.62, -2.18, 0.86),
              parent=root, line=0.004, bevel=0.02)
    T.plane(f"{name}_kennzeichen_v", (0.5, 0.12), T.mat("Kennzeichen", "#ffffff", tex=tex("kennzeichen.png")),
            loc=(0, 2.33, 0.52), rot=(90, 0, 180), parent=root)
    T.plane(f"{name}_kennzeichen_h", (0.5, 0.12), T.mat("Kennzeichen", "#ffffff", tex=tex("kennzeichen.png")),
            loc=(0, -2.29, 0.6), rot=(90, 0, 0), parent=root)
    # Dach und Säulen: hoher Fahrgastraum (Toon-Figuren haben große Köpfe), Frontscheibe nach hinten geneigt
    T.box(f"{name}_dach", (1.62, 1.75, 0.07), lack, loc=(0, -0.125, DACH_Z), parent=root, line=line, bevel=0.03)
    for sx in (-1, 1):
        o = T.box(f"{name}_saeule_a_{sx}", (0.07, 0.09, 0.9), lack, loc=(sx * 0.82, 0.90, 1.32), parent=root, line=0.005)
        o.rotation_euler[0] = math.radians(26.6)
        T.box(f"{name}_saeule_b_{sx}", (0.07, 0.1, 0.76), lack, loc=(sx * 0.82, -0.10, 1.345), parent=root, line=0.005)
        o = T.box(f"{name}_saeule_c_{sx}", (0.07, 0.14, 0.78), lack, loc=(sx * 0.82, -1.10, 1.36), parent=root,
                  line=0.005)
        o.rotation_euler[0] = math.radians(-22.6)
    # Räder
    for sx in (-1, 1):
        for sy in (-1, 1):
            T.cylinder(f"{name}_rad_{sx}_{sy}", 0.34, 0.24, T.mat("Reifen", "#18181b"), loc=(sx * 0.82, sy * 1.36, 0.34),
                       parent=root, axis="X", line=line, segs=28)
            T.cylinder(f"{name}_felge_{sx}_{sy}", 0.2, 0.26, chrom, loc=(sx * 0.82, sy * 1.36, 0.34), parent=root,
                       axis="X", line=0.003, segs=20)
    # Scheibe hinten rechts als eigene Gruppe (fährt in Teil 2 am Ende von selbst herunter)
    fenster = T.empty(f"{name}_fenster_hr", (0.83, -0.57, 0.0), root) if fenster_hr else None

    def scheibe_eltern(sx, k, x, y):
        """(Eltern, lokale x, lokale y) für Teile einer Seitenscheibe: Wurzel, offene Tür oder Fenstergruppe."""
        if sx == -1 and k == 1 and scharnier is not None:
            return scharnier, x + 0.87, y + 0.10
        if sx == 1 and k == 1 and fenster is not None:
            return fenster, x - 0.83, y + 0.57
        return root, x, y

    glasobj = []
    if glas:
        for sx in (-1, 1):
            for k, (y, w) in enumerate(((0.45, 0.95), (-0.57, 0.86))):
                par, lx, ly = scheibe_eltern(sx, k, sx * 0.83, y)
                o = T.box(f"{name}_glas_seite_{sx}_{k}", (0.02, w, 0.7), glasm, loc=(lx, ly, 1.33), parent=par, line=0)
                glasobj.append(o)
        # Comic-Glanzstreifen auf den Seitenscheiben (innen und außen): zeigt, dass die Fenster zu sind
        glanz = T.mat("Glanz", "#e9f3ff")
        for sx in (-1, 1):
            for k, y in enumerate((0.45, -0.57)):
                for seite, xx in (("i", 0.812), ("a", 0.848)):
                    for j, (dy, b, h) in enumerate(((-0.12, 0.034, 0.52), (0.06, 0.016, 0.4))):
                        par, lx, ly = scheibe_eltern(sx, k, sx * xx, y + dy)
                        o = T.box(f"{name}_glanz_{sx}_{k}_{seite}_{j}", (0.006, b, h), glanz,
                                  loc=(lx, ly, 1.34), parent=par, line=0)
                        o.rotation_euler[0] = math.radians(-35)
        if fenster is not None:   # sichtbare Oberkante der Scheibe (wandert beim Öffnen mit nach unten)
            T.box(f"{name}_fenster_hr_kante", (0.03, 0.84, 0.022), T.mat("Glaskante", "#cfe0ee"), loc=(0, 0, 1.675),
                  parent=fenster, line=0)
        o = T.box(f"{name}_glas_front", (1.58, 0.02, 0.88), glasm, loc=(0, 0.9, 1.32), parent=root, line=0)
        o.rotation_euler[0] = math.radians(26.6)
        glasobj.append(o)
        o = T.box(f"{name}_glas_heck", (1.58, 0.02, 0.76), glasm, loc=(0, -1.1, 1.36), parent=root, line=0)
        o.rotation_euler[0] = math.radians(-22.6)
        glasobj.append(o)
    halter = None
    if innen:
        # Sitze vorn
        for sx in (-1, 1):
            T.box(f"{name}_sitz_v_{sx}", (0.5, 0.52, 0.12), sitz, loc=(sx * 0.4, 0.28, 0.5), parent=root, line=0.005,
                  bevel=0.03)
            o = T.box(f"{name}_lehne_v_{sx}", (0.5, 0.12, 0.55), sitz, loc=(sx * 0.4, 0.0, 0.82), parent=root,
                      line=0.005, bevel=0.04)
            o.rotation_euler[0] = math.radians(-10)
            T.box(f"{name}_kopfst_{sx}", (0.24, 0.09, 0.15), sitz, loc=(sx * 0.4, -0.06, 1.2), parent=root, line=0.004,
                  bevel=0.03)
        T.box(f"{name}_himmel", (1.52, 1.62, 0.03), T.mat("AutoHimmel", "#cfcbc2"), loc=(0, -0.125, DACH_Z - 0.05), parent=root,
              line=0.004)
        # Rückbank
        T.box(f"{name}_bank", (1.5, 0.55, 0.14), sitz, loc=(0, -0.62, 0.46), parent=root, line=0.005, bevel=0.03)
        o = T.box(f"{name}_banklehne", (1.5, 0.12, 0.62), sitz, loc=(0, -0.92, 0.82), parent=root, line=0.005, bevel=0.04)
        o.rotation_euler[0] = math.radians(10)
        # Armaturen, Lenkrad, Mittelkonsole, Innenspiegel
        T.box(f"{name}_armatur", (1.62, 0.45, 0.32), innenm, loc=(0, 0.98, 0.95), parent=root, line=0.006, bevel=0.06)
        T.box(f"{name}_konsole", (0.25, 0.9, 0.3), innenm, loc=(0, 0.35, 0.55), parent=root, line=0.005, bevel=0.04)
        lenk = T.torus(f"{name}_lenkrad", 0.17, 0.022, dunkel, loc=(-0.4, 0.66, 1.0), parent=root, line=0.003,
                       axis="Y")
        lenk.rotation_euler[0] = math.radians(-25)
        T.box(f"{name}_innenspiegel", (0.24, 0.03, 0.07), dunkel, loc=(0, 0.66, 1.58), parent=root, line=0.003,
              bevel=0.01)
        for sx in (-1, 1):
            if sx == -1 and scharnier is not None:   # hinterer Teil der Verkleidung sitzt an der offenen Tür
                T.box(f"{name}_innentuer_{sx}", (0.06, 1.05, 0.45), innenm, loc=(sx * 0.8, 0.42, 0.75), parent=root,
                      line=0.004)
                continue
            T.box(f"{name}_innentuer_{sx}", (0.06, 2.0, 0.45), innenm, loc=(sx * 0.8, -0.05, 0.75), parent=root,
                  line=0.004)
            T.box(f"{name}_fensterheber_{sx}", (0.04, 0.08, 0.04), chrom, loc=(sx * 0.77, -0.55, 0.92), parent=root,
                  line=0.002)
            T.box(f"{name}_griffmulde_{sx}", (0.02, 0.24, 0.1), dunkel, loc=(sx * 0.772, -0.3, 0.95), parent=root,
                  line=0.002, bevel=0.01)
            T.box(f"{name}_innengriff_{sx}", (0.045, 0.18, 0.045), chrom, loc=(sx * 0.752, -0.3, 0.95), parent=root,
                  line=0.003, bevel=0.01)
        # Handyhalter mit Fahrer-Handy (Bildschirm wird je Einstellung gesetzt)
        halter = T.empty(f"{name}_handyhalter", HANDYHALTER, root, rot=(70, 0, 0))
        T.box(f"{name}_fahrerhandy", (0.075, 0.15, 0.01), dunkel, parent=halter, line=0.003, bevel=0.005)
        T.plane(f"{name}_fahrerhandy_bild", (0.068, 0.142), T.mat("Fahrerhandy_bild", "#06080c", tex=tex("anruf_aus.png")),
                loc=(0, 0, 0.0055), rot=(0, 0, 0), parent=halter)
    if lichter:   # Lichthupe: vierstrahlige Blitze vor den Scheinwerfern, Größe 0 = aus
        flare = T.mat("Flare", "#fffbe0")
        for sx in (-1, 1):
            fl = T.empty(f"{name}_flare_{sx}", (sx * 0.6, 2.34, 0.78), root)
            for j, (w, ang) in enumerate(((1.1, 0), (1.1, 90), (0.5, 45), (0.5, -45))):
                o = T.box(f"{name}_flare_{sx}_{j}", (w, 0.012, 0.06 if w > 1 else 0.04), flare, parent=fl, line=0)
                o.rotation_euler[1] = math.radians(ang)
            fl.scale = (0.001, 0.001, 0.001)
    return root, glasobj, halter


def haus(name, x, y, breite, tiefe, hoehe, farbe, dach, seite):
    root = T.empty(name, (x, y, 0))
    T.box(f"{name}_wand", (tiefe, breite, hoehe), T.mat(f"Fassade_{farbe}", farbe), loc=(0, 0, hoehe / 2), parent=root,
          line=0.03)
    T.box(f"{name}_dach", (tiefe + 0.6, breite + 0.6, 0.5), T.mat(f"Dach_{dach}", dach), loc=(0, 0, hoehe + 0.25),
          parent=root, line=0.03)
    fen = T.mat("HausFenster", "#9cc3de")
    rahmen = T.mat("HausRahmen", "#f4f4f0")
    etagen = max(1, int(hoehe / 3.0))
    for e in range(etagen):
        for k in range(max(1, int(breite / 3.0))):
            yy = -breite / 2 + 1.5 + k * 3.0
            if yy > breite / 2 - 1.0:
                continue
            T.box(f"{name}_fenster_{e}_{k}", (0.1, 1.3, 1.4), rahmen, loc=(-seite * (tiefe / 2 + 0.03), yy, 1.6 + e * 3.0),
                  parent=root, line=0.01)
            T.box(f"{name}_glas_{e}_{k}", (0.1, 1.1, 1.2), fen, loc=(-seite * (tiefe / 2 + 0.06), yy, 1.6 + e * 3.0),
                  parent=root, line=0)


def baum(name, x, y, s=1.0):
    T.cylinder(f"{name}_stamm", 0.18 * s, 2.6 * s, T.mat("Stamm", "#6b4a32"), loc=(x, y, 1.3 * s), line=0.015)
    T.ellipsoid(f"{name}_krone", (2.6 * s, 2.6 * s, 2.9 * s),
                T.mat("Krone", ("#4f8a3e", "#5c9a47", "#467d37")[int(_hash(name, 1) * 3) % 3]),
                loc=(x, y, 3.6 * s), line=0.03, segs=16, rings=10)


def hof():
    """Hinterhof der Schule im Regen. Gibt (auto_wurzel, glas, halter) zurück."""
    asph = T.mat("HofAsphalt", "#6d7178")
    T.box("hof_boden", (60, 60, 0.2), asph, loc=(0, 20, -0.1), line=0)
    pfuetze = T.mat("Pfuetze", "#525861")
    for k in range(9):
        o = T.ellipsoid(f"pfuetze_{k}", (1.6 + _hash("p", k) * 2, 0.9 + _hash("p", k + 3), 0.01), pfuetze,
                        loc=(-8 + _hash("p", k + 5) * 16, 3 + _hash("p", k + 7) * 14, 0.006), line=0, segs=20, rings=4)
    # Schul-Rückwand mit Kellertür (Treppenschacht) und Fenstern
    wand = T.mat("Rueckwand", "#d9c7a8")
    T.box("rueckwand", (40, 0.4, 10), wand, loc=(0, -0.2, 5), line=0.02)
    T.box("tuer_rahmen", (1.3, 0.1, 2.3), T.mat("TuerRahmen", "#5d6672"), loc=(0, 0.02, 1.15), line=0.01)
    T.box("tuer_blatt", (1.05, 0.08, 2.1), T.mat("Kellertuer", "#7f8c99"), loc=(-0.45, 0.45, 1.05), line=0.01)
    T.plane("hof_notausgang", (0.5, 0.18), T.mat("HofNotausgang", "#16964f", tex=tex("notausgang.png")),
            loc=(0, 0.06, 2.55), rot=(90, 0, 180))
    fen = T.mat("RueckFenster", "#8fb3cc")
    for k in range(10):
        for e in range(2):
            x = -16 + k * 3.6
            if abs(x) < 2:
                continue
            T.box(f"rueck_fenster_{k}_{e}", (1.8, 0.1, 1.3), fen, loc=(x, 0.02, 3.6 + e * 3.4), line=0.012)
    # Müllcontainer, Fahrradständer, Zaun mit Tor
    gruen = T.mat("Container", "#3c7d4a")
    for k, x in enumerate((-6.5, -4.2)):
        T.box(f"container_{k}", (2.0, 1.3, 1.3), gruen, loc=(x, 2.5, 0.75), line=0.012, bevel=0.04)
        T.box(f"container_deckel_{k}", (2.05, 1.4, 0.08), T.mat("Deckel", "#2f6a3c"), loc=(x, 2.5, 1.44), line=0.008)
        for sx in (-1, 1):
            T.cylinder(f"container_rad_{k}_{sx}", 0.1, 0.08, T.mat("Reifen", "#18181b"), loc=(x + sx * 0.8, 2.0, 0.1),
                       axis="X", line=0.004)
    metall = T.mat("HofMetall", "#8a9099")
    for k in range(6):
        T.torus(f"radbuegel_{k}", 0.38, 0.03, metall, loc=(6 + k * 0.8, 3.0, 0.38), line=0.004, axis="X")
    for k in range(25):
        x = -12 + k * 1.2
        if 1.0 < x < 6.0:
            continue  # Tor
        T.cylinder(f"zaun_pfosten_{k}", 0.04, 2.0, metall, loc=(x, 18.5, 1.0), line=0.004, segs=8)
    for z in (0.35, 0.95, 1.55, 2.0):  # Spanndrähte statt Gittertextur (Workbench kann keine Transparenz)
        T.box(f"zaun_draht_l_{z}", (11.0, 0.03, 0.03), metall, loc=(-6.5, 18.5, z), line=0.002)
        T.box(f"zaun_draht_r_{z}", (6.0, 0.03, 0.03), metall, loc=(9.0, 18.5, z), line=0.002)
    # Turnhalle rechts hinten (Regel 6: „hinter der Turnhalle“)
    T.box("turnhalle", (14, 22, 7.5), T.mat("Turnhalle", "#c7b08f"), loc=(19, 26, 3.75), line=0.04)
    T.box("turnhalle_dach", (14.6, 22.6, 0.6), T.mat("TurnhalleDach", "#6e4b3c"), loc=(19, 26, 7.8), line=0.03)
    T.plane("turnhalle_schild", (5.0, 1.0), T.mat("Turnhalleschild", "#ffffff", tex=tex("schild_turnhalle.png")),
            loc=(11.95, 22.0, 5.8), rot=(90, 0, -90))
    for k in range(5):
        T.box(f"turnhalle_fenster_{k}", (0.1, 2.4, 1.0), fen, loc=(11.95, 17 + k * 4.0, 5.0), line=0.015)
    # Straße hinter dem Zaun, Häuser, Bäume
    T.box("hof_strasse", (60, 8, 0.05), T.mat("StrasseAsphalt", "#55595f"), loc=(0, 23, 0.02), line=0)
    for k in range(6):
        haus(f"hofhaus_{k}", -24 + k * 9.5, 33, 8, 7, 9 + 3 * _hash("hh", k),
             ("#e3cfae", "#c9d6e3", "#e6b8a2", "#d8d0c4")[k % 4], ("#7a4a3a", "#5a5f6b")[k % 2], seite=-1)
    for k in range(5):
        baum(f"hofbaum_{k}", -15 + k * 6.5 + 2 * _hash("hb", k), 21.0, 0.9 + 0.2 * _hash("hb", k + 9))
    r, g, h = auto("blaues_auto", loc=AUTO_HOF, rot=AUTO_HOF_ROT, innen=True, glas=True, tuer_hl_offen=True,
                   lichter=True)
    return r, g, h


def strasse(laenge=280.0):
    """Gerade Straße entlang +Y bis zur Ampel. Gibt die Ampel-Lichter zurück (rot/gelb/grün)."""
    T.box("str_asphalt", (9, laenge, 0.1), T.mat("StrasseAsphalt", "#55595f"), loc=(0, laenge / 2 - 10, -0.05), line=0)
    weiss = T.mat("Markierung", "#f2f2ee")
    for k in range(int(laenge / 6)):
        T.box(f"str_strich_{k}", (0.15, 3.0, 0.01), weiss, loc=(0, -8 + k * 6, 0.006), line=0)
    for sx in (-1, 1):
        T.box(f"str_gehweg_{sx}", (3.0, laenge, 0.2), T.mat("Gehweg", "#a7a39b"), loc=(sx * 6.0, laenge / 2 - 10, 0.1),
              line=0)
        T.box(f"str_bordstein_{sx}", (0.2, laenge, 0.22), T.mat("Bordstein", "#c9c5bd"), loc=(sx * 4.5, laenge / 2 - 10, 0.11),
              line=0.01)
    T.box("str_wiese", (80, laenge, 0.05), T.mat("Rasen", "#7fae5d"), loc=(0, laenge / 2 - 10, -0.12), line=0)
    farben = ("#e3cfae", "#c9d6e3", "#e6b8a2", "#d8d0c4", "#cfe0c3", "#e9d8a6")
    dach = ("#7a4a3a", "#5a5f6b", "#8a5a44")
    for sx in (-1, 1):
        y = -6.0
        k = 0
        while y < laenge - 15:
            b = 7 + 4 * _hash(f"h{sx}", k)
            haus(f"str_haus_{sx}_{k}", sx * (11.5 + 2 * _hash(f"hx{sx}", k)), y + b / 2, b, 7,
                 6 + 6 * _hash(f"hz{sx}", k), farben[(k + (sx > 0)) % len(farben)], dach[k % 3], seite=sx)
            y += b + 1.5 + 3 * _hash(f"hg{sx}", k)
            k += 1
        for j in range(int(laenge / 11)):
            baum(f"str_baum_{sx}_{j}", sx * 7.6, -4 + j * 11 + 3 * _hash(f"b{sx}", j), 0.8 + 0.3 * _hash(f"bs{sx}", j))
        for j in range(int(laenge / 25)):
            T.cylinder(f"laterne_{sx}_{j}", 0.07, 5.0, T.mat("Laterne", "#3e434b"), loc=(sx * 5.2, 4 + j * 25, 2.5),
                       line=0.008, segs=10)
            T.box(f"laternenkopf_{sx}_{j}", (0.8, 0.3, 0.14), T.mat("Laterne", "#3e434b"), loc=(sx * 4.9, 4 + j * 25, 5.0),
                  line=0.006)
    # geparkte Autos am Rand (ohne Innenraum)
    for k, (yy, c) in enumerate(((24, "#c0392b"), (67, "#ecf0f1"), (121, "#2d3436"), (178, "#f1c40f"), (222, "#8e44ad"))):
        auto(f"geparkt_{k}", farbe=c, loc=(3.4, yy, 0), rot=0, innen=False, glas=True, line=0.01)
    # wartendes Auto an der Haltelinie (Bremslichter an); das blaue Auto hält dahinter
    auto("wartend", farbe="#b8423a", loc=(SPUR_X, AMPEL_Y - 5.6, 0), rot=0, innen=False, glas=True, line=0.01)
    # Ampel rechts vor der Haltelinie
    T.box("haltelinie", (4.2, 0.4, 0.012), weiss, loc=(SPUR_X, AMPEL_Y - 3.0, 0.006), line=0)
    T.cylinder("ampel_mast", 0.09, 4.2, T.mat("AmpelMast", "#3e434b"), loc=(4.4, AMPEL_Y, 2.1), line=0.008, segs=12)
    T.box("ampel_kasten", (0.42, 0.32, 1.15), T.mat("AmpelKasten", "#202227"), loc=(4.4, AMPEL_Y - 0.18, 3.6), line=0.008,
          bevel=0.04)
    lichter = {}
    for k, (n, c) in enumerate((("rot", "#ff3b30"), ("gelb", "#ffcc00"), ("gruen", "#34c759"))):
        lichter[n] = T.mat(f"Ampel_{n}", c)
        T.cylinder(f"ampel_{n}", 0.12, 0.05, lichter[n], loc=(4.4, AMPEL_Y - 0.36, 3.95 - k * 0.35), axis="Y",
                   line=0.003, segs=20)
    return lichter

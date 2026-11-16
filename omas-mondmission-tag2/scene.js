/* Omas Mondmission – Tag 1. Schrebergarten in Kuhweide im Abendlicht: Oma Gisela (78), Kuh Berta mit Raumhelm, eine Rakete
 * aus dem alten Heizöltank und Herr Krause vom Gartenverein hinter der Hecke. Jeder Kommentar = 1 Liter Treibstoff. */
(() => {
  const { $, clamp, lerp, E, prog, popS, rng, cue, setT, disp, camLerp, OUT, sw, humanEls, humanDefaults, poseHuman,
    faceMarkup, armMarkup, envAt } = Engine;

  // ---------------------------------------------------------------- Farben
  const SKIN = '#F3CDB0', SKIN_SH = '#E3A98A';
  const HAIR = '#E6E4EE', HAIR_SH = '#B9B6C9';
  const CARDI = '#D2465E', CARDI_D = '#A93248';
  const NAVY = '#22183A';
  const W = { ground: 1500, rocket: { x: 1000, y: 1500 }, oma: { x: 1235, y: 1540, s: 1.3 }, berta: { x: 1640, y: 1550, s: 1.02 },
    krause: { x: 1965, y: 1296, s: 1.35 }, gnome: { x: 630, y: 1534 } };

  // ---------------------------------------------------------------- Definitionen
  const defs = `
  <defs>
    <linearGradient id="gSky" gradientUnits="userSpaceOnUse" x1="0" y1="-900" x2="0" y2="1330">
      <stop offset="0" stop-color="#16204F"/><stop offset=".3" stop-color="#3E3F8C"/><stop offset=".55" stop-color="#9A5A9A"/>
      <stop offset=".74" stop-color="#EE7C7C"/><stop offset=".88" stop-color="#FFAE6B"/><stop offset="1" stop-color="#FFE4A8"/>
    </linearGradient>
    <radialGradient id="gSun"><stop offset="0" stop-color="#FFFDF2"/><stop offset=".6" stop-color="#FFEFC0"/><stop offset="1" stop-color="#FFD089"/></radialGradient>
    <radialGradient id="gGlow"><stop offset="0" stop-color="#FFF0C2" stop-opacity=".95"/><stop offset=".22" stop-color="#FFD08A" stop-opacity=".55"/>
      <stop offset=".55" stop-color="#FFA070" stop-opacity=".18"/><stop offset="1" stop-color="#FF8A70" stop-opacity="0"/></radialGradient>
    <linearGradient id="gLawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9C95E"/><stop offset=".18" stop-color="#86B651"/>
      <stop offset=".6" stop-color="#5F9A43"/><stop offset="1" stop-color="#3F7A38"/></linearGradient>
    <linearGradient id="gMeadow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D8D27A"/><stop offset="1" stop-color="#93B65A"/></linearGradient>
    <linearGradient id="gHedge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4E8C45"/><stop offset="1" stop-color="#2C5E33"/></linearGradient>
    <linearGradient id="gTank" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B9DB98"/><stop offset=".16" stop-color="#8DBE78"/>
      <stop offset=".55" stop-color="#679A62"/><stop offset=".85" stop-color="#4C7A50"/><stop offset="1" stop-color="#3D6544"/></linearGradient>
    <linearGradient id="gFunnel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF9A7E"/><stop offset=".25" stop-color="#E5543F"/>
      <stop offset=".75" stop-color="#C23D33"/><stop offset="1" stop-color="#93292A"/></linearGradient>
    <linearGradient id="gPot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F0A06A"/><stop offset=".4" stop-color="#D0703F"/><stop offset="1" stop-color="#9A4A2A"/></linearGradient>
    <linearGradient id="gFin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9D0DA"/><stop offset=".5" stop-color="#7E8796"/><stop offset="1" stop-color="#555C6B"/></linearGradient>
    <radialGradient id="gGlass" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#F0FAFF"/><stop offset=".45" stop-color="#A9DAF2"/><stop offset="1" stop-color="#4E8FBF"/></radialGradient>
    <radialGradient id="gHelmet" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".42"/><stop offset=".55" stop-color="#D6EEFF" stop-opacity=".1"/>
      <stop offset=".9" stop-color="#9FD3F0" stop-opacity=".28"/><stop offset="1" stop-color="#E8F7FF" stop-opacity=".7"/></radialGradient>
    <radialGradient id="gSmoke" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFFBF4"/><stop offset=".7" stop-color="#F3E3E2"/><stop offset="1" stop-color="#D9C3CF" stop-opacity="0"/></radialGradient>
    <radialGradient id="gFireGlow"><stop offset="0" stop-color="#FFF1B0" stop-opacity=".95"/><stop offset=".4" stop-color="#FFB040" stop-opacity=".5"/><stop offset="1" stop-color="#FF6A20" stop-opacity="0"/></radialGradient>
    <radialGradient id="gLamp"><stop offset="0" stop-color="#FFF4C8" stop-opacity=".95"/><stop offset=".4" stop-color="#FFC870" stop-opacity=".35"/><stop offset="1" stop-color="#FFB050" stop-opacity="0"/></radialGradient>
    <mask id="mMoon"><circle r="56" fill="#fff"/><circle cx="24" cy="-16" r="50" fill="#000"/></mask>
    <clipPath id="cpBoard" clipPathUnits="userSpaceOnUse"><rect id="cpBoardR" x="-320" y="-1040" width="0" height="80"/></clipPath>
    <clipPath id="cpKrause" clipPathUnits="userSpaceOnUse"><rect x="1400" y="-2000" width="2000" height="3480"/></clipPath>
    <clipPath id="cpNames" clipPathUnits="userSpaceOnUse"><rect id="cpNamesR" x="-165" y="-410" width="0" height="170"/></clipPath>
    <filter id="fBlur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>
    <filter id="fBlur5" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="fBlur10" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="10"/></filter>
    <filter id="fBlur24" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="24"/></filter>
  </defs>`;

  // ---------------------------------------------------------------- Himmel
  const cloud = (x, y, s) => `
    <g class="cloud" data-x="${x}" data-y="${y}" data-s="${s}" transform="translate(${x},${y}) scale(${s})">
      <ellipse cx="0" cy="10" rx="210" ry="40" fill="#E99A9E" opacity=".85"/>
      <ellipse cx="-90" cy="-16" rx="96" ry="56" fill="#F6B4A6"/>
      <ellipse cx="20" cy="-44" rx="120" ry="74" fill="#FFC6AA"/>
      <ellipse cx="128" cy="-10" rx="86" ry="48" fill="#F8B8A4"/>
      <path d="M-200 18 Q-60 46 80 34 Q170 28 214 10" stroke="#FFE2B4" stroke-width="12" fill="none" stroke-linecap="round" opacity=".9"/>
      <ellipse cx="-30" cy="-80" rx="60" ry="22" fill="#FFD7BC" opacity=".8"/>
    </g>`;

  const skyMarkup = () => {
    const R = rng(7);
    let stars = '';
    for (let i = 0; i < 90; i++) {
      const x = -1200 + R() * 4800, y = -900 + R() * 1250, r = 1.6 + R() * 3.2;
      stars += `<circle class="star" data-p="${(R() * 6.28).toFixed(2)}" data-o="${(0.35 + 0.65 * clamp((700 - y) / 900)).toFixed(2)}" cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r.toFixed(1)}" fill="#FFF8E6"/>`;
    }
    let rays = '';
    for (let i = 0; i < 14; i++) {
      const a = (i / 14) * 360, w = i % 2 ? 7 : 12;
      rays += `<path d="M0 0 L${-w} -1400 L${w} -1400 Z" fill="#FFE6B0" opacity="${i % 2 ? 0.1 : 0.16}" transform="rotate(${a})"/>`;
    }
    return `<g id="pxSky">
      <rect x="-2200" y="-2400" width="7400" height="4300" fill="url(#gSky)"/>
      <g id="stars">${stars}</g>
      <g id="moon" transform="translate(1550,380)">
        <circle r="150" fill="#FFF3D0" opacity=".16" filter="url(#fBlur24)"/>
        <g mask="url(#mMoon)"><circle r="56" fill="#FFF4D6"/><circle cx="-24" cy="10" r="9" fill="#EADBB4"/><circle cx="-8" cy="30" r="6" fill="#EADBB4"/><circle cx="-34" cy="-16" r="5" fill="#EADBB4"/></g>
      </g>
      <g id="sunG" transform="translate(820,1170)">
        <g id="sunRays">${rays}</g>
        <circle r="640" fill="url(#gGlow)"/>
        <circle r="118" fill="url(#gSun)"/>
      </g>
      <g id="clouds">${[[-420, 760, 1.25], [380, 560, 0.85], [1450, 690, 1.3], [2380, 520, 1.0], [3150, 800, 1.15], [900, 930, 0.7], [1950, 980, 0.75]].map(([x, y, s]) => cloud(x, y, s)).join('')}</g>
    </g>`;
  };

  // ---------------------------------------------------------------- Ferne Hügel, Dorf, Kuhweide
  const house = (x, y, w, h, roof, win) => `
    <rect x="${x}" y="${y - h}" width="${w}" height="${h}" fill="#7A5288"/>
    <path d="M${x - 8} ${y - h} L${x + w / 2} ${y - h - roof} L${x + w + 8} ${y - h} Z" fill="#6A4478"/>
    ${win.map(([wx, wy]) => `<rect class="win" x="${x + wx}" y="${y - h + wy}" width="12" height="14" rx="2" fill="#FFD27A"/>`).join('')}`;
  const farMarkup = () => `<g id="pxFar">
      <path d="M-1800 1290 Q-1200 1120 -620 1220 Q-60 1110 560 1240 Q1150 1140 1720 1225 Q2300 1120 2900 1215 Q3500 1130 4300 1250 L4300 1800 L-1800 1800 Z" fill="#C98EA9"/>
      <path d="M-1800 1290 Q-1200 1120 -620 1220 Q-60 1110 560 1240 Q1150 1140 1720 1225 Q2300 1120 2900 1215 Q3500 1130 4300 1250" stroke="#FFC9A8" stroke-width="5" fill="none" opacity=".7"/>
      <g>
        ${house(1880, 1262, 70, 46, 34, [[12, 14], [44, 14]])}
        ${house(1966, 1258, 58, 40, 30, [[22, 12]])}
        <rect x="2050" y="1150" width="38" height="110" fill="#6E4780"/><path d="M2042 1150 L2069 1078 L2096 1150 Z" fill="#5E3A70"/>
        <path d="M2069 1078 L2069 1056 M2060 1066 L2078 1066" stroke="#5E3A70" stroke-width="4"/>
        <rect class="win" x="2062" y="1176" width="14" height="20" rx="7" fill="#FFD27A"/>
        ${house(2104, 1262, 76, 50, 36, [[14, 16], [48, 16]])}
        ${house(2196, 1268, 60, 40, 28, [[24, 12]])}
        ${house(2270, 1272, 66, 42, 30, [[10, 14], [40, 14]])}
      </g>
      <path d="M-1800 1330 Q-1100 1220 -400 1300 Q300 1215 1000 1305 Q1700 1230 2400 1300 Q3100 1235 4300 1320 L4300 1800 L-1800 1800 Z" fill="#A47197"/>
    </g>`;

  // Kuhweide (Wiese mit Fußballtor), hintere Hecke, Gartenlaube, Wäscheleine, Sonnenblumen
  const sunflower = (x, y, h, s, ph) => `
    <g class="sway" data-p="${ph}" transform="translate(${x},${y})">
      <path d="M0 0 Q${6 * s} ${-h / 2} 0 ${-h}" stroke="#4E8A3A" stroke-width="${9 * s}" fill="none"/>
      <path d="M0 ${-h * 0.45} Q${-40 * s} ${-h * 0.55} ${-56 * s} ${-h * 0.42} Q${-30 * s} ${-h * 0.4} 0 ${-h * 0.45} Z" fill="#5E9A43" stroke="${OUT}" stroke-width="3"/>
      <path d="M0 ${-h * 0.62} Q${40 * s} ${-h * 0.72} ${58 * s} ${-h * 0.6} Q${32 * s} ${-h * 0.57} 0 ${-h * 0.62} Z" fill="#5E9A43" stroke="${OUT}" stroke-width="3"/>
      <g transform="translate(0,${-h}) scale(${s})">
        ${Array.from({ length: 14 }, (_, i) => `<ellipse cx="0" cy="-44" rx="13" ry="28" fill="${i % 2 ? '#FFC83A' : '#FFB21E'}" stroke="${OUT}" stroke-width="3" transform="rotate(${i * 25.7})"/>`).join('')}
        <circle r="30" fill="#7A4A26" stroke="${OUT}" stroke-width="4"/><circle r="18" fill="#5C3418"/>
      </g>
    </g>`;
  const midMarkup = () => {
    const R = rng(21);
    let tufts = '';
    for (let i = 0; i < 26; i++) { const x = -900 + i * 150 + R() * 60, y = 1336 + R() * 40; tufts += `<path d="M${x} ${y} l6 -22 l6 22 l7 -16 l5 16" stroke="#7FA44A" stroke-width="4" fill="none"/>`; }
    let hedge = '';
    for (let i = 0; i < 34; i++) { const x = -900 + i * 80, y = 1392 + Math.sin(i * 1.7) * 10; hedge += `<circle cx="${x}" cy="${y}" r="${52 + (i % 3) * 8}" fill="${['#4C8A45', '#447F40', '#55944B'][i % 3]}"/>`; }
    let hl = '';
    for (let i = 0; i < 34; i++) { const x = -920 + i * 80, y = 1374 + Math.sin(i * 1.7) * 10; hl += `<ellipse cx="${x}" cy="${y}" rx="26" ry="14" fill="#7DB35A" opacity=".55"/>`; }
    return `<g id="pxMid">
      <path d="M-1400 1318 Q0 1290 1400 1312 Q2600 1296 4000 1320 L4000 1500 L-1400 1500 Z" fill="url(#gMeadow)"/>
      ${tufts}
      <g transform="translate(2280,1352)"><path d="M-46 0 L-46 -40 L46 -40 L46 0" stroke="#fff" stroke-width="6" fill="none"/><path d="M-46 -40 L-34 -30 L34 -30 L46 -40 M-34 -30 L-36 0 M34 -30 L36 0" stroke="#fff" stroke-width="2" opacity=".7" fill="none"/></g>
      <g opacity=".9">${Array.from({ length: 22 }, (_, i) => `<rect x="${1560 + i * 60}" y="1318" width="7" height="34" fill="#8A6A4A"/>`).join('')}
        <path d="M1560 1326 H2880 M1560 1340 H2880" stroke="#8A6A4A" stroke-width="4"/></g>
      <g transform="translate(2420,1344) scale(.32)" opacity=".9"><rect x="-150" y="-210" width="300" height="130" rx="56" fill="#F6F6F8"/><path d="M-60 -200 Q-20 -210 10 -190 Q16 -160 -14 -152 Q-50 -146 -66 -176 Z" fill="${OUT}"/><circle cx="-200" cy="-210" r="56" fill="#F6F6F8"/><rect x="-120" y="-100" width="26" height="100" fill="#F6F6F8"/><rect x="90" y="-100" width="26" height="100" fill="#F6F6F8"/></g>
      <g>${hedge}${hl}<rect x="-1000" y="1392" width="2860" height="110" fill="url(#gHedge)"/></g>
      <g id="shed" transform="translate(330,1468)">
        <ellipse cx="60" cy="6" rx="300" ry="20" fill="#2B3A1E" opacity=".25"/>
        <rect x="-210" y="-300" width="420" height="300" fill="#C9864F" ${sw}/>
        ${Array.from({ length: 9 }, (_, i) => `<path d="M${-210 + i * 46.6} -300 V0" stroke="#A86A3C" stroke-width="4"/>`).join('')}
        <path d="M80 -300 L210 -300 L210 0 L80 0 Z" fill="#7A3E28" opacity=".22"/>
        <path d="M-250 -296 L0 -440 L250 -296 Z" fill="#8E3D30" ${sw}/>
        <path d="M-250 -296 L0 -440 L250 -296" stroke="#B5513F" stroke-width="10" fill="none" stroke-linejoin="round"/>
        <path d="M-120 -350 Q-90 -368 -60 -356 M40 -400 Q70 -410 96 -392 M120 -340 Q150 -352 176 -330" stroke="#7DA04A" stroke-width="12" stroke-linecap="round" fill="none"/>
        <rect x="-150" y="-210" width="110" height="210" rx="6" fill="#9A5A34" ${sw}/>
        <path d="M-104 -170 q-10 -12 0 -18 q10 6 0 18 q-10 -6 0 0 Z" fill="${OUT}"/>
        <path d="M-95 -160 m-12 0 a12 12 0 1 1 24 0 l-12 14 l-12 -14 z" fill="#3A2416"/>
        <circle cx="-56" cy="-104" r="6" fill="#E8C35A" ${sw}/>
        <rect x="20" y="-232" width="130" height="100" rx="6" fill="#FFE5A8" ${sw}/>
        <path d="M85 -232 V-132 M20 -182 H150" stroke="${OUT}" stroke-width="5"/>
        <path d="M24 -228 Q50 -200 40 -140 L24 -140 Z M146 -228 Q120 -200 130 -140 L146 -140 Z" fill="#E8574F" opacity=".85"/>
        <rect x="10" y="-132" width="150" height="26" rx="4" fill="#7A4A2A" ${sw}/>
        ${[30, 58, 86, 114, 140].map((x, i) => `<circle cx="${x}" cy="-140" r="13" fill="${['#FF4B5C', '#FF7A8A', '#FF4B5C', '#FFD43B', '#FF4B5C'][i]}" stroke="${OUT}" stroke-width="3"/>`).join('')}
        <g transform="translate(-20,-262)"><rect x="-58" y="-24" width="116" height="44" rx="8" fill="#F4E9D2" ${sw}/>
          <text x="0" y="8" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="24" fill="${OUT}">PARZELLE 17</text></g>
        <g id="lantern" transform="translate(196,-246)"><circle id="lampGlow" r="120" fill="url(#gLamp)"/>
          <path d="M0 -30 V-14" stroke="${OUT}" stroke-width="4"/><rect x="-16" y="-14" width="32" height="40" rx="6" fill="#FFE9A0" ${sw}/><path d="M-20 -14 H20 M-20 26 H20" stroke="${OUT}" stroke-width="6"/></g>
      </g>
      <g id="line">
        <path d="M540 1180 V1470" stroke="#8A6040" stroke-width="12"/><path d="M528 1182 H552" stroke="#8A6040" stroke-width="8"/>
        <path id="lineP" d="M528 1190 Q760 1240 960 1196" stroke="#F4EEE4" stroke-width="4" fill="none"/>
        <g class="wash" data-x="600" data-y="1206" data-p="0"><g><path d="M-26 0 H26 L32 70 Q0 82 -32 70 Z" fill="#FFB3C7" ${sw}/><path d="M-30 52 Q0 62 30 52" stroke="#fff" stroke-width="5" fill="none"/></g></g>
        <g class="wash" data-x="686" data-y="1220" data-p="1.4"><g><path d="M-14 0 H14 L16 56 Q24 70 34 68 L36 80 Q8 84 -10 72 L-14 0 Z" fill="#7FB8E8" ${sw}/></g></g>
        <g class="wash" data-x="760" data-y="1224" data-p="2.6"><g><path d="M-40 0 H40 L46 86 L-46 86 Z" fill="#FFF6E2" ${sw}/><path d="M-40 26 H40 M-42 52 H42" stroke="#E8574F" stroke-width="7"/></g></g>
        <g class="wash" data-x="850" data-y="1216" data-p="3.3"><g><path d="M-14 0 H14 L16 56 Q24 70 34 68 L36 80 Q8 84 -10 72 L-14 0 Z" fill="#FFD43B" ${sw}/></g></g>
      </g>
      ${sunflower(130, 1500, 330, 0.95, 0.4)}${sunflower(40, 1510, 280, 0.85, 1.6)}${sunflower(570, 1505, 300, 0.9, 2.8)}
    </g>`;
  };

  // ---------------------------------------------------------------- Rakete (Ursprung: Mitte unten)
  const rivets = (y, n = 9) => Array.from({ length: n }, (_, i) => `<circle cx="${-130 + i * (260 / (n - 1))}" cy="${y}" r="5" fill="#3D6544" opacity=".8"/>`).join('');
  const TAGS = [
    { id: 'tgPot', ax: -96, ay: -64, lx: -232, ly: 50, text: 'BLUMENTOPF' },
    { id: 'tgFin', ax: 228, ay: -150, lx: 236, ly: -262, text: 'BACKBLECHE' },
    { id: 'tgPort', ax: 70, ay: -650, lx: 236, ly: -770, text: 'WASCHMASCHINE' },
    { id: 'tgNose', ax: -40, ay: -880, lx: -222, ly: -990, text: 'TRICHTER' },
  ];
  const tagMarkup = (g) => {
    const w = g.text.length * 25 + 44;
    return `<g id="${g.id}" style="display:none">
      <path d="M${g.ax} ${g.ay} L${g.lx} ${g.ly}" stroke="#fff" stroke-width="7" stroke-linecap="round"/>
      <path d="M${g.ax} ${g.ay} L${g.lx} ${g.ly}" stroke="${NAVY}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>
      <circle cx="${g.ax}" cy="${g.ay}" r="13" fill="#FFD43B" stroke="${NAVY}" stroke-width="5"/>
      <g class="lab" transform="translate(${g.lx},${g.ly})"><rect x="${-w / 2}" y="-38" width="${w}" height="72" rx="20" fill="#fff" stroke="${NAVY}" stroke-width="6"/>
        <text x="0" y="13" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="${NAVY}">${g.text}</text></g>
    </g>`;
  };
  const omaPortFace = () => `
    <g id="rkPortFace" style="display:none">
      <circle cx="0" cy="18" r="44" fill="${SKIN}" stroke="${OUT}" stroke-width="4"/>
      <circle cx="0" cy="-26" r="20" fill="${HAIR}" stroke="${OUT}" stroke-width="4"/>
      <path d="M-40 -4 Q0 -22 40 -4" stroke="#6B4A2F" stroke-width="10" fill="none"/>
      <circle cx="-17" cy="8" r="15" fill="#C99A3C" stroke="${OUT}" stroke-width="3"/><circle cx="17" cy="8" r="15" fill="#C99A3C" stroke="${OUT}" stroke-width="3"/>
      <circle cx="-17" cy="8" r="10" fill="url(#gGlass)"/><circle cx="17" cy="8" r="10" fill="url(#gGlass)"/>
      <path d="M-18 34 Q0 50 18 34 Q0 40 -18 34 Z" fill="#7A2633" stroke="${OUT}" stroke-width="3"/>
      <ellipse cx="-30" cy="28" rx="8" ry="5" fill="#FF8E9A" opacity=".7"/><ellipse cx="30" cy="28" rx="8" ry="5" fill="#FF8E9A" opacity=".7"/>
    </g>`;
  const rocketMarkup = () => {
    const R = rng(3);
    let dots = '';
    for (let i = 0; i < 16; i++) {
      const v = R(), y = -790 - v * 160, half = lerp(140, 30, v), x = (R() * 2 - 1) * half * 0.8;
      dots += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(7 + R() * 5).toFixed(1)}" fill="#FFF3EA" opacity=".92"/>`;
    }
    let bulbs = '';
    for (let i = 0; i < 13; i++) {
      const k = i / 12, x = lerp(-140, 140, k), y = -760 + Math.sin(k * Math.PI) * 30;
      bulbs += `<circle class="bulb" data-p="${(i * 1.7).toFixed(1)}" cx="${x.toFixed(0)}" cy="${(y + 8).toFixed(0)}" r="9" fill="${['#FFD43B', '#FF5C8A', '#5CC8FF', '#7EE07A'][i % 4]}" stroke="${OUT}" stroke-width="2.5"/>`;
    }
    return `
  <g id="rocket">
    <g id="rkShake">
      <ellipse id="rkShadow" cx="150" cy="8" rx="300" ry="24" fill="#2B3A1E" opacity=".3"/>
      <g id="rkGround">
        <g id="rkLadderW"><g id="rkLadder">
          <path d="M-196 0 L-158 -640 M-272 0 L-234 -640" stroke="#B5814F" stroke-width="14" stroke-linecap="round"/>
          <path d="M-196 0 L-158 -640 M-272 0 L-234 -640" stroke="${OUT}" stroke-width="3" fill="none" opacity=".5"/>
          ${Array.from({ length: 8 }, (_, i) => { const k = (i + 0.6) / 8.4; return `<path d="M${lerp(-270, -232, k)} ${-k * 640} L${lerp(-194, -156, k)} ${-k * 640}" stroke="#B5814F" stroke-width="11" stroke-linecap="round"/>`; }).join('')}
        </g>
        </g>
        <path d="M-172 -300 Q-230 -250 -228 -120 Q-226 -30 -300 -6 Q-380 14 -400 -10" stroke="#3FA45A" stroke-width="14" fill="none" stroke-linecap="round"/>
        <path d="M-172 -300 Q-230 -250 -228 -120 Q-226 -30 -300 -6 Q-380 14 -400 -10" stroke="#7FD88E" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
      </g>
      <g id="rkLift">
        <g id="rkFlame" style="display:none"></g>
        <path d="M-150 -360 L-268 -70 L-268 0 L-214 0 L-150 -130 Z" fill="url(#gFin)" ${sw}/>
        <path d="M-160 -320 L-250 -84 L-250 -14" stroke="#E6EBF1" stroke-width="5" fill="none" opacity=".8"/>
        <ellipse cx="-212" cy="-150" rx="14" ry="9" fill="#7A4A26" opacity=".55"/><ellipse cx="-190" cy="-210" rx="10" ry="7" fill="#7A4A26" opacity=".45"/>
        <path d="M150 -360 L268 -70 L268 0 L214 0 L150 -130 Z" fill="url(#gFin)" ${sw}/>
        <path d="M160 -320 L250 -84 L250 -14" stroke="#9AA3B0" stroke-width="5" fill="none" opacity=".6"/>
        <ellipse cx="214" cy="-170" rx="12" ry="8" fill="#7A4A26" opacity=".5"/>
        <g id="rkPot"><path d="M-66 -134 L66 -134 L100 -22 L-100 -22 Z" fill="url(#gPot)" ${sw}/>
          <rect x="-110" y="-30" width="220" height="30" rx="8" fill="#B65C34" ${sw}/>
          <path d="M-52 -120 L-80 -36" stroke="#F5B88A" stroke-width="6" opacity=".6"/></g>
        <rect x="-150" y="-776" width="300" height="660" rx="44" fill="url(#gTank)" ${sw}/>
        <path d="M-150 -704 Q0 -690 150 -704 M-150 -446 Q0 -432 150 -446 M-150 -190 Q0 -176 150 -190" stroke="#3D6544" stroke-width="7" fill="none" opacity=".55"/>
        <path d="M-150 -698 Q0 -684 150 -698 M-150 -440 Q0 -426 150 -440 M-150 -184 Q0 -170 150 -184" stroke="#C8E6AE" stroke-width="3" fill="none" opacity=".45"/>
        ${rivets(-746)}${rivets(-152)}
        <path d="M-132 -760 Q-140 -460 -134 -150" stroke="#E4F4D2" stroke-width="10" fill="none" opacity=".45" stroke-linecap="round"/>
        <path d="M60 -560 q30 -10 44 18 q-6 26 -34 22 q-24 -14 -10 -40 Z M-120 -300 q18 -8 28 10 q-4 18 -22 14 Z M96 -270 q20 4 18 24 q-16 12 -28 -4 Z" fill="#B8693D" opacity=".75"/>
        <text x="-6" y="-456" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="64" letter-spacing="5" fill="#F4EEDC" opacity=".93">HEIZÖL</text>
        <g transform="translate(70,-232)"><rect x="-44" y="-18" width="88" height="34" rx="5" fill="#D9DDE3" stroke="${OUT}" stroke-width="3"/>
          <text x="0" y="6" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="17" fill="${OUT}">BJ. 1974</text></g>
        <g id="rkNames" transform="translate(48,-352) rotate(-6)">
          <path d="M0 26 C-46 -6 -44 -44 -18 -46 C-6 -47 0 -38 0 -30 C0 -38 6 -47 18 -46 C44 -44 46 -6 0 26 Z" fill="none" stroke="#3D6544" stroke-width="6" stroke-linejoin="round"/>
          <path d="M0 26 C-46 -6 -44 -44 -18 -46 C-6 -47 0 -38 0 -30 C0 -38 6 -47 18 -46 C44 -44 46 -6 0 26 Z" fill="none" stroke="#B9DB98" stroke-width="2" stroke-linejoin="round" transform="translate(-2,-2)" opacity=".7"/>
          <text x="0" y="-12" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="22" fill="#2F5636">H+G</text>
          <text x="0" y="52" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="17" fill="#2F5636" opacity=".85">1974</text>
        </g>
        <g id="rkNameLayer"></g>
        <g id="rkSoot" opacity="0" filter="url(#fBlur5)">
          <ellipse cx="-60" cy="-170" rx="80" ry="46" fill="#2E2A36" opacity=".6"/><ellipse cx="70" cy="-150" rx="70" ry="40" fill="#2E2A36" opacity=".55"/>
          <ellipse cx="0" cy="-250" rx="60" ry="30" fill="#2E2A36" opacity=".35"/><ellipse cx="-110" cy="-320" rx="30" ry="50" fill="#2E2A36" opacity=".35"/>
          <ellipse cx="0" cy="-90" rx="110" ry="40" fill="#2E2A36" opacity=".6"/>
        </g>
        <g transform="translate(-96,-528) rotate(-30)"><rect x="-30" y="-10" width="60" height="20" rx="3" fill="#C8CCD3" stroke="${OUT}" stroke-width="3"/></g>
        <g transform="translate(-96,-528) rotate(30)"><rect x="-30" y="-10" width="60" height="20" rx="3" fill="#D6DAE0" stroke="${OUT}" stroke-width="3"/></g>
        <g id="rkGauge" transform="translate(-86,-214)">
          <circle r="50" fill="#FDFBF4" ${sw}/>
          <path d="M-36 20 A42 42 0 0 1 -30 -28" stroke="#FF4B5C" stroke-width="10" fill="none"/>
          ${Array.from({ length: 9 }, (_, i) => { const a = (-120 + i * 30) * Math.PI / 180; return `<path d="M${(Math.sin(a) * 34).toFixed(1)} ${(-Math.cos(a) * 34).toFixed(1)} L${(Math.sin(a) * 42).toFixed(1)} ${(-Math.cos(a) * 42).toFixed(1)}" stroke="${OUT}" stroke-width="3"/>`; }).join('')}
          <text x="0" y="30" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="14" fill="${OUT}">LITER</text>
          <g id="rkNeedle" transform="rotate(-120)"><path d="M-4 0 L0 -40 L4 0 Z" fill="#E8243B" stroke="${OUT}" stroke-width="2"/></g>
          <circle r="7" fill="${OUT}"/>
          <g transform="translate(0,66)"><rect x="-38" y="-14" width="76" height="28" rx="8" fill="#3A2E58" stroke="${OUT}" stroke-width="3"/>
            <circle id="rkLamp" cx="-22" cy="0" r="7" fill="#FF3B4E"/><text x="8" y="7" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="16" fill="#FFB3BC">LEER</text></g>
        </g>
        <g transform="translate(-150,-300)"><rect x="-26" y="-16" width="30" height="32" rx="5" fill="#9AA3B0" stroke="${OUT}" stroke-width="3"/></g>
        <g id="rkPort" transform="translate(10,-600)">
          <circle r="88" fill="#E1E7EF" ${sw}/><circle r="74" fill="#A9B5C4" stroke="${OUT}" stroke-width="3"/>
          <circle r="62" fill="url(#gGlass)" stroke="${OUT}" stroke-width="3"/>
          ${omaPortFace()}
          <path d="M-40 -30 Q-20 -52 10 -54" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".85"/>
          <circle cx="30" cy="30" r="7" fill="#fff" opacity=".6"/>
          <rect x="-102" y="-18" width="20" height="36" rx="5" fill="#C9D1DB" stroke="${OUT}" stroke-width="3"/>
          <rect x="80" y="-12" width="26" height="24" rx="6" fill="#C9D1DB" stroke="${OUT}" stroke-width="3"/>
        </g>
        <path d="M-150 -760 Q0 -700 150 -760" stroke="#2B2240" stroke-width="3" fill="none" opacity=".75"/>
        ${bulbs}
        <g id="rkNose">
          <path d="M-150 -776 L-30 -968 L30 -968 L150 -776 Z" fill="url(#gFunnel)" ${sw}/>
          ${dots}
          <path d="M-118 -790 L-26 -950" stroke="#FFC2B2" stroke-width="7" opacity=".6" stroke-linecap="round"/>
          <rect x="-22" y="-1060" width="44" height="100" rx="9" fill="url(#gFunnel)" ${sw}/>
          <rect x="-162" y="-792" width="324" height="30" rx="14" fill="#B53A30" ${sw}/>
          <path d="M0 -1060 V-1170" stroke="#8A6040" stroke-width="7"/>
          <g id="rkFlag" transform="translate(4,-1166)"><path id="rkFlagP" d="M0 0 Q30 -10 60 2 Q90 12 120 2 L120 56 Q90 66 60 56 Q30 46 0 56 Z" fill="#FFD43B" stroke="${OUT}" stroke-width="4"/>
            <g transform="translate(60,28)"><circle r="18" fill="#22183A"/><circle cx="7" cy="-5" r="16" fill="#FFD43B"/></g></g>
        </g>
        <g id="rkPaint" style="display:none"></g>
        ${TAGS.map(tagMarkup).join('')}
      </g>
    </g>
  </g>`;
  };

  // ---------------------------------------------------------------- Namen auf der Rakete (ab Tag 2)
  const NAME_ZONES = [
    [[-136, -712], [136, -712], [136, -126], [-136, -126]],          // Tank
    [[-132, -806], [132, -806], [34, -952], [-34, -952]],            // Trichter
    [[-60, -126], [60, -126], [90, -36], [-90, -36]],                // Blumentopf
  ];
  const NAME_BLOCK = [
    { c: [10, -600, 98] }, { c: [-86, -214, 60] },
    { r: [-130, -510, 120, -438] }, { r: [-134, -556, -58, -502] }, { r: [-128, -168, -44, -128] }, { r: [20, -254, 120, -210] },
  ];
  const NAME_COLORS = ['#FFF8E8', '#FFF8E8', '#FFD43B', '#FF9EC4', '#9FE1FF', '#FFF8E8', '#C9F59B'];
  const spanAt = (poly, y) => {
    const xs = [];
    for (let i = 0; i < poly.length; i++) {
      const [x1, y1] = poly[i], [x2, y2] = poly[(i + 1) % poly.length];
      if ((y >= Math.min(y1, y2)) && (y <= Math.max(y1, y2)) && y1 !== y2) xs.push(x1 + (x2 - x1) * (y - y1) / (y2 - y1));
    }
    return xs.length >= 2 ? [Math.min(...xs), Math.max(...xs)] : null;
  };
  function packNames(list, fs) {
    const R = rng(4242), out = [];
    let k = 0;
    const lineH = fs * 1.22;
    for (const poly of NAME_ZONES) {
      const ys = poly.map((p) => p[1]);
      for (let y = Math.min(...ys) + fs * 0.85; y <= Math.max(...ys) - fs * 0.15 && k < list.length; y += lineH) {
        const top = y - fs * 0.78, bot = y + fs * 0.22;
        const a = spanAt(poly, top), b = spanAt(poly, bot);
        if (!a || !b) continue;
        let free = [[Math.max(a[0], b[0]) + 6, Math.min(a[1], b[1]) - 6]];
        for (const o of NAME_BLOCK) {
          let bx = null;
          if (o.c) { const [cx, cy, r] = o.c, dy = Math.max(0, Math.max(top - cy, cy - bot)); if (dy < r) { const h = Math.sqrt(r * r - dy * dy); bx = [cx - h, cx + h]; } }
          else { const [x0, y0, x1, y1] = o.r; if (bot > y0 && top < y1) bx = [x0, x1]; }
          if (!bx) continue;
          free = free.flatMap(([f0, f1]) => (bx[1] <= f0 || bx[0] >= f1) ? [[f0, f1]] : [[f0, bx[0] - 4], [bx[1] + 4, f1]].filter(([u, v]) => v - u > fs));
        }
        for (const [f0, f1] of free) {
          let cur = f0 + R() * 6;
          while (k < list.length) {
            const nm = list[k].replace(/^@/, ''), w = nm.length * fs * 0.56 + 8;
            if (cur + w > f1) break;
            out.push({ nm, x: cur + w / 2, y: y + (R() - 0.5) * 4, rot: (R() - 0.5) * 12, c: NAME_COLORS[k % NAME_COLORS.length] });
            cur += w + 6 + R() * 6; k++;
          }
        }
      }
    }
    return { out, all: k >= list.length };
  }
  let namesCache = null;
  function namesMarkup(list) {
    const key = list.join('|');
    if (namesCache && namesCache.key === key) return namesCache.svg;
    let best = null;
    for (let fs = 26; fs >= 12; fs -= 1) { best = packNames(list, fs); best.fs = fs; if (best.all) break; }
    const svg = best.out.map((n) => `<text x="${n.x.toFixed(1)}" y="${n.y.toFixed(1)}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="${best.fs}" fill="${n.c}" stroke="${OUT}" stroke-width="${(best.fs / 7).toFixed(1)}" paint-order="stroke" transform="rotate(${n.rot.toFixed(1)} ${n.x.toFixed(1)} ${n.y.toFixed(1)})">${n.nm.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`).join('');
    namesCache = { key, svg, fs: best.fs, n: best.out.length };
    window.NAMES_INFO = { schrift: best.fs, platziert: best.out.length, gesamt: list.length };
    return svg;
  }

  // ---------------------------------------------------------------- Namenstafel „Bodenkontrolle Kuhweide“ (Entwurf)
  const BOARD = { w: 760, h: 900 };
  const boardMarkup = () => `
    <g id="board" style="display:none">
      <ellipse cx="80" cy="16" rx="420" ry="26" fill="#2B3A1E" opacity=".28"/>
      <path d="M-300 0 L-280 -360 M300 0 L280 -360" stroke="#8A5A34" stroke-width="26" stroke-linecap="round"/>
      <rect x="${-BOARD.w / 2 - 34}" y="${-BOARD.h - 320}" width="${BOARD.w + 68}" height="${BOARD.h + 68}" rx="26" fill="#B5814F" ${sw}/>
      <rect x="${-BOARD.w / 2 - 22}" y="${-BOARD.h - 308}" width="${BOARD.w + 44}" height="${BOARD.h + 44}" rx="18" fill="none" stroke="#D9A46C" stroke-width="6" opacity=".7"/>
      <rect x="${-BOARD.w / 2}" y="${-BOARD.h - 286}" width="${BOARD.w}" height="${BOARD.h}" rx="10" fill="#2F4A3A" stroke="${OUT}" stroke-width="5"/>
      <path d="M${-BOARD.w / 2 + 30} ${-BOARD.h - 250} Q0 ${-BOARD.h - 270} ${BOARD.w / 2 - 60} ${-BOARD.h - 240}" stroke="#FFFFFF" stroke-width="40" opacity=".04" fill="none"/>
      <g transform="translate(0,${-BOARD.h - 300})"><rect x="-300" y="-58" width="600" height="96" rx="20" fill="#FFD43B" stroke="${OUT}" stroke-width="7"/>
        <text x="0" y="12" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="54" fill="${OUT}">BODENKONTROLLE</text></g>
      <text x="0" y="${-BOARD.h - 190}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="#F4F1E6" opacity=".85" letter-spacing="3">KUHWEIDE · MISSION MOND</text>
      <path d="M${-BOARD.w / 2 + 40} ${-BOARD.h - 166} H${BOARD.w / 2 - 40}" stroke="#F4F1E6" stroke-width="3" opacity=".5" stroke-dasharray="14 10"/>
      <g id="boardNames"></g>
      <g id="boardChalk"><g clip-path="url(#cpBoard)"><text x="-312" y="-985" font-family="Fredoka" font-weight="600" font-size="46" fill="#FFFDF4" transform="rotate(-2 -312 -985)">DEIN NAME?</text></g>
        <g id="chalk" style="display:none"><rect x="-6" y="-46" width="16" height="56" rx="5" fill="#FFFDF4" stroke="${OUT}" stroke-width="3" transform="rotate(24)"/></g></g>
      <rect x="${BOARD.w / 2 - 120}" y="-404" width="90" height="16" rx="6" fill="#EDE6D3" transform="rotate(-8 ${BOARD.w / 2 - 75} -396)"/>
    </g>`;
  function boardSlotsMarkup(n = 24, names = []) {
    const cols = 2, rows = n / cols, top = -1000, colW = (BOARD.w - 60) / cols, lh = 56;
    let o = '';
    for (let i = 0; i < n; i++) {
      const c = Math.floor(i / rows), r = i % rows, x = -BOARD.w / 2 + 30 + c * colW + 12, y = top + r * lh + 15;
      o += `<text x="${x}" y="${y}" font-family="Fredoka" font-weight="600" font-size="30" fill="#F4F1E6" opacity="${i === 0 || i < names.length ? 0.9 : 0.4}">${i + 1}.</text>`;
      if (i < names.length) {
        const nm = names[i].replace(/^@/, '').replace(/&/g, '&amp;').replace(/</g, '&lt;');
        o += `<text class="bn" data-i="${i}" x="${x + 46}" y="${y}" font-family="Fredoka" font-weight="600" font-size="${nm.length > 14 ? 26 : 31}" fill="#FFFDF4" transform="rotate(${((i * 37) % 5) - 2} ${x + 46} ${y})">${nm}</text>`;
      } else if (i > 0) o += `<path d="M${x + 52} ${y + 2} H${x + colW - 50}" stroke="#F4F1E6" stroke-width="3" opacity=".25" stroke-dasharray="10 9"/>`;
    }
    return o + `<text x="0" y="-352" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="30" fill="#FFD43B" opacity=".9">… und Platz für alle! ⛽</text>`;
  }
  function boardNamesMarkup(list) {
    const cols = list.length > 66 ? 3 : 2, rows = Math.ceil(list.length / cols);
    const top = -BOARD.h - 120, bottom = -330, colW = (BOARD.w - 60) / cols;
    const lh = Math.min(46, (bottom - top) / Math.max(1, rows));
    const fs = Math.min(36, lh * 0.8, colW / 11);
    const R = rng(77);
    return list.map((n, i) => {
      const c = Math.floor(i / rows), r = i % rows;
      const x = -BOARD.w / 2 + 30 + c * colW + 12, y = top + r * lh + fs;
      const nm = n.replace(/^@/, '').replace(/&/g, '&amp;').replace(/</g, '&lt;');
      return `<text x="${x.toFixed(0)}" y="${y.toFixed(0)}" font-family="Fredoka" font-weight="600" font-size="${fs.toFixed(1)}" fill="#F4F1E6" opacity="${(0.82 + R() * 0.18).toFixed(2)}" transform="rotate(${((R() - 0.5) * 3).toFixed(1)} ${x.toFixed(0)} ${y.toFixed(0)})">${i + 1}. ${nm}</text>`;
    }).join('');
  }

  // ---------------------------------------------------------------- Postkarte vom Mond (Overlay, 820×540)
  const INK = '#2A3F8F';
  const postcardMarkup = () => {
    const R = rng(9);
    let st = '';
    for (let i = 0; i < 46; i++) st += `<circle cx="${(36 + R() * 748).toFixed(0)}" cy="${(36 + R() * 300).toFixed(0)}" r="${(1.4 + R() * 2.6).toFixed(1)}" fill="#FFF8E6" opacity="${(0.45 + R() * 0.55).toFixed(2)}"/>`;
    const tear = 'M18 0 L802 0 Q820 0 820 18 L820 404 L796 420 L772 402 L748 424 L722 404 L698 426 L672 406 L648 428 L622 408 L598 430 L574 410 L548 432 L522 414 L498 434 L484 470 L500 498 L482 520 L494 540 L18 540 Q0 540 0 522 L0 18 Q0 0 18 0 Z';
    const hand = (x, y, size, txt, rot, col = INK, w = 600) => `<text x="${x}" y="${y}" font-family="Fredoka" font-weight="${w}" font-size="${size}" fill="${col}" transform="rotate(${rot} ${x} ${y})">${txt}</text>`;
    return `
    <div id="postcard" class="ov"><svg viewBox="-10 -10 840 560" width="840" height="560">
      <defs>
        <linearGradient id="pcSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141A45"/><stop offset="1" stop-color="#3B3277"/></linearGradient>
        <clipPath id="pcClip"><path d="${tear}"/></clipPath>
      </defs>
      <g id="pcFront">
        <rect x="0" y="0" width="820" height="540" rx="18" fill="#FFF8E8" stroke="${NAVY}" stroke-width="8"/>
        <rect x="24" y="24" width="772" height="492" rx="8" fill="url(#pcSky)"/>
        ${st}
        <g transform="translate(112,168)"><circle r="40" fill="#4FA3E0" stroke="${NAVY}" stroke-width="3"/><path d="M-26 -12 q18 -14 34 2 q-6 18 -26 14 z M8 16 q16 -4 22 10 q-14 10 -24 0 z" fill="#5CC27A"/></g>
        <path d="M24 404 Q200 330 410 362 Q620 330 796 398 L796 516 L24 516 Z" fill="#E6DCC0"/>
        <path d="M24 404 Q200 330 410 362 Q620 330 796 398" stroke="#FFF4DA" stroke-width="6" fill="none"/>
        ${[[150, 452, 46, 12], [330, 480, 30, 9], [720, 450, 38, 10], [250, 418, 20, 6]].map(([x, y, rx, ry]) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="#CFC3A2"/><path d="M${x - rx} ${y} Q${x} ${y - ry * 1.4} ${x + rx} ${y}" stroke="#B3A684" stroke-width="3" fill="none"/>`).join('')}
        <g transform="translate(652,420)">
          <path d="M-30 0 L-30 -150 Q0 -214 30 -150 L30 0 Z" fill="#F4F4F6" stroke="${NAVY}" stroke-width="5"/>
          <path d="M-30 -62 L-58 0 L-30 0 Z M30 -62 L58 0 L30 0 Z" fill="#E8433E" stroke="${NAVY}" stroke-width="5" stroke-linejoin="round"/>
          <circle cx="0" cy="-112" r="13" fill="#8FD3F4" stroke="${NAVY}" stroke-width="4"/>
          <path d="M-30 -36 H30" stroke="#E8433E" stroke-width="9"/>
        </g>
        <g transform="translate(548,428) scale(.55)"><path d="M-30 0 Q-34 -50 0 -54 Q34 -50 30 0 Z" fill="#3F6FC2" stroke="${NAVY}" stroke-width="5"/><circle cx="0" cy="-70" r="20" fill="#F3CDB0" stroke="${NAVY}" stroke-width="5"/><path d="M-22 -64 Q0 -28 22 -64 Z" fill="#fff" stroke="${NAVY}" stroke-width="4"/><path d="M-24 -80 L4 -146 L22 -80 Z" fill="#E8433E" stroke="${NAVY}" stroke-width="5" stroke-linejoin="round"/></g>
        <g transform="translate(450,430)">
          <rect x="-24" y="-62" width="20" height="62" rx="7" fill="#F28C28" stroke="${NAVY}" stroke-width="4"/><rect x="4" y="-62" width="20" height="62" rx="7" fill="#F28C28" stroke="${NAVY}" stroke-width="4"/>
          <ellipse cx="-14" cy="2" rx="18" ry="8" fill="#3A3346"/><ellipse cx="14" cy="2" rx="18" ry="8" fill="#3A3346"/>
          <path d="M-30 -110 Q-50 -92 -48 -66" stroke="${NAVY}" stroke-width="20" stroke-linecap="round" fill="none"/><path d="M-30 -110 Q-50 -92 -48 -66" stroke="#F28C28" stroke-width="12" stroke-linecap="round" fill="none"/>
          <path id="pcWave" d="M30 -110 Q52 -132 56 -162" stroke="${NAVY}" stroke-width="20" stroke-linecap="round" fill="none"/><path d="M30 -110 Q52 -132 56 -162" stroke="#F28C28" stroke-width="12" stroke-linecap="round" fill="none"/>
          <circle cx="56" cy="-168" r="11" fill="#F1C6A0" stroke="${NAVY}" stroke-width="4"/>
          <rect x="-32" y="-124" width="64" height="74" rx="20" fill="#F28C28" stroke="${NAVY}" stroke-width="5"/>
          <path d="M-31 -86 H31" stroke="#C9601A" stroke-width="7"/><rect x="-8" y="-92" width="16" height="12" rx="3" fill="#FFD43B" stroke="${NAVY}" stroke-width="3"/>
          <circle cx="0" cy="-156" r="29" fill="#F1C6A0" stroke="${NAVY}" stroke-width="4"/>
          <path d="M-30 -160 Q-30 -192 0 -192 Q30 -192 30 -160 Q22 -178 0 -178 Q-22 -178 -30 -160 Z" fill="#6B4423" stroke="${NAVY}" stroke-width="3"/>
          <rect x="-31" y="-166" width="7" height="22" rx="3" fill="#6B4423"/><rect x="24" y="-166" width="7" height="22" rx="3" fill="#6B4423"/>
          <circle cx="-11" cy="-158" r="10" fill="#BFE6FF" fill-opacity=".6" stroke="${NAVY}" stroke-width="3.5"/><circle cx="11" cy="-158" r="10" fill="#BFE6FF" fill-opacity=".6" stroke="${NAVY}" stroke-width="3.5"/>
          <circle cx="-11" cy="-157" r="3.5" fill="${NAVY}"/><circle cx="11" cy="-157" r="3.5" fill="${NAVY}"/>
          <path d="M-14 -141 Q0 -150 14 -141 Q0 -136 -14 -141 Z" fill="#6B4423"/><path d="M-9 -134 Q0 -126 9 -134" stroke="${NAVY}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
          <circle cx="0" cy="-158" r="44" fill="#CDEBFF" fill-opacity=".16" stroke="#EAF7FF" stroke-width="5"/>
          <path d="M-30 -182 Q-18 -198 2 -200" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>
        </g>
        <text x="450" y="104" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="60" fill="#FFD43B" stroke="${NAVY}" stroke-width="12" paint-order="stroke" stroke-linejoin="round" letter-spacing="2">GRÜSSE VOM MOND</text>
        <g transform="translate(60,488) rotate(-6)"><rect x="-8" y="-30" width="98" height="40" rx="6" fill="#FFF8E8" stroke="${NAVY}" stroke-width="4"/><text x="41" y="0" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="28" fill="${NAVY}">1974</text></g>
      </g>
      <g id="pcBack" style="display:none">
        <g clip-path="url(#pcClip)">
          <rect x="0" y="0" width="820" height="540" fill="#FFF6E2"/>
          <path d="M0 0 H820 V540 H0 Z" fill="none" stroke="${NAVY}" stroke-width="16"/>
          <path d="M452 46 V390" stroke="#C9B99A" stroke-width="4"/>
          <g transform="translate(700,108) rotate(4)"><rect x="-60" y="-70" width="120" height="140" fill="#FFD43B" stroke="${NAVY}" stroke-width="4" stroke-dasharray="8 5"/>
            <rect x="-48" y="-58" width="96" height="116" fill="#2A3270"/><circle cx="-6" cy="-6" r="30" fill="#FFF4D6"/><circle cx="8" cy="-14" r="27" fill="#2A3270"/>
            <text x="0" y="48" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="17" fill="#FFD43B">MONDPOST</text></g>
          <g transform="translate(600,124) rotate(-12)" opacity=".75"><circle r="50" fill="none" stroke="#7A4A8A" stroke-width="5"/>
            <text x="0" y="-8" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="17" fill="#7A4A8A">MOND</text>
            <text x="0" y="16" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="20" fill="#7A4A8A">1974</text>
            <path d="M54 -18 Q90 -30 126 -18 M54 0 Q90 -12 126 0 M54 18 Q90 6 126 18" stroke="#7A4A8A" stroke-width="5" fill="none"/></g>
          ${hand(484, 262, 38, 'An Gisela', -2)}${hand(484, 316, 34, 'Parzelle 17', -2)}${hand(484, 368, 34, 'Kuhweide', -2)}
          <path d="M478 274 H780 M478 328 H780 M478 380 H780" stroke="#C9B99A" stroke-width="3"/>
          ${hand(40, 104, 46, 'Liebe Gisela,', -3)}
          ${hand(70, 178, 60, 'komm nach!', -4, INK, 700)}
          ${hand(110, 250, 46, 'Dein Heinz', -3)}<path transform="translate(352,232) rotate(-8) scale(1.1)" d="M0 14 C-22 -2 -20 -20 -9 -21 C-3 -21 0 -17 0 -13 C0 -17 3 -21 9 -21 C20 -20 22 -2 0 14 Z" fill="#E8433E"/>
          ${hand(40, 330, 34, 'PS: Bring Kuchen mit.', -2)}
          <text id="pcPPS" x="468" y="452" text-anchor="end" font-family="Fredoka" font-weight="700" font-size="36" fill="#D23A3A" transform="rotate(-2 468 452)">PPS: Vorsicht vor den M</text>
        </g>
        <path d="${tear}" fill="none" stroke="${NAVY}" stroke-width="7" stroke-linejoin="round"/>
      </g>
    </svg></div>`;
  };
  document.getElementById('ov').insertAdjacentHTML('beforeend', postcardMarkup());

  // ---------------------------------------------------------------- Oma Gisela (Rig wie Kalle, Füße bei 0)
  const omaMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="80" cy="6" rx="130" ry="16" fill="#2B3A1E" opacity=".26" transform="rotate(5 80 6)"/>
    <g id="${p}-bob">
      <ellipse cx="-30" cy="-11" rx="36" ry="16" fill="#FF8FBF" ${sw}/><ellipse cx="30" cy="-11" rx="36" ry="16" fill="#FF8FBF" ${sw}/>
      <circle cx="-50" cy="-22" r="13" fill="#FFD3E6" ${sw}/><circle cx="50" cy="-22" r="13" fill="#FFD3E6" ${sw}/>
      <rect x="-36" y="-66" width="24" height="52" rx="9" fill="#E7C2A2" ${sw}/><rect x="12" y="-66" width="24" height="52" rx="9" fill="#E7C2A2" ${sw}/>
      <path d="M-62 -60 L62 -60 L52 -130 L-52 -130 Z" fill="#4A4C82" ${sw}/>
      <path d="M-40 -60 L-34 -126 M0 -60 V-128 M40 -60 L34 -126" stroke="#3A3C6E" stroke-width="4"/>
      <g id="${p}-armL" transform="translate(-46,-160)">${armMarkup(p, 'L', CARDI, CARDI_D, SKIN)}</g>
      <path d="M-52 -178 Q-78 -140 -70 -84 Q0 -68 70 -84 Q78 -140 52 -178 Q0 -194 -52 -178 Z" fill="${CARDI}" ${sw}/>
      <path d="M-62 -100 Q0 -88 62 -100" stroke="${CARDI_D}" stroke-width="10" fill="none"/>
      ${[-56, -40, -24, 24, 40, 56].map((x) => `<path d="M${x} -170 V-96" stroke="#E86A80" stroke-width="3" opacity=".55"/>`).join('')}
      <path d="M-30 -182 L-36 -76 Q0 -68 36 -76 L30 -182 Q0 -170 -30 -182 Z" fill="#8CCBEE" ${sw}/>
      ${[[-18, -150], [12, -156], [-4, -128], [20, -118], [-22, -104], [6, -96]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4.5" fill="#fff"/>`).join('')}
      <path d="M-24 -116 H24 V-90 Q0 -84 -24 -90 Z" fill="#7AB8DD" stroke="${OUT}" stroke-width="3.5"/>
      <g transform="translate(14,-118) rotate(18)"><rect x="-5" y="-30" width="10" height="34" rx="3" fill="#9AA3B0" stroke="${OUT}" stroke-width="3"/><path d="M-12 -40 Q-12 -26 0 -26 Q12 -26 12 -40 L6 -40 L6 -32 L-6 -32 L-6 -40 Z" fill="#9AA3B0" stroke="${OUT}" stroke-width="3"/></g>
      <path d="M-22 -186 L0 -164 L22 -186" fill="#fff" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/>
      ${[-150, -124].map((y) => `<circle cx="-42" cy="${y}" r="6" fill="#FFD43B" stroke="${OUT}" stroke-width="3"/><circle cx="42" cy="${y}" r="6" fill="#FFD43B" stroke="${OUT}" stroke-width="3"/>`).join('')}
      <g id="${p}-armR" transform="translate(46,-160)">${armMarkup(p, 'R', CARDI, CARDI_D, SKIN)}</g>
      <g id="${p}-head">
        <circle cx="0" cy="-322" r="36" fill="${HAIR}" ${sw}/>
        <path d="M-14 -340 Q0 -350 16 -338" stroke="${HAIR_SH}" stroke-width="4" fill="none"/>
        <path d="M-40 -366 L34 -300" stroke="#E0A030" stroke-width="6" stroke-linecap="round"/><circle cx="-42" cy="-368" r="7" fill="#FF5C8A" stroke="${OUT}" stroke-width="3"/>
        ${[[-70, -262, 20], [-78, -232, 18], [-72, -204, 15], [70, -262, 20], [78, -232, 18], [72, -204, 15]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${HAIR}" ${sw}/>`).join('')}
        <ellipse cx="-66" cy="-214" rx="11" ry="15" fill="${SKIN}" stroke="${OUT}" stroke-width="4"/><circle cx="-68" cy="-196" r="5" fill="#FFF8F0" stroke="${OUT}" stroke-width="2"/>
        <ellipse cx="66" cy="-214" rx="11" ry="15" fill="${SKIN}" stroke="${OUT}" stroke-width="4"/><circle cx="68" cy="-196" r="5" fill="#FFF8F0" stroke="${OUT}" stroke-width="2"/>
        <ellipse cx="0" cy="-232" rx="66" ry="70" fill="${SKIN}" ${sw}/>
        <path d="M-62 -262 Q-56 -306 -10 -306 Q-30 -292 -34 -278 Q-14 -300 22 -302 Q4 -290 4 -280 Q30 -300 58 -284 Q66 -272 62 -258 Q40 -284 0 -282 Q-36 -282 -62 -262 Z" fill="${HAIR}" ${sw}/>
        <path d="M-66 -286 Q0 -312 66 -286" stroke="#6B4A2F" stroke-width="15" fill="none" stroke-linecap="round"/>
        <g transform="translate(-26,-294)"><circle r="23" fill="#C99A3C" ${sw}/><circle r="15" fill="url(#gGlass)" stroke="${OUT}" stroke-width="2.5"/><path d="M-8 -6 Q-2 -12 6 -10" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
        <g transform="translate(26,-294)"><circle r="23" fill="#C99A3C" ${sw}/><circle r="15" fill="url(#gGlass)" stroke="${OUT}" stroke-width="2.5"/><path d="M-8 -6 Q-2 -12 6 -10" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
        <path d="M-3 -294 H3" stroke="${OUT}" stroke-width="8"/>
        <ellipse cx="-44" cy="-196" rx="15" ry="9" fill="#FF8E9A" opacity=".55"/><ellipse cx="44" cy="-196" rx="15" ry="9" fill="#FF8E9A" opacity=".55"/>
        ${faceMarkup(p, { brow: '#C3C1D2', browW: 8, eyeRx: 16, eyeRy: 18, pup: 9 })}
        <path d="M-46 -246 Q-27 -256 -8 -246 M8 -246 Q27 -256 46 -246" stroke="${SKIN_SH}" stroke-width="4" fill="none" stroke-linecap="round"/>
        <path d="M-52 -236 l-11 -6 M-53 -228 l-12 0 M-52 -220 l-11 5 M52 -236 l11 -6 M53 -228 l12 0 M52 -220 l11 5" stroke="#C98E74" stroke-width="3" stroke-linecap="round"/>
        <path d="M-40 -208 Q-36 -200 -30 -196 M40 -208 Q36 -200 30 -196" stroke="#D99A7E" stroke-width="3" fill="none" stroke-linecap="round"/>
        <ellipse cx="0" cy="-206" rx="13" ry="11" fill="#F0B496" stroke="${OUT}" stroke-width="3.5"/>
        <circle cx="-4" cy="-210" r="3.5" fill="#fff" opacity=".7"/>
        <g id="${p}-soot" opacity="0">
          <ellipse cx="-36" cy="-252" rx="24" ry="12" fill="#3A3346" opacity=".55"/><ellipse cx="34" cy="-208" rx="19" ry="11" fill="#3A3346" opacity=".5"/>
          <ellipse cx="-14" cy="-176" rx="15" ry="7" fill="#3A3346" opacity=".42"/><ellipse cx="46" cy="-266" rx="12" ry="8" fill="#3A3346" opacity=".5"/>
          <ellipse cx="-50" cy="-206" rx="10" ry="7" fill="#3A3346" opacity=".45"/>
        </g>
        <g id="${p}-frizz" opacity="0" stroke="${HAIR}" stroke-width="7" fill="none" stroke-linecap="round">
          <path d="M-20 -350 l-10 -24 l12 -6 l-8 -22 M10 -354 l6 -26 l-10 -6 l8 -24 M34 -340 l18 -18 l-6 -10 l16 -14 M-40 -336 l-22 -14 l4 -12 l-18 -12"/>
          <path d="M-84 -250 l-22 -6 l4 -10 l-20 -8 M84 -250 l22 -6 l-4 -10 l20 -8" />
          <path d="M-20 -350 l-10 -24 l12 -6 l-8 -22 M10 -354 l6 -26 l-10 -6 l8 -24" stroke="${OUT}" stroke-width="2" opacity=".5"/>
        </g>
        <path d="M-32 -192 Q-36 -180 -28 -172 M32 -192 Q36 -180 28 -172" stroke="#D99A7E" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Kuh Berta mit Raumhelm (schaut nach links)
  const spot = (d) => `<path d="${d}" fill="${OUT}"/>`;
  const bertaMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="60" cy="6" rx="200" ry="16" fill="#2B3A1E" opacity=".25" transform="rotate(4 60 6)"/>
    <g id="${p}-bob">
      <g id="${p}-tail" transform="translate(148,-196)"><path d="M0 0 Q20 50 10 110" stroke="${OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M2 104 Q16 96 22 120 Q8 136 0 116 Z" fill="${OUT}"/></g>
      ${[96, 124].map((x) => `<rect x="${x - 15}" y="-112" width="30" height="112" rx="12" fill="#F6F6F8" ${sw}/><rect x="${x - 15}" y="-18" width="30" height="18" rx="5" fill="#59606E" ${sw}/>`).join('')}
      <rect x="-156" y="-218" width="312" height="132" rx="56" fill="#F6F6F8" ${sw}/>
      <path d="M-120 -120 Q0 -100 140 -124" stroke="#D9DAE6" stroke-width="18" fill="none" opacity=".7"/>
      ${spot('M-60 -214 Q-20 -222 10 -200 Q20 -170 -10 -160 Q-50 -150 -70 -180 Q-80 -205 -60 -214 Z')}
      ${spot('M60 -150 Q90 -170 120 -150 Q130 -120 100 -110 Q70 -100 56 -124 Z')}
      ${spot('M110 -214 Q140 -212 150 -190 Q140 -176 118 -186 Z')}
      <ellipse cx="50" cy="-86" rx="26" ry="14" fill="#FFB3C1" ${sw}/>
      ${[-110, -82].map((x) => `<rect x="${x - 15}" y="-112" width="30" height="112" rx="12" fill="#F6F6F8" ${sw}/><rect x="${x - 15}" y="-18" width="30" height="18" rx="5" fill="#59606E" ${sw}/>`).join('')}
      <g id="${p}-head">
        <path d="M-210 -270 L-226 -296 L-198 -282 Z M-144 -270 L-128 -296 L-156 -282 Z" fill="#F5E6C4" ${sw}/>
        <ellipse cx="-236" cy="-246" rx="26" ry="13" fill="#F6F6F8" ${sw} transform="rotate(-20 -236 -246)"/>
        <ellipse cx="-118" cy="-246" rx="26" ry="13" fill="#F6F6F8" ${sw} transform="rotate(20 -118 -246)"/>
        <ellipse cx="-177" cy="-222" rx="56" ry="62" fill="#F6F6F8" ${sw}/>
        ${spot('M-150 -276 Q-128 -260 -130 -232 Q-150 -226 -164 -246 Q-170 -268 -150 -276 Z')}
        <g id="${p}-eyes">
          <circle cx="-198" cy="-236" r="11" fill="#fff" stroke="${OUT}" stroke-width="3.5"/><circle cx="-156" cy="-236" r="11" fill="#fff" stroke="${OUT}" stroke-width="3.5"/>
          <circle cx="-197" cy="-234" r="6" fill="${OUT}"/><circle cx="-155" cy="-234" r="6" fill="${OUT}"/>
          <path d="M-212 -244 l-6 -6 M-142 -244 l6 -6" stroke="${OUT}" stroke-width="3" stroke-linecap="round"/>
        </g>
        <g id="${p}-muzzle">
          <ellipse cx="-177" cy="-176" rx="48" ry="32" fill="#FFB3C1" ${sw}/>
          <ellipse cx="-193" cy="-182" rx="7" ry="5" fill="#C9677A"/><ellipse cx="-161" cy="-182" rx="7" ry="5" fill="#C9677A"/>
          <path id="${p}-mouth" d="M-196 -162 Q-177 -152 -158 -162" stroke="${OUT}" stroke-width="4" fill="none" stroke-linecap="round"/>
          <ellipse id="${p}-moo" cx="-177" cy="-160" rx="14" ry="10" fill="#7A2633" stroke="${OUT}" stroke-width="3" style="display:none"/>
        </g>
        <path d="M-200 -124 Q-177 -110 -154 -124" stroke="#E23A4E" stroke-width="10" fill="none" stroke-linecap="round"/>
        <path d="M-190 -116 L-164 -116 L-158 -88 L-196 -88 Z" fill="#F2C14E" ${sw}/>
        <g id="${p}-helmet">
          <ellipse id="${p}-fog" cx="-182" cy="-196" rx="96" ry="78" fill="#F4FAFF" opacity="0" filter="url(#fBlur10)"/>
          <circle cx="-177" cy="-228" r="114" fill="url(#gHelmet)"/>
          <circle cx="-177" cy="-228" r="114" fill="none" stroke="#F2FBFF" stroke-width="7" opacity=".9"/>
          <circle cx="-177" cy="-228" r="118" fill="none" stroke="${OUT}" stroke-width="3.5" opacity=".75"/>
          <path d="M-262 -262 Q-246 -318 -192 -334" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".85"/>
          <ellipse cx="-252" cy="-232" rx="7" ry="14" fill="#fff" opacity=".7" transform="rotate(16 -252 -232)"/>
          <path d="M-96 -170 Q-84 -200 -88 -240" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity=".45"/>
          <ellipse cx="-177" cy="-120" rx="90" ry="22" fill="#B9C3D2" ${sw}/>
          <path d="M-262 -122 Q-177 -104 -92 -122" stroke="#E8EEF5" stroke-width="5" fill="none" opacity=".8"/>
          ${[-240, -205, -177, -149, -114].map((x) => `<circle cx="${x}" cy="${-116 + Math.abs(x + 177) * 0.05}" r="5" fill="#7E8898" stroke="${OUT}" stroke-width="2"/>`).join('')}
          <path d="M-150 -338 L-128 -392" stroke="${OUT}" stroke-width="5" stroke-linecap="round"/>
          <circle id="${p}-ant" cx="-126" cy="-398" r="12" fill="#FF4B5C" stroke="${OUT}" stroke-width="3.5"/>
        </g>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Herr Krause (Ursprung: Oberkante Hecke)
  const krauseMarkup = () => `
  <g id="krause">
    <g id="krBob">
      <path d="M-78 120 Q-86 10 -66 -36 Q0 -56 66 -36 Q86 10 78 120 Z" fill="#9CBFE0" ${sw}/>
      <path d="M-70 -10 H70 M-74 30 H74 M-76 70 H76 M-30 -46 V120 M30 -46 V120" stroke="#6E95BF" stroke-width="4" opacity=".7"/>
      <path d="M-78 120 Q-86 10 -66 -36 Q-40 -44 -22 -46 L-14 120 Z" fill="#C9B07E" ${sw}/>
      <path d="M78 120 Q86 10 66 -36 Q40 -44 22 -46 L14 120 Z" fill="#C9B07E" ${sw}/>
      <rect x="-64" y="20" width="34" height="28" rx="4" fill="#B79E6C" stroke="${OUT}" stroke-width="3"/><rect x="30" y="20" width="34" height="28" rx="4" fill="#B79E6C" stroke="${OUT}" stroke-width="3"/>
      <path d="M-16 -44 L0 -12 L16 -44" fill="none" stroke="#3E5C8A" stroke-width="5"/>
      <g transform="translate(-36,58)"><rect x="-26" y="-16" width="52" height="34" rx="5" fill="#fff" stroke="${OUT}" stroke-width="3"/>
        <text x="0" y="0" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="11" fill="${OUT}">VORSTAND</text>
        <text x="0" y="13" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="9" fill="#8A8B91">GARTENVEREIN</text></g>
      <rect x="-16" y="-62" width="32" height="22" fill="#EBC3A3" stroke="${OUT}" stroke-width="4"/>
      <g id="krHead">
        <ellipse cx="-54" cy="-126" rx="11" ry="16" fill="#EBC3A3" ${sw}/><ellipse cx="54" cy="-126" rx="11" ry="16" fill="#EBC3A3" ${sw}/>
        <ellipse cx="0" cy="-130" rx="54" ry="74" fill="#EBC3A3" ${sw}/>
        <g id="krSoot" opacity="0"><ellipse cx="0" cy="-120" rx="50" ry="64" fill="#3A3346"/></g>
        <g id="krHair"><path d="M-50 -170 Q-20 -214 40 -196 M-48 -160 Q-10 -206 50 -180 M-44 -150 Q0 -190 52 -166" stroke="#6E6C7C" stroke-width="5" fill="none" stroke-linecap="round"/></g>
        <g id="krHairUp" style="display:none"><path d="M-30 -196 L-40 -260 M-6 -202 L-4 -272 M18 -198 L34 -262 M38 -186 L62 -240" stroke="#6E6C7C" stroke-width="5" fill="none" stroke-linecap="round"/></g>
        <path d="M-50 -128 L-50 -150 Q-40 -170 -46 -190 M50 -128 L50 -150 Q42 -172 46 -186" stroke="#6E6C7C" stroke-width="10" fill="none" stroke-linecap="round"/>
        <rect x="-40" y="-146" width="32" height="24" rx="5" fill="#FFFFFF" fill-opacity=".35" stroke="${OUT}" stroke-width="4"/>
        <rect x="8" y="-146" width="32" height="24" rx="5" fill="#FFFFFF" fill-opacity=".35" stroke="${OUT}" stroke-width="4"/>
        <path d="M-8 -136 H8" stroke="${OUT}" stroke-width="4"/>
        <circle cx="-22" cy="-133" r="5" fill="${OUT}"/><circle cx="26" cy="-133" r="5" fill="${OUT}"/>
        <path id="krBrows" d="M-44 -156 L-10 -146 M44 -156 L10 -146" stroke="#4A4656" stroke-width="9" stroke-linecap="round"/>
        <path d="M2 -128 Q16 -96 4 -88 Q-6 -86 -6 -96" fill="#E0AE8C" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/>
        <path d="M-36 -78 Q-20 -94 0 -86 Q20 -94 36 -78 Q24 -72 12 -78 Q0 -70 -12 -78 Q-24 -72 -36 -78 Z" fill="#5A4636" ${sw}/>
        <ellipse id="krMouth" cx="0" cy="-62" rx="16" ry="11" fill="#7A2633" stroke="${OUT}" stroke-width="3.5"/>
        <path id="krMouthC" d="M-14 -62 Q0 -70 14 -62" stroke="${OUT}" stroke-width="4" fill="none" style="display:none"/>
      </g>
      <g id="krArm" transform="translate(66,-26)">
        <path d="M-16 -6 Q-4 -60 6 -104 L30 -98 Q24 -50 18 0 Z" fill="#9CBFE0" ${sw}/>
        <circle cx="18" cy="-114" r="18" fill="#EBC3A3" ${sw}/>
        <rect x="12" y="-162" width="12" height="38" rx="6" fill="#EBC3A3" ${sw}/>
      </g>
      <g id="krClip" transform="translate(-92,6) rotate(-10)">
        <rect x="-42" y="-60" width="84" height="110" rx="8" fill="#A87A4A" ${sw}/><rect x="-32" y="-46" width="64" height="88" rx="3" fill="#fff" stroke="${OUT}" stroke-width="3"/>
        <rect x="-14" y="-68" width="28" height="16" rx="4" fill="#9AA3B0" stroke="${OUT}" stroke-width="3"/>
        <text x="0" y="-12" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="30" fill="#E8243B">§17</text>
        <path d="M-22 6 H22 M-22 18 H22 M-22 30 H12" stroke="#B0B4BF" stroke-width="4"/>
        <circle cx="34" cy="20" r="16" fill="#EBC3A3" ${sw}/>
      </g>
      <g id="krSign" style="display:none" transform="translate(-70,-10) scale(.82)">
        <path d="M-6 30 V150" stroke="#8A6040" stroke-width="12"/>
        <g transform="rotate(-6)"><rect x="-170" y="-110" width="340" height="150" rx="10" fill="#E8C98E" ${sw}/>
          <text x="0" y="-52" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="46" fill="#E8243B">FRIST:</text>
          <text x="0" y="8" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="54" fill="${OUT}">SONNTAG!</text></g>
      </g>
    </g>
  </g>`;

  const bubbleMarkup = () => `
    <g id="krBubble" style="display:none">
      <path d="M-300 -150 Q-300 -230 -220 -230 L220 -230 Q300 -230 300 -150 L300 -70 Q300 10 220 10 L40 10 L-10 80 L0 10 L-220 10 Q-300 10 -300 -70 Z" fill="#fff" stroke="${NAVY}" stroke-width="9" stroke-linejoin="round"/>
      <text x="0" y="-130" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="58" fill="${NAVY}">RAKETEN SIND</text>
      <text x="0" y="-60" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="64" fill="#E8243B">VERBOTEN! §17</text>
    </g>`;

  // Hecke von Krause (Hauptebene, verdeckt ihn bis zur Brust)
  const hedgeMarkup = () => {
    let b = '';
    const hx = W.krause.x - 185;
    for (let i = 0; i < 16; i++) { const x = hx + i * 70, y = 1296 + Math.sin(i * 2.1) * 9; b += `<circle cx="${x}" cy="${y}" r="${48 + (i % 3) * 8}" fill="${['#3F7D3E', '#478A45', '#3A7339'][i % 3]}" ${i % 4 === 0 ? `stroke="${OUT}" stroke-width="0"` : ''}/>`; }
    let hl = '';
    for (let i = 0; i < 16; i++) { const x = hx - 14 + i * 70, y = 1276 + Math.sin(i * 2.1) * 9; hl += `<ellipse cx="${x}" cy="${y}" rx="24" ry="12" fill="#77B05A" opacity=".55"/>`; }
    let leaves = '';
    const R = rng(31);
    for (let i = 0; i < 46; i++) leaves += `<ellipse cx="${(hx - 20 + R() * 1100).toFixed(0)}" cy="${(1320 + R() * 160).toFixed(0)}" rx="12" ry="7" fill="${R() > 0.5 ? '#2F6634' : '#5C9A4C'}" transform="rotate(${(R() * 180).toFixed(0)} ${0} ${0})" opacity=".8"/>`;
    return `<g id="hedgeR">${b}${hl}<path d="M${hx - 50} 1300 Q${hx - 40} 1296 ${hx - 20} 1300 L${hx - 20} 1510 L${hx + 1100} 1510 L${hx + 1100} 1300 Z" fill="url(#gHedge)"/>${leaves}
      <path d="M${hx - 40} 1306 Q${hx - 50} 1400 ${hx - 34} 1508" stroke="#26512C" stroke-width="10" fill="none" opacity=".6"/></g>`;
  };

  // Gartenzwerg mit Fernglas
  const gnomeMarkup = () => `
    <g id="gnome">
      <ellipse cx="34" cy="4" rx="56" ry="9" fill="#2B3A1E" opacity=".25"/>
      <g id="gnBob">
        <rect x="-26" y="-30" width="22" height="30" rx="6" fill="#6B4A2F" ${sw}/><rect x="4" y="-30" width="22" height="30" rx="6" fill="#6B4A2F" ${sw}/>
        <path d="M-38 -24 Q-44 -90 0 -96 Q44 -90 38 -24 Z" fill="#3F6FC2" ${sw}/>
        <path d="M-34 -50 H34" stroke="#2A4D92" stroke-width="8"/>
        <circle cx="0" cy="-118" r="28" fill="${SKIN}" ${sw}/>
        <path d="M-28 -112 Q-30 -60 0 -52 Q30 -60 28 -112 Q14 -100 0 -104 Q-14 -100 -28 -112 Z" fill="#fff" ${sw}/>
        <g id="gnHat"><path d="M-32 -128 Q0 -138 32 -128 L6 -206 Q0 -212 -4 -204 Z" fill="#E8433E" ${sw}/></g>
        <g transform="translate(0,-122)"><rect x="-26" y="-10" width="22" height="20" rx="6" fill="#2B2240"/><rect x="4" y="-10" width="22" height="20" rx="6" fill="#2B2240"/>
          <circle cx="-15" cy="0" r="5" fill="#8FD3F4"/><circle cx="15" cy="0" r="5" fill="#8FD3F4"/></g>
        <circle cx="-30" cy="-112" r="11" fill="${SKIN}" ${sw}/><circle cx="30" cy="-112" r="11" fill="${SKIN}" ${sw}/>
      </g>
    </g>`;

  // Rasen, Gemüsebeet, Trittsteine, Vordergrund
  const lawnMarkup = () => {
    const R = rng(11);
    let tufts = '';
    for (let i = 0; i < 60; i++) { const x = -400 + R() * 3200, y = 1540 + R() * 520, s = 0.7 + R() * 0.9; tufts += `<path d="M${x.toFixed(0)} ${y.toFixed(0)} l${(5 * s).toFixed(1)} ${(-20 * s).toFixed(1)} l${(5 * s).toFixed(1)} ${(20 * s).toFixed(1)} l${(6 * s).toFixed(1)} ${(-15 * s).toFixed(1)} l${(5 * s).toFixed(1)} ${(15 * s).toFixed(1)}" stroke="#4E8A3C" stroke-width="4" fill="none" opacity=".8"/>`; }
    let flowers = '';
    for (let i = 0; i < 40; i++) { const x = -300 + R() * 3000, y = 1500 + R() * 600; flowers += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(5 + R() * 4).toFixed(1)}" fill="${['#FFF', '#FFD43B', '#FF8FBF', '#B98CFF'][i % 4]}" opacity=".9"/>`; }
    return `<g id="lawn">
      <path d="M-1400 1478 Q0 1462 1400 1476 Q2700 1466 4000 1480 L4000 3000 L-1400 3000 Z" fill="url(#gLawn)"/>
      <path d="M-1400 1478 Q0 1462 1400 1476 Q2700 1466 4000 1480" stroke="#C7DE84" stroke-width="6" fill="none" opacity=".6"/>
      ${[[420, 1560, 70], [560, 1640, 80], [720, 1730, 90], [900, 1830, 100]].map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 0.32}" fill="#C9BBA6" stroke="${OUT}" stroke-width="3"/><ellipse cx="${x - r * 0.2}" cy="${y - r * 0.08}" rx="${r * 0.5}" ry="${r * 0.12}" fill="#E6DCCB"/>`).join('')}
      <g transform="translate(-180,1600)"><rect x="-200" y="-30" width="460" height="80" rx="20" fill="#7A5236" stroke="${OUT}" stroke-width="4"/>
        ${[-150, -60, 30, 120, 210].map((x, i) => `<g transform="translate(${x},${-14 + (i % 2) * 8})"><circle r="34" fill="#7DBF5A" ${sw}/><path d="M-20 -8 Q0 -30 20 -8 M-26 6 Q0 -12 26 6" stroke="#4E8A3C" stroke-width="4" fill="none"/><circle r="12" fill="#A9DC7E"/></g>`).join('')}</g>
      ${tufts}${flowers}
    </g>`;
  };
  const fgMarkup = () => `
    <g id="fg" filter="url(#fBlur5)">
      <path d="M-500 2020 Q-300 1820 -120 2000 Q-40 1860 80 2010 Q160 1880 260 2030 L260 2200 L-500 2200 Z" fill="#3F7A38"/>
      <path d="M2000 2030 Q2120 1860 2240 2010 Q2330 1880 2440 2020 Q2560 1850 2700 2040 L2700 2200 L2000 2200 Z" fill="#3F7A38"/>
      ${[[-60, 1930, '#FF8FBF'], [140, 1950, '#FFD43B'], [2200, 1940, '#FFF'], [2380, 1960, '#B98CFF']].map(([x, y, c]) => `<g transform="translate(${x},${y})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-16" rx="10" ry="18" fill="${c}" transform="rotate(${a})"/>`).join('')}<circle r="9" fill="#FFB21E"/></g>`).join('')}
    </g>`;

  const knockMarkup = () => `
    <g id="knock" style="display:none">
      <path d="M40 -22 L260 -40 L260 40 L40 26 Z" fill="${CARDI}" ${sw}/>
      <rect x="30" y="-30" width="30" height="62" rx="10" fill="${CARDI_D}" ${sw}/>
      <circle cx="0" cy="0" r="34" fill="${SKIN}" ${sw}/>
      <path d="M-22 -22 Q-34 -10 -26 4 M-26 4 Q-34 16 -22 26" stroke="${OUT}" stroke-width="4" fill="none"/>
    </g>`;

  // ---------------------------------------------------------------- Welt
  const world = () => `${defs}
    ${skyMarkup()}${farMarkup()}${midMarkup()}
    <g id="lawnW">${lawnMarkup()}</g>
    <g clip-path="url(#cpKrause)"><g id="krauseW" transform="translate(${W.krause.x},${W.krause.y}) scale(${W.krause.s})">${krauseMarkup()}</g></g>
    ${hedgeMarkup()}
    <g id="bubbleW" transform="translate(${W.krause.x - 170},${W.krause.y - 340})">${bubbleMarkup()}</g>
    <g id="smokeB"></g>
    <g id="gnomeW" transform="translate(${W.gnome.x},${W.gnome.y}) scale(1.05)">${gnomeMarkup()}</g>
    <g id="rocketW" transform="translate(${W.rocket.x},${W.rocket.y})">${rocketMarkup()}</g>
    <g id="omaW">${omaMarkup('om')}</g>
    <g id="bertaW">${bertaMarkup('bb')}</g>
    <g id="knockW">${knockMarkup()}</g>
    <g id="boardW" transform="translate(330,1560) scale(.62)">${boardMarkup()}</g>
    <g id="smokeF"></g>
    <g id="fireGlow" style="display:none"><circle r="420" fill="url(#gFireGlow)"/></g>
    ${fgMarkup()}`;

  // ---------------------------------------------------------------- Zustand und Schnitte
  const OM = humanEls('om', 46);
  const base = () => ({
    oma: Object.assign(humanDefaults(), { show: true, x: W.oma.x, y: W.oma.y, s: W.oma.s, cap: false, armL: 12, armR: -12, fist: false, soot: 0 }),
    berta: { show: true, x: W.berta.x, y: W.berta.y, s: W.berta.s, moo: false, fog: 0 },
    krause: { up: 0, wag: false, mouth: false, sign: false, blown: false, soot: 0, bubble: null },
    rocket: { lift: 0, fire: 0, shake: 0, ignite: null, portFace: false, needle: 0, tags: null, paint: null, puff: false, names: null, tilt: 0, soot: 0, boom: null },
    knock: null, hook: null, hud: null, demo: null, cta: null, flash: null, grade: 0, gnomeHat: null, board: (window.TANK || {}).namen || [], boardWrite: null, postcard: null, boardPop: null, boomText: null,
    ui: { title: 999 },
  });

  const shots = {
    s01: (S, t, seg, lt, d) => {
      // Kalter Einstieg: die Testzündung explodiert schon im ersten Bild
      const B0 = -0.12, bl = t - B0;
      S.rocket.boom = B0; S.rocket.ignite = B0; S.rocket.fire = clamp(1 - bl / 0.45);
      S.rocket.lift = bl < 0.8 ? 190 * Math.sin(Math.PI * clamp(bl / 0.8)) : 0;
      S.rocket.tilt = bl < 0.8 ? 9 * clamp(bl / 0.4) : 5 + 2 * Math.exp(-(bl - 0.8) * 6) * Math.cos((bl - 0.8) * 20);
      S.rocket.soot = clamp(bl * 2.5); S.rocket.needle = 0; S.rocket.puffK = clamp(1 - (bl - 0.9) / 1.3);
      S.cam = camLerp([1235, 1300, 1.0], [1300, 1310, 1.14], E.inOut(clamp(lt / d)));
      S.shake = 1.3 * Math.exp(-bl * 2.6);
      S.oma.soot = 1; S.oma.expr = bl < 1.1 ? 'o' : 'smile'; S.oma.look = [0, 0]; S.oma.armL = 40; S.oma.armR = -40;
      S.berta.fog = 1; S.gnomeHat = B0 + 0.05;
      S.hook = { t0: -1, t1: seg.end - 0.15 }; S.boomText = { t0: -0.2, t1: 1.25 };
    },
    s02: (S, t, seg, lt) => {
      S.cam = camLerp([955, 1286, 2.0], [960, 1288, 2.12], clamp(lt / 2));
      S.rocket.tilt = 5; S.rocket.soot = 1; S.rocket.needle = (window.TANK || {}).liter / 100 || 0;
      S.hud = { t0: seg.start + 0.1, value: (window.TANK || {}).liter || 0 };
      S.knock = [cue('s02', 'klong', 0)];
      S.oma.show = false;
    },
    s03: (S, t, seg, lt, d) => {
      S.cam = camLerp([1250, 1330, 1.42], [1255, 1325, 1.5], clamp(lt / d));
      S.rocket.tilt = 5; S.rocket.soot = 1;
      S.oma.soot = 1; S.oma.expr = 'happy'; S.oma.look = [-4, -9]; S.oma.armR = -40; S.oma.armL = 40; S.berta.fog = 0.8;
      S.postcard = { t0: seg.start - 0.05, out: seg.end - 0.1 };
    },
    s04: (S, t, seg, lt, d) => {
      S.cam = camLerp([360, 1200, 1.4], [330, 1205, 1.8], E.inOut(clamp(lt / 0.9)));
      S.boardPop = seg.start + 0.35; S.hearts = [seg.start + 1.6, seg.start + 1.9];
      S.rocket.tilt = 5; S.rocket.soot = 1; S.oma.show = false;
    },
    s05: (S, t, seg, lt) => {
      S.cam = camLerp([1930, 1150, 1.25], [1935, 1140, 1.32], clamp(lt / 3));
      S.krause.up = E.back(prog(lt, 0.15, 0.4)); S.krause.sign = true; S.krause.signT0 = cue('s05', 'stamp') - 0.05; S.krause.mouth = lt > 0.4;
      S.rocket.tilt = 5; S.rocket.soot = 1;
    },
    s06: (S, t, seg, lt) => {
      S.cam = camLerp([1395, 1325, 1.06], [1400, 1322, 1.1], clamp(lt / 3));
      S.rocket.tilt = 5; S.rocket.soot = 1; S.rocket.needle = (window.TANK || {}).liter / 100 || 0;
      S.hud = { t0: seg.start + 0.05, value: (window.TANK || {}).liter || 0, big: true };
      S.cta = seg.start + 0.25;
      S.oma.soot = 1; S.oma.expr = 'smile'; S.oma.armR = -168; S.oma.fingerR = true; S.oma.look = [0, -6];
      const m = cue('s06', 'moo'); S.berta.moo = t > m && t < m + 0.8; S.berta.fog = 0.6 + 0.4 * clamp((t - m) * 3);
    },
    boardTest: (S) => {
      S.cam = [760, 1080, 0.95]; S.board = window.TEST_NAMES || []; S.oma.expr = 'happy'; S.oma.talk = false; S.oma.armL = 150; S.oma.x = 960;
    },
    boardClose: (S) => {
      S.cam = [470, 1015, 1.75]; S.board = window.TEST_NAMES || []; S.oma.show = false;
    },
    namesTest: (S) => {
      S.cam = [1180, 1000, 1.0]; S.rocket.names = window.TEST_NAMES || []; S.oma.talk = false; S.oma.expr = 'happy'; S.oma.armR = -150; S.oma.fingerR = true;
    },
    namesClose: (S) => {
      S.cam = [1000, 1080, 1.75]; S.rocket.names = window.TEST_NAMES || [];
    },
    cover: (S, t) => {
      S.cam = [1250, 1390, 1.28]; S.gnomeHat = t - 0.4;
      S.rocket.boom = t - 0.3; S.rocket.ignite = t - 0.3; S.rocket.tilt = 7; S.rocket.soot = 1; S.rocket.lift = 120; S.rocket.smokeK = 0.45; S.rocket.fire = 0.8;
      S.oma.soot = 1; S.oma.expr = 'o'; S.oma.talk = false; S.oma.armL = 60; S.oma.armR = -60; S.berta.fog = 1;
    },
  };

  // ---------------------------------------------------------------- Zeichnen
  const om = () => document.getElementById('omaW');
  const bq = (k) => document.getElementById(`bb-${k}`);
  const MR = rng(77);
  const motes = Array.from({ length: 30 }, () => ({ x: MR() * 1080, y: 300 + MR() * 1300, v: 10 + MR() * 22, r: 2 + MR() * 3.5, p: MR() * 6.28 }));
  const SR = rng(55);
  const puffs = Array.from({ length: 46 }, (_, i) => ({ side: i % 2 ? 1 : -1, d: SR() * 0.9, v: 220 + SR() * 520, up: 30 + SR() * 140, r: 50 + SR() * 70, ph: SR() * 6 }));
  let lastS = null;
  const DR = rng(808);
  const DEBRIS = Array.from({ length: 14 }, (_, i) => ({ a: -Math.PI / 2 + (DR() - 0.5) * 2.4, v: 650 + DR() * 700, r: DR() * 360, vr: (DR() - 0.5) * 1400,
    s: 0.8 + DR() * 1.2, c: ['#C8683E', '#B65C34', '#7E8796', '#5E8F5A', '#E8433E'][i % 5] }));
  const COVER = Array.from({ length: 16 }, (_, i) => ({ x: 680 + DR() * 1250, y: 1400 + DR() * 260, r: 130 + DR() * 140, dx: (DR() - 0.5) * 120 }));

  function poseBerta(P, t) {
    setT(bq('bob'), `translate(0,${Math.sin(t * 3) * 2})`);
    setT(bq('tail'), `translate(148,-196) rotate(${Math.sin(t * 4) * 12})`);
    setT(bq('head'), `rotate(${Math.sin(t * 1.7) * 2 + (P.moo ? -7 : 0)} -150 -150)`);
    disp(bq('moo'), P.moo); disp(bq('mouth'), !P.moo);
    bq('fog').setAttribute('opacity', (0.97 * clamp(P.fog)).toFixed(3));
    bq('ant').setAttribute('fill', Math.sin(t * 6) > 0 ? '#FF4B5C' : '#FFB3BC');
  }

  function poseKrause(K, t) {
    const up = K.up;
    setT($('krauseW'), `translate(${W.krause.x},${W.krause.y + (1 - up) * 420}) scale(${W.krause.s})`);
    setT($('krBob'), `translate(0,${Math.sin(t * 3.4) * 3})`);
    const wag = K.wag ? Math.sin(t * 14) * 14 : 0;
    setT($('krArm'), `translate(66,-26) rotate(${wag})`);
    disp($('krArm'), !K.sign); disp($('krClip'), !K.sign); disp($('krSign'), K.sign);
    if (K.sign) setT($('krSign'), `translate(-30,-150) scale(${(0.9 * (K.signT0 !== undefined ? popS(t, K.signT0, 0.25) : 1)).toFixed(3)}) rotate(-4)`);
    disp($('krMouth'), K.mouth); disp($('krMouthC'), !K.mouth);
    if (K.mouth) setT($('krMouth'), `translate(0,-62) scale(1,${0.7 + 0.4 * Math.abs(Math.sin(t * 11))}) translate(0,62)`);
    disp($('krHair'), !K.blown); disp($('krHairUp'), K.blown);
    $('krSoot').setAttribute('opacity', (0.75 * K.soot).toFixed(2));
    const b = $('krBubble');
    if (K.bubble !== null && t >= K.bubble && up > 0.5) {
      const s = popS(t, K.bubble, 0.3);
      disp(b, true); setT(b, `translate(0,${(1 - up) * 420}) scale(${Math.max(0.001, s)}) rotate(${Math.sin(t * 7) * 1.5})`);
    } else disp(b, false);
  }

  function drawRocket(S, t) {
    const R = S.rocket;
    const fall = R.lift > 0 ? E.in(clamp(R.lift / 260)) : 0;
    setT($('rkLadder'), `rotate(${-fall * 62} -234 0)`);
    disp($('rkGround'), true);
    setT($('rkLift'), `translate(${R.lift > 0 ? Math.sin(t * 40) * 3 : 0},${-R.lift}) rotate(${R.tilt + (R.lift > 0 ? Math.sin(t * 6) * 1.2 : 0)})`);
    $('rkSoot').setAttribute('opacity', R.soot.toFixed(2));
    $('rkShadow').setAttribute('opacity', (0.3 * clamp(1 - R.lift / 500)).toFixed(2));
    setT($('rkNeedle'), `rotate(${-120 + R.needle * 240})`);
    $('rkLamp').setAttribute('fill', Math.sin(t * 7) > -0.2 ? '#FF3B4E' : '#6E2633');
    disp($('rkPortFace'), R.portFace);
    setT($('rkFlagP'), `skewY(${Math.sin(t * 5) * 4})`);
    document.querySelectorAll('.bulb').forEach((el) => el.setAttribute('opacity', (0.55 + 0.45 * Math.sin(t * 3.2 + +el.dataset.p)).toFixed(2)));
    // Beschriftungen
    for (const g of TAGS) {
      const el = $(g.id), t0 = R.tags ? R.tags[g.id] : null;
      if (t0 === null || t0 === undefined || t < t0) { disp(el, false); continue; }
      disp(el, true);
      const s = popS(t, t0, 0.3);
      setT(el.querySelector('.lab'), `translate(${g.lx},${g.ly}) scale(${Math.max(0.001, s)}) rotate(${Math.sin(t * 3 + g.lx) * 2})`);
      el.querySelector('path').setAttribute('opacity', clamp(s));
    }
    // Namen der Tankenden (ab Tag 2) statt Hinweis und „DEIN NAME?“
    const nl = $('rkNameLayer');
    if (R.names && R.names.length) { nl.innerHTML = namesMarkup(R.names); disp($('rkNames'), false); }
    else { if (nl.innerHTML) nl.innerHTML = ''; disp($('rkNames'), true); }
    // Name auf die Rakete malen
    const P = R.paint, pr = P ? clamp((t - P.t0) / P.d) : 0;
    $('cpNamesR').setAttribute('width', (pr * 330).toFixed(1));
    disp($('rkNamesHint'), pr <= 0); disp($('rkNamesHint2'), pr <= 0);
    const pb = $('rkPaint');
    if (P && t >= P.t0 - 0.3 && t < P.t0 + P.d + 0.5) {
      const bx = -150 + pr * 300, by = -350 + Math.sin(pr * 30) * 12 + pr * 30 - (t < P.t0 ? (P.t0 - t) * 200 : 0) - (t > P.t0 + P.d ? (t - P.t0 - P.d) * 260 : 0);
      disp(pb, true);
      pb.innerHTML = `<g transform="translate(${bx.toFixed(1)},${by.toFixed(1)}) rotate(28)"><rect x="-9" y="-150" width="18" height="120" rx="8" fill="#C8763E" stroke="${OUT}" stroke-width="4"/>
        <rect x="-13" y="-40" width="26" height="22" rx="3" fill="#C9D1DB" stroke="${OUT}" stroke-width="4"/><path d="M-13 -18 Q-14 10 0 22 Q14 10 13 -18 Z" fill="${NAVY}" stroke="${OUT}" stroke-width="3"/></g>`;
    } else disp(pb, false);
    // Feuer und Rauch
    const fl = $('rkFlame');
    if (R.fire > 0) {
      disp(fl, true);
      const f = R.fire, len = (160 + 120 * Math.sin(t * 31) * 0.3 + 90 * Math.sin(t * 17)) * f;
      const w = 90 * f;
      fl.innerHTML = `<g transform="translate(0,-12)">
        <path d="M${-w} 0 Q${-w * 0.9} ${len * 0.6} 0 ${len * 1.25} Q${w * 0.9} ${len * 0.6} ${w} 0 Z" fill="#FF7A1E" opacity=".95"/>
        <path d="M${-w * 0.7} 0 Q${-w * 0.6} ${len * 0.5} 0 ${len} Q${w * 0.6} ${len * 0.5} ${w * 0.7} 0 Z" fill="#FFC23A"/>
        <path d="M${-w * 0.4} 0 Q${-w * 0.3} ${len * 0.35} 0 ${len * 0.65} Q${w * 0.3} ${len * 0.35} ${w * 0.4} 0 Z" fill="#FFF6D6"/></g>`;
    } else disp(fl, false);
    const gl = $('fireGlow');
    if (R.fire > 0) { disp(gl, true); setT(gl, `translate(${W.rocket.x},${W.rocket.y - R.lift + 60}) scale(${(0.8 + 0.15 * Math.sin(t * 23)) * R.fire})`); }
    else disp(gl, false);
    let back = '', front = '';
    if (R.ignite !== null && t > R.ignite) {
      const lt = t - R.ignite;
      for (const p of puffs) {
        const a = lt - p.d;
        if (a <= 0) continue;
        const k = 1 - Math.exp(-a * 1.6);
        const x = W.rocket.x + p.side * (40 + p.v * k), y = W.rocket.y - 10 - p.up * k * 0.9 - a * 18;
        const r = p.r * (0.5 + 1.5 * k) * (1 + 0.06 * Math.sin(t * 3 + p.ph));
        const o = clamp(a * 4) * clamp(2.6 - a * 0.55) * (R.puffK ?? 1);
        const c = `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r.toFixed(0)}" fill="url(#gSmoke)" opacity="${o.toFixed(2)}"/>`;
        if (p.ph > 3) front += c; else back += c;
      }
      // Rauchsäule unter der aufsteigenden Rakete
      for (let i = 0; i < 12; i++) {
        const yy = W.rocket.y - (R.lift * i / 12) + 30;
        const r = 70 + i * 6 + 10 * Math.sin(t * 5 + i);
        if (R.lift > 40) back += `<circle cx="${(W.rocket.x + Math.sin(i * 1.7 + t) * 22).toFixed(0)}" cy="${yy.toFixed(0)}" r="${r.toFixed(0)}" fill="url(#gSmoke)" opacity=".85"/>`;
      }
    }
    if (R.puff) {
      // Leerlauf: kleine Wölkchen aus dem Blumentopf
      for (let i = 0; i < 6; i++) {
        const a = ((t + i * 0.37) % 2.2) / 2.2;
        const x = W.rocket.x + (i % 2 ? 1 : -1) * (30 + a * 120), y = W.rocket.y - 6 - a * 60;
        front += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(16 + a * 30).toFixed(0)}" fill="url(#gSmoke)" opacity="${(Math.sin(a * Math.PI) * 0.8).toFixed(2)}"/>`;
      }
    }
    if (R.boom !== null && t >= R.boom) {
      // Explosion: Feuerball, Scherben, dichte Rauchwolke, die sich verzieht
      const lt = t - R.boom, bx = W.rocket.x, by = W.rocket.y - 60;
      const co = clamp(1 - (lt - 0.1) / 1.4) * (R.smokeK ?? 1);
      if (co > 0) for (const c of COVER) {
        const g = 1 + 0.3 * clamp(lt);
        front += `<circle cx="${(c.x + c.dx * lt).toFixed(0)}" cy="${(c.y - 40 * lt).toFixed(0)}" r="${(c.r * g).toFixed(0)}" fill="url(#gSmoke)" opacity="${(0.92 * co).toFixed(2)}"/>`;
      }
      if (lt < 0.8) {
        const r = 90 + 380 * E.out(clamp(lt / 0.6)), o = clamp(1 - lt / 0.8);
        front += `<circle cx="${bx}" cy="${by}" r="${r.toFixed(0)}" fill="#FF8A2A" opacity="${(0.8 * o).toFixed(2)}"/>`;
        front += `<circle cx="${bx}" cy="${by - 20}" r="${(r * 0.66).toFixed(0)}" fill="#FFD44A" opacity="${(0.88 * o).toFixed(2)}"/>`;
        front += `<circle cx="${bx}" cy="${by - 30}" r="${(r * 0.34).toFixed(0)}" fill="#FFF6D6" opacity="${clamp(1 - lt / 0.45).toFixed(2)}"/>`;
      }
      for (const d of DEBRIS) {
        if (lt > 1.8) break;
        const x = bx + Math.cos(d.a) * d.v * lt, y = by + Math.sin(d.a) * d.v * lt + 1700 * lt * lt;
        front += `<g transform="translate(${x.toFixed(0)},${y.toFixed(0)}) rotate(${(d.r + d.vr * lt).toFixed(0)}) scale(${d.s})"><path d="M-16 -10 L18 -14 L12 12 L-14 8 Z" fill="${d.c}" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/></g>`;
      }
      // Rauchfäden über Omas Kopf
      if (lt > 0.8 && lt < 6) for (let i = 0; i < 4; i++) {
        const a = ((lt * 0.8 + i * 0.25) % 1);
        front += `<circle cx="${(W.oma.x + Math.sin(a * 6 + i) * 20).toFixed(0)}" cy="${(W.oma.y - 470 - a * 160).toFixed(0)}" r="${(14 + a * 26).toFixed(0)}" fill="#8E8794" opacity="${(Math.sin(a * Math.PI) * 0.55).toFixed(2)}"/>`;
      }
    }
    $('smokeB').innerHTML = back; $('smokeF').innerHTML = front;
  }

  function drawOverlay(S, t) {
    const [cx, cy, z] = S.cam;
    const toScreen = (wx, wy) => [540 + (wx - cx) * z, 960 + (wy - cy) * z];
    // Schlagzeile
    const hk = $('hook');
    if (S.hook && t >= S.hook.t0 && t < S.hook.t1 + 0.25) {
      const s = popS(t, S.hook.t0, 0.35) * (1 - E.in(prog(t, S.hook.t1, 0.25)));
      hk.style.display = 'block'; hk.style.opacity = clamp(s * 3);
      hk.style.transform = `translateX(-50%) rotate(-2deg) scale(${Math.max(0.001, s) * (1 + 0.015 * Math.sin(t * 5))})`;
    } else hk.style.display = 'none';
    // Tankanzeige
    const hud = $('tankHud');
    if (S.hud && t >= S.hud.t0) {
      const s = popS(t, S.hud.t0, 0.35);
      hud.style.display = 'block';
      hud.style.transform = `translateX(-50%) scale(${Math.max(0.001, s) * (S.hud.big ? 1.06 + 0.025 * Math.sin(t * 6) : 1)})`;
      $('thVal').textContent = S.hud.value;
      $('thFill').style.width = `${S.hud.value}%`;
      $('thZero').style.opacity = S.hud.value > 0 ? 0 : (Math.sin(t * 7) > -0.2 ? 1 : 0.25);
    } else hud.style.display = 'none';
    // Beispiel-Kommentar fliegt in den Tank
    const dm = $('demo'), pl = $('plus');
    if (S.demo && t >= S.demo.t0) {
      const s = popS(t, S.demo.t0, 0.3), f = E.in(prog(t, S.demo.fly, 0.35));
      dm.style.display = 'flex';
      dm.style.opacity = clamp(s * 3) * (1 - clamp((f - 0.85) * 7));
      dm.style.transform = `translate(0px,${-f * 300}px) rotate(${-2 + f * 8}deg) scale(${Math.max(0.001, s * lerp(1, 0.18, f))})`;
      if (t >= S.demo.plus) {
        const k = prog(t, S.demo.plus, 1.1);
        pl.style.display = 'block'; pl.style.opacity = clamp((1 - k) * 3);
        pl.style.transform = `translateX(-50%) translateY(${-k * 70}px) scale(${popS(t, S.demo.plus, 0.25)})`;
      } else pl.style.display = 'none';
    } else { dm.style.display = 'none'; pl.style.display = 'none'; }
    // Aufruf
    const ct = $('cta');
    if (S.cta !== null && t >= S.cta) {
      const s = popS(t, S.cta, 0.35);
      ct.style.display = 'block';
      ct.style.transform = `translateX(-50%) rotate(-3deg) scale(${Math.max(0.001, s) * (1 + 0.045 * Math.max(0, Math.sin(t * 8)))})`;
    } else ct.style.display = 'none';
    // Postkarte vom Mond
    const pc = $('postcard');
    if (S.postcard && t >= S.postcard.t0 && t < S.postcard.out + 0.3) {
      const P = S.postcard;
      const s0 = popS(t, P.t0, 0.35) * (1 - E.in(prog(t, P.out, 0.3)));
      let fx = 1, back = !!P.back;
      if (P.flip !== undefined && t >= P.flip) { const f = clamp((t - P.flip) / 0.36); fx = Math.abs(Math.cos(Math.PI * f)); back = f > 0.5; }
      const zk = P.zoom ? E.inOut(prog(t, P.zoom.t0, P.zoom.d)) : 0, z = 1 + 1.15 * zk;
      disp($('pcFront'), !back); disp($('pcBack'), back);
      pc.style.display = 'block'; pc.style.opacity = clamp(s0 * 3);
      pc.style.transform = `translate(${156 * z * zk}px,${(130 - 182 * z) * zk}px) rotate(${-3 + Math.sin(t * 2) * 1.2}deg) scale(${Math.max(0.001, s0 * z * fx)},${Math.max(0.001, s0 * z)})`;
      setT($('pcWave'), `rotate(${Math.sin(t * 9) * 14} 30 -110)`);
      $('pcPPS').setAttribute('fill', zk > 0.6 && Math.sin(t * 10) > 0 ? '#FF2D2D' : '#D23A3A');
    } else pc.style.display = 'none';
    // KABUMM
    const bm = $('boom');
    if (S.boomText && t < S.boomText.t1) {
      const k = clamp((S.boomText.t1 - t) / 0.3);
      bm.style.display = 'block'; bm.style.opacity = k;
      bm.style.transform = `translate(-50%,-50%) rotate(${-8 + Math.sin(t * 30) * 3}deg) scale(${(1.15 - 0.15 * clamp((t - S.boomText.t0) / 0.4)) * (0.9 + 0.1 * k)})`;
    } else bm.style.display = 'none';
    // KLONG!
    ['klong1', 'klong2'].forEach((id, i) => {
      const el = $(id), k0 = S.knock ? S.knock[i] : null;
      if (k0 === null || t < k0 || t > k0 + 0.7) { el.style.display = 'none'; return; }
      const [sx, sy] = toScreen(W.rocket.x + 60 + i * 40, W.rocket.y - 330 - i * 70);
      el.style.display = 'block'; el.style.left = `${sx - 150}px`; el.style.top = `${sy - 70}px`;
      el.style.opacity = clamp((0.7 - (t - k0)) * 4);
      el.style.transform = `rotate(${i ? 8 : -10}deg) scale(${popS(t, k0, 0.18)})`;
    });
    // Blitz und Farbstimmung beim Start
    $('flash').style.opacity = S.flash !== null && t >= S.flash ? (1 - clamp((t - S.flash) / 0.35)) * 0.9 : 0;
    $('grade').style.background = `rgba(255, 120, 60, ${0.35 * S.grade})`;
    // Lichtstaub
    let m = '';
    for (const p of motes) {
      const y = ((p.y - t * p.v) % 1400 + 1400) % 1400 + 300, x = p.x + Math.sin(t * 0.6 + p.p) * 24;
      m += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${p.r}" fill="#FFE9B0" opacity="${(0.35 + 0.35 * Math.sin(t * 2 + p.p)).toFixed(2)}"/>`;
    }
    $('motes').innerHTML = m;
  }

  function drawWorld(S, t) {
    lastS = S;
    const [pcx, pcy] = S.cam;
    setT($('pxSky'), `translate(${(pcx - 1300) * 0.72},${(pcy - 1150) * 0.72})`);
    setT($('pxFar'), `translate(${(pcx - 1300) * 0.45},${(pcy - 1150) * 0.32})`);
    setT($('pxMid'), `translate(${(pcx - 1300) * 0.18},${(pcy - 1150) * 0.1})`);
    $('pxFar').style.filter = 'blur(1.2px)';
    setT($('sunRays'), `rotate(${t * 2.5})`);
    document.querySelectorAll('.cloud').forEach((el) => setT(el, `translate(${+el.dataset.x + t * 9},${el.dataset.y}) scale(${el.dataset.s})`));
    document.querySelectorAll('.star').forEach((el) => el.setAttribute('opacity', (+el.dataset.o * (0.55 + 0.45 * Math.sin(t * 2.4 + +el.dataset.p))).toFixed(2)));
    document.querySelectorAll('.sway').forEach((el) => {
      const tr = el.getAttribute('transform').replace(/ rotate\([^)]*\)/, '');
      el.setAttribute('transform', `${tr} rotate(${Math.sin(t * 1.2 + +el.dataset.p) * 2})`);
    });
    document.querySelectorAll('.wash').forEach((el) => setT(el, `translate(${el.dataset.x},${el.dataset.y}) rotate(${Math.sin(t * 2 + +el.dataset.p) * 6})`));
    $('lampGlow').setAttribute('opacity', (0.75 + 0.15 * Math.sin(t * 9) * Math.sin(t * 3.1)).toFixed(2));
    // Oma
    const O = S.oma;
    disp(om(), O.show);
    if (O.show) {
      setT(om(), `translate(${O.x},${O.y}) scale(${O.s})`);
      poseHuman(OM, O, t);
      $('om-soot').setAttribute('opacity', O.soot.toFixed(2));
      $('om-frizz').setAttribute('opacity', O.soot.toFixed(2));
    }
    // Berta
    const B = S.berta;
    disp($('bertaW'), B.show);
    if (B.show) { setT($('bertaW'), `translate(${B.x},${B.y}) scale(${B.s})`); poseBerta(B, t); }
    poseKrause(S.krause, t);
    setT($('gnBob'), `translate(0,${Math.sin(t * 2.2) * 1.5})`);
    if (S.gnomeHat !== null && t > S.gnomeHat) { const a = t - S.gnomeHat; setT($('gnHat'), `translate(${-a * 160},${-a * 520 + a * a * 300}) rotate(${-a * 400} 0 -170)`); }
    else setT($('gnHat'), '');
    // Klopfende Faust am Tank
    const kn = $('knock');
    if (S.knock) {
      const near = S.knock.map((k) => Math.max(0, 1 - Math.abs(t - k) / 0.16));
      const hit = Math.max(...near);
      disp(kn, true);
      setT(kn, `translate(${W.rocket.x + 170 - hit * 40},${W.rocket.y - 300}) rotate(${-8 + hit * 6})`);
    } else disp(kn, false);
    drawRocket(S, t);
    setT($('rocketW'), `translate(${W.rocket.x},${W.rocket.y})`);
    const bd = $('board');
    disp(bd, true);
    const k = (S.board || []).join('|');
    if (bd.dataset.k !== k || bd.dataset.k === undefined) { $('boardNames').innerHTML = S.board && S.board.length > 24 ? boardNamesMarkup(S.board) : boardSlotsMarkup(24, S.board || []); bd.dataset.k = k; }
    document.querySelectorAll('.bn').forEach((el) => { const p0 = S.boardPop === null ? -1 : S.boardPop + (+el.dataset.i) * 0.11; el.setAttribute('opacity', clamp((t - p0) * 6).toFixed(2)); });
    disp($('boardChalk'), !(S.board && S.board.length));
    const BW = S.boardWrite, bp = BW ? clamp((t - BW.t0) / BW.d) : 1;
    $('cpBoardR').setAttribute('width', (bp * 330).toFixed(1));
    const ch = $('chalk');
    if (BW && t > BW.t0 - 0.2 && t < BW.t0 + BW.d + 0.3) { disp(ch, true); setT(ch, `translate(${-300 + bp * 290},${-990 + Math.sin(bp * 40) * 8})`); }
    else disp(ch, false);
    drawOverlay(S, t);
  }

  Engine.start({
    world, shots, drawWorld,
    baseState: base,
    highlight: '#FFD43B',
    whip: { skip: [] },
    karaoke: true,
    punch: 0.06,
    confettiColors: ['#FFD43B', '#FF5C8A', '#fff', '#5CC8FF', '#7EE07A', '#FF9F2E'],
    preload: '🚀⛽🐄„“§',
    ui: {
      day: 'TAG 2',
      profile: { name: 'Omas Mondmission', handle: '@omas.mondmission', avatar: '🚀', stat: 'Liter', foot: '1 Kommentar = 1 Liter ⛽' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '⛽', text: 'GETANKT!' }, plusOne: '+1 LITER', zirp: '',
      ticket: '', tstamp: '', kasse: 'TANK',
      cards: [{ color: '#FFD43B', icon: '', label: '' }, { color: '#FF5C8A', icon: '', label: '' }, { color: '#5CC8FF', icon: '', label: '' }],
      floats: [], ccards: [],
    },
  });
  window.ART = { omaMarkup, bertaMarkup, rocketMarkup, krauseMarkup, defs, OUT };
})();

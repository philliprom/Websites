/* Monsterdöner – Tag 1: Leo hat eine Dönerbude für Monster eröffnet. Seitenansicht: Leo links hinter dem Dönerspieß,
 * Theke in der Mitte, Kunden rechts, Ladentür mit Vollmond ganz rechts. Kunden: Vampir Graf Vladi, Geist, Werwolf Wolfgang,
 * Zombie Günther. Am Ende klopft die Lebensmittelkontrolle (mit Geister-Staubsauger). */
(() => {
  const { $, clamp, lerp, E, prog, popS, rng, cue, setT, disp, camLerp, OUT, sw, humanEls, humanDefaults, poseHuman,
    faceMarkup, armMarkup } = Engine;
  const NAVY = '#1B1430';
  const FLOOR = 1700;
  const POS = { leo: 760, cust: 1590, door: 2170 };
  const SKIN = '#F1C6A0';

  // ---------------------------------------------------------------- Definitionen
  const defs = `
  <defs>
    <pattern id="pTiles" width="72" height="72" patternUnits="userSpaceOnUse">
      <rect width="72" height="72" fill="#DDE9DE"/><rect x="3" y="3" width="66" height="66" rx="4" fill="#E9F2E7"/>
      <path d="M8 10 Q20 6 30 12" stroke="#fff" stroke-width="4" opacity=".6" fill="none"/></pattern>
    <pattern id="pFloor" width="140" height="140" patternUnits="userSpaceOnUse">
      <rect width="140" height="140" fill="#3D3352"/><rect width="70" height="70" fill="#574A72"/><rect x="70" y="70" width="70" height="70" fill="#574A72"/></pattern>
    <pattern id="pPlaid" width="40" height="40" patternUnits="userSpaceOnUse">
      <rect width="40" height="40" fill="#C8323A"/><rect width="40" height="12" y="14" fill="#7A1C24" opacity=".8"/><rect height="40" width="12" x="14" fill="#7A1C24" opacity=".8"/>
      <rect width="40" height="3" y="19" fill="#1B1430" opacity=".6"/><rect height="40" width="3" x="19" fill="#1B1430" opacity=".6"/></pattern>
    <linearGradient id="gNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1235"/><stop offset=".7" stop-color="#2B2462"/><stop offset="1" stop-color="#4B3478"/></linearGradient>
    <radialGradient id="gHeat"><stop offset="0" stop-color="#FFE7A0" stop-opacity=".95"/><stop offset=".45" stop-color="#FF8A2A" stop-opacity=".55"/><stop offset="1" stop-color="#FF5A1A" stop-opacity="0"/></radialGradient>
    <radialGradient id="gMoon"><stop offset="0" stop-color="#FFFBE8"/><stop offset=".75" stop-color="#FFF0BC"/><stop offset="1" stop-color="#F6DC8C"/></radialGradient>
    <radialGradient id="gMoonGlow"><stop offset="0" stop-color="#FFF4C8" stop-opacity=".6"/><stop offset="1" stop-color="#FFF4C8" stop-opacity="0"/></radialGradient>
    <radialGradient id="gLampCone" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#FFF6D0" stop-opacity=".55"/><stop offset="1" stop-color="#FFF6D0" stop-opacity="0"/></radialGradient>
    <linearGradient id="gSteel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF2F7"/><stop offset="1" stop-color="#AEB8C6"/></linearGradient>
    <linearGradient id="gMeat" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C47A44"/><stop offset=".45" stop-color="#9A5228"/><stop offset="1" stop-color="#6A3418"/></linearGradient>
    <radialGradient id="gPoof" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#E4DDF0"/><stop offset="1" stop-color="#C9BEDF" stop-opacity="0"/></radialGradient>
    <clipPath id="cpCone" clipPathUnits="userSpaceOnUse"><path d="M-90 -470 L90 -470 L58 -50 L-58 -50 Z"/></clipPath>
    <clipPath id="cpGlass" clipPathUnits="userSpaceOnUse"><rect x="2010" y="810" width="320" height="560" rx="14"/></clipPath>
    <filter id="fNeon" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="fBlur6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>`;

  // ---------------------------------------------------------------- Laden
  const doner = (s = 1) => `<g transform="scale(${s})">
      <path d="M-70 10 Q-74 -50 0 -62 Q74 -50 70 10 Z" fill="#EBC27A" ${sw}/>
      <path d="M-58 -2 Q-56 -40 0 -48 Q56 -40 58 -2" fill="#8A4A2A" stroke="${OUT}" stroke-width="3"/>
      <path d="M-50 -28 q12 -16 24 -2 q12 -16 24 0 q12 -16 24 0 q10 -12 22 2" stroke="#5CC24E" stroke-width="10" fill="none" stroke-linecap="round"/>
      <circle cx="-22" cy="-38" r="7" fill="#E8433E"/><circle cx="16" cy="-40" r="7" fill="#E8433E"/>
      <path d="M-40 -10 q2 22 -2 30 M8 -12 q3 18 0 26 M40 -8 q2 14 0 22" stroke="#FFFDF4" stroke-width="9" fill="none" stroke-linecap="round"/>
      <path d="M-70 10 Q0 24 70 10" stroke="#C99A52" stroke-width="5" fill="none"/></g>`;
  const breadBag = () => `<g><path d="M-80 0 L-66 -170 L66 -170 L80 0 Z" fill="#E9D3A6" ${sw}/><path d="M-66 -170 l12 -20 l12 20 l12 -20 l12 20 l12 -20 l12 20 l12 -20 l12 20 l12 -20 l12 20" fill="#E9D3A6" stroke="${OUT}" stroke-width="4"/>
      <text x="0" y="-110" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="22" fill="#2E7D32">KNOBLAUCH-</text>
      <text x="0" y="-82" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="22" fill="${OUT}">FLADENBROT</text>
      <g transform="translate(0,-40)"><path d="M0 -20 Q-26 -8 -22 10 Q-12 24 0 22 Q12 24 22 10 Q26 -8 0 -20 Z" fill="#FFFDF4" stroke="${OUT}" stroke-width="3"/><path d="M0 -20 V-30" stroke="#7CBF5A" stroke-width="4"/></g></g>`;
  const broom = () => `<g transform="rotate(10)"><rect x="-6" y="-260" width="12" height="300" rx="5" fill="#B5814F" ${sw}/><path d="M-40 40 L40 40 L56 130 L-56 130 Z" fill="#E8C55A" ${sw}/>
      <path d="M-30 60 V122 M-10 60 V126 M10 60 V126 M30 60 V122" stroke="#B89A3A" stroke-width="4"/></g>`;
  const bottle = (x, y, col, cap, label, lc) => `<g transform="translate(${x},${y})">
      <path d="M-24 0 L-24 -96 Q-24 -112 -10 -116 L-8 -132 L8 -132 L10 -116 Q24 -112 24 -96 L24 0 Z" fill="${col}" ${sw}/>
      <rect x="-9" y="-150" width="18" height="20" rx="4" fill="${cap}" ${sw}/>
      <rect x="-22" y="-80" width="44" height="40" rx="6" fill="#fff" stroke="${OUT}" stroke-width="3"/>
      <text x="0" y="-55" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="${label.length > 6 ? 9 : 12}" fill="${lc}">${label}</text></g>`;
  const shopMarkup = () => {
    let lamps = '';
    for (const lx of [820, 1520]) lamps += `<g transform="translate(${lx},300)"><path d="M0 0 V120" stroke="${NAVY}" stroke-width="5"/>
      <path class="lampCone" d="M-60 150 L-330 1400 L330 1400 L60 150 Z" fill="url(#gLampCone)" opacity=".6"/>
      <path d="M-62 150 Q0 96 62 150 Z" fill="#7CFF6B" ${sw}/><ellipse cx="0" cy="152" rx="40" ry="10" fill="#FFF8D8"/></g>`;
    let drinks = '';
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) drinks += `<rect x="${80 + c * 66}" y="${1050 + r * 150}" width="40" height="110" rx="12" fill="${['#E8433E', '#7CFF6B', '#FF9F2E', '#5CC8FF'][(r + c) % 4]}" stroke="${OUT}" stroke-width="3"/>`;
    return `
    <g id="shop">
      <rect x="-800" y="-400" width="4400" height="2200" fill="url(#pTiles)"/>
      <rect x="-800" y="-400" width="4400" height="700" fill="#2A1E3F"/>
      <rect x="-800" y="290" width="4400" height="22" fill="#1B1430"/>
      <rect x="-800" y="1440" width="4400" height="270" fill="#8E2A3A"/><rect x="-800" y="1440" width="4400" height="16" fill="#C8475A"/>
      ${lamps}
      <g id="neon" transform="translate(1170,470)">
        <rect x="-430" y="-110" width="860" height="200" rx="26" fill="#1B1430" stroke="#0E0A1A" stroke-width="6"/>
        <g filter="url(#fNeon)">
          <text id="neon1" x="-30" y="-12" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="92" fill="none" stroke="#7CFF6B" stroke-width="7" letter-spacing="6">MONSTER</text>
          <text id="neon2" x="-30" y="76" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="76" fill="none" stroke="#FF5CC8" stroke-width="6" letter-spacing="10">DÖNER</text>
        </g>
        <g transform="translate(330,-6) scale(.9)" filter="url(#fNeon)"><path d="M-62 30 Q-66 -36 0 -46 Q66 -36 62 30 Z" fill="none" stroke="#FFD43B" stroke-width="6"/>
          <path d="M-20 30 l8 22 l8 -22 M12 30 l8 22 l8 -22" fill="none" stroke="#FFFFFF" stroke-width="5"/></g>
      </g>
      <g transform="translate(1170,780)">
        <rect x="-400" y="-120" width="800" height="250" rx="16" fill="#231A35" stroke="${NAVY}" stroke-width="8"/>
        ${[['DÖNER', '5 €'], ['DÜRÜM', '6 €'], ['VAMPIR-TELLER (OHNE KNOBLAUCH)', '7 €'], ['HIRN-BOX', '4 €']].map(([a, b], i) =>
          `<text x="-370" y="${-66 + i * 54}" font-family="Fredoka" font-weight="600" font-size="36" fill="#F4F1E6">${a}</text>
           <text x="370" y="${-66 + i * 54}" text-anchor="end" font-family="Fredoka" font-weight="700" font-size="36" fill="#FFD43B">${b}</text>`).join('')}
      </g>
      <g id="fridge"><rect x="40" y="980" width="340" height="720" rx="16" fill="#C9D1DB" ${sw}/><rect x="62" y="1004" width="296" height="600" rx="8" fill="#BFE9FF" opacity=".55"/>
        ${drinks}<rect x="62" y="1004" width="296" height="600" rx="8" fill="#E8F8FF" opacity=".25"/><rect x="330" y="1220" width="14" height="120" rx="6" fill="#7E8898"/>
        <g transform="translate(210,960) rotate(-4)"><rect x="-120" y="-26" width="240" height="44" rx="10" fill="#E8433E" ${sw}/>
          <text x="0" y="6" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="24" fill="#fff">BLUTORANGEN-LIMO</text></g></g>
      <g id="spit" transform="translate(540,1350)">
        <rect x="-118" y="-500" width="70" height="470" rx="14" fill="#5E6676" ${sw}/>
        <circle id="heatGlow" cx="-40" cy="-260" r="260" fill="url(#gHeat)"/>
        ${Array.from({ length: 8 }, (_, i) => `<path d="M-112 ${-470 + i * 56} H-54" stroke="#FFB45A" stroke-width="8" opacity=".9"/>`).join('')}
        <path d="M0 -520 V30" stroke="#7E8898" stroke-width="12"/>
        <g id="cone"><path d="M-90 -470 L90 -470 L58 -50 L-58 -50 Z" fill="url(#gMeat)" ${sw}/>
          <g clip-path="url(#cpCone)"><g id="coneTex">${Array.from({ length: 16 }, (_, i) => `<path d="M${-160 + i * 30} -480 L${-150 + i * 30} -40" stroke="#5A2A12" stroke-width="7" opacity=".45"/>`).join('')}</g>
            ${Array.from({ length: 7 }, (_, i) => `<path d="M-100 ${-420 + i * 56} Q0 ${-404 + i * 56} 100 ${-420 + i * 56}" stroke="#E8A066" stroke-width="5" fill="none" opacity=".6"/>`).join('')}</g>
          <path d="M-80 -460 Q-84 -260 -50 -60" stroke="#F2B478" stroke-width="8" fill="none" opacity=".5"/></g>
        <rect x="-90" y="20" width="180" height="26" rx="8" fill="url(#gSteel)" ${sw}/>
      </g>
      <g id="shopCounter" transform="translate(1170,1390)">
        <rect x="-200" y="0" width="400" height="310" fill="#E8433E" ${sw}/>
        <rect x="-200" y="120" width="400" height="34" fill="#fff"/><text x="0" y="250" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" opacity=".9">🥙 SEIT TAG 1</text>
        <rect x="-226" y="-26" width="452" height="34" rx="10" fill="url(#gSteel)" ${sw}/>
        <g id="btlK">${bottle(-140, -26, '#FFFDF4', '#7CFF6B', 'KNOBLAUCH', '#1B1430')}</g><g id="btlS">${bottle(-80, -26, '#E8433E', '#FFD43B', 'SCHARF', '#E8433E')}</g>
        <g transform="translate(40,-26)"><rect x="-40" y="-60" width="80" height="60" rx="8" fill="#fff" ${sw}/><path d="M-26 -60 q26 -26 52 0" fill="#fff" stroke="${OUT}" stroke-width="3"/></g>
        <g transform="translate(140,-26)"><path d="M-34 0 L-30 -86 L30 -86 L34 0 Z" fill="#BFE6FF" fill-opacity=".5" ${sw}/>
          <circle cx="-8" cy="-22" r="12" fill="#FFD43B" stroke="${OUT}" stroke-width="3"/><circle cx="12" cy="-34" r="12" fill="#FFD43B" stroke="${OUT}" stroke-width="3"/>
          <g id="jarBat" style="display:none" transform="translate(0,-56) scale(.55)"><path d="M0 0 Q-40 -30 -70 -10 Q-50 0 -46 14 Q-30 4 0 10 Z M0 0 Q40 -30 70 -10 Q50 0 46 14 Q30 4 0 10 Z" fill="${NAVY}"/>
            <ellipse cx="0" cy="4" rx="16" ry="20" fill="${NAVY}"/><path d="M-12 -12 L-8 -26 L-2 -14 Z M12 -12 L8 -26 L2 -14 Z" fill="${NAVY}"/><circle cx="-6" cy="0" r="4" fill="#FF3B4E"/><circle cx="6" cy="0" r="4" fill="#FF3B4E"/></g>
          <g transform="translate(0,-120) rotate(4)"><rect x="-70" y="-18" width="140" height="34" rx="6" fill="#FFF6E2" stroke="${OUT}" stroke-width="3"/>
            <text x="0" y="5" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="15" fill="${OUT}">TRINKGELD (KEINE SEELEN)</text></g></g>
        <g id="zArmOnCounter" style="display:none"></g>
      </g>
      <g id="door">
        <rect x="1980" y="780" width="380" height="920" rx="18" fill="#6B4A8A" ${sw}/>
        <g clip-path="url(#cpGlass)">
          <rect x="2010" y="810" width="320" height="560" fill="url(#gNight)"/>
          ${Array.from({ length: 22 }, (_, i) => `<circle class="star" data-p="${i}" cx="${2020 + ((i * 97) % 300)}" cy="${830 + ((i * 53) % 260)}" r="${1.5 + (i % 3)}" fill="#FFF8E6"/>`).join('')}
          <g id="moon"><circle cx="2170" cy="990" r="150" fill="url(#gMoonGlow)"/><circle cx="2170" cy="990" r="78" fill="url(#gMoon)"/>
            <circle cx="2148" cy="975" r="12" fill="#EADBA8"/><circle cx="2190" cy="1010" r="9" fill="#EADBA8"/></g>
          <g id="moonClouds"><ellipse cx="2150" cy="990" rx="150" ry="52" fill="#3A3270"/><ellipse cx="2210" cy="960" rx="110" ry="46" fill="#463C82"/><ellipse cx="2120" cy="1030" rx="120" ry="40" fill="#332B66"/></g>
          <path d="M2010 1250 L2060 1180 L2110 1250 L2150 1160 L2210 1250 L2260 1190 L2330 1250 L2330 1370 L2010 1370 Z" fill="#1B1430"/>
          ${[[2050, 1230], [2160, 1210], [2280, 1240]].map(([x, y]) => `<rect x="${x}" y="${y}" width="14" height="18" fill="#FFD27A"/>`).join('')}
          <g id="insp" style="display:none">
            <g id="inspBody"><rect x="2190" y="1060" width="110" height="180" rx="20" fill="#120C20"/>
              <path d="M2190 1090 Q2150 1100 2160 1200 L2200 1230 Z" fill="#120C20"/>
              <circle cx="2170" cy="1020" r="56" fill="#120C20"/><path d="M2108 990 Q2170 940 2232 990 L2240 1004 L2100 1004 Z" fill="#120C20"/>
              <rect x="2100" y="996" width="150" height="16" rx="6" fill="#120C20"/>
              <path d="M2230 1080 Q2320 1100 2300 1240" stroke="#120C20" stroke-width="22" fill="none"/>
              <rect x="2080" y="1100" width="60" height="80" rx="6" fill="#120C20"/>
              <circle id="inspLight" cx="2150" cy="1030" r="10" fill="#7CFF6B"/></g>
          </g>
        </g>
        <rect x="2010" y="810" width="320" height="560" rx="14" fill="none" stroke="${OUT}" stroke-width="6"/>
        <path d="M2030 830 L2120 830 L2030 960 Z" fill="#fff" opacity=".12"/>
        <rect x="2290" y="1400" width="40" height="120" rx="10" fill="#FFD43B" ${sw}/>
        <g transform="translate(2170,1450)"><rect x="-80" y="-30" width="160" height="56" rx="12" fill="#1B1430" ${sw}/>
          <text x="0" y="10" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="#7CFF6B" filter="url(#fNeon)">OFFEN</text></g>
        <g id="bell" transform="translate(2170,760)"><path d="M0 -20 V0" stroke="${OUT}" stroke-width="4"/><path d="M-22 26 Q-22 -6 0 -6 Q22 -6 22 26 Z" fill="#FFD43B" ${sw}/></g>
      </g>
      <rect x="-800" y="${FLOOR}" width="4400" height="900" fill="url(#pFloor)"/>
      <rect x="-800" y="${FLOOR}" width="4400" height="14" fill="#1B1430" opacity=".6"/>
    </g>`;
  };

  // ---------------------------------------------------------------- Figuren (Rig wie Kalle: Füße bei 0, Kopf um -234)
  const shadow = (rx = 120) => `<ellipse cx="0" cy="6" rx="${rx}" ry="16" fill="#0E0A1A" opacity=".35"/>`;
  const leoMarkup = (p) => `
  <g id="${p}">${shadow(110)}
    <g id="${p}-bob">
      <rect x="-40" y="-78" width="32" height="74" rx="10" fill="#3A4A7A" ${sw}/><rect x="8" y="-78" width="32" height="74" rx="10" fill="#3A4A7A" ${sw}/>
      <path d="M-50 0 L-6 0 L-6 -18 Q-6 -26 -16 -26 L-42 -26 Q-52 -26 -52 -14 Z" fill="#fff" ${sw}/><path d="M50 0 L6 0 L6 -18 Q6 -26 16 -26 L42 -26 Q52 -26 52 -14 Z" fill="#fff" ${sw}/>
      <g id="${p}-armL" transform="translate(-48,-160)">${armMarkup(p, 'L', '#2A2A35', '#2A2A35', SKIN)}<g id="${p}-propL" transform="translate(0,104)"></g></g>
      <path d="M-54 -176 Q-80 -130 -70 -76 Q0 -62 70 -76 Q80 -130 54 -176 Q0 -190 -54 -176 Z" fill="#2A2A35" ${sw}/>
      <path d="M-36 -160 L36 -160 L44 -60 Q0 -50 -44 -60 Z" fill="#E8433E" ${sw}/>
      <path d="M-30 -160 Q-40 -186 -26 -194 M30 -160 Q40 -186 26 -194" stroke="#E8433E" stroke-width="7" fill="none"/>
      <g transform="translate(0,-118)"><circle r="20" fill="#fff" stroke="${OUT}" stroke-width="3"/><text y="7" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="20" fill="#E8433E">MD</text></g>
      <g id="${p}-armR" transform="translate(48,-160)">${armMarkup(p, 'R', '#2A2A35', '#2A2A35', SKIN)}<g id="${p}-propR" transform="translate(0,104)"></g></g>
      <g id="${p}-head">
        <ellipse cx="-72" cy="-226" rx="13" ry="17" fill="${SKIN}" ${sw}/><ellipse cx="72" cy="-226" rx="13" ry="17" fill="${SKIN}" ${sw}/>
        <ellipse cx="0" cy="-232" rx="72" ry="72" fill="${SKIN}" ${sw}/>
        <path d="M-74 -244 Q-80 -300 -30 -312 Q-10 -330 10 -312 Q30 -332 50 -306 Q82 -296 76 -246 Q60 -280 30 -282 Q0 -268 -30 -284 Q-60 -280 -74 -244 Z" fill="#6B4423" ${sw}/>
        <g id="${p}-cap"><path d="M-58 -296 L-46 -336 L58 -336 L66 -296 Z" fill="#fff" ${sw}/><path d="M-60 -304 H64" stroke="#E8433E" stroke-width="10"/></g>
        <g id="${p}-mess" style="display:none" stroke="#6B4423" stroke-width="8" stroke-linecap="round" fill="none">
          <path d="M-60 -290 l-26 -30 M-30 -310 l-8 -40 M0 -316 l6 -42 M30 -310 l18 -36 M60 -292 l28 -26"/></g>
        ${[[-44, -200], [-36, -192], [-50, -190], [44, -200], [36, -192], [50, -190]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#C98256"/>`).join('')}
        ${faceMarkup(p, { brow: '#4A2E18', browW: 9 })}
        <path d="M-8 -212 Q0 -198 8 -212" stroke="#D9967A" stroke-width="5" fill="none" stroke-linecap="round"/>
      </g>
    </g>
  </g>`;

  const VSKIN = '#E4DDF0';
  const vladiMarkup = (p) => `
  <g id="${p}">${shadow(150)}
    <g id="${p}-bob">
      <path id="${p}-cape" d="M-70 -190 Q-160 -100 -170 0 L170 0 Q160 -100 70 -190 Z" fill="#1B1430" ${sw}/>
      <path d="M-60 -180 Q-120 -100 -126 -6 L-70 -6 Q-80 -100 -40 -170 Z M60 -180 Q120 -100 126 -6 L70 -6 Q80 -100 40 -170 Z" fill="#8E1B2E"/>
      <rect x="-36" y="-82" width="28" height="80" rx="8" fill="#1B1430" ${sw}/><rect x="8" y="-82" width="28" height="80" rx="8" fill="#1B1430" ${sw}/>
      <g id="${p}-armL" transform="translate(-50,-160)">${armMarkup(p, 'L', '#22182E', '#FFFFFF', VSKIN)}</g>
      <path d="M-50 -178 Q-70 -130 -62 -76 Q0 -64 62 -76 Q70 -130 50 -178 Q0 -190 -50 -178 Z" fill="#22182E" ${sw}/>
      <path d="M-22 -182 L0 -120 L22 -182 Z" fill="#fff" stroke="${OUT}" stroke-width="4"/>
      <circle cx="0" cy="-118" r="12" fill="#C8323A" stroke="#FFD43B" stroke-width="4"/>
      <g id="${p}-armR" transform="translate(50,-160)">${armMarkup(p, 'R', '#22182E', '#FFFFFF', VSKIN)}<g id="${p}-propR" transform="translate(0,104)"></g></g>
      <path d="M-86 -186 L-112 -300 L-56 -214 Z M86 -186 L112 -300 L56 -214 Z" fill="#8E1B2E" ${sw}/>
      <g id="${p}-head">
        <path d="M-70 -236 L-104 -270 L-66 -206 Z M70 -236 L104 -270 L66 -206 Z" fill="${VSKIN}" ${sw}/>
        <ellipse cx="0" cy="-234" rx="64" ry="76" fill="${VSKIN}" ${sw}/>
        <path d="M-66 -244 Q-70 -312 0 -318 Q70 -312 66 -244 Q58 -284 26 -290 L0 -262 L-26 -290 Q-58 -284 -66 -244 Z" fill="#141022" ${sw}/>
        <ellipse cx="-27" cy="-226" rx="26" ry="20" fill="#B9A9D6" opacity=".8"/><ellipse cx="27" cy="-226" rx="26" ry="20" fill="#B9A9D6" opacity=".8"/>
        ${faceMarkup(p, { brow: '#141022', browW: 10, eyeRx: 17, eyeRy: 19, pup: 9 })}
        <path d="M-6 -214 L0 -196 L6 -214" fill="${VSKIN}" stroke="#9C8CBC" stroke-width="3"/>
        <path id="${p}-fangs" d="M-14 -184 L-10 -168 L-6 -184 Z M6 -184 L10 -168 L14 -184 Z" fill="#fff" stroke="${OUT}" stroke-width="2.5"/>
        <ellipse id="${p}-sick" cx="0" cy="-226" rx="62" ry="72" fill="#8BD46A" opacity="0" style="mix-blend-mode:multiply"/>
        <g id="${p}-glow" style="display:none" filter="url(#fNeon)"><circle cx="-27" cy="-228" r="13" fill="#FF2D3D"/><circle cx="27" cy="-228" r="13" fill="#FF2D3D"/>
          <circle cx="-27" cy="-228" r="5" fill="#FFE0E0"/><circle cx="27" cy="-228" r="5" fill="#FFE0E0"/></g>
      </g>
    </g>
  </g>`;

  const WSKIN = '#E8B98F';
  const wolfMarkup = (p) => `
  <g id="${p}">${shadow(140)}
    <g id="${p}-bob">
      <rect x="-44" y="-84" width="36" height="82" rx="10" fill="#3A4A7A" ${sw}/><rect x="8" y="-84" width="36" height="82" rx="10" fill="#3A4A7A" ${sw}/>
      <ellipse cx="-26" cy="-6" rx="30" ry="12" fill="#5A3A22" ${sw}/><ellipse cx="26" cy="-6" rx="30" ry="12" fill="#5A3A22" ${sw}/>
      <g id="${p}-armL" transform="translate(-64,-160)">${armMarkup(p, 'L', 'url(#pPlaid)', '#7A1C24', WSKIN)}</g>
      <path d="M-70 -180 Q-100 -130 -86 -70 Q0 -54 86 -70 Q100 -130 70 -180 Q0 -196 -70 -180 Z" fill="url(#pPlaid)" ${sw}/>
      <g id="${p}-fur" opacity="0">${Array.from({ length: 9 }, (_, i) => `<path d="M${-70 + i * 17} -184 l8 -22 l8 22" fill="#7A6450" stroke="${OUT}" stroke-width="3"/>`).join('')}</g>
      <g id="${p}-armR" transform="translate(64,-160)">${armMarkup(p, 'R', 'url(#pPlaid)', '#7A1C24', WSKIN)}</g>
      <g id="${p}-head">
        <g id="${p}-human">
          <ellipse cx="-74" cy="-226" rx="14" ry="18" fill="${WSKIN}" ${sw}/><ellipse cx="74" cy="-226" rx="14" ry="18" fill="${WSKIN}" ${sw}/>
          <ellipse cx="0" cy="-234" rx="76" ry="76" fill="${WSKIN}" ${sw}/>
          <path d="M-78 -240 Q-90 -320 -20 -318 Q10 -340 40 -316 Q90 -310 78 -240 Q60 -290 30 -284 Q0 -300 -30 -284 Q-62 -290 -78 -240 Z" fill="#4A2E1A" ${sw}/>
          ${faceMarkup(p, { brow: '#3A2414', browW: 14 })}
          <path d="M-62 -196 Q-70 -130 0 -112 Q70 -130 62 -196 Q40 -170 0 -168 Q-40 -170 -62 -196 Z" fill="#5A3A22" ${sw}/>
        </g>
        <g id="${p}-wolf" style="display:none">
          <path d="M-62 -268 L-52 -350 L-14 -290 Z M62 -268 L52 -350 L14 -290 Z" fill="#6E5A48" ${sw}/><path d="M-50 -282 L-46 -326 L-26 -292 Z M50 -282 L46 -326 L26 -292 Z" fill="#E8A0A8"/>
          <ellipse cx="0" cy="-236" rx="84" ry="82" fill="#7A6450" ${sw}/>
          ${Array.from({ length: 10 }, (_, i) => { const a = Math.PI * (0.15 + i * 0.08); return `<path d="M${(Math.cos(a) * 80).toFixed(0)} ${(-236 + Math.sin(a) * 78).toFixed(0)} l${(Math.cos(a) * 26).toFixed(0)} ${(Math.sin(a) * 18).toFixed(0)}" stroke="#7A6450" stroke-width="12" stroke-linecap="round"/>`; }).join('')}
          <path d="M-46 -210 Q-50 -150 0 -140 Q50 -150 46 -210 Q0 -230 -46 -210 Z" fill="#B8A18A" ${sw}/>
          <ellipse cx="0" cy="-206" rx="18" ry="12" fill="#1B1430"/>
          <path id="${p}-jaw" d="M-36 -168 Q0 -140 36 -168 Q30 -120 0 -114 Q-30 -120 -36 -168 Z" fill="#7A2633" ${sw}/>
          <path d="M-26 -166 l6 16 l6 -16 M14 -166 l6 16 l6 -16" fill="#fff" stroke="${OUT}" stroke-width="2"/>
          <ellipse cx="-30" cy="-252" rx="14" ry="11" fill="#FFD43B" ${sw}/><ellipse cx="30" cy="-252" rx="14" ry="11" fill="#FFD43B" ${sw}/>
          <circle cx="-30" cy="-252" r="5" fill="${OUT}"/><circle cx="30" cy="-252" r="5" fill="${OUT}"/>
          <path d="M-52 -274 L-12 -262 M52 -274 L12 -262" stroke="#3A2414" stroke-width="9" stroke-linecap="round"/>
        </g>
      </g>
    </g>
  </g>`;

  const ZSKIN = '#A9CC86';
  const zombieMarkup = (p) => `
  <g id="${p}">${shadow(115)}
    <g id="${p}-bob">
      <path d="M-38 -84 L-8 -84 L-10 0 L-40 0 Z M8 -84 L38 -84 L40 0 L10 0 Z" fill="#4A4258" ${sw}/>
      <path d="M-40 -16 l6 -10 l6 10 l6 -10 l6 10 M10 -16 l6 -10 l6 10 l6 -10 l6 10" stroke="${OUT}" stroke-width="3" fill="none"/>
      <g id="${p}-armL" transform="translate(-50,-160)">${armMarkup(p, 'L', '#8FB8D8', '#6E95BF', ZSKIN)}</g>
      <path d="M-54 -176 Q-80 -130 -70 -76 L-50 -66 L-36 -80 L-20 -64 L0 -80 L18 -64 L36 -80 L52 -66 L70 -76 Q80 -130 54 -176 Q0 -190 -54 -176 Z" fill="#8FB8D8" ${sw}/>
      <ellipse cx="-24" cy="-130" rx="12" ry="9" fill="#5A4E6E"/><ellipse cx="28" cy="-108" rx="9" ry="12" fill="#5A4E6E"/>
      <g id="${p}-armR" transform="translate(50,-160)">${armMarkup(p, 'R', '#8FB8D8', '#6E95BF', ZSKIN)}</g>
      <g id="${p}-head">
        <ellipse cx="-70" cy="-224" rx="13" ry="17" fill="${ZSKIN}" ${sw}/><ellipse cx="72" cy="-230" rx="10" ry="12" fill="${ZSKIN}" ${sw}/>
        <ellipse cx="0" cy="-232" rx="70" ry="74" fill="${ZSKIN}" ${sw}/>
        <path d="M-70 -250 Q-60 -310 -10 -306 L0 -292 L14 -310 Q60 -306 70 -250 Q50 -280 30 -272 L20 -288 L0 -270 L-30 -290 Q-56 -280 -70 -250 Z" fill="#3E5A3A" ${sw}/>
        <path d="M-40 -284 L-10 -268 M-34 -284 L-30 -272 M-24 -280 L-20 -268 M-14 -276 L-10 -264" stroke="${OUT}" stroke-width="3"/>
        <ellipse cx="-27" cy="-226" rx="28" ry="26" fill="#7E9E66" opacity=".8"/><ellipse cx="27" cy="-226" rx="22" ry="22" fill="#7E9E66" opacity=".8"/>
        ${faceMarkup(p, { brow: '#2E3E2A', browW: 7, eyeRx: 18, eyeRy: 18, pup: 6 })}
        <path d="M-10 -210 Q0 -202 10 -210" stroke="#6E8E56" stroke-width="5" fill="none"/>
      </g>
    </g>
  </g>`;

  const ghostMarkup = () => `
  <g id="gho"><ellipse cx="0" cy="6" rx="100" ry="14" fill="#0E0A1A" opacity=".2"/>
    <g id="gho-bob">
      <g opacity=".92">
        <path d="M-124 -60 Q-136 -330 0 -350 Q136 -330 124 -60 Q104 -20 84 -60 Q64 -20 42 -60 Q22 -20 0 -60 Q-22 -20 -42 -60 Q-64 -20 -84 -60 Q-104 -20 -124 -60 Z" fill="#F4F6FF" stroke="${NAVY}" stroke-width="6" stroke-linejoin="round"/>
        <path id="gho-armL" d="M-118 -200 Q-170 -180 -160 -140 Q-140 -150 -116 -160" fill="#F4F6FF" stroke="${NAVY}" stroke-width="5"/>
        <path id="gho-armR" d="M118 -200 Q170 -180 160 -140 Q140 -150 116 -160" fill="#F4F6FF" stroke="${NAVY}" stroke-width="5"/>
        <path d="M-90 -300 Q-60 -330 -20 -334" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/>
      </g>
      <g id="gho-eyes"><ellipse cx="-40" cy="-238" rx="18" ry="27" fill="${NAVY}"/><ellipse cx="40" cy="-238" rx="18" ry="27" fill="${NAVY}"/>
        <circle cx="-34" cy="-248" r="6" fill="#fff"/><circle cx="46" cy="-248" r="6" fill="#fff"/></g>
      <path id="gho-sad" d="M-62 -280 L-24 -268 M62 -280 L24 -268" stroke="${NAVY}" stroke-width="7" stroke-linecap="round" style="display:none"/>
      <ellipse id="gho-mouth" cx="0" cy="-178" rx="16" ry="20" fill="${NAVY}"/>
      <ellipse cx="-66" cy="-200" rx="16" ry="9" fill="#FFB3C7" opacity=".6"/><ellipse cx="66" cy="-200" rx="16" ry="9" fill="#FFB3C7" opacity=".6"/>
      <path id="gho-tear" d="M-44 -206 Q-50 -186 -44 -178 Q-38 -186 -44 -206 Z" fill="#7FD3FF" stroke="${NAVY}" stroke-width="2" style="display:none"/>
    </g>
  </g>`;

  const batMarkup = () => `<g id="bat" style="display:none"><g id="batWings">
      <path d="M0 0 Q-40 -40 -90 -20 Q-70 -10 -66 10 Q-50 0 -40 14 Q-24 4 0 10 Z" fill="${NAVY}"/><path d="M0 0 Q40 -40 90 -20 Q70 -10 66 10 Q50 0 40 14 Q24 4 0 10 Z" fill="${NAVY}"/></g>
      <ellipse cx="0" cy="4" rx="16" ry="20" fill="${NAVY}"/><path d="M-12 -12 L-8 -26 L-2 -14 Z M12 -12 L8 -26 L2 -14 Z" fill="${NAVY}"/>
      <circle cx="-6" cy="0" r="3.5" fill="#FF3B4E"/><circle cx="6" cy="0" r="3.5" fill="#FF3B4E"/><path d="M-4 12 l2 6 l2 -6" fill="#fff"/></g>`;

  const swarmMarkup = () => Array.from({ length: 12 }, (_, i) => `<g id="sw${i}" style="display:none"><g class="swW"><path d="M0 0 Q-40 -40 -90 -20 Q-70 -10 -66 10 Q-50 0 -40 14 Q-24 4 0 10 Z" fill="${NAVY}"/><path d="M0 0 Q40 -40 90 -20 Q70 -10 66 10 Q50 0 40 14 Q24 4 0 10 Z" fill="${NAVY}"/></g>
      <ellipse cx="0" cy="4" rx="16" ry="20" fill="${NAVY}"/><circle cx="-6" cy="0" r="3.5" fill="#FF3B4E"/><circle cx="6" cy="0" r="3.5" fill="#FF3B4E"/></g>`).join('');

  // ---------------------------------------------------------------- Welt
  const world = () => `${defs}${shopMarkup()}
    <g id="leoW">${leoMarkup('leo')}</g>
    <g id="custW">
      <g id="vlaW">${vladiMarkup('vla')}</g>
      <g id="ghoW">${ghostMarkup()}</g>
      <g id="wwfW">${wolfMarkup('wwf')}</g>
      <g id="zomW">${zombieMarkup('zom')}</g>
    </g>
    <g id="handDoner" style="display:none">${doner(1.1)}</g>
    <g id="fallDoner" style="display:none">${doner(1.1)}</g>
    <g id="splat" style="display:none"><ellipse rx="110" ry="22" fill="#FFFDF4" ${sw}/><circle cx="-50" cy="-10" r="12" fill="#5CC24E"/><circle cx="30" cy="-6" r="10" fill="#E8433E"/><path d="M-20 -14 q20 -10 40 0" stroke="#8A4A2A" stroke-width="10" fill="none"/></g>
    <g id="zArm" style="display:none"><g transform="rotate(90)">${armMarkup('zarm', 'L', '#8FB8D8', '#6E95BF', ZSKIN)}</g></g>
    ${batMarkup()}
    <g id="swarm">${swarmMarkup()}</g>
    <g id="poofs"></g>`;

  // ---------------------------------------------------------------- Zustand
  const LEO = humanEls('leo', 48), VLA = humanEls('vla', 50), WWF = humanEls('wwf', 64), ZOM = humanEls('zom', 50);
  const fig = (x, s, extra = {}) => Object.assign(humanDefaults(), { show: false, x, y: FLOOR, s, cap: false }, extra);
  const base = () => ({
    leo: fig(POS.leo, 1.42, { show: true, prop: null, propL: null, mess: false, duck: 0, tremble: 0 }),
    vla: fig(POS.cust, 1.5, { prop: null, glow: false, sick: 0, lean: 0 }), wwf: fig(POS.cust, 1.55, { wolf: 0 }), zom: fig(POS.cust, 1.42, { armOff: null }),
    gho: { show: false, x: POS.cust, y: FLOOR - 40, s: 1.3, sad: false, tear: false, talk: true },
    bat: null, fall: null, hand: null, moon: 0, spitEaten: false, insp: 0, poofs: [], comics: [], hook: null, cta: null, flash: null,
    swarm: null, btlFall: null, jarBat: false,
    ui: { title: 999 },
  });

  // Kunde links neben der Tür, rechts von der Theke
  const custShot = (S, z = 1.5) => { S.cam = [POS.cust - 10, FLOOR - 470 + 220 / z, z]; };
  const leoShot = (S, z = 1.55) => { S.cam = [POS.leo + 40, FLOOR - 450 + 220 / z, z]; };
  const twoShot = (S, z = 0.98) => { S.cam = [1180, FLOOR - 360, z]; };

  const shots = {
    s01: (S, t, seg, lt, d) => {
      // Kalter Einstieg: Vampir hängt fauchend über der Theke, Leo klebt zitternd am Spieß
      Object.assign(S.vla, { show: true, x: 1430, lean: -16, armL: 150, armR: -150, expr: 'o', glow: true, talk: false, look: [-10, 2] });
      Object.assign(S.leo, { x: 640, expr: 'o', armL: 130, armR: -130, tremble: 1, look: [10, 0], talk: true });
      S.hook = { t0: -1, t1: 2.9 };
      if (lt < 1.4) S.cam = camLerp([1060, FLOOR - 380, 1.3], [1050, FLOOR - 390, 1.38], E.inOut(clamp(lt / 1.4)));
      else if (lt < 2.9) { S.cam = camLerp([1400, FLOOR - 560, 1.85], [1395, FLOOR - 565, 1.95], clamp((lt - 1.4) / 1.5)); S.shake = 0.25; }
      else S.cam = camLerp([680, FLOOR - 520, 1.8], [690, FLOOR - 525, 1.9], clamp((lt - 2.9) / 1.6));
    },
    s02: (S, t, seg, lt) => {
      custShot(S, 1.55); S.vla.show = true; S.vla.look = [-6, 0]; S.vla.armR = -110; S.vla.fingerR = true; S.vla.expr = 'smile';
      S.ui.chip = { text: '⏪ 30 SEKUNDEN VORHER', t0: seg.start - 0.05, cls: 'dark', top: 250 };
      S.flash = seg.start - 0.05;
    },
    s03: (S, t, seg, lt, d) => {
      const e = seg.speechEnd, sw = cue('s03', 'boing'), h0 = cue('s04', 'card'), bite = cue('s04', 'crunch');
      S.vla.show = true;
      if (t < e + 0.05) { leoShot(S, 1.6); S.leo.expr = 'happy'; S.leo.armR = -110; S.leo.prop = 'garlic'; }
      else if (t < sw + 0.25) {
        S.cam = [POS.leo + 170, FLOOR - 600, 2.3]; S.leo.armR = -110; S.leo.expr = 'o'; S.leo.look = [10, -8];
        S.leo.prop = t < sw ? 'garlic' : 'scharf';
        S.comics = [{ id: 'cm0', text: t < sw ? 'KNOBLAUCH?!' : 'PUH …', t0: t < sw ? e + 0.05 : sw, t1: sw + 0.3, wx: POS.leo + 260, wy: FLOOR - 860, rot: -8 }];
      } else {
        twoShot(S, 1.05); S.leo.expr = 'happy'; S.vla.look = [-6, 0];
        if (t < h0 + 0.35) { S.leo.armR = -80; S.hand = { x: lerp(POS.leo + 150, POS.cust - 80, E.inOut(prog(t, h0, 0.35))), y: FLOOR - 430 }; }
        else { S.vla.prop = t < bite ? 'doner' : 'bitten'; S.vla.armR = -120; S.vla.expr = t < bite ? 'smile' : 'o'; }
      }
    },
    s04: (S, t, seg, lt, d) => {
      custShot(S, 1.6); S.vla.show = true; S.vla.prop = 'bitten'; S.vla.armR = -120; S.vla.expr = 'worried'; S.vla.look = [-4, -6];
      S.vla.sick = clamp((lt - d * 0.5) / (d * 0.5));
    },
    s05: (S, t, seg, lt, d) => {
      S.leo.propL = 'bag'; S.leo.armL = 120; S.leo.expr = lt < 0.4 ? 'o' : 'worried'; S.leo.look = [-8, -8];
      if (lt < 0.45) leoShot(S, 1.55); else S.cam = [POS.leo - 90, FLOOR - 600, 2.05];
    },
    s06: (S, t, seg, lt, d) => {
      const pf = seg.speechEnd + 0.05;
      if (t < pf + 0.1) {
        custShot(S, 1.7); Object.assign(S.vla, { show: true, sick: 1, expr: 'o', armL: 150, armR: -150, prop: null, glow: true }); S.shake = 0.6;
      } else {
        S.cam = camLerp([1250, FLOOR - 380, 0.95], [1230, FLOOR - 385, 1.0], clamp((t - pf) / 1.5)); S.shake = 0.35;
        S.swarm = pf; S.btlFall = cue('s06', 'klong') - 0.15;
        S.leo.duck = E.out(clamp((t - pf - 0.15) / 0.3)); S.leo.armL = 160; S.leo.armR = -160; S.leo.expr = 'o';
        S.comics = [{ id: 'cm0', text: 'PUFF!', t0: pf, t1: pf + 0.7, wx: POS.cust, wy: FLOOR - 720, rot: -8 },
          { id: 'cm1', text: 'FLATTER FLATTER!', t0: pf + 0.5, t1: pf + 1.5, wx: 1200, wy: 760, rot: 5 }];
      }
      S.poofs = [{ x: POS.cust, y: FLOOR - 340, t0: pf, s: 1.5 }];
    },
    s07: (S, t, seg, lt) => {
      S.cam = camLerp([1000, FLOOR - 450, 1.32], [990, FLOOR - 455, 1.4], clamp(lt / 2.5));
      Object.assign(S.leo, { mess: true, prop: 'broom', armR: -40, armL: 20, expr: 'worried', look: [4, 0] });
      S.btlFall = -10; S.jarBat = true;
    },
    s08: (S, t, seg, lt) => {
      S.cam = camLerp([1120, FLOOR - 420, 0.98], [1110, FLOOR - 425, 1.02], clamp(lt / 3));
      Object.assign(S.leo, { mess: true, expr: 'happy', armR: -150, fingerR: true, look: [0, 0] });
      S.btlFall = -10; S.jarBat = true;
      S.ui.cards = [cue('s08', 'pop', 0), cue('s08', 'pop', 1), cue('s08', 'pop', 2)];
      S.ui.vote = cue('s08', 'pop', 2) + 0.2;
      S.cta = seg.start + 0.2;
    },
    cover: (S, t) => {
      Object.assign(S.vla, { show: true, x: 1430, lean: -16, armL: 150, armR: -150, expr: 'o', glow: true, talk: false, look: [-10, 2] });
      Object.assign(S.leo, { x: 640, expr: 'o', armL: 130, armR: -130, look: [10, 0], talk: false });
      S.cam = [1060, FLOOR - 330, 1.25];
      return;
      S.leo.expr = 'o'; S.leo.armR = -70; S.leo.prop = 'doner'; S.leo.look = [8, 0]; S.leo.talk = false;
      Object.assign(S.vla, { show: true, x: 1520, expr: 'o', armL: 150, armR: -150, talk: false });
      Object.assign(S.gho, { show: true, x: 1880, talk: false });
      S.moon = 1;
    },
  };

  // ---------------------------------------------------------------- Zeichnen
  const PR = rng(31);
  const POOF = Array.from({ length: 12 }, () => ({ a: PR() * Math.PI * 2, d: 60 + PR() * 120, r: 40 + PR() * 50 }));
  const toScreen = (S, wx, wy) => [540 + (wx - S.cam[0]) * S.cam[2], 960 + (wy - S.cam[1]) * S.cam[2]];

  function placeHuman(H, id, P, t) {
    disp($(id), P.show);
    if (!P.show) return;
    const jx = P.tremble ? Math.sin(t * 70) * 5 * P.tremble : 0, dy = (P.duck || 0) * 150;
    setT($(id), `translate(${P.x + jx},${P.y + dy}) rotate(${P.lean || 0}) scale(${P.s})`);
    poseHuman(H, P, t);
  }
  // Requisiten stehen aufrecht in der Hand (Gruppe wird gegen den Armwinkel gedreht)
  const propMarkup = (k) => k === 'doner' ? `<g transform="translate(0,-10)">${doner(0.9)}</g>`
    : k === 'bitten' ? `<g transform="translate(0,-10)">${doner(0.9)}<circle cx="58" cy="-40" r="32" fill="#22182E"/></g>`
    : k === 'garlic' ? `<g transform="translate(0,60) scale(1.15)">${bottle(0, 0, '#FFFDF4', '#7CFF6B', 'KNOBLAUCH', '#1B1430')}</g>`
    : k === 'scharf' ? `<g transform="translate(0,60) scale(1.15)">${bottle(0, 0, '#E8433E', '#FFD43B', 'SCHARF', '#E8433E')}</g>`
    : k === 'bag' ? `<g transform="translate(0,70) scale(1.15)">${breadBag()}</g>` : k === 'broom' ? `<g transform="translate(0,40)">${broom()}</g>` : '';

  function drawWorld(S, t) {
    // Neon flackert, Spieß dreht sich, Hitze flimmert
    $('neon2').setAttribute('opacity', (Math.sin(t * 13) > 0.92 ? 0.35 : 1).toFixed(2));
    setT($('coneTex'), `translate(${(t * 60) % 30},0)`);
    $('heatGlow').setAttribute('opacity', (0.75 + 0.2 * Math.sin(t * 7)).toFixed(2));
    disp($('cone'), !S.spitEaten);
    document.querySelectorAll('.star').forEach((el) => el.setAttribute('opacity', (0.5 + 0.5 * Math.sin(t * 3 + +el.dataset.p)).toFixed(2)));
    setT($('moonClouds'), `translate(${S.moon * 260},${-S.moon * 40})`);
    $('moonClouds').setAttribute('opacity', (1 - S.moon * 0.7).toFixed(2));
    document.querySelectorAll('.lampCone').forEach((el) => el.setAttribute('opacity', (0.5 + 0.06 * Math.sin(t * 5)).toFixed(2)));
    // Leo
    placeHuman(LEO, 'leoW', S.leo, t);
    const pk = `${S.leo.prop}|${S.leo.propL}|${S.vla.prop}`;
    if ($('leo-propR').dataset.k !== pk) {
      $('leo-propR').innerHTML = propMarkup(S.leo.prop); $('leo-propL').innerHTML = propMarkup(S.leo.propL); $('vla-propR').innerHTML = propMarkup(S.vla.prop);
      $('leo-propR').dataset.k = pk;
    }
    setT($('leo-propR'), `translate(0,104) rotate(${-S.leo.armR})`); setT($('leo-propL'), `translate(0,104) rotate(${-S.leo.armL})`);
    setT($('vla-propR'), `translate(0,104) rotate(${-S.vla.armR})`);
    disp($('leo-mess'), S.leo.mess); setT($('leo-cap'), S.leo.mess ? 'rotate(-14 0 -310) translate(-10,6)' : '');
    disp($('vla-glow'), S.vla.glow); $('vla-sick').setAttribute('opacity', (0.75 * S.vla.sick).toFixed(2));
    // Flaschen fallen um, Fledermaus im Trinkgeldglas
    const bf = S.btlFall !== null ? E.out(clamp((t - S.btlFall) / 0.35)) : 0;
    setT($('btlK'), `rotate(${-82 * bf} -164 -26)`); setT($('btlS'), `rotate(${70 * bf} -56 -26)`);
    disp($('jarBat'), S.jarBat);
    // Fledermausschwarm: kreist durch den Laden, fliegt dann zur Tür hinaus
    for (let i = 0; i < 12; i++) {
      const el = $(`sw${i}`);
      if (S.swarm === null || t < S.swarm) { disp(el, false); continue; }
      const a = t - S.swarm, k = clamp(a / 0.5), out = clamp((a - 1.9 - i * 0.04) / 0.7);
      const ph = i * 0.52, rx = 380 + (i % 4) * 110, ry = 170 + (i % 3) * 60;
      let x = lerp(POS.cust, 1250 + Math.cos(a * 3.2 + ph) * rx, k), y = lerp(FLOOR - 560, 1080 + Math.sin(a * 4.1 + ph * 1.7) * ry, k);
      x = lerp(x, POS.door + 400, E.in(out)); y = lerp(y, 900, E.in(out));
      disp(el, out < 1);
      setT(el, `translate(${x.toFixed(0)},${y.toFixed(0)}) scale(${(1 + (i % 3) * 0.25).toFixed(2)})`);
      setT(el.querySelector('.swW'), `scale(1,${(0.35 + 0.65 * Math.abs(Math.sin(t * 24 + i))).toFixed(2)})`);
    }
    // Kunden
    placeHuman(VLA, 'vlaW', S.vla, t);
    const W = S.wwf;
    placeHuman(WWF, 'wwfW', W, t);
    if (W.show) { disp($('wwf-human'), W.wolf < 0.5); disp($('wwf-wolf'), W.wolf >= 0.5); $('wwf-fur').setAttribute('opacity', W.wolf);
      setT($('wwf-jaw'), `translate(0,${Math.abs(Math.sin(t * 9)) * 10})`); }
    const Z = S.zom;
    placeHuman(ZOM, 'zomW', Z, t);
    if (Z.show && Z.armOff !== null && t >= Z.armOff) {
      // Arm fällt ab und landet auf der Theke
      const k = clamp((t - Z.armOff) / 0.45);
      disp(ZOM.armL, false);
      const sx = Z.x - 50 * Z.s, sy = Z.y - 160 * Z.s;
      const tx = 1300, ty = 1360;
      disp($('zArm'), true);
      setT($('zArm'), `translate(${lerp(sx, tx, k)},${lerp(sy, ty, k) - Math.sin(k * Math.PI) * 140}) rotate(${k * 260}) scale(${Z.s * 0.95})`);
    } else { disp($('zArm'), false); if (Z.show) disp(ZOM.armL, true); }
    const G = S.gho;
    disp($('ghoW'), G.show);
    if (G.show) {
      setT($('ghoW'), `translate(${G.x},${G.y + Math.sin(t * 2.6) * 14}) scale(${G.s})`);
      const talk = G.talk ? Engine.envAt(t) : 0;
      setT($('gho-mouth'), `translate(0,-178) scale(1,${(G.sad ? 0.55 : 0.7) + talk * 0.9}) translate(0,178)`);
      disp($('gho-sad'), G.sad); disp($('gho-tear'), G.tear);
      const bt = (t + 0.4) % 3.1; setT($('gho-eyes'), `translate(0,-238) scale(1,${bt < 0.12 ? 0.15 : 1}) translate(0,238)`);
    }
    // Döner in der Hand, fallender Döner, Matsch
    const hd = $('handDoner');
    if (S.hand) { disp(hd, true); setT(hd, `translate(${S.hand.x},${S.hand.y})`); } else disp(hd, false);
    const fd = $('fallDoner'), spl = $('splat');
    if (S.fall) {
      const done = t >= S.fall.splat;
      disp(fd, !done); setT(fd, `translate(${S.fall.x},${S.fall.y}) rotate(${S.fall.rot})`);
      disp(spl, done); setT(spl, `translate(${S.fall.x},${FLOOR - 4}) scale(${done ? 1 + 0.15 * popS(t, S.fall.splat, 0.2) : 1})`);
    } else { disp(fd, false); disp(spl, false); }
    // Fledermaus
    const b = $('bat');
    if (S.bat) { disp(b, true); setT(b, `translate(${S.bat.x},${S.bat.y}) scale(${S.bat.s})`); setT($('batWings'), `scale(1,${0.4 + 0.6 * Math.abs(Math.sin(t * 22))})`); }
    else disp(b, false);
    // Kontrolleur hinter der Glastür
    disp($('insp'), S.insp > 0); $('insp').setAttribute('opacity', S.insp.toFixed(2));
    setT($('inspBody'), `translate(${(1 - S.insp) * 160},0)`);
    $('inspLight').setAttribute('opacity', Math.sin(t * 8) > 0 ? 1 : 0.3);
    // Rauchwolken
    let pf = '';
    for (const P of S.poofs) {
      const lt = t - P.t0;
      if (lt < 0 || lt > 1.1) continue;
      const k = E.out(clamp(lt / 0.5)), o = clamp(1 - (lt - 0.3) / 0.8);
      for (const q of POOF) pf += `<circle cx="${(P.x + Math.cos(q.a) * q.d * k * P.s).toFixed(0)}" cy="${(P.y + Math.sin(q.a) * q.d * k * P.s * 0.8).toFixed(0)}" r="${(q.r * P.s * (0.6 + 0.6 * k)).toFixed(0)}" fill="url(#gPoof)" opacity="${o.toFixed(2)}"/>`;
    }
    $('poofs').innerHTML = pf;
    drawOverlay(S, t);
  }

  function drawOverlay(S, t) {
    const hk = $('hook');
    if (S.hook && t < S.hook.t1 + 0.25) {
      const s = 1 - E.in(prog(t, S.hook.t1, 0.25));
      hk.style.display = 'block'; hk.style.opacity = clamp(s * 3);
      hk.style.transform = `translateX(-50%) rotate(-2deg) scale(${Math.max(0.001, s) * (1 + 0.015 * Math.sin(t * 5))})`;
    } else hk.style.display = 'none';
    const ct = $('cta');
    if (S.cta !== null && t >= S.cta) {
      ct.style.display = 'block';
      ct.style.transform = `translateX(-50%) rotate(-3deg) scale(${popS(t, S.cta, 0.35) * (1 + 0.04 * Math.max(0, Math.sin(t * 8)))})`;
    } else ct.style.display = 'none';
    ['cm0', 'cm1', 'cm2'].forEach((id) => {
      const el = $(id), c = S.comics.find((x) => x.id === id);
      if (!c || t < c.t0 || t > c.t1) { el.style.display = 'none'; return; }
      const [sx, sy] = toScreen(S, c.wx, c.wy);
      if (el.dataset.text !== c.text) { el.textContent = c.text; el.dataset.text = c.text; }
      el.style.display = 'block'; el.style.left = `${sx}px`; el.style.top = `${sy}px`;
      el.style.opacity = clamp((c.t1 - t) * 4);
      el.style.transform = `translate(-50%,-50%) rotate(${c.rot}deg) scale(${popS(t, c.t0, 0.2)})`;
    });
    $('flash').style.opacity = S.flash !== null && t >= S.flash ? (1 - clamp((t - S.flash) / 0.3)) * 0.8 : 0;
  }

  const emoIcon = (e) => `<div class="icon">${e}</div>`;
  Engine.start({
    world, shots, drawWorld,
    baseState: base,
    highlight: '#7CFF6B',
    whip: { skip: ['s05'] },
    karaoke: true,
    punch: 0.06,
    confettiColors: ['#7CFF6B', '#FF5CC8', '#FFD43B', '#fff', '#5CC8FF', '#B67CFF'],
    preload: '🧛🥙👻🧟🐺😬😰⏪!…',
    ui: {
      day: 'TAG 1',
      profile: { name: 'Monsterdöner', handle: '@monsterdoener', avatar: '🥙', stat: 'Kunden', foot: '1 Follower = 1 Kunde 🥙' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '🥙', text: 'BESTELLT!' }, plusOne: '+1 KUNDE', zirp: '',
      ticket: '', tstamp: '', kasse: 'KASSE',
      cards: [
        { color: '#B9876A', icon: emoIcon('🐺'), label: 'WERWOLF' },
        { color: '#E9EEFF', icon: emoIcon('👻'), label: 'GEIST' },
        { color: '#A9CC86', icon: emoIcon('🧟'), label: 'ZOMBIE' },
      ],
      floats: [], ccards: [],
    },
  });
  window.ART = { leoMarkup, vladiMarkup, ghostMarkup, wolfMarkup, zombieMarkup, doner, defs, OUT, NAVY };
})();

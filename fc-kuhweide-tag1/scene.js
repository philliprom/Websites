/* FC Kuhweide – Tag 1. Dorf-Bolzplatz, Trainer Kalle und Torwart Berta (eine Kuh). */
(() => {
  const { $, clamp, lerp, E, prog, popS, rng, byId, cue, cues, setT, disp, fmt, camLerp, OUT, sw,
    humanEls, humanDefaults, poseHuman, faceMarkup, armMarkup, TL } = Engine;

  const SKIN = '#F1C6A0', SKIN_SH = '#DFA67E';
  const HAIR = '#5A3A22';
  const SUIT = '#1F8A55', SUIT_D = '#17704A';

  // ---------------------------------------------------------------- Trainer Kalle
  const kalleMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="0" cy="4" rx="86" ry="13" fill="#1E3A1A" opacity=".22"/>
    <g id="${p}-bob">
      <path d="M-40 -70 L-12 -70 L-12 -30 L-40 -30 Z" fill="${SUIT_D}" ${sw}/>
      <path d="M12 -70 L40 -70 L40 -30 L12 -30 Z" fill="${SUIT_D}" ${sw}/>
      <path d="M-38 -66 L-38 -32 M38 -66 L38 -32" stroke="#fff" stroke-width="5"/>
      <path d="M-52 0 L-6 0 L-6 -24 Q-6 -34 -16 -34 L-40 -34 Q-52 -34 -52 -20 Z" fill="#fff" ${sw}/>
      <path d="M52 0 L6 0 L6 -24 Q6 -34 16 -34 L40 -34 Q52 -34 52 -20 Z" fill="#fff" ${sw}/>
      <path d="M-52 -6 H-6 M52 -6 H6" stroke="#E23A4E" stroke-width="6"/>
      <g id="${p}-armL" transform="translate(-56,-160)">${armMarkup(p, 'L', SUIT, '#fff', SKIN)}</g>
      <path d="M-56 -174 Q-86 -120 -76 -66 Q0 -50 76 -66 Q86 -120 56 -174 Q0 -188 -56 -174 Z" fill="${SUIT}" ${sw}/>
      <path d="M24 -178 Q50 -176 56 -172 Q84 -120 74 -68 Q54 -58 34 -58 Q52 -116 24 -178 Z" fill="${SUIT_D}" opacity=".6"/>
      <path d="M-56 -170 Q-80 -120 -74 -70 M56 -170 Q80 -120 74 -70" stroke="#fff" stroke-width="5" fill="none"/>
      <line x1="0" y1="-176" x2="0" y2="-58" stroke="#E9EEF4" stroke-width="5"/>
      <rect x="-4" y="-150" width="8" height="12" rx="2" fill="#C9D3DE"/>
      <path d="M-26 -184 L0 -164 L26 -184" stroke="#fff" stroke-width="7" fill="none" stroke-linejoin="round"/>
      <path d="M-18 -176 Q-4 -150 14 -132" stroke="#E23A4E" stroke-width="3.5" fill="none"/>
      <g transform="translate(18,-128) rotate(-20)"><rect x="-14" y="-7" width="28" height="15" rx="7" fill="#C9D3DE" stroke="${OUT}" stroke-width="3.5"/><rect x="12" y="-4" width="12" height="8" rx="2" fill="#C9D3DE" stroke="${OUT}" stroke-width="3"/></g>
      <g id="${p}-armR" transform="translate(56,-160)">${armMarkup(p, 'R', SUIT, '#fff', SKIN)}</g>
      <g id="${p}-head">
        <ellipse cx="-75" cy="-226" rx="14" ry="18" fill="${SKIN}" ${sw}/>
        <ellipse cx="75" cy="-226" rx="14" ry="18" fill="${SKIN}" ${sw}/>
        <ellipse cx="0" cy="-234" rx="77" ry="75" fill="${SKIN}" ${sw}/>
        <path d="M-80 -232 Q-90 -300 -30 -316 Q40 -330 78 -284 Q86 -262 80 -232 Q72 -268 50 -282 Q10 -290 -20 -284 Q-46 -292 -64 -270 Q-74 -256 -80 -232 Z" fill="${HAIR}" ${sw}/>
        <path d="M-20 -284 Q-6 -306 22 -312" stroke="#7A5232" stroke-width="5" fill="none" stroke-linecap="round"/>
        <ellipse cx="-50" cy="-200" rx="14" ry="8" fill="#FF7E86" opacity=".5"/>
        <ellipse cx="50" cy="-200" rx="14" ry="8" fill="#FF7E86" opacity=".5"/>
        ${faceMarkup(p, { brow: HAIR, browW: 11 })}
        <path d="M-9 -212 Q0 -198 9 -212" stroke="${SKIN_SH}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M-46 -188 Q-24 -212 0 -198 Q24 -212 46 -188 Q34 -184 22 -190 Q10 -182 0 -190 Q-10 -182 -22 -190 Q-34 -184 -46 -188 Z" fill="${HAIR}" ${sw}/>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Kuh Berta (schaut nach links)
  const spot = (d) => `<path d="${d}" fill="${OUT}"/>`;
  const bertaMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="0" cy="4" rx="170" ry="14" fill="#1E3A1A" opacity=".22"/>
    <g id="${p}-bob">
      <g id="${p}-tail" transform="translate(148,-196)"><path d="M0 0 Q20 50 10 110" stroke="${OUT}" stroke-width="6" fill="none" stroke-linecap="round"/>
        <path d="M2 104 Q16 96 22 120 Q8 136 0 116 Z" fill="${OUT}"/></g>
      ${[[96, 1], [124, 1]].map(([x]) => `<rect x="${x - 15}" y="-112" width="30" height="112" rx="12" fill="#F6F6F8" ${sw}/><rect x="${x - 15}" y="-18" width="30" height="18" rx="5" fill="#59606E" ${sw}/>`).join('')}
      <rect x="-156" y="-218" width="312" height="132" rx="56" fill="#F6F6F8" ${sw}/>
      ${spot('M-60 -214 Q-20 -222 10 -200 Q20 -170 -10 -160 Q-50 -150 -70 -180 Q-80 -205 -60 -214 Z')}
      ${spot('M60 -150 Q90 -170 120 -150 Q130 -120 100 -110 Q70 -100 56 -124 Z')}
      ${spot('M110 -214 Q140 -212 150 -190 Q140 -176 118 -186 Z')}
      <ellipse cx="50" cy="-86" rx="26" ry="14" fill="#FFB3C1" ${sw}/>
      ${[[-110, 1], [-82, 1]].map(([x]) => `<rect x="${x - 15}" y="-112" width="30" height="112" rx="12" fill="#F6F6F8" ${sw}/>
        <g transform="translate(${x},-14)"><path d="M-24 14 L-24 -14 Q-24 -30 -8 -30 L8 -30 Q24 -30 24 -14 L24 14 Z" fill="#FF7A1A" ${sw}/>
        <path d="M-24 -6 H24" stroke="#fff" stroke-width="6"/><path d="M-30 -20 Q-34 -34 -22 -36" stroke="${OUT}" stroke-width="5" fill="#FF7A1A"/></g>`).join('')}
      <g id="${p}-head">
        <path d="M-210 -270 L-226 -296 L-198 -282 Z M-144 -270 L-128 -296 L-156 -282 Z" fill="#F5E6C4" ${sw}/>
        <ellipse cx="-236" cy="-246" rx="26" ry="13" fill="#F6F6F8" ${sw} transform="rotate(-20 -236 -246)"/>
        <ellipse cx="-118" cy="-246" rx="26" ry="13" fill="#F6F6F8" ${sw} transform="rotate(20 -118 -246)"/>
        <ellipse cx="-177" cy="-222" rx="56" ry="62" fill="#F6F6F8" ${sw}/>
        ${spot('M-150 -276 Q-128 -260 -130 -232 Q-150 -226 -164 -246 Q-170 -268 -150 -276 Z')}
        <g id="${p}-eyes">
          <circle cx="-198" cy="-236" r="11" fill="#fff" stroke="${OUT}" stroke-width="3.5"/><circle cx="-156" cy="-236" r="11" fill="#fff" stroke="${OUT}" stroke-width="3.5"/>
          <circle cx="-197" cy="-234" r="6" fill="${OUT}"/><circle cx="-155" cy="-234" r="6" fill="${OUT}"/>
          <path d="M-210 -240 Q-198 -250 -186 -240 Z M-168 -240 Q-156 -250 -144 -240 Z" fill="#E4E4EA" stroke="${OUT}" stroke-width="3"/>
          <path d="M-212 -244 l-6 -6 M-142 -244 l6 -6" stroke="${OUT}" stroke-width="3" stroke-linecap="round"/>
        </g>
        <g id="${p}-muzzle">
          <ellipse cx="-177" cy="-176" rx="48" ry="32" fill="#FFB3C1" ${sw}/>
          <ellipse cx="-193" cy="-182" rx="7" ry="5" fill="#C9677A"/><ellipse cx="-161" cy="-182" rx="7" ry="5" fill="#C9677A"/>
          <path id="${p}-mouth" d="M-196 -162 Q-177 -152 -158 -162" stroke="${OUT}" stroke-width="4" fill="none" stroke-linecap="round"/>
          <ellipse id="${p}-moo" cx="-177" cy="-160" rx="14" ry="10" fill="#7A2633" stroke="${OUT}" stroke-width="3" style="display:none"/>
          <g id="${p}-grass" style="display:none"><path d="M-160 -160 L-138 -186 M-158 -158 L-130 -170 M-162 -160 L-148 -192" stroke="#3FAE5A" stroke-width="5" stroke-linecap="round"/></g>
          <g id="${p}-bill" style="display:none" transform="translate(-150,-166) rotate(-14)"><rect x="0" y="-12" width="54" height="26" rx="3" fill="#7FD3A0" stroke="${OUT}" stroke-width="3"/>
            <text x="27" y="7" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="15" fill="${OUT}">50 €</text></g>
        </g>
        <path d="M-200 -124 Q-177 -110 -154 -124" stroke="#E23A4E" stroke-width="10" fill="none" stroke-linecap="round"/>
        <path d="M-190 -116 L-164 -116 L-158 -88 L-196 -88 Z" fill="#F2C14E" ${sw}/>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Requisiten
  const ballMarkup = () => `<circle r="26" fill="#fff" ${sw}/><path d="M0 -10 L10 -3 L6 9 L-6 9 L-10 -3 Z" fill="${OUT}"/>
    <path d="M0 -10 L0 -25 M10 -3 L24 -8 M6 9 L14 21 M-6 9 L-14 21 M-10 -3 L-24 -8" stroke="${OUT}" stroke-width="3"/>`;
  const pigeonMarkup = () => `
    <path d="M18 -30 L44 -22 L20 -16 Z" fill="#7C8798" ${sw}/>
    <ellipse cx="0" cy="-26" rx="30" ry="22" fill="#A7B1C1" ${sw}/>
    <path d="M-4 -40 Q16 -30 30 -20" stroke="#7C8798" stroke-width="7" fill="none" stroke-linecap="round"/>
    <g id="pgHead"><ellipse cx="-24" cy="-44" rx="16" ry="14" fill="#8FA0B5" ${sw}/><path d="M-34 -36 Q-26 -28 -14 -34" stroke="#6FB59A" stroke-width="6" fill="none"/>
      <path d="M-38 -46 L-50 -42 L-38 -40 Z" fill="#F2C14E" stroke="${OUT}" stroke-width="2.5"/><circle cx="-28" cy="-48" r="4" fill="#FF8A2B" stroke="${OUT}" stroke-width="2"/></g>
    <path d="M-6 -4 L-8 4 M6 -4 L8 4" stroke="#F58FA8" stroke-width="4" stroke-linecap="round"/>`;
  const bucketMarkup = () => `
    <path d="M-30 -60 L-20 -120 M-10 -64 L0 -128 M10 -62 L22 -122 M24 -60 L36 -112 M-22 -62 L-38 -110" stroke="#3FAE5A" stroke-width="7" stroke-linecap="round"/>
    <path d="M-44 -66 L44 -66 L36 0 L-36 0 Z" fill="#B7C0CC" ${sw}/><path d="M-40 -40 H40" stroke="#8E99AA" stroke-width="5"/>
    <path d="M-44 -66 Q0 -110 44 -66" stroke="${OUT}" stroke-width="4" fill="none"/>`;
  const boxMarkup = () => `
    <rect x="-70" y="-56" width="140" height="56" rx="8" fill="#8E99AA" ${sw}/>
    <rect x="-14" y="-40" width="28" height="18" rx="4" fill="#F2C14E" ${sw}/>
    <g id="boxCoins"></g>
    <g id="boxLid" transform="translate(0,-56)"><rect x="-74" y="-22" width="148" height="22" rx="6" fill="#A7B1C1" ${sw}/><rect x="-24" y="-30" width="48" height="10" rx="5" fill="${OUT}"/></g>`;
  const moleMarkup = () => `<g id="mole" style="display:none"><ellipse cx="0" cy="-30" rx="26" ry="24" fill="#4A3A34" ${sw}/>
    <ellipse cx="0" cy="-20" rx="12" ry="9" fill="#FF8FA6" ${sw}/><rect x="-24" y="-46" width="48" height="14" rx="7" fill="${OUT}"/><path d="M-14 -40 H14" stroke="#5CC8FF" stroke-width="4"/></g>`;

  // ---------------------------------------------------------------- Welt
  const HILLS = [[30, 1190], [220, 1250], [420, 1180], [600, 1400], [1050, 1430], [1400, 1210], [1500, 1480], [480, 1520], [2000, 1420], [2250, 1220], [-150, 1350], [1250, 1600], [760, 1700], [1800, 1650]];
  function world() {
    const r = rng(12);
    const clouds = [[200, 300, 1.1], [850, 200, 0.9], [1500, 360, 1.3], [2200, 240, 1.0], [-400, 260, 1.1]].map(([x, y, s], i) =>
      `<g id="cloud${i}" data-x="${x}" data-y="${y}" data-s="${s}"><g fill="#fff" opacity=".93"><ellipse rx="120" ry="40"/><circle cx="-50" cy="-20" r="46"/><circle cx="20" cy="-40" r="58"/><circle cx="74" cy="-12" r="40"/></g></g>`).join('');
    let trees = '';
    for (let i = 0; i < 12; i++) {
      const x = -400 + i * 300 + r() * 100, s = 0.6 + r() * 0.5;
      if (x > 200 && x < 700) continue;
      trees += `<g transform="translate(${x},990) scale(${s})"><rect x="-10" y="-60" width="20" height="60" fill="#6B4A2E"/><circle cx="0" cy="-120" r="74" fill="#5FA548"/><circle cx="-46" cy="-80" r="46" fill="#5FA548"/><circle cx="48" cy="-84" r="50" fill="#5FA548"/></g>`;
    }
    let stripes = '';
    let y = 1060;
    for (let i = 0; i < 16; i++) { const h = 40 + i * 22; stripes += `<rect x="-1500" y="${y}" width="5200" height="${h}" fill="${i % 2 ? '#78C152' : '#6DB549'}"/>`; y += h; }
    const hills = HILLS.map(([x, yy], i) => `<g id="hill${i}" transform="translate(${x},${yy})"><path d="M-44 0 Q-36 -30 0 -32 Q36 -30 44 0 Z" fill="#8A5A36" ${sw}/><path d="M-18 -18 Q0 -26 16 -18" stroke="#A9744A" stroke-width="5" fill="none" stroke-linecap="round"/></g>`).join('');
    return `
    <defs>
      <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5BB3F0"/><stop offset="1" stop-color="#CDEBFF"/></linearGradient>
      <pattern id="netPat" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M0 0 L22 22 M22 0 L0 22" stroke="#fff" stroke-width="2"/></pattern>
    </defs>
    <rect x="-1500" y="-2600" width="5200" height="3700" fill="url(#gSky)"/>
    <g id="clouds">${clouds}</g>
    <path d="M-1500 1000 Q-900 820 -300 960 Q300 840 900 960 Q1500 830 2100 950 Q2700 860 3700 980 L3700 1100 L-1500 1100 Z" fill="#9CD27A"/>
    <path d="M-1500 1040 Q-700 900 0 1010 Q800 920 1600 1010 Q2400 930 3700 1030 L3700 1100 L-1500 1100 Z" fill="#86C566"/>
    <g transform="translate(2150,960)"><rect x="-26" y="-140" width="52" height="140" fill="#F4EFE6"/><path d="M-30 -140 L0 -250 L30 -140 Z" fill="#5A6577"/><rect x="-10" y="-110" width="20" height="30" rx="10" fill="#5A6577"/></g>
    ${trees}
    <g id="barn" transform="translate(440,1010)">
      <rect x="-200" y="-220" width="400" height="220" fill="#C8443A" ${sw}/>
      <path d="M-226 -210 L-120 -330 L120 -330 L226 -210 Z" fill="#6A4A3A" ${sw}/>
      <rect x="-70" y="-150" width="140" height="150" fill="#fff" ${sw}/>
      <path d="M-70 -150 L70 0 M70 -150 L-70 0" stroke="#C8443A" stroke-width="12"/>
      <rect x="-30" y="-290" width="60" height="50" fill="#fff" ${sw}/>
    </g>
    ${stripes}
    <g id="fence">${Array.from({ length: 40 }, (_, i) => `<rect x="${-1200 + i * 130}" y="1010" width="14" height="70" fill="#B98048"/>`).join('')}
      <rect x="-1300" y="1022" width="5000" height="12" fill="#D9A066"/><rect x="-1300" y="1052" width="5000" height="12" fill="#D9A066"/></g>
    <g id="flagBanner" transform="translate(820,1004) rotate(-1.5)">
      <rect x="-280" y="-40" width="560" height="78" rx="6" fill="#fff" ${sw}/>
      <text x="0" y="10" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#E23A4E">FC KUHWEIDE · GEGR. HEUTE</text>
    </g>
    <g fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".92">
      <path d="M-1400 1110 Q-400 1104 600 1114 Q1600 1120 3600 1108"/>
      <path d="M1560 1300 Q1556 1220 1562 1130 M1562 1300 Q1800 1306 2140 1298"/>
      <path d="M380 1600 Q300 1460 380 1330 Q470 1250 560 1320"/>
    </g>
    <g id="hills">${hills}</g>
    ${moleMarkup()}
    <g id="tribSign" transform="translate(600,1300)"><rect x="-7" y="-170" width="14" height="172" fill="#8C5A30" ${sw}/>
      <rect x="-90" y="-210" width="180" height="56" rx="8" fill="#fff" ${sw}/><text x="0" y="-172" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="#E23A4E">TRIBÜNE</text></g>
    <g id="bench"><rect x="640" y="1262" width="390" height="22" rx="6" fill="#C08A52" ${sw}/>
      <path d="M670 1284 L660 1330 M700 1284 L710 1330 M970 1284 L960 1330 M1000 1284 L1010 1330" stroke="#8C5A30" stroke-width="10" stroke-linecap="round"/></g>
    <g id="ghost" transform="translate(830,1262)" style="display:none">
      <ellipse cx="0" cy="2" rx="62" ry="14" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="12 10"/>
      <g id="ghostBody"><rect x="-30" y="-92" width="60" height="92" rx="28" fill="#E23A4E" ${sw}/>
        <path d="M-30 -60 H30" stroke="#fff" stroke-width="10"/>
        <circle cx="0" cy="-124" r="36" fill="#FFE0C7" ${sw}/><circle cx="-12" cy="-128" r="5" fill="${OUT}"/><circle cx="12" cy="-128" r="5" fill="${OUT}"/>
        <path d="M-12 -112 Q0 -102 12 -112" stroke="${OUT}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
        <path id="ghostArm" d="M26 -70 L52 -110" stroke="#E23A4E" stroke-width="18" stroke-linecap="round"/></g>
      <g id="ghostArrow"><path d="M-22 -230 H22 V-262 H-22 Z M-40 -230 L0 -190 L40 -230 Z" fill="#FFC83A" ${sw}/></g>
    </g>
    <g id="pigeon" style="display:none">${pigeonMarkup()}</g>
    <g id="cashbox" transform="translate(760,1262)" style="display:none">${boxMarkup()}</g>
    <g id="goal">
      <rect id="goalNet" x="1650" y="1090" width="400" height="210" fill="url(#netPat)" opacity=".7" style="display:none"/>
      <rect x="1626" y="1070" width="24" height="232" fill="#fff" ${sw}/><rect x="2050" y="1070" width="24" height="232" fill="#fff" ${sw}/>
      <rect x="1626" y="1064" width="448" height="24" fill="#fff" ${sw}/>
      <g id="netTag" transform="translate(1840,1088)" style="display:none"><line x1="0" y1="0" x2="0" y2="26" stroke="${OUT}" stroke-width="3"/>
        <g transform="translate(0,26) rotate(6)"><rect x="-80" y="0" width="160" height="46" rx="8" fill="#fff" ${sw}/>
          <text x="0" y="33" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" fill="#E8243B">OHNE NETZ</text></g></g>
    </g>
    <g id="bucket" transform="translate(1600,1340)" style="display:none">${bucketMarkup()}</g>
    <g id="bertaW" style="display:none">${bertaMarkup('b1')}</g>
    <g id="kalleW" transform="translate(1180,1350)">${kalleMarkup('k1')}</g>
    <g id="ball" transform="translate(1290,1336)">${ballMarkup()}</g>
    <g id="qmarks" font-family="Fredoka" font-weight="700" font-size="70" fill="#fff" stroke="${OUT}" stroke-width="8" paint-order="stroke" style="display:none">
      <text id="q1">?</text><text id="q2">?</text>
    </g>`;
  }

  // ---------------------------------------------------------------- Traum-Stadion
  const CROWD = (() => {
    const r = rng(77), out = [];
    for (let i = 0; i < 2600; i++) {
      const a = r() * Math.PI * 2, k = 0.62 + r() * 0.36;
      out.push({ x: 540 + Math.cos(a) * 560 * k, y: 1150 + Math.sin(a) * 470 * k, c: Math.floor(r() * 4), o: r() });
    }
    return out.sort((a, b) => a.o - b.o);
  })();
  function alt() {
    const r = rng(9);
    let stars = '';
    for (let i = 0; i < 80; i++) stars += `<circle class="star" cx="${r() * 1080}" cy="${r() * 600}" r="${1 + r() * 2.5}" fill="#fff" data-p="${r() * 6}"/>`;
    const tower = (x, y, flip) => `<g transform="translate(${x},${y}) scale(${flip ? -1 : 1},1)">
      <path d="M0 0 L-30 -520 L120 -560 Z" fill="#FFFBD6" opacity=".14"/>
      <rect x="-8" y="-420" width="16" height="420" fill="#8E99AA"/>
      <rect x="-60" y="-470" width="120" height="70" rx="8" fill="#5A6577" ${sw}/>
      ${[-40, -14, 12, 38].map((xx) => `<circle cx="${xx}" cy="-446" r="10" fill="#FFF7C2"/><circle cx="${xx}" cy="-420" r="10" fill="#FFF7C2"/>`).join('')}</g>`;
    return `
    <defs><linearGradient id="gNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16204A"/><stop offset="1" stop-color="#2E3D7A"/></linearGradient></defs>
    <rect width="1080" height="1920" fill="url(#gNight)"/>
    <g id="stars">${stars}</g>
    <g id="stadCam">
      ${tower(110, 760, false)}${tower(970, 760, true)}
      <ellipse cx="540" cy="1150" rx="600" ry="510" fill="#3A4466" ${sw}/>
      <ellipse cx="540" cy="1150" rx="560" ry="470" fill="#48527A"/>
      <g id="crowd"><path id="cr0" fill="#E23A4E"/><path id="cr1" fill="#FFFFFF"/><path id="cr2" fill="#FFC83A"/><path id="cr3" fill="#5CC8FF"/></g>
      <ellipse cx="540" cy="1150" rx="350" ry="260" fill="#4FA83A" ${sw}/>
      ${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="${190 + i * 116}" y="890" width="58" height="520" fill="#5DB846" opacity=".7"/>`).join('')}
      <g fill="none" stroke="#fff" stroke-width="5" opacity=".9"><ellipse cx="540" cy="1150" rx="300" ry="215"/><line x1="540" y1="935" x2="540" y2="1365"/><circle cx="540" cy="1150" r="60"/></g>
      <g id="stadKalle" transform="translate(540,1200) scale(.55)">${kalleMarkup('k2')}</g>
    </g>`;
  }

  // ---------------------------------------------------------------- Icons
  const lightIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><path d="M58 40 L20 112 L100 112 Z" fill="#FFF3A6" opacity=".8"/>
    <rect x="56" y="34" width="8" height="84" fill="#8E99AA" stroke="${OUT}" stroke-width="3"/>
    <rect x="22" y="8" width="76" height="40" rx="8" fill="#5A6577" stroke="${OUT}" stroke-width="5"/>
    ${[34, 52, 70, 88].map((x) => `<circle cx="${x - 4}" cy="20" r="6" fill="#FFF7C2"/><circle cx="${x - 4}" cy="36" r="6" fill="#FFF7C2"/>`).join('')}</svg>`;
  const netIcon = `<svg width="130" height="120" viewBox="0 0 130 120"><rect x="14" y="26" width="102" height="80" fill="url(#iconNet)"/>
    <defs><pattern id="iconNet" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 0 L12 12 M12 0 L0 12" stroke="#8E99AA" stroke-width="2"/></pattern></defs>
    <path d="M10 108 L10 22 L120 22 L120 108" fill="none" stroke="${OUT}" stroke-width="9" stroke-linejoin="round"/>
    <path d="M10 108 L10 22 L120 22 L120 108" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
    <g transform="translate(66,82) scale(.6)">${ballMarkup()}</g></svg>`;
  const qIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><text x="60" y="100" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="112" fill="#FF4B5C" stroke="${OUT}" stroke-width="7" paint-order="stroke">?</text></svg>`;

  // ---------------------------------------------------------------- Zustand + Schnitte
  const base = () => ({
    kal: Object.assign(humanDefaults(), { x: 1180, y: 1350, s: 1 }),
    berta: null, ball: { x: 1290, y: 1336, r: 0 }, hills: 1, mole: null, ghost: null, pigeon: null, bucket: null, box: null,
    net: false, netTag: null, qmarks: null,
  });
  const B = (o) => Object.assign({ x: 1850, y: 1302, s: 1, chew: true, moo: false, grass: false, bill: false, hop: false }, o);

  const shots = {
    s01(S, t, s, lt, d) { S.cam = camLerp([1250, 1100, 0.72], [1250, 1140, 0.8], E.inOut(clamp(lt / d))); S.ui.title = s.start - 0.15; S.kal.armR = -150 + Math.sin(t * 12) * 16; S.berta = B({}); },
    s02(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1160, 2.55], [1180, 1160, 2.72], lt / d);
      S.kal.armR = -150 + Math.sin(t * 12) * 18;
      S.ui.chip = { t0: cue('s02', 'pop'), text: '📣 KALLE · TRAINER', cls: 'yellow' };
    },
    s03(S, t, s, lt, d) {
      S.cam = camLerp([1230, 1150, 1.2], [1230, 1145, 1.32], lt / d);
      const st = cue('s03', 'stamp');
      if (t < st) { S.kal.armL = 70; S.kal.armR = -70; } else { S.kal.armL = 155 + Math.sin(t * 9) * 8; S.kal.armR = -155; S.kal.expr = 'happy'; S.kal.bounce = true; }
      S.ui.stamp = st; S.confetti = cue('s03', 'confetti');
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s04(S, t, s, lt, d) {
      S.cam = camLerp([1060, 1080, 0.95], [1060, 1080, 1.0], lt / d);
      S.kal.armR = -160; S.kal.fingerR = true; S.kal.look = [3, -7];
      S.ui.profile = { t0: s.start + 0.03, followAt: null };
    },
    s05(S, t, s, lt, d) {
      S.cam = camLerp([1060, 1080, 1.0], [1060, 1080, 1.05], lt / d);
      S.kal.armR = -160; S.kal.fingerR = true; S.kal.look = [-6, 0];
      S.ui.profile = { t0: byId.s04.start + 0.03, followAt: cue('s05', 'ding') };
      S.ghost = { t0: cue('s05', 'pop'), arrow: false };
      S.ui.plusOne = cue('s05', 'pop'); S.ui.plusOneTop = 860;
    },
    s06(S, t, s, lt, d) {
      S.cam = camLerp([850, 1170, 2.0], [850, 1175, 2.12], lt / d);
      S.ghost = { t0: s.start - 1, arrow: true };
      S.ui.chip = { t0: cue('s06', 'pop'), text: '⬇️ DEIN PLATZ', cls: 'green' };
    },
    s07(S, t, s, lt, d) {
      S.cam = camLerp([1250, 1150, 0.95], [1250, 1130, 1.05], E.out(lt / d));
      S.kal.armL = 72; S.kal.armR = -72; S.kal.expr = 'happy'; S.berta = B({});
      S.ui.banner = s.start + 0.04; S.sparkle = s.start + 0.05;
    },
    s08(S, t, s, lt, d) {
      S.cam = camLerp([1300, 1190, 0.82], [1300, 1190, 0.88], lt / d); S.berta = B({});
      S.ui.chip = { t0: cue('s08', 'pop'), text: '🏟️ STADION: KUHWEIDE', cls: '' };
    },
    s09(S, t, s, lt, d) {
      S.cam = camLerp([1150, 1330, 1.05], [1150, 1330, 1.12], lt / d);
      S.hills = { t0: cue('s09', 'hearts') };
      S.mole = { t0: s.start + 0.6 };
      S.kal.expr = 'o'; S.kal.look = [-4, 6];
      S.ui.chip = { t0: cue('s09', 'pop'), text: '🕳️ 14 × MAULWURFSHÜGEL', cls: 'red' };
    },
    s10(S, t, s, lt, d) {
      S.cam = camLerp([1850, 1170, 1.55], [1850, 1170, 1.65], lt / d);
      S.netTag = cues('s10', 'pop')[1];
      S.ui.chip = { t0: cue('s10', 'pop'), text: '🥅 1 × TOR', cls: '' };
    },
    s11(S, t, s, lt, d) { S.cam = camLerp([830, 1210, 2.1], [830, 1210, 2.25], lt / d); S.ui.chip = { t0: cue('s11', 'pop'), text: '🪑 TRIBÜNE: 1 BIERBANK', cls: '' }; },
    s12(S, t, s, lt, d) {
      S.cam = camLerp([960, 1200, 1.3], [960, 1200, 1.36], lt / d);
      S.kal.armL = 55; S.kal.armR = -55; S.kal.tilt = 8; S.kal.look = [Math.sin(t * 3) * 7, 0];
      S.ui.zirp = { t0: cue('s12', 'crickets'), x: 300, y: 1160 };
    },
    s13(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1150, 2.6], [1180, 1150, 2.75], lt / d);
      S.kal.expr = 'worried'; S.kal.tilt = -6; S.kal.look = [-5, -4]; S.kal.armL = 30;
      S.qmarks = s.start + 0.2;
      S.ui.chip = { t0: cue('s13', 'pop'), text: '📋 MEIN TEAM?', cls: '' };
    },
    s14(S, t, s, lt, d) {
      S.cam = camLerp([1700, 1150, 1.25], [1700, 1150, 1.32], lt / d);
      const p = E.out(prog(t, s.start, 0.6));
      const m = cue('s14', 'moo');
      S.berta = B({ x: lerp(2500, 1850, p), hop: p < 1, moo: t > m && t < m + 0.9, chew: false });
      S.kal.look = [8, -2]; S.kal.expr = t > m ? 'happy' : 'smile';
      S.ui.chip = { t0: cue('s14', 'pop'), text: '🧤 TORWART', cls: 'yellow' };
    },
    s15(S, t, s, lt, d) {
      S.cam = camLerp([1730, 1150, 2.35], [1730, 1150, 2.5], lt / d);
      S.berta = B({ grass: t > cue('s15', 'crunch') - 0.1 });
      S.bucket = { t0: s.start + 0.15 };
      S.ui.chip = { t0: cue('s15', 'pop'), text: '💰 GEHALT: 1 EIMER GRAS', cls: 'yellow' };
    },
    s16(S, t, s, lt, d) {
      S.cam = camLerp([1500, 1180, 0.92], [1500, 1180, 0.96], lt / d);
      S.berta = B({ grass: true });
      const k = cue('s16', 'kick_ball'), b = cue('s16', 'boing');
      if (t < k) S.ball = { x: 1290, y: 1336, r: 0 };
      else if (t < b) { const p = prog(t, k, b - k); S.ball = { x: lerp(1290, 1690, p), y: lerp(1336, 1100, p) - Math.sin(p * Math.PI) * 120, r: p * 720 }; }
      else { const p = E.out(prog(t, b, 0.8)); S.ball = { x: lerp(1690, 1480, p), y: lerp(1100, 1336, p) - Math.sin(p * Math.PI) * 90, r: 720 - p * 400 }; }
      S.kal.armL = t > k ? 40 : 9; S.kal.armR = t > k ? -120 : -9; S.kal.expr = t > b ? 'o' : 'smile';
      S.ui.chip = { t0: cue('s16', 'pop'), text: '🧤 PARADE (ZUFALL)', cls: 'green' };
    },
    s17(S, t, s, lt, d) { S.cam = camLerp([830, 1200, 1.8], [830, 1200, 1.9], lt / d); S.ui.chip = { t0: cue('s17', 'pop'), text: '🏟️ PLÄTZE: 1 BANK', cls: '' }; },
    s18(S, t, s, lt, d) {
      S.layer = 'alt';
      const p = E.inOut(prog(t, s.start, 0.7));
      const ch = cue('s18', 'cheer');
      const fill = E.out(prog(t, ch - 0.2, 1.3));
      S.stad = { z: lerp(2.4, 1, p), f: [540, lerp(1150, 1130, p)], fill };
      S.ui.chip = { t0: s.start - 5, text: `🏟️ FANS: ${fmt(80000 * fill)}`, cls: fill > 0 ? 'green' : '' };
    },
    s19(S, t, s, lt, d) {
      S.cam = camLerp([1260, 1140, 1.0], [1260, 1140, 1.06], lt / d); S.berta = B({});
      S.kal.armR = -165; S.kal.armL = 30; S.kal.look = [0, -6];
      S.ui.chip = { t0: cue('s19', 'pop'), text: '📅 SA · 15:30 · ANPFIFF', cls: '' };
    },
    s20(S, t, s, lt, d) { S.cam = camLerp([830, 1190, 2.0], [830, 1190, 2.1], lt / d); S.ui.chip = { t0: cue('s20', 'pop'), text: '👀 FANS: ?', cls: '' }; },
    s21(S, t, s, lt, d) {
      S.cam = camLerp([830, 1190, 2.1], [830, 1190, 2.2], lt / d);
      S.pigeon = { t0: s.start + 0.05, coo: cue('s21', 'coo') };
      S.ui.chip = { t0: cue('s21', 'pop'), text: '🐦 1 × TAUBE', cls: 'red' };
    },
    s22(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1010, 2.35], [1180, 1010, 2.45], lt / d);
      S.kal.armR = -158; S.kal.fingerR = true; S.kal.look = [3, -7];
      S.ui.profile = { t0: s.start + 0.02, followAt: cue('s22', 'tap'), hand: true };
    },
    s23(S, t, s, lt, d) {
      S.cam = camLerp([1400, 1170, 0.98], [1400, 1170, 1.04], lt / d);
      S.berta = B({ x: 1640, y: 1340, hop: true, chew: false });
      S.kal.armL = 150 + Math.sin(t * 9) * 8; S.kal.armR = -150; S.kal.expr = 'happy'; S.kal.bounce = true;
      S.ui.comment = cue('s23', 'blip');
    },
    s24(S, t, s, lt, d) {
      S.cam = camLerp([1400, 1170, 1.04], [1400, 1170, 1.08], lt / d);
      S.berta = B({ x: 1640, y: 1340 });
      S.dim = clamp(lt / 0.2) * 0.85;
      const st = cue('s24', 'stamp');
      S.ui.ticket = { t0: cue('s24', 'pop'), stamp: st };
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s25(S, t, s, lt, d) {
      S.cam = camLerp([1400, 1170, 1.08], [1400, 1170, 1.12], lt / d);
      S.berta = B({ x: 1640, y: 1340 }); S.dim = 0.85;
      S.ui.ticket = { t0: s.start - 5, stamp: s.start - 5 };
      const n = cues('s25', 'tick').filter((x) => t >= x).length;
      S.ui.chip2 = { t0: cue('s25', 'tick'), text: `⏰ NUR HEUTE · 23:59:${String(59 - n).padStart(2, '0')}`, cls: 'red', top: 860 };
    },
    s26(S, t, s, lt, d) {
      S.cam = camLerp([1350, 1160, 1.0], [1350, 1160, 1.08], lt / d);
      S.berta = B({ x: 1640, y: 1340 }); S.kal.armL = 70; S.kal.armR = -70;
      S.ui.chip = { t0: cue('s26', 'pop'), text: '🗳️ AB JETZT BESTIMMT IHR', cls: 'green' };
      const b = cues('s26', 'blip'); S.floatBubbles = [b[0], b[1], b[2], b[2] + 0.2];
    },
    s27(S, t, s, lt, d) {
      S.cam = camLerp([880, 1180, 2.3], [880, 1180, 2.42], lt / d);
      S.box = { open: 0 }; S.berta = B({ x: 1090, y: 1340, look: true });
      S.ui.kasse = { t0: cue('s27', 'pop'), value: 0 };
    },
    s28(S, t, s, lt, d) {
      S.cam = camLerp([880, 1180, 2.42], [880, 1175, 2.55], lt / d);
      const k = cue('s28', 'kaching'), c = cue('s28', 'crunch');
      S.box = { open: E.back(prog(t, k, 0.3)), coinsAt: k };
      S.berta = B({ x: 1090, y: 1340, bill: t > c, chew: t > c });
      S.ui.kasse = { t0: byId.s27.start - 5, value: 500 * E.out(prog(t, k, 0.55)) - (t > c ? 50 * prog(t, c, 0.3) : 0) };
    },
    s29(S, t, s, lt, d) { cardsShot(S, t); S.kal.armR = -160; S.kal.fingerR = true; S.kal.look = [0, -7]; },
    s30(S, t, s, lt, d) { cardsShot(S, t); S.net = true; },
    s31(S, t, s, lt, d) { cardsShot(S, t); S.kal.armL = 60; S.kal.armR = -60; S.kal.tilt = 8; const m = cue('s31', 'moo'); S.berta.moo = t > m && t < m + 0.9; },
    s32(S, t, s, lt, d) {
      cardsShot(S, t);
      S.kal.armR = -150 + Math.sin(t * 12) * 16; S.kal.expr = t > s.speechEnd ? 'happy' : 'smile';
      S.berta.hop = t > s.speechEnd;
      S.ui.vote = cue('s32', 'pop');
      const p = E.out(prog(t, s.start + 0.2, 2.6));
      S.ui.likes = [344 * p, 467 * p, 129 * p];
      S.hearts = cues('s32', 'hearts');
    },
  };
  // Titelbild (nicht Teil des Videos): Kalle groß im Vordergrund, Berta im Tor
  shots.cover = (S, t) => {
    S.cam = [1450, 1180, 1.0];
    S.kal = Object.assign(S.kal, { x: 1150, y: 1560, s: 1.75, armL: 155, armR: -100, fingerR: true, expr: 'happy', look: [6, -2], talk: false });
    S.ball = { x: 1330, y: 1545, r: 20 };
    S.berta = B({ grass: true, chew: false });
  };

  function cardsShot(S, t) {
    const a = byId.s29.start;
    S.cam = camLerp([1420, 1100, 0.95], [1420, 1090, 1.04], clamp((t - a) / (TL.duration - a)));
    S.berta = B({ x: 1850, y: 1302 });
    S.ui.cards = [cue('s29', 'card'), cue('s30', 'card'), cue('s31', 'card')];
  }

  // ---------------------------------------------------------------- Zeichnen
  const K1 = humanEls('k1', 56), K2 = humanEls('k2', 56);
  const bq = (s) => document.getElementById(`b1-${s}`);
  function poseBerta(P, t) {
    setT(bq('bob'), `translate(0,${Math.sin(t * 3) * 2 + (P.hop ? -Math.abs(Math.sin(t * 7)) * 18 : 0)})`);
    setT(bq('tail'), `translate(148,-196) rotate(${Math.sin(t * 4) * 12})`);
    setT(bq('head'), `rotate(${Math.sin(t * 1.7) * 2 + (P.moo ? -8 : 0)} -150 -150)`);
    setT(bq('muzzle'), `translate(${P.chew ? Math.sin(t * 9) * 4 : 0},0)`);
    disp(bq('moo'), P.moo); disp(bq('mouth'), !P.moo);
    disp(bq('grass'), P.grass); disp(bq('bill'), P.bill);
  }

  function drawWorld(S, t) {
    for (let i = 0; i < 5; i++) {
      const c = $(`cloud${i}`);
      setT(c, `translate(${+c.dataset.x + t * 12 * c.dataset.s},${+c.dataset.y}) scale(${c.dataset.s})`);
    }
    // Maulwurfshügel
    HILLS.forEach(([x, y], i) => {
      const el = $(`hill${i}`);
      const sc = S.hills === 1 ? 1 : popS(t, S.hills.t0 + i * 0.06, 0.25);
      setT(el, `translate(${x},${y}) scale(${sc})`);
    });
    const mole = $('mole');
    if (S.mole && t >= S.mole.t0) { disp(mole, true); setT(mole, `translate(1050,${1430 - 14 * popS(t, S.mole.t0)})`); } else disp(mole, false);
    // Geist (+1 Fan)
    const g = $('ghost');
    if (S.ghost && t >= S.ghost.t0) {
      disp(g, true);
      setT($('ghostBody'), `scale(${popS(t, S.ghost.t0, 0.35)})`);
      $('ghostArm').setAttribute('d', `M26 -70 L${52 + Math.sin(t * 12) * 8} -110`);
      disp($('ghostArrow'), S.ghost.arrow); setT($('ghostArrow'), `translate(0,${Math.sin(t * 7) * 10})`);
    } else disp(g, false);
    // Taube
    const pg = $('pigeon');
    if (S.pigeon && t >= S.pigeon.t0) {
      disp(pg, true);
      const p = E.out(prog(t, S.pigeon.t0, 0.35));
      setT(pg, `translate(${lerp(1060, 900, p)},${lerp(1120, 1262, p)})`);
      const coo = t > S.pigeon.coo && t < S.pigeon.coo + 0.7;
      setT($('pgHead'), `translate(${coo ? Math.sin(t * 30) * 3 : 0},${coo ? -4 : 0})`);
    } else disp(pg, false);
    // Kasse
    const bx = $('cashbox');
    if (S.box) {
      disp(bx, true);
      setT($('boxLid'), `translate(0,-56) rotate(${-70 * clamp(S.box.open, 0, 1.2)} -74 0)`);
      let coins = '';
      if (S.box.coinsAt && t >= S.box.coinsAt) {
        const lt = t - S.box.coinsAt, cr = rng(17);
        for (let i = 0; i < 14; i++) {
          const a = -Math.PI / 2 + (cr() - 0.5) * 1.8, v = 160 + cr() * 220;
          const tt = Math.min(lt, 0.9);
          const x = Math.cos(a) * v * tt, y = -56 + Math.sin(a) * v * tt + 420 * tt * tt;
          coins += `<ellipse cx="${lt > 0.9 ? x * 0.3 : x}" cy="${lt > 0.9 ? -60 - cr() * 12 : Math.min(y, -58)}" rx="11" ry="9" fill="#F7CF4B" stroke="${OUT}" stroke-width="3"/>`;
        }
      }
      $('boxCoins').innerHTML = coins;
    } else disp(bx, false);
    // Tor
    disp($('goalNet'), S.net);
    const nt = $('netTag');
    if (S.netTag && t >= S.netTag) { disp(nt, true); setT(nt, `translate(1840,1088) scale(${popS(t, S.netTag)}) rotate(${Math.sin(t * 3) * 3})`); } else disp(nt, false);
    const bu = $('bucket');
    if (S.bucket && t >= S.bucket.t0) { disp(bu, true); setT(bu, `translate(1600,1340) scale(${popS(t, S.bucket.t0)})`); } else disp(bu, false);
    // Fragezeichen
    const qm = $('qmarks');
    if (S.qmarks && t >= S.qmarks) {
      disp(qm, true);
      setT($('q1'), `translate(1090,${1000 + Math.sin(t * 5) * 6}) rotate(-14) scale(${popS(t, S.qmarks)})`);
      setT($('q2'), `translate(1250,${975 + Math.sin(t * 5 + 1) * 6}) rotate(12) scale(${popS(t, S.qmarks + 0.2)})`);
    } else disp(qm, false);
    // Ball
    setT($('ball'), `translate(${S.ball.x},${S.ball.y}) rotate(${S.ball.r})`);
    // Kalle
    const k = S.kal;
    setT($('kalleW'), `translate(${k.x},${k.y}) scale(${k.s})`);
    poseHuman(K1, k, t);
    // Berta
    const bw = $('bertaW');
    if (S.berta) { disp(bw, true); setT(bw, `translate(${S.berta.x},${S.berta.y}) scale(${S.berta.s})`); poseBerta(S.berta, t); }
    else disp(bw, false);
  }

  function drawAlt(S, t) {
    const P = S.stad;
    setT($('stadCam'), `translate(540,960) scale(${P.z}) translate(${-P.f[0]},${-P.f[1]})`);
    const n = Math.floor(CROWD.length * P.fill);
    const d = ['', '', '', ''];
    for (let i = 0; i < n; i++) {
      const c = CROWD[i];
      const jy = Math.abs(Math.sin(t * 9 + i)) * 4;
      d[c.c] += `M${c.x.toFixed(1)} ${(c.y - jy).toFixed(1)}h9v9h-9z`;
    }
    for (let i = 0; i < 4; i++) $(`cr${i}`).setAttribute('d', d[i]);
    poseHuman(K2, Object.assign(humanDefaults(), { armL: 155 + Math.sin(t * 9) * 8, armR: -155, expr: 'happy', bounce: true }), t);
    for (const st of document.querySelectorAll('.star')) st.setAttribute('opacity', 0.35 + 0.65 * Math.abs(Math.sin(t * 1.5 + +st.dataset.p)));
  }

  // Figuren-Grafik für Profilbild & Co. (engine/render_avatar.cjs)
  window.ART = { kalleMarkup, bertaMarkup, ballMarkup, OUT };

  Engine.start({
    world, alt, shots, drawWorld, drawAlt,
    baseState: base,
    highlight: '#FFD43B',
    confettiColors: ['#E23A4E', '#fff', '#FFC83A', '#2DBE60', '#5CC8FF', '#fff'],
    preload: '📣⚽🏟️🕳️🥅🪑📋🧤💰📅👀🐦⏰🗳️💡😂🐄',
    ui: {
      profile: { name: 'FC Kuhweide', handle: '@fc.kuhweide', avatar: '⚽', stat: 'Fans', foot: '1 Follower = 1 Fan ⚽' },
      comment: 'Ich bin Fan Nr. 1! ⚽❤️',
      banner: { small: 'WILLKOMMEN BEIM', big: 'FC KUHWEIDE' },
      stamp: { emo: '⚽', text: 'GEGRÜNDET!' },
      plusOne: '+1 FAN ⚽',
      zirp: 'zirp …',
      ticket: `<div class="main"><div class="kicker">DAUERKARTE · SAISON 1</div><div class="title">FC KUHWEIDE</div>
        <div class="grid"><div><small>BLOCK</small><b>A (Bierbank)</b></div><div><small>PLATZ</small><b>1</b></div>
        <div><small>NAME</small><b>DU</b></div><div><small>GÜLTIG</small><b>für immer</b></div></div>
        <div class="note">nur für Kommentierer · Tag 1</div></div>
        <div class="stub"><div class="emo">⚽</div><small>NR.</small><div class="big">001</div></div>`,
      tstamp: '✓ FAN<br>NR. 1',
      kasse: 'VEREINSKASSE',
      cards: [
        { color: '#FFC83A', icon: lightIcon, label: 'FLUTLICHT' },
        { color: '#5CC8FF', icon: netIcon, label: 'NETZ<br>FÜRS TOR' },
        { color: '#FF8A94', icon: qIcon, label: 'WAS<br>ANDERES' },
      ],
      floats: ['Flutlicht!! 💡', 'Tag 2?! 👀', 'Berta 😂🐄', 'Ich bin Fan! ⚽'],
    },
  });
})();

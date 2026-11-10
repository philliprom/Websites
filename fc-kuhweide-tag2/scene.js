/* FC Kuhweide – Tag 2: Der Kader. Welt und Figuren wie Tag 1, Daten aus kader.json (window.KADER). */
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

  // ---------------------------------------------------------------- Tag 2: Spieler, Ultra
  const legMarkup = (id, x) => `<g id="${id}" transform="translate(${x},-64)">
      <rect x="-9" y="0" width="18" height="50" rx="8" fill="#F1C6A0" ${sw}/>
      <rect x="-10" y="20" width="20" height="28" rx="6" fill="#E23A4E" ${sw}/>
      <path d="M-12 46 L16 46 Q22 46 22 54 L22 62 L-12 62 Z" fill="${OUT}"/></g>`;
  const playerMarkup = () => `
    <ellipse cx="0" cy="3" rx="50" ry="9" fill="#1E3A1A" opacity=".22"/>
    <g id="plBob">
      ${legMarkup('plLegL', -12)}${legMarkup('plLegR', 12)}
      <path d="M-30 -70 L30 -70 L28 -44 L-28 -44 Z" fill="#fff" ${sw}/>
      <path d="M-30 -132 L-54 -88 M30 -132 L54 -88" stroke="#F1C6A0" stroke-width="14" stroke-linecap="round"/>
      <rect x="-34" y="-146" width="68" height="82" rx="22" fill="#E23A4E" ${sw}/>
      <path d="M-34 -120 L34 -120" stroke="#fff" stroke-width="6"/>
      <text x="0" y="-80" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#fff" stroke="${OUT}" stroke-width="3" paint-order="stroke">${window.KADER.neuner.num}</text>
      <circle cx="0" cy="-184" r="40" fill="#F1C6A0" ${sw}/>
      <path d="M-41 -190 Q-38 -230 0 -228 Q38 -230 41 -190 Q20 -206 0 -201 Q-20 -206 -41 -190 Z" fill="#3A2A1E" ${sw}/>
      <circle cx="-14" cy="-184" r="6.5" fill="${OUT}"/><circle cx="14" cy="-184" r="6.5" fill="${OUT}"/>
      <path id="plMouth" d="M-12 -166 Q0 -156 12 -166" stroke="${OUT}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path id="plSad" d="M-12 -160 Q0 -170 12 -160" stroke="${OUT}" stroke-width="4" fill="none" stroke-linecap="round" style="display:none"/>
    </g>`;
  const ultraMini = (id, scarf) => `<g id="${id}"><g class="umb">
      <path d="M-14 -60 L-30 -104" stroke="#E0A57E" stroke-width="11" stroke-linecap="round"/>
      <rect x="-22" y="-70" width="44" height="70" rx="17" fill="#1F2A44" ${sw}/>
      <path d="M-20 -62 L22 -40" stroke="${scarf}" stroke-width="11"/><path d="M-20 -62 L22 -40" stroke="#fff" stroke-width="11" stroke-dasharray="8 8"/>
      <circle cx="0" cy="-92" r="22" fill="#F1C6A0" ${sw}/>
      <path d="M-22 -97 Q0 -126 22 -97 Z" fill="${scarf}" ${sw}/>
      <circle cx="-7" cy="-92" r="3" fill="${OUT}"/><circle cx="7" cy="-92" r="3" fill="${OUT}"/>
      <ellipse cx="0" cy="-80" rx="7" ry="5" fill="#7A2633" ${sw}/>
      <circle cx="-32" cy="-108" r="9" fill="#E0A57E" ${sw}/></g></g>`;
  const ultraMarkup = () => `
    <g id="drum" transform="translate(78,0)">
      <rect x="-36" y="-62" width="72" height="62" rx="10" fill="#E23A4E" ${sw}/>
      <path d="M-36 -44 L36 -18 M-36 -18 L36 -44" stroke="#FFC83A" stroke-width="5"/>
      <ellipse id="drumSkin" cx="0" cy="-62" rx="36" ry="11" fill="#F4F4F4" ${sw}/></g>
    <g id="ultraBody">
      <rect x="-26" y="-80" width="52" height="80" rx="20" fill="#1F2A44" ${sw}/>
      <path d="M-24 -70 L26 -44" stroke="#E23A4E" stroke-width="13"/>
      <path d="M-24 -70 L26 -44" stroke="#fff" stroke-width="13" stroke-dasharray="9 9"/>
      <path d="M-20 -62 L-40 -24" stroke="#E0A57E" stroke-width="12" stroke-linecap="round"/>
      <circle cx="0" cy="-104" r="26" fill="#E0A57E" ${sw}/>
      <path d="M-26 -110 Q0 -142 26 -110 Z" fill="#E23A4E" ${sw}/>
      <circle cx="0" cy="-140" r="7" fill="#fff" ${sw}/>
      <circle cx="-9" cy="-104" r="3.5" fill="${OUT}"/><circle cx="9" cy="-104" r="3.5" fill="${OUT}"/>
      <ellipse cx="0" cy="-90" rx="8" ry="6" fill="#7A2633" ${sw}/>
      <g id="mega" transform="translate(20,-112) rotate(-28)">
        <path d="M18 -1 L-2 -40" stroke="#E0A57E" stroke-width="12" stroke-linecap="round" transform="translate(-22,40)"/>
        <path d="M0 -9 L52 -28 L52 28 L0 9 Z" fill="#D5DCE6" ${sw}/>
        <rect x="-16" y="-9" width="18" height="18" rx="4" fill="#8E99AA" ${sw}/>
        <path d="M62 -26 l16 -8 M64 0 l18 0 M62 26 l16 8" stroke="#fff" stroke-width="5" stroke-linecap="round"/></g>
    </g>`;

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
    <g id="crowdBack"></g>
    <g id="bench"><rect x="640" y="1262" width="390" height="22" rx="6" fill="#C08A52" ${sw}/>
      <path d="M670 1284 L660 1330 M700 1284 L710 1330 M970 1284 L960 1330 M1000 1284 L1010 1330" stroke="#8C5A30" stroke-width="10" stroke-linecap="round"/></g>
    <g id="crowdFront"></g>
    <g id="ultra2" style="display:none">${ultraMini('u2', '#E23A4E')}</g>
    <g id="ultra3" style="display:none">${ultraMini('u3', '#2F80D1')}</g>
    <g id="ultra" style="display:none">${ultraMarkup()}</g>
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
    <g id="shooter" style="display:none">${playerMarkup()}</g>
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
  // ---------------------------------------------------------------- Zustand + Schnitte (Tag 2: Der Kader)
  const KD = window.KADER;
  const base = () => ({
    kal: Object.assign(humanDefaults(), { x: 1180, y: 1350, s: 1 }),
    berta: null, ball: { x: 1290, y: 1336, r: 0 }, hills: 1, mole: null, ghost: null, pigeon: null, bucket: null, box: null,
    net: null, netTag: null, qmarks: null, crowd: null, board: null,
  });
  const B = (o) => Object.assign({ x: 1850, y: 1302, s: 1, chew: true, moo: false, grass: false, bill: false, hop: false }, o);
  const keyOf = (pred) => KD.aufstellung.findIndex(pred);
  const PINS = () => cue('s07', 'pins');

  const CC = { netz: 0, ultra: 1, tor: 2, burst: 3, ultraMehr: 3 + window.KADER.kommentare.burst.length };
  const BURST = [[70, 235, -4], [190, 385, 3], [80, 535, -2], [180, 685, 4], [70, 835, -3], [180, 985, 2], [90, 1135, -2]];
  function ballFlight(t, k) {
    const h = Math.max(cue('s11', 'boing'), k + 0.25);
    if (t < k) return { x: 1520, y: 1345, r: 0 };
    if (t < h) { const p = prog(t, k, h - k); return { x: lerp(1520, 1690, p), y: lerp(1345, 1095, p) - Math.sin(p * Math.PI) * 90, r: p * 540 }; }
    const p = E.out(prog(t, h, 0.9));
    return { x: lerp(1690, 1430, p), y: lerp(1095, 1342, p) - Math.sin(p * Math.PI) * 160, r: 540 - p * 300 };
  }

  const shots = {
    s01(S, t, s, lt, d) {
      S.cam = camLerp([830, 1170, 1.85], [830, 1170, 1.95], lt / d);
      S.pigeon = { mode: 'bench' };
      S.ui.counter = { t0: s.start - 0.1, label: 'GESTERN', unit: 'FANS', value: 0, cls: 'zero', top: 300 };
    },
    s02(S, t, s, lt, d) {
      S.cam = camLerp([850, 1175, 1.85], [850, 1175, 1.7], E.out(clamp(lt / d)));
      S.crowd = { t0: s.start };
      S.pigeon = { mode: 'fly', flyAt: cue('s02', 'flap') };
      S.ui.counter = { t0: s.start, label: 'HEUTE', unit: 'FANS', value: KD.fans * E.out(prog(t, s.start, 0.7)), cls: 'today', top: 300 };
      S.confetti = cue('s02', 'confetti');
    },
    s03(S, t, s, lt, d) {
      S.cam = [1100, 1170, 1.0]; S.crowd = { t0: -10 }; S.berta = B({}); S.dim = 0.55;
      const b = cues('s03', 'blip');
      S.ui.ccards = BURST.map(([x, y, rot], i) => ({ i: CC.burst + i, t0: b[i] ?? b[b.length - 1], x, y, rot, s: 0.88 }));
    },
    s04(S, t, s, lt, d) {
      S.cam = camLerp([1850, 1160, 1.45], [1850, 1160, 1.52], lt / d);
      S.berta = B({}); S.pigeon = { mode: 'bar' };
      S.ui.ccards = [{ i: CC.netz, t0: cue('s04', 'blip'), x: 130, y: 290, rot: -3 }];
    },
    s05(S, t, s, lt, d) {
      S.cam = camLerp([1850, 1160, 1.52], [1850, 1160, 1.6], lt / d);
      S.berta = B({ hop: true, chew: false }); S.pigeon = { mode: 'bar' }; S.net = s.start;
      const k = cue('s05', 'kaching');
      S.ui.kasse = { t0: s.start, value: lerp(KD.kasse_start, KD.kasse_rest, E.out(prog(t, k, 0.5))) };
    },
    s06(S, t, s, lt, d) {
      S.cam = camLerp([860, 1180, 1.6], [860, 1180, 1.68], lt / d); S.crowd = { t0: -10 };
      const ub = cues('s06', 'blip');
      S.ui.ccards = [{ i: CC.ultra, t0: ub[0], x: 130, y: 290, rot: 2 },
        { i: CC.ultraMehr, t0: ub[1] ?? ub[0], x: 200, y: 440, rot: -3 }, { i: CC.ultraMehr + 1, t0: ub[2] ?? ub[0], x: 110, y: 590, rot: 2 }];
    },
    s07(S, t, s, lt, d) {
      S.cam = camLerp([930, 1150, 1.9], [930, 1150, 2.0], lt / d); S.crowd = { t0: -10 }; S.kal.x = 1400;
      S.ultra = { t0: s.start, drums: cues('s07', 'drum') };
      S.ui.chip = { t0: s.start + 0.05, text: KD.ultra.chip || `📣 ULTRA-BLOCK · ${KD.ultra.handle}`, cls: 'red' };
    },
    s08(S, t, s, lt, d) {
      S.cam = camLerp([1800, 1140, 1.6], [1800, 1140, 1.68], lt / d);
      S.berta = B({}); S.net = true; S.pigeon = { mode: 'bar' };
      S.ui.ccards = [{ i: CC.tor, t0: cue('s08', 'blip'), x: 130, y: 290, rot: -2 }];
    },
    s09(S, t, s, lt, d) {
      S.cam = camLerp([1780, 1120, 2.2], [1780, 1120, 2.35], lt / d);
      const m = cue('s09', 'moo');
      S.berta = B({ hop: t < m, moo: t > m && t < m + 0.9, chew: false }); S.net = true;
      S.ui.chip2 = { t0: m, text: '🐄 MUUH! (heißt: NEIN)', cls: 'red', top: 300 };
    },
    s10(S, t, s, lt, d) {
      S.cam = camLerp([1600, 1170, 1.05], [1640, 1170, 1.12], lt / d);
      S.berta = B({}); S.net = true; S.pigeon = { mode: 'bar' };
      const k = cue('s10', 'kick_ball');
      S.shooter = { x: lerp(1330, 1470, E.inOut(prog(t, s.start + 0.4, Math.max(0.3, k - s.start - 0.4)))), kickAt: k };
      S.ball = ballFlight(t, k);
      S.ui.chip = { t0: cue('s10', 'whistle'), text: '⚽ ELFMETER-TEST', cls: 'yellow' };
      S.ui.chip2 = { t0: s.start + 0.6, text: `🎽 NR. ${KD.neuner.num} · ${KD.neuner.handle}`, cls: '', top: 390 };
    },
    s11(S, t, s, lt, d) {
      S.cam = camLerp([1680, 1150, 1.5], [1680, 1150, 1.62], lt / d);
      const k = cue('s10', 'kick_ball'), h = cue('s11', 'boing');
      S.berta = B({}); S.net = true; S.pigeon = { mode: 'bar' };
      S.shooter = { x: 1470, kickAt: k, sad: t > h };
      S.ball = ballFlight(t, k);
      S.ui.big = { t0: h, text: 'GEHALTEN!', cls: 'mid', rot: -6 };
      S.shake = t >= h ? Math.max(0, 1 - (t - h) / 0.25) : 0;
    },
    s12(S, t, s, lt, d) { boardShot(S, t); S.board = { seq: cue('s12', 'pins') }; },
    s13(S, t, s, lt, d) {
      boardShot(S, t);
      const p = cues('s13', 'pop'), bo = cue('s13', 'boing');
      const glow = [];
      if (t >= p[0]) glow.push('pos:' + keyOf((x) => x.duo));
      if (t >= p[1]) KD.staff.forEach((x, i) => { if (/Co-Trainer/.test(x.rolle)) glow.push('st:' + i); });
      if (t >= bo) glow.push('pos:' + keyOf((x) => x.pos === 'RV'));
      S.board = { seq: cue('s12', 'pins'), glow, vs: bo };
    },
    s14(S, t, s, lt, d) {
      S.cam = [1000, 1180, 1.2]; S.crowd = { t0: -10 }; S.berta = B({}); S.net = true;
      S.dim = clamp(lt / 0.2) * 0.85;
      const st = cue('s14', 'stamp');
      S.ui.ticket = { t0: cue('s14', 'pop'), stamp: st };
      S.confetti = cue('s14', 'confetti');
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s15(S, t, s, lt, d) {
      S.cam = camLerp([1560, 1150, 1.0], [1560, 1145, 1.05], lt / d);
      S.berta = B({ hop: true, chew: false }); S.net = true; S.pigeon = { mode: 'bar' };
      const c = cues('s15', 'card');
      S.ui.cards = [c[0], c[1], null];
      S.kal.look = [6, -2]; S.kal.armR = -100; S.kal.fingerR = true;
    },
    s16(S, t, s, lt, d) {
      S.cam = camLerp([1560, 1145, 1.05], [1560, 1140, 1.08], lt / d);
      S.berta = B({ hop: true, chew: false }); S.net = true; S.pigeon = { mode: 'bar' };
      const c = cues('s15', 'card');
      S.ui.cards = [c[0], c[1], null];
      S.ui.vote = cue('s16', 'pop');
      S.ui.chip = { t0: cue('s16', 'pop') + 0.3, text: '🏷️ MARKIER DEINEN KUMPEL!', cls: 'green', top: 1180 };
      const h = cue('s16', 'hearts'); S.hearts = [h, h + 0.5];
      S.kal.expr = 'happy'; S.kal.armR = -150 + Math.sin(t * 12) * 16;
    },
    s17(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1060, 2.3], [1180, 1060, 2.45], lt / d);
      S.kal.expr = t > cue('s17', 'pop') ? 'happy' : 'smile'; S.kal.look = [0, -8]; S.kal.armR = -150; S.kal.fingerR = true;
      S.post = { t0: cue('s17', 'pop') };
      S.dim = clamp((t - cue('s17', 'pop')) / 0.25) * 0.35;
    },
  };
  function boardShot(S, t) { S.cam = [1250, 1150, 1.04]; S.berta = B({}); S.crowd = { t0: -10 }; S.dim = 0.55; S.net = true; }

  // Titelbild: Taktiktafel mit Kalle
  shots.cover = (S, t) => { boardShot(S, t); S.dim = 0.45; S.board = { blur: true, zoom: 0.78, ty: 285 }; };

  // ---------------------------------------------------------------- Fan-Menge
  const SLOTS = (() => {
    const r = rng(31), out = [];
    const shirts = ['#E23A4E', '#FFFFFF', '#E23A4E', '#FFC83A', '#2F80D1', '#2DBE60', '#E23A4E', '#FFFFFF'];
    const skins = ['#F1C6A0', '#E0A57E', '#C68858', '#8D5A3B', '#F6D3B8'];
    const rows = [
      { y: 1262, x0: 660, x1: 1000, n: 12, back: false },  // sitzen auf der Bank
      { y: 1336, x0: 600, x1: 1080, n: 14, back: false },  // stehen davor
      { y: 1236, x0: 630, x1: 1040, n: 13, back: true },   // stehen dahinter
      { y: 1196, x0: 650, x1: 1010, n: 10, back: true },   // auf Schultern
      { y: 1300, x0: 520, x1: 600, n: 3, back: false },
    ];
    for (const row of rows) for (let i = 0; i < row.n; i++) {
      out.push({ x: row.x0 + (row.x1 - row.x0) * (i + 0.5) / row.n + (r() - 0.5) * 10, y: row.y + (r() - 0.5) * 6, back: row.back,
        c: shirts[Math.floor(r() * shirts.length)], skin: skins[Math.floor(r() * skins.length)], ph: r() * 6, sc: 0.95 + r() * 0.15 });
    }
    return out;
  })();
  const fanSvg = (f, t, s) => {
    const yy = f.y - Math.abs(Math.sin(t * 8 + f.ph)) * 6;
    const a = Math.sin(t * 9 + f.ph) * 5;
    return `<g transform="translate(${f.x.toFixed(1)},${yy.toFixed(1)}) scale(${(f.sc * s).toFixed(3)})">
      <path d="M-9 -38 L${-18 + a} -66 M9 -38 L${18 - a} -66" stroke="${f.skin}" stroke-width="8" stroke-linecap="round"/>
      <path d="M-9 -38 L${-18 + a} -66 M9 -38 L${18 - a} -66" stroke="${OUT}" stroke-width="2" stroke-linecap="round" opacity=".5"/>
      <rect x="-15" y="-46" width="30" height="46" rx="12" fill="${f.c}" stroke="${OUT}" stroke-width="3.5"/>
      <path d="M-13 -40 H13" stroke="${f.c === '#E23A4E' ? '#fff' : '#E23A4E'}" stroke-width="5"/>
      <circle cx="0" cy="-60" r="15" fill="${f.skin}" stroke="${OUT}" stroke-width="3.5"/>
      <circle cx="-5" cy="-62" r="2.2" fill="${OUT}"/><circle cx="5" cy="-62" r="2.2" fill="${OUT}"/>
      <path d="M-5 -55 Q0 -50 5 -55" stroke="${OUT}" stroke-width="2.2" fill="none"/></g>`;
  };
  function drawCrowd(S, t) {
    let back = '', front = '';
    if (S.crowd) {
      const n = Math.min(KD.fans, SLOTS.length);
      const order = SLOTS.map((f, i) => [f, i]).slice(0, n).sort((a, b) => a[0].y - b[0].y);
      for (const [f, i] of order) {
        const sc = popS(t, S.crowd.t0 + i * 0.02, 0.25);
        if (sc <= 0.01) continue;
        if (f.back) back += fanSvg(f, t, sc); else front += fanSvg(f, t, sc);
      }
    }
    $('crowdBack').innerHTML = back;
    $('crowdFront').innerHTML = front;
  }

  // ---------------------------------------------------------------- Taktiktafel
  let boardEls = null;
  function buildBoard() {
    const W = 902, H = 740;
    const pos = KD.aufstellung.map((p, i) => {
      const names = p.names.map((n) => `<div class="nm">${n}</div>`);
      let inner = names[0];
      if (names.length > 1) inner = names.join(`<div class="tagline${p.duo ? ' duo' : ''}" data-vs="${p.duel ? 1 : 0}">${p.duo ? 'DUO' : 'VS'}</div>`);
      const note = p.note ? `<div class="tagline${p.note === 'Joker' ? ' joker' : ''}">${p.note === 'Joker' ? '🃏 JOKER' : p.note}</div>` : '';
      return `<div class="pos" data-k="pos:${i}" style="left:${(p.x * W).toFixed(0)}px;top:${(p.y * H).toFixed(0)}px">
        <div class="jersey${p.pos === 'TW' ? ' gk' : ''}">${p.pos === 'TW' ? '🐄' : p.num}</div><div class="names">${inner}${note}</div></div>`;
    }).join('');
    const lines = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" fill="none" stroke="#fff" stroke-width="5" opacity=".85">
      <rect x="14" y="10" width="${W - 28}" height="${H - 20}" rx="6"/>
      <path d="M${W / 2 - 110} 10 A110 110 0 0 0 ${W / 2 + 110} 10"/>
      <rect x="${W * 0.22}" y="${H * 0.80}" width="${W * 0.56}" height="${H * 0.2 - 10}"/>
      <rect x="${W * 0.38}" y="${H * 0.92}" width="${W * 0.24}" height="${H * 0.08 - 10}"/>
      <path d="M${W * 0.40} ${H * 0.80} A80 80 0 0 1 ${W * 0.60} ${H * 0.80}"/></svg>`;
    const staff = KD.staff.map((s, i) => `<div class="st${s.wide ? ' wide' : ''}" data-k="st:${i}">${s.emo} ${s.rolle}<b>${s.handle}</b></div>`).join('');
    const el = document.createElement('div');
    el.id = 'board'; el.className = 'ui';
    el.innerHTML = `<div class="head">📋 KADER · FC KUHWEIDE</div><div class="pitch">${lines}${pos}</div><div class="staff">${staff}</div>`;
    $('ui').appendChild(el);
    const lupe = document.createElement('div');
    lupe.id = 'lupe'; lupe.className = 'ui'; lupe.textContent = '🔍';
    $('ui').appendChild(lupe);
    boardEls = { el, lupe, items: [...el.querySelectorAll('[data-k]')], vs: [...el.querySelectorAll('[data-vs="1"]')] };
  }
  function drawBoard(S, t) {
    if (!boardEls) return;
    const { el, lupe, items, vs } = boardEls;
    const B_ = S.board;
    if (!B_) { el.style.display = 'none'; lupe.style.display = 'none'; return; }
    el.style.display = '';
    el.classList.toggle('blurred', !!B_.blur);
    el.style.transform = `translateY(${B_.ty || 0}px) scale(${B_.zoom || 1})`;
    const glow = new Set(B_.glow || []);
    items.forEach((it, i) => {
      const sc = B_.seq !== undefined ? popS(t, B_.seq + i * 0.08, 0.25) : 1;
      const isPos = it.classList.contains('pos');
      it.style.transform = `${isPos ? 'translate(-50%, -35px) ' : ''}scale(${Math.max(0.001, sc)})`;
      it.style.opacity = clamp(sc * 3);
      const g = glow.has(it.dataset.k);
      const target = isPos ? it.querySelector('.jersey') : it;
      target.classList.toggle('glow', g);
      if (isPos) it.querySelectorAll('.nm').forEach((n) => n.classList.toggle('glow', g));
    });
    vs.forEach((v) => {
      const k = B_.vs && t >= B_.vs ? 1 + 0.35 * Math.abs(Math.sin((t - B_.vs) * 9)) : 1;
      v.style.transform = `scale(${k})`;
      v.style.background = B_.vs && t >= B_.vs ? '#FF2D3D' : '';
    });
    if (B_.lupe !== undefined && t >= B_.lupe) {
      const p = prog(t, B_.lupe, 1.3);
      lupe.style.display = '';
      lupe.style.left = `${lerp(80, 640, p)}px`;
      lupe.style.top = `${560 + Math.sin(p * Math.PI * 2) * 180}px`;
      lupe.style.transform = `rotate(${-10 + Math.sin(t * 6) * 8}deg)`;
    } else lupe.style.display = 'none';
  }

  // ---------------------------------------------------------------- Briefumschlag (Cliffhanger)
  let postEl = null;
  function buildPost() {
    postEl = document.createElement('div');
    postEl.id = 'post'; postEl.className = 'ui';
    postEl.innerHTML = `<div class="env"><div class="flap"></div><div class="addr"><small>AN</small><b class="to">Den größten Kreisligaverein<br>der Welt</b><small>VON</small><b>FC KUHWEIDE</b></div>
      <div class="stampbox">🐄</div><div class="seal">!</div><div class="chall">HERAUSFORDERUNG</div></div>`;
    $('ui').appendChild(postEl);
  }
  function drawPost(S, t) {
    if (!postEl) return;
    if (!S.post || t < S.post.t0) { postEl.style.display = 'none'; return; }
    const k = popS(t, S.post.t0, 0.35);
    postEl.style.display = '';
    postEl.style.transform = `translateX(-50%) translateY(${(1 - E.out(prog(t, S.post.t0, 0.35))) * 400}px) rotate(${-6 + Math.sin(t * 8) * 2}deg) scale(${k})`;
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
    // Fan-Menge auf und um die Bierbank (Tag 2)
    drawCrowd(S, t);
    // Taube: sitzt auf der Bank, fliegt weg, landet auf der Latte
    const pg = $('pigeon');
    if (S.pigeon) {
      disp(pg, true);
      let x = 1030, y = 1262, rot = 0, sx = 1, sy = 1;
      if (S.pigeon.mode === 'bar') { x = 1995; y = 1066; }
      else if (S.pigeon.mode === 'fly' && t >= S.pigeon.flyAt) {
        const p = prog(t, S.pigeon.flyAt, 0.9);
        x = lerp(1030, 1360, p); y = lerp(1262, 960, E.out(p)); rot = 12; sx = -1; sy = 0.6 + 0.4 * Math.abs(Math.sin(t * 30));
      }
      setT(pg, `translate(${x},${y}) rotate(${rot}) scale(${sx},${sy})`);
      const coo = S.pigeon.coo && t > S.pigeon.coo && t < S.pigeon.coo + 0.7;
      setT($('pgHead'), `translate(${coo ? Math.sin(t * 30) * 3 : 0},${coo ? -4 : 0})`);
    } else disp(pg, false);
    // Netz (erscheint mit Plopp)
    const gn = $('goalNet');
    if (S.net) { disp(gn, true); gn.setAttribute('opacity', S.net === true ? 0.75 : 0.75 * clamp((t - S.net) * 4)); } else disp(gn, false);
    // Elfmeter-Schütze
    const sh_ = $('shooter');
    if (S.shooter) {
      disp(sh_, true);
      const k = S.shooter.kickAt;
      let legR = 0, legL = 0, lean = 0;
      if (t < k - 0.22) { legR = Math.sin(t * 18) * 28; legL = -legR; lean = 6; }
      else if (t < k) { legR = 50 * prog(t, k - 0.22, 0.2); lean = -4; }
      else { legR = lerp(-75, 0, prog(t, k, 0.45)); lean = 4; }
      setT($('plLegR'), `translate(12,-64) rotate(${legR})`);
      setT($('plLegL'), `translate(-12,-64) rotate(${legL})`);
      setT($('plBob'), `rotate(${lean} 0 -64) translate(0,${t < k - 0.22 ? -Math.abs(Math.sin(t * 18)) * 8 : 0})`);
      disp($('plMouth'), !S.shooter.sad); disp($('plSad'), !!S.shooter.sad);
      setT(sh_, `translate(${S.shooter.x},1352) scale(1.1)`);
    } else disp(sh_, false);
    // Ultra mit Megafon und Trommel
    const ul = $('ultra');
    if (S.ultra) {
      disp(ul, true);
      setT(ul, `translate(980,1262) scale(${1.55 * popS(t, S.ultra.t0, 0.3)})`);
      setT($('mega'), `translate(20,-112) rotate(${-28 + Math.sin(t * 10) * 6})`);
      const hit = (S.ultra.drums || []).some((x) => t > x && t < x + 0.12);
      setT($('drumSkin'), `translate(0,${hit ? 4 : 0}) scale(1,${hit ? 0.7 : 1})`);
      setT($('ultraBody'), `translate(0,${-Math.abs(Math.sin(t * 7)) * 8})`);
    } else disp(ul, false);
    [['ultra2', 870, 0.12], ['ultra3', 1175, 0.24]].forEach(([id, x, dl]) => {
      const el = $(id);
      if (S.ultra) {
        disp(el, true);
        setT(el, `translate(${x},1262) scale(${1.35 * popS(t, S.ultra.t0 + dl, 0.3)})`);
        el.querySelector('.umb').setAttribute('transform', `translate(0,${-Math.abs(Math.sin(t * 7 + dl * 9)) * 9})`);
      } else disp(el, false);
    });
    drawPost(S, t);
    drawBoard(S, t);
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

  window.ART = { kalleMarkup, bertaMarkup, ballMarkup, OUT };
  const emoIcon = (e) => `<div class="icon">${e}</div>`;
  const FLO = KD.torwart_herausforderer.name.toUpperCase();

  Engine.start({
    world, alt, shots, drawWorld, drawAlt,
    baseState: base,
    highlight: '#FFD43B',
    whip: true,
    confettiColors: ['#E23A4E', '#fff', '#FFC83A', '#2DBE60', '#5CC8FF', '#fff'],
    preload: '📣⚽🏟️🥅📋🧤💰👀🐦🗳️🐄🔍⭐🎟️🏷️🃏🇹🇷',
    ui: {
      day: 'TAG 2',
      profile: { name: 'FC Kuhweide', handle: '@fc.kuhweide', avatar: '⚽', avatarImg: '../fc-kuhweide-tag1/out/profilbild_kalle.png', stat: 'Fans', foot: '1 Follower = 1 Fan ⚽' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '⚽', text: 'KADER!' }, plusOne: '+1 FAN', zirp: '',
      ticket: `<div class="main"><div class="kicker">DAUERKARTE · SAISON 1</div><div class="title">FC KUHWEIDE</div>
        <div class="grid"><div><small>NAME</small><b>${KD.dauerkarte_001.handle}</b></div><div><small>PLATZ</small><b>1 (Bierbank)</b></div>
        <div><small>STATUS</small><b>Fan Nr. 1</b></div><div><small>GÜLTIG</small><b>für immer</b></div></div>
        <div class="note">eingelöst an Tag 2 · danke fürs Kommentieren!</div></div>
        <div class="stub"><div class="emo">🎟️</div><small>NR.</small><div class="big">001</div></div>`,
      tstamp: '✓ FAN<br>NR. 1',
      kasse: 'VEREINSKASSE',
      cards: [
        { color: '#FFC83A', icon: emoIcon('🐄'), label: 'BERTA<small>schreib „BERTA“</small>' },
        { color: '#5CC8FF', icon: emoIcon('🧤'), label: `${FLO}<small>schreib „${FLO}“</small>` },
        { color: '#FF8A94', icon: '', label: '' },
      ],
      floats: [],
      ccards: [KD.kommentare.netz, KD.kommentare.ultra, KD.kommentare.tor, ...KD.kommentare.burst, ...(KD.kommentare.ultra_mehr || [])],
    },
  });
  buildBoard();
  buildPost();
})();

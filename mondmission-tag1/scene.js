/* Omas Mondmission – Tag 1. Schrebergarten, Regentonnen-Rakete, Oma Gisela und Dackel Waldi. */
(() => {
  const { $, clamp, lerp, E, prog, popS, rng, byId, cue, cues, setT, disp, fmt, camLerp, OUT, sw,
    humanEls, humanDefaults, poseHuman, faceMarkup, armMarkup, TL } = Engine;

  const SKIN = '#F7CDAE', SKIN_SH = '#E8AE8A';
  const HAIR = '#ECE7E2', HAIR_D = '#C4BCB4';
  const DRESS = '#8CC3F0', DRESS_SH = '#6FA7DA';

  // ---------------------------------------------------------------- Oma Gisela
  const giselaMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="0" cy="4" rx="84" ry="13" fill="#1E3A1A" opacity=".2"/>
    <g id="${p}-bob">
      <rect x="-30" y="-58" width="20" height="36" rx="8" fill="#E9B999" ${sw}/>
      <rect x="10" y="-58" width="20" height="36" rx="8" fill="#E9B999" ${sw}/>
      <path d="M-48 0 L-6 0 L-6 -18 Q-6 -28 -16 -28 L-36 -28 Q-48 -28 -48 -14 Z" fill="#7A4A26" ${sw}/>
      <path d="M48 0 L6 0 L6 -18 Q6 -28 16 -28 L36 -28 Q48 -28 48 -14 Z" fill="#7A4A26" ${sw}/>
      <g id="${p}-armL" transform="translate(-50,-160)">${armMarkup(p, 'L', DRESS, '#fff', SKIN)}</g>
      <path d="M-48 -172 Q-66 -110 -84 -56 Q-60 -42 -30 -50 Q0 -40 30 -50 Q60 -42 84 -56 Q66 -110 48 -172 Q0 -186 -48 -172 Z" fill="url(#gDots)" ${sw}/>
      <path d="M20 -176 Q40 -174 48 -170 Q64 -112 80 -58 Q60 -48 34 -50 Q40 -112 20 -176 Z" fill="${DRESS_SH}" opacity=".55"/>
      <path d="M-34 -132 Q0 -124 34 -132 L40 -66 Q0 -56 -40 -66 Z" fill="#FFFFFF" ${sw}/>
      <path d="M-22 -104 H22 V-82 Q0 -78 -22 -82 Z" fill="#FFE3EC" stroke="${OUT}" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M-30 -180 Q0 -158 30 -180 L22 -168 Q0 -150 -22 -168 Z" fill="#fff" ${sw}/>
      <g id="${p}-scarfTail"><path d="M18 -170 Q60 -176 92 -160 Q118 -150 130 -126 Q104 -136 82 -138 Q50 -146 22 -152 Z" fill="#fff" ${sw}/></g>
      <path d="M-34 -176 Q0 -160 34 -176" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round"/>
      <path d="M-34 -176 Q0 -160 34 -176" stroke="${OUT}" stroke-width="3" fill="none" opacity=".4"/>
      <g fill="#fff" stroke="${OUT}" stroke-width="2">${[-22, -11, 0, 11, 22].map((x) => `<circle cx="${x}" cy="${-160 + Math.abs(x) * -0.25}" r="5"/>`).join('')}</g>
      <g id="${p}-armR" transform="translate(50,-160)">${armMarkup(p, 'R', DRESS, '#fff', SKIN)}</g>
      <g id="${p}-head">
        <ellipse cx="-74" cy="-226" rx="13" ry="17" fill="${SKIN}" ${sw}/>
        <ellipse cx="74" cy="-226" rx="13" ry="17" fill="${SKIN}" ${sw}/>
        <ellipse cx="0" cy="-232" rx="77" ry="74" fill="${SKIN}" ${sw}/>
        <circle cx="0" cy="-326" r="34" fill="${HAIR}" ${sw}/>
        <path d="M-20 -334 Q0 -344 20 -334" stroke="${HAIR_D}" stroke-width="4" fill="none" stroke-linecap="round"/>
        <path d="M-84 -226 Q-92 -290 -40 -308 Q0 -320 40 -308 Q92 -290 84 -226 Q74 -244 64 -262 Q40 -282 10 -276 Q-8 -290 -36 -276 Q-60 -268 -70 -246 Q-76 -238 -84 -226 Z" fill="${HAIR}" ${sw}/>
        <path d="M-58 -282 Q-36 -296 -12 -288 M14 -290 Q40 -298 58 -282" stroke="${HAIR_D}" stroke-width="4" fill="none" stroke-linecap="round"/>
        <ellipse cx="-48" cy="-196" rx="15" ry="9" fill="#FF8A9A" opacity=".6"/>
        <ellipse cx="48" cy="-196" rx="15" ry="9" fill="#FF8A9A" opacity=".6"/>
        <path d="M-62 -232 l-8 -4 M-62 -224 l-9 0 M62 -232 l8 -4 M62 -224 l9 0" stroke="${SKIN_SH}" stroke-width="3" stroke-linecap="round"/>
        ${faceMarkup(p, { brow: '#B9B0A8', eyeRx: 18, eyeRy: 21, pup: 10 })}
        <g fill="none" stroke="#C9952E" stroke-width="4.5">
          <circle cx="-27" cy="-228" r="27"/><circle cx="27" cy="-228" r="27"/><path d="M-1 -232 Q0 -238 1 -232"/>
          <path d="M-54 -232 L-74 -238 M54 -232 L74 -238"/>
        </g>
        <path d="M-7 -203 Q0 -195 7 -203" stroke="${SKIN_SH}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <g id="${p}-cap">
          <path d="M-82 -280 Q0 -300 82 -280" stroke="#7A4A26" stroke-width="13" fill="none"/>
          <g transform="translate(-30,-288)"><circle r="22" fill="#9ED8F5" stroke="#C9952E" stroke-width="7"/><path d="M-10 -6 Q-4 -12 4 -12" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
          <g transform="translate(30,-288)"><circle r="22" fill="#9ED8F5" stroke="#C9952E" stroke-width="7"/><path d="M-10 -6 Q-4 -12 4 -12" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
          <rect x="-9" y="-294" width="18" height="10" rx="4" fill="#7A4A26"/>
        </g>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Dackel Waldi (schaut nach links)
  const waldiMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="-10" cy="3" rx="120" ry="11" fill="#1E3A1A" opacity=".2"/>
    <g id="${p}-bob">
      <g id="${p}-tail" transform="translate(84,-84)"><path d="M0 0 Q30 -20 46 -60 Q50 -66 44 -66 Q26 -36 -4 -12 Z" fill="#8A4A24" ${sw}/></g>
      ${[-84, -56, 46, 72].map((x) => `<rect x="${x - 11}" y="-52" width="22" height="50" rx="9" fill="#7E4220" ${sw}/><ellipse cx="${x - 4}" cy="-3" rx="15" ry="7" fill="#7E4220" ${sw}/>`).join('')}
      <rect x="-118" y="-112" width="214" height="72" rx="36" fill="#A0582C" ${sw}/>
      <path d="M-100 -52 Q-10 -36 80 -52" stroke="#C88250" stroke-width="12" fill="none" stroke-linecap="round"/>
      <g id="${p}-head" >
        <path d="M-104 -112 Q-118 -134 -130 -150 L-92 -100 Z" fill="#A0582C"/>
        <ellipse cx="-128" cy="-136" rx="44" ry="38" fill="#A0582C" ${sw}/>
        <ellipse cx="-176" cy="-120" rx="44" ry="22" fill="#A0582C" ${sw}/>
        <circle cx="-218" cy="-126" r="11" fill="${OUT}"/>
        <circle cx="-221" cy="-130" r="3" fill="#fff"/>
        <g id="${p}-jaw" transform="translate(-150,-104)">
          <path d="M0 0 L-60 -4 Q-60 10 -40 14 Q-10 16 0 8 Z" fill="#8A4A24" ${sw}/>
          <path d="M-14 4 Q-30 16 -44 8" fill="#FF7B8A" stroke="${OUT}" stroke-width="3"/>
        </g>
        <g id="${p}-eye"><circle cx="-142" cy="-148" r="11" fill="#fff" stroke="${OUT}" stroke-width="3.5"/><circle id="${p}-pup" cx="-145" cy="-147" r="6" fill="${OUT}"/></g>
        <text id="${p}-euro" x="-142" y="-136" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="32" fill="#2DBE60" stroke="${OUT}" stroke-width="3" paint-order="stroke" style="display:none">€</text>
        <path d="M-156 -164 L-130 -160" stroke="${OUT}" stroke-width="5" stroke-linecap="round"/>
        <g id="${p}-ear" transform="translate(-104,-150)"><path d="M0 0 Q22 10 18 56 Q12 70 0 62 Q-10 30 -12 4 Z" fill="#6E3A1C" ${sw}/></g>
        <path d="M-96 -112 Q-110 -98 -100 -82" stroke="#E2374B" stroke-width="12" fill="none" stroke-linecap="round"/>
        <circle cx="-106" cy="-80" r="8" fill="#F2C14E" stroke="${OUT}" stroke-width="3"/>
        <g id="${p}-helmet">
          <path d="M-174 -160 Q-170 -206 -124 -208 Q-80 -206 -76 -160 Z" fill="#D5DCE6" ${sw}/>
          <g fill="#8E99AA">${[[-150, -184], [-128, -192], [-106, -184], [-140, -170], [-116, -170], [-94, -170], [-160, -170]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4"/>`).join('')}</g>
          <path d="M-184 -162 L-170 -162 M-80 -162 L-66 -162" stroke="${OUT}" stroke-width="7" stroke-linecap="round"/>
          <rect x="-180" y="-166" width="110" height="10" rx="5" fill="#BAC4D2" ${sw}/>
        </g>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Requisiten
  const rocketMarkup = (p) => `
    <g id="${p}-flame" style="display:none">
      <path d="M-56 -4 Q-40 80 0 150 Q40 80 56 -4 Z" fill="#FF8A2B"/>
      <path d="M-32 -4 Q-22 50 0 100 Q22 50 32 -4 Z" fill="#FFD43B"/>
    </g>
    <path d="M-84 -92 L-140 0 L-84 0 Z" fill="#E2374B" ${sw}/>
    <path d="M84 -92 L140 0 L84 0 Z" fill="#E2374B" ${sw}/>
    <rect x="-86" y="-292" width="172" height="292" rx="26" fill="#3E9A4A" ${sw}/>
    <rect x="-62" y="-280" width="20" height="268" rx="10" fill="#5DBB68" opacity=".7"/>
    ${[-58, -146, -234].map((y) => `<rect x="-88" y="${y - 9}" width="176" height="18" rx="9" fill="#2F7D3A" ${sw}/>`).join('')}
    <rect x="-9" y="-80" width="18" height="80" rx="4" fill="#E2374B" ${sw}/>
    <text x="0" y="-178" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="46" fill="#fff" stroke="${OUT}" stroke-width="5" paint-order="stroke">GS-1</text>
    <g transform="translate(0,-102)"><circle r="34" fill="#AEB8C6" ${sw}/><circle r="23" fill="#8FD0F5" stroke="${OUT}" stroke-width="4"/>
      <path d="M-10 -8 Q-4 -14 4 -14" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>
    <path d="M-92 -290 L0 -402 L92 -290 Z" fill="#C9D3DE" ${sw}/>
    <path d="M-30 -330 L0 -396 L8 -330 Z" fill="#E9EEF4"/>
    <rect x="-11" y="-428" width="22" height="34" rx="5" fill="#C9D3DE" ${sw}/>
    <path d="M60 -300 L84 -352" stroke="${OUT}" stroke-width="5" stroke-linecap="round"/><circle cx="86" cy="-358" r="9" fill="#E2374B" stroke="${OUT}" stroke-width="4"/>`;

  const gnomeMarkup = () => `
    <path d="M-50 0 L-40 -96 M50 0 L40 -96 M-40 -96 L40 -96" stroke="#7B8696" stroke-width="7" stroke-linecap="round"/>
    <rect x="-48" y="-104" width="96" height="16" rx="6" fill="#2F80D1" ${sw}/>
    <path d="M-42 -100 L-46 -170 L46 -170 L42 -100" fill="url(#chairStripes)" ${sw}/>
    <rect x="-34" y="-112" width="68" height="18" rx="8" fill="#7A4A26" ${sw}/>
    <path d="M-30 -102 L-40 -60 L-20 -58 M30 -102 L40 -60 L20 -58" stroke="#7A4A26" stroke-width="16" fill="none" stroke-linecap="round"/>
    <ellipse cx="-34" cy="-56" rx="16" ry="9" fill="${OUT}"/><ellipse cx="34" cy="-56" rx="16" ry="9" fill="${OUT}"/>
    <path d="M-36 -110 Q-40 -170 0 -172 Q40 -170 36 -110 Z" fill="#2F80D1" ${sw}/>
    <circle cx="0" cy="-192" r="30" fill="${SKIN}" ${sw}/>
    <path d="M-30 -186 Q-36 -130 0 -120 Q36 -130 30 -186 Q14 -170 0 -176 Q-14 -170 -30 -186 Z" fill="#fff" ${sw}/>
    <circle cx="0" cy="-184" r="10" fill="#F59A8C" ${sw}/>
    <g id="gnomeBino"><rect x="-30" y="-218" width="26" height="22" rx="8" fill="${OUT}"/><rect x="4" y="-218" width="26" height="22" rx="8" fill="${OUT}"/>
      <circle cx="-17" cy="-207" r="7" fill="#5DA8E0"/><circle cx="17" cy="-207" r="7" fill="#5DA8E0"/>
      <path d="M-32 -198 L-46 -170 M32 -198 L46 -170" stroke="#2F80D1" stroke-width="12" stroke-linecap="round"/></g>
    <path d="M-34 -214 Q0 -230 34 -214 L6 -320 Q0 -326 -6 -320 Z" fill="#E2374B" ${sw}/>`;

  const crateMarkup = () => `
    ${[-40, 0, 40].map((x, i) => `<g transform="translate(${x},-60)"><rect x="-15" y="-96" width="30" height="100" rx="12" fill="#7FCBB0" ${sw}/>
      <rect x="-9" y="-118" width="18" height="24" rx="4" fill="#2F80D1" ${sw}/><rect x="-15" y="-66" width="30" height="30" fill="#fff" opacity=".85"/>
      <text x="0" y="-45" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="11" fill="#2F80D1">MEDIUM</text></g>`).join('')}
    <rect x="-72" y="-70" width="144" height="70" rx="8" fill="#F2C14E" ${sw}/>
    <path d="M-60 -50 H60 M-60 -30 H60" stroke="#C9952E" stroke-width="5"/>`;

  const pigMarkup = () => `
    <g id="pigBody">
      ${[-40, -14, 18, 44].map((x) => `<rect x="${x - 9}" y="-30" width="18" height="30" rx="6" fill="#F58FA8" ${sw}/>`).join('')}
      <path d="M70 -60 q24 -10 14 10 q-8 12 10 8" stroke="${OUT}" stroke-width="5" fill="none" stroke-linecap="round"/>
      <ellipse cx="0" cy="-66" rx="80" ry="54" fill="#FFA8BE" ${sw}/>
      <path d="M-50 -110 L-40 -140 L-22 -114 Z M20 -116 L36 -142 L44 -108 Z" fill="#F58FA8" ${sw}/>
      <ellipse cx="-82" cy="-66" rx="18" ry="22" fill="#F58FA8" ${sw}/>
      <circle cx="-86" cy="-72" r="4" fill="${OUT}"/><circle cx="-86" cy="-58" r="4" fill="${OUT}"/>
      <circle cx="-46" cy="-84" r="7" fill="${OUT}"/><circle cx="-44" cy="-87" r="2.5" fill="#fff"/>
      <rect x="-22" y="-122" width="44" height="10" rx="5" fill="${OUT}"/>
    </g>
    <g id="pigCoins"></g>`;

  const sausageMarkup = () => `
    <path d="M-60 0 Q-64 -26 -30 -28 L30 -28 Q64 -26 60 0 Q64 26 30 28 L-30 28 Q-64 26 -60 0 Z" fill="#E8A3A0" ${sw}/>
    <path d="M-40 -10 Q0 -18 40 -10" stroke="#fff" stroke-width="6" opacity=".6" fill="none" stroke-linecap="round"/>
    <rect x="-74" y="-8" width="14" height="16" rx="3" fill="#C9D3DE" ${sw}/><rect x="60" y="-8" width="14" height="16" rx="3" fill="#C9D3DE" ${sw}/>`;

  // ---------------------------------------------------------------- Welt
  function world() {
    const r = rng(8);
    const clouds = [[300, 380, 1.1], [900, 250, 0.9], [1500, 430, 1.3], [2200, 300, 1.0], [-300, 260, 1.1]].map(([x, y, s], i) =>
      `<g id="cloud${i}" data-x="${x}" data-y="${y}" data-s="${s}"><g fill="#fff" opacity=".9"><ellipse rx="120" ry="40"/><circle cx="-50" cy="-20" r="46"/><circle cx="20" cy="-40" r="58"/><circle cx="74" cy="-12" r="40"/></g></g>`).join('');
    let trees = '';
    for (let i = 0; i < 16; i++) {
      const x = -500 + i * 230 + r() * 80, y = 1050, s = 0.8 + r() * 0.6;
      trees += `<g transform="translate(${x},${y}) scale(${s})"><rect x="-10" y="-60" width="20" height="60" fill="#7A5A3A"/>
        <circle cx="0" cy="-120" r="80" fill="${i % 2 ? '#78B565' : '#6AAA5A'}"/><circle cx="-50" cy="-80" r="50" fill="${i % 2 ? '#78B565' : '#6AAA5A'}"/><circle cx="52" cy="-84" r="54" fill="${i % 2 ? '#78B565' : '#6AAA5A'}"/></g>`;
    }
    let fence = '';
    for (let x = -600; x < 3000; x += 64) fence += `<path d="M${x} 1080 L${x + 64} 1150 M${x + 64} 1080 L${x} 1150" stroke="#D9A066" stroke-width="12" stroke-linecap="round"/>`;
    for (let x = -600; x < 3000; x += 256) fence += `<rect x="${x - 8}" y="1066" width="16" height="96" rx="4" fill="#B98048"/>`;
    let stones = '';
    [[1230, 1880, 70], [1260, 1720, 62], [1290, 1580, 54], [1315, 1460, 46], [1335, 1370, 40]].forEach(([x, y, s]) => {
      stones += `<ellipse cx="${x}" cy="${y}" rx="${s * 1.4}" ry="${s * 0.5}" fill="#B9BEC6" stroke="#8E95A1" stroke-width="5"/>`;
    });
    let veg = '';
    for (let i = 0; i < 5; i++) veg += `<g transform="translate(${290 + i * 95},${1470 + (i % 2) * 18})"><circle r="34" fill="#7FCB5A" ${sw}/><path d="M-18 -6 Q0 -22 18 -6 M-12 8 Q0 -4 12 8" stroke="#4F9A3A" stroke-width="4" fill="none"/></g>`;
    for (let i = 0; i < 6; i++) veg += `<g transform="translate(${270 + i * 80},${1532})"><path d="M0 0 L-10 -34 M0 0 L0 -40 M0 0 L10 -34" stroke="#3FAE5A" stroke-width="7" stroke-linecap="round"/><path d="M-8 0 L0 16 L8 0 Z" fill="#FF8A2B"/></g>`;
    return `
    <defs>
      <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6FB6EE"/><stop offset=".6" stop-color="#B7D9F2"/><stop offset="1" stop-color="#FFD9AE"/></linearGradient>
      <linearGradient id="gLawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#93D36E"/><stop offset="1" stop-color="#5EAA4A"/></linearGradient>
      <pattern id="gDots" width="34" height="34" patternUnits="userSpaceOnUse"><rect width="34" height="34" fill="${DRESS}"/><circle cx="8" cy="8" r="4.5" fill="#fff"/><circle cx="25" cy="25" r="4.5" fill="#fff"/></pattern>
      <pattern id="chairStripes" width="20" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#fff"/><rect x="10" width="10" height="10" fill="#2F80D1"/></pattern>
      <pattern id="curtain" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#fff"/><rect width="8" height="8" fill="#E2374B"/><rect x="8" y="8" width="8" height="8" fill="#E2374B"/></pattern>
    </defs>
    <rect x="-1500" y="-2600" width="5200" height="3700" fill="url(#gSky)"/>
    <g id="moon" transform="translate(1720,330)">
      <circle r="88" fill="#FFFFFF" opacity=".25"/><circle r="70" fill="#F4F2EC"/>
      <circle cx="-22" cy="-14" r="14" fill="#DDD9CF"/><circle cx="24" cy="16" r="10" fill="#DDD9CF"/><circle cx="10" cy="-30" r="7" fill="#DDD9CF"/>
    </g>
    <g id="clouds">${clouds}</g>
    ${trees}
    <path d="M-1500 1100 Q-1400 1010 -1300 1100 ${Array.from({ length: 50 }, (_, i) => `Q${-1250 + i * 100} 1020 ${-1200 + i * 100} 1100`).join(' ')} L3700 1200 L-1500 1200 Z" fill="#4E8F47"/>
    ${fence}
    <rect x="-1500" y="1140" width="5200" height="2600" fill="url(#gLawn)"/>
    <g opacity=".12">${Array.from({ length: 12 }, (_, i) => `<rect x="${-1500 + i * 440}" y="1140" width="220" height="2600" fill="#fff"/>`).join('')}</g>
    <g id="laube">
      <rect x="420" y="960" width="440" height="250" fill="#D79A5B" ${sw}/>
      ${[470, 520, 570, 620, 670, 720, 770, 820].map((x) => `<line x1="${x}" y1="964" x2="${x}" y2="1206" stroke="#B9783E" stroke-width="4"/>`).join('')}
      <path d="M386 978 L640 820 L894 978 Z" fill="#C8443A" ${sw}/>
      <path d="M420 960 L640 840 L860 960" stroke="#A8332B" stroke-width="6" fill="none"/>
      <rect x="470" y="1010" width="130" height="100" fill="#9ED8F5" ${sw}/>
      <path d="M470 1010 L520 1010 L505 1110 L470 1110 Z M600 1010 L550 1010 L565 1110 L600 1110 Z" fill="url(#curtain)" stroke="${OUT}" stroke-width="3"/>
      <rect x="460" y="1110" width="150" height="26" rx="5" fill="#8C5A30" ${sw}/>
      ${[485, 515, 545, 575].map((x) => `<circle cx="${x}" cy="1102" r="11" fill="#FF5A7A" stroke="${OUT}" stroke-width="3"/>`).join('')}
      <rect x="700" y="1040" width="100" height="170" fill="#8C5A30" ${sw}/>
      <circle cx="782" cy="1130" r="6" fill="#F2C14E"/>
      <rect x="560" y="900" width="160" height="40" rx="8" fill="#fff" ${sw}/>
      <text x="640" y="928" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="24" fill="${OUT}">PARZELLE 17</text>
    </g>
    ${stones}
    <g>${veg}</g>
    <g id="pad"><rect x="1240" y="1300" width="220" height="40" rx="6" fill="#A9AFB9" ${sw}/><line x1="1313" y1="1302" x2="1313" y2="1338" stroke="${OUT}" stroke-width="4"/><line x1="1386" y1="1302" x2="1386" y2="1338" stroke="${OUT}" stroke-width="4"/></g>
    <path id="hose" d="M1520 1300 Q1480 1330 1420 1310" stroke="#E0B92A" stroke-width="12" fill="none" stroke-linecap="round"/>
    <g id="smoke"></g>
    <g id="rocket" transform="translate(1350,1306)">${rocketMarkup('r1')}</g>
    <g id="crate" transform="translate(1590,1334)">${crateMarkup()}</g>
    <g id="gnome" transform="translate(1890,1370)">${gnomeMarkup()}</g>
    <g id="pig" transform="translate(1210,1372)" style="display:none">${pigMarkup()}</g>
    <g id="giselaW" transform="translate(1110,1350)">${giselaMarkup('g1')}</g>
    <g id="waldiW" style="display:none">${waldiMarkup('w1')}</g>
    <g id="sausage" style="display:none">${sausageMarkup()}</g>
    <g id="qmarks" font-family="Fredoka" font-weight="700" font-size="70" fill="#fff" stroke="${OUT}" stroke-width="8" paint-order="stroke" style="display:none">
      <text id="q1">?</text><text id="q2">?</text>
    </g>`;
  }

  // ---------------------------------------------------------------- Weltraum
  const EARTH = [330, 1980], EARTH_R = 760, MOON = [800, 560];
  const PATH = { a: [560, 1270], c: [380, 760], b: [690, 610] };
  const bez = (p) => {
    const u = 1 - p;
    return [u * u * PATH.a[0] + 2 * u * p * PATH.c[0] + p * p * PATH.b[0], u * u * PATH.a[1] + 2 * u * p * PATH.c[1] + p * p * PATH.b[1]];
  };
  function alt() {
    const r = rng(42);
    let stars = '';
    for (let i = 0; i < 160; i++) stars += `<circle class="star" cx="${r() * 1080}" cy="${r() * 1920}" r="${1 + r() * 3}" fill="#fff" data-p="${r() * 6}"/>`;
    return `
    <defs>
      <radialGradient id="gSpace" cx=".5" cy=".4" r=".9"><stop offset="0" stop-color="#3A2C80"/><stop offset="1" stop-color="#110C30"/></radialGradient>
      <radialGradient id="gEarth" cx=".4" cy=".25" r=".8"><stop offset="0" stop-color="#5EC1FF"/><stop offset="1" stop-color="#1C5FB0"/></radialGradient>
      <clipPath id="clipEarth"><circle cx="${EARTH[0]}" cy="${EARTH[1]}" r="${EARTH_R}"/></clipPath>
    </defs>
    <rect width="1080" height="1920" fill="url(#gSpace)"/>
    <g id="stars">${stars}</g>
    <g id="spaceCam">
      <circle cx="${MOON[0]}" cy="${MOON[1]}" r="230" fill="#FFF" opacity=".08"/>
      <g transform="translate(${MOON[0]},${MOON[1]})">
        <circle r="190" fill="#E6E3DA" ${sw}/>
        <circle cx="-60" cy="-40" r="36" fill="#CFCABD"/><circle cx="70" cy="30" r="26" fill="#CFCABD"/><circle cx="20" cy="-90" r="18" fill="#CFCABD"/><circle cx="-30" cy="80" r="22" fill="#CFCABD"/>
        <g id="moonFlag" transform="translate(70,-170)" style="display:none"><line x1="0" y1="0" x2="0" y2="-120" stroke="${OUT}" stroke-width="7"/>
          <path d="M4 -118 L90 -100 L4 -80 Z" fill="#B98CFF" ${sw}/><text x="34" y="-93" font-family="Fredoka" font-weight="700" font-size="18" fill="#fff">GS-1</text></g>
        <g id="moonGisela" transform="translate(-40,-180) scale(.55)" style="display:none">${giselaMarkup('g2')}</g>
      </g>
      <circle cx="${EARTH[0]}" cy="${EARTH[1]}" r="${EARTH_R + 40}" fill="#7FD0FF" opacity=".18"/>
      <circle cx="${EARTH[0]}" cy="${EARTH[1]}" r="${EARTH_R}" fill="url(#gEarth)" ${sw}/>
      <g clip-path="url(#clipEarth)" fill="#7ED957" stroke="#4FA83A" stroke-width="8">
        <path d="M-200 1400 Q0 1240 220 1300 Q360 1340 300 1440 Q200 1520 40 1500 Q-120 1480 -200 1400 Z"/>
        <path d="M420 1260 Q520 1210 640 1250 Q720 1300 660 1360 Q560 1400 470 1360 Q400 1320 420 1260 Z"/>
        <path d="M760 1420 Q880 1380 960 1460 Q1000 1560 880 1580 Q760 1560 760 1420 Z"/>
        <ellipse cx="200" cy="1600" rx="160" ry="60" fill="#fff" stroke="none" opacity=".6"/>
        <ellipse cx="620" cy="1480" rx="120" ry="34" fill="#fff" stroke="none" opacity=".6"/>
      </g>
      <g id="homePin" transform="translate(${PATH.a[0]},${PATH.a[1]})">
        <path d="M0 0 Q-14 -22 -14 -32 A14 14 0 1 1 14 -32 Q14 -22 0 0 Z" fill="#FF4B5C" stroke="${OUT}" stroke-width="4"/><circle cy="-32" r="5" fill="#fff"/>
        <g id="homeLabel" transform="translate(0,-74)">
          <rect x="-120" y="-24" width="240" height="42" rx="21" fill="#fff" stroke="${OUT}" stroke-width="4"/>
          <text x="0" y="6" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" fill="${OUT}">OMAS GARTEN · 0 m</text>
        </g>
      </g>
      <path id="traj" d="M${PATH.a[0]} ${PATH.a[1]} Q${PATH.c[0]} ${PATH.c[1]} ${PATH.b[0]} ${PATH.b[1]}" fill="none" stroke="#fff" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round" opacity=".7"/>
      <g id="miniRocket" style="display:none"><g transform="scale(.28)">${rocketMarkup('r2')}</g></g>
    </g>`;
  }

  // ---------------------------------------------------------------- Icons für die Abstimmung
  const chuteIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><path d="M10 52 Q60 -10 110 52 Q96 42 85 52 Q72 40 60 52 Q48 40 35 52 Q24 42 10 52 Z" fill="#FF8A9A" stroke="${OUT}" stroke-width="6" stroke-linejoin="round"/>
    <path d="M35 52 Q47 30 60 52 M60 52 Q73 30 85 52" fill="#fff" stroke="${OUT}" stroke-width="4"/>
    <path d="M12 54 L52 96 M108 54 L68 96 M60 52 L60 92" stroke="${OUT}" stroke-width="3"/><rect x="46" y="88" width="28" height="24" rx="8" fill="#8CC3F0" stroke="${OUT}" stroke-width="5"/></svg>`;
  const helmetIcon = `<svg width="130" height="120" viewBox="-250 -240 220 230"><circle cx="-130" cy="-130" r="96" fill="#BFE8FF" opacity=".55" stroke="${OUT}" stroke-width="7"/>
    <g transform="translate(0,0)">${waldiMarkup('wc')}</g><path d="M-200 -190 Q-180 -212 -150 -218" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/></svg>`;
  const qIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><text x="60" y="100" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="112" fill="#FF4B5C" stroke="${OUT}" stroke-width="7" paint-order="stroke">?</text></svg>`;

  // ---------------------------------------------------------------- Szenenzustand + Schnitte
  const base = () => ({
    gis: Object.assign(humanDefaults(), { x: 1110, y: 1350, s: 1, talk: false }),
    waldi: null, rocketLift: 0, flame: 0, pig: null, sausage: null, qmarks: null, gnomeLook: false,
  });
  const W = (o) => Object.assign({ x: 900, y: 1372, s: 1, flip: true, jaw: 0, euro: false, helmet: true, hop: false, look: [0, 0] }, o);

  const shots = {
    s01(S, t, s, lt, d) { S.cam = camLerp([1250, 1110, 0.72], [1250, 1150, 0.8], E.inOut(clamp(lt / d))); S.ui.title = s.start - 0.15; S.gis.armR = -150 + Math.sin(t * 12) * 16; },
    s02(S, t, s, lt, d) {
      S.cam = camLerp([1110, 1160, 2.55], [1110, 1160, 2.72], lt / d);
      S.gis.armR = -150 + Math.sin(t * 12) * 18; S.gis.expr = 'happy';
      S.ui.chip = { t0: cue('s02', 'pop'), text: '👵 GISELA · 78 JAHRE', cls: 'yellow' };
    },
    s03(S, t, s, lt, d) {
      S.cam = camLerp([1230, 1130, 1.15], [1230, 1125, 1.28], lt / d);
      const st = cue('s03', 'stamp');
      if (t < st) { S.gis.armR = -160; S.gis.fingerR = true; S.gis.look = [5, -8]; }
      else { S.gis.armL = 155 + Math.sin(t * 9) * 8; S.gis.armR = -155; S.gis.expr = 'happy'; S.gis.bounce = true; }
      S.ui.stamp = st; S.confetti = cue('s03', 'confetti');
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s04(S, t, s, lt, d) {
      S.cam = camLerp([1250, 1060, 0.95], [1250, 1060, 1.0], lt / d);
      S.gis.armR = -160; S.gis.fingerR = true; S.gis.look = [3, -7];
      S.ui.profile = { t0: s.start + 0.03, followAt: null };
    },
    s05(S, t, s, lt, d) {
      S.cam = camLerp([1250, 1060, 1.0], [1250, 1060, 1.05], lt / d);
      S.gis.armR = -160; S.gis.fingerR = true; S.gis.look = [6, -4];
      S.ui.profile = { t0: byId.s04.start + 0.03, followAt: cue('s05', 'ding') };
      const rk = cue('s05', 'rocket');
      S.rocketLift = 34 * E.out(prog(t, rk, 0.6));
      S.flame = t > rk ? (t < rk + 0.9 ? 1 : 0.35) : 0;
      S.ui.plusOne = cue('s05', 'pop'); S.ui.plusOneTop = 900;
    },
    s06(S, t, s, lt, d) {
      S.cam = camLerp([1250, 1150, 0.95], [1250, 1130, 1.05], E.out(lt / d));
      S.gis.armL = 72; S.gis.armR = -72; S.gis.expr = 'happy';
      S.ui.banner = s.start + 0.04; S.sparkle = s.start + 0.05;
    },
    s07(S, t, s, lt, d) { S.cam = camLerp([1350, 1150, 2.05], [1350, 1150, 2.2], lt / d); S.ui.chip = { t0: cue('s07', 'pop'), text: '🛢️ REGENTONNE · BJ. 1987', cls: '' }; },
    s08(S, t, s, lt, d) { S.cam = camLerp([1350, 960, 2.8], [1350, 955, 2.95], lt / d); S.ui.chip = { t0: cue('s08', 'pop'), text: '🍳 1 × TRICHTER (AUS DER KÜCHE)', cls: '' }; },
    s09(S, t, s, lt, d) { S.cam = camLerp([1570, 1210, 2.5], [1570, 1210, 2.65], lt / d); S.ui.chip = { t0: cue('s09', 'pop'), text: '⛽ 3 × SPRUDEL (MEDIUM)', cls: 'red' }; },
    s10(S, t, s, lt, d) {
      S.cam = camLerp([1240, 1170, 1.15], [1240, 1170, 1.2], lt / d);
      S.gis.armL = 55; S.gis.armR = -55; S.gis.tilt = 8; S.gis.look = [Math.sin(t * 3) * 7, 0];
      S.ui.chip = { t0: s.start + 0.05, text: '📏 HÖHE: 0 m', cls: 'red' };
      S.ui.zirp = { t0: cue('s10', 'crickets'), x: 640, y: 1150 };
    },
    s11(S, t, s, lt, d) {
      S.cam = camLerp([1110, 1150, 2.6], [1110, 1150, 2.75], lt / d);
      S.gis.expr = 'worried'; S.gis.tilt = -6; S.gis.look = [-5, -4]; S.gis.armL = 30;
      S.qmarks = s.start + 0.2;
      S.ui.chip = { t0: cue('s11', 'pop'), text: '🧑‍🚀 CREW: ?', cls: '' };
    },
    s12(S, t, s, lt, d) {
      S.cam = camLerp([980, 1240, 1.9], [980, 1240, 2.0], lt / d);
      const p = E.out(prog(t, s.start, 0.5));
      const b = cue('s12', 'bark');
      S.waldi = W({ x: lerp(560, 900, p), hop: p < 1, jaw: t > b && t < b + 0.35 ? 30 : 0 });
      S.gis.look = [-8, 4]; S.gis.expr = t > b ? 'happy' : 'smile';
      S.ui.chip = { t0: cue('s12', 'pop'), text: '🐶 KOPILOT', cls: 'yellow' };
    },
    s13(S, t, s, lt, d) {
      S.cam = camLerp([1040, 1250, 2.7], [1040, 1250, 2.85], lt / d);
      const c = cue('s13', 'crunch');
      S.waldi = W({ jaw: t > c - 0.15 && t < c + 0.4 ? 26 * Math.abs(Math.sin((t - c) * 20)) : 0, look: [3, 1] });
      S.sausage = { t0: s.start + 0.1, gone: c };
      S.ui.chip = { t0: cue('s13', 'pop'), text: '💰 GEHALT: 1 LEBERWURST', cls: 'yellow' };
    },
    s14(S, t, s, lt, d) {
      S.cam = camLerp([1010, 1210, 1.5], [1010, 1210, 1.56], lt / d);
      const [b1, b2] = cues('s14', 'beep'); const bk = cue('s14', 'bark');
      S.waldi = W({ jaw: t > bk && t < bk + 0.45 ? 32 : 0, hop: t > bk });
      S.ui.big = t >= bk ? { t0: bk, text: 'WUFF!', cls: 'red', rot: -8 } : t >= b2 ? { t0: b2, text: '2' } : { t0: b1, text: '3' };
      if (t >= bk) { S.gis.expr = 'o'; S.gis.armR = -170; } else { S.gis.look = [0, -6]; }
    },
    s15(S, t, s, lt, d) {
      S.layer = 'alt';
      S.space = { z: lerp(3.3, 3.45, lt / d), f: PATH.a, label: true, rocket: null, moon: false };
      S.ui.chip = { t0: cue('s15', 'pop'), text: '📏 HÖHE: 0 m', cls: '' };
    },
    s16(S, t, s, lt, d) {
      S.layer = 'alt';
      const p = E.inOut(prog(t, s.start, 0.6));
      const fly = E.inOut(prog(t, cue('s16', 'rocket'), 1.0));
      S.space = { z: lerp(3.45, 1, p), f: [lerp(PATH.a[0], 540, p), lerp(PATH.a[1], 960, p)], label: false, rocket: fly, moon: fly >= 1 };
      const h = Math.pow(prog(t, cue('s16', 'rocket'), 1.05), 2) * 384400000;
      S.ui.chip = { t0: s.start - 5, text: `📏 HÖHE: ${fmt(h)} m`, cls: h > 0 ? 'green' : '' };
    },
    s17(S, t, s, lt, d) {
      S.cam = camLerp([1300, 1140, 1.0], [1300, 1140, 1.06], lt / d);
      S.gis.armL = 60; S.gis.armR = -150; S.gis.look = [6, -6];
      S.ui.chip = { t0: cue('s17', 'pop'), text: '⏰ MORGEN · 7:00 · START', cls: '' };
    },
    s18(S, t, s, lt, d) {
      S.cam = camLerp([1650, 1220, 1.5], [1700, 1225, 1.55], lt / d);
      S.ui.chip = { t0: cue('s18', 'pop'), text: '👀 ZUSCHAUER: ?', cls: '' };
    },
    s19(S, t, s, lt, d) {
      S.cam = camLerp([1890, 1230, 2.6], [1890, 1230, 2.75], lt / d);
      S.gnomeLook = true;
      S.ui.chip = { t0: cue('s19', 'pop'), text: '👀 1 × GARTENZWERG', cls: 'red' };
      S.ui.zirp = { t0: cue('s19', 'crickets'), x: 120, y: 1150 };
    },
    s20(S, t, s, lt, d) {
      S.cam = camLerp([1110, 1010, 2.35], [1110, 1010, 2.45], lt / d);
      S.gis.armR = -158; S.gis.fingerR = true; S.gis.look = [3, -7];
      S.ui.profile = { t0: s.start + 0.02, followAt: cue('s20', 'tap'), hand: true };
    },
    s21(S, t, s, lt, d) {
      S.cam = camLerp([1080, 1190, 1.3], [1080, 1190, 1.38], lt / d);
      S.waldi = W({ hop: true });
      S.gis.armL = 150 + Math.sin(t * 9) * 8; S.gis.armR = -150; S.gis.expr = 'happy'; S.gis.bounce = true;
      S.ui.comment = cue('s21', 'blip');
    },
    s22(S, t, s, lt, d) {
      S.cam = camLerp([1080, 1190, 1.38], [1080, 1190, 1.44], lt / d);
      S.waldi = W({});
      S.dim = clamp(lt / 0.2) * 0.85;
      const st = cue('s22', 'stamp');
      S.ui.ticket = { t0: cue('s22', 'pop'), stamp: st };
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s23(S, t, s, lt, d) {
      S.cam = camLerp([1080, 1190, 1.44], [1080, 1190, 1.48], lt / d);
      S.waldi = W({}); S.dim = 0.85;
      S.ui.ticket = { t0: s.start - 5, stamp: s.start - 5 };
      const n = cues('s23', 'tick').filter((x) => t >= x).length;
      S.ui.chip2 = { t0: cue('s23', 'tick'), text: `⏰ NUR HEUTE · 23:59:${String(59 - n).padStart(2, '0')}`, cls: 'red', top: 860 };
    },
    s24(S, t, s, lt, d) {
      S.cam = camLerp([1200, 1160, 1.12], [1200, 1160, 1.2], lt / d);
      S.waldi = W({}); S.gis.armL = 70; S.gis.armR = -70;
      S.ui.chip = { t0: cue('s24', 'pop'), text: '🗳️ AB JETZT BESTIMMT IHR', cls: 'green' };
      const b = cues('s24', 'blip');
      S.floatBubbles = [b[0], b[1], b[2], b[2] + 0.2];
    },
    s25(S, t, s, lt, d) {
      S.cam = camLerp([1260, 1270, 2.7], [1260, 1270, 2.85], lt / d);
      S.pig = { coins: null };
      S.waldi = W({ x: 1540, y: 1382, flip: false, look: [-3, 2] });
      S.ui.kasse = { t0: cue('s25', 'pop'), value: 0 };
    },
    s26(S, t, s, lt, d) {
      S.cam = camLerp([1260, 1270, 2.85], [1260, 1265, 3.0], lt / d);
      const k = cue('s26', 'kaching');
      S.pig = { coins: k };
      S.waldi = W({ x: 1540, y: 1382, flip: false, euro: t > k + 0.1, jaw: t > k + 0.1 ? 22 : 0 });
      S.ui.kasse = { t0: byId.s25.start - 5, value: 500 * E.out(prog(t, k, 0.55)) };
    },
    s27(S, t, s, lt, d) { cardsShot(S, t); S.gis.armR = -160; S.gis.fingerR = true; S.gis.look = [0, -7]; },
    s28(S, t, s, lt, d) { cardsShot(S, t); const b = cue('s28', 'bark'); S.waldi.hop = true; S.waldi.jaw = t > b && t < b + 0.35 ? 30 : 0; },
    s29(S, t, s, lt, d) { cardsShot(S, t); S.gis.armL = 60; S.gis.armR = -60; S.gis.tilt = 8; },
    s30(S, t, s, lt, d) {
      cardsShot(S, t);
      S.gis.armR = -150 + Math.sin(t * 12) * 16; S.gis.expr = t > s.speechEnd ? 'happy' : 'smile';
      S.waldi.hop = t > s.speechEnd;
      S.ui.vote = cue('s30', 'pop');
      const p = E.out(prog(t, s.start + 0.2, 2.6));
      S.ui.likes = [287 * p, 512 * p, 143 * p];
      S.hearts = cues('s30', 'hearts');
    },
  };
  function cardsShot(S, t) {
    const a = byId.s27.start;
    S.cam = camLerp([1230, 1110, 1.0], [1230, 1100, 1.1], clamp((t - a) / (TL.duration - a)));
    S.pig = { coins: null, still: true };
    S.waldi = W({ x: 960, y: 1382 });
    S.ui.cards = [cue('s27', 'card'), cue('s28', 'card'), cue('s29', 'card')];
  }

  // ---------------------------------------------------------------- Zeichnen
  const G1 = humanEls('g1'), G2 = humanEls('g2');
  const wq = (p, s) => document.getElementById(`${p}-${s}`);
  function poseWaldi(p, P, t) {
    setT(wq(p, 'bob'), `translate(0,${Math.sin(t * 6) * 2 + (P.hop ? -Math.abs(Math.sin(t * 10)) * 20 : 0)})`);
    setT(wq(p, 'tail'), `translate(84,-84) rotate(${Math.sin(t * 16) * 18})`);
    setT(wq(p, 'jaw'), `translate(-150,-104) rotate(${-P.jaw})`);
    setT(wq(p, 'ear'), `translate(-104,-150) rotate(${P.jaw ? -25 : Math.sin(t * 3) * 4})`);
    setT(wq(p, 'pup'), `translate(${P.look[0]},${P.look[1]})`);
    disp(wq(p, 'eye'), !P.euro); disp(wq(p, 'euro'), P.euro);
    disp(wq(p, 'helmet'), P.helmet);
  }

  function drawWorld(S, t) {
    for (let i = 0; i < 5; i++) {
      const c = $(`cloud${i}`);
      setT(c, `translate(${+c.dataset.x + t * 12 * c.dataset.s},${+c.dataset.y}) scale(${c.dataset.s})`);
    }
    // Rakete
    const lift = S.rocketLift;
    setT($('rocket'), `translate(${1350 + (S.flame > 0.5 ? Math.sin(t * 70) * 2 : 0)},${1306 - lift})`);
    const fl = $('r1-flame');
    disp(fl, S.flame > 0);
    if (S.flame > 0) setT(fl, `scale(${0.7 + 0.3 * Math.sin(t * 40)},${S.flame * (0.8 + 0.25 * Math.sin(t * 33))})`);
    let smoke = '';
    if (S.flame > 0) {
      for (let i = 0; i < 7; i++) {
        const k = ((t * 1.6 + i / 7) % 1);
        smoke += `<circle cx="${1350 + (i % 2 ? 1 : -1) * (40 + k * 160)}" cy="${1320 - k * 30}" r="${30 + k * 50}" fill="#fff" opacity="${0.75 * (1 - k)}"/>`;
      }
    }
    $('smoke').innerHTML = smoke;
    // Zwerg
    setT($('gnomeBino'), `translate(0,${S.gnomeLook ? Math.sin(t * 2) * 3 : 0})`);
    // Sparschwein
    const pig = $('pig');
    if (S.pig) {
      disp(pig, true);
      const k = S.pig.coins;
      const wob = k && t > k && t < k + 0.6 ? Math.sin((t - k) * 40) * 4 * (1 - (t - k) / 0.6) : 0;
      setT($('pigBody'), `rotate(${wob} 0 -60)`);
      let coins = '';
      if (k && t >= k) {
        const lt = t - k, cr = rng(17);
        for (let i = 0; i < 16; i++) {
          const a = -Math.PI / 2 + (cr() - 0.5) * 1.6, v = 200 + cr() * 260;
          const tt = Math.min(lt, 1.2);
          const x = Math.cos(a) * v * tt, y = -118 + Math.sin(a) * v * tt + 520 * tt * tt;
          if (y > 0) continue;
          coins += `<ellipse cx="${x}" cy="${y}" rx="12" ry="10" fill="#F7CF4B" stroke="${OUT}" stroke-width="3"/>`;
        }
      }
      $('pigCoins').innerHTML = coins;
      setT(pig, S.pig.still ? 'translate(760,1414) scale(.8)' : 'translate(1210,1372)');
    } else disp(pig, false);
    // Leberwurst
    const sg = $('sausage');
    if (S.sausage && t >= S.sausage.t0 && t < S.sausage.gone + 0.2) {
      disp(sg, true);
      const s = popS(t, S.sausage.t0) * (1 - E.in(prog(t, S.sausage.gone - 0.05, 0.25)));
      setT(sg, `translate(${lerp(1190, 1120, prog(t, S.sausage.gone - 0.2, 0.25))},${1250 + Math.sin(t * 5) * 4}) scale(${0.6 * s}) rotate(10)`);
    } else disp(sg, false);
    // Fragezeichen
    const qm = $('qmarks');
    if (S.qmarks && t >= S.qmarks) {
      disp(qm, true);
      setT($('q1'), `translate(1020,${1000 + Math.sin(t * 5) * 6}) rotate(-14) scale(${popS(t, S.qmarks)})`);
      setT($('q2'), `translate(1180,${975 + Math.sin(t * 5 + 1) * 6}) rotate(12) scale(${popS(t, S.qmarks + 0.2)})`);
    } else disp(qm, false);
    // Gisela
    const g = S.gis;
    setT($('giselaW'), `translate(${g.x},${g.y}) scale(${g.s})`);
    poseHuman(G1, g, t);
    setT($('g1-scarfTail'), `rotate(${Math.sin(t * 5) * 6} 20 -165)`);
    // Waldi
    const ww = $('waldiW');
    if (S.waldi) {
      disp(ww, true);
      const w = S.waldi;
      setT(ww, `translate(${w.x},${w.y}) scale(${w.flip ? -w.s : w.s},${w.s})`);
      poseWaldi('w1', w, t);
    } else disp(ww, false);
  }

  function drawAlt(S, t) {
    const P = S.space;
    setT($('spaceCam'), `translate(540,960) scale(${P.z}) translate(${-P.f[0]},${-P.f[1]})`);
    disp($('homeLabel'), P.label);
    setT($('homeLabel'), `translate(0,-74) scale(${1 / Math.max(1, P.z / 1.6)})`);
    const mr = $('miniRocket');
    if (P.rocket !== null && P.rocket > 0) {
      disp(mr, true);
      const [x, y] = bez(Math.min(P.rocket, 0.999));
      const [x2, y2] = bez(Math.min(P.rocket + 0.01, 1));
      const ang = Math.atan2(y2 - y, x2 - x) * 180 / Math.PI + 90;
      setT(mr, `translate(${x},${y}) rotate(${ang})`);
      disp($('r2-flame'), true);
      setT($('r2-flame'), `scale(${0.8 + 0.2 * Math.sin(t * 40)},${1 + 0.3 * Math.sin(t * 30)})`);
    } else disp(mr, false);
    disp($('moonFlag'), P.moon); disp($('moonGisela'), P.moon);
    if (P.moon) poseHuman(G2, Object.assign(humanDefaults(), { armL: 155 + Math.sin(t * 9) * 8, armR: -155, expr: 'happy', talk: false, bounce: true }), t);
    for (const st of document.querySelectorAll('.star')) st.setAttribute('opacity', 0.35 + 0.65 * Math.abs(Math.sin(t * 1.5 + +st.dataset.p)));
  }

  Engine.start({
    world, alt, shots, drawWorld, drawAlt,
    baseState: base,
    highlight: '#FFD43B',
    confettiColors: ['#B98CFF', '#FFC83A', '#FF8A9A', '#5CC8FF', '#fff', '#7ED957'],
    preload: '👵🚀🛢️🍳⛽📏🧑‍🚀🐶💰⏰👀🗳️🪂😂🌕',
    ui: {
      profile: { name: 'Omas Mondmission', handle: '@omas.mondmission', avatar: '🚀', stat: 'Meter', foot: '1 Follower = 1 Meter höher 🚀' },
      comment: 'Oma, nimm mich mit! 🚀',
      banner: { small: 'WILLKOMMEN BEI', big: 'OMAS MONDMISSION' },
      stamp: { emo: '🚀', text: 'MISSION MOND!' },
      plusOne: '+1 METER 🚀',
      zirp: 'zirp …',
      ticket: `<div class="main"><div class="kicker">BORDKARTE</div><div class="title">MONDFLUG GS-1</div>
        <div class="grid"><div><small>VON</small><b>Parzelle 17</b></div><div><small>NACH</small><b>Mond 🌕</b></div>
        <div><small>NAME</small><b>DU</b></div><div><small>SITZ</small><b>1A</b></div></div>
        <div class="note">nur für Kommentierer · Tag 1</div></div>
        <div class="stub"><div class="emo">🚀</div><small>NR.</small><div class="big">001</div></div>`,
      tstamp: '✓ AN BORD<br>TAG 1',
      kasse: 'OMAS SPARSCHWEIN',
      cards: [
        { color: '#FFC83A', icon: chuteIcon, label: 'FALLSCHIRM' },
        { color: '#5CC8FF', icon: helmetIcon, label: 'RAUMHELM<br>FÜR WALDI' },
        { color: '#FF8A94', icon: qIcon, label: 'WAS<br>ANDERES' },
      ],
      floats: ['Fallschirm!! 🪂', 'Tag 2?! 👀', 'Go Oma! 🚀', 'Waldi 😂🐶'],
    },
  });
})();

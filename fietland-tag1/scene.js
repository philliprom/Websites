/* Fietland – Tag 1
 * Deterministische Szene: window.renderAt(t) zeichnet exakt den Frame zum Zeitpunkt t (Sekunden).
 * Alle Figuren und Requisiten sind eigenes Vektor-Artwork (SVG).
 */
(() => {
  const TL = window.TL;
  const $ = (id) => document.getElementById(id);
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const E = {
    out: (t) => 1 - Math.pow(1 - t, 3),
    in: (t) => t * t * t,
    inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    back: (t) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  };
  const prog = (t, a, d) => clamp((t - a) / d);
  const popS = (t, t0, d = 0.3) => (t < t0 ? 0 : E.back(prog(t, t0, d)));
  function rng(seed) {
    return () => {
      seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const SEGS = TL.segments;
  const byId = {};
  SEGS.forEach((s) => (byId[s.id] = s));
  const cue = (id, name, n = 0) => {
    const hits = byId[id].sfx.filter((x) => x[0] === name);
    return hits[n] ? hits[n][1] : byId[id].start;
  };
  const segAt = (t) => { let cur = SEGS[0]; for (const s of SEGS) if (t >= s.start - 1e-4) cur = s; return cur; };
  const envAt = (t) => TL.env[clamp(Math.floor(t * TL.fps), 0, TL.env.length - 1)] || 0;

  // ---------------------------------------------------------------- Farben
  const OUT = '#2B2240';
  const SKIN = '#F9CFAE', SKIN_SH = '#ECB08B';
  const HAIR = '#E2733A', HAIR_D = '#B4532A';
  const COAT = '#FFC83A', COAT_SH = '#EEA720';
  const NAVY = '#22305A', NAVY_D = '#18213F';
  const sw = `stroke="${OUT}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;

  // ---------------------------------------------------------------- Fiete
  const capMarkup = () => `
      <path d="M-72 -280 Q-76 -322 -60 -340 Q0 -358 60 -340 Q76 -322 72 -280 Z" fill="${NAVY}" ${sw}/>
      <path d="M-46 -338 Q0 -350 46 -338" stroke="#3B4D86" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M-75 -294 Q0 -304 75 -294 L75 -276 Q0 -286 -75 -276 Z" fill="${NAVY_D}" ${sw}/>
      <path d="M-62 -291 Q0 -300 62 -291" stroke="#F2C14E" stroke-width="3.5" fill="none"/>
      <path d="M-68 -280 Q0 -294 68 -280 Q62 -266 0 -268 Q-62 -266 -68 -280 Z" fill="#151A2A" ${sw}/>
      <path d="M-38 -281 Q0 -289 38 -281" stroke="#46506B" stroke-width="4" fill="none" stroke-linecap="round"/>
      <g transform="translate(0,-318)">
        <circle r="14" fill="#F2C14E" stroke="${OUT}" stroke-width="3"/>
        <path d="M0 -8 V8 M-7 3 Q0 11 7 3 M-5 -3 H5" stroke="${OUT}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
      </g>`;

  const armMarkup = (p, side) => `
      <path d="M-16 -8 Q-19 40 -14 74 L14 74 Q19 40 16 -8 Q0 -16 -16 -8 Z" fill="${COAT}" ${sw}/>
      <rect id="${p}-finger${side}" x="-5" y="94" width="10" height="26" rx="5" fill="${SKIN}" ${sw} style="display:none"/>
      <rect x="-17" y="66" width="34" height="13" rx="6" fill="${COAT_SH}" ${sw}/>
      <circle cx="0" cy="91" r="17" fill="${SKIN}" ${sw}/>`;

  const fieteMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="0" cy="4" rx="80" ry="13" fill="#0B2540" opacity=".2"/>
    <g id="${p}-bob">
      <rect x="-37" y="-68" width="27" height="42" rx="9" fill="#3A4A70" ${sw}/>
      <rect x="10" y="-68" width="27" height="42" rx="9" fill="#3A4A70" ${sw}/>
      <path d="M-50 0 L-6 0 L-6 -34 Q-6 -41 -13 -41 L-38 -41 Q-45 -41 -45 -34 L-45 -15 Q-52 -10 -50 0 Z" fill="#2C4E86" ${sw}/>
      <path d="M50 0 L6 0 L6 -34 Q6 -41 13 -41 L38 -41 Q45 -41 45 -34 L45 -15 Q52 -10 50 0 Z" fill="#2C4E86" ${sw}/>
      <g id="${p}-armL" transform="translate(-50,-160)">${armMarkup(p, 'L')}</g>
      <path d="M-42 -172 Q0 -150 42 -172 Q32 -190 0 -192 Q-32 -190 -42 -172 Z" fill="${COAT_SH}" ${sw}/>
      <path d="M-50 -172 Q-62 -118 -73 -60 Q0 -46 73 -60 Q62 -118 50 -172 Q0 -184 -50 -172 Z" fill="${COAT}" ${sw}/>
      <path d="M20 -176 Q42 -174 50 -170 Q61 -118 70 -62 Q50 -54 28 -52 Q38 -112 20 -176 Z" fill="${COAT_SH}" opacity=".75"/>
      <line x1="0" y1="-168" x2="0" y2="-52" stroke="${OUT}" stroke-width="4"/>
      <circle cx="11" cy="-146" r="5.5" fill="${NAVY}"/><circle cx="11" cy="-116" r="5.5" fill="${NAVY}"/><circle cx="11" cy="-86" r="5.5" fill="${NAVY}"/>
      <path d="M-58 -96 H-26 M26 -96 H58" stroke="${OUT}" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M-32 -180 L-4 -150 L-3 -178 Z" fill="${COAT}" ${sw}/>
      <path d="M32 -180 L4 -150 L3 -178 Z" fill="${COAT}" ${sw}/>
      <g id="${p}-armR" transform="translate(50,-160)">${armMarkup(p, 'R')}</g>
      <g id="${p}-head">
        <ellipse cx="-75" cy="-228" rx="14" ry="18" fill="${SKIN}" ${sw}/>
        <ellipse cx="75" cy="-228" rx="14" ry="18" fill="${SKIN}" ${sw}/>
        <ellipse cx="0" cy="-234" rx="77" ry="75" fill="${SKIN}" ${sw}/>
        <path d="M40 -170 Q70 -190 74 -230 Q76 -200 60 -178 Q50 -168 40 -170 Z" fill="${SKIN_SH}" opacity=".55"/>
        <path d="M-80 -282 Q-98 -252 -82 -226 Q-80 -246 -66 -262 Q-76 -250 -70 -236 Q-62 -262 -58 -280 Z" fill="${HAIR}" ${sw}/>
        <path d="M80 -282 Q98 -252 82 -226 Q80 -246 66 -262 Q76 -250 70 -236 Q62 -262 58 -280 Z" fill="${HAIR}" ${sw}/>
        <g id="${p}-hairTop" style="display:none">
          <path d="M-74 -262 Q-84 -318 -40 -330 Q-30 -352 0 -340 Q26 -360 44 -332 Q86 -322 74 -262 Q60 -290 40 -282 Q30 -300 10 -286 Q-6 -304 -22 -284 Q-44 -298 -56 -276 Q-66 -276 -74 -262 Z" fill="${HAIR}" ${sw}/>
        </g>
        <ellipse cx="-47" cy="-197" rx="15" ry="9" fill="#FF7E86" opacity=".55"/>
        <ellipse cx="47" cy="-197" rx="15" ry="9" fill="#FF7E86" opacity=".55"/>
        <g fill="${HAIR_D}" opacity=".55">
          <circle cx="-55" cy="-210" r="3"/><circle cx="-45" cy="-214" r="3"/><circle cx="-37" cy="-207" r="3"/>
          <circle cx="55" cy="-210" r="3"/><circle cx="45" cy="-214" r="3"/><circle cx="37" cy="-207" r="3"/>
        </g>
        <g id="${p}-eyes">
          <g id="${p}-eyeL" transform="translate(-27,-228)">
            <ellipse rx="21" ry="25" fill="#fff" stroke="${OUT}" stroke-width="4.5"/>
            <g id="${p}-pupL"><circle r="11.5" fill="${OUT}"/><circle cx="4" cy="-5" r="4.2" fill="#fff"/></g>
          </g>
          <g id="${p}-eyeR" transform="translate(27,-228)">
            <ellipse rx="21" ry="25" fill="#fff" stroke="${OUT}" stroke-width="4.5"/>
            <g id="${p}-pupR"><circle r="11.5" fill="${OUT}"/><circle cx="4" cy="-5" r="4.2" fill="#fff"/></g>
          </g>
        </g>
        <g id="${p}-happy" style="display:none" fill="none" stroke="${OUT}" stroke-width="6.5" stroke-linecap="round">
          <path d="M-45 -224 Q-27 -246 -9 -224"/><path d="M9 -224 Q27 -246 45 -224"/>
        </g>
        <path id="${p}-browL" d="M-42 -262 Q-27 -269 -12 -262" stroke="${HAIR_D}" stroke-width="7.5" fill="none" stroke-linecap="round"/>
        <path id="${p}-browR" d="M12 -262 Q27 -269 42 -262" stroke="${HAIR_D}" stroke-width="7.5" fill="none" stroke-linecap="round"/>
        <path d="M-7 -205 Q0 -197 7 -205" stroke="${SKIN_SH}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path id="${p}-mSmile" d="M-24 -185 Q0 -166 24 -185" stroke="${OUT}" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path id="${p}-mFrown" d="M-17 -176 Q0 -188 17 -176" stroke="${OUT}" stroke-width="5.5" fill="none" stroke-linecap="round" style="display:none"/>
        <g id="${p}-mOpen" transform="translate(0,-186)" style="display:none">
          <path d="M-24 0 Q0 4 24 0 Q22 30 0 32 Q-22 30 -24 0 Z" fill="#7A2633" ${sw}/>
          <path d="M-13 21 Q0 12 13 21 Q9 30 0 30 Q-9 30 -13 21 Z" fill="#FF7B8A"/>
          <path d="M-18 3 Q0 6 18 3 L16 9 Q0 11 -16 9 Z" fill="#fff"/>
        </g>
        <ellipse id="${p}-mO" cx="0" cy="-180" rx="12" ry="15" fill="#7A2633" ${sw} style="display:none"/>
        <g id="${p}-cap">${capMarkup()}</g>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Jürgen (Möwe)
  const jurgenMarkup = (p) => `
  <g id="${p}">
    <ellipse cx="0" cy="3" rx="48" ry="9" fill="#0B2540" opacity=".2"/>
    <g id="${p}-bob">
      <path d="M-12 -32 L-14 -2 M12 -32 L14 -2" stroke="#F08A2E" stroke-width="7" stroke-linecap="round"/>
      <path d="M-32 0 L-14 -4 L-2 0 Z M2 0 L14 -4 L30 0 Z" fill="#F08A2E" stroke="${OUT}" stroke-width="3" stroke-linejoin="round"/>
      <path d="M28 -68 L86 -84 L78 -50 Z" fill="#B8C2CF" ${sw}/>
      <path d="M70 -80 L86 -84 L82 -64 Z" fill="${OUT}"/>
      <ellipse cx="0" cy="-64" rx="50" ry="41" fill="#FBFBFD" ${sw}/>
      <path d="M-34 -40 Q0 -20 36 -40 Q20 -26 0 -25 Q-20 -26 -34 -40 Z" fill="#E4E9F0"/>
      <g id="${p}-wing" transform="translate(4,-86)">
        <path d="M-8 0 Q42 -16 70 18 Q50 44 6 36 Q-14 18 -8 0 Z" fill="#B8C2CF" ${sw}/>
        <path d="M46 8 Q62 12 70 18 Q60 30 48 32 Q54 20 46 8 Z" fill="${OUT}"/>
      </g>
      <g transform="translate(-22,-92)">
        <path d="M-7 0 L7 0 L5 9 L-5 9 Z" fill="#E23A4E" stroke="${OUT}" stroke-width="2.8" stroke-linejoin="round"/>
        <path d="M-5 9 L5 9 L9 36 L0 45 L-9 36 Z" fill="#E23A4E" stroke="${OUT}" stroke-width="2.8" stroke-linejoin="round"/>
      </g>
      <g id="${p}-head">
        <circle cx="-14" cy="-118" r="34" fill="#FBFBFD" ${sw}/>
        <path d="M-44 -122 L-90 -114 Q-97 -108 -88 -104 L-44 -106 Z" fill="#FFC53D" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/>
        <g id="${p}-jaw" transform="translate(-44,-106)">
          <path d="M0 0 L-42 1 Q-32 12 0 9 Z" fill="#F2A928" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/>
          <circle cx="-31" cy="4" r="4.5" fill="#E23A4E"/>
        </g>
        <g id="${p}-eyeN">
          <circle cx="-25" cy="-127" r="11.5" fill="#fff" stroke="${OUT}" stroke-width="3.5"/>
          <circle id="${p}-pup" cx="-28" cy="-125" r="5.8" fill="${OUT}"/>
          <path id="${p}-lid" d="M-37 -124 L-13 -131 Q-17 -141 -26 -140 Q-36 -138 -37 -124 Z" fill="#D9DFE7" stroke="${OUT}" stroke-width="3" stroke-linejoin="round"/>
        </g>
        <text id="${p}-euro" x="-25" y="-113" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="34" fill="#2DBE60" stroke="${OUT}" stroke-width="3" paint-order="stroke" style="display:none">€</text>
        <path d="M-42 -142 L-12 -134" stroke="${OUT}" stroke-width="5.5" stroke-linecap="round"/>
        <g id="${p}-cap" transform="translate(-12,-140) scale(.5) translate(0,300)" style="display:none">${capMarkup()}</g>
      </g>
    </g>
  </g>`;

  // ---------------------------------------------------------------- Requisiten
  const palmMarkup = () => {
    const leaf = (rot, len, flip) => `
      <g transform="${flip ? 'scale(-1,1) ' : ''}rotate(${rot})">
        <path d="M0 0 C${len * 0.3} ${-len * 0.36} ${len * 0.72} ${-len * 0.3} ${len} ${len * 0.16} C${len * 0.66} ${-len * 0.04} ${len * 0.3} ${-len * 0.06} 0 0 Z" fill="#3FB35C" ${sw}/>
        <path d="M6 -2 C${len * 0.35} ${-len * 0.2} ${len * 0.7} ${-len * 0.16} ${len * 0.94} ${len * 0.1}" stroke="#2A8A45" stroke-width="4" fill="none" stroke-linecap="round"/>
      </g>`;
    return `
      <path d="M-16 0 Q-34 -160 -40 -338 L-16 -338 Q-12 -160 16 0 Z" fill="#B47A45" ${sw}/>
      ${[-40, -90, -140, -190, -240, -290].map((y, i) => `<path d="M${-22 - i * 2.6} ${y} q14 8 ${26 - i} 0" stroke="#8C5A30" stroke-width="4" fill="none" stroke-linecap="round"/>`).join('')}
      <g id="palmTag" transform="translate(-14,-150)" style="display:none">
        <line x1="0" y1="0" x2="18" y2="18" stroke="${OUT}" stroke-width="3"/>
        <g transform="translate(16,16) rotate(14)">
          <rect x="0" y="0" width="118" height="46" rx="8" fill="#fff" ${sw}/>
          <text x="59" y="33" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" fill="#E8243B">PLASTIK</text>
        </g>
      </g>
      <g id="palmTop" transform="translate(-28,-340)">
        ${leaf(-38, 170, false)}${leaf(-2, 190, false)}${leaf(34, 150, false)}
        ${leaf(-38, 170, true)}${leaf(-2, 190, true)}${leaf(34, 150, true)}
        ${leaf(-88, 120, false)}
        <circle cx="-12" cy="12" r="15" fill="#7A4A26" ${sw}/><circle cx="12" cy="14" r="15" fill="#7A4A26" ${sw}/><circle cx="0" cy="28" r="14" fill="#6A3E1F" ${sw}/>
      </g>`;
  };

  const korbMarkup = () => `
      <path d="M-106 -118 L-106 -222 Q-106 -276 0 -276 Q106 -276 106 -222 L106 -118 Z" fill="#EAD5A6" ${sw}/>
      <path d="M-82 -122 L-82 -214 Q-82 -248 0 -248 Q82 -248 82 -214 L82 -122 Z" fill="url(#korbStripes)" ${sw}/>
      <rect x="-104" y="-122" width="208" height="122" rx="10" fill="#EAD5A6" ${sw}/>
      ${[-100, -82, -64, -46, -28].map((y) => `<line x1="-96" y1="${y}" x2="96" y2="${y}" stroke="#CDAE73" stroke-width="4"/>`).join('')}
      <rect x="-84" y="-136" width="168" height="28" rx="10" fill="#2F80D1" ${sw}/>
      <rect x="-118" y="-150" width="30" height="62" rx="8" fill="#D9BC84" ${sw}/>
      <rect x="88" y="-150" width="30" height="62" rx="8" fill="#D9BC84" ${sw}/>
      <path d="M-106 -222 Q-106 -276 0 -276 Q106 -276 106 -222" stroke="#2F80D1" stroke-width="12" fill="none"/>
      <path d="M-106 -222 Q-106 -276 0 -276 Q106 -276 106 -222" stroke="${OUT}" stroke-width="5" fill="none"/>`;

  const signMarkup = () => `
      <rect x="-9" y="-170" width="18" height="172" rx="6" fill="#8C5A30" ${sw}/>
      <g transform="rotate(-4 0 -150)">
        <rect x="-118" y="-214" width="236" height="104" rx="14" fill="#C98B4F" ${sw}/>
        <text x="0" y="-170" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="40" fill="#4A2A12">FIETLAND</text>
        <text id="signCount" x="0" y="-128" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" fill="#4A2A12">EINWOHNER: 0</text>
      </g>`;

  const ferryMarkup = () => `
      <path d="M-290 -66 L290 -66 L256 12 L-246 12 Z" fill="#fff" ${sw}/>
      <path d="M-282 -46 L282 -46 L276 -30 L-276 -30 Z" fill="#E2374B"/>
      <path d="M-252 -4 L262 -4 L256 12 L-246 12 Z" fill="${NAVY}"/>
      <path d="M-290 -66 L290 -66 L256 12 L-246 12 Z" fill="none" ${sw}/>
      <text x="-170" y="-50" font-family="Fredoka" font-weight="700" font-size="22" fill="${NAVY}" text-anchor="middle">MS MOIN</text>
      <rect x="-150" y="-158" width="270" height="94" rx="14" fill="#fff" ${sw}/>
      ${[-128, -78, -28, 22, 72].map((x) => `<rect x="${x}" y="-140" width="36" height="34" rx="8" fill="#8FD0F5" stroke="${OUT}" stroke-width="4"/>`).join('')}
      <rect x="-60" y="-212" width="150" height="56" rx="12" fill="#fff" ${sw}/>
      <rect x="-44" y="-200" width="118" height="26" rx="7" fill="#8FD0F5" stroke="${OUT}" stroke-width="4"/>
      <rect x="96" y="-252" width="44" height="76" rx="6" fill="#E2374B" ${sw}/>
      <rect x="96" y="-252" width="44" height="18" rx="5" fill="${OUT}"/>
      <path d="M-280 -80 H-160 M-280 -66 V-80 M-250 -66 V-80 M-220 -66 V-80 M-190 -66 V-80" stroke="${OUT}" stroke-width="4" stroke-linecap="round"/>`;

  const duckMarkup = () => `
      <ellipse cx="0" cy="-22" rx="44" ry="26" fill="#FFD43B" ${sw}/>
      <path d="M30 -34 Q52 -50 48 -22" fill="#FFD43B" ${sw}/>
      <circle cx="-26" cy="-60" r="23" fill="#FFD43B" ${sw}/>
      <path d="M-46 -58 L-70 -54 Q-72 -46 -62 -46 L-44 -50 Z" fill="#F08A2E" stroke="${OUT}" stroke-width="4" stroke-linejoin="round"/>
      <circle cx="-32" cy="-66" r="4.5" fill="${OUT}"/>
      <path d="M-8 -26 Q8 -12 24 -24" stroke="#E9B521" stroke-width="5" fill="none" stroke-linecap="round"/>`;

  const fishbunMarkup = () => `
      <path d="M-64 6 Q-60 34 0 36 Q60 34 64 6 Z" fill="#E7A85C" ${sw}/>
      <path d="M-70 4 Q-50 -10 -30 2 Q-10 -12 10 2 Q30 -12 50 2 Q62 -6 70 4" stroke="#57B947" stroke-width="10" fill="none" stroke-linecap="round"/>
      <path d="M-74 -6 Q-30 -26 40 -12 L78 -26 L72 -2 L80 14 L42 0 Q-30 12 -74 -6 Z" fill="#C3CFDA" ${sw}/>
      <circle cx="-56" cy="-8" r="3.5" fill="${OUT}"/>
      <path d="M-62 -14 Q-60 -54 0 -56 Q60 -54 62 -14 Z" fill="#F0B465" ${sw}/>
      <g fill="#FFF3D6"><ellipse cx="-24" cy="-40" rx="4" ry="2.5"/><ellipse cx="6" cy="-46" rx="4" ry="2.5"/><ellipse cx="30" cy="-36" rx="4" ry="2.5"/></g>`;

  const chestMarkup = () => `
      <rect x="-62" y="-62" width="124" height="62" rx="8" fill="#A0632F" ${sw}/>
      <rect x="-62" y="-40" width="124" height="10" fill="#F2C14E"/>
      <rect x="-40" y="-62" width="12" height="62" fill="#F2C14E"/><rect x="28" y="-62" width="12" height="62" fill="#F2C14E"/>
      <rect x="-62" y="-62" width="124" height="62" rx="8" fill="none" ${sw}/>
      <g id="coins"></g>
      <g id="chestLid" transform="translate(0,-62)">
        <path d="M-66 0 Q-66 -46 0 -48 Q66 -46 66 0 Z" fill="#B9773A" ${sw}/>
        <rect x="-40" y="-46" width="12" height="46" fill="#F2C14E"/><rect x="28" y="-46" width="12" height="46" fill="#F2C14E"/>
        <path d="M-66 0 Q-66 -46 0 -48 Q66 -46 66 0 Z" fill="none" ${sw}/>
        <rect x="-12" y="-10" width="24" height="24" rx="5" fill="#F2C14E" ${sw}/>
      </g>`;

  const ghostMarkup = () => `
      <ellipse cx="0" cy="2" rx="62" ry="16" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="12 10"/>
      <g id="ghostBody">
        <rect x="-30" y="-92" width="60" height="92" rx="28" fill="#6CC6FF" ${sw}/>
        <circle cx="0" cy="-124" r="36" fill="#FFE0C7" ${sw}/>
        <circle cx="-12" cy="-128" r="5" fill="${OUT}"/><circle cx="12" cy="-128" r="5" fill="${OUT}"/>
        <path d="M-12 -112 Q0 -102 12 -112" stroke="${OUT}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
        <path id="ghostArm" d="M26 -70 L52 -110" stroke="#6CC6FF" stroke-width="18" stroke-linecap="round"/>
      </g>
      <g id="ghostArrow"><path d="M-22 -230 H22 V-262 H-22 Z M-40 -230 L0 -190 L40 -230 Z" fill="#FFC83A" ${sw}/></g>`;

  // ---------------------------------------------------------------- Welt
  function worldMarkup() {
    const r = rng(7);
    const clouds = [[200, 300, 1.2], [760, 180, 0.9], [1420, 260, 1.4], [2050, 160, 1.0], [2700, 300, 1.2], [-400, 120, 1.0]]
      .map(([x, y, s], i) => `<g id="cloud${i}" data-x="${x}" data-y="${y}" data-s="${s}">
        <g fill="#fff" opacity=".93"><ellipse cx="0" cy="0" rx="120" ry="44"/><circle cx="-50" cy="-22" r="48"/><circle cx="20" cy="-44" r="62"/><circle cx="76" cy="-14" r="44"/></g></g>`).join('');
    const turbines = [[1960, 762, 1], [2140, 766, 0.85], [2300, 760, 0.95], [-120, 764, 0.8]]
      .map(([x, y, s], i) => `<g transform="translate(${x},${y}) scale(${s})" opacity=".75">
        <path d="M-4 0 L-2 -130 L2 -130 L4 0 Z" fill="#fff"/>
        <g id="turb${i}" transform="translate(0,-130)"><circle r="6" fill="#fff"/>
          ${[0, 120, 240].map((a) => `<path transform="rotate(${a})" d="M-3 0 L0 -70 L3 0 Z" fill="#fff"/>`).join('')}
        </g></g>`).join('');
    let shells = '';
    for (let i = 0; i < 10; i++) {
      const a = r() * Math.PI * 2, d = 0.3 + r() * 0.6;
      shells += `<ellipse cx="${1200 + Math.cos(a) * 340 * d}" cy="${1322 + Math.sin(a) * 80 * d}" rx="${5 + r() * 4}" ry="${3 + r() * 2}" fill="${r() > 0.5 ? '#fff' : '#F7B9A8'}" opacity=".9"/>`;
    }
    return `
    <defs>
      <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#5DAEF0"/><stop offset=".55" stop-color="#A6D6F8"/><stop offset="1" stop-color="#FFE2C6"/>
      </linearGradient>
      <linearGradient id="gSea" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#7FD3EE"/><stop offset=".06" stop-color="#43B4E4"/><stop offset=".3" stop-color="#2393D2"/><stop offset="1" stop-color="#135892"/>
      </linearGradient>
      <radialGradient id="gSun"><stop offset="0" stop-color="#FFF7D0"/><stop offset=".3" stop-color="#FFE58F" stop-opacity=".9"/><stop offset="1" stop-color="#FFE58F" stop-opacity="0"/></radialGradient>
      <radialGradient id="gSand" cx=".42" cy=".3" r=".75"><stop offset="0" stop-color="#FCEBC0"/><stop offset="1" stop-color="#EBC488"/></radialGradient>
      <pattern id="korbStripes" width="30" height="10" patternUnits="userSpaceOnUse"><rect width="15" height="10" fill="#2F80D1"/><rect x="15" width="15" height="10" fill="#fff"/></pattern>
    </defs>
    <rect x="-1500" y="-2600" width="5200" height="3364" fill="url(#gSky)"/>
    <circle cx="1720" cy="470" r="280" fill="url(#gSun)"/>
    <circle cx="1720" cy="470" r="74" fill="#FFF3C0"/>
    <g id="clouds">${clouds}</g>
    <g transform="translate(330,762)">
      <ellipse cx="0" cy="0" rx="70" ry="14" fill="#5D7186"/>
      <path d="M-18 -4 L-12 -120 L12 -120 L18 -4 Z" fill="#fff"/>
      <path d="M-16 -36 L16 -36 L15 -56 L-15 -56 Z M-14 -78 L14 -78 L13 -98 L-13 -98 Z" fill="#E2374B"/>
      <rect x="-14" y="-140" width="28" height="22" fill="#FFE07A"/><path d="M-20 -140 L0 -160 L20 -140 Z" fill="#E2374B"/>
    </g>
    ${turbines}
    <rect x="-1500" y="758" width="5200" height="3200" fill="url(#gSea)"/>
    <rect x="-1500" y="756" width="5200" height="6" fill="#E9F7FF" opacity=".7"/>
    <g id="waves" fill="none" stroke="#fff" stroke-linecap="round"></g>
    <g id="ferry" transform="translate(3000,1272)">${ferryMarkup()}</g>
    <g id="island">
      <ellipse id="foam" cx="1200" cy="1332" rx="458" ry="134" fill="none" stroke="#fff" stroke-width="12" opacity=".6"/>
      <ellipse id="wet" cx="1200" cy="1332" rx="432" ry="122" fill="#D6AC6A"/>
      <ellipse id="sand" cx="1200" cy="1320" rx="404" ry="106" fill="url(#gSand)" stroke="#C99A55" stroke-width="4"/>
      <g id="shells">${shells}</g>
    </g>
    <g id="pier">
      ${[1640, 1760, 1880, 1975].map((x) => `<rect x="${x}" y="1300" width="20" height="70" fill="#7A4E2A" stroke="${OUT}" stroke-width="4"/>`).join('')}
      <rect x="1560" y="1290" width="440" height="30" rx="4" fill="#C08A52" ${sw}/>
      ${[1620, 1680, 1740, 1800, 1860, 1920].map((x) => `<line x1="${x}" y1="1292" x2="${x}" y2="1318" stroke="#8C5A30" stroke-width="3"/>`).join('')}
    </g>
    <g id="flagpole">
      <rect x="1288" y="1286" width="28" height="14" rx="4" fill="#7B8696" ${sw}/>
      <line x1="1302" y1="1290" x2="1302" y2="930" stroke="#9AA6B5" stroke-width="9"/>
      <line x1="1302" y1="1290" x2="1302" y2="930" stroke="${OUT}" stroke-width="2" opacity=".5"/>
      <circle cx="1302" cy="924" r="11" fill="#F2C14E" stroke="${OUT}" stroke-width="4"/>
    </g>
    <g id="palm" transform="translate(1000,1318)">${palmMarkup()}</g>
    <g id="korb" transform="translate(1430,1326)">${korbMarkup()}</g>
    <g id="sign" transform="translate(860,1352)">${signMarkup()}</g>
    <g id="ripples" fill="none" stroke="#fff" stroke-width="6" opacity="0"></g>
    <g id="ghost" transform="translate(1040,1350)" style="display:none">${ghostMarkup()}</g>
    <g id="chest" transform="translate(1310,1360)" style="display:none">${chestMarkup()}</g>
    <g id="fieteW" transform="translate(1170,1338)">${fieteMarkup('f1')}</g>
    <g id="jurgenW" style="display:none">${jurgenMarkup('j1')}</g>
    <g id="duck" style="display:none">${duckMarkup()}</g>
    <g id="fishbun" style="display:none">${fishbunMarkup()}</g>
    <g id="puff"></g>
    <g id="qmarks" font-family="Fredoka" font-weight="700" font-size="70" fill="#fff" stroke="${OUT}" stroke-width="8" paint-order="stroke" style="display:none">
      <text id="q1" x="0" y="0">?</text><text id="q2" x="0" y="0">?</text>
    </g>`;
  }

  // ---------------------------------------------------------------- Globus
  function globeMarkup() {
    const r = rng(42);
    let stars = '';
    for (let i = 0; i < 140; i++) stars += `<circle class="star" cx="${r() * 1080}" cy="${r() * 1920}" r="${1 + r() * 3}" fill="#fff" data-p="${r() * 6}"/>`;
    const cont = `
      <path d="M-700 -220 Q-640 -320 -520 -300 Q-430 -250 -470 -150 Q-520 -60 -600 -90 Q-680 -120 -700 -220 Z"/>
      <path d="M-560 -40 Q-480 -60 -440 20 Q-420 140 -500 260 Q-560 300 -580 200 Q-600 80 -560 -40 Z"/>
      <path d="M-260 -300 Q-160 -340 -40 -310 Q40 -260 -20 -200 Q-80 -170 -60 -110 Q-120 -60 -200 -120 Q-300 -200 -260 -300 Z"/>
      <path d="M-160 -40 Q-40 -60 0 40 Q20 180 -80 280 Q-160 260 -170 140 Q-200 40 -160 -40 Z"/>
      <path d="M120 -280 Q300 -330 480 -260 Q560 -180 460 -120 Q380 -80 300 -130 Q200 -100 160 -170 Q90 -220 120 -280 Z"/>
      <path d="M380 60 Q480 40 540 120 Q520 200 430 200 Q360 170 380 60 Z"/>
      <path d="M640 -160 Q720 -200 780 -120 Q760 -40 690 -60 Q620 -90 640 -160 Z"/>`;
    return `
    <defs>
      <radialGradient id="gSpace" cx=".5" cy=".55" r=".8"><stop offset="0" stop-color="#2E2A78"/><stop offset="1" stop-color="#0E1233"/></radialGradient>
      <radialGradient id="gOcean" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#5EC1FF"/><stop offset="1" stop-color="#1C6FC4"/></radialGradient>
      <radialGradient id="gShade" cx=".35" cy=".3" r=".85"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#0A1035" stop-opacity=".55"/></radialGradient>
      <clipPath id="clipGlobe"><circle r="400"/></clipPath>
    </defs>
    <rect width="1080" height="1920" fill="url(#gSpace)"/>
    <g id="stars">${stars}</g>
    <g id="globeCam">
      <circle r="452" fill="#6FC3FF" opacity=".16"/>
      <circle r="426" fill="#6FC3FF" opacity=".18"/>
      <circle r="400" fill="url(#gOcean)"/>
      <g clip-path="url(#clipGlobe)">
        <g id="continents" fill="#7ED957" stroke="#4FA83A" stroke-width="8" stroke-linejoin="round">
          <g>${cont}</g><g transform="translate(1600,0)">${cont}</g><g transform="translate(-1600,0)">${cont}</g>
        </g>
      </g>
      <circle r="400" fill="url(#gShade)"/>
      <circle r="400" fill="none" stroke="${OUT}" stroke-width="9"/>
      <g id="gIsland" transform="translate(70,-60)">
        <circle id="gRing" r="40" fill="none" stroke="#FFC83A" stroke-width="5" stroke-dasharray="10 8"/>
        <ellipse rx="9" ry="4" fill="#F3D9A0" stroke="${OUT}" stroke-width="1.5"/>
        <path d="M-1 -1 Q-2 -8 -3 -12" stroke="#8C5A30" stroke-width="1.6" fill="none"/>
        <path d="M-3 -12 l-6 2 M-3 -12 l6 2 M-3 -12 l-4 -3 M-3 -12 l4 -3" stroke="#3FB35C" stroke-width="2" fill="none" stroke-linecap="round"/>
        <g id="gLabel" transform="translate(0,-60)">
          <rect x="-128" y="-26" width="256" height="44" rx="22" fill="#fff" stroke="${OUT}" stroke-width="4"/>
          <text x="0" y="6" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="24" fill="${NAVY}">FIETLAND · 12 m²</text>
        </g>
      </g>
      <g id="pins"></g>
      <g id="fieteG" transform="translate(0,-398) scale(.62)">${fieteMarkup('f2')}</g>
    </g>`;
  }

  // ---------------------------------------------------------------- UI
  const flagIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><line x1="30" y1="12" x2="30" y2="112" stroke="${OUT}" stroke-width="8" stroke-linecap="round"/>
    <path d="M34 16 Q60 6 78 18 Q94 28 108 20 L108 66 Q94 74 78 64 Q60 52 34 62 Z" fill="#FFC83A" stroke="${OUT}" stroke-width="6" stroke-linejoin="round"/>
    <path d="M60 28 V54 M52 48 Q60 58 68 48 M55 34 H65" stroke="${NAVY}" stroke-width="4" fill="none" stroke-linecap="round"/></svg>`;
  const korbIcon = `<svg width="128" height="120" viewBox="-128 -290 256 296">${korbMarkup()}
    <g transform="translate(14,-118) scale(.8)">${jurgenMarkup('jc')}</g></svg>`;
  const qIcon = `<svg width="120" height="120" viewBox="0 0 120 120"><text x="60" y="100" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="112" fill="#FF4B5C" stroke="${OUT}" stroke-width="7" paint-order="stroke">?</text></svg>`;
  const emblem = `<svg width="230" height="230" viewBox="-115 -115 230 230">
    <circle r="100" fill="none" stroke="#F6CF6B" stroke-width="8"/><circle r="84" fill="none" stroke="#F6CF6B" stroke-width="3"/>
    <path d="M0 -58 V54 M-36 22 Q0 70 36 22 M-22 -26 H22" stroke="#F6CF6B" stroke-width="11" fill="none" stroke-linecap="round"/>
    <circle cy="-66" r="13" fill="none" stroke="#F6CF6B" stroke-width="8"/>
    <path d="M-70 -10 Q-86 -40 -64 -64 M70 -10 Q86 -40 64 -64" stroke="#F6CF6B" stroke-width="7" fill="none" stroke-linecap="round"/></svg>`;

  function uiMarkup() {
    return `
    <div id="title" class="ui badge">TAG 1</div>
    <div id="badge" class="ui badge">TAG 1</div>
    <div id="chip" class="ui chip"></div>
    <div id="chip2" class="ui chip"></div>
    <div id="plaetscher" class="ui chip green small">plätscher …</div>
    <div id="plusOne" class="ui chip green">+1 EINWOHNER</div>
    <div id="stamp" class="ui"><span class="emo">🏝️</span>GEGRÜNDET!</div>
    <div id="banner" class="ui"><span>WILLKOMMEN IN</span><b>FIETLAND</b></div>
    <div id="profile" class="ui">
      <div class="top"><div><div class="name">Fietland</div><div class="handle">@fietland · Republik</div></div><div class="avatar"><div>🏝️</div></div></div>
      <div class="stats"><div><b id="stF">0</b><span>Follower</span></div><div><b id="stE">0</b><span>Einwohner</span></div><div><b id="stL">0</b><span>Likes</span></div></div>
      <div class="btns"><div id="btnFollow" class="btn follow">Folgen</div><div class="btn">Nachricht</div></div>
      <div class="foot">1 Follower = 1 Einwohner 🏝️</div>
    </div>
    <div id="hand" class="ui emo">👆</div>
    <div id="comment" class="ui"><div class="av">D</div><div><div class="meta"><b>du</b> · gerade eben<i>TAG 1</i></div><div class="txt">Tag 1! Ich zieh ein 🏝️❤️</div></div><div class="heart">♡</div></div>
    <div id="passport" class="ui"><div class="l1">REPUBLIK</div><div class="l2">FIETLAND</div>${emblem}<div class="l3">GRÜNDER-REISEPASS</div>
      <div class="l4">Nr. 001 · Tag 1</div><div class="l5">nur für Kommentierer</div></div>
    <div id="pstamp" class="ui">✓ GRÜNDER<br>TAG 1</div>
    <div id="list" class="ui"><div class="clip"></div><div class="paper"><h3>EINWOHNERLISTE</h3>
      <div class="row first"><div id="listMark" class="mark"></div><span>1. DU ✨</span></div>
      <div class="row empty"><span>2. …</span></div><div class="row empty"><span>3. …</span></div><div class="row empty"><span>4. …</span></div></div></div>
    <div id="kasse" class="ui"><small>STAATSKASSE</small><b id="kasseVal">0 €</b></div>
    <div id="cardA" class="ui card"><div class="letter" style="background:#FFC83A">A</div>${flagIcon}<div class="lab">FLAGGE</div><div class="likes">❤️ <span id="likesA">0</span></div></div>
    <div id="cardB" class="ui card"><div class="letter" style="background:#5CC8FF">B</div>${korbIcon}<div class="lab">STRANDKORB<br>FÜR JÜRGEN</div><div class="likes">❤️ <span id="likesB">0</span></div></div>
    <div id="cardC" class="ui card"><div class="letter" style="background:#FF8A94">C</div>${qIcon}<div class="lab">WAS<br>ANDERES</div><div class="likes">❤️ <span id="likesC">0</span></div></div>
    <div id="votePill" class="ui chip red">💬 STIMM IN DEN KOMMENTAREN AB!</div>
    <div id="floaters"></div>`;
  }

  // ---------------------------------------------------------------- Aufbau
  $('cam').innerHTML = worldMarkup();
  $('globe').innerHTML = globeMarkup();
  $('ui').innerHTML = uiMarkup();

  const FLOAT_TEXTS = ['Flagge!! 🚩', 'Tag 2?! 👀', 'Ich zieh ein! 🏝️', 'Jürgen 😂🐦'];
  const floaters = [];
  for (let i = 0; i < 4; i++) {
    const d = document.createElement('div');
    d.className = 'ui floater bubble';
    d.textContent = FLOAT_TEXTS[i];
    $('floaters').appendChild(d);
    floaters.push(d);
  }
  const hearts = [];
  for (let i = 0; i < 16; i++) {
    const d = document.createElement('div');
    d.className = 'ui floater heartf';
    d.textContent = ['❤️', '🩷', '❤️', '💬'][i % 4];
    $('floaters').appendChild(d);
    hearts.push(d);
  }

  const q = (id) => document.getElementById(id);
  const fieteEls = (p) => ({
    root: q(p), bob: q(`${p}-bob`), armL: q(`${p}-armL`), armR: q(`${p}-armR`), head: q(`${p}-head`),
    eyes: q(`${p}-eyes`), eyeL: q(`${p}-eyeL`), eyeR: q(`${p}-eyeR`), pupL: q(`${p}-pupL`), pupR: q(`${p}-pupR`),
    happy: q(`${p}-happy`), browL: q(`${p}-browL`), browR: q(`${p}-browR`), mSmile: q(`${p}-mSmile`), mFrown: q(`${p}-mFrown`),
    mOpen: q(`${p}-mOpen`), mO: q(`${p}-mO`), cap: q(`${p}-cap`), hairTop: q(`${p}-hairTop`),
    fingerL: q(`${p}-fingerL`), fingerR: q(`${p}-fingerR`),
  });
  const F1 = fieteEls('f1'), F2 = fieteEls('f2');
  const jEls = (p) => ({ bob: q(`${p}-bob`), wing: q(`${p}-wing`), jaw: q(`${p}-jaw`), head: q(`${p}-head`), pup: q(`${p}-pup`),
    lid: q(`${p}-lid`), euro: q(`${p}-euro`), eyeN: q(`${p}-eyeN`), cap: q(`${p}-cap`) });
  const J1 = jEls('j1');

  // Wellenkämme (fest verteilt, deterministisch)
  const crestR = rng(3);
  const crests = [];
  for (let i = 0; i < 150; i++) {
    const y = 780 + Math.pow(crestR(), 1.6) * 1500;
    const depth = (y - 760) / 1500;
    crests.push({ x: -500 + crestR() * 3400, y, s: 10 + depth * 60, ph: crestR() * 6.28, sp: 0.6 + crestR() * 0.8, w: 2 + depth * 6 });
  }

  const pins = [];
  const pinR = rng(11);
  for (let i = 0; i < 18; i++) {
    const a = pinR() * Math.PI * 2, d = Math.sqrt(pinR()) * 330;
    pins.push({ x: Math.cos(a) * d, y: Math.sin(a) * d * 0.95, t: pinR() });
  }
  pins.sort((a, b) => a.t - b.t);
  $('pins').innerHTML = pins.map((p, i) => `<g id="pin${i}" transform="translate(${p.x},${p.y})" style="display:none">
      <g class="pinI"><path d="M0 0 Q-20 -30 -20 -46 A20 20 0 1 1 20 -46 Q20 -30 0 0 Z" fill="#FF4B5C" stroke="${OUT}" stroke-width="5"/><circle cy="-46" r="8" fill="#fff"/></g></g>`).join('');

  // ---------------------------------------------------------------- Helfer fürs Rendern
  const setT = (el, tr) => el.setAttribute('transform', tr);
  const disp = (el, on) => { el.style.display = on ? '' : 'none'; };
  function uiPop(el, t, t0, opts = {}) {
    const { center = true, rot = 0, d = 0.3, hideBefore = true, extra = '' } = opts;
    if (t0 === null || (hideBefore && t < t0)) { el.style.display = 'none'; return 0; }
    const s = popS(t, t0, d);
    el.style.display = '';
    el.style.opacity = clamp(s * 3);
    el.style.transform = `${center ? 'translateX(-50%) ' : ''}${extra} rotate(${rot}deg) scale(${Math.max(0.001, s)})`;
    return s;
  }
  const fmt = (n) => Math.round(n).toLocaleString('de-DE');

  // ---------------------------------------------------------------- Posen
  function poseFiete(E_, P, t) {
    const talk = P.talk ? envAt(t) : 0;
    const bounce = P.bounce ? -Math.abs(Math.sin(t * 8.5)) * 16 : 0;
    setT(E_.bob, `translate(0,${Math.sin(t * 4.2) * 2.5 + bounce})`);
    setT(E_.armL, `translate(-50,-160) rotate(${P.armL})`);
    setT(E_.armR, `translate(50,-160) rotate(${P.armR})`);
    setT(E_.head, `rotate(${P.tilt + Math.sin(t * 2.1) * 1.5 + talk * 2} 0 -165)`);
    disp(E_.fingerR, P.fingerR); disp(E_.fingerL, false);
    const bt = (t + 0.7) % 3.3;
    let eyeS = bt < 0.14 ? Math.max(0.08, Math.abs(bt - 0.07) / 0.07) : 1;
    let eyeScale = P.expr === 'o' ? 1.14 : 1;
    const happy = P.expr === 'happy';
    disp(E_.eyes, !happy); disp(E_.happy, happy);
    setT(E_.eyeL, `translate(-27,-228) scale(${eyeScale},${eyeScale * eyeS})`);
    setT(E_.eyeR, `translate(27,-228) scale(${eyeScale},${eyeScale * eyeS})`);
    const [lx, ly] = P.look;
    setT(E_.pupL, `translate(${lx},${ly})`); setT(E_.pupR, `translate(${lx},${ly})`);
    const worried = P.expr === 'worried';
    const browUp = P.expr === 'o' ? -10 : worried ? -4 : 0;
    setT(E_.browL, `translate(0,${browUp}) rotate(${worried ? -12 : 0} -27 -262)`);
    setT(E_.browR, `translate(0,${browUp}) rotate(${worried ? 12 : 0} 27 -262)`);
    // Mund
    const open = talk > 0.06;
    let mode = P.expr === 'o' ? 'o' : worried ? 'frown' : happy ? 'open' : 'smile';
    if (open) mode = 'open';
    disp(E_.mSmile, mode === 'smile'); disp(E_.mFrown, mode === 'frown'); disp(E_.mO, mode === 'o'); disp(E_.mOpen, mode === 'open');
    if (mode === 'open') {
      const k = open ? 0.25 + 0.8 * talk : 0.85;
      setT(E_.mOpen, `translate(0,-186) scale(1,${clamp(k, 0.2, 1.05)})`);
    }
    if (mode === 'o') setT(E_.mO, `translate(0,${0}) scale(1,${1 + talk * 0.3})`);
    disp(E_.cap, P.cap); disp(E_.hairTop, !P.cap);
  }

  function poseJurgen(J, P, t) {
    setT(J.bob, `translate(0,${Math.sin(t * 5 + 1) * 2 + (P.hop ? -Math.abs(Math.sin(t * 10)) * 18 : 0)})`);
    setT(J.wing, `translate(4,-86) rotate(${P.wing})`);
    setT(J.jaw, `translate(-44,-106) rotate(${-P.jaw})`);
    setT(J.head, `rotate(${P.headTilt} -14 -100)`);
    setT(J.pup, `translate(${P.look[0]},${P.look[1]})`);
    disp(J.eyeN, !P.euro); disp(J.euro, P.euro);
    disp(J.cap, P.cap);
  }

  // ---------------------------------------------------------------- Szenenzustand
  function baseState() {
    return {
      layer: 'world',
      cam: [1200, 1150, 1],
      fiete: { x: 1170, y: 1338, s: 1, armL: 9, armR: -9, expr: 'smile', look: [0, 0], tilt: 0, fingerR: false, cap: true, talk: true, bounce: false, show: true, flip: false },
      jur: { show: false, x: 1430, y: 1052, s: 1, flip: false, wing: 0, jaw: 0, headTilt: 0, look: [0, 0], euro: false, cap: false, hop: false },
      sand: 1, ghost: null, chest: null, ferryX: 3000, duck: null, fishbun: null, palmTag: false, ripples: 0, puff: null, qmarks: false,
      dim: 0, shake: 0,
      ui: {},
    };
  }

  const camLerp = (a, b, p) => [lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)];

  const SHOTS = {
    s01(S, t, s, lt, d) {
      S.cam = camLerp([1200, 1060, 0.7], [1200, 1110, 0.8], E.inOut(clamp(lt / d)));
      S.fiete.armR = -150 + Math.sin(t * 12) * 16;
      S.ui.title = s.start - 0.15;
    },
    s02(S, t, s, lt, d) {
      S.cam = camLerp([1170, 1150, 2.55], [1170, 1150, 2.72], lt / d);
      S.fiete.armR = -150 + Math.sin(t * 12) * 18;
      S.ui.chip = { t0: cue('s02', 'pop'), text: '👋 FIETE · PRÄSIDENT', cls: 'yellow' };
    },
    s03(S, t, s, lt, d) {
      S.cam = camLerp([1210, 1170, 1.25], [1210, 1165, 1.38], lt / d);
      const st = cue('s03', 'stamp');
      if (t < st) { S.fiete.armL = 70; S.fiete.armR = -70; }
      else { S.fiete.armL = 155 + Math.sin(t * 9) * 8; S.fiete.armR = -155 - Math.sin(t * 9) * 8; S.fiete.expr = 'happy'; S.fiete.bounce = true; }
      S.ui.stamp = st;
      S.confetti = cue('s03', 'confetti');
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s04(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1070, 0.95], [1180, 1070, 1.02], lt / d);
      S.fiete.armR = -160; S.fiete.fingerR = true; S.fiete.look = [3, -6];
      S.ui.profile = { t0: s.start + 0.03, followAt: null };
    },
    s05(S, t, s, lt, d) {
      S.cam = camLerp([1180, 1070, 1.02], [1180, 1070, 1.08], lt / d);
      S.fiete.armR = -160; S.fiete.fingerR = true; S.fiete.look = [3, -6];
      S.ui.profile = { t0: byId.s04.start + 0.03, followAt: cue('s05', 'ding') };
      const gp = cue('s05', 'pop');
      S.ghost = { t0: gp, arrow: false };
      S.ui.plusOne = gp;
    },
    s06(S, t, s, lt, d) {
      S.cam = camLerp([1080, 1210, 2.0], [1080, 1215, 2.12], lt / d);
      S.ghost = { t0: s.start - 1, arrow: true };
      S.fiete.look = [-6, 0]; S.fiete.armL = 40;
      S.ui.chip = { t0: cue('s06', 'pop'), text: '⬇️ HIER WOHNST DU', cls: 'green' };
    },
    s07(S, t, s, lt, d) {
      S.cam = camLerp([1200, 1150, 0.95], [1200, 1135, 1.05], E.out(lt / d));
      S.fiete.armL = 72; S.fiete.armR = -72; S.fiete.expr = 'happy';
      S.ui.banner = s.start + 0.04;
      S.sparkle = s.start + 0.05;
    },
    s08(S, t, s, lt, d) {
      S.cam = camLerp([1200, 1275, 1.48], [1200, 1275, 1.58], lt / d);
      S.fiete.armL = 60; S.fiete.armR = -9;
      S.ui.chip = { t0: cue('s08', 'pop'), text: '📍 NORDSEE · 12 m²', cls: '' };
    },
    s09(S, t, s, lt, d) {
      S.cam = camLerp([1200, 1285, 1.5], [1200, 1290, 1.42], lt / d);
      const p = E.inOut(prog(t, s.start, 0.9));
      S.sand = lerp(1, 0.5, p);
      S.ripples = p;
      S.fiete.expr = p > 0.2 ? 'o' : 'smile'; S.fiete.armL = lerp(9, 40, p); S.fiete.armR = lerp(-9, -40, p); S.fiete.look = [0, 6];
      S.ui.chip = { t0: cue('s09', 'pop'), text: '🌊 BEI FLUT: 4 m²', cls: 'blue' };
    },
    s10(S, t, s, lt, d) {
      S.cam = camLerp([985, 1095, 2.25], [985, 1085, 2.4], lt / d);
      S.palmTag = cue('s10', 'pop', 1);
      S.ui.chip = { t0: cue('s10', 'pop'), text: '🌴 1 × PALME', cls: '' };
    },
    s11(S, t, s, lt, d) {
      S.cam = camLerp([1430, 1175, 2.25], [1430, 1180, 2.4], lt / d);
      S.ui.chip = { t0: cue('s11', 'pop'), text: '🏖️ 1 × STRANDKORB', cls: '' };
    },
    s12(S, t, s, lt, d) {
      S.cam = camLerp([1020, 1215, 1.4], [1020, 1215, 1.45], lt / d);
      S.fiete.armL = 55; S.fiete.armR = -55; S.fiete.tilt = 8; S.fiete.look = [Math.sin(t * 3) * 7, 0];
      S.ui.plaetscher = s.start + 0.45;
      S.signBlink = true;
    },
    s13(S, t, s, lt, d) {
      S.cam = camLerp([1170, 1150, 2.6], [1170, 1150, 2.78], lt / d);
      S.fiete.expr = 'worried'; S.fiete.tilt = -6; S.fiete.look = [-5, -4]; S.fiete.armL = 30;
      S.qmarks = s.start + 0.2;
      S.ui.chip = { t0: cue('s13', 'pop'), text: '🏛️ MEINE REGIERUNG?', cls: '' };
    },
    s14(S, t, s, lt, d) {
      S.cam = camLerp([1320, 1110, 1.42], [1320, 1110, 1.5], lt / d);
      const p = E.out(prog(t, s.start, 0.55));
      S.jur.show = true;
      S.jur.x = lerp(1760, 1430, p); S.jur.y = lerp(700, 1052, p);
      S.jur.wing = p < 1 ? -40 + Math.sin(t * 40) * 40 : -4;
      const sq = cue('s14', 'squawk');
      S.jur.jaw = t > sq && t < sq + 0.35 ? 22 : 0;
      S.fiete.look = [7, -5]; S.fiete.expr = t > sq ? 'happy' : 'smile';
      S.ui.chip = { t0: cue('s14', 'pop'), text: '💼 FINANZMINISTER', cls: 'yellow' };
    },
    s15(S, t, s, lt, d) {
      S.cam = camLerp([1405, 975, 3.0], [1405, 980, 3.15], lt / d);
      S.jur.show = true;
      const g = cue('s15', 'gulp');
      S.fishbun = { t0: s.start + 0.1, gulp: g };
      S.jur.jaw = t > g - 0.15 && t < g + 0.15 ? 26 : 0;
      S.jur.look = t < g ? [-3, 2] : [0, 0];
      S.ui.chip = { t0: cue('s15', 'pop'), text: '💰 GEHALT: 1 FISCHBRÖTCHEN', cls: 'yellow' };
      S.hideFlag = true;
    },
    s16(S, t, s, lt, d) {
      S.cam = camLerp([1250, 1170, 1.6], [1250, 1170, 1.66], lt / d);
      const pf = cue('s16', 'poof');
      S.jur.show = true; S.jur.x = 1330; S.jur.y = 1345; S.jur.look = [4, 2];
      S.jur.cap = t >= pf; S.fiete.cap = t < pf;
      S.fiete.expr = t >= pf ? 'o' : 'smile';
      S.fiete.armL = t >= pf ? 150 : 9; S.fiete.armR = t >= pf ? -150 : -9;
      const sq = cue('s16', 'squawk');
      S.jur.jaw = t > sq && t < sq + 0.35 ? 22 : 0;
      S.jur.hop = t > sq;
      S.puff = pf;
      S.ui.chip = { t0: pf, text: '🧢 GEKLAUT!', cls: 'red' };
    },
    s17(S, t, s, lt, d) {
      S.layer = 'globe';
      S.globe = { z: lerp(3.1, 3.25, lt / d), f: [70, -60], rot: 0, pins: 0, ring: true, fiete: false };
      S.ui.chip = { t0: cue('s17', 'pop'), text: '🏝️ EINWOHNER: 0', cls: '' };
    },
    s18(S, t, s, lt, d) {
      S.layer = 'globe';
      const p = E.inOut(prog(t, s.start, 0.75));
      S.globe = { z: lerp(3.25, 1, p), f: [lerp(70, 0, p), lerp(-60, 60, p)], rot: lt * 70, pins: clamp((t - cue('s18', 'pins')) / 1.1), ring: false, fiete: true };
      const n = Math.pow(clamp((t - cue('s18', 'pins')) / 1.2), 2) * 1000000;
      S.ui.chip = { t0: s.start - 5, text: `🏝️ EINWOHNER: ${fmt(n)}`, cls: n > 0 ? 'green' : '' };
    },
    s19(S, t, s, lt, d) {
      S.cam = camLerp([1900, 1150, 1.08], [1915, 1160, 1.14], lt / d);
      S.ferryX = lerp(2800, 2185, E.out(prog(t, s.start, d * 0.95)));
      S.fiete.x = 1820; S.fiete.y = 1300; S.fiete.look = [7, 0]; S.fiete.armR = -150 + Math.sin(t * 12) * 16;
      S.ui.chip = { t0: cue('s19', 'pop'), text: '⛴️ MORGEN · 6:12 · 1. FÄHRE', cls: '' };
    },
    s20(S, t, s, lt, d) {
      S.cam = camLerp([2160, 1110, 2.3], [2160, 1110, 2.45], lt / d);
      S.ferryX = 2185;
      S.fiete.x = 1820; S.fiete.y = 1300;
      S.ui.chip = { t0: cue('s20', 'pop'), text: '👤 PASSAGIERE: 0', cls: 'red' };
    },
    s21(S, t, s, lt, d) {
      S.cam = camLerp([1960, 1240, 1.42], [1960, 1240, 1.48], lt / d);
      S.ferryX = 2185;
      S.fiete.x = 1820; S.fiete.y = 1300; S.fiete.expr = 'worried'; S.fiete.look = [6, 6]; S.fiete.tilt = 6;
      S.duck = { x: lerp(2300, 2010, E.out(prog(t, s.start, d))), sq: cue('s21', 'squeak') };
      S.ui.chip = { t0: cue('s21', 'squeak'), text: '🦆 1 × ENTE (GUMMI)', cls: 'yellow' };
    },
    s22(S, t, s, lt, d) {
      S.cam = camLerp([1170, 1000, 2.4], [1170, 1000, 2.5], lt / d);
      S.fiete.armR = -158; S.fiete.fingerR = true; S.fiete.look = [3, -7];
      S.ui.profile = { t0: s.start + 0.02, followAt: cue('s22', 'tap'), hand: true };
    },
    s23(S, t, s, lt, d) {
      S.cam = camLerp([1240, 1180, 1.32], [1240, 1180, 1.4], lt / d);
      S.jur.show = true; S.jur.x = 1330; S.jur.y = 1345; S.jur.hop = true;
      S.fiete.armL = 150 + Math.sin(t * 9) * 8; S.fiete.armR = -150; S.fiete.expr = 'happy'; S.fiete.bounce = true;
      S.ui.comment = cue('s23', 'blip');
    },
    s24(S, t, s, lt, d) {
      S.cam = camLerp([1240, 1180, 1.4], [1240, 1180, 1.46], lt / d);
      S.jur.show = true; S.jur.x = 1330; S.jur.y = 1345;
      S.dim = clamp(lt / 0.2) * 0.85;
      S.ui.passport = { t0: cue('s24', 'pop'), stamp: cue('s24', 'stamp') };
      const st = cue('s24', 'stamp');
      S.shake = t >= st ? Math.max(0, 1 - (t - st) / 0.25) : 0;
    },
    s25(S, t, s, lt, d) {
      S.cam = camLerp([1240, 1180, 1.46], [1240, 1180, 1.5], lt / d);
      S.jur.show = true; S.jur.x = 1330; S.jur.y = 1345;
      S.dim = 0.85;
      S.ui.passport = { t0: byId.s24.start - 5, stamp: byId.s24.start - 5 };
      const ticks = byId.s25.sfx.filter((x) => x[0] === 'tick').map((x) => x[1]).filter((x) => t >= x).length;
      S.ui.chip2 = { t0: cue('s25', 'tick'), text: `⏰ NUR HEUTE · 23:59:${String(59 - ticks).padStart(2, '0')}`, cls: 'red', top: 1060 };
    },
    s26(S, t, s, lt, d) {
      S.cam = camLerp([1170, 1180, 1.9], [1170, 1180, 2.0], lt / d);
      S.fiete.armR = -100; S.fiete.fingerR = true; S.fiete.expr = 'happy';
      S.dim = 0.6;
      S.ui.list = { t0: s.start + 0.03, mark: cue('s26', 'sparkle') };
      S.sparkle = cue('s26', 'sparkle');
    },
    s27(S, t, s, lt, d) {
      S.cam = camLerp([1240, 1170, 1.15], [1240, 1170, 1.22], lt / d);
      S.jur.show = true; S.jur.x = 1330; S.jur.y = 1345;
      S.fiete.armL = 70; S.fiete.armR = -70;
      S.ui.chip = { t0: cue('s27', 'pop'), text: '🗳️ AB JETZT BESTIMMT IHR', cls: 'green' };
      S.floatBubbles = [cue('s27', 'blip', 0), cue('s27', 'blip', 1), cue('s27', 'blip', 2), cue('s27', 'blip', 2) + 0.2];
    },
    s28(S, t, s, lt, d) {
      S.cam = camLerp([1335, 1270, 2.9], [1335, 1270, 3.05], lt / d);
      S.chest = { open: 0 };
      S.jur.show = true; S.jur.x = 1450; S.jur.y = 1365; S.jur.look = [-4, 3];
      S.ui.kasse = { t0: cue('s28', 'pop'), value: 0 };
    },
    s29(S, t, s, lt, d) {
      S.cam = camLerp([1335, 1270, 3.05], [1335, 1265, 3.2], lt / d);
      const k = cue('s29', 'kaching');
      S.chest = { open: E.back(prog(t, k, 0.3)), coinsAt: k };
      S.jur.show = true; S.jur.x = 1450; S.jur.y = 1365; S.jur.euro = t > k + 0.1; S.jur.jaw = t > k + 0.1 ? 18 : 0;
      S.ui.kasse = { t0: byId.s28.start - 5, value: 500 * E.out(prog(t, k, 0.55)) };
    },
    s30(S, t, s, lt, d) { cardsShot(S, t, s, lt, d); S.fiete.armR = -160; S.fiete.fingerR = true; S.fiete.look = [0, -7]; },
    s31(S, t, s, lt, d) { cardsShot(S, t, s, lt, d); S.jur.hop = true; const sq = cue('s31', 'squawk'); S.jur.jaw = t > sq && t < sq + 0.4 ? 24 : 0; },
    s32(S, t, s, lt, d) { cardsShot(S, t, s, lt, d); S.fiete.armL = 60; S.fiete.armR = -60; S.fiete.tilt = 8; },
    s33(S, t, s, lt, d) {
      cardsShot(S, t, s, lt, d);
      S.fiete.armR = -150 + Math.sin(t * 12) * 16; S.fiete.expr = t > s.speechEnd ? 'happy' : 'smile';
      S.jur.hop = t > s.speechEnd;
      S.ui.vote = cue('s33', 'pop');
      const p = E.out(prog(t, s.start + 0.2, 2.6));
      S.ui.likes = [312 * p, 498 * p, 176 * p];
      S.hearts = [cue('s33', 'hearts', 0), cue('s33', 'hearts', 1)];
    },
  };

  function cardsShot(S, t, s, lt, d) {
    const a = byId.s30.start;
    S.cam = camLerp([1240, 1135, 1.0], [1240, 1125, 1.1], clamp((t - a) / (TL.duration - a)));
    S.chest = { open: 1, still: true };
    S.jur.show = true; S.jur.x = 1400; S.jur.y = 1365;
    S.ui.cards = [cue('s30', 'card'), cue('s31', 'card'), cue('s32', 'card')];
  }

  // ---------------------------------------------------------------- Zeichnen
  const confR = rng(99);
  const confetti = [];
  for (let i = 0; i < 90; i++) confetti.push({ a: -Math.PI / 2 + (confR() - 0.5) * 2.6, v: 700 + confR() * 900, rot: confR() * 360, vr: (confR() - 0.5) * 900, c: ['#FFC83A', '#FF4B5C', '#2DBE60', '#5CC8FF', '#fff', '#B67CFF'][i % 6], w: 14 + confR() * 14, h: 8 + confR() * 8 });
  const sparkR = rng(5);
  const sparkles = [];
  for (let i = 0; i < 14; i++) sparkles.push({ x: 120 + sparkR() * 840, y: 230 + sparkR() * 380, ph: sparkR(), s: 0.6 + sparkR() * 0.8 });

  function drawFx(S, t) {
    let out = '';
    if (S.confetti && t >= S.confetti) {
      const lt = t - S.confetti;
      for (const c of confetti) {
        const x = 540 + Math.cos(c.a) * c.v * lt;
        const y = 420 + Math.sin(c.a) * c.v * lt + 1300 * lt * lt;
        out += `<rect x="${-c.w / 2}" y="${-c.h / 2}" width="${c.w}" height="${c.h}" rx="2" fill="${c.c}" transform="translate(${x},${y}) rotate(${c.rot + c.vr * lt})" opacity="${clamp(2 - lt)}"/>`;
      }
    }
    if (S.sparkle && t >= S.sparkle) {
      const lt = t - S.sparkle;
      for (const sp of sparkles) {
        const k = Math.max(0, Math.sin((lt * 2.2 + sp.ph) * Math.PI)) * sp.s * clamp(lt * 4);
        if (k <= 0.02) continue;
        out += `<path transform="translate(${sp.x},${sp.y}) scale(${k})" d="M0 -34 Q4 -4 34 0 Q4 4 0 34 Q-4 4 -34 0 Q-4 -4 0 -34 Z" fill="#FFF3B0" stroke="#fff" stroke-width="3"/>`;
      }
    }
    $('fx').innerHTML = out;
  }

  function drawWaves(t, S) {
    let d = '';
    const z = S.cam[2];
    for (const c of crests) {
      const k = 0.5 + 0.5 * Math.sin(t * c.sp * 2 + c.ph);
      if (k < 0.25) continue;
      const x = c.x + Math.sin(t * 0.5 + c.ph) * 14;
      const s = c.s * (0.6 + 0.4 * k);
      d += `<path d="M${x - s} ${c.y} Q${x} ${c.y - s * 0.35} ${x + s} ${c.y}" stroke-width="${c.w}" opacity="${(0.25 + 0.5 * k).toFixed(2)}"/>`;
    }
    $('waves').innerHTML = d;
  }

  function drawWorld(S, t) {
    const [cx, cy, z] = S.cam;
    const sh = S.shake ? [Math.sin(t * 90) * 14 * S.shake, Math.cos(t * 77) * 10 * S.shake] : [0, 0];
    setT($('cam'), `translate(${540 + sh[0]},${960 + sh[1]}) scale(${z}) translate(${-cx},${-cy})`);
    // Wolken & Windräder
    for (let i = 0; i < 6; i++) {
      const c = $(`cloud${i}`);
      const x = +c.dataset.x + t * 14 * c.dataset.s, y = +c.dataset.y;
      setT(c, `translate(${x},${y}) scale(${c.dataset.s})`);
    }
    for (let i = 0; i < 4; i++) setT($(`turb${i}`), `translate(0,-130) rotate(${t * 70 + i * 40})`);
    drawWaves(t, S);
    // Insel
    const sx = S.sand;
    setT($('island'), `translate(1200,1326) scale(${sx},${0.75 + 0.25 * sx}) translate(-1200,-1326)`);
    $('foam').setAttribute('rx', 458 + Math.sin(t * 2.5) * 8);
    $('foam').setAttribute('ry', 134 + Math.sin(t * 2.5) * 3);
    // Wellenringe bei Flut
    const rp = $('ripples');
    if (S.ripples > 0) {
      rp.style.opacity = S.ripples;
      const k = (t * 1.3) % 1;
      rp.innerHTML = [[1000, 1318, 50], [1430, 1328, 120], [1170, 1340, 70], [860, 1352, 30]].map(([x, y, r]) =>
        `<ellipse cx="${x}" cy="${y}" rx="${r + 20 + k * 40}" ry="${(r + 20 + k * 40) * 0.25}" opacity="${1 - k}"/>`).join('');
    } else rp.style.opacity = 0;
    disp($('flagpole'), !S.hideFlag);
    // Palme
    setT($('palmTop'), `translate(-28,-340) rotate(${Math.sin(t * 1.6) * 3})`);
    const tag = $('palmTag');
    if (S.palmTag && t >= S.palmTag) { disp(tag, true); setT(tag, `translate(-14,-150) scale(${popS(t, S.palmTag)})`); } else disp(tag, false);
    // Schild
    $('signCount').setAttribute('fill', S.signBlink && Math.floor(t * 4) % 2 ? '#E8243B' : '#4A2A12');
    // Geist (+1 Einwohner)
    const g = $('ghost');
    if (S.ghost && t >= S.ghost.t0) {
      disp(g, true);
      const s = popS(t, S.ghost.t0, 0.35);
      setT($('ghostBody'), `scale(${s})`);
      $('ghostArm').setAttribute('d', `M26 -70 L${52 + Math.sin(t * 12) * 8} -110`);
      disp($('ghostArrow'), S.ghost.arrow);
      setT($('ghostArrow'), `translate(0,${Math.sin(t * 7) * 10})`);
    } else disp(g, false);
    // Truhe
    const ch = $('chest');
    if (S.chest) {
      disp(ch, true);
      setT($('chestLid'), `translate(0,-62) scale(1,${1 - 1.9 * clamp(S.chest.open, 0, 1.2)})`);
      let coins = '';
      if (S.chest.open > 0.05) {
        const lt = S.chest.coinsAt ? t - S.chest.coinsAt : 2;
        const cr = rng(17);
        for (let i = 0; i < 14; i++) {
          const a = -Math.PI / 2 + (cr() - 0.5) * 1.8, v = 160 + cr() * 220;
          const tt = Math.min(lt, 0.9);
          const x = Math.cos(a) * v * tt, y = -60 + Math.sin(a) * v * tt + 420 * tt * tt;
          const yy = Math.min(y, -64 + cr() * 6);
          coins += `<ellipse cx="${x * (lt > 0.9 ? 0.3 : 1)}" cy="${lt > 0.9 ? -64 - cr() * 16 : yy}" rx="11" ry="9" fill="#F7CF4B" stroke="${OUT}" stroke-width="3"/>`;
        }
      }
      $('coins').innerHTML = coins;
    } else disp(ch, false);
    // Fähre
    setT($('ferry'), `translate(${S.ferryX},${1272 + Math.sin(t * 2) * 4}) rotate(${Math.sin(t * 1.6) * 1.2})`);
    // Ente
    const dk = $('duck');
    if (S.duck) {
      disp(dk, true);
      const sq = t > S.duck.sq && t < S.duck.sq + 0.3 ? 1.18 : 1;
      setT(dk, `translate(${S.duck.x},${1440 + Math.sin(t * 3) * 6}) rotate(${Math.sin(t * 2.4) * 6}) scale(${sq})`);
    } else disp(dk, false);
    // Fischbrötchen
    const fb = $('fishbun');
    if (S.fishbun && t >= S.fishbun.t0 && t < S.fishbun.gulp) {
      disp(fb, true);
      const s = popS(t, S.fishbun.t0) * (1 - E.in(prog(t, S.fishbun.gulp - 0.25, 0.25)));
      const x = lerp(1310, 1352, prog(t, S.fishbun.gulp - 0.25, 0.25));
      setT(fb, `translate(${x},${972 + Math.sin(t * 5) * 4}) scale(${0.62 * s}) rotate(-8)`);
    } else disp(fb, false);
    // Puff
    if (S.puff && t >= S.puff && t < S.puff + 0.6) {
      const lt = (t - S.puff) / 0.6;
      $('puff').innerHTML = [[-40, -10], [30, -20], [0, 20], [-20, -40], [40, 10]].map(([x, y], i) =>
        `<circle cx="${1170 + x * (1 + lt * 2)}" cy="${1030 + y * (1 + lt * 2)}" r="${(30 + i * 4) * (1 - lt * 0.6)}" fill="#fff" opacity="${1 - lt}"/>`).join('');
    } else $('puff').innerHTML = '';
    // Fragezeichen
    const qm = $('qmarks');
    if (S.qmarks && t >= S.qmarks) {
      disp(qm, true);
      const a = popS(t, S.qmarks), b = popS(t, S.qmarks + 0.2);
      setT($('q1'), `translate(1080,${1000 + Math.sin(t * 5) * 6}) rotate(-14) scale(${a})`);
      setT($('q2'), `translate(1240,${975 + Math.sin(t * 5 + 1) * 6}) rotate(12) scale(${b})`);
    } else disp(qm, false);
    // Fiete
    const f = S.fiete;
    disp($('fieteW'), f.show);
    setT($('fieteW'), `translate(${f.x},${f.y}) scale(${f.s})`);
    poseFiete(F1, f, t);
    // Jürgen
    const jw = $('jurgenW');
    disp(jw, S.jur.show);
    if (S.jur.show) {
      setT(jw, `translate(${S.jur.x},${S.jur.y}) scale(${S.jur.flip ? -S.jur.s : S.jur.s},${S.jur.s})`);
      poseJurgen(J1, S.jur, t);
    }
  }

  function drawGlobe(S, t) {
    const G = S.globe;
    setT($('globeCam'), `translate(540,1130) scale(${G.z}) translate(${-G.f[0]},${-G.f[1]})`);
    setT($('continents'), `translate(${-(G.rot % 1600)},0)`);
    disp($('gRing'), G.ring);
    $('gRing').setAttribute('r', 40 + Math.sin(t * 6) * 4);
    disp($('gLabel'), G.ring);
    for (let i = 0; i < pins.length; i++) {
      const el = $(`pin${i}`);
      const on = G.pins > (i + 1) / pins.length - 1e-6 && G.pins > 0;
      disp(el, on);
      if (on) {
        const t0 = (i / pins.length) * 1.1;
        el.firstElementChild.setAttribute('transform', `scale(${Math.min(1.2, 0.35 + G.pins * 2 - i * 0.1)})`);
      }
    }
    disp($('fieteG'), G.fiete);
    if (G.fiete) poseFiete(F2, { armL: 155 + Math.sin(t * 9) * 8, armR: -155, expr: 'happy', look: [0, 0], tilt: 0, fingerR: false, cap: true, talk: true, bounce: true }, t);
    for (const st of document.querySelectorAll('.star')) st.setAttribute('opacity', 0.35 + 0.65 * Math.abs(Math.sin(t * 1.5 + +st.dataset.p)));
  }

  function drawUI(S, t, seg) {
    const U = S.ui;
    // Titel & Badge
    uiPop($('title'), t, U.title ?? null, { d: 0.4 });
    if (seg.id === 's01') { $('badge').style.display = 'none'; }
    else { const b = $('badge'); b.style.display = ''; b.style.opacity = 1; b.style.transform = `rotate(-3deg) scale(${1 + 0.04 * Math.sin(t * 4)})`; }
    // Chips
    for (const [key, el] of [['chip', $('chip')], ['chip2', $('chip2')]]) {
      const c = U[key];
      if (!c) { el.style.display = 'none'; continue; }
      if (el.dataset.text !== c.text) { el.textContent = c.text; el.dataset.text = c.text; }
      el.className = `ui chip ${c.cls || ''}`;
      el.style.top = (c.top || 278) + 'px';
      uiPop(el, t, c.t0, { rot: key === 'chip' ? -2 : 2 });
    }
    uiPop($('plaetscher'), t, U.plaetscher ?? null, { center: false, rot: -8 });
    $('plaetscher').style.left = '650px'; $('plaetscher').style.top = '1160px';
    uiPop($('plusOne'), t, U.plusOne ?? null, { extra: `translateY(${-prog(t, U.plusOne || 0, 1.2) * 40}px)` });
    $('plusOne').style.top = '1010px';
    uiPop($('stamp'), t, U.stamp ?? null, { rot: -7, d: 0.22 });
    uiPop($('banner'), t, U.banner ?? null, { rot: -2 });
    // Profilkarte
    const pr = $('profile');
    if (U.profile) {
      uiPop(pr, t, U.profile.t0);
      const followed = U.profile.followAt && t >= U.profile.followAt;
      const bf = $('btnFollow');
      bf.className = 'btn follow' + (followed ? ' done' : '');
      bf.textContent = followed ? 'Gefolgt ✓' : 'Folgen';
      const pulse = !followed ? 1 + 0.05 * Math.max(0, Math.sin(t * 10)) : 1;
      bf.style.transform = `scale(${pulse})`;
      $('stF').textContent = followed ? '1' : '0';
      $('stE').textContent = followed ? '1' : '0';
      const h = $('hand');
      if (U.profile.hand) {
        const r = bf.getBoundingClientRect();
        const tx = r.left + r.width * 0.55, ty = r.top + r.height * 0.55;
        const p = E.inOut(prog(t, U.profile.t0 + 0.1, U.profile.followAt - U.profile.t0 - 0.12));
        const x = lerp(820, tx, p), y = lerp(1100, ty, p);
        const tap = t > U.profile.followAt - 0.06 && t < U.profile.followAt + 0.12 ? 0.85 : 1;
        h.style.display = ''; h.style.left = (x - 30) + 'px'; h.style.top = (y - 8) + 'px'; h.style.transform = `scale(${tap})`;
      } else h.style.display = 'none';
    } else { pr.style.display = 'none'; $('hand').style.display = 'none'; }
    uiPop($('comment'), t, U.comment ?? null, { rot: -1.5 });
    // Reisepass
    if (U.passport) {
      uiPop($('passport'), t, U.passport.t0, { rot: -3 });
      const ps = $('pstamp');
      if (t >= U.passport.stamp) {
        const k = prog(t, U.passport.stamp, 0.14);
        ps.style.display = ''; ps.style.opacity = clamp(k * 2) * 0.95;
        ps.style.transform = `translateX(-50%) rotate(-14deg) scale(${lerp(2.6, 1, E.out(k))})`;
      } else ps.style.display = 'none';
    } else { $('passport').style.display = 'none'; $('pstamp').style.display = 'none'; }
    // Liste
    if (U.list) {
      uiPop($('list'), t, U.list.t0, { rot: 2 });
      $('listMark').style.width = `${E.out(prog(t, U.list.mark, 0.35)) * 100}%`;
    } else $('list').style.display = 'none';
    // Kasse
    if (U.kasse) {
      uiPop($('kasse'), t, U.kasse.t0, { rot: -2 });
      $('kasseVal').textContent = `${Math.round(U.kasse.value)} €`;
    } else $('kasse').style.display = 'none';
    // Karten
    const cards = [$('cardA'), $('cardB'), $('cardC')];
    cards.forEach((el, i) => {
      el.style.left = `${100 + i * 300}px`;
      if (U.cards) uiPop(el, t, U.cards[i], { center: false, rot: [-4, 0, 4][i], extra: `translateY(${i === 1 ? -10 : 0}px)` });
      else el.style.display = 'none';
    });
    const likes = U.likes || [0, 0, 0];
    $('likesA').textContent = fmt(likes[0]); $('likesB').textContent = fmt(likes[1]); $('likesC').textContent = fmt(likes[2]);
    uiPop($('votePill'), t, U.vote ?? null, { rot: -1.5 });
    // Kommentar-Blasen
    floaters.forEach((el, i) => {
      const t0 = S.floatBubbles ? S.floatBubbles[i] : null;
      if (t0 === null || t0 === undefined || t < t0) { el.style.display = 'none'; return; }
      const lt = t - t0;
      el.style.display = '';
      el.style.left = `${[90, 560, 140, 600][i]}px`;
      el.style.top = `${1180 - lt * 230 - i * 10}px`;
      el.style.opacity = clamp(lt * 5) * clamp(2.2 - lt);
      el.style.transform = `rotate(${[-5, 4, 3, -4][i]}deg) scale(${popS(t, t0, 0.25)})`;
    });
    // Herzen
    hearts.forEach((el, i) => {
      if (!S.hearts) { el.style.display = 'none'; return; }
      const t0 = S.hearts[i % 2] + (i >> 1) * 0.09;
      if (t < t0) { el.style.display = 'none'; return; }
      const lt = t - t0;
      el.style.display = '';
      el.style.left = `${120 + ((i * 137) % 760)}px`;
      el.style.top = `${1700 - lt * 520}px`;
      el.style.opacity = clamp(lt * 6) * clamp(1.6 - lt);
      el.style.transform = `translateX(${Math.sin(lt * 5 + i) * 30}px) scale(${0.6 + (i % 3) * 0.2})`;
    });
  }

  function drawCaption(t, seg) {
    const c1 = $('cap1'), c2 = $('cap2');
    let chunk = null;
    for (const c of seg.caps) if (t >= c.start - 0.02) chunk = c;
    if (!chunk || seg.id === 's01' && t < seg.start) { c1.textContent = ''; c2.textContent = ''; return; }
    const col = { w: '#fff', g: '#FFD43B', r: '#FF5A64', y: '#5CCBFF' };
    const build = (el, words) => {
      el.innerHTML = words.map(([w, s]) => `<tspan fill="${col[s]}">${w}</tspan>`).join(' ');
    };
    const k = popS(t, chunk.start, 0.16);
    const sc = lerp(0.82, 1, k);
    build(c1, chunk.words);
    c1.setAttribute('font-size', 84); c2.textContent = '';
    let w = c1.getComputedTextLength();
    let lines = 1;
    if (w > 900 && chunk.words.length > 1) {
      const mid = Math.ceil(chunk.words.length / 2);
      build(c1, chunk.words.slice(0, mid)); build(c2, chunk.words.slice(mid));
      lines = 2;
    }
    let fs = 84;
    const maxW = Math.max(c1.getComputedTextLength(), lines === 2 ? c2.getComputedTextLength() : 0);
    if (maxW > 920) fs = Math.floor(84 * 920 / maxW);
    c1.setAttribute('font-size', fs); c2.setAttribute('font-size', fs);
    const y0 = lines === 2 ? 1350 : 1395;
    setT(c1, `translate(540,${y0}) scale(${sc}) translate(-540,${-y0})`);
    c1.setAttribute('y', y0);
    c2.setAttribute('y', y0 + fs * 1.08);
    setT(c2, `translate(540,${y0}) scale(${sc}) translate(-540,${-y0})`);
  }

  window.renderAt = (t) => {
    const seg = segAt(t);
    const S = baseState();
    const lt = t - seg.start, d = seg.end - seg.start;
    SHOTS[seg.id](S, t, seg, lt, d);
    const isGlobe = S.layer === 'globe';
    $('world').style.display = isGlobe ? 'none' : '';
    $('globe').style.display = isGlobe ? 'block' : 'none';
    if (isGlobe) drawGlobe(S, t); else drawWorld(S, t);
    $('dim').style.opacity = S.dim;
    drawFx(S, t);
    drawUI(S, t, seg);
    drawCaption(t, seg);
  };

  // Schriften vorladen, dann bereit
  const allText = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜabcdefghijklmnopqrstuvwxyzäöüß0123456789 .,:!?·€✓✨…→⬇️👋📍🌊🌴🏖️🏛️💼💰🧢🏝️⛴️👤🦆🗳️⏰💬❤️🩷👆♡🚩👀😂🐦';
  Promise.all([
    document.fonts.load('900 84px Nunito', allText), document.fonts.load('800 30px Nunito', allText),
    document.fonts.load('700 60px Fredoka', allText), document.fonts.load('600 40px Fredoka', allText),
    document.fonts.load('40px "Noto Color Emoji"', allText),
  ]).then(() => document.fonts.ready).then(() => {
    window.renderAt(0.3);
    window.READY = true;
  });
})();

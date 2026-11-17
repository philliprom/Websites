// Tech-Lupe – Folge 2 „Das Jahr-2038-Problem“: reine Bewegtgrafik im Bildschirm-Raum (Ebene „alt“).
(() => {
  const { $, clamp, lerp, E, prog, popS, cue, rng } = Engine;
  const C = { bg: '#0E1430', panel: '#141C3A', line: '#2A3A6E', cyan: '#3DDCFF', yel: '#FFD43B', red: '#FF4D6D', grn: '#7CFF6B', grey: '#7F8BB5', w: '#FFFFFF' };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const T = (x, y, s, o = {}) => `<text x="${x}" y="${y}"${o.m ? ' class="m"' : ''} text-anchor="${o.a || 'middle'}" dominant-baseline="${o.b || 'alphabetic'}" font-size="${o.s || 60}" fill="${o.f || C.w}"${o.st ? ` stroke="${o.st}" stroke-width="${o.sw || 10}" paint-order="stroke fill" stroke-linejoin="round"` : ''}${o.op !== undefined ? ` opacity="${o.op}"` : ''}${o.tr ? ` transform="${o.tr}"` : ''}>${o.raw ? s : esc(s)}</text>`;
  const pop = (t, t0, d = 0.25) => (t0 === null || t < t0 ? 0 : popS(t, t0, d));
  const at = (x, y, s, r = 0) => `translate(${x},${y}) rotate(${r}) scale(${Math.max(0.001, s)}) translate(${-x},${-y})`;
  const chip = (x, y, txt, t, t0, o = {}) => {
    const k = pop(t, t0); if (k <= 0) return '';
    const fs = o.s || 46, w = o.w || txt.length * fs * 0.62 + 70;
    return `<g transform="${at(x, y, k, o.r || -2)}"><rect x="${x - w / 2}" y="${y - fs * 0.95}" width="${w}" height="${fs * 1.9}" rx="${fs * 0.95}" fill="${o.bg || C.red}" stroke="#0B1022" stroke-width="7"/>${T(x, y + fs * 0.34, txt, { s: fs, f: o.fg || C.w })}</g>`;
  };
  const caps = (seg, i, fb) => (seg.caps && seg.caps[i] ? seg.caps[i].start : fb);
  const panel = (x, y, w, h, title) => `<g filter="url(#sh)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="34" fill="${C.panel}" stroke="${C.line}" stroke-width="5"/></g>
    <rect x="${x}" y="${y}" width="${w}" height="74" rx="34" fill="#1B2550"/><rect x="${x}" y="${y + 40}" width="${w}" height="34" fill="#1B2550"/>
    <circle cx="${x + 46}" cy="${y + 38}" r="13" fill="#FF5F57"/><circle cx="${x + 86}" cy="${y + 38}" r="13" fill="#FEBC2E"/><circle cx="${x + 126}" cy="${y + 38}" r="13" fill="#28C840"/>
    ${T(x + w / 2, y + 50, title, { s: 34, f: C.grey, m: true })}`;

  const statics = () => `
    <defs>
      <radialGradient id="bgG" cx="50%" cy="40%" r="80%"><stop offset="0" stop-color="#1A2456"/><stop offset=".6" stop-color="#0E1430"/><stop offset="1" stop-color="#070A1A"/></radialGradient>
      <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="0" flood-color="#000" flood-opacity=".45"/></filter>
      <filter id="gl" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <clipPath id="lane"><rect x="70" y="0" width="940" height="1920"/></clipPath>
      <linearGradient id="fadeG" x1="0" x2="1"><stop offset=".72" stop-color="#fff"/><stop offset=".95" stop-color="#fff" stop-opacity="0"/></linearGradient>
      <mask id="fadeR" maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1920"><rect width="1080" height="1920" fill="url(#fadeG)"/></mask>
    </defs>
    <rect width="1080" height="1920" fill="url(#bgG)"/>
    <g opacity=".08" stroke="#8FB4FF" stroke-width="2">${Array.from({ length: 13 }, (_, i) => `<line x1="${i * 90}" y1="0" x2="${i * 90}" y2="1920"/>`).join('')}${Array.from({ length: 22 }, (_, i) => `<line x1="0" y1="${i * 90}" x2="1080" y2="${i * 90}"/>`).join('')}</g>
    <g id="dyn"></g>
    <g transform="translate(540,128)"><rect x="-185" y="-46" width="370" height="92" rx="46" fill="${C.cyan}" stroke="#0B1022" stroke-width="7"/>${T(0, 17, '🔍 TECH-LUPE', { s: 46, f: '#0B1022' })}</g>`;

  const shots = {};
  const out = (S, html) => { S.layer = 'alt'; S.html = html; };

  const NOW = 1794934800; // Unix-Zeit am 17.11.2026, 18:00 Uhr
  const MAX = 2147483647;
  const de = (n) => n.toLocaleString('de-DE');
  const bits32 = (n) => ((n >>> 0).toString(2)).padStart(32, '0');

  // Digitaluhr wie auf einem Gerät
  const clock = (y, date, time, o = {}) => {
    const col = o.red ? C.red : C.cyan;
    const gl = o.glitch || 0;
    let h = `<g filter="url(#sh)"><rect x="110" y="${y}" width="860" height="420" rx="40" fill="#0A0F24" stroke="${o.red ? C.red : C.line}" stroke-width="7"/></g>`;
    h += T(540, y + 70, o.label || 'SYSTEMZEIT', { s: 38, f: C.grey });
    for (let k = 0; k < (gl ? 3 : 1); k++) {
      const dx = gl ? (k - 1) * 14 * gl : 0, f = gl ? ['#FF4D6D', '#3DDCFF', '#fff'][k] : col;
      h += `<g opacity="${gl ? 0.7 : 1}" transform="translate(${dx},0)">${T(540, y + 210, date, { s: 118, f, m: true })}${T(540, y + 345, time, { s: 96, f, m: true, op: 0.85 })}</g>`;
    }
    return h;
  };
  const scramble = (s, t) => s.replace(/[0-9]/g, (_, i) => String(Math.floor((Math.sin(t * 97 + i * 13) + 1) * 4.999)));

  // s01: 2038 -> 1901
  shots.s01 = (S, t, seg) => {
    const flip = cue('s01', 'boom');
    const lt = t - seg.start;
    const sec = Math.min(7, 5 + Math.floor(lt / 0.5));
    let h = '';
    if (t < flip - 0.3) {
      h += clock(470, '19.01.2038', `04:14:0${sec}`);
      if (sec === 7) h += chip(540, 1010, '⚠️ LETZTE SEKUNDE', t, seg.start + 1.0, { bg: C.yel, fg: '#0B1022', s: 48, w: 560 });
    } else if (t < flip) {
      const g = 1 - (flip - t) / 0.3;
      h += clock(470, scramble('19.01.2038', t), scramble('04:14:08', t), { glitch: 0.5 + g });
    } else {
      const k = E.out(prog(t, flip, 0.3));
      h += `<g transform="${at(540, 680, 1 + 0.08 * (1 - k))}">${clock(470, '13.12.1901', '21:45:52', { red: true })}</g>`;
      h += chip(540, 1010, '😱 JAHR 1901?!', t, flip + 0.05, { bg: C.red, s: 56, w: 560, r: -3 });
      S.shake = t - flip < 0.3 ? 0.6 * (1 - (t - flip) / 0.3) : 0;
    }
    h += T(540, 390, 'DAS JAHR-2038-PROBLEM', { s: 54, f: C.yel });
    out(S, `<g transform="translate(${S.shake ? Math.sin(t * 90) * 14 * S.shake : 0},0)">${h}</g>`);
  };

  // s02: Sekunden seit 1970
  shots.s02 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 1.4);
    const p = E.inOut(clamp((t - seg.start - 0.2) / Math.max(1.5, seg.end - seg.start - 0.6)));
    let h = T(540, 400, 'UNIX-ZEIT', { s: 64, f: C.cyan });
    h += T(540, 465, 'Sekunden seit dem 01.01.1970', { s: 42, f: C.grey });
    h += `<line x1="150" y1="700" x2="930" y2="700" stroke="${C.line}" stroke-width="10" stroke-linecap="round"/>`;
    h += `<line x1="150" y1="700" x2="${150 + 780 * p}" y2="700" stroke="${C.cyan}" stroke-width="10" stroke-linecap="round" filter="url(#gl)"/>`;
    h += `<circle cx="${150 + 780 * p}" cy="700" r="22" fill="${C.yel}" stroke="#0B1022" stroke-width="5"/>`;
    h += T(150, 790, '1970', { s: 48, f: C.w }) + T(930, 790, 'HEUTE', { s: 48, f: C.w });
    h += T(150, 640, '0', { s: 52, f: C.yel, m: true });
    h += T(540, 980, de(Math.round(NOW * p)), { s: 96, f: C.yel, m: true });
    h += T(540, 1050, 'Sekunden', { s: 44, f: C.grey });
    out(S, h);
  };

  // s03: heute fast 1,8 Milliarden
  shots.s03 = (S, t, seg) => {
    const d = cue('s03', 'ding');
    const n = NOW + Math.floor((t - seg.start) * 1);
    let h = T(540, 470, 'HEUTE (17.11.2026)', { s: 46, f: C.grey });
    h += `<g transform="${at(540, 650, pop(t, seg.start, 0.3))}">${T(540, 690, de(n), { s: 120, f: C.yel, m: true })}</g>`;
    h += T(540, 790, 'Sekunden seit 1970', { s: 44, f: C.grey });
    h += chip(540, 960, '≈ 1,8 MILLIARDEN', t, Math.min(d, seg.start + 1.2), { bg: C.cyan, fg: '#0B1022', s: 56, w: 580 });
    out(S, h);
  };

  // 32-Bit-Register
  const reg = (y, bits, o = {}) => {
    const s = 108, x0 = 540 - 4 * s;
    let h = '';
    for (let i = 0; i < 32; i++) {
      const r = Math.floor(i / 8), c = i % 8, b = bits[i];
      const sign = i === 0;
      const fill = b === '1' ? (sign && o.redSign ? C.red : C.cyan) : '#1A2350';
      h += `<rect x="${x0 + c * s + 5}" y="${y + r * s + 5}" width="${s - 10}" height="${s - 10}" rx="14" fill="${fill}" stroke="${sign ? C.yel : '#3A4C8A'}" stroke-width="${sign ? 6 : 3}"/>`;
      h += T(x0 + c * s + s / 2, y + r * s + s / 2 + 21, b, { s: 58, f: b === '1' ? '#0B1022' : C.grey, m: true });
    }
    if (o.signLabel) h += T(x0 + 54, y - 22, '↓ Vorzeichen', { s: 34, f: C.yel, a: 'start' });
    return h;
  };

  // s04: 32 Bit, Maximum
  shots.s04 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 2.0);
    const max = t >= c2;
    let h = chip(540, 300, '32 BIT', t, seg.start, { bg: C.cyan, fg: '#0B1022', s: 56, w: 300 });
    h += reg(420, max ? bits32(MAX) : bits32(NOW), { signLabel: max });
    h += T(540, 990, max ? de(MAX) : de(NOW), { s: 92, f: max ? C.red : C.yel, m: true });
    h += T(540, 1060, max ? 'größte Zahl in 32 Bit' : 'heute', { s: 44, f: C.grey });
    if (max) h += chip(540, 1190, 'MAXIMUM = 19.01.2038', t, c2 + 0.2, { bg: C.red, s: 46, w: 640 });
    out(S, h);
  };

  // s05: +1 -> negativ
  shots.s05 = (S, t, seg) => {
    const st = cue('s05', 'sting');
    const ripple = clamp((t - st + 0.35) / 0.35);
    const flipped = Math.floor(ripple * 32);
    let bits = bits32(MAX).split('');
    for (let i = 0; i < flipped; i++) { const j = 31 - i; bits[j] = j === 0 ? '1' : '0'; }
    bits = bits.join('');
    const neg = flipped >= 32;
    let h = chip(540, 300, '+1 SEKUNDE', t, seg.start + 0.1, { bg: C.yel, fg: '#0B1022', s: 52, w: 420 });
    h += reg(420, bits, { signLabel: true, redSign: neg });
    h += T(540, 990, neg ? '−2.147.483.648' : de(MAX), { s: 92, f: neg ? C.red : C.w, m: true });
    if (neg) h += chip(540, 1130, 'NEGATIV!', t, st, { bg: C.red, s: 56, w: 380, r: 3 });
    S.shake = neg && t - st < 0.35 ? 0.5 : 0;
    out(S, `<g transform="translate(${S.shake ? Math.sin(t * 90) * 12 : 0},0)">${h}</g>`);
  };

  // s06: Zeitstrahl 2038 -> 1901
  shots.s06 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 2.4);
    const x = (yr) => 120 + (yr - 1901) / (2038 - 1901) * 840;
    const jump = E.inOut(clamp((t - seg.start - 0.4) / 1.4));
    const cx = lerp(x(2038), x(1901), jump);
    let h = `<line x1="100" y1="760" x2="980" y2="760" stroke="${C.line}" stroke-width="10" stroke-linecap="round"/>`;
    for (const [yr, lab] of [[1901, '1901'], [1970, '1970'], [2026, 'heute'], [2038, '2038']]) {
      h += `<line x1="${x(yr)}" y1="735" x2="${x(yr)}" y2="785" stroke="${C.grey}" stroke-width="6"/>` + T(x(yr), yr === 2026 ? 700 : 850, lab, { s: yr === 2026 ? 36 : 44, f: yr === 1901 ? C.red : yr === 2026 ? C.grey : C.w });
    }
    h += `<path d="M ${x(2038)} 730 Q ${(x(2038) + cx) / 2} ${560 - 120 * Math.sin(Math.PI * jump)} ${cx} 730" fill="none" stroke="${C.red}" stroke-width="7" stroke-dasharray="16 10" opacity="${jump > 0.02 ? 0.9 : 0}"/>`;
    h += `<circle cx="${cx}" cy="760" r="26" fill="${C.red}" stroke="#0B1022" stroke-width="6" filter="url(#gl)"/>`;
    h += T(540, 470, '−2,1 MILLIARDEN SEKUNDEN', { s: 56, f: C.red });
    h += T(540, 540, 'zurück ab 1970', { s: 44, f: C.grey });
    if (t >= c2) h += `<g transform="${at(540, 1010, pop(t, c2, 0.3), -2)}">${T(540, 1040, '📅 13.12.1901', { s: 96, f: C.w, st: '#0B1022', sw: 12 })}</g>`;
    out(S, h);
  };

  // s07: 64 Bit
  shots.s07 = (S, t, seg) => {
    const kc = cue('s07', 'kaching');
    const fill = clamp((t - seg.start - 0.1) / 1.2);
    const nb = Math.floor(fill * 64), s = 80, x0 = 540 - 4 * s, y0 = 380;
    let h = chip(540, 300, '64 BIT', t, seg.start, { bg: C.grn, fg: '#0B1022', s: 56, w: 300 });
    for (let i = 0; i < 64; i++) {
      const r = Math.floor(i / 8), c = i % 8;
      h += `<rect x="${x0 + c * s + 4}" y="${y0 + r * s + 4}" width="${s - 8}" height="${s - 8}" rx="12" fill="${i < nb ? C.grn : '#1A2350'}" opacity="${i < nb ? 0.9 : 1}"/>`;
    }
    const k = pop(t, Math.min(kc - 0.4, seg.start + 1.6), 0.3);
    if (k > 0) h += `<g transform="${at(540, 1100, k)}"><rect x="90" y="1030" width="900" height="150" rx="40" fill="#0B1022" stroke="${C.grn}" stroke-width="8"/>${T(540, 1130, '✅ 292 MILLIARDEN JAHRE', { s: 66, f: C.grn })}</g>`;
    out(S, h);
  };

  // s08: modern vs. alt
  shots.s08 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 1.4);
    const card = (x, title, sub, emo, col, t0) => {
      const k = pop(t, t0, 0.3);
      return `<g transform="${at(x, 720, k, x < 540 ? -3 : 3)}"><rect x="${x - 215}" y="520" width="430" height="400" rx="40" fill="${C.panel}" stroke="${col}" stroke-width="8"/>${T(x, 650, emo, { s: 110 })}${T(x, 770, title, { s: 50, f: C.w })}${T(x, 840, sub, { s: 42, f: col })}</g>`;
    };
    let h = card(300, 'NEUE SYSTEME', 'schon 64 Bit', '✅', C.grn, seg.start + 0.1);
    h += card(780, 'ALTE GERÄTE', 'teils noch 32 Bit', '⚠️', C.yel, c2);
    out(S, h);
  };

  // s09: Folgen
  shots.s09 = (S, t, seg) => {
    const k = pop(t, seg.start, 0.35);
    let h = `<g transform="${at(540, 600, k)}">${T(540, 560, '🔍', { s: 200 })}${T(540, 720, 'TECH-LUPE', { s: 120, f: C.cyan, st: '#0B1022', sw: 14 })}</g>`;
    h += `<g opacity="${clamp((t - seg.start - 0.3) * 4)}">${T(540, 810, 'Informatik in 30 Sekunden', { s: 52, f: C.w })}</g>`;
    const b = pop(t, seg.start + 0.5) * (1 + 0.05 * Math.max(0, Math.sin(t * 9)));
    if (b > 0) h += `<g transform="${at(540, 950, b)}"><rect x="320" y="895" width="440" height="110" rx="55" fill="${C.red}" stroke="#0B1022" stroke-width="8"/>${T(540, 970, '+ FOLGEN', { s: 60 })}</g>`;
    h += chip(540, 1150, 'WELCHES THEMA ALS NÄCHSTES? 👇', t, seg.start + 1.1, { bg: C.yel, fg: '#0B1022', s: 42, w: 820, r: -2 });
    out(S, h);
  };

  // Titelbild: Uhr auf 1901
  shots.cover = (S) => out(S, `<g transform="translate(0,250)">${clock(470, '13.12.1901', '21:45:52', { red: true, label: 'SYSTEMZEIT NACH 19.01.2038' })}</g>`);

  Engine.start({
    world: () => '',
    alt: statics,
    drawAlt: (S) => { $('dyn').innerHTML = S.html || ''; },
    drawWorld: () => {},
    shots,
    baseState: () => ({ layer: 'alt', html: '' }),
    highlight: '#3DDCFF',
    whip: { skip: [] },
    karaoke: true,
    punch: 0.05,
    preload: '🔍😱⚠️✅📅↓−≈👇',
    ui: {
      day: '', profile: { name: 'Tech-Lupe', handle: '@techlupe', avatar: '🔍', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

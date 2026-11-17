// Tech-Lupe – Testvideo „0,1 + 0,2“: reine Bewegtgrafik im Bildschirm-Raum (Ebene „alt“), keine Figuren.
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

  const RES = '0.30000000000000004';
  const BITS01 = '0011111110111001100110011001100110011001100110011001100110011010'; // 0.1 als double (0x3FB999999999999A)
  const shots = {};
  const out = (S, html) => { S.layer = 'alt'; S.html = html; };

  // s01: Terminal, 0.1 + 0.2 -> 0.30000000000000004
  const terminal = (t, t0, opts = {}) => {
    const lt = t - t0;
    const full = opts.full;
    const n = full ? RES.length : Math.max(0, Math.min(RES.length, Math.floor((lt - 0.15) / 0.026)));
    const done = full || n === RES.length;
    const tDone = t0 + 0.15 + RES.length * 0.026;
    const shake = !full && done && t - tDone < 0.35 ? Math.sin(t * 80) * 10 * (1 - (t - tDone) / 0.35) : 0;
    let h = panel(70, 420, 940, 640, 'python3');
    h += `<g transform="translate(${shake},0)">`;
    h += T(118, 610, '>>>', { a: 'start', s: 66, f: C.grn, m: true }) + T(285, 610, '0.1 + 0.2', { a: 'start', s: 66, m: true });
    const body = RES.slice(0, Math.min(n, RES.length - 1)), four = n === RES.length;
    h += `<text x="118" y="760" class="m" font-size="72" fill="${C.w}">${body}${four ? `<tspan fill="${C.red}">4</tspan>` : ''}</text>`;
    if (!done && Math.floor(t * 3) % 2 === 0) h += `<rect x="${118 + n * 43.2}" y="704" width="38" height="68" fill="${C.cyan}"/>`;
    if (four) {
      const k = full ? 1 : E.out(prog(t, tDone, 0.4));
      h += `<ellipse cx="${118 + 18.5 * 43.2}" cy="736" rx="${44 * k}" ry="${58 * k}" fill="none" stroke="${C.red}" stroke-width="8" filter="url(#gl)"/>`;
    }
    h += '</g>';
    const kc = full ? 1 : pop(t, tDone + 0.35);
    if (kc > 0) h += `<g opacity="${clamp(kc)}">${T(118, 900, '# erwartet: 0.3', { a: 'start', s: 54, f: C.grey, m: true })}</g>`;
    const ke = full ? 1 : pop(t, tDone + 0.15, 0.3);
    if (ke > 0) h += `<g transform="${at(890, 480, ke, 12)}">${T(890, 520, '🤯', { s: 130 })}</g>`;
    return h;
  };
  shots.s01 = (S, t, seg) => {
    const z = 1.02 + 0.05 * clamp((t - seg.start) / 3);
    out(S, `<g transform="${at(540, 740, z)}">${terminal(t, seg.start)}</g>`);
  };

  // s02: Nullen zählen
  shots.s02 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 0.8), c2 = caps(seg, 2, seg.start + 2.2);
    const cw = 50.4, x0 = 540 - (RES.length * cw) / 2, y = 760;
    let h = '';
    const sweep = clamp((t - c1) / Math.max(0.6, c2 - c1 - 0.1));
    const lit = Math.floor(sweep * 15 + 1e-6);
    for (let i = 3; i < 3 + lit; i++) h += `<rect x="${x0 + i * cw + 2}" y="${y - 70}" width="${cw - 4}" height="92" rx="10" fill="${C.yel}" opacity=".9"/>`;
    h += `<text x="${x0}" y="${y}" class="m" font-size="84" fill="${C.w}">${RES.slice(0, 3)}<tspan fill="${lit > 0 ? '#0B1022' : C.w}">${'0'.repeat(15)}</tspan><tspan fill="${C.red}">4</tspan></text>`;
    if (lit > 0) h += chip(540, 960, `${lit} NULLEN`, t, c1, { bg: C.yel, fg: '#0B1022', s: 56, w: 420, r: -3 });
    const k = t >= c2 ? E.out(prog(t, c2, 0.35)) : 0;
    if (k > 0) {
      const cx = x0 + 18.5 * cw;
      h += `<circle cx="${cx}" cy="${y - 26}" r="${70 * k}" fill="none" stroke="${C.red}" stroke-width="10" filter="url(#gl)"/>`;
      h += `<g transform="${at(cx - 40, 560, pop(t, c2 + 0.1), -6)}">${T(cx - 40, 560, 'DIE 4?! 😳', { s: 64, f: C.red, st: '#0B1022', sw: 12 })}</g>`;
    }
    h += T(540, 470, 'ERGEBNIS IM COMPUTER', { s: 44, f: C.grey });
    out(S, h);
  };

  // s03: Binärsystem
  shots.s03 = (S, t, seg) => {
    const R = rng(3); const cells = [];
    for (let r = 0; r < 10; r++) for (let c = 0; c < 9; c++) cells.push({ x: 108 + c * 108, y: 350 + r * 92, ph: R(), sp: 2 + R() * 5 });
    let h = '<g opacity=".9">';
    for (const c of cells) {
      const b = Math.floor(t * c.sp + c.ph * 10) % 2;
      const glow = (Math.sin(t * c.sp + c.ph * 6) + 1) / 2;
      h += T(c.x, c.y, String(b), { s: 70, f: b ? C.cyan : '#3A4C8A', m: true, op: (0.35 + 0.65 * glow).toFixed(2) });
    }
    h += '</g>';
    const k = pop(t, seg.start + 0.1, 0.3);
    h += `<g transform="${at(540, 760, k, -2)}"><rect x="160" y="650" width="760" height="200" rx="40" fill="#0B1022" stroke="${C.cyan}" stroke-width="8" filter="url(#gl)"/>${T(540, 735, 'BINÄRSYSTEM', { s: 74, f: C.cyan })}${T(540, 815, 'nur 0 und 1', { s: 54, f: C.w, m: true })}</g>`;
    out(S, h);
  };

  // Lauftext für endlose Kommazahlen
  const marquee = (y, prefix, digits, t, t0, o = {}) => {
    const cw = (o.s || 84) * 0.6, per = o.per || 0.09;
    const n = Math.max(0, Math.floor((t - t0) / per));
    let s = '';
    for (let i = 0; i < n + 1; i++) s += digits[i % digits.length];
    const maxN = Math.ceil((1000 - 90) / cw) - prefix.length + 1;
    s = s.slice(0, maxN);
    const col = o.colorize ? s.split('').map((ch, i) => `<tspan fill="${Math.floor(i / 4) % 2 ? C.cyan : C.w}">${ch}</tspan>`).join('') : s;
    return `<g clip-path="url(#lane)" mask="url(#fadeR)"><text x="90" y="${y}" class="m" font-size="${o.s || 84}" fill="${o.f || C.w}">${prefix}${col}</text></g>`;
  };

  // s04: 1/3
  shots.s04 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 1.8);
    let h = `<g transform="${at(540, 520, pop(t, seg.start, 0.3))}">${T(540, 560, '1 ÷ 3 =', { s: 130, f: C.yel })}</g>`;
    h += marquee(760, '0,', '3', t, seg.start + 0.25, { per: 0.09, f: C.w });
    h += `<rect x="70" y="680" width="80" height="110" fill="url(#bgG)" opacity="0"/>`;
    h += chip(540, 960, '♾️ HÖRT NIE AUF', t, c2, { bg: C.red, s: 54, w: 560, r: -3 });
    h += T(540, 1130, 'Dezimalsystem', { s: 44, f: C.grey });
    out(S, h);
  };

  // s05: 0,1 binär
  shots.s05 = (S, t, seg) => {
    const k = pop(t, seg.start, 0.3);
    let h = `<g transform="${at(540, 480, k)}">${T(540, 520, '0,1', { s: 150, f: C.yel })}${T(540, 590, 'dezimal', { s: 44, f: C.grey })}</g>`;
    h += T(540, 700, '⬇', { s: 70, f: C.cyan });
    h += marquee(860, '0,0', '0011', t, seg.start + 0.3, { per: 0.07, s: 76, colorize: true });
    h += T(540, 960, 'binär', { s: 44, f: C.grey });
    h += chip(540, 1110, '♾️ AUCH ENDLOS', t, seg.start + 1.4, { bg: C.red, s: 52, w: 540, r: 3 });
    out(S, h);
  };

  // s06: 64 Bit, abschneiden
  shots.s06 = (S, t, seg) => {
    const cut = cue('s06', 'scratch'), drop = cue('s06', 'card');
    const fill = clamp((t - seg.start - 0.1) / Math.max(0.8, cut - seg.start - 0.5));
    const nb = Math.floor(fill * 64);
    let h = chip(540, 300, '64 BIT', t, seg.start, { bg: C.cyan, fg: '#0B1022', s: 56, w: 300 });
    const s = 84, x0 = 540 - 4 * s, y0 = 370;
    for (let i = 0; i < 64; i++) {
      const r = Math.floor(i / 8), c = i % 8, on = i < nb;
      h += `<rect x="${x0 + c * s + 5}" y="${y0 + r * s + 5}" width="${s - 10}" height="${s - 10}" rx="14" fill="${on ? (BITS01[i] === '1' ? C.cyan : '#22305E') : '#151D3D'}" stroke="${on ? '#5E7BD6' : '#24305C'}" stroke-width="3"/>`;
      if (on) h += T(x0 + c * s + s / 2, y0 + r * s + s / 2 + 17, BITS01[i], { s: 46, f: BITS01[i] === '1' ? '#0B1022' : C.grey, m: true });
    }
    // Überlauf: was nicht mehr reinpasst
    if (nb >= 64) {
      const fall = t > drop ? (t - drop) : 0;
      const y = 1120 + 900 * fall * fall, op = clamp(1 - fall * 1.6);
      h += `<g opacity="${op}" transform="rotate(${fall * 12} 540 ${y})">${T(540, y, '1001100110011…', { s: 70, f: C.red, m: true })}</g>`;
      if (t > cut - 0.05) {
        const sx = lerp(80, 1000, E.inOut(prog(t, cut - 0.05, 0.4)));
        h += T(sx, 1100, '✂️', { s: 90, tr: 'rotate(-90 ' + sx + ' 1072)' });
        h += `<line x1="70" y1="1062" x2="${sx}" y2="1062" stroke="${C.red}" stroke-width="6" stroke-dasharray="18 12"/>`;
      }
      if (t > drop) h += chip(540, 1210, 'ABGESCHNITTEN!', t, drop, { bg: C.red, s: 50, w: 520, r: -3 });
    }
    out(S, h);
  };

  // s07: Reste -> Ergebnis
  shots.s07 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1.2);
    let h = T(540, 360, 'SO SPEICHERT ER ES WIRKLICH:', { s: 44, f: C.grey });
    const row = (y, a, z, tail, t0) => {
      const k = pop(t, t0, 0.3);
      return `<g opacity="${clamp(k * 2)}" transform="translate(${(1 - k) * 60},0)">${T(90, y, a, { a: 'start', s: 64, f: C.yel })}<text x="270" y="${y}" class="m" font-size="56" fill="${C.w}">${z}<tspan fill="${C.red}">${tail}</tspan></text></g>`;
    };
    h += row(500, '0,1 ≈', '0,10000000000000000', '55…', seg.start + 0.05);
    h += row(620, '0,2 ≈', '0,20000000000000001', '11…', seg.start + 0.35);
    h += `<line x1="90" y1="680" x2="990" y2="680" stroke="${C.line}" stroke-width="6"/>`;
    const k = t >= c1 ? E.out(prog(t, c1, 0.35)) : 0;
    if (k > 0) {
      h += `<g transform="${at(540, 820, 0.7 + 0.3 * k)}" opacity="${k}"><text x="540" y="840" text-anchor="middle" class="m" font-size="80" fill="${C.w}">0,3000000000000000<tspan fill="${C.red}" filter="url(#gl)">4</tspan></text></g>`;
      const p = E.inOut(prog(t, c1 - 0.3, 0.5));
      h += `<path d="M 960 520 Q 1060 700 ${lerp(960, 905, p)} ${lerp(520, 790, p)}" fill="none" stroke="${C.red}" stroke-width="6" stroke-dasharray="14 10" opacity=".85"/>`;
      h += `<path d="M 940 640 Q 1010 740 ${lerp(940, 905, p)} ${lerp(640, 790, p)}" fill="none" stroke="${C.red}" stroke-width="6" stroke-dasharray="14 10" opacity=".85"/>`;
    }
    h += chip(540, 1050, 'WINZIGER REST = DIE 4', t, c1 + 0.4, { bg: C.red, s: 48, w: 680, r: -2 });
    out(S, h);
  };

  // s08: Banken rechnen in Cent
  shots.s08 = (S, t, seg) => {
    const kc = cue('s08', 'kaching');
    let h = `<g transform="${at(540, 430, pop(t, seg.start, 0.3))}">${T(540, 480, '🏦', { s: 150 })}</g>`;
    const card = (x, top, big, small, col, mark, t0) => {
      const k = pop(t, t0, 0.3);
      return `<g transform="${at(x, 740, k, x < 540 ? -3 : 3)}"><rect x="${x - 200}" y="600" width="400" height="280" rx="34" fill="${C.panel}" stroke="${col}" stroke-width="8"/>${T(x, 660, top, { s: 36, f: C.grey })}${T(x, 770, big, { s: 78, f: C.w, m: true })}${T(x, 850, small, { s: 46, f: col })}${T(x + 170, 625, mark, { s: 80 })}</g>`;
    };
    h += card(285, 'KOMMAZAHL', '10,50 €', 'ungenau', C.red, '⚠️', seg.start + 0.2);
    h += T(540, 760, '➜', { s: 90, f: C.cyan, op: clamp((t - seg.start - 0.6) * 4) });
    h += card(795, 'GANZE ZAHL', '1050', 'Cent, exakt', C.grn, '✅', seg.start + 0.9);
    h += chip(540, 1040, 'GANZE ZAHLEN = KEINE RESTE', t, Math.min(kc, seg.start + 1.6), { bg: C.grn, fg: '#0B1022', s: 44, w: 720, r: -2 });
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

  // Titelbild: Terminal fertig
  shots.cover = (S, t) => out(S, `<g transform="translate(0,120)">${terminal(t, 0, { full: true })}</g>`);

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
    preload: '🔍🤯😳♾️✂️🏦⚠️✅➜⬇👇≈÷',
    ui: {
      day: '', profile: { name: 'Tech-Lupe', handle: '@techlupe', avatar: '🔍', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

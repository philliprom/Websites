// Tech-Lupe – Folge 3 „So funktioniert ChatGPT wirklich“: reine Bewegtgrafik im Bildschirm-Raum (Ebene „alt“).
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
`;

  const shots = {};
  const out = (S, html) => { S.layer = 'alt'; S.html = html; };

  const NAVY = '#0B1022';
  // Sprechblasen
  const bubble = (side, y, txt, o = {}) => {
    const fs = o.s || 50, w = Math.min(860, (o.w || txt.length * fs * 0.52) + 70), h = fs * 1.9;
    const x = side === 'r' ? 1000 - w : 80;
    const fill = side === 'r' ? C.cyan : '#23305E', col = side === 'r' ? NAVY : C.w;
    let g = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2.4}" fill="${fill}" stroke="${o.stroke || 'none'}" stroke-width="6"/>`;
    g += `<text x="${x + 35}" y="${y + h * 0.66}" font-size="${fs}" fill="${col}">${o.raw ? txt : esc(txt)}</text>`;
    if (side === 'l') g += T(x - 2, y - 14, o.who || '🤖 KI', { s: 34, f: C.grey, a: 'start' });
    return g;
  };
  const chatPanel = (y, h) => `<g filter="url(#sh)"><rect x="50" y="${y}" width="980" height="${h}" rx="40" fill="${C.panel}" stroke="${C.line}" stroke-width="5"/></g>`;
  const typed = (s, t, t0, cps = 16) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps))));
  const cursor = (t) => (Math.floor(t * 3) % 2 ? '' : '<tspan fill="#3DDCFF">▌</tspan>');
  const bars = (y0, rows, t, t0, o = {}) => {
    let h = '';
    rows.forEach(([w, p], i) => {
      const k = E.out(clamp((t - t0 - i * 0.18) / 0.45));
      const y = y0 + i * 100, hi = o.hi === i;
      h += T(300, y + 46, w, { s: 52, f: hi ? C.yel : C.w, a: 'end', m: true });
      h += `<rect x="330" y="${y}" width="440" height="64" rx="18" fill="#1A2350"/>`;
      h += `<rect x="330" y="${y}" width="${440 * p / 100 * k}" height="64" rx="18" fill="${hi ? C.yel : C.cyan}"${hi ? ' filter="url(#gl)"' : ''}/>`;
      h += T(905, y + 46, `${Math.round(p * k)} %`, { s: 44, f: C.w, a: 'end', m: true, op: k.toFixed(2) });
    });
    h += T(540, y0 + rows.length * 100 + 30, 'Beispielwerte', { s: 32, f: C.grey });
    return h;
  };
  const P1 = [['blau', 62], ['oft', 14], ['heute', 9], ['grau', 7], ['voller', 3]];
  const P2 = [['.', 48], ['und', 21], [',', 14], ['–', 6]];

  // s01: Chat, die KI schreibt, nächstes Wort?
  shots.s01 = (S, t, seg) => {
    const st = cue('s01', 'sting');
    let h = T(540, 330, 'WAS CHATGPT WIRKLICH MACHT', { s: 54, f: C.yel });
    h += chatPanel(370, 580);
    h += bubble('r', 420, 'Erzähl mir was über den Himmel.', { s: 50, w: 780 });
    const ans = typed('Der Himmel ist', t, seg.start, 10);
    const ask = t >= st;
    h += bubble('l', 640, `${esc(ans)}${ask ? ' <tspan fill="#FFD43B">???</tspan>' : cursor(t)}`, { raw: true, s: 72, w: 820, stroke: ask ? C.yel : 'none' });
    if (ask) h += chip(540, 1050, '🎲 NÄCHSTES WORT?', t, st, { bg: C.yel, fg: NAVY, s: 54, w: 640, r: -3 });
    out(S, h);
  };

  // s02: Wahrscheinlichkeiten
  shots.s02 = (S, t, seg) => {
    let h = chatPanel(250, 230) + bubble('l', 320, 'Der Himmel ist <tspan fill="#FFD43B">???</tspan>', { raw: true, s: 56, w: 640 });
    h += bars(600, P1, t, seg.start + 0.6);
    out(S, h);
  };

  // s03: eins auswählen, anhängen, von vorn
  shots.s03 = (S, t, seg) => {
    const pick = seg.start + 0.45, add = cue('s03', 'pop'), loop = cue('s03', 'blip');
    let h = chatPanel(250, 230);
    if (t < add) {
      const kk = t >= pick ? E.inOut(prog(t, pick, add - pick)) : 0;
      h += bubble('l', 320, `Der Himmel ist <tspan fill="#FFD43B" opacity="${(1 - clamp((kk - 0.6) / 0.3)).toFixed(2)}">???</tspan>`, { raw: true, s: 56, w: 640 });
      h += bars(600, P1, t, seg.start - 5, { hi: t >= pick ? 0 : null });
      if (t >= pick) {
        const k = E.inOut(prog(t, pick, add - pick));
        h += `<g transform="translate(${lerp(0, 323, k)},${lerp(0, -256, k)})">${T(300, 646, 'blau', { s: 52, f: C.yel, a: 'end', m: true })}</g>`;
      }
    } else {
      h += bubble('l', 320, 'Der Himmel ist <tspan fill="#FFD43B">blau</tspan> <tspan fill="#FFD43B">???</tspan>', { raw: true, s: 56, w: 820 });
      h += bars(600, P2, t, add + 0.2);
    }
    if (t >= loop - 0.1) {
      const k = E.out(prog(t, loop - 0.1, 0.5));
      h += `<g transform="${at(820, 1110, k)}"><circle cx="820" cy="1110" r="62" fill="${C.grn}" stroke="${NAVY}" stroke-width="7"/>${T(820, 1138, '↻', { s: 84, f: NAVY })}</g>`;
      h += chip(520, 1110, 'VON VORN', t, loop - 0.1, { bg: C.grn, fg: NAVY, s: 46, w: 330 });
    }
    out(S, h);
  };

  // s04: Training
  shots.s04 = (S, t, seg) => {
    const c3 = caps(seg, 3, seg.start + 2.4);
    let h = '';
    const R = rng(4);
    for (let i = 0; i < 18; i++) {
      const ph = R(), lane = R();
      const k = ((t - seg.start) * 0.9 + ph) % 1;
      const x = lerp(60, 440, k), y = 420 + lane * 560 + Math.sin(k * 6 + i) * 20;
      h += T(x, y, '📄', { s: 64, op: (Math.min(k * 4, 1) * (1 - Math.max(0, k - 0.8) * 5)).toFixed(2) });
    }
    h += T(260, 360, 'Riesige Mengen Text', { s: 40, f: C.grey });
    h += `<g filter="url(#sh)"><rect x="520" y="420" width="390" height="560" rx="40" fill="#0A0F24" stroke="${C.cyan}" stroke-width="7"/></g>`;
    h += T(715, 490, 'SPRACHMODELL', { s: 38, f: C.cyan });
    const R2 = rng(9);
    for (let r = 0; r < 9; r++) for (let c = 0; c < 3; c++) {
      const v = (Math.sin(t * (2 + R2() * 4) + R2() * 10) * 2).toFixed(2);
      h += T(600 + c * 115, 560 + r * 46, v, { s: 28, f: v < 0 ? C.red : C.grn, m: true, op: 0.85 });
    }
    h += chip(560, 1100, 'MILLIARDEN ZAHLEN', t, c3, { bg: C.cyan, fg: NAVY, s: 44, w: 520, r: -2 });
    out(S, h);
  };

  // s05: passend ≠ wahr
  shots.s05 = (S, t, seg) => {
    const c3 = caps(seg, 3, seg.start + 2.0), nq = cue('s05', 'card');
    let h = `<g transform="${at(540, 560, pop(t, seg.start + 0.1, 0.3))}">${T(540, 590, 'PASSEND ✅', { s: 120, f: C.grn, st: NAVY, sw: 14 })}</g>`;
    if (t >= Math.min(c3, nq) - 0.1) {
      h += `<g transform="${at(540, 760, pop(t, Math.min(c3, nq) - 0.1, 0.3), -4)}">${T(540, 800, '≠', { s: 150, f: C.red, st: NAVY, sw: 14 })}</g>`;
      h += `<g transform="${at(540, 940, pop(t, Math.min(c3, nq), 0.3))}">${T(540, 980, 'WAHR ❓', { s: 120, f: C.w, st: NAVY, sw: 14 })}</g>`;
    }
    out(S, h);
  };

  // s06: überzeugend falsch
  shots.s06 = (S, t, seg) => {
    const sp = cue('s06', 'stamp');
    let h = chatPanel(300, 640);
    h += bubble('r', 360, 'Hauptstadt von Australien?', { s: 48 });
    h += bubble('l', 580, `${esc(typed('Ganz klar: Sydney! 😎', t, seg.start + 0.2, 14))}`, { raw: true, s: 60, w: 720 });
    if (t >= sp) {
      const k = E.out(prog(t, sp, 0.18));
      h += `<g transform="translate(760,800) rotate(-10) scale(${lerp(2.4, 1, k)})" opacity="${clamp(k * 2)}"><rect x="-200" y="-70" width="400" height="140" rx="20" fill="none" stroke="${C.red}" stroke-width="12"/>${T(0, 28, 'FALSCH', { s: 84, f: C.red })}</g>`;
      h += chip(540, 1060, '✅ Richtig: Canberra', t, sp + 0.35, { bg: C.grn, fg: NAVY, s: 50, w: 560 });
      h += T(540, 1180, 'Beispiel', { s: 32, f: C.grey, op: clamp((t - sp - 0.35) * 4) });
    }
    out(S, h);
  };

  // s07: selbst prüfen
  shots.s07 = (S, t, seg) => {
    let h = `<g transform="${at(540, 520, pop(t, seg.start, 0.3))}">${T(540, 580, '🔍', { s: 180 })}</g>`;
    ['Quelle suchen', 'Zweite Quelle', 'Nachrechnen'].forEach((txt, i) => {
      const t0 = seg.start + 0.5 + i * 0.4, k = pop(t, t0, 0.25);
      if (k > 0) h += `<g transform="${at(540, 780 + i * 120, k)}"><rect x="250" y="${730 + i * 120}" width="580" height="96" rx="30" fill="${C.panel}" stroke="${C.grn}" stroke-width="6"/>${T(300, 795 + i * 120, '✅', { s: 50, a: 'start' })}${T(380, 795 + i * 120, txt, { s: 50, a: 'start' })}</g>`;
    });
    out(S, h);
  };

  // s08: Folgen
  shots.s08 = (S, t, seg) => {
    const k = pop(t, seg.start, 0.35);
    let h = `<g transform="${at(540, 600, k)}">${T(540, 560, '🔍', { s: 200 })}${T(540, 720, 'TECH-LUPE', { s: 120, f: C.cyan, st: NAVY, sw: 14 })}</g>`;
    h += `<g opacity="${clamp((t - seg.start - 0.3) * 4)}">${T(540, 810, 'Informatik in 30 Sekunden', { s: 52, f: C.w })}</g>`;
    const b = pop(t, seg.start + 0.5) * (1 + 0.05 * Math.max(0, Math.sin(t * 9)));
    if (b > 0) h += `<g transform="${at(540, 950, b)}"><rect x="320" y="895" width="440" height="110" rx="55" fill="${C.red}" stroke="${NAVY}" stroke-width="8"/>${T(540, 970, '+ FOLGEN', { s: 60 })}</g>`;
    h += chip(540, 1150, 'WELCHES THEMA ALS NÄCHSTES? 👇', t, seg.start + 1.1, { bg: C.yel, fg: NAVY, s: 36, w: 700, r: -2 });
    out(S, h);
  };

  // Titelbild
  shots.cover = (S) => {
    let h = chatPanel(640, 230) + bubble('l', 710, 'Der Himmel ist <tspan fill="#FFD43B">???</tspan>', { raw: true, s: 56, w: 640 });
    h += bars(960, P1.slice(0, 3), 10, 0);
    out(S, h);
  };

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
    preload: '🔍🤖🎲📄✅❓≠😎↻▌–👇',
    ui: {
      day: '', profile: { name: 'Tech-Lupe', handle: '@techlupe', avatar: '🔍', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

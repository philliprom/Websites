// Wo geht dein Geld hin? – Folge 1 „Der 8-Euro-Döner“: Bewegtgrafik im Bildschirm-Raum (Ebene „alt“).
(() => {
  const { $, clamp, lerp, E, prog, popS, cue } = Engine;
  const C = { panel: '#13392D', line: '#2C5E4C', gold: '#FFC94A', red: '#FF5A5F', mint: '#5CE1A6', blue: '#5AB0FF', orange: '#FF9A3C',
    grey: '#9DB8AC', w: '#FFFFFF', paper: '#FFF8E8', ink: '#1B1B1B', dark: '#071510' };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const T = (x, y, s, o = {}) => `<text x="${x}" y="${y}"${o.m ? ' class="m"' : ''} text-anchor="${o.a || 'middle'}" font-size="${o.s || 60}" fill="${o.f || C.w}"${o.st ? ` stroke="${o.st}" stroke-width="${o.sw || 10}" paint-order="stroke fill" stroke-linejoin="round"` : ''}${o.op !== undefined ? ` opacity="${o.op}"` : ''}${o.tr ? ` transform="${o.tr}"` : ''}>${o.raw ? s : esc(s)}</text>`;
  const pop = (t, t0, d = 0.25) => (t0 === null || t0 === undefined || t < t0 ? 0 : popS(t, t0, d));
  const at = (x, y, s, r = 0) => `translate(${x},${y}) rotate(${r}) scale(${Math.max(0.001, s)}) translate(${-x},${-y})`;
  const chip = (x, y, txt, t, t0, o = {}) => {
    const k = pop(t, t0); if (k <= 0) return '';
    const fs = o.s || 46, w = o.w || txt.length * fs * 0.62 + 70;
    return `<g transform="${at(x, y, k, o.r || -2)}"><rect x="${x - w / 2}" y="${y - fs * 0.95}" width="${w}" height="${fs * 1.9}" rx="${fs * 0.95}" fill="${o.bg || C.red}" stroke="${C.dark}" stroke-width="7"/>${T(x, y + fs * 0.34, txt, { s: fs, f: o.fg || C.w })}</g>`;
  };
  const caps = (seg, i, fb) => (seg.caps && seg.caps[i] ? seg.caps[i].start : fb);
  const eur = (v) => `${v < 0 ? '−' : ''}${Math.abs(v).toFixed(2).replace('.', ',')} €`;
  const shots = {};
  const out = (S, html) => { S.layer = 'alt'; S.html = html; };

  const statics = () => `
    <defs>
      <radialGradient id="bgG" cx="50%" cy="38%" r="85%"><stop offset="0" stop-color="#1D4A3B"/><stop offset=".6" stop-color="#0F2A22"/><stop offset="1" stop-color="#06120D"/></radialGradient>
      <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="0" flood-color="#000" flood-opacity=".4"/></filter>
      <filter id="gl" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="1080" height="1920" fill="url(#bgG)"/>
    <g opacity=".07" fill="#FFE9A8">${Array.from({ length: 60 }, (_, i) => `<circle cx="${(i * 197) % 1080}" cy="${(i * 331) % 1920}" r="${3 + (i % 4)}"/>`).join('')}</g>
    <g id="dyn"></g>`;

  // Preisbalken: 8 € = 940 px
  const PRICE = 8, BX = 70, BW = 940, BY = 340, BH = 92;
  const PARTS = { mwst: [0.52, C.red, 'MwSt'], zut: [3.0, C.orange, 'Zutaten'], fix: [2.67, C.blue, 'Miete, Personal …'], pack: [0.1, '#C8D6CF', ''], gew: [1.71, C.mint, 'Gewinn'] };
  const ORDER = ['mwst', 'zut', 'fix', 'pack', 'gew'];
  const bar = (t, shown, o = {}) => {
    let h = `<rect x="${BX}" y="${BY}" width="${BW}" height="${BH}" rx="22" fill="#0A1E17" stroke="${C.line}" stroke-width="5"/>`;
    let x = BX;
    for (const key of ORDER) {
      const st = shown[key];
      if (st === undefined) continue;
      let [v, col, lab] = PARTS[key];
      if (o.override && o.override[key] !== undefined) v = o.override[key];
      const k = E.out(clamp((t - st) / 0.45));
      const w = (v / PRICE) * BW * k;
      if (w > 0.5) {
        h += `<rect x="${x}" y="${BY + 6}" width="${w}" height="${BH - 12}" rx="14" fill="${o.col && o.col[key] ? o.col[key] : col}"/>`;
        if (lab && w > 110) h += T(x + w / 2, BY + 60, lab, { s: 30, f: C.dark });
      }
      x += w;
    }
    if (o.rest) {
      const w = BX + BW - x;
      if (w > 4) h += `<rect x="${x}" y="${BY + 6}" width="${w}" height="${BH - 12}" rx="14" fill="none" stroke="${C.grey}" stroke-width="4" stroke-dasharray="14 10"/>` + T(x + w / 2, BY + 60, o.rest, { s: 32, f: C.grey });
    }
    h += T(BX, BY - 22, '💸 WO GEHT DEIN GELD HIN?', { s: 32, f: C.gold, a: 'start' }) + T(BX + BW, BY - 22, '8,00 €', { s: 34, f: C.gold, a: 'end' });
    return h;
  };
  const priceTag = (x, y, txt, s = 1, r = -8, col = C.gold, fs = 78) => `<g transform="translate(${x},${y}) rotate(${r}) scale(${s})">
      <path d="M -150 -70 L 110 -70 L 170 0 L 110 70 L -150 70 Z" fill="${col}" stroke="${C.dark}" stroke-width="8" stroke-linejoin="round"/>
      <circle cx="105" cy="0" r="14" fill="${C.dark}"/>${T(fs < 60 ? -38 : -20, fs * 0.33, txt, { s: fs, f: C.dark })}</g>`;

  // s01: 8 € – was bleibt?
  shots.s01 = (S, t, seg) => {
    const st = cue('s01', 'sting');
    const sw = Math.sin(t * 3) * 5;
    let h = bar(t, {}, { rest: '' });
    h += `<g transform="${at(540, 820, 1 + 0.03 * Math.sin(t * 2))}">${T(540, 920, '🥙', { s: 330 })}</g>`;
    h += `<g transform="${at(760, 640, 1 + 0.06 * Math.max(0, Math.sin(t * 6)))}">${priceTag(760, 640, '8,00 €', 1, -10 + sw)}</g>`;
    if (t >= st) h += `<g transform="${at(540, 1140, pop(t, st, 0.3), -2)}">${T(540, 1170, 'WAS BLEIBT BEIM LADEN?', { s: 56, f: C.w, st: C.dark, sw: 12 })}</g>`;
    out(S, h);
  };

  // s02: Mehrwertsteuer
  shots.s02 = (S, t, seg) => {
    const sp = cue('s02', 'stamp');
    let h = bar(t, { mwst: seg.start + 0.2 }, { rest: '' });
    h += `<g transform="${at(540, 640, pop(t, seg.start + 0.2, 0.3))}">${T(540, 690, '0,52 €', { s: 170, f: C.red, st: C.dark, sw: 14 })}</g>`;
    h += T(540, 790, 'MEHRWERTSTEUER (7 %)', { s: 54, f: C.w, op: clamp((t - seg.start - 0.4) * 4) });
    h += T(540, 860, 'seit 2026 auch im Laden 7 %', { s: 40, f: C.grey, op: clamp((t - seg.start - 0.8) * 4) });
    if (t >= sp) h += `<g transform="${at(540, 1040, pop(t, sp, 0.25), -6)}"><rect x="250" y="970" width="580" height="140" rx="22" fill="none" stroke="${C.red}" stroke-width="10"/>${T(540, 1062, '🏛️ FINANZAMT', { s: 64, f: C.red })}</g>`;
    out(S, h);
  };

  // Kassenbon
  const receipt = (x, y, w, rows, t, o = {}) => {
    const rh = o.rh || 86, hgt = 60 + rows.length * rh + (o.sum ? rh + 20 : 0);
    let h = `<g filter="url(#sh)"><path d="M ${x} ${y} H ${x + w} V ${y + hgt} ${Array.from({ length: 12 }, (_, i) => `L ${x + w - (i + 0.5) * w / 12} ${y + hgt + 16} L ${x + w - (i + 1) * w / 12} ${y + hgt}`).join(' ')} Z" fill="${C.paper}"/></g>`;
    rows.forEach((r, i) => {
      const k = pop(t, r.t0, 0.25);
      if (k <= 0) return;
      const yy = y + 60 + i * rh + 30;
      if (r.hi) h += `<rect x="${x + 14}" y="${yy - 52}" width="${w - 28}" height="${rh - 8}" rx="14" fill="${C.gold}" opacity=".55"/>`;
      h += `<g transform="${at(x + w / 2, yy - 10, k)}">${T(x + 36, yy, r.e, { s: 54, a: 'start' })}${T(x + 120, yy, r.n, { s: 50, f: C.ink, a: 'start' })}${T(x + w - 36, yy, r.v, { s: 50, f: C.ink, a: 'end', m: true })}</g>`;
    });
    if (o.sum) {
      const yy = y + 60 + rows.length * rh + 50, k = pop(t, o.sum.t0, 0.25);
      h += `<line x1="${x + 30}" y1="${yy - 60}" x2="${x + w - 30}" y2="${yy - 60}" stroke="${C.ink}" stroke-width="4" stroke-dasharray="10 8"/>`;
      if (k > 0) h += `<g transform="${at(x + w / 2, yy - 10, k)}">${T(x + 36, yy, o.sum.n, { s: 54, f: C.ink, a: 'start' })}${T(x + w - 36, yy, o.sum.v, { s: 56, f: C.red, a: 'end', m: true })}</g>`;
    }
    return h;
  };

  // s03: Zutaten
  shots.s03 = (S, t, seg) => {
    const c2 = caps(seg, 2, seg.start + 1.6);
    const ps = [0.5, 0.7, 0.9, 1.1, 1.3].map((x) => seg.start + x);
    let h = bar(t, { mwst: -9, zut: seg.start + 0.2 }, { rest: '' });
    h += receipt(160, 480, 740, [
      { e: '🥩', n: 'Fleisch (125 g)', v: '2,00 €', t0: ps[0], hi: t >= c2 },
      { e: '🫓', n: 'Brot', v: '0,38 €', t0: ps[1] },
      { e: '🥗', n: 'Salat', v: '0,39 €', t0: ps[2] },
      { e: '🥣', n: 'Soße', v: '0,15 €', t0: ps[3] },
      { e: '🌶️', n: 'Gewürze', v: '0,08 €', t0: ps[4] },
    ], t, { sum: { n: 'ZUTATEN', v: '3,00 €', t0: ps[4] + 0.3 } });
    h += T(530, 1235, 'Quelle: Verband der Dönerproduzenten', { s: 28, f: C.grey });
    out(S, h);
  };

  // s04: Rest 4,48 €
  shots.s04 = (S, t, seg) => {
    const p = [cue('s04', 'pop', 0), cue('s04', 'pop', 1), cue('s04', 'pop', 2)];
    let h = bar(t, { mwst: -9, zut: -9 }, { rest: 'REST' });
    h += `<g transform="${at(540, 600, pop(t, seg.start + 0.1, 0.3))}">${T(540, 650, '4,48 €', { s: 160, f: C.w, st: C.dark, sw: 14 })}</g>`;
    h += T(540, 740, 'bleiben übrig für …', { s: 46, f: C.grey });
    [['🏠', 'Miete'], ['👨‍🍳', 'Personal'], ['⚡', 'Strom']].forEach(([e, n], i) => {
      const k = pop(t, p[i], 0.3), x = 250 + i * 270;
      if (k > 0) h += `<g transform="${at(x, 930, k)}"><circle cx="${x}" cy="900" r="100" fill="${C.panel}" stroke="${C.blue}" stroke-width="7"/>${T(x, 932, e, { s: 90 })}${T(x, 1065, n, { s: 44 })}</g>`;
    });
    out(S, h);
  };

  // s05: Beispiel-Laden, Fixkosten pro Döner
  shots.s05 = (S, t, seg) => {
    const cd = cue('s05', 'card');
    let h = bar(t, { mwst: -9, zut: -9, fix: cd, pack: cd + 0.3 }, { rest: t < cd ? 'REST' : '' });
    const rows = [['🥙', '150 Döner am Tag'], ['🏠', 'Miete 3.000 €'], ['👨‍🍳', '2 Angestellte (Mindestlohn)'], ['⚡', 'Strom & Co. 900 €'], ['🧾', 'Sonstiges 2.300 €']];
    h += `<g filter="url(#sh)"><rect x="120" y="470" width="790" height="560" rx="34" fill="${C.panel}" stroke="${C.line}" stroke-width="6"/></g>`;
    h += T(515, 535, 'BEISPIEL-LADEN', { s: 42, f: C.gold });
    rows.forEach(([e, n], i) => {
      const k = pop(t, seg.start + 0.1 + i * 0.12, 0.25);
      if (k > 0) h += `<g opacity="${k}">${T(170, 620 + i * 76, e, { s: 50, a: 'start' })}${T(250, 620 + i * 76, n, { s: 44, a: 'start' })}</g>`;
    });
    h += T(515, 995, '= 12.000 € im Monat', { s: 48, f: C.w, op: clamp((t - seg.start - 0.8) * 4) });
    h += chip(520, 1130, '÷ 4.500 Döner = 2,67 € pro Döner', t, cd, { bg: C.blue, fg: C.dark, s: 38, w: 740 });
    out(S, h);
  };

  // s06: Gewinn
  shots.s06 = (S, t, seg) => {
    const kc = cue('s06', 'kaching');
    let h = bar(t, { mwst: -9, zut: -9, fix: -9, pack: -9, gew: seg.start + 0.15 });
    h += `<g transform="${at(540, 620, pop(t, seg.start + 0.15, 0.3))}">${T(540, 680, '1,71 €', { s: 180, f: C.mint, st: C.dark, sw: 14 })}</g>`;
    h += T(540, 780, 'GEWINN PRO DÖNER', { s: 52, f: C.w });
    h += chip(540, 900, 'VOR STEUERN', t, caps(seg, 2, seg.start + 1.4), { bg: C.gold, fg: C.dark, s: 44, w: 380 });
    if (t >= kc - 0.2) h += `<g transform="${at(540, 1080, pop(t, kc - 0.2, 0.3))}">${T(540, 1100, '👨‍🍳 davon lebt der Inhaber', { s: 54, f: C.w })}</g>`;
    out(S, h);
  };

  // s07: nur 60 Döner am Tag -> Verlust
  shots.s07 = (S, t, seg) => {
    const bo = cue('s07', 'boing');
    const k = E.inOut(clamp((t - seg.start - 0.3) / 1.6));
    const perDay = Math.round(lerp(150, 60, k));
    const fix = 12000 / (perDay * 30), gain = 4.48 - fix - 0.10;
    const neg = gain < 0;
    let h = bar(t, { mwst: -9, zut: -9, fix: -9, pack: -9, gew: gain > 0 ? -9 : undefined }, { override: { fix: Math.min(fix, 8 - 0.52 - 3 - 0.1), gew: Math.max(0, gain) }, col: { fix: neg ? C.red : C.blue } });
    h += T(540, 560, 'DÖNER PRO TAG', { s: 44, f: C.grey });
    h += T(540, 700, String(perDay), { s: 170, f: neg ? C.red : C.w, m: true });
    h += T(540, 820, `Fixkosten pro Döner: ${eur(fix)}`, { s: 46, f: C.blue });
    h += T(540, 960, eur(gain), { s: 120, f: neg ? C.red : C.mint, st: C.dark, sw: 12 });
    if (t >= bo) h += `<g transform="translate(540,1110) rotate(-8) scale(${lerp(2.2, 1, E.out(prog(t, bo, 0.18)))})" opacity="${clamp((t - bo) * 6)}"><rect x="-250" y="-70" width="500" height="140" rx="20" fill="none" stroke="${C.red}" stroke-width="12"/>${T(0, 28, 'VERLUST', { s: 84, f: C.red })}</g>`;
    out(S, h);
  };

  // s08: voller vs. leerer Laden
  shots.s08 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 0.6), c2 = caps(seg, 2, seg.start + 1.4);
    const shop = (x, title, sub, people, tag, col, t0) => {
      const k = pop(t, t0, 0.3);
      let g = `<g transform="${at(x, 760, k)}"><rect x="${x - 190}" y="470" width="380" height="560" rx="36" fill="${C.panel}" stroke="${col}" stroke-width="8"/>`;
      g += T(x, 560, title, { s: 44, f: col }) + T(x, 720, '🏪', { s: 140 }) + T(x, 850, people, { s: 62 }) + T(x, 950, sub, { s: 40, f: C.grey });
      return g + '</g>';
    };
    let h = shop(290, 'VOLLER LADEN', '150 am Tag', '🧍🧍🧍🧍', '€', C.mint, c1 - 0.2) + shop(715, 'LEERER LADEN', '60 am Tag', '🦗', '€€€', C.red, c1 + 0.1);
    if (t >= c2) {
      h += `<g transform="${at(290, 1130, pop(t, c2, 0.3))}">${priceTag(290, 1130, 'günstiger', 0.8, -6, C.mint, 48)}</g>`;
      h += `<g transform="${at(715, 1130, pop(t, c2 + 0.2, 0.3))}">${priceTag(700, 1130, 'teurer', 0.8, 6, C.red, 56)}</g>`;
    }
    out(S, h);
  };

  // s09: Was kostet er bei dir?
  shots.s09 = (S, t, seg) => {
    let h = `<g transform="${at(540, 700, 1 + 0.03 * Math.sin(t * 2))}">${T(540, 800, '🥙', { s: 280 })}</g>`;
    h += `<g transform="${at(780, 560, pop(t, seg.start + 0.1, 0.35))}">${priceTag(780, 560, '?? €', 0.9, -10 + Math.sin(t * 3) * 5)}</g>`;
    h += chip(540, 1010, 'SCHREIB DEINEN PREIS 👇', t, cue('s09', 'pop'), { bg: C.gold, fg: C.dark, s: 50, w: 700 });
    h += T(540, 1140, 'Folge für mehr Alltagspreise', { s: 40, f: C.grey, op: clamp((t - seg.start - 1.2) * 4) });
    out(S, h);
  };

  // Titelbild
  shots.cover = (S) => {
    let h = `<g transform="translate(0,360)">${bar(9, { mwst: 0, zut: 0, fix: 0, pack: 0, gew: 0 })}</g>`;
    h += T(540, 1330, '🥙', { s: 330 }) + priceTag(790, 1040, '8,00 €', 0.95, -10);
    out(S, h);
  };

  Engine.start({
    world: () => '',
    alt: statics,
    drawAlt: (S) => { $('dyn').innerHTML = S.html || ''; },
    drawWorld: () => {},
    shots,
    baseState: () => ({ layer: 'alt', html: '' }),
    highlight: '#FFC94A',
    whip: { skip: [] },
    karaoke: true,
    punch: 0.05,
    preload: '💸🥙🏛️🥩🫓🥗🥣🌶️🏠👨‍🍳⚡🧾🏪🧍🦗👇−÷',
    ui: {
      day: '', profile: { name: 'Wo geht dein Geld hin?', handle: '@wogehtdeingeld', avatar: '💸', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

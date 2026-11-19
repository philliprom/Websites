// Tech-Lupe – Folge 4 „Hub vs. Switch“: reine Bewegtgrafik im Bildschirm-Raum (Ebene „alt“).
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

  const NAVY = '#0B1022', ORANGE = '#FF9F43';
  // Geräte und Anschlüsse
  const DEV = [
    { n: 'Anna', x: 205, y: 470, c: '#FF6B9A', port: [395, 720], mac: 'A4:83:E7:2B:11:0A' },
    { n: 'Ben', x: 820, y: 470, c: '#FFD43B', port: [685, 720], mac: '3C:22:FB:90:4C:1B' },
    { n: 'Cem', x: 205, y: 1110, c: '#7CFF6B', port: [395, 860], mac: 'F0:18:98:6D:22:3C' },
    { n: 'Dana', x: 800, y: 1110, c: '#B98CFF', port: [685, 860], mac: '00:1A:2B:3C:4D:5E' },
  ];
  const BOX = [540, 790];
  const top = (d) => d.y < 790;
  const anchor = (d) => [d.x, top(d) ? d.y + 70 : d.y - 70];
  const laptop = (d, o = {}) => {
    const { x, y } = d, dim = o.dim ? 0.3 : 1;
    let h = `<g opacity="${dim}">`;
    h += `<rect x="${x - 95}" y="${y - 70}" width="190" height="125" rx="14" fill="#10172F" stroke="${d.c}" stroke-width="8"/>`;
    h += `<rect x="${x - 78}" y="${y - 54}" width="156" height="92" rx="6" fill="${d.c}" opacity=".25"/>`;
    h += `<path d="M ${x - 125} ${y + 62} L ${x + 125} ${y + 62} L ${x + 105} ${y + 84} L ${x - 105} ${y + 84} Z" fill="#2A3A6E" stroke="${d.c}" stroke-width="5"/>`;
    h += T(x, top(d) ? y - 92 : y + 140, d.n, { s: 48, f: d.c });
    if (o.badge) h += T(x + 66, y - 40, o.badge, { s: 64 });
    if (o.mail) h += envelope(x, y - 8, d.c === o.mail ? d.c : o.mail, 0.9, o.mailLabel);
    return h + '</g>';
  };
  const envelope = (x, y, col, s = 1, lab) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-46" y="-32" width="92" height="64" rx="8" fill="#fff" stroke="${col}" stroke-width="7"/><path d="M -44 -28 L 0 6 L 44 -28" fill="none" stroke="${col}" stroke-width="6"/>${lab ? `<g transform="translate(0,58)">${T(0, 12, lab, { s: 30, f: C.w })}</g>` : ''}</g>`;
  const box = (type, t, o = {}) => {
    const col = type === 'hub' ? ORANGE : type === 'switch' ? C.cyan : C.grey;
    const lab = type === 'hub' ? 'HUB' : type === 'switch' ? 'SWITCH' : '?';
    let h = `<g filter="url(#sh)"><rect x="360" y="720" width="360" height="140" rx="26" fill="#121A36" stroke="${o.red ? C.red : col}" stroke-width="9"${o.red ? ' filter="url(#gl)"' : ''}/></g>`;
    h += T(540, 812, lab, { s: 68, f: o.red ? C.red : col });
    DEV.forEach((d, i) => {
      const on = Math.sin(t * 9 + i * 1.7) > 0.2 || (o.leds && o.leds[i]);
      h += `<circle cx="${d.port[0]}" cy="${d.port[1] < 790 ? 742 : 838}" r="9" fill="${on ? C.grn : '#24305C'}"/>`;
    });
    return h;
  };
  const cables = (prog = 1) => DEV.map((d) => {
    const [ax, ay] = anchor(d), [px, py] = d.port;
    return `<line x1="${ax}" y1="${ay}" x2="${lerp(ax, px, prog)}" y2="${lerp(ay, py, prog)}" stroke="#3A4C8A" stroke-width="9" stroke-linecap="round"/>`;
  }).join('');
  // Paket entlang Gerät -> Anschluss -> Box -> Anschluss -> Gerät
  const along = (pts, k) => {
    const seg = []; let L = 0;
    for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(l); L += l; }
    let d = clamp(k) * L;
    for (let i = 0; i < seg.length; i++) { if (d <= seg[i]) { const f = seg[i] ? d / seg[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)]; } d -= seg[i]; }
    return pts[pts.length - 1];
  };
  const inPath = (d) => [anchor(d), d.port, BOX];
  const outPath = (d) => [BOX, d.port, anchor(d)];
  const packet = (t, from, to, t0, t1, col, lab) => {
    if (t < t0) return '';
    const k = clamp((t - t0) / (t1 - t0));
    if (k >= 1) return '';
    const [x, y] = along(inPath(DEV[from]).concat(outPath(DEV[to]).slice(1)), E.inOut(k));
    return envelope(x, y, col, 0.8, lab);
  };
  const inbound = (t, from, t0, t1, col, lab) => {
    if (t < t0) return '';
    const k = clamp((t - t0) / (t1 - t0));
    const [x, y] = along(inPath(DEV[from]), E.inOut(k));
    return k < 1 ? envelope(x, y, col, 0.8, lab) : '';
  };
  const outbound = (t, to, t0, t1, col, lab) => {
    if (t < t0) return '';
    const k = clamp((t - t0) / (t1 - t0));
    const [x, y] = along(outPath(DEV[to]), E.inOut(k));
    return k < 1 ? envelope(x, y, col, 0.8, lab) : '';
  };
  const net = (type, t, o = {}) => cables(o.cable === undefined ? 1 : o.cable) + box(type, t, o) +
    DEV.map((d, i) => (o.show && !o.show[i] ? '' : laptop(d, { dim: o.dim && o.dim[i], badge: o.badge && o.badge[i], mail: o.mail && o.mail[i], mailLabel: o.mailLab && o.mailLab[i] }))).join('');

  // s01: Hub und Switch sehen gleich aus
  shots.s01 = (S, t, seg) => {
    const st = cue('s01', 'sting');
    const red = t >= st;
    const mini = (x, lab, col, rd) => {
      let h = `<g filter="url(#sh)"><rect x="${x - 200}" y="540" width="400" height="190" rx="30" fill="#121A36" stroke="${rd ? C.red : col}" stroke-width="10"${rd ? ' filter="url(#gl)"' : ''}/></g>`;
      for (let i = 0; i < 6; i++) {
        const px = x - 150 + i * 60;
        h += `<rect x="${px - 20}" y="650" width="40" height="34" rx="6" fill="#0A0F24" stroke="#3A4C8A" stroke-width="3"/>`;
        h += `<circle cx="${px}" cy="630" r="8" fill="${Math.sin(t * 8 + i * 2.1 + x) > 0 ? C.grn : '#24305C'}"/>`;
      }
      h += T(x, 610, lab, { s: 60, f: rd ? C.red : col });
      return h;
    };
    let h = T(540, 330, 'SEHEN GLEICH AUS …', { s: 58, f: C.w });
    h += mini(300, 'HUB', ORANGE, red) + mini(780, 'SWITCH', C.cyan, false);
    if (red) {
      const k = E.out(prog(t, st, 0.9));
      [[-1, -1], [1, -1], [-1, 1], [1, 1], [0, 1.3]].forEach(([dx, dy]) => {
        h += envelope(300 + dx * 220 * k, 640 + dy * 260 * k, C.red, 0.75);
      });
      h += chip(300, 1110, '📨 AN JEDEN!', t, st + 0.1, { bg: C.red, s: 52, w: 460, r: -3 });
    }
    out(S, h);
  };

  // s02: Netzwerk aufbauen
  shots.s02 = (S, t, seg) => {
    const show = DEV.map((_, i) => t >= seg.start + 0.5 + i * 0.2);
    out(S, T(540, 330, 'NETZWERK', { s: 54, f: C.grey }) + net('neutral', t, { show, cable: clamp((t - seg.start - 0.4) / 0.9) }));
  };

  // s03: Hub kopiert an alle
  shots.s03 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1.1), c2 = caps(seg, 2, seg.start + 2.2);
    let h = net('hub', t, { leds: t >= c2 ? [1, 1, 1, 1] : null });
    h += inbound(t, 0, c1 - 0.1, c2, DEV[0].c, 'an Cem');
    [1, 2, 3].forEach((i) => { h += outbound(t, i, c2, c2 + 0.9, DEV[0].c, 'an Cem'); });
    if (t >= c2) h += chip(540, 640, 'KOPIE AN ALLE', t, c2, { bg: ORANGE, fg: NAVY, s: 44, w: 440 });
    out(S, T(540, 330, 'HUB', { s: 54, f: ORANGE }) + h);
  };

  // s04: alle bekommen es
  shots.s04 = (S, t, seg) => {
    const p = [0.3, 0.5, 0.7].map((x) => seg.start + x);
    const badge = [null, t >= p[0] ? '👀' : null, t >= p[1] ? '✅' : null, t >= p[2] ? '👀' : null];
    const mail = [null, DEV[0].c, DEV[0].c, DEV[0].c];
    let h = net('hub', t, { badge, mail });
    h += chip(540, 640, 'NUR CEM WAR GEMEINT', t, p[2] + 0.2, { bg: C.red, s: 42, w: 560 });
    out(S, T(540, 330, 'HUB', { s: 54, f: ORANGE }) + h);
  };

  // s05: Kollision
  shots.s05 = (S, t, seg) => {
    const t0 = seg.start + 0.3, tb = cue('s05', 'boom'), c2 = caps(seg, 2, tb + 0.8);
    let h = net('hub', t, { red: t >= tb && t < tb + 0.6 });
    h += inbound(t, 0, t0, tb, DEV[0].c, 'an Cem') + inbound(t, 3, t0, tb, DEV[3].c, 'an Ben');
    if (t >= tb) {
      const k = E.out(prog(t, tb, 0.5));
      h += `<g transform="${at(540, 790, 0.4 + 1.2 * k)}" opacity="${clamp(1.6 - (t - tb) * 1.2)}">${T(540, 840, '💥', { s: 170 })}</g>`;
      h += chip(540, 640, 'KOLLISION!', t, tb + 0.05, { bg: C.red, s: 50, w: 400, r: -3 });
    }
    if (t >= c2) {
      h += chip(205, 300, '⟳ nochmal', t, c2, { bg: '#23305E', s: 40, w: 300 });
      h += chip(760, 960, '⟳ nochmal', t, c2 + 0.1, { bg: '#23305E', s: 40, w: 260 });
    }
    out(S, h);
  };

  // MAC-Tabelle
  const table = (rows, t, y0, o = {}) => {
    let h = `<rect x="70" y="${y0}" width="840" height="${80 + rows.length * 70}" rx="28" fill="#0A0F24" stroke="${C.cyan}" stroke-width="6"/>`;
    h += T(110, y0 + 55, 'PORT', { s: 32, f: C.grey, a: 'start' }) + T(260, y0 + 55, 'MAC-ADRESSE', { s: 32, f: C.grey, a: 'start' }) + T(885, y0 + 55, 'GERÄT', { s: 32, f: C.grey, a: 'end' });
    rows.forEach((i, r) => {
      const d = DEV[i], y = y0 + 120 + r * 70, hi = o.hi === i;
      if (hi) h += `<rect x="85" y="${y - 50}" width="810" height="66" rx="16" fill="${C.cyan}" opacity=".25"/>`;
      h += T(140, y, String(i + 1), { s: 40, f: C.w, m: true }) + T(260, y, d.mac, { s: 34, f: C.w, m: true, a: 'start' }) + T(885, y, d.n, { s: 40, f: d.c, a: 'end' });
    });
    return h;
  };
  const small = (inner) => `<g transform="translate(540,250) scale(0.62) translate(-540,-300)">${inner}</g>`;

  // s06: Switch merkt sich Geräte
  shots.s06 = (S, t, seg) => {
    const ticks = [1.8, 2.2, 2.6, 3.0].map((x) => seg.start + x);
    const rows = [0, 1, 2, 3].filter((i) => t >= ticks[i]);
    let inner = net('switch', t);
    [0, 1, 2, 3].forEach((i) => { inner += inbound(t, i, ticks[i] - 0.45, ticks[i], DEV[i].c); });
    let h = small(inner);
    h += table(rows, t, 900);
    out(S, h);
  };

  // s07: MAC-Adresse
  shots.s07 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 0.9);
    const k = pop(t, seg.start + 0.1, 0.35);
    let h = `<g transform="${at(540, 650, k, -3)}">`;
    h += `<rect x="190" y="470" width="700" height="330" rx="20" fill="#1E6B45" stroke="#0E3B25" stroke-width="8"/>`;
    for (let i = 0; i < 14; i++) h += `<rect x="${240 + i * 44}" y="800" width="30" height="46" rx="4" fill="#E8B84A"/>`;
    h += `<rect x="250" y="520" width="170" height="170" rx="14" fill="#14161F"/>` + T(335, 620, 'NIC', { s: 40, f: C.grey, m: true });
    h += `<rect x="470" y="540" width="370" height="120" rx="12" fill="#F4F4F4"/>`;
    h += T(655, 590, 'MAC', { s: 34, f: '#333', m: true }) + T(655, 640, DEV[0].mac, { s: 30, f: '#111', m: true });
    h += `</g>`;
    h += T(540, 360, 'NETZWERKKARTE', { s: 50, f: C.grey });
    h += chip(540, 1000, 'FESTE ADRESSE: MAC', t, c1, { bg: C.cyan, fg: NAVY, s: 48, w: 600 });
    h += T(540, 1110, 'z. B. A4:83:E7:2B:11:0A (ausgedacht)', { s: 34, f: C.grey, m: true, op: clamp((t - c1 - 0.3) * 4) });
    out(S, h);
  };

  // s08: gezielt
  shots.s08 = (S, t, seg) => {
    const t0 = seg.start + 0.3, mid = t0 + 0.9, t1 = mid + 0.9;
    let h = net('switch', t, { dim: [false, true, false, true] });
    h += inbound(t, 0, t0, mid, DEV[0].c, 'an Cem') + outbound(t, 2, mid, t1, DEV[0].c, 'an Cem');
    if (t >= mid) h += chip(540, 640, 'Cem → Port 3', t, mid, { bg: C.cyan, fg: NAVY, s: 44, w: 420 });
    if (t >= t1) h += T(320, 1060, '✅', { s: 80 });
    out(S, T(540, 330, 'SWITCH', { s: 54, f: C.cyan }) + h);
  };

  // s09: gleichzeitig
  shots.s09 = (S, t, seg) => {
    const t0 = seg.start + 0.2, mid = t0 + 0.7, t1 = mid + 0.7;
    let h = net('switch', t);
    h += inbound(t, 0, t0, mid, DEV[0].c, 'an Cem') + outbound(t, 2, mid, t1, DEV[0].c, 'an Cem');
    h += inbound(t, 1, t0, mid, DEV[1].c, 'an Dana') + outbound(t, 3, mid, t1, DEV[1].c, 'an Dana');
    if (t >= t1) h += chip(540, 640, '✅ GLEICHZEITIG', t, t1, { bg: C.grn, fg: NAVY, s: 46, w: 480 });
    if (t >= t1 + 0.3) h += T(320, 1060, '✅', { s: 72 }) + T(720, 1000, '✅', { s: 72 });
    out(S, T(540, 330, 'SWITCH', { s: 54, f: C.cyan }) + h);
  };

  // s10: Vergleich + Router
  shots.s10 = (S, t, seg) => {
    const c3 = caps(seg, 3, seg.start + 2.2);
    let h = '';
    const col = (x, title, colr, rows, t0) => {
      const k = pop(t, t0, 0.3);
      let g = `<g transform="${at(x, 640, k)}"><rect x="${x - 230}" y="380" width="460" height="560" rx="36" fill="${C.panel}" stroke="${colr}" stroke-width="8"/>${T(x, 470, title, { s: 64, f: colr })}`;
      rows.forEach(([e, s], i) => { g += T(x - 180, 590 + i * 110, e, { s: 56, a: 'start' }) + T(x - 105, 590 + i * 110, s, { s: 44, a: 'start' }); });
      return g + '</g>';
    };
    h += col(290, 'HUB', ORANGE, [['❌', 'an alle'], ['❌', 'Kollisionen'], ['🦖', 'veraltet']], seg.start + 0.1);
    h += col(790, 'SWITCH', C.cyan, [['✅', 'gezielt'], ['✅', 'gleichzeitig'], ['🏆', 'Standard']], seg.start + 0.4);
    if (t >= c3) h += chip(540, 1080, '📶 IM ROUTER: SWITCH', t, c3, { bg: C.cyan, fg: NAVY, s: 50, w: 640 });
    out(S, h);
  };

  // s11: Folgen
  shots.s11 = (S, t, seg) => {
    const k = pop(t, seg.start, 0.35);
    let h = `<g transform="${at(540, 600, k)}">${T(540, 560, '🔍', { s: 200 })}${T(540, 720, 'TECH-LUPE', { s: 120, f: C.cyan, st: NAVY, sw: 14 })}</g>`;
    h += `<g opacity="${clamp((t - seg.start - 0.3) * 4)}">${T(540, 810, 'Informatik einfach erklärt', { s: 52, f: C.w })}</g>`;
    const b = pop(t, seg.start + 0.5) * (1 + 0.05 * Math.max(0, Math.sin(t * 9)));
    if (b > 0) h += `<g transform="${at(540, 950, b)}"><rect x="320" y="895" width="440" height="110" rx="55" fill="${C.red}" stroke="${NAVY}" stroke-width="8"/>${T(540, 970, '+ FOLGEN', { s: 60 })}</g>`;
    h += chip(540, 1150, 'WELCHES THEMA ALS NÄCHSTES? 👇', t, seg.start + 1.1, { bg: C.yel, fg: NAVY, s: 36, w: 700, r: -2 });
    out(S, h);
  };

  // Titelbild: Hub kopiert an alle
  shots.cover = (S) => {
    let h = net('hub', 1.0, { leds: [1, 1, 1, 1] });
    [1, 2, 3].forEach((i) => { const [x, y] = along(outPath(DEV[i]), 0.55); h += envelope(x, y, DEV[0].c, 0.8); });
    out(S, `<g transform="translate(0,230)">${h}</g>`);
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
    preload: '🔍📨👀✅💥⟳❌🦖🏆📶→👇',
    ui: {
      day: '', profile: { name: 'Tech-Lupe', handle: '@techlupe', avatar: '🔍', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

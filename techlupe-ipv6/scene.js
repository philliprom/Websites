// Tech-Lupe – Folge 5 „IPv4 vs. IPv6“: reine Bewegtgrafik im Bildschirm-Raum (Ebene „alt“).
// Sichere Zonen: nichts über y 260, rechts ab x 920 nur oberhalb y 800, Untertitel ab y 1390.
(() => {
  const { $, clamp, lerp, E, prog, popS, cue, cues, rng } = Engine;
  const C = { bg: '#0E1430', panel: '#141C3A', line: '#2A3A6E', cyan: '#3DDCFF', yel: '#FFD43B', red: '#FF4D6D', grn: '#7CFF6B', grey: '#7F8BB5', w: '#FFFFFF' };
  const NAVY = '#0B1022', ORANGE = '#FF9F43';
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const T = (x, y, s, o = {}) => `<text x="${x}" y="${y}"${o.m ? ' class="m"' : ''} text-anchor="${o.a || 'middle'}" font-size="${o.s || 60}" fill="${o.f || C.w}"${o.st ? ` stroke="${o.st}" stroke-width="${o.sw || 10}" paint-order="stroke fill" stroke-linejoin="round"` : ''}${o.op !== undefined ? ` opacity="${o.op}"` : ''}${o.tr ? ` transform="${o.tr}"` : ''}>${o.raw ? s : esc(s)}</text>`;
  const pop = (t, t0, d = 0.25) => (t0 === null || t0 === undefined || t < t0 ? 0 : popS(t, t0, d));
  const at = (x, y, s, r = 0) => `translate(${x},${y}) rotate(${r}) scale(${Math.max(0.001, s)}) translate(${-x},${-y})`;
  const chip = (x, y, txt, t, t0, o = {}) => {
    const k = pop(t, t0); if (k <= 0) return '';
    const fs = o.s || 46, w = o.w || txt.length * fs * 0.62 + 70;
    return `<g transform="${at(x, y, k, o.r ?? -2)}"><rect x="${x - w / 2}" y="${y - fs * 0.95}" width="${w}" height="${fs * 1.9}" rx="${fs * 0.95}" fill="${o.bg || C.red}" stroke="${NAVY}" stroke-width="7"/>${T(x, y + fs * 0.34, txt, { s: fs, f: o.fg || C.w, m: o.m })}</g>`;
  };
  const caps = (seg, i, fb) => (seg.caps && seg.caps[i] ? seg.caps[i].start : fb);
  const fmt = (n) => Math.round(n).toLocaleString('de-DE');
  // Potenz „2 hoch n =“ ohne Unicode-Hochzahlen (die Code-Schrift hat keine)
  const pow = (x, y, exp, o = {}) => `<g opacity="${o.op ?? 1}">${T(x - 20 - exp.length * 11, y, '2', { s: 60, f: C.grey, m: true })}${T(x - 4 - exp.length * 11, y - 30, exp, { s: 34, f: C.grey, m: true, a: 'start' })}${T(x + exp.length * 12 + 30, y, '=', { s: 60, f: C.grey, m: true })}</g>`;
  const panel = (x, y, w, h, title) => `<g filter="url(#sh)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="34" fill="${C.panel}" stroke="${C.line}" stroke-width="5"/></g>
    <rect x="${x}" y="${y}" width="${w}" height="74" rx="34" fill="#1B2550"/><rect x="${x}" y="${y + 40}" width="${w}" height="34" fill="#1B2550"/>
    <circle cx="${x + 46}" cy="${y + 38}" r="13" fill="#FF5F57"/><circle cx="${x + 86}" cy="${y + 38}" r="13" fill="#FEBC2E"/><circle cx="${x + 126}" cy="${y + 38}" r="13" fill="#28C840"/>
    ${T(x + w / 2 + 40, y + 50, title, { s: 30, f: C.grey, m: true })}`;
  const envelope = (x, y, col, s = 1) => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-46" y="-32" width="92" height="64" rx="8" fill="#fff" stroke="${col}" stroke-width="7"/><path d="M -44 -28 L 0 6 L 44 -28" fill="none" stroke="${col}" stroke-width="6"/></g>`;

  const statics = () => `
    <defs>
      <radialGradient id="bgG" cx="50%" cy="40%" r="80%"><stop offset="0" stop-color="#1A2456"/><stop offset=".6" stop-color="#0E1430"/><stop offset="1" stop-color="#070A1A"/></radialGradient>
      <filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" stdDeviation="0" flood-color="#000" flood-opacity=".45"/></filter>
      <filter id="gl" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
    <rect width="1080" height="1920" fill="url(#bgG)"/>
    <g opacity=".08" stroke="#8FB4FF" stroke-width="2">${Array.from({ length: 13 }, (_, i) => `<line x1="${i * 90}" y1="0" x2="${i * 90}" y2="1920"/>`).join('')}${Array.from({ length: 22 }, (_, i) => `<line x1="0" y1="${i * 90}" x2="1080" y2="${i * 90}"/>`).join('')}</g>
    <g id="dyn"></g>
`;
  const shots = {};
  const out = (S, html) => { S.layer = 'alt'; S.html = html; };

  // Gerätesymbole (einfach, ohne Emoji-Abhängigkeit)
  const phone = (x, y, s, col, screen = '') => `<g transform="translate(${x},${y}) scale(${s})"><rect x="-90" y="-170" width="180" height="340" rx="30" fill="#10172F" stroke="${col}" stroke-width="9"/>
    <rect x="-72" y="-140" width="144" height="260" rx="12" fill="${col}" opacity=".18"/><circle cx="0" cy="145" r="10" fill="${col}"/>${screen}</g>`;

  // s01: Zähler läuft auf 0, Stempel AUSVERKAUFT
  const stampAt = () => cue('s01', 'stamp');
  const s01Html = (t, st) => {
    let h = panel(120, 420, 840, 560, 'RIPE NCC · EUROPA');
    h += T(540, 580, 'FREIE IPv4-ADRESSEN', { s: 46, f: C.grey });
    const v = t >= st - 0.25 ? 0 : Math.round(1024 * (1 - E.in(clamp(t / Math.max(0.3, st - 0.3)))));
    const blink = v === 0 && Math.sin(t * 12) < -0.3 ? 0.35 : 1;
    h += T(540, 800, fmt(v), { s: 190, f: v === 0 ? C.red : C.yel, m: true, op: blink });
    if (t >= st) {
      const k = E.out(prog(t, st, 0.18));
      h += `<g transform="${at(540, 760, lerp(2.3, 1, k), -12)}" opacity="${clamp(k * 2)}"><rect x="170" y="660" width="740" height="190" rx="22" fill="none" stroke="${C.red}" stroke-width="16"/>${T(540, 790, 'AUSVERKAUFT', { s: 108, f: C.red, st: NAVY, sw: 8 })}</g>`;
      h += chip(540, 1120, '25.11.2019', t, st + 0.4, { bg: C.red, s: 54, m: true, r: 2 });
    }
    return h;
  };
  shots.s01 = (S, t) => out(S, s01Html(t, stampAt()));

  // s02: IP-Adresse = Hausnummer
  shots.s02 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1), c2 = caps(seg, 2, seg.start + 2), c3 = caps(seg, 3, seg.start + 3);
    let h = '';
    const kp = pop(t, seg.start + 0.05, 0.35);
    h += `<g transform="${at(300, 850, kp)}">${phone(300, 850, 1.1, C.cyan, T(0, 20, '🌐', { s: 90 }))}</g>`;
    h += chip(300, 560, 'IP 203.0.113.42', t, c1, { bg: C.cyan, fg: NAVY, s: 38, m: true, w: 450 });
    // Haus mit Hausnummer
    const kh = pop(t, c2, 0.35);
    if (kh > 0) {
      h += `<g transform="${at(760, 900, kh)}"><path d="M 630 830 L 760 700 L 890 830 Z" fill="#23305E" stroke="${C.yel}" stroke-width="8" stroke-linejoin="round"/>
        <rect x="650" y="830" width="220" height="220" fill="#141C3A" stroke="${C.yel}" stroke-width="8"/><rect x="730" y="940" width="60" height="110" rx="6" fill="${C.yel}" opacity=".35"/>
        <rect x="700" y="860" width="120" height="60" rx="10" fill="#fff" stroke="${NAVY}" stroke-width="5"/>${T(760, 905, '42', { s: 46, f: NAVY, m: true })}</g>`;
      h += T(760, 1120, 'HAUSNUMMER', { s: 38, f: C.yel, op: clamp((t - c2) * 4) });
    }
    // Paket fliegt aus dem Netz zum Handy
    if (t >= c3 - 0.1) {
      const k = E.inOut(clamp((t - c3 + 0.1) / 0.9));
      if (k < 1) h += envelope(lerp(540, 300, k), lerp(380, 760, k) - Math.sin(k * Math.PI) * 60, C.cyan, 0.9);
      else h += T(400, 700, '✅', { s: 80 });
    }
    h += T(540, 360, '🌐 INTERNET', { s: 50, f: C.grey });
    out(S, h);
  };

  // s03: IPv4-Adresse, 4 Zahlen 0–255
  const OCT = ['203', '0', '113', '42'], OX = [150, 370, 590, 810];
  shots.s03 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1.2), pops = cues('s03', 'pop');
    let h = '';
    const k = pop(t, c1, 0.35);
    if (k > 0) h += `<g transform="${at(540, 430, k)}">${T(540, 470, 'IPv4', { s: 150, f: ORANGE, st: NAVY, sw: 14 })}</g>`;
    OCT.forEach((o, i) => {
      const kb = pop(t, seg.start + 0.15 + i * 0.12, 0.3);
      if (kb <= 0) return;
      h += `<g transform="${at(OX[i], 700, kb)}"><rect x="${OX[i] - 90}" y="630" width="180" height="140" rx="22" fill="${C.panel}" stroke="${ORANGE}" stroke-width="7"/>${T(OX[i], 728, o, { s: 76, m: true })}</g>`;
      if (i < 3) h += T(OX[i] + 110, 735, '.', { s: 90, f: C.grey, m: true, op: clamp(kb) });
    });
    OCT.forEach((_, i) => {
      const t0 = pops[i]; const kl = pop(t, t0, 0.25);
      if (kl <= 0) return;
      h += `<g transform="${at(OX[i], 860, kl)}"><path d="M ${OX[i] - 80} 800 Q ${OX[i] - 80} 828 ${OX[i] - 40} 828 L ${OX[i] - 10} 828 L ${OX[i]} 846 L ${OX[i] + 10} 828 L ${OX[i] + 40} 828 Q ${OX[i] + 80} 828 ${OX[i] + 80} 800" fill="none" stroke="${C.yel}" stroke-width="6"/>${T(OX[i], 900, '0–255', { s: 40, f: C.yel, m: true })}</g>`;
    });
    if (pops.length && t >= pops[3] + 0.3) h += T(540, 1060, '4 Zahlen · je 8 Bit', { s: 46, f: C.grey, op: clamp((t - pops[3] - 0.3) * 4) });
    out(S, h);
  };

  // s04: 32 Bit, 2^32 Adressen
  const BITS = ['11001011', '00000000', '01110001', '00101010'];
  shots.s04 = (S, t, seg) => {
    const ticks = cues('s04', 'tick'), c2 = caps(seg, 2, seg.end - 1.4);
    let h = chip(540, 380, '32 BIT', t, seg.start + 0.05, { bg: ORANGE, fg: NAVY, s: 56, w: 300 });
    BITS.forEach((b, i) => {
      const t0 = ticks[i] ?? seg.start + 0.4 + i * 0.2, k = pop(t, t0, 0.2);
      if (k <= 0) return;
      const x = i % 2 ? 760 : 320, y = i < 2 ? 560 : 660;
      h += `<g transform="${at(x, y - 20, k)}">${T(x, y, b, { s: 62, f: C.cyan, m: true })}${T(x, y + 44, OCT[i], { s: 30, f: C.grey, m: true })}</g>`;
    });
    if (t >= c2 - 0.6) {
      const k = E.out(clamp((t - c2 + 0.6) / 1.0));
      h += pow(540, 840, '32', { op: clamp((t - c2 + 0.6) * 4) });
      h += T(540, 950, fmt(4294967296 * k), { s: 92, f: C.yel, m: true });
      h += chip(540, 1110, '≈ 4,3 MILLIARDEN', t, c2 + 0.3, { bg: C.yel, fg: NAVY, s: 50, w: 560 });
    }
    out(S, h);
  };

  // s05: mehr Geräte als Adressen
  const DEVS = ['📱', '💻', '📺', '⌚', '🎮', '🖨️', '📱', '🔌', '💻', '📱', '🚗', '📷', '📱', '🎧'];
  const DR = rng(55);
  const DPOS = DEVS.map(() => [170 + DR() * 700, 930 + DR() * 330]);
  shots.s05 = (S, t, seg) => {
    const st = cue('s05', 'sting');
    let h = T(160, 470, 'ADRESSEN', { s: 40, f: C.grey, a: 'start' });
    h += `<rect x="160" y="500" width="520" height="70" rx="18" fill="${ORANGE}" stroke="${NAVY}" stroke-width="5"/>${T(420, 548, '4,3 Mrd', { s: 40, f: NAVY, m: true })}`;
    h += `<line x1="680" y1="470" x2="680" y2="760" stroke="${C.w}" stroke-width="5" stroke-dasharray="14 10"/>`;
    h += T(160, 650, 'GERÄTE', { s: 40, f: C.grey, a: 'start' });
    const g = E.out(clamp((t - seg.start - 0.2) / Math.max(0.5, st - seg.start - 0.2)));
    const w = lerp(40, 740, g), over = 160 + w > 680;
    h += `<rect x="160" y="680" width="${w.toFixed(0)}" height="70" rx="18" fill="${over ? C.red : C.cyan}" stroke="${NAVY}" stroke-width="5"/>`;
    if (over) h += T(160 + w - 20, 728, '↑', { s: 46, f: C.w, a: 'end' });
    DEVS.forEach((d, i) => {
      const k = pop(t, seg.start + 0.25 + i * 0.12, 0.25);
      if (k > 0) h += `<g transform="${at(DPOS[i][0], DPOS[i][1], k, ((i * 37) % 30) - 15)}">${T(DPOS[i][0], DPOS[i][1] + 30, d, { s: 84 })}</g>`;
    });
    if (t >= st) h += chip(540, 860, 'ZU WENIG ADRESSEN!', t, st, { bg: C.red, s: 48, w: 620, r: -3 });
    out(S, h);
  };

  // s06: NAT – ein Router, eine öffentliche Adresse für alle
  shots.s06 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1), c2 = caps(seg, 2, seg.start + 2), pops = cues('s06', 'pop');
    let h = `<path d="M 150 700 L 540 500 L 930 700" fill="none" stroke="${C.yel}" stroke-width="10" stroke-linejoin="round" opacity=".9"/>`;
    h += `<rect x="190" y="700" width="700" height="560" rx="16" fill="#121A36" stroke="${C.yel}" stroke-width="8" opacity=".9"/>`;
    h += T(540, 1240, '🏠 ZU HAUSE', { s: 36, f: C.yel, op: 0.8 });
    // Router
    const kr = pop(t, c1, 0.3);
    if (kr > 0) {
      h += `<g transform="${at(540, 780, kr)}"><rect x="430" y="740" width="220" height="80" rx="16" fill="${C.panel}" stroke="${C.cyan}" stroke-width="7"/>${T(540, 792, 'ROUTER', { s: 40, f: C.cyan })}
        <path d="M 480 740 L 470 700 M 600 740 L 610 700" stroke="${C.cyan}" stroke-width="7" stroke-linecap="round"/></g>`;
    }
    h += chip(540, 400, '203.0.113.42 · öffentlich', t, c2, { bg: C.cyan, fg: NAVY, s: 38, m: true, w: 640 });
    const devs = [['📱', 290, '.20'], ['💻', 540, '.21'], ['📺', 790, '.22']];
    devs.forEach(([e, x, ip], i) => {
      const k = pop(t, pops[i] ?? c2 + i * 0.2, 0.25);
      if (k <= 0) return;
      h += `<line x1="${x}" y1="960" x2="540" y2="820" stroke="#3A4C8A" stroke-width="7" stroke-linecap="round" opacity="${clamp(k)}"/>`;
      h += `<g transform="${at(x, 1010, k)}">${T(x, 1040, e, { s: 96 })}${T(x, 1120, ip, { s: 38, f: C.grey, m: true })}</g>`;
    });
    if (pops.length >= 3 && t >= pops[2] + 0.2) h += T(540, 1190, 'privat: 192.168.178.x', { s: 34, f: C.grey, m: true, op: clamp((t - pops[2] - 0.2) * 4) });
    // Pakete wandern über den Router hinaus
    if (pops.length >= 3 && t >= pops[2]) {
      for (let i = 0; i < 3; i++) {
        const k = ((t - pops[2]) * 0.8 + i / 3) % 1;
        const y = lerp(960, 450, k), x = lerp(devs[i][1], 540, clamp(k * 1.8));
        h += envelope(x, y, C.cyan, 0.55);
      }
    }
    out(S, h);
  };

  // s07: IPv6 – 128 Bit
  shots.s07 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1.1), c2 = caps(seg, 2, seg.start + 1.8), c3 = caps(seg, 3, seg.start + 2.4);
    let h = '';
    const k = pop(t, c1, 0.35);
    if (k > 0) h += `<g transform="${at(540, 400, k)}" filter="url(#gl)">${T(540, 450, 'IPv6', { s: 160, f: C.grn, st: NAVY, sw: 14 })}</g>`;
    const lines = ['2001:0db8:85a3:0000', '0000:8a2e:0370:7334'];
    const full = lines.join('');
    const n = Math.floor(clamp((t - c1 - 0.2) / 1.2) * full.length);
    let used = 0;
    lines.forEach((ln, i) => {
      const part = ln.slice(0, Math.max(0, n - used)); used += ln.length;
      if (part) h += T(540, 620 + i * 90, part, { s: 60, f: C.w, m: true });
    });
    if (t >= c1 + 1.4) h += T(540, 790, '8 Blöcke · Hex 0–9, a–f', { s: 36, f: C.grey, op: clamp((t - c1 - 1.4) * 4) });
    // Balken 32 vs. 128 Bit
    const kb = clamp((t - c2) / 0.8);
    if (t >= c2) {
      h += T(150, 920, 'IPv4', { s: 40, f: ORANGE, a: 'start' }) + `<rect x="300" y="885" width="${(150 * clamp(kb * 3)).toFixed(0)}" height="50" rx="14" fill="${ORANGE}"/>` + T(470, 924, '32', { s: 36, f: C.w, m: true, a: 'start', op: clamp(kb * 3) });
      h += T(150, 1020, 'IPv6', { s: 40, f: C.grn, a: 'start' }) + `<rect x="300" y="985" width="${(560 * E.out(kb)).toFixed(0)}" height="50" rx="14" fill="${C.grn}"/>` + T(300 + 560 * E.out(kb) - 16, 1024, '128', { s: 36, f: NAVY, m: true, a: 'end', op: clamp(kb * 2) });
    }
    if (t >= c3) h += chip(540, 1160, '4× SO LANG', t, c3, { bg: C.grn, fg: NAVY, s: 50, w: 420 });
    out(S, h);
  };

  // s08: 340 Sextillionen, Sandkörner
  const BIG = ['340.282.366.920.', '938.463.463.374.', '607.431.768.211.456'];
  const SR = rng(808), SAND = Array.from({ length: 160 }, () => [180 + SR() * 720, 960 + SR() * 200, 3 + SR() * 5]);
  shots.s08 = (S, t, seg) => {
    const c1 = caps(seg, 1, seg.start + 1), c3 = caps(seg, 3, seg.start + 3), c4 = caps(seg, 4, seg.end - 1.2);
    let h = pow(540, 410, '128');
    const full = BIG.join(''), n = Math.floor(clamp((t - seg.start - 0.1) / 1.0) * full.length);
    let used = 0;
    BIG.forEach((ln, i) => { const part = ln.slice(0, Math.max(0, n - used)); used += ln.length; if (part) h += T(540, 510 + i * 80, part, { s: 58, f: C.yel, m: true }); });
    h += chip(540, 820, '≈ 340 SEXTILLIONEN', t, c1, { bg: C.yel, fg: NAVY, s: 52, w: 640 });
    if (t >= c3 - 0.2) {
      const k = clamp((t - c3 + 0.2) * 3);
      h += `<path d="M 150 1170 Q 540 900 930 1170 Z" fill="#E8C27A" opacity="${(0.9 * k).toFixed(2)}"/>`;
      SAND.forEach(([x, y, r], i) => { if (y > 1170 - (1 - Math.abs(x - 540) / 390) * 260 * 0.9) h += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r.toFixed(1)}" fill="${i % 3 ? '#C99A4A' : '#FFF1C8'}" opacity="${k.toFixed(2)}"/>`; });
      h += T(540, 930, '🏖️', { s: 80, op: k });
    }
    if (t >= c4) h += chip(540, 1230, 'BILLIONEN ADRESSEN PRO SANDKORN', t, c4, { bg: C.grn, fg: NAVY, s: 34, w: 740 });
    out(S, h);
  };

  // s09: rund die Hälfte bei Google, Handy kann beides
  shots.s09 = (S, t, seg) => {
    const c3 = caps(seg, 3, seg.end - 1.6), pops = cues('s09', 'pop');
    let h = T(540, 400, 'ZUGRIFFE AUF GOOGLE (2026)', { s: 40, f: C.grey });
    const k = E.out(clamp((t - seg.start - 0.2) / 1.2)), cx = 540, cy = 760, r = 240;
    const arc = (f, col, w) => { const a0 = Math.PI, a1 = Math.PI + Math.PI * f; return `<path d="M ${cx + r * Math.cos(a0)} ${cy + r * Math.sin(a0)} A ${r} ${r} 0 0 1 ${(cx + r * Math.cos(a1)).toFixed(1)} ${(cy + r * Math.sin(a1)).toFixed(1)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`; };
    h += arc(1, '#23305E', 70) + arc(0.5 * k + 0.0001, C.grn, 70);
    h += T(cx, cy - 30, `≈ ${Math.round(50 * k)} %`, { s: 110, f: C.grn, m: true }) + T(cx, cy + 40, 'über IPv6', { s: 44, f: C.w });
    if (t >= c3 - 0.2) {
      const kp = pop(t, c3 - 0.2, 0.3);
      h += `<g transform="${at(300, 1080, kp)}">${phone(300, 1080, 0.62, C.cyan)}</g>`;
      h += chip(610, 1020, 'IPv4 ✅', t, pops[0] ?? c3, { bg: ORANGE, fg: NAVY, s: 46, w: 300 });
      h += chip(610, 1140, 'IPv6 ✅', t, pops[1] ?? c3 + 0.2, { bg: C.grn, fg: NAVY, s: 46, w: 300 });
    }
    out(S, h);
  };

  // s10: Folgen
  shots.s10 = (S, t, seg) => {
    const k = pop(t, seg.start, 0.35);
    let h = `<g transform="${at(540, 600, k)}">${T(540, 560, '🔍', { s: 200 })}${T(540, 720, 'TECH-LUPE', { s: 120, f: C.cyan, st: NAVY, sw: 14 })}</g>`;
    h += `<g opacity="${clamp((t - seg.start - 0.3) * 4)}">${T(540, 810, 'Informatik einfach erklärt', { s: 52, f: C.w })}</g>`;
    const b = pop(t, seg.start + 0.5) * (1 + 0.05 * Math.max(0, Math.sin(t * 9)));
    if (b > 0) h += `<g transform="${at(540, 950, b)}"><rect x="320" y="895" width="440" height="110" rx="55" fill="${C.red}" stroke="${NAVY}" stroke-width="8"/>${T(540, 970, '+ FOLGEN', { s: 60 })}</g>`;
    h += chip(540, 1150, 'WELCHES THEMA ALS NÄCHSTES? 👇', t, seg.start + 1.1, { bg: C.yel, fg: NAVY, s: 36, w: 700, r: -2 });
    out(S, h);
  };

  // Titelbild: Zähler auf 0, Stempel AUSVERKAUFT
  shots.cover = (S) => out(S, `<g transform="translate(0,260)">${s01Html(5, 2)}</g>`);

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
    preload: '🔍📨✅📱💻📺⌚🎮🖨️🔌🚗📷🎧🏠🌐🏖️↑–·👇',
    ui: {
      day: '', profile: { name: 'Tech-Lupe', handle: '@techlupe', avatar: '🔍', stat: 'Likes', foot: '' },
      comment: '', banner: { small: '', big: '' }, stamp: { emo: '', text: '' }, plusOne: '', zirp: '',
      ticket: '', tstamp: '', kasse: '', floats: [], ccards: [],
      cards: [0, 1, 2].map(() => ({ color: '#fff', icon: '', label: '' })),
    },
  });
})();

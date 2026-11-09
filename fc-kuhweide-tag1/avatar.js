/* Profilbilder für FC Kuhweide (rund, 1080×1080). Wird von engine/render_avatar.cjs aufgerufen:
 *   window.buildAvatar('wappen') – Vereinswappen mit Berta
 *   window.buildAvatar('kalle')  – Trainer Kalle im Wappenring
 */
window.buildAvatar = (variant) => {
  const { kalleMarkup, bertaMarkup, ballMarkup, OUT } = window.ART;
  const NAVY = '#1F2A44', RED = '#E23A4E';
  let stripes = '';
  for (let i = 0; i < 12; i++) stripes += `<rect x="0" y="${560 + i * 50}" width="1080" height="50" fill="${i % 2 ? '#78C152' : '#6DB549'}"/>`;
  const glove = (x, y, r) => `<g transform="translate(${x},${y}) rotate(${r}) scale(2.6)">
      <path d="M-24 14 L-24 -14 Q-24 -30 -8 -30 L8 -30 Q24 -30 24 -14 L24 14 Z" fill="#FF7A1A" stroke="${OUT}" stroke-width="5" stroke-linejoin="round"/>
      <path d="M-24 -6 H24" stroke="#fff" stroke-width="6"/>
      <path d="M-30 -20 Q-34 -34 -22 -36" stroke="${OUT}" stroke-width="5" fill="#FF7A1A"/></g>`;

  let hero;
  if (variant === 'kalle') {
    hero = `<g transform="translate(540,1130) scale(2.75)">${kalleMarkup('kv')}</g>`;
  } else {
    hero = `
      <g transform="translate(968,1010) scale(2.45)">${bertaMarkup('bv')}</g>
      <g transform="translate(540,752) scale(2.7)">${ballMarkup()}</g>
      ${glove(432, 768, -24)}${glove(648, 768, 24)}`;
  }

  const svg = `
  <svg id="avatar" viewBox="0 0 1080 1080" width="1080" height="1080" style="position:absolute;left:0;top:0;z-index:99">
    <defs>
      <clipPath id="avInner"><circle cx="540" cy="540" r="372"/></clipPath>
      <linearGradient id="avSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5BB3F0"/><stop offset="1" stop-color="#CDEBFF"/></linearGradient>
      <path id="arcTop" d="M 130 540 A 410 410 0 0 1 950 540"/>
      <path id="arcBot" d="M 72 540 A 468 468 0 0 0 1008 540"/>
    </defs>
    <rect width="1080" height="1080" fill="${NAVY}"/>
    <circle cx="540" cy="540" r="532" fill="${NAVY}"/>
    <circle cx="540" cy="540" r="508" fill="${RED}" stroke="#fff" stroke-width="16"/>
    <g clip-path="url(#avInner)">
      <rect width="1080" height="1080" fill="url(#avSky)"/>
      <path d="M0 600 Q270 520 540 590 Q810 520 1080 600 L1080 1080 L0 1080 Z" fill="#86C566"/>
      ${stripes}
      <path d="M0 640 Q540 628 1080 640" stroke="#fff" stroke-width="10" fill="none" opacity=".9"/>
      ${hero}
    </g>
    <circle cx="540" cy="540" r="376" fill="none" stroke="${NAVY}" stroke-width="14"/>
    <circle cx="540" cy="540" r="508" fill="none" stroke="${NAVY}" stroke-width="10"/>
    <text font-family="Fredoka" font-weight="700" font-size="104" fill="#fff" letter-spacing="8" text-anchor="middle"
      stroke="${NAVY}" stroke-width="10" paint-order="stroke" stroke-linejoin="round">
      <textPath href="#arcTop" startOffset="50%">FC KUHWEIDE</textPath></text>
    <text font-family="Fredoka" font-weight="700" font-size="62" fill="#FFD43B" letter-spacing="6" text-anchor="middle"
      stroke="${NAVY}" stroke-width="8" paint-order="stroke" stroke-linejoin="round">
      <textPath href="#arcBot" startOffset="50%">GEGR. TAG 1</textPath></text>
    ${[[118, 540], [962, 540]].map(([x, y]) => `<path transform="translate(${x},${y}) scale(1.6)" d="M0 -20 L6 -6 L21 -6 L9 3 L13 18 L0 9 L-13 18 L-9 3 L-21 -6 L-6 -6 Z" fill="#FFD43B" stroke="${NAVY}" stroke-width="4" stroke-linejoin="round"/>`).join('')}
  </svg>`;

  const old = document.getElementById('avatar');
  if (old) old.remove();
  document.getElementById('stage').insertAdjacentHTML('beforeend', svg);

  // Berta nur als Kopf zeigen (Körper ausblenden), Grashalm im Maul
  const bob = document.getElementById('bv-bob');
  if (bob) {
    for (const ch of bob.children) if (ch.id !== 'bv-head') ch.style.display = 'none';
    const grass = document.getElementById('bv-grass');
    if (grass) grass.style.display = '';
    // Halsband und Glocke (letzte zwei Elemente des Kopfes) ohne Körper ausblenden
    const head = document.getElementById('bv-head');
    [...head.children].slice(-2).forEach((el) => { el.style.display = 'none'; });
  }
  // Kalle: fröhliches Gesicht mit offenem Mund
  const m = (id) => document.getElementById(id);
  if (variant === 'kalle') {
    m('kv-mSmile').style.display = 'none';
    m('kv-mOpen').style.display = '';
    m('kv-mOpen').setAttribute('transform', 'translate(0,-186) scale(1,.85)');
    m('kv-armL').setAttribute('transform', 'translate(-56,-160) rotate(9)');
    m('kv-armR').setAttribute('transform', 'translate(56,-160) rotate(-9)');
    m('kv-eyeL').setAttribute('transform', 'translate(-27,-228)');
    m('kv-eyeR').setAttribute('transform', 'translate(27,-228)');
  }
};

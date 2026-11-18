/* Profilbilder für „Wo geht dein Geld hin?“ (rund, 1080×1080). Aufruf über engine/render_avatar.cjs:
 *   window.buildAvatar('logo') – Euro-Münze als Ringdiagramm: der Preis zerfällt in seine Teile (Markenzeichen des Kanals)
 *   window.buildAvatar('tag')  – Preisschild mit „€?“
 * Muss auch klein (56 px neben Kommentaren) erkennbar sein: wenige, kräftige Formen.
 */
window.buildAvatar = (variant) => {
  const old = document.getElementById('avatar');
  if (old) old.remove();
  const DARK = '#071510', GOLD = '#FFC94A';
  const ring = (cx, cy, r0, r1, parts) => {
    let a = -Math.PI / 2, h = '';
    const tot = parts.reduce((s, p) => s + p[0], 0);
    for (const [v, col] of parts) {
      const b = a + (v / tot) * Math.PI * 2, gap = 0.035;
      const p = (r, ang) => `${(cx + r * Math.cos(ang)).toFixed(1)} ${(cy + r * Math.sin(ang)).toFixed(1)}`;
      const large = b - a - 2 * gap > Math.PI ? 1 : 0;
      h += `<path d="M ${p(r1, a + gap)} A ${r1} ${r1} 0 ${large} 1 ${p(r1, b - gap)} L ${p(r0, b - gap)} A ${r0} ${r0} 0 ${large} 0 ${p(r0, a + gap)} Z" fill="${col}"/>`;
      a = b;
    }
    return h;
  };
  // Anteile wie beim 8-Euro-Döner: Mehrwertsteuer, Zutaten, Miete/Personal, Gewinn
  const parts = [[0.52, '#FF5A5F'], [3.0, '#FF9A3C'], [2.77, '#5AB0FF'], [1.71, '#5CE1A6']];
  const inner = variant === 'tag' ? `
      <g transform="translate(540,560) rotate(-12)">
        <path d="M -330 -170 L 230 -170 L 370 0 L 230 170 L -330 170 Z" fill="${GOLD}" stroke="${DARK}" stroke-width="22" stroke-linejoin="round"/>
        <circle cx="225" cy="0" r="38" fill="${DARK}"/>
        <text x="-60" y="95" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="300" fill="${DARK}">€?</text>
      </g>` : `
      ${ring(540, 540, 250, 420, parts)}
      <circle cx="540" cy="540" r="232" fill="${GOLD}" stroke="${DARK}" stroke-width="16"/>
      <circle cx="540" cy="540" r="196" fill="none" stroke="#D9A21F" stroke-width="10"/>
      <text x="540" y="652" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="320" fill="${DARK}">€</text>`;
  const svg = `
  <svg id="avatar" viewBox="0 0 1080 1080" width="1080" height="1080" style="position:absolute;left:0;top:0;z-index:99">
    <defs>
      <clipPath id="avInner"><circle cx="540" cy="540" r="486"/></clipPath>
      <radialGradient id="avBg" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#1D4A3B"/><stop offset="1" stop-color="#06120D"/></radialGradient>
    </defs>
    <rect width="1080" height="1080" fill="${DARK}"/>
    <circle cx="540" cy="540" r="536" fill="${GOLD}"/>
    <circle cx="540" cy="540" r="500" fill="${DARK}"/>
    <g clip-path="url(#avInner)">
      <rect width="1080" height="1080" fill="url(#avBg)"/>
      ${Array.from({ length: 22 }, (_, i) => `<circle cx="${80 + ((i * 331) % 920)}" cy="${80 + ((i * 197) % 920)}" r="${4 + (i % 3)}" fill="#FFE9A8" opacity=".12"/>`).join('')}
      ${inner}
    </g>
  </svg>`;
  document.body.insertAdjacentHTML('beforeend', svg);
};

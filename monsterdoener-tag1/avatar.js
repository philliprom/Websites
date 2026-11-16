/* Profilbilder für Monsterdöner (rund, 1080×1080). Aufruf über engine/render_avatar.cjs:
 *   window.buildAvatar('logo') – Döner mit Vampirzähnen und Augen vor Neon-Hintergrund
 *   window.buildAvatar('leo')  – Leo mit Döner-Mütze, daneben der Vampir
 */
window.buildAvatar = (variant) => {
  const { leoMarkup, vladiMarkup, doner, defs, OUT, NAVY } = window.ART;
  const logo = variant === 'logo';
  const svg = `
  <svg id="avatar" viewBox="0 0 1080 1080" width="1080" height="1080" style="position:absolute;left:0;top:0;z-index:99">
    ${defs}
    <defs><clipPath id="avInner"><circle cx="540" cy="540" r="486"/></clipPath>
      <radialGradient id="avBg" cx=".5" cy=".42" r=".7"><stop offset="0" stop-color="#6A2FB0"/><stop offset="1" stop-color="#1B1030"/></radialGradient></defs>
    <rect width="1080" height="1080" fill="${NAVY}"/>
    <circle cx="540" cy="540" r="536" fill="#7CFF6B"/>
    <circle cx="540" cy="540" r="500" fill="${NAVY}"/>
    <g clip-path="url(#avInner)">
      <rect width="1080" height="1080" fill="url(#avBg)"/>
      <circle cx="830" cy="250" r="90" fill="url(#gMoon)" opacity=".9"/>
      ${Array.from({ length: 18 }, (_, i) => `<circle cx="${100 + ((i * 331) % 880)}" cy="${90 + ((i * 197) % 360)}" r="${3 + (i % 3)}" fill="#FFF8E6" opacity=".7"/>`).join('')}
      ${logo ? `
        <g transform="translate(540,640) scale(5.2)">${doner(1)}</g>
        <g transform="translate(540,560)">
          <ellipse cx="-110" cy="-40" rx="62" ry="70" fill="#fff" stroke="${OUT}" stroke-width="14"/><ellipse cx="110" cy="-40" rx="62" ry="70" fill="#fff" stroke="${OUT}" stroke-width="14"/>
          <circle cx="-96" cy="-26" r="30" fill="${OUT}"/><circle cx="124" cy="-26" r="30" fill="${OUT}"/><circle cx="-86" cy="-38" r="10" fill="#fff"/><circle cx="134" cy="-38" r="10" fill="#fff"/>
          <path d="M-170 -130 L-60 -100 M170 -130 L60 -100" stroke="${OUT}" stroke-width="22" stroke-linecap="round"/>
          <path d="M-70 150 L-48 230 L-26 150 Z M26 150 L48 230 L70 150 Z" fill="#fff" stroke="${OUT}" stroke-width="10" stroke-linejoin="round"/>
        </g>` : `
        <g transform="translate(830,1500) scale(3.1)">${vladiMarkup('av2')}</g>
        <g transform="translate(400,1440) scale(3.4)">${leoMarkup('av1')}</g>`}
    </g>
    <circle cx="540" cy="540" r="490" fill="none" stroke="${NAVY}" stroke-width="16"/>
  </svg>`;
  const old = document.getElementById('avatar');
  if (old) old.remove();
  document.getElementById('stage').insertAdjacentHTML('beforeend', svg);
  if (!logo) {
    const q = (id) => document.getElementById(id);
    q('av1-mSmile').style.display = 'none'; q('av1-mOpen').style.display = ''; q('av1-mOpen').setAttribute('transform', 'translate(0,-186) scale(1,.9)');
  }
};

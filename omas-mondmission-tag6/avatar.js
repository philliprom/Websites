/* Profilbilder für Omas Mondmission (rund, 1080×1080). Wird von engine/render_avatar.cjs aufgerufen:
 *   window.buildAvatar('oma') – Oma Gisela mit Fliegerbrille vor dem Abendhimmel, Rakete und Mond
 *   window.buildAvatar('duo') – Oma Gisela und Berta mit Raumhelm
 */
window.buildAvatar = (variant) => {
  const { omaMarkup, bertaMarkup, rocketMarkup, defs, OUT } = window.ART;
  const NAVY = '#22183A';
  let stars = '';
  for (let i = 0; i < 26; i++) {
    const x = 120 + ((i * 397) % 860), y = 120 + ((i * 211) % 330), r = 3 + (i % 3) * 2;
    stars += `<circle cx="${x}" cy="${y}" r="${r}" fill="#FFF8E6" opacity="${0.5 + (i % 4) * 0.12}"/>`;
  }
  const duo = variant === 'duo';
  const svg = `
  <svg id="avatar" viewBox="0 0 1080 1080" width="1080" height="1080" style="position:absolute;left:0;top:0;z-index:99">
    ${defs}
    <defs>
      <clipPath id="avInner"><circle cx="540" cy="540" r="486"/></clipPath>
      <linearGradient id="avSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A2C6E"/><stop offset=".45" stop-color="#9A5A9A"/>
        <stop offset=".75" stop-color="#F08A78"/><stop offset="1" stop-color="#FFC982"/></linearGradient>
    </defs>
    <rect width="1080" height="1080" fill="${NAVY}"/>
    <circle cx="540" cy="540" r="536" fill="#FFD43B"/>
    <circle cx="540" cy="540" r="500" fill="${NAVY}"/>
    <g clip-path="url(#avInner)">
      <rect width="1080" height="1080" fill="url(#avSky)"/>
      ${stars}
      <g transform="translate(820,250)"><circle r="150" fill="#FFF3D0" opacity=".18"/>
        <g mask="url(#mMoon)" transform="scale(1.6)"><circle r="56" fill="#FFF4D6"/><circle cx="-24" cy="10" r="9" fill="#EADBB4"/><circle cx="-8" cy="30" r="6" fill="#EADBB4"/></g></g>
      <g transform="translate(${duo ? 150 : 175},1160) scale(${duo ? 0.95 : 1.05})">${rocketMarkup().replace(/id="/g, 'id="av')}</g>
      ${duo ? `<g id="avBerta" transform="translate(1090,1060) scale(1.9)">${bertaMarkup('bv')}</g>` : ''}
      <g transform="translate(${duo ? 400 : 560},${duo ? 1290 : 1370}) scale(${duo ? 2.85 : 3.3})">${omaMarkup('ov')}</g>
    </g>
    <circle cx="540" cy="540" r="490" fill="none" stroke="${NAVY}" stroke-width="16"/>
  </svg>`;
  const old = document.getElementById('avatar');
  if (old) old.remove();
  document.getElementById('stage').insertAdjacentHTML('beforeend', svg);
  // Oma lacht: offener Mund statt Lächeln, Arme unten
  const q = (id) => document.getElementById(id);
  q('ov-mSmile').style.display = 'none';
  q('ov-mOpen').style.display = '';
  q('ov-mOpen').setAttribute('transform', 'translate(0,-186) scale(1,.9)');
  // Berta: nur Kopf mit Helm
  if (duo) {
    for (const el of Array.from(q('bv-bob').children)) if (el.id !== 'bv-head') el.style.display = 'none';
    q('bv-moo').style.display = 'none';
  }
};

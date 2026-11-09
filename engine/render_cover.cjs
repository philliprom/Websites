// Rendert das Titelbild eines Projekts: Szene im Cover-Modus (shots.cover) + Overlay aus <projekt>/cover.html.
//   node engine/render_cover.cjs <projekt>   -> <projekt>/out/titelbild.png (1080x1920) und titelbild_profilraster.png (3:4-Vorschau)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dir = path.resolve(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const overlay = fs.readFileSync(path.join(dir, 'cover.html'), 'utf8');
  await page.evaluate((html) => {
    window.renderAt(2.0, 'cover');
    for (const id of ['badge', 'cap1', 'cap2']) { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
    document.getElementById('vignette').style.opacity = '0.6';
    const wrap = document.createElement('div');
    wrap.innerHTML = html;
    document.getElementById('stage').appendChild(wrap);
    // Schlagzeilen-Zeilen auf maximal 980 px Breite einpassen
    for (const id of ['h1', 'h2', 'h3']) {
      const el = document.getElementById(id);
      if (!el) continue;
      const w = el.getComputedTextLength();
      if (w > 980) el.setAttribute('font-size', Math.floor(parseFloat(el.getAttribute('font-size')) * 980 / w));
    }
  }, overlay);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  fs.mkdirSync(path.join(dir, 'out'), { recursive: true });
  const out = path.join(dir, 'out', 'titelbild.png');
  await page.screenshot({ path: out });
  await page.screenshot({ path: path.join(dir, 'out', 'titelbild_profilraster.png'), clip: { x: 0, y: 240, width: 1080, height: 1440 } });
  console.log('Titelbild:', out);
  await browser.close();
})();

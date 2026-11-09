// Rendert Profilbilder eines Projekts mit dessen avatar.js (window.buildAvatar).
//   node engine/render_avatar.cjs <projekt> wappen kalle
//   -> <projekt>/out/profilbild_<variante>.png (1080x1080) + profilbild_vorschau.png (rund, groß und klein)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const dir = path.resolve(process.argv[2]);
  const variants = process.argv.slice(3);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  await page.addScriptTag({ path: path.join(dir, 'avatar.js') });
  fs.mkdirSync(path.join(dir, 'out'), { recursive: true });
  const files = [];
  for (const v of variants) {
    await page.evaluate((vv) => window.buildAvatar(vv), v);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const out = path.join(dir, 'out', `profilbild_${v}.png`);
    await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: 1080 } });
    files.push(out);
    console.log('Profilbild:', out);
  }
  // Vorschau: so erscheint es rund in groß (Profil) und klein (neben Kommentaren)
  const prev = await browser.newPage({ viewport: { width: 200 + variants.length * 460, height: 480 } });
  const imgs = files.map((f) => {
    const src = 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
    return `<div style="display:flex;align-items:center;gap:30px">
      <img src="${src}" style="width:380px;height:380px;border-radius:50%">
      <img src="${src}" style="width:56px;height:56px;border-radius:50%"></div>`;
  }).join('');
  await prev.setContent(`<body style="margin:0;background:#121212;display:flex;gap:40px;padding:50px;align-items:center">${imgs}</body>`);
  await prev.waitForTimeout(300);
  await prev.screenshot({ path: path.join(dir, 'out', 'profilbild_vorschau.png') });
  await browser.close();
})();

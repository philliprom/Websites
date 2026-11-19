// Prüft, ob Texte dort liegen, wo TikTok etwas darüberlegt (oben Suche/Tabs, rechts die Knöpfe, unten Name und Beschreibung).
//   node engine/safe_check.cjs <projekt>                 -> alle 0,5 s prüfen, Verstöße auflisten (Exit-Code 1 bei Verstößen)
//   node engine/safe_check.cjs <projekt> --bild 1.0,5.0  -> zusätzlich Standbilder mit eingezeichneten Zonen (build/safe_<t>.png)
// Zonen gelten für 1080×1920 und sind aus einem echten Screenshot abgeleitet (18.11.2026, Döner-Video):
// oben bis 260 px, rechts ab x 920 zwischen y 800 und 1700, unten ab y 1660.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const ZONES = [
  { name: 'oben (Suche/Tabs)', x0: 0, y0: 0, x1: 1080, y1: 260 },
  { name: 'rechts (Knöpfe)', x0: 920, y0: 800, x1: 1080, y1: 1700 },
  { name: 'unten (Name/Beschreibung)', x0: 0, y0: 1660, x1: 1080, y1: 1920 },
];

(async () => {
  const dir = path.resolve(process.argv[2]);
  const args = process.argv.slice(3);
  const bi = args.indexOf('--bild');
  const shots = bi >= 0 ? args[bi + 1].split(',').map(Number) : [];
  const tl = JSON.parse(fs.readFileSync(path.join(dir, 'build', 'timeline.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const found = new Map();
  const step = 0.5;
  for (let t = 0.05; t < tl.duration; t += step) {
    const hits = await page.evaluate(({ tt, zones }) => {
      window.renderAt(tt);
      const out = [];
      const vis = (el) => {
        let o = 1;
        for (let e = el; e && e.nodeType === 1; e = e.parentNode) {
          const cs = getComputedStyle(e);
          if (cs.display === 'none' || cs.visibility === 'hidden') return 0;
          o *= parseFloat(cs.opacity || '1');
          const a = e.getAttribute && e.getAttribute('opacity');
          if (a !== null && a !== undefined && a !== '') o *= parseFloat(a);
        }
        return o;
      };
      const walker = document.createTreeWalker(document.getElementById('stage'), NodeFilter.SHOW_TEXT);
      const seen = new Set();
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        const txt = n.textContent.trim();
        if (!txt) continue;
        const el = n.parentNode;
        if (seen.has(el)) continue;
        seen.add(el);
        const op = vis(el);
        if (op < 0.2) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 4 || r.height < 4) continue;
        const x0 = Math.max(0, r.left), y0 = Math.max(0, r.top), x1 = Math.min(1080, r.right), y1 = Math.min(1920, r.bottom);
        if (x1 <= x0 || y1 <= y0) continue;
        const inWorld = !!el.closest('#world');
        for (const z of zones) {
          const ix = Math.min(x1, z.x1) - Math.max(x0, z.x0), iy = Math.min(y1, z.y1) - Math.max(y0, z.y0);
          if (ix > 2 && iy > 2) out.push({ txt: txt.slice(0, 40), zone: z.name, box: [x0, y0, x1, y1].map(Math.round), world: inWorld });
        }
      }
      return out;
    }, { tt: t, zones: ZONES });
    for (const h of hits) {
      const k = `${h.zone}|${h.txt}`;
      if (!found.has(k)) found.set(k, { ...h, t0: t, n: 0 });
      found.get(k).n++;
    }
  }
  for (const t of shots) {
    await page.evaluate((tt) => window.renderAt(tt), t);
    await page.evaluate((zones) => {
      let o = document.getElementById('safeOv');
      if (!o) { o = document.createElement('div'); o.id = 'safeOv'; o.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:999'; document.getElementById('stage').appendChild(o); }
      o.innerHTML = zones.map((z) => `<div style="position:absolute;left:${z.x0}px;top:${z.y0}px;width:${z.x1 - z.x0}px;height:${z.y1 - z.y0}px;background:rgba(255,0,60,.28);outline:3px dashed #ff2050"></div>`).join('');
    }, ZONES);
    await page.screenshot({ path: path.join(dir, 'build', `safe_${t.toFixed(2)}.png`) });
    await page.evaluate(() => { const o = document.getElementById('safeOv'); if (o) o.remove(); });
  }
  await browser.close();
  const list = [...found.values()];
  const ui = list.filter((h) => !h.world), world = list.filter((h) => h.world);
  if (!list.length) { console.log('Sichere Zonen: alles frei ✓'); return; }
  const show = (h) => `  ${h.t0.toFixed(1).padStart(5)} s  ${h.zone.padEnd(26)} „${h.txt}“  [${h.box.join(', ')}]  (${h.n}× gesehen)`;
  if (ui.length) { console.log(`Text in überdeckten Zonen (${ui.length}):`); ui.forEach((h) => console.log(show(h))); }
  if (world.length) { console.log(`Hinweis, Text in der Szene (Kulisse) in überdeckten Zonen (${world.length}):`); world.forEach((h) => console.log(show(h))); }
  process.exitCode = ui.length ? 1 : 0;
})();

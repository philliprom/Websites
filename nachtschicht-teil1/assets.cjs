// Erzeugt die 2D-Grafiken für Nachtschicht Teil 1 als PNG (Playwright/Chromium):
//   build/assets/phone_bg.png   Sperrbildschirm 02:47 (1080×1920)
//   build/assets/notif1.png     Nachricht „Chef: Mach die Tür auf. Sofort.“ (transparent)
//   build/assets/notif2.png     Nachricht „Chef: Er friert.“ (transparent)
//   build/assets/cardA.png / cardB.png   Entscheidungskarten (transparent)
// Aufruf: node nachtschicht-teil1/assets.cjs
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'build', 'assets');
fs.mkdirSync(OUT, { recursive: true });
const font = (f) => 'file://' + path.join(__dirname, 'fonts', f);
const CSS = `
  @font-face { font-family: Oswald; src: url('${font('Oswald-Bold.ttf')}'); font-weight: 700; }
  @font-face { font-family: Oswald; src: url('${font('Oswald-Medium.ttf')}'); font-weight: 500; }
  @font-face { font-family: Elite; src: url('${font('SpecialElite-Regular.ttf')}'); }
  html, body { margin: 0; padding: 0; background: transparent; }
  * { box-sizing: border-box; }
  body { font-family: 'Nunito', 'Noto Color Emoji', sans-serif; }
`;
const nunito = ['800', '900'].map((w) => `<link rel="stylesheet" href="file://${path.join(__dirname, '..', 'engine', 'node_modules', '@fontsource', 'nunito', w + '.css')}">`).join('');

const phoneBg = `
  <div style="width:1080px;height:1920px;position:relative;overflow:hidden;
    background: radial-gradient(ellipse at 30% 25%, #1d2a44 0%, #0b1020 55%, #04060c 100%);">
    ${(() => { let sd = 7; const R = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); return Array.from({ length: 90 }, () => [R(), R(), R()]); })().map(([a, b, c]) => {
      const x = a * 1080, y = b * 1920, r = 5 + c * 20;
      return `<div style="position:absolute;left:${x}px;top:${y}px;width:${r}px;height:${r * 1.25}px;border-radius:50%;
        background: radial-gradient(circle at 35% 30%, rgba(255,255,255,.55), rgba(140,170,220,.18) 45%, rgba(0,0,0,0) 70%);
        box-shadow: 0 0 6px rgba(120,150,210,.25);"></div>`;
    }).join('')}
    <div style="position:absolute;left:0;right:0;top:390px;text-align:center;color:rgba(255,255,255,.92);
      font-family:Oswald;font-weight:500;font-size:250px;letter-spacing:4px;line-height:1">02:47</div>
    <div style="position:absolute;left:0;right:0;top:330px;text-align:center;color:rgba(255,255,255,.8);
      font-family:Nunito;font-weight:800;font-size:44px">Dienstag, 24. November</div>
    <div style="position:absolute;left:0;right:0;bottom:120px;text-align:center;color:rgba(255,255,255,.55);
      font-family:Nunito;font-weight:800;font-size:34px">Zum Entsperren nach oben wischen</div>
  </div>`;
const notif = (text, sub) => `
  <div style="width:760px;padding:28px 32px 30px;border-radius:44px;background:rgba(38,40,50,.86);
    box-shadow: 0 18px 50px rgba(0,0,0,.55); border:2px solid rgba(255,255,255,.08); color:#fff;">
    <div style="display:flex;align-items:center;gap:22px">
      <div style="width:74px;height:74px;border-radius:20px;background:linear-gradient(180deg,#5ef07a,#22b84a);
        display:flex;align-items:center;justify-content:center;font-size:44px">💬</div>
      <div style="flex:1;font-family:Nunito;font-weight:900;font-size:40px">Chef</div>
      <div style="font-family:Nunito;font-weight:800;font-size:32px;color:rgba(255,255,255,.6)">${sub}</div>
    </div>
    <div style="margin-top:18px;font-family:Nunito;font-weight:800;font-size:50px;line-height:1.2">${text}</div>
  </div>`;
const card = (letter, title, sub, icon, col, bg) => `
  <div style="width:740px;height:220px;border-radius:40px;background:${bg};border:6px solid ${col};
    box-shadow: 0 0 40px ${col}66, 0 16px 0 rgba(0,0,0,.45); display:flex;align-items:center;gap:30px;padding:0 34px;color:#fff">
    <div style="width:120px;height:120px;border-radius:50%;background:${col};color:#0b0b10;display:flex;align-items:center;
      justify-content:center;font-family:Oswald;font-weight:700;font-size:86px;flex:0 0 120px">${letter}</div>
    <div style="flex:1">
      <div style="font-family:Oswald;font-weight:700;font-size:56px;letter-spacing:1px;line-height:1.05;white-space:nowrap">${title}</div>
      <div style="font-family:Nunito;font-weight:800;font-size:36px;color:rgba(255,255,255,.75);margin-top:6px">${sub}</div>
    </div>
    <div style="font-size:72px;flex:0 0 auto;font-family:'Noto Color Emoji'">${icon}</div>
  </div>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const shot = async (html, file, sel) => {
    const tmp = path.join(OUT, '_tmp.html');
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8">${nunito}<style>${CSS}</style></head><body>${html}</body></html>`);
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const el = await page.$(sel || 'body > div');
    await el.screenshot({ path: path.join(OUT, file), omitBackground: true });
  };
  await shot(phoneBg, 'phone_bg.png');
  await shot(notif('Mach die Tür auf. Sofort.', 'jetzt'), 'notif1.png');
  await shot(notif('Er friert.', 'jetzt'), 'notif2.png');
  await shot(card('A', 'AUFMACHEN', 'Dein Chef sagt: sofort.', '🚪', '#FF4D5E', 'rgba(42,10,16,.92)'), 'cardA.png');
  await shot(card('B', 'NICHT AUFMACHEN', 'Regel 4: niemals.', '🔒', '#3DDCFF', 'rgba(8,22,36,.92)'), 'cardB.png');
  await browser.close();
  fs.unlinkSync(path.join(OUT, '_tmp.html'));
  console.log('Grafiken fertig:', fs.readdirSync(OUT).join(', '));
})();

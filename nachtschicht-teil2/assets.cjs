// 2D-Grafiken für Nachtschicht Teil 2 (beide Fassungen) als PNG, Stil wie Teil 1 (Playwright/Chromium):
//   build/assets/lock_a.png, lock_b.png       Sperrbildschirm 02:49 / 02:48 (1080×1920)
//   build/assets/notif_a1.png                 „Chef: Wer hat dir gesagt, dass du aufmachen sollst?“
//   build/assets/chat_a.png                   Chat mit dem Chef: Nachricht von 18:02, dann nur die neue – die von 02:47 fehlt
//   build/assets/notif_b1.png, notif_b2.png   „Er friert.“ / „Warum machst du nicht auf?“
//   build/assets/vote_a.png, vote_b.png       Abstimmungsergebnis aus Teil 1 (Karte mit „MEHRHEIT“)
//   build/assets/card_a_A.png … card_b_B.png  Entscheidungskarten für Teil 3
// Aufruf: node nachtschicht-teil2/assets.cjs
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'build', 'assets');
fs.mkdirSync(OUT, { recursive: true });
const font = (f) => 'file://' + path.join(__dirname, '..', 'nachtschicht-teil1', 'fonts', f);
const CSS = `
  @font-face { font-family: Oswald; src: url('${font('Oswald-Bold.ttf')}'); font-weight: 700; }
  @font-face { font-family: Oswald; src: url('${font('Oswald-Medium.ttf')}'); font-weight: 500; }
  html, body { margin: 0; padding: 0; background: transparent; }
  * { box-sizing: border-box; }
  body { font-family: 'Nunito', 'Noto Color Emoji', sans-serif; }
`;
const nunito = ['800', '900'].map((w) => `<link rel="stylesheet" href="file://${path.join(__dirname, '..', 'engine', 'node_modules', '@fontsource', 'nunito', w + '.css')}">`).join('');

const lock = (time, date) => `
  <div style="width:1080px;height:1920px;position:relative;overflow:hidden;
    background: radial-gradient(ellipse at 30% 25%, #1d2a44 0%, #0b1020 55%, #04060c 100%);">
    ${(() => { let sd = 11; const R = () => ((sd = (sd * 16807) % 2147483647) / 2147483647); return Array.from({ length: 90 }, () => [R(), R(), R()]); })().map(([a, b, c]) => {
      const x = a * 1080, y = b * 1920, r = 5 + c * 20;
      return `<div style="position:absolute;left:${x}px;top:${y}px;width:${r}px;height:${r * 1.25}px;border-radius:50%;
        background: radial-gradient(circle at 35% 30%, rgba(255,255,255,.55), rgba(140,170,220,.18) 45%, rgba(0,0,0,0) 70%);"></div>`;
    }).join('')}
    <div style="position:absolute;left:0;right:0;top:390px;text-align:center;color:rgba(255,255,255,.92);
      font-family:Oswald;font-weight:500;font-size:250px;letter-spacing:4px;line-height:1">${time}</div>
    <div style="position:absolute;left:0;right:0;top:330px;text-align:center;color:rgba(255,255,255,.8);
      font-family:Nunito;font-weight:800;font-size:44px">${date}</div>
    <div style="position:absolute;left:0;right:0;bottom:120px;text-align:center;color:rgba(255,255,255,.55);
      font-family:Nunito;font-weight:800;font-size:34px">Zum Entsperren nach oben wischen</div>
  </div>`;
const notif = (text, sub) => `
  <div style="width:760px;padding:28px 32px 30px;border-radius:44px;background:rgba(38,40,50,.88);
    box-shadow: 0 18px 50px rgba(0,0,0,.55); border:2px solid rgba(255,255,255,.08); color:#fff;">
    <div style="display:flex;align-items:center;gap:22px">
      <div style="width:74px;height:74px;border-radius:20px;background:linear-gradient(180deg,#5ef07a,#22b84a);
        display:flex;align-items:center;justify-content:center;font-size:44px">💬</div>
      <div style="flex:1;font-family:Nunito;font-weight:900;font-size:40px">Chef</div>
      <div style="font-family:Nunito;font-weight:800;font-size:32px;color:rgba(255,255,255,.6)">${sub}</div>
    </div>
    <div style="margin-top:18px;font-family:Nunito;font-weight:800;font-size:50px;line-height:1.2">${text}</div>
  </div>`;
// Chat: oben Kopfzeile, eine alte Nachricht vom Nachmittag, „HEUTE“, dann nur die neue Nachricht. Die von 02:47 ist weg.
const bubble = (text, time, hi) => `
  <div style="max-width:780px;align-self:flex-start;background:${hi ? '#3a2226' : '#26282f'};border-radius:10px 40px 40px 40px;
    padding:26px 34px 18px;margin:14px 0;color:#fff;font-family:Nunito;font-weight:800;font-size:46px;line-height:1.25;
    ${hi ? 'box-shadow:0 0 0 4px #ff4d5e;' : ''}">${text}
    <div style="text-align:right;font-size:28px;color:rgba(255,255,255,.55);margin-top:8px">${time}</div></div>`;
const chat = `
  <div style="width:1080px;height:2600px;background:#0e1014;position:relative;overflow:hidden;display:flex;flex-direction:column">
    <div style="height:230px;background:#1a1d24;display:flex;align-items:flex-end;padding:0 40px 34px;gap:28px;color:#fff">
      <div style="font-family:Nunito;font-weight:900;font-size:56px;color:#8fd6ff">‹</div>
      <div style="width:100px;height:100px;border-radius:50%;background:#3c4250;display:flex;align-items:center;justify-content:center;
        font-family:Oswald;font-weight:700;font-size:52px">M</div>
      <div><div style="font-family:Nunito;font-weight:900;font-size:50px">Chef</div>
        <div style="font-family:Nunito;font-weight:800;font-size:30px;color:rgba(255,255,255,.5)">zuletzt online um 18:04</div></div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;padding:40px 50px">
      <div style="align-self:center;background:#22252c;color:rgba(255,255,255,.6);font-family:Nunito;font-weight:800;font-size:30px;
        padding:10px 26px;border-radius:20px;margin:20px 0">GESTERN</div>
      ${bubble('Schlüssel liegt unter der Kasse.', '18:02', false)}
      ${bubble('Halt dich an die Regeln. Alle.', '18:03', false)}
      <div style="height:900px"></div>
      <div style="align-self:center;background:#22252c;color:rgba(255,255,255,.6);font-family:Nunito;font-weight:800;font-size:30px;
        padding:10px 26px;border-radius:20px;margin:20px 0">HEUTE</div>
      ${bubble('Wer hat dir gesagt, dass du aufmachen sollst?', '02:49', true)}
    </div>
  </div>`;
const card = (letter, title, sub, icon, col, bg, badge) => `<div style="display:inline-block;padding:${badge ? "64px 44px 24px 12px" : "0"}">
  <div style="position:relative;width:740px;height:220px;border-radius:40px;background:${bg};border:6px solid ${col};
    box-shadow: 0 0 40px ${col}66, 0 16px 0 rgba(0,0,0,.45); display:flex;align-items:center;gap:30px;padding:0 34px;color:#fff">
    <div style="width:120px;height:120px;border-radius:50%;background:${col};color:#0b0b10;display:flex;align-items:center;
      justify-content:center;font-family:Oswald;font-weight:700;font-size:86px;flex:0 0 120px">${letter}</div>
    <div style="flex:1">
      <div style="font-family:Oswald;font-weight:700;font-size:56px;letter-spacing:1px;line-height:1.05;white-space:nowrap">${title}</div>
      <div style="font-family:Nunito;font-weight:800;font-size:36px;color:rgba(255,255,255,.75);margin-top:6px">${sub}</div>
    </div>
    <div style="font-size:72px;flex:0 0 auto;font-family:'Noto Color Emoji'">${icon}</div>
    ${badge ? `<div style="position:absolute;right:-26px;top:-38px;transform:rotate(8deg);background:#ffd23f;color:#111;
      font-family:Oswald;font-weight:700;font-size:44px;padding:8px 26px;border-radius:14px;box-shadow:0 8px 0 rgba(0,0,0,.4)">✓ MEHRHEIT</div>` : ''}
  </div></div>`;
const RED = ['#FF4D5E', 'rgba(42,10,16,.92)'], BLUE = ['#3DDCFF', 'rgba(8,22,36,.92)'];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 2600 }, deviceScaleFactor: 1 });
  const shot = async (html, file) => {
    const tmp = path.join(OUT, '_tmp.html');
    fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8">${nunito}<style>${CSS}</style></head><body>${html}</body></html>`);
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const el = await page.$('body > div');
    await el.screenshot({ path: path.join(OUT, file), omitBackground: true });
  };
  await shot(lock('02:49', 'Dienstag, 24. November'), 'lock_a.png');
  await shot(lock('02:48', 'Dienstag, 24. November'), 'lock_b.png');
  await shot(notif('Wer hat dir gesagt, dass du aufmachen sollst?', 'jetzt'), 'notif_a1.png');
  await shot(chat, 'chat_a.png');
  await shot(notif('Er friert.', 'jetzt'), 'notif_b1.png');
  await shot(notif('Warum machst du nicht auf?', 'jetzt'), 'notif_b2.png');
  await shot(card('A', 'AUFMACHEN', 'Dein Chef sagt: sofort.', '🚪', ...RED, true), 'vote_a.png');
  await shot(card('B', 'NICHT AUFMACHEN', 'Regel 4: niemals.', '🔒', ...BLUE, true), 'vote_b.png');
  await shot(card('A', 'UMDREHEN', 'Du willst es wissen.', '👀', ...RED, false), 'card_a_A.png');
  await shot(card('B', 'RAUSRENNEN', 'Raus in den Regen.', '🌧️', ...BLUE, false), 'card_a_B.png');
  await shot(card('A', 'VERSTECKEN', 'Im Kühlraum.', '🧊', ...RED, false), 'card_b_A.png');
  await shot(card('B', 'RAUSRENNEN', 'Durch die Vordertür.', '🌧️', ...BLUE, false), 'card_b_B.png');
  await browser.close();
  fs.unlinkSync(path.join(OUT, '_tmp.html'));
  console.log('Grafiken fertig:', fs.readdirSync(OUT).join(', '));
})();

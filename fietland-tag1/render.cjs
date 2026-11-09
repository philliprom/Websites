// Rendert die Szene Frame für Frame mit Chromium (Playwright) und schreibt ein Video ohne Ton.
//   node render.cjs                      -> build/video_noaudio.mp4
//   node render.cjs --stills 1.2,5.5     -> build/stills/still_<t>.png
//   node render.cjs --sheet              -> build/stills/sheet_*.png (ein Bild pro Segment)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const BUILD = path.join(HERE, 'build');

(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('PAGEERROR', e.message));
  page.on('console', (m) => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
  await page.goto('file://' + path.join(HERE, 'index.html'));
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const tl = JSON.parse(fs.readFileSync(path.join(BUILD, 'timeline.json'), 'utf8'));

  const stillsDir = path.join(BUILD, 'stills');
  if (args[0] === '--stills' || args[0] === '--sheet') {
    fs.mkdirSync(stillsDir, { recursive: true });
    let times;
    if (args[0] === '--stills') times = args[1].split(',').map(Number);
    else times = tl.segments.map((s) => +(s.start + Math.min(0.75, (s.end - s.start) * 0.7)).toFixed(2));
    for (const t of times) {
      await page.evaluate((tt) => window.renderAt(tt), t);
      await page.screenshot({ path: path.join(stillsDir, `still_${t.toFixed(2)}.png`) });
    }
    console.log('stills:', times.join(', '));
    await browser.close();
    return;
  }

  const fps = tl.fps;
  const n = Math.round(tl.duration * fps);
  const out = path.join(BUILD, 'video_noaudio.mp4');
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    const t = i / fps;
    await page.evaluate((tt) => window.renderAt(tt), t);
    const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log('fertig:', out, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  await browser.close();
})();

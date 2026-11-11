/* Gemeinsame Engine für die „Tag 1“-Videos.
 * Ein Projekt liefert Welt-Grafik, Figuren und eine Schnittliste (shots); die Engine kümmert sich um
 * Kamera, UI-Bausteine (Chips, Profil-Karte, Ticket, Abstimmung …), Effekte und Untertitel.
 * window.renderAt(t) zeichnet deterministisch den Frame zum Zeitpunkt t.
 */
window.Engine = (() => {
  const TL = window.TL;
  const $ = (id) => document.getElementById(id);
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const E = {
    out: (t) => 1 - Math.pow(1 - t, 3),
    in: (t) => t * t * t,
    inOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
    back: (t) => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  };
  const prog = (t, a, d) => clamp((t - a) / d);
  const popS = (t, t0, d = 0.3) => (t < t0 ? 0 : E.back(prog(t, t0, d)));
  function rng(seed) {
    return () => {
      seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const SEGS = TL.segments;
  const byId = {};
  SEGS.forEach((s) => (byId[s.id] = s));
  const cue = (id, name, n = 0) => {
    const hits = byId[id].sfx.filter((x) => x[0] === name);
    return hits[n] ? hits[n][1] : byId[id].start;
  };
  const cues = (id, name) => byId[id].sfx.filter((x) => x[0] === name).map((x) => x[1]);
  const segAt = (t) => { let cur = SEGS[0]; for (const s of SEGS) if (t >= s.start - 1e-4) cur = s; return cur; };
  const envAt = (t) => TL.env[clamp(Math.floor(t * TL.fps), 0, TL.env.length - 1)] || 0;
  const setT = (el, tr) => { if (el) el.setAttribute('transform', tr); };
  const disp = (el, on) => { if (el) el.style.display = on ? '' : 'none'; };
  const fmt = (n) => Math.round(n).toLocaleString('de-DE');
  const camLerp = (a, b, p) => [lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)];
  const OUT = '#2B2240';
  const sw = `stroke="${OUT}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"`;

  // ---------------------------------------------------------------- Menschliche Figuren (gemeinsames Rig)
  // Elemente werden erst beim ersten Zugriff gesucht – die Szene darf humanEls() also aufrufen,
  // bevor Engine.start() die Grafik ins Dokument schreibt.
  const humanEls = (p, shoulder = 50) => {
    const parts = ['bob', 'armL', 'armR', 'head', 'eyes', 'eyeL', 'eyeR', 'pupL', 'pupR', 'happy', 'browL', 'browR',
      'mSmile', 'mFrown', 'mOpen', 'mO', 'cap', 'hairTop', 'fingerL', 'fingerR', 'extra'];
    const o = { shoulder }, cache = {};
    Object.defineProperty(o, 'root', { get: () => document.getElementById(p) });
    for (const k of parts) Object.defineProperty(o, k, { get: () => cache[k] || (cache[k] = document.getElementById(`${p}-${k}`)) });
    return o;
  };
  const humanDefaults = () => ({ armL: 9, armR: -9, expr: 'smile', look: [0, 0], tilt: 0, fingerR: false, cap: true, talk: true, bounce: false });

  function poseHuman(H, P, t) {
    const talk = P.talk ? envAt(t) : 0;
    const bounce = P.bounce ? -Math.abs(Math.sin(t * 8.5)) * 16 : 0;
    const s = H.shoulder;
    setT(H.bob, `translate(0,${Math.sin(t * 4.2) * 2.5 + bounce})`);
    setT(H.armL, `translate(${-s},-160) rotate(${P.armL})`);
    setT(H.armR, `translate(${s},-160) rotate(${P.armR})`);
    setT(H.head, `rotate(${P.tilt + Math.sin(t * 2.1) * 1.5 + talk * 2} 0 -165)`);
    disp(H.fingerR, P.fingerR); disp(H.fingerL, false);
    const bt = (t + 0.7) % 3.3;
    const eyeS = bt < 0.14 ? Math.max(0.08, Math.abs(bt - 0.07) / 0.07) : 1;
    const eyeScale = P.expr === 'o' ? 1.14 : 1;
    const happy = P.expr === 'happy';
    disp(H.eyes, !happy); disp(H.happy, happy);
    setT(H.eyeL, `translate(-27,-228) scale(${eyeScale},${eyeScale * eyeS})`);
    setT(H.eyeR, `translate(27,-228) scale(${eyeScale},${eyeScale * eyeS})`);
    const [lx, ly] = P.look;
    setT(H.pupL, `translate(${lx},${ly})`); setT(H.pupR, `translate(${lx},${ly})`);
    const worried = P.expr === 'worried';
    const browUp = P.expr === 'o' ? -10 : worried ? -4 : 0;
    setT(H.browL, `translate(0,${browUp}) rotate(${worried ? -12 : 0} -27 -262)`);
    setT(H.browR, `translate(0,${browUp}) rotate(${worried ? 12 : 0} 27 -262)`);
    const open = talk > 0.06;
    let mode = P.expr === 'o' ? 'o' : worried ? 'frown' : happy ? 'open' : 'smile';
    if (open) mode = 'open';
    disp(H.mSmile, mode === 'smile'); disp(H.mFrown, mode === 'frown'); disp(H.mO, mode === 'o'); disp(H.mOpen, mode === 'open');
    if (mode === 'open') setT(H.mOpen, `translate(0,-186) scale(1,${clamp(open ? 0.25 + 0.8 * talk : 0.85, 0.2, 1.05)})`);
    if (mode === 'o') setT(H.mO, `scale(1,${1 + talk * 0.3})`);
    disp(H.cap, P.cap); disp(H.hairTop, !P.cap);
  }

  // Standard-Gesichtsteile (Augen, Brauen, Münder) für das Rig
  const faceMarkup = (p, o = {}) => {
    const brow = o.brow || '#5A3A22';
    const browW = o.browW || 7.5;
    return `
        <g id="${p}-eyes">
          <g id="${p}-eyeL" transform="translate(-27,-228)">
            <ellipse rx="${o.eyeRx || 21}" ry="${o.eyeRy || 25}" fill="#fff" stroke="${OUT}" stroke-width="4.5"/>
            <g id="${p}-pupL"><circle r="${o.pup || 11.5}" fill="${OUT}"/><circle cx="4" cy="-5" r="4.2" fill="#fff"/></g>
          </g>
          <g id="${p}-eyeR" transform="translate(27,-228)">
            <ellipse rx="${o.eyeRx || 21}" ry="${o.eyeRy || 25}" fill="#fff" stroke="${OUT}" stroke-width="4.5"/>
            <g id="${p}-pupR"><circle r="${o.pup || 11.5}" fill="${OUT}"/><circle cx="4" cy="-5" r="4.2" fill="#fff"/></g>
          </g>
        </g>
        <g id="${p}-happy" style="display:none" fill="none" stroke="${OUT}" stroke-width="6.5" stroke-linecap="round">
          <path d="M-45 -224 Q-27 -246 -9 -224"/><path d="M9 -224 Q27 -246 45 -224"/>
        </g>
        <path id="${p}-browL" d="M-42 -262 Q-27 -269 -12 -262" stroke="${brow}" stroke-width="${browW}" fill="none" stroke-linecap="round"/>
        <path id="${p}-browR" d="M12 -262 Q27 -269 42 -262" stroke="${brow}" stroke-width="${browW}" fill="none" stroke-linecap="round"/>
        <path id="${p}-mSmile" d="M-24 -185 Q0 -166 24 -185" stroke="${OUT}" stroke-width="5.5" fill="none" stroke-linecap="round"/>
        <path id="${p}-mFrown" d="M-17 -176 Q0 -188 17 -176" stroke="${OUT}" stroke-width="5.5" fill="none" stroke-linecap="round" style="display:none"/>
        <g id="${p}-mOpen" transform="translate(0,-186)" style="display:none">
          <path d="M-24 0 Q0 4 24 0 Q22 30 0 32 Q-22 30 -24 0 Z" fill="#7A2633" ${sw}/>
          <path d="M-13 21 Q0 12 13 21 Q9 30 0 30 Q-9 30 -13 21 Z" fill="#FF7B8A"/>
          <path d="M-18 3 Q0 6 18 3 L16 9 Q0 11 -16 9 Z" fill="#fff"/>
        </g>
        <ellipse id="${p}-mO" cx="0" cy="-180" rx="12" ry="15" fill="#7A2633" ${sw} style="display:none"/>`;
  };

  const armMarkup = (p, side, sleeve, cuff, skin) => `
      <path d="M-16 -8 Q-19 40 -14 74 L14 74 Q19 40 16 -8 Q0 -16 -16 -8 Z" fill="${sleeve}" ${sw}/>
      <rect id="${p}-finger${side}" x="-5" y="94" width="10" height="26" rx="5" fill="${skin}" ${sw} style="display:none"/>
      <rect x="-17" y="66" width="34" height="13" rx="6" fill="${cuff}" ${sw}/>
      <circle cx="0" cy="91" r="17" fill="${skin}" ${sw}/>`;

  // ---------------------------------------------------------------- UI
  function uiMarkup(C) {
    const cards = C.cards.map((c, i) => `<div id="card${i}" class="ui card"><div class="letter" style="background:${c.color}">${'ABC'[i]}</div>${c.icon}<div class="lab">${c.label}</div><div class="likes">❤️ <span id="likes${i}">0</span></div></div>`).join('');
    return `
    <div id="title" class="ui badge">${C.day || 'TAG 1'}</div>
    <div id="badge" class="ui badge">${C.day || 'TAG 1'}</div>
    <div id="chip" class="ui chip"></div>
    <div id="chip2" class="ui chip"></div>
    <div id="zirp" class="ui chip green small">${C.zirp || 'zirp …'}</div>
    <div id="plusOne" class="ui chip green">${C.plusOne}</div>
    <div id="stamp" class="ui"><span class="emo">${C.stamp.emo}</span>${C.stamp.text}</div>
    <div id="banner" class="ui"><span>${C.banner.small}</span><b>${C.banner.big}</b></div>
    <div id="profile" class="ui">
      <div class="top"><div><div class="name">${C.profile.name}</div><div class="handle">${C.profile.handle}</div></div><div class="avatar">${C.profile.avatarImg ? `<img src="${C.profile.avatarImg}" style="width:100%;height:100%;border-radius:50%;display:block">` : `<div>${C.profile.avatar}</div>`}</div></div>
      <div class="stats"><div><b id="stF">0</b><span>Follower</span></div><div><b id="stE">0</b><span>${C.profile.stat}</span></div><div><b id="stL">0</b><span>Likes</span></div></div>
      <div class="btns"><div id="btnFollow" class="btn follow">Folgen</div><div class="btn">Nachricht</div></div>
      <div class="foot">${C.profile.foot}</div>
    </div>
    <div id="hand" class="ui emo">👆</div>
    <div id="comment" class="ui"><div class="av">D</div><div><div class="meta"><b>du</b> · gerade eben<i>TAG 1</i></div><div class="txt">${C.comment}</div></div><div class="heart">♡</div></div>
    <div id="ticket" class="ui">${C.ticket}</div>
    <div id="tstamp" class="ui">${C.tstamp}</div>
    <div id="kasse" class="ui"><small>${C.kasse}</small><b id="kasseVal">0 €</b></div>
    <div id="big" class="ui"></div>
    ${cards}
    <div id="votePill" class="ui chip red">💬 STIMM IN DEN KOMMENTAREN AB!</div>
    <div id="counter" class="ui"><div class="lbl" id="counterLbl"></div><div class="unit" id="counterUnit"></div><div class="val" id="counterVal">0</div></div>
    <div id="ccards">${(C.ccards || []).map((c, i) => `<div class="ui ccard" id="cc${i}"><div class="av" style="background:${c.color || '#5CC8FF'}">${(c.handle || '?').replace('@', '').charAt(0).toUpperCase()}</div>
      <div class="body"><div class="who"><b>${c.handle}</b> · gerade eben</div><div class="txt">${c.text}</div></div><div class="heart">♡<small>${c.likes || ''}</small></div></div>`).join('')}</div>
    <div id="floaters"></div>`;
  }

  function uiPop(el, t, t0, opts = {}) {
    const { center = true, rot = 0, d = 0.3, extra = '' } = opts;
    if (t0 === null || t0 === undefined || t < t0) { el.style.display = 'none'; return 0; }
    const s = popS(t, t0, d);
    el.style.display = '';
    el.style.opacity = clamp(s * 3);
    el.style.transform = `${center ? 'translateX(-50%) ' : ''}${extra} rotate(${rot}deg) scale(${Math.max(0.001, s)})`;
    return s;
  }

  // ---------------------------------------------------------------- Start
  function start(P) {
    $('cam').innerHTML = P.world();
    $('alt').innerHTML = P.alt ? P.alt() : '';
    $('ui').innerHTML = uiMarkup(P.ui);
    const floaters = (P.ui.floats || []).map((txt) => {
      const d = document.createElement('div');
      d.className = 'ui floater bubble'; d.textContent = txt; $('floaters').appendChild(d); return d;
    });
    const hearts = [];
    for (let i = 0; i < 16; i++) {
      const d = document.createElement('div');
      d.className = 'ui floater heartf'; d.textContent = ['❤️', '🩷', '❤️', '💬'][i % 4];
      $('floaters').appendChild(d); hearts.push(d);
    }
    const confR = rng(99);
    const confetti = [];
    for (let i = 0; i < 90; i++) confetti.push({ a: -Math.PI / 2 + (confR() - 0.5) * 2.6, v: 700 + confR() * 900, rot: confR() * 360, vr: (confR() - 0.5) * 900, c: (P.confettiColors || ['#FFC83A', '#FF4B5C', '#2DBE60', '#5CC8FF', '#fff', '#B67CFF'])[i % 6], w: 14 + confR() * 14, h: 8 + confR() * 8 });
    const sparkR = rng(5);
    const sparkles = [];
    for (let i = 0; i < 14; i++) sparkles.push({ x: 120 + sparkR() * 840, y: 230 + sparkR() * 380, ph: sparkR(), s: 0.6 + sparkR() * 0.8 });

    function drawFx(S, t) {
      let out = '';
      if (S.confetti && t >= S.confetti) {
        const lt = t - S.confetti;
        for (const c of confetti) {
          const x = 540 + Math.cos(c.a) * c.v * lt;
          const y = 420 + Math.sin(c.a) * c.v * lt + 1300 * lt * lt;
          out += `<rect x="${-c.w / 2}" y="${-c.h / 2}" width="${c.w}" height="${c.h}" rx="2" fill="${c.c}" transform="translate(${x},${y}) rotate(${c.rot + c.vr * lt})" opacity="${clamp(2 - lt)}"/>`;
        }
      }
      if (S.sparkle && t >= S.sparkle) {
        const lt = t - S.sparkle;
        for (const sp of sparkles) {
          const k = Math.max(0, Math.sin((lt * 2.2 + sp.ph) * Math.PI)) * sp.s * clamp(lt * 4);
          if (k <= 0.02) continue;
          out += `<path transform="translate(${sp.x},${sp.y}) scale(${k})" d="M0 -34 Q4 -4 34 0 Q4 4 0 34 Q-4 4 -34 0 Q-4 -4 0 -34 Z" fill="#FFF3B0" stroke="#fff" stroke-width="3"/>`;
        }
      }
      $('fx').innerHTML = out;
    }

    function drawUI(S, t, seg) {
      const U = S.ui;
      uiPop($('title'), t, U.title, { d: 0.4 });
      if (seg.id === 's01' && U.title !== undefined && U.title !== null) $('badge').style.display = 'none';
      else { const b = $('badge'); b.style.display = ''; b.style.opacity = 1; b.style.transform = `rotate(-3deg) scale(${1 + 0.04 * Math.sin(t * 4)})`; }
      for (const key of ['chip', 'chip2']) {
        const el = $(key), c = U[key];
        if (!c) { el.style.display = 'none'; continue; }
        if (el.dataset.text !== c.text) { el.textContent = c.text; el.dataset.text = c.text; }
        el.className = `ui chip ${c.cls || ''}`;
        el.style.top = (c.top || 278) + 'px';
        uiPop(el, t, c.t0, { rot: key === 'chip' ? -2 : 2 });
      }
      const z = $('zirp');
      uiPop(z, t, U.zirp ? U.zirp.t0 : null, { center: false, rot: -8 });
      if (U.zirp) { z.style.left = U.zirp.x + 'px'; z.style.top = U.zirp.y + 'px'; }
      uiPop($('plusOne'), t, U.plusOne, { extra: `translateY(${-prog(t, U.plusOne || 0, 1.2) * 40}px)` });
      $('plusOne').style.top = (U.plusOneTop || 1010) + 'px';
      uiPop($('stamp'), t, U.stamp, { rot: -7, d: 0.22 });
      uiPop($('banner'), t, U.banner, { rot: -2 });
      const pr = $('profile');
      if (U.profile) {
        uiPop(pr, t, U.profile.t0);
        const followed = U.profile.followAt && t >= U.profile.followAt;
        const bf = $('btnFollow');
        bf.className = 'btn follow' + (followed ? ' done' : '');
        bf.textContent = followed ? 'Gefolgt ✓' : 'Folgen';
        bf.style.transform = `scale(${!followed ? 1 + 0.05 * Math.max(0, Math.sin(t * 10)) : 1})`;
        $('stF').textContent = followed ? '1' : '0';
        $('stE').textContent = followed ? '1' : '0';
        const h = $('hand');
        if (U.profile.hand) {
          const r = bf.getBoundingClientRect();
          const tx = r.left + r.width * 0.55, ty = r.top + r.height * 0.55;
          const p = E.inOut(prog(t, U.profile.t0 + 0.1, U.profile.followAt - U.profile.t0 - 0.12));
          const x = lerp(820, tx, p), y = lerp(1100, ty, p);
          const tap = t > U.profile.followAt - 0.06 && t < U.profile.followAt + 0.12 ? 0.85 : 1;
          h.style.display = ''; h.style.left = (x - 30) + 'px'; h.style.top = (y - 8) + 'px'; h.style.transform = `scale(${tap})`;
        } else h.style.display = 'none';
      } else { pr.style.display = 'none'; $('hand').style.display = 'none'; }
      uiPop($('comment'), t, U.comment, { rot: -1.5 });
      if (U.ticket) {
        uiPop($('ticket'), t, U.ticket.t0, { rot: -3 });
        const ps = $('tstamp');
        if (t >= U.ticket.stamp) {
          const k = prog(t, U.ticket.stamp, 0.14);
          ps.style.display = ''; ps.style.opacity = clamp(k * 2) * 0.95;
          ps.style.transform = `translateX(-50%) rotate(-14deg) scale(${lerp(2.6, 1, E.out(k))})`;
        } else ps.style.display = 'none';
      } else { $('ticket').style.display = 'none'; $('tstamp').style.display = 'none'; }
      if (U.kasse) { uiPop($('kasse'), t, U.kasse.t0, { rot: -2 }); $('kasseVal').textContent = `${Math.round(U.kasse.value)} €`; }
      else $('kasse').style.display = 'none';
      const big = $('big');
      if (U.big) {
        if (big.dataset.text !== U.big.text) { big.textContent = U.big.text; big.dataset.text = U.big.text; }
        big.className = `ui ${U.big.cls || ''}`;
        uiPop(big, t, U.big.t0, { rot: U.big.rot || 0, d: 0.22 });
      } else big.style.display = 'none';
      const nCards = U.cards ? U.cards.filter((x) => x !== null && x !== undefined).length : 3;
      [0, 1, 2].forEach((i) => {
        const el = $(`card${i}`);
        el.style.left = nCards === 2 ? `${230 + i * 340}px` : `${100 + i * 300}px`;
        if (U.cards) uiPop(el, t, U.cards[i], { center: false, rot: [-4, 0, 4][i], extra: `translateY(${i === 1 ? -10 : 0}px)` });
        else el.style.display = 'none';
        $(`likes${i}`).textContent = fmt((U.likes || [0, 0, 0])[i]);
      });
      uiPop($('votePill'), t, U.vote, { rot: -1.5 });
      const cn = $('counter');
      if (U.counter) {
        uiPop(cn, t, U.counter.t0, { rot: U.counter.rot || -2 });
        cn.className = `ui ${U.counter.cls || ''}`;
        $('counterLbl').textContent = U.counter.label || '';
        $('counterUnit').textContent = U.counter.unit || '';
        $('counterVal').textContent = fmt(U.counter.value);
        cn.style.top = (U.counter.top || 300) + 'px';
      } else cn.style.display = 'none';
      (P.ui.ccards || []).forEach((c, i) => {
        const el = $(`cc${i}`);
        const st = (U.ccards || []).find((x) => x.i === i);
        if (!st || t < st.t0) { el.style.display = 'none'; return; }
        const k = popS(t, st.t0, 0.28);
        const fly = 1 - E.out(prog(t, st.t0, 0.3));
        el.style.display = '';
        el.style.left = `${st.x ?? 130}px`;
        el.style.top = `${(st.y ?? 300) + fly * 260}px`;
        el.style.opacity = clamp(k * 3);
        el.style.transform = `rotate(${st.rot || 0}deg) scale(${Math.max(0.001, k * (st.s || 1))})`;
      });
      floaters.forEach((el, i) => {
        const t0 = S.floatBubbles ? S.floatBubbles[i] : null;
        if (t0 === null || t0 === undefined || t < t0) { el.style.display = 'none'; return; }
        const lt = t - t0;
        el.style.display = '';
        el.style.left = `${[90, 560, 140, 600][i]}px`;
        el.style.top = `${1180 - lt * 230 - i * 10}px`;
        el.style.opacity = clamp(lt * 5) * clamp(2.2 - lt);
        el.style.transform = `rotate(${[-5, 4, 3, -4][i]}deg) scale(${popS(t, t0, 0.25)})`;
      });
      hearts.forEach((el, i) => {
        if (!S.hearts) { el.style.display = 'none'; return; }
        const t0 = S.hearts[i % 2] + (i >> 1) * 0.09;
        if (t < t0) { el.style.display = 'none'; return; }
        const lt = t - t0;
        el.style.display = '';
        el.style.left = `${120 + ((i * 137) % 760)}px`;
        el.style.top = `${1700 - lt * 520}px`;
        el.style.opacity = clamp(lt * 6) * clamp(1.6 - lt);
        el.style.transform = `translateX(${Math.sin(lt * 5 + i) * 30}px) scale(${0.6 + (i % 3) * 0.2})`;
      });
    }

    function drawCaption(t, seg) {
      const c1 = $('cap1'), c2 = $('cap2');
      let chunk = null;
      for (const c of seg.caps) if (t >= c.start - 0.02) chunk = c;
      if (!chunk) { c1.textContent = ''; c2.textContent = ''; return; }
      const col = { w: '#fff', g: P.highlight || '#FFD43B', r: '#FF5A64', y: '#5CCBFF' };
      // P.karaoke: noch nicht gesprochene Wörter sind blass, das aktuelle Wort leuchtet auf
      let spoken = 1e9;
      if (P.karaoke) {
        const ci = seg.caps.indexOf(chunk);
        const end = seg.caps[ci + 1] ? seg.caps[ci + 1].start : Math.max(seg.speechEnd || 0, chunk.start + 0.3);
        const lens = chunk.words.map(([w]) => w.length + 1.5), tot = lens.reduce((x, y) => x + y, 0);
        const pr = clamp((t - chunk.start) / Math.max(0.1, end - chunk.start)) * tot;
        let acc = 0; spoken = 0;
        for (let i = 0; i < lens.length; i++) { if (pr >= acc) spoken = i; acc += lens[i]; }
      }
      let wi = 0;
      const build = (el, words) => { el.innerHTML = words.map(([w, s]) => { const k = wi++; return `<tspan fill="${col[s]}"${k > spoken ? ' fill-opacity=".4" stroke-opacity=".55"' : ''}>${w}</tspan>`; }).join(' '); };
      const sc = lerp(0.82, 1, popS(t, chunk.start, 0.16));
      build(c1, chunk.words);
      c1.setAttribute('font-size', 84); c2.textContent = '';
      let lines = 1;
      if (c1.getComputedTextLength() > 900 && chunk.words.length > 1) {
        const mid = Math.ceil(chunk.words.length / 2);
        wi = 0;
        build(c1, chunk.words.slice(0, mid)); build(c2, chunk.words.slice(mid));
        lines = 2;
      }
      const maxW = Math.max(c1.getComputedTextLength(), lines === 2 ? c2.getComputedTextLength() : 0);
      const fs = maxW > 920 ? Math.floor(84 * 920 / maxW) : 84;
      c1.setAttribute('font-size', fs); c2.setAttribute('font-size', fs);
      const y0 = lines === 2 ? 1350 : 1395;
      c1.setAttribute('y', y0); c2.setAttribute('y', y0 + fs * 1.08);
      setT(c1, `translate(540,${y0}) scale(${sc}) translate(-540,${-y0})`);
      setT(c2, `translate(540,${y0}) scale(${sc}) translate(-540,${-y0})`);
    }

    window.renderAt = (t, shotId) => {
      const seg = shotId ? { id: shotId, start: t, end: t + 1, speechEnd: t, caps: [], sfx: [] } : segAt(t);
      const S = Object.assign({ layer: 'world', cam: [1200, 1150, 1], dim: 0, shake: 0, ui: {} }, P.baseState());
      P.shots[seg.id](S, t, seg, t - seg.start, seg.end - seg.start);
      const alt = S.layer === 'alt';
      $('world').style.display = alt ? 'none' : '';
      $('alt').style.display = alt ? 'block' : 'none';
      if (alt) P.drawAlt(S, t);
      else {
        let [cx, cy, z] = S.cam;
        if (P.punch && !shotId && seg.id !== SEGS[0].id && !((P.whip && P.whip.skip) || []).includes(seg.id)) {
          const pk = 1 - clamp((t - seg.start) / 0.3); z *= 1 + P.punch * pk * pk;
        }
        const sh = S.shake ? [Math.sin(t * 90) * 14 * S.shake, Math.cos(t * 77) * 10 * S.shake] : [0, 0];
        setT($('cam'), `translate(${540 + sh[0]},${960 + sh[1]}) scale(${z}) translate(${-cx},${-cy})`);
        P.drawWorld(S, t);
      }
      if (P.whip) {
        const k = seg.id !== SEGS[0].id && !shotId && !(P.whip.skip || []).includes(seg.id) ? 1 - clamp((t - seg.start) / 0.14) : 0;
        const dir = (SEGS.indexOf(seg) % 2) ? -1 : 1;
        const tr = k > 0 ? `translateX(${dir * k * k * 140}px)` : '';
        $(alt ? 'alt' : 'world').style.transform = tr;
        $(alt ? 'alt' : 'world').style.filter = k > 0.02 ? `blur(${(k * 7).toFixed(1)}px)` : '';
      }
      $('dim').style.opacity = S.dim;
      drawFx(S, t);
      drawUI(S, t, seg);
      if (S.noCap) { $('cap1').textContent = ''; $('cap2').textContent = ''; } else drawCaption(t, seg);
    };

    const allText = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜabcdefghijklmnopqrstuvwxyzäöüß0123456789 .,:!?·€✓✨…→⬇️👋📍💬❤️🩷👆♡' + (P.preload || '');
    Promise.all([
      document.fonts.load('900 84px Nunito', allText), document.fonts.load('800 30px Nunito', allText),
      document.fonts.load('700 60px Fredoka', allText), document.fonts.load('600 40px Fredoka', allText),
    ]).then(() => document.fonts.ready).then(() => { window.renderAt(0.3); window.READY = true; });
  }

  return { TL, $, clamp, lerp, E, prog, popS, rng, byId, cue, cues, segAt, envAt, setT, disp, fmt, camLerp, OUT, sw,
    humanEls, humanDefaults, poseHuman, faceMarkup, armMarkup, uiPop, start };
})();

/* Galaxy Makers - client-side "simulation".
 * The original site faked a 10-second wait and then showed pre-rendered movies picked by a
 * lookup table. Here the same lookup runs in the browser, instantly, and only the media for
 * the page you are looking at is loaded. */
(function () {
  'use strict';
  const D = window.GM_DATA;
  const $ = (s, r) => (r || document).querySelector(s);
  const el = (tag, attrs, html) => {
    const e = document.createElement(tag);
    if (attrs) for (const k in attrs) { if (attrs[k] != null) e.setAttribute(k, attrs[k]); }
    if (html != null) e.innerHTML = html;
    return e;
  };
  const GAL_TYPES = Object.keys(D.galaxies);

  /* ---------- the "physics": slider values -> which pre-rendered run ---------- */
  function classify(p) {
    const dm = p.dm < 21 ? 'L' : p.dm < 54 ? 'M' : 'H';
    const agn = ['L', 'M', 'H'][Math.min(3, Math.max(1, p.agn)) - 1];
    const tot = p.low + p.medium + p.high;
    const f = tot ? p.high / tot : 0;
    const sn = f < 0.35 ? 'L' : f < 0.70 ? 'M' : 'H';
    return { dm, agn, sn, key: dm + '_DM.' + agn + '_AGN.' + sn + '_SN.L_G' };
  }
  // Fitted to the original site's scores (119 samples, max error 1 point): distance from the
  // real Universe (84% dark matter, medium black-hole power, star mix 40/35/25).
  function score(p) {
    const tot = p.low + p.medium + p.high;
    const l = tot ? p.low / tot : 0, m = tot ? p.medium / tot : 0, h = tot ? p.high / tot : 0;
    const v = 100 - 35 * Math.abs(p.dm / 100 - 0.84) - (p.agn === 2 ? 0 : 18)
      - 10 * (Math.abs(l - 0.40) + Math.abs(m - 0.35) + Math.abs(h - 0.25));
    return Math.max(0, Math.min(100, Math.round(v)));
  }
  const clampInt = (v, lo, hi, dflt) => { v = parseInt(v, 10); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : dflt; };
  function readParams(q) {
    if (!q.has('dm')) return null;
    return { dm: clampInt(q.get('dm'), 0, 100, 75), agn: clampInt(q.get('agn'), 1, 3, 1),
      low: clampInt(q.get('low'), 0, 100, 75), medium: clampInt(q.get('medium'), 0, 100, 75), high: clampInt(q.get('high'), 0, 100, 75) };
  }
  const rnd = n => Math.floor(Math.random() * (n + 1));
  const randomParams = () => ({ dm: rnd(100), agn: 1 + rnd(2), low: rnd(100), medium: rnd(100), high: rnd(100) });
  const universeCode = p => 'U' + [p.dm, p.agn, p.low, p.medium, p.high].join('-');
  function parseCode(code) {
    code = (code || '').trim().toLowerCase().replace(/\s+/g, '');
    let m = code.match(/^u-?(\d+)-(\d+)-(\d+)-(\d+)-(\d+)$/);
    if (m) return 'universe.html?dm=' + m[1] + '&agn=' + m[2] + '&low=' + m[3] + '&medium=' + m[4] + '&high=' + m[5];
    const g = code.replace(/[-\s]/g, '_');
    if (D.galaxies[g]) return 'galaxy.html?type=' + g;
    return null;
  }

  /* ---------- building blocks ---------- */
  function videoBlock(normalSrc, holoSrc, normalText, holoText) {
    const box = el('div');
    const vb = el('div', { class: 'vidbox' });
    const v = el('video', { controls: '', loop: '', muted: '', playsinline: '', preload: 'metadata' });
    v.muted = true;
    vb.appendChild(v);
    const row = el('div', { class: 'btnrow' });
    const bN = el('button', { type: 'button', class: 'btn ghost on' }, 'Normal video');
    const bH = el('button', { type: 'button', class: 'btn ghost' }, 'Hologram video');
    row.append(bN, bH);
    const txt = el('div');
    function show(holo) {
      bN.classList.toggle('on', !holo); bH.classList.toggle('on', holo);
      vb.classList.toggle('holo', holo);
      txt.innerHTML = holo ? holoText : normalText;
      const src = holo ? holoSrc : normalSrc;
      if (v.getAttribute('src') !== src) { v.setAttribute('src', src); v.load(); }
      v.play().catch(() => {});
    }
    bN.onclick = () => show(false); bH.onclick = () => show(true);
    box.append(vb, row, txt);
    show(false);
    return box;
  }
  function compareBlock(realSrc, simSrc) {
    const c = el('div', { class: 'compare' });
    const bottom = el('img', { src: simSrc, alt: 'Simulation', loading: 'eager' });
    const top = el('div', { class: 'top' }); top.appendChild(el('img', { src: realSrc, alt: 'Real galaxy (telescope image)' }));
    const handle = el('div', { class: 'handle' });
    const r = el('input', { type: 'range', min: 0, max: 100, value: 50, 'aria-label': 'Slide between the real image and the simulation' });
    r.oninput = () => { top.style.clipPath = 'inset(0 ' + (100 - r.value) + '% 0 0)'; handle.style.left = r.value + '%'; };
    c.append(bottom, top, handle, el('span', { class: 'tag l' }, 'Telescope'), el('span', { class: 'tag r' }, 'Simulation'), r);
    return c;
  }
  function pieBlock(values) {
    const { labels, colors } = D.galaxyPie;
    const total = values.reduce((a, b) => a + b, 0);
    let acc = 0; const stops = [];
    values.forEach((v, i) => { const a = acc / total * 360, b = (acc + v) / total * 360; stops.push(colors[i] + ' ' + a.toFixed(1) + 'deg ' + b.toFixed(1) + 'deg'); acc += v; });
    const p = el('div', { class: 'pie' });
    const disc = el('div', { class: 'disc', role: 'img', 'aria-label': 'Pie chart of what the galaxy is made of' });
    disc.style.background = 'conic-gradient(' + stops.join(',') + ')';
    const ul = el('ul');
    values.forEach((v, i) => { const li = el('li'); li.append(el('i'), document.createTextNode(labels[i] + ': ' + Math.round(v / total * 100) + '%')); li.firstChild.style.background = colors[i]; ul.appendChild(li); });
    p.append(disc, ul);
    return p;
  }
  const card = (html, cls) => el('div', { class: 'card' + (cls ? ' ' + cls : '') }, html);
  function figureRow(imgSrc, html, imgRight) {
    const row = el('div', { class: 'cols' });
    const a = el('div', { class: 'card' }); a.appendChild(el('img', { src: imgSrc, alt: '', loading: 'lazy' }));
    const b = card(html);
    row.append(...(imgRight ? [b, a] : [a, b]));
    return row;
  }
  function linksPage(keys) {
    const row = el('div', { class: 'cols' });
    keys.forEach(k => { const L = D.links[k]; const a = el('a', { class: 'card linkcard', href: L.href, target: '_blank', rel: 'noopener' }); a.append(el('img', { src: L.img, alt: L.alt, loading: 'lazy' }), el('p', null, L.text)); row.appendChild(a); });
    return row;
  }

  /* ---------- page runner: renders one sub-page at a time ---------- */
  function runPages(root, pages, baseQuery) {
    let cur = 0;
    const titleEl = el('h1', { class: 'sectitle' });
    const body = el('div');
    const nav = el('div', { class: 'pagenav' });
    const dots = el('div', { class: 'dots' });
    root.replaceChildren(titleEl, body, nav, dots);
    function go(i, push) {
      cur = Math.min(pages.length - 1, Math.max(0, i));
      const pg = pages[cur];
      titleEl.textContent = pg.title;
      body.replaceChildren(...pg.build());
      nav.replaceChildren();
      if (cur > 0) { const b = el('button', { type: 'button', class: 'btn' }, '&larr; ' + pages[cur - 1].title); b.onclick = () => go(cur - 1, true); nav.appendChild(b); } else nav.appendChild(el('span', { class: 'spacer' }));
      if (cur < pages.length - 1) { const b = el('button', { type: 'button', class: 'btn' }, pages[cur + 1].title + ' &rarr;'); b.onclick = () => go(cur + 1, true); nav.appendChild(b); }
      dots.innerHTML = pages.map((p, j) => j === cur ? '<b>&#9679;</b>' : '<span>&#9679;</span>').join('');
      if (push) { history.pushState({ p: cur }, '', '?' + baseQuery + '&p=' + cur); window.scrollTo({ top: 0, behavior: 'smooth' }); }
      // warm the cache for the next page's media while the reader is on this one
      if (pages[cur + 1] && pages[cur + 1].prefetch) pages[cur + 1].prefetch.forEach(u => { if (!document.querySelector('link[href="' + u + '"]')) { const l = el('link', { rel: 'prefetch', href: u, as: u.endsWith('.mp4') ? 'video' : 'image' }); document.head.appendChild(l); } });
    }
    window.addEventListener('popstate', e => { const q = new URLSearchParams(location.search); go(clampInt(q.get('p'), 0, pages.length - 1, 0), false); });
    const q = new URLSearchParams(location.search);
    go(clampInt(q.get('p'), 0, pages.length - 1, 0), false);
  }

  /* ---------- Universe ---------- */
  function universePages(p) {
    const c = classify(p), U = D.universe, V = D.verdict, k = c.key;
    const side = n => 'content/universe/1_Side/' + k + '_' + n + '_EVO.mp4';
    const four = n => 'content/universe/4_Side/' + k + '_' + n + '_ROTATE_4SIDE.mp4';
    const plot = i => 'content/universe/plots/' + k + '.' + i + '.png';
    const galN = 'content/universe/1_Side_Gal/' + k + '_STARS_ROTATE_SINGLE.mp4', galH = 'content/universe/4_Side_Gal/' + k + '_STARS_ROTATE_mosaic.mp4';
    const s = score(p), code = universeCode(p);
    const codeCard = () => card('<div class="codebar"><span>Your universe code is <span class="code">' + code + '</span> &mdash; enter it on the <a href="code.html">code page</a> or share this link to get straight back here.</span><button type="button" class="btn" data-copy>Copy link</button></div>');
    return [
      { title: U.titles[0], prefetch: [side('GAS')], build: () => [card('', 'tb').appendChild(videoBlock(side('DM'), four('DM'), U.dmVid, U.dmHolo)).parentNode, card(V.dm[c.dm]), codeCard()] },
      { title: U.titles[1], prefetch: [side('STARS')], build: () => [card('', 'tb').appendChild(videoBlock(side('GAS'), four('GAS'), U.gasVid, U.gasHolo)).parentNode, card(V.agn[c.agn])] },
      { title: U.titles[2], prefetch: [galN], build: () => [card('', 'tb').appendChild(videoBlock(side('STARS'), four('STARS'), U.starsVid, U.starsHolo)).parentNode, card(V.sn[c.sn])] },
      { title: 'The biggest galaxy in your Universe', prefetch: [plot(0), plot(1)], build: () => [card('', 'tb').appendChild(videoBlock(galN, galH, '', U.galaxyHolo)).parentNode, card(U.galaxy)] },
      { title: U.titles[4], build: () => [card('<p class="score">Your score is: ' + s + '/100</p>' + V.dm[c.dm] + V.agn[c.agn] + V.sn[c.sn]), card(U.thanks)] },
      { title: U.titles[5], build: () => {
          const E = U.extra, out = [];
          out.push(figureRow(plot(0), E[1].html));
          out.push(figureRow(plot(1), E[2].html, true));
          out.push(figureRow(plot(2), E[5].html));
          out.push(figureRow(plot(3), E[6].html, true));
          return out; } },
      { title: U.titles[6], build: () => [linksPage(['apod', 'spacescoop', 'codecademy', 'eagle'])] },
    ];
  }
  function initUniverse() {
    const form = $('#maker'), result = $('#result');
    const fields = ['dm', 'low', 'medium', 'high'];
    fields.forEach(f => { const r = form.elements[f], o = $('output[for=' + f + ']', form); const upd = () => { o.textContent = r.value; }; r.addEventListener('input', upd); upd(); });
    const fill = p => { fields.forEach(f => { form.elements[f].value = p[f]; form.elements[f].dispatchEvent(new Event('input')); }); form.elements.agn.value = String(p.agn); };
    const show = (p, push) => {
      const q = 'dm=' + p.dm + '&agn=' + p.agn + '&low=' + p.low + '&medium=' + p.medium + '&high=' + p.high;
      if (push) history.pushState({}, '', '?' + q + '&p=0');
      $('#makerwrap').classList.add('hidden'); result.classList.remove('hidden');
      runPages(result, universePages(p), q);
      $('#again').classList.remove('hidden');
      window.scrollTo(0, 0);
    };
    form.addEventListener('submit', e => { e.preventDefault(); show({ dm: +form.elements.dm.value, agn: +form.elements.agn.value, low: +form.elements.low.value, medium: +form.elements.medium.value, high: +form.elements.high.value }, true); });
    $('#randomize').onclick = () => fill(randomParams());
    $('#again').onclick = () => { history.pushState({}, '', 'universe.html'); location.reload(); };
    document.addEventListener('click', e => { const b = e.target.closest('[data-copy]'); if (b) { navigator.clipboard.writeText(location.origin + location.pathname + location.search.replace(/&p=\d+/, '')).then(() => { b.textContent = 'Copied!'; }); } });
    const q = new URLSearchParams(location.search);
    if (q.has('random')) { const p = randomParams(); fill(p); history.replaceState({}, '', '?dm=' + p.dm + '&agn=' + p.agn + '&low=' + p.low + '&medium=' + p.medium + '&high=' + p.high + '&p=0'); show(p, false); }
    else { const p = readParams(q); if (p) { fill(p); show(p, false); } }
  }

  /* ---------- Galaxy ---------- */
  function galaxyPages(type) {
    const G = D.galaxies[type], C = D.galaxyCommon, dir = 'content/galaxy/' + type + '/';
    return [
      { title: G.title, prefetch: [dir + 'hst.jpg', dir + 'skirt.jpg'], build: () => [card('', 'tb').appendChild(videoBlock(dir + 'video.mp4', dir + 'holo.mp4', '', C.holo)).parentNode, card(C.intro), card('<div class="codebar"><span>Your galaxy code is <span class="code">' + type + '</span>.</span></div>')] },
      { title: C.titles[1], prefetch: [dir + 'stars.jpg'], build: () => [card('', 'tb').appendChild(compareBlock(dir + 'hst.jpg', dir + 'skirt.jpg')).parentNode, card(G.closer)] },
      { title: C.titles[2], build: () => [card('', 'tb').appendChild(pieBlock(G.pie)).parentNode, card(G.pieText)] },
      { title: C.titles[3], prefetch: [dir + 'gas.jpg'], build: () => [figureRow(dir + 'stars.jpg', G.stars)] },
      { title: C.titles[4], prefetch: [dir + 'dm.jpg'], build: () => [figureRow(dir + 'gas.jpg', G.gas)] },
      { title: C.titles[5], build: () => [figureRow(dir + 'dm.jpg', G.dm)] },
      { title: C.titles[6], build: () => [linksPage(['apod', 'spacescoop', 'galaxyzoo', 'eagle'])] },
    ];
  }
  function initGalaxy() {
    const q = new URLSearchParams(location.search);
    let type = q.get('type');
    if (!D.galaxies[type]) { type = GAL_TYPES[Math.floor(Math.random() * GAL_TYPES.length)]; history.replaceState({}, '', '?type=' + type + '&p=0'); }
    runPages($('#result'), galaxyPages(type), 'type=' + type);
    $('#another').onclick = () => { const others = GAL_TYPES.filter(t => t !== type); location.href = 'galaxy.html?type=' + others[Math.floor(Math.random() * others.length)]; };
  }

  /* ---------- Code ---------- */
  function initCode() {
    const f = $('#codeform'), msg = $('#codemsg');
    f.addEventListener('submit', e => { e.preventDefault(); const dest = parseCode(f.elements.code.value); if (dest) location.href = dest; else { msg.textContent = "Oh dear, it looks like that's not a valid code."; msg.classList.remove('hidden'); } });
  }

  const page = document.body.dataset.page;
  if (page === 'universe') initUniverse();
  else if (page === 'galaxy') initGalaxy();
  else if (page === 'code') initCode();
  window.GM = { classify, score, parseCode };
})();

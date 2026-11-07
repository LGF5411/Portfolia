/* The sky over Tallinn.
   The page colours follow the real sun above Tallinn: daylight, low sun, blue hour, twilight, night.
   Override: the "Light" buttons in the footer, or ?sky=day|low|blue|dusk|night in the address. */
(function () {
  var LAT = 59.437, LON = 24.7536, R = Math.PI / 180, TZ = 'Europe/Tallinn';
  var root = document.documentElement;
  root.classList.add('js');
  var REDUCE = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);

  /* First visit of the home page in this session: the sentence arrives with the sun (see html.intro in CSS) */
  var INTRO = false;
  if (!REDUCE && root.getAttribute('data-page') === 'home') {
    try { INTRO = !sessionStorage.getItem('intro'); sessionStorage.setItem('intro', '1'); } catch (e) { INTRO = true; }
    if (INTRO) root.classList.add('arriving');
  }

  /* Sun altitude and azimuth in degrees at time t (ms), accurate to ~1° — enough for a sky. */
  function sunAlt(t) { return sun(t).alt; }
  function sun(t) {
    var d = t / 864e5 - 10957.5;
    var g = R * (357.529 + 0.98560028 * d);
    var q = 280.459 + 0.98564736 * d;
    var L = R * (q + 1.915 * Math.sin(g) + 0.02 * Math.sin(2 * g));
    var e = R * (23.439 - 3.6e-7 * d);
    var ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L));
    var dec = Math.asin(Math.sin(e) * Math.sin(L));
    var H = R * ((18.697374558 + 24.06570982441908 * d) * 15 + LON) - ra;
    return {
      alt: Math.asin(Math.sin(R * LAT) * Math.sin(dec) + Math.cos(R * LAT) * Math.cos(dec) * Math.cos(H)) / R,
      az: Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(R * LAT) - Math.tan(dec) * Math.cos(R * LAT)) / R + 180
    };
  }
  function skyFor(a) { return a >= 10 ? 'day' : a >= 0 ? 'low' : a >= -6 ? 'blue' : a >= -12 ? 'dusk' : 'night'; }
  var WORDS = { day: 'daylight', low: 'low sun', blue: 'blue hour', dusk: 'twilight', night: 'night' };
  var BG = { day: '#E4EAEE', low: '#EFE1D2', blue: '#22355A', dusk: '#131C31', night: '#0A0D14' };
  var forced = (location.search.match(/[?&]sky=(day|low|blue|dusk|night)\b/) || [])[1];

  function pref() { try { return localStorage.getItem('sky') || 'auto'; } catch (e) { return 'auto'; } }
  function setPref(v) { try { localStorage.setItem('sky', v); } catch (e) {} }

  var alt = 0, real = 'night';
  function applySky() {
    var pos = sun(Date.now());
    alt = pos.alt; real = skyFor(alt);
    var p = pref(), s = forced || (p === 'day' ? 'day' : p === 'night' ? 'night' : real);
    root.setAttribute('data-sky', s);
    /* The page is a window facing south: east on the left, west on the right, the horizon at the bottom edge */
    root.style.setProperty('--gx', Math.max(-40, Math.min(140, (pos.az - 90) / 180 * 100)).toFixed(1) + '%');
    root.style.setProperty('--gy', (100 - alt * 1.6).toFixed(1) + '%');
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', BG[s]);
  }
  applySky();

  /* Tallinn wall time */
  var hmFmt = null, partsFmt = null;
  try {
    hmFmt = new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
    partsFmt = new Intl.DateTimeFormat('en-GB', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
  } catch (e) {}
  function hm(t) { return hmFmt ? hmFmt.format(new Date(t)) : ''; }
  function midnight(now) {
    if (!partsFmt) return now - (now % 864e5);
    var p = {};
    partsFmt.formatToParts(new Date(now)).forEach(function (x) { p[x.type] = x.value; });
    var wall = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute);
    return Date.UTC(+p.year, +p.month - 1, +p.day) - (wall - Math.floor(now / 6e4) * 6e4);
  }
  function degText(a) { return Math.round(Math.abs(a)) + '° ' + (a >= 0 ? 'above' : 'below') + ' the horizon'; }

  /* Today's sun path, drawn as thin lines: x = time of day, y = altitude */
  var STEP = 3e5, N = 288, W = 400, H0 = 150, K = 130 / 60;
  var NS = 'http://www.w3.org/2000/svg';
  var sunSvg = null, dot, drop, today = null, cap = null, sunText = '', hovering = false;
  function y(a) { return H0 - a * K; }
  function el(n, at) { var e = document.createElementNS(NS, n); for (var k in at) e.setAttribute(k, at[k]); return e; }
  function computeDay(now) {
    var m0 = midnight(now), pts = [], rise = null, set = null, prev = null, c = -0.833;
    for (var i = 0; i <= N; i++) {
      var t = m0 + i * STEP, a = sunAlt(t);
      pts.push((i / N * W).toFixed(1) + ' ' + y(a).toFixed(1));
      if (prev !== null) {
        var tc = t - STEP + STEP * (c - prev) / (a - prev);
        if (prev < c && a >= c && rise === null) rise = tc;
        if (prev >= c && a < c && set === null) set = tc;
      }
      prev = a;
    }
    return { m0: m0, d: 'M' + pts.join('L'), rise: rise, set: set };
  }
  function buildSun() {
    today = computeDay(Date.now());
    sunSvg.setAttribute('viewBox', '0 0 400 300');
    while (sunSvg.firstChild) sunSvg.removeChild(sunSvg.firstChild);
    var defs = el('defs', {}), cp = el('clipPath', { id: 'sky-above' });
    cp.appendChild(el('rect', { x: -10, y: -40, width: 420, height: H0 + 40 }));
    defs.appendChild(cp); sunSvg.appendChild(defs);
    sunSvg.appendChild(el('line', { 'class': 'h', x1: 0, y1: H0, x2: W, y2: H0 }));
    [0, 100, 200, 300, 400].forEach(function (x) { sunSvg.appendChild(el('line', { 'class': 'tick', x1: x, y1: H0 - 5, x2: x, y2: H0 + 5 })); });
    sunSvg.appendChild(el('path', { 'class': 'below', d: today.d }));
    sunSvg.appendChild(el('path', { 'class': 'above', d: today.d, 'clip-path': 'url(#sky-above)' }));
    drop = el('line', { 'class': 'drop' }); sunSvg.appendChild(drop);
    dot = el('circle', { 'class': 'now', r: 7 }); sunSvg.appendChild(dot);
  }
  function placeDot(t) {
    var x = ((t - today.m0) / 864e5 * W).toFixed(1), a = sunAlt(t), yy = y(a).toFixed(1);
    dot.setAttribute('cx', x); dot.setAttribute('cy', yy);
    dot.setAttribute('class', 'now ' + (a >= -0.833 ? 'up' : 'down'));
    drop.setAttribute('x1', x); drop.setAttribute('x2', x); drop.setAttribute('y1', H0); drop.setAttribute('y2', yy);
  }
  function travelDot(now) {
    /* On load the sun travels from midnight to now: it shows where in the day Tallinn is. */
    if (REDUCE) { placeDot(now); return; }
    var start = null, from = today.m0, dur = INTRO ? 2600 : 1200;
    function f(ts) {
      if (start === null) start = ts;
      var k = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - k, 3);
      placeDot(from + (now - from) * e);
      if (k < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  }

  function updateTexts() {
    var now = Date.now(), i, n;
    n = document.querySelectorAll('.js-now');
    for (i = 0; i < n.length; i++) n[i].textContent = ', where it’s ' + hm(now) + ' and the sun is ' + degText(alt);
    n = document.querySelectorAll('.js-sky');
    for (i = 0; i < n.length; i++) n[i].textContent = 'Colours follow the sky over Tallinn — ' + hm(now) + ', ' + WORDS[real] + '.';
    if (sunSvg && today) {
      sunText = 'Tallinn today: ' + (today.rise && today.set ? 'sunrise ' + hm(today.rise) + ', sunset ' + hm(today.set) + '. ' : '') +
        'Now ' + hm(now) + ', the sun is ' + degText(alt) + '.';
      if (cap && !hovering) cap.textContent = sunText;
    }
  }

  /* Home: hovering a part of the sentence previews that project */
  function initPreview() {
    var win = document.querySelector('.window');
    if (!win) return;
    var frame = win.querySelector('.frame'), imgs = {}, active = null;
    cap = win.querySelector('figcaption');
    var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
    Array.prototype.forEach.call(document.querySelectorAll('.sentence a[data-slug]'), function (a) {
      var slug = a.getAttribute('data-slug');
      if (fine) {
        var im = new Image();
        im.alt = ''; im.className = 'pv';
        im.onload = function () { imgs[slug] = im; frame.appendChild(im); };
        im.src = a.getAttribute('data-cover');
      }
      function on() {
        if (fine && !root.classList.contains('arriving')) { a.classList.remove('play'); void a.offsetWidth; a.classList.add('play'); }
        active = a; hovering = true;
        var cur = imgs[slug];
        win.classList.toggle('showing', !!cur);
        for (var k in imgs) imgs[k].classList.toggle('on', imgs[k] === cur);
        cap.textContent = a.getAttribute('data-meta');
      }
      function off() {
        a.classList.remove('play');
        if (active !== a) return;
        active = null; hovering = false;
        win.classList.remove('showing');
        for (var k in imgs) imgs[k].classList.remove('on');
        cap.textContent = sunText;
      }
      a.addEventListener('mouseenter', on); a.addEventListener('focus', on);
      a.addEventListener('mouseleave', off); a.addEventListener('blur', off);
    });
  }

  /* Case pages: images and films load from assets/work/...; a missing file shows where to put it */
  function initMedia() {
    var reduce = REDUCE;
    Array.prototype.forEach.call(document.querySelectorAll('.shot[data-src]'), function (f) {
      var src = f.getAttribute('data-src'), frame = f.querySelector('.frame'), isV = /\.(mp4|webm)$/i.test(src);
      var m = document.createElement(isV ? 'video' : 'img');
      if (isV) {
        m.muted = true; m.loop = true; m.playsInline = true; m.setAttribute('playsinline', '');
        if (reduce) m.controls = true; else m.autoplay = true;
      } else {
        m.alt = f.getAttribute('data-alt') || ''; m.loading = 'lazy'; m.decoding = 'async';
      }
      m.addEventListener('error', function () { frame.classList.add('missing'); if (m.parentNode) m.parentNode.removeChild(m); });
      m.src = src;
      frame.insertBefore(m, frame.firstChild);
    });
  }

  /* Case pages: a rule gets crossed out when you reach it */
  function initStrikes() {
    var rules = document.querySelectorAll('.rule');
    if (!rules.length) return;
    if (!('IntersectionObserver' in window)) { Array.prototype.forEach.call(rules, function (r) { r.classList.add('struck'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('struck'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -22% 0px' });
    Array.prototype.forEach.call(rules, function (r) { io.observe(r); });
  }

  function initLight() {
    var bs = document.querySelectorAll('[data-light]');
    function sync() {
      var p = pref();
      Array.prototype.forEach.call(bs, function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-light') === p)); });
    }
    Array.prototype.forEach.call(bs, function (b) {
      b.addEventListener('click', function () { forced = null; setPref(b.getAttribute('data-light')); applySky(); sync(); updateTexts(); });
    });
    sync();
  }

  function ready() {
    sunSvg = document.querySelector('svg.sun');
    if (sunSvg) buildSun();
    initPreview(); initMedia(); initStrikes(); initLight(); updateTexts();
    if (sunSvg) travelDot(Date.now());
    if (INTRO) setTimeout(function () { root.classList.remove('arriving'); }, 3400);
    setInterval(function () {
      applySky();
      if (sunSvg) { if (midnight(Date.now()) !== today.m0) buildSun(); placeDot(Date.now()); }
      updateTexts();
    }, 60000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
})();

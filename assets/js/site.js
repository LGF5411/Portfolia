/* Portfolio behaviour. Everything here is an extra: with JS off the pages read the same, just still. */
(function () {
  var root = document.documentElement;
  /* calm = the system asks for less motion, or the visitor switched it off (set in <head>, before paint) */
  var reduce = root.classList.contains('calm');
  var osReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 0a. One site, three reading orders. ?for=product | ecommerce | beauty puts the relevant work first.
        The choice is kept for the visit, so it survives a trip into a case and back. Without it, nothing changes. */
  (function () {
    var f = null;
    try { f = new URLSearchParams(location.search).get('for') || sessionStorage.getItem('for'); } catch (e) {}
    var orders = { product: ['bolt', 'lobby', 'pilk', 'tallink'], ecommerce: ['manguarvutid', 'cosmetics', 'restart'], beauty: ['cosmetics', 'manguarvutid', 'restart'] };
    if (!f || !orders[f]) return;
    try { sessionStorage.setItem('for', f); } catch (e) {}
    var more = document.querySelector('section.more'), first = document.querySelector('section.proj');
    if (!more || !first) return;
    var order = orders[f];
    if (f === 'product') {
      order.forEach(function (id) { var el = document.getElementById(id); if (el) more.parentNode.insertBefore(el, more); });
    } else {
      first.parentNode.insertBefore(more, first);
      var grid = more.querySelector('.mgrid');
      order.forEach(function (id) { var el = document.getElementById(id); if (el) grid.appendChild(el); });
      var tpl = document.querySelector('template[data-for="' + f + '"]'), rel = document.querySelector('.hero .stage .rel'), cap = document.querySelector('.hero .cap');
      if (tpl && rel) { rel.innerHTML = ''; rel.appendChild(tpl.content.cloneNode(true)); if (cap) cap.textContent = tpl.getAttribute('data-cap'); }
    }
    var ol = document.querySelector('.index ol');
    if (ol) order.slice().reverse().forEach(function (id) {
      var a = ol.querySelector('a[href="#' + id + '"]'); if (a) ol.insertBefore(a.parentNode, ol.firstChild);
    });
  })();

  /* 0. Motion switch: footer always; header only when the system setting silenced the page. */
  [].forEach.call(document.querySelectorAll('[data-motion]'), function (b) {
    var top = b.classList.contains('motion--top');
    b.textContent = reduce ? (top ? 'Turn motion on' : 'Motion is off. Turn on') : 'Motion is on. Turn off';
    if (top) b.hidden = !(reduce && osReduce);
    b.addEventListener('click', function () {
      try { localStorage.setItem('motion', reduce ? 'on' : 'off'); } catch (e) {}
      location.reload();
    });
  });

  /* 1. Reveal on scroll. Low threshold + a failsafe, so nothing can stay hidden on a tall desktop screen. */
  var items = [].slice.call(document.querySelectorAll('[data-r]'));
  function show(el) { el.classList.add('in'); }
  if (!('IntersectionObserver' in window)) {
    items.forEach(show);
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -5% 0px' });
    items.forEach(function (el) { io.observe(el); });
    /* failsafe: anything already above the fold line after load is shown even if the observer never fires */
    window.addEventListener('load', function () {
      setTimeout(function () {
        items.forEach(function (el) {
          if (el.getBoundingClientRect().top < window.innerHeight) show(el);
        });
      }, 400);
    });
  }

  /* 2. Videos play only while on screen. */
  var vids = [].slice.call(document.querySelectorAll('video[data-auto]'));
  if ('IntersectionObserver' in window && !reduce) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { v.muted = true; vio.observe(v); });
  } else if (reduce) {
    /* calm: nothing plays by itself; case-page videos get controls, home videos stay as stills inside their links */
    vids.forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.controls = !v.closest('a'); });
  }

  /* 3. The page takes the light of the project in view. */
  var tones = [].slice.call(document.querySelectorAll('[data-tone-zone]'));
  var base = root.getAttribute('data-tone') || '';
  function tone() {
    var mid = window.innerHeight * 0.5, pick = base;
    for (var i = 0; i < tones.length; i++) {
      var r = tones[i].getBoundingClientRect();
      if (r.top <= mid && r.bottom >= mid) { pick = tones[i].getAttribute('data-tone-zone'); break; }
    }
    if (pick) root.setAttribute('data-tone', pick); else root.removeAttribute('data-tone');
  }

  /* 4. Small parallax for the phone frames. */
  var pars = reduce ? [] : [].slice.call(document.querySelectorAll('[data-par]'));
  function par() {
    var h = window.innerHeight;
    pars.forEach(function (el) {
      var host = el.parentElement.getBoundingClientRect();
      if (host.bottom < -100 || host.top > h + 100) return;
      var t = (host.top + host.height / 2 - h / 2) / h;          /* -0.5 .. 0.5 around the middle */
      el.style.transform = 'translate3d(0,' + (t * -parseFloat(el.getAttribute('data-par'))).toFixed(1) + 'px,0)';
    });
  }
  var tick = false;
  function onScroll() {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { tick = false; if (tones.length) tone(); par(); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* 5. Hero follows the pointer a little (desktop). */
  var stage = document.querySelector('.hero .stage');
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (stage && fine && !reduce) {
    window.addEventListener('pointermove', function (e) {
      stage.style.setProperty('--mx', (e.clientX / window.innerWidth - 0.5).toFixed(3));
      stage.style.setProperty('--my', (e.clientY / window.innerHeight - 0.5).toFixed(3));
    }, { passive: true });
  }

  /* 6. "Open case" label that rides the pointer over project media (desktop). */
  if (fine) {
    var c = document.createElement('div');
    c.className = 'cursor'; c.setAttribute('aria-hidden', 'true');
    document.body.appendChild(c);
    [].forEach.call(document.querySelectorAll('[data-cursor]'), function (a) {
      a.addEventListener('pointerenter', function () { c.textContent = a.getAttribute('data-cursor') + '  →'; c.classList.add('on'); });
      a.addEventListener('pointerleave', function () { c.classList.remove('on'); });
      a.addEventListener('pointermove', function (e) {
        c.style.setProperty('--x', (e.clientX + 18) + 'px');
        c.style.setProperty('--y', (e.clientY + 18) + 'px');
      });
    });
  }
})();

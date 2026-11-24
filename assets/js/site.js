/* Portfolio behaviour. Everything here is an extra: with JS off the pages read the same, just still. */
(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Reveal on scroll. Low threshold + a failsafe, so nothing can stay hidden on a tall desktop screen. */
  var items = [].slice.call(document.querySelectorAll('[data-r]'));
  function show(el) { el.classList.add('in'); }
  if (reduce || !('IntersectionObserver' in window)) {
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
    vids.forEach(function (v) { v.removeAttribute('autoplay'); v.controls = true; });
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

// Signup and unsubscribe: post to the site's API and show the result inline.
(function () {
  var params = new URLSearchParams(location.search);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // A small burst of palette confetti from the button.
  function confetti(from) {
    if (reduce || !from.animate) return;
    var r = from.getBoundingClientRect();
    var cols = ['#8A2E3B', '#7E4B6B', '#C9902F', '#24585C', '#7FA3BF', '#C9A7B5', '#4F6B3A'];
    for (var i = 0; i < 34; i++) {
      var p = document.createElement('i');
      var w = 6 + Math.random() * 6, round = Math.random() < .3;
      p.style.cssText = 'position:fixed;z-index:60;pointer-events:none;left:' + (r.left + r.width / 2) + 'px;top:' + (r.top + r.height / 2) + 'px;width:' + w + 'px;height:' + (round ? w : w * .5) + 'px;background:' + cols[i % cols.length] + ';border-radius:' + (round ? '50%' : '1px');
      document.body.appendChild(p);
      var a = -Math.PI / 2 + (Math.random() - .5) * 2.2, v = 110 + Math.random() * 160;
      var dx = Math.cos(a) * v, dy = Math.sin(a) * v, rot = (Math.random() - .5) * 720;
      p.animate([
        { transform: 'translate(-50%,-50%) rotate(0deg)', opacity: 1 },
        { transform: 'translate(calc(-50% + ' + dx + 'px),calc(-50% + ' + dy + 'px)) rotate(' + rot / 2 + 'deg)', opacity: 1, offset: .45 },
        { transform: 'translate(calc(-50% + ' + dx * 1.3 + 'px),calc(-50% + ' + (dy + 220) + 'px)) rotate(' + rot + 'deg)', opacity: 0 }
      ], { duration: 1300 + Math.random() * 600, easing: 'cubic-bezier(.2,.7,.4,1)' }).onfinish = (function (el) { return function () { el.remove(); }; })(p);
    }
  }
  function success(form, note) {
    confetti(form.querySelector('button'));
    var box = document.createElement('div');
    box.className = 'signup-ok';
    box.setAttribute('role', 'status');
    box.innerHTML = '<strong>You\u2019re in<span>.</span></strong><p>A welcome email is on its way. Your first issue lands at 9 AM IST on the next weekday.</p>';
    form.replaceWith(box);
    note.textContent = '';
  }
  function wire(form, done, fallback) {
    var input = form.querySelector('input[type=email]');
    var note = form.nextElementSibling;
    var btn = form.querySelector('button');
    if (form.hasAttribute('data-unsub') && params.get('e')) input.value = params.get('e');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (input.value || '').trim();
      if (!input.checkValidity() || !email) { input.reportValidity(); return; }
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = 'One moment…';
      fetch(form.getAttribute('action'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, website: form.querySelector('.hp').value, source: location.pathname })
      }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok && d.ok, d: d }; }); })
        .then(function (res) {
          if (res.ok && form.hasAttribute('data-signup')) { success(form, note); }
          else if (res.ok) { form.classList.add('done'); input.value = ''; note.textContent = done; btn.textContent = label; }
          else { note.textContent = (res.d && res.d.error) || fallback; btn.disabled = false; btn.textContent = label; }
        })
        .catch(function () { note.textContent = fallback; btn.disabled = false; btn.textContent = label; });
    });
  }
  document.querySelectorAll('form[data-signup]').forEach(function (f) {
    wire(f, "You're in. Your first issue arrives at 9 AM IST on the next weekday.", 'Something went wrong. Please try again in a minute.');
  });
  document.querySelectorAll('form[data-unsub]').forEach(function (f) {
    wire(f, "You're unsubscribed. No more issues will be sent to that address.", 'Something went wrong. Please try again in a minute.');
  });
})();

// Latest issue: trim the summary so the text column ends level with the image, then "Read the issue".
(function () {
  var narrow = window.matchMedia('(max-width:860px)');
  function fit() {
    document.querySelectorAll('.clamp').forEach(function (p) {
      p.style.maxHeight = '';
      if (narrow.matches) { p.style.webkitLineClamp = ''; return; }
      var lh = parseFloat(getComputedStyle(p).lineHeight) || 30;
      var n = Math.max(2, Math.floor(p.clientHeight / lh));
      p.style.webkitLineClamp = String(n);
      p.style.maxHeight = n * lh + 'px';
    });
  }
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('load', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();

// Nav: scrolls away as you read, slides back in as soon as you scroll up.
(function () {
  var nav = document.querySelector('header.nav');
  if (!nav) return;
  var spacer = document.createElement('div');
  nav.parentNode.insertBefore(spacer, nav);
  var inFlow = getComputedStyle(nav).position !== 'absolute';
  var last = window.scrollY, pinned = false, ticking = false;
  function pin() {
    if (pinned) return;
    pinned = true;
    if (inFlow) spacer.style.height = nav.offsetHeight + 'px';
    nav.classList.add('pinned', 'hidden');
    requestAnimationFrame(function () { requestAnimationFrame(function () { nav.classList.remove('hidden'); }); });
  }
  function unpin() {
    if (!pinned) return;
    pinned = false;
    nav.classList.remove('pinned', 'hidden');
    spacer.style.height = '';
  }
  function update() {
    ticking = false;
    var y = window.scrollY, h = nav.offsetHeight;
    if (y <= (pinned ? 0 : h)) { unpin(); }
    else if (y < last - 6) { pin(); nav.classList.remove('hidden'); }
    else if (y > last + 6 && pinned) { nav.classList.add('hidden'); }
    if (Math.abs(y - last) > 6 || y <= 0) last = y;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', function () { inFlow = !pinned ? getComputedStyle(nav).position !== 'absolute' : inFlow; });
})();

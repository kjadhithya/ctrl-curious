// Archive: search, month, year, sort and pagination over the embedded issue list.
(function () {
  var PER = 10;
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var data = JSON.parse(document.getElementById('issues-data').textContent);
  var q = document.getElementById('q');
  var month = document.getElementById('month');
  var year = document.getElementById('year');
  var sort = document.getElementById('sort');
  var list = document.getElementById('list');
  var pager = document.getElementById('pager');
  var showing = document.getElementById('showing');
  var page = 1;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }

  // read initial state from the address bar
  var params = new URLSearchParams(location.search);
  q.value = params.get('q') || '';
  month.value = params.get('month') || '';
  year.value = params.get('year') || '';
  sort.value = params.get('sort') === 'old' ? 'old' : 'new';
  page = Math.max(1, parseInt(params.get('page') || '1', 10) || 1);

  function row(i) {
    return '<li class="row"><span class="num" aria-hidden="true">' + i.n + '</span>' +
      '<a class="pic" href="' + i.href + '" tabindex="-1" aria-hidden="true"><img src="' + esc(i.img) + '" alt="" loading="lazy"><span class="grain"></span></a>' +
      '<div class="txt"><div class="meta"><span class="tag" style="background:' + i.color + '">' + esc(i.day) + ' · ' + esc(i.theme) + '</span><span>' + esc(i.long) + '</span></div>' +
      '<h3><a href="' + i.href + '">' + esc(i.title) + '</a></h3><p>' + esc(i.dek) + '</p></div>' +
      '</li>';
  }

  function render(push) {
    var terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    var items = data.filter(function (i) {
      if (month.value && String(i.m) !== month.value) return false;
      if (year.value && String(i.y) !== year.value) return false;
      for (var k = 0; k < terms.length; k++) if (i.text.indexOf(terms[k]) === -1) return false;
      return true;
    });
    items.sort(function (a, b) { return sort.value === 'old' ? a.issue - b.issue : b.issue - a.issue; });
    var pages = Math.max(1, Math.ceil(items.length / PER));
    if (page > pages) page = pages;
    var slice = items.slice((page - 1) * PER, page * PER);

    var groups = [];
    slice.forEach(function (i) {
      var key = MONTHS[i.m - 1] + ' ' + i.y;
      var g = groups[groups.length - 1];
      if (!g || g.key !== key) groups.push((g = { key: key, items: [] }));
      g.items.push(i);
    });
    var counts = {};
    items.forEach(function (i) { var key = MONTHS[i.m - 1] + ' ' + i.y; counts[key] = (counts[key] || 0) + 1; });

    list.innerHTML = groups.length
      ? groups.map(function (g) {
          return '<section class="month"><div class="month-head"><h2>' + g.key + '</h2><span>' + plural(counts[g.key], 'issue') + '</span></div><ul class="rows">' + g.items.map(row).join('') + '</ul></section>';
        }).join('')
      : '<p class="empty">No issues match that yet. Try a different word, or clear the month and year.</p>';

    showing.textContent = items.length === data.length ? 'Showing ' + plural(items.length, 'issue') : 'Showing ' + plural(items.length, 'issue') + ' of ' + data.length;

    var btns = '<button type="button" data-p="' + (page - 1) + '"' + (page === 1 ? ' disabled' : '') + '>← Newer</button>';
    for (var p = 1; p <= pages; p++) btns += '<button type="button" data-p="' + p + '"' + (p === page ? ' aria-current="page"' : '') + '>' + p + '</button>';
    btns += '<button type="button" data-p="' + (page + 1) + '"' + (page === pages ? ' disabled' : '') + '>Older →</button>';
    if (sort.value === 'old') btns = btns.replace('← Newer', '← Previous').replace('Older →', 'Next →');
    pager.innerHTML = '<span>Page ' + page + ' of ' + pages + '</span><div class="pg">' + btns + '</div>';

    if (push) {
      var s = new URLSearchParams();
      if (q.value) s.set('q', q.value);
      if (month.value) s.set('month', month.value);
      if (year.value) s.set('year', year.value);
      if (sort.value === 'old') s.set('sort', 'old');
      if (page > 1) s.set('page', page);
      var qs = s.toString();
      history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
    }
  }

  var t;
  q.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { page = 1; render(true); }, 120); });
  [month, year, sort].forEach(function (el) { el.addEventListener('change', function () { page = 1; render(true); }); });
  pager.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-p]');
    if (!b || b.disabled) return;
    page = parseInt(b.getAttribute('data-p'), 10);
    render(true);
    document.getElementById('showing').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  render(false);
})();

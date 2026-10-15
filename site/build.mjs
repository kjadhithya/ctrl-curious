// Builds the Ctrl+Curious website into ./public from the issue files in ./issues.
// No dependencies: run with `node site/build.mjs` (Vercel runs this on every push).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'public');
const SITE = 'https://ctrl-curious.vercel.app';
const SIGNUP_TO = 'kjadhithya05@gmail.com';
const RAW = 'https://raw.githubusercontent.com/kjadhithya/ctrl-curious/main/';

const DAYS = {
  1: { name: 'Monday', theme: 'The wave', color: '#2B4C6F', art: 'assets/email/days/mon/mon_02.jpg' },
  2: { name: 'Tuesday', theme: 'Night shift', color: '#1C3050', art: 'assets/email/days/tue/tue_07.jpg' },
  3: { name: 'Wednesday', theme: 'Type specimen', color: '#7E4B6B', art: 'assets/email/days/wed/wed_01.jpg' },
  4: { name: 'Thursday', theme: 'Field notes', color: '#24585C', art: 'assets/email/days/thu/thu_02.jpg' },
  5: { name: 'Friday', theme: 'Weekend tabs', color: '#8A2E3B', art: 'assets/email/days/fri/fri_05.jpg' },
};
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

// ---------- helpers ----------
const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const pad = (n) => String(n).padStart(3, '0');
const safeUrl = (u) => (/^https?:\/\//i.test(u || '') ? u : '#');
const linkify = (md) =>
  esc(md).replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, (_, t, u) => `<a class="link" href="${u}">${t}</a>`);
const plain = (md) => String(md).replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
const img = (u) => {
  if (!u) return '/assets/email/days/thu/thu_01.jpg';
  if (u.startsWith(RAW)) return '/' + u.slice(RAW.length);
  if (u.startsWith('assets/')) return '/' + u;
  return u;
};
function parseDate(s) {
  const [y, m, d] = s.split('-').map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  return { y, m, d, wd: dt.getUTCDay(), dt };
}
const longDate = (p) => `${['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][p.wd]}, ${p.d} ${MONTHS[p.m - 1]} ${p.y}`;
const plural = (n, w) => `${n} ${w}${n === 1 ? '' : 's'}`;

// ---------- load issues ----------
const issueDir = path.join(ROOT, 'issues');
const issues = fs
  .readdirSync(issueDir)
  .filter((f) => /^\d{3}\.json$/.test(f))
  .map((f) => {
    const j = JSON.parse(fs.readFileSync(path.join(issueDir, f), 'utf8'));
    const p = parseDate(j.date);
    const day = DAYS[p.wd] || { name: longDate(p).split(',')[0], theme: 'Extra', color: '#7E4B6B' };
    return {
      ...j,
      num: pad(j.issue),
      p,
      day,
      long: longDate(p),
      href: `/issues/${pad(j.issue)}`,
      heroSrc: img(j.hero),
      reads: j.reads || [],
      watch: j.watch || [],
      meetups: j.meetups || [],
    };
  })
  .sort((a, b) => b.issue - a.issue);

// ---------- shared chrome ----------
const LOGO_SVG = (fill) =>
  `<svg viewBox="0 0 86 86" aria-hidden="true"><rect x="29" y="0" width="28" height="86" fill="${fill}"/><rect x="0" y="29" width="86" height="28" fill="${fill}"/></svg>`;
const logo = (dark = false) =>
  `<a class="logo${dark ? ' dark' : ''}" href="/" aria-label="Ctrl+Curious home"><span class="lr"><span class="a">CTRL</span>${LOGO_SVG(dark ? '#C9A7B5' : '#8A2E3B')}</span><span class="b">Curious</span></a>`;

function nav(current, rule = true) {
  const item = (href, label, key, cls = '') =>
    `<li${cls ? ` class="${cls}"` : ''}><a href="${href}"${current === key ? ' aria-current="page"' : ''}>${label}</a></li>`;
  return `<header class="nav wrap${rule ? ' rule' : ''}">${logo()}<nav aria-label="Main"><ul>${item('/archive', 'Archive', 'archive')}${item('/#week', 'The week', 'week', 'hide-s')}${item('/about', 'About', 'about', 'hide-xs')}<li><a class="btn" href="#signup">Get the emails</a></li></ul></nav></header>`;
}

const signupForm = (id, note) => `<form class="signup" data-signup action="mailto:${SIGNUP_TO}" method="post" enctype="text/plain">
<label class="sr" for="${id}">Your email</label>
<input id="${id}" name="email" type="email" required autocomplete="email" placeholder="you@studio.com">
<button class="btn" type="submit">Get the emails</button>
</form><p class="signup-note" aria-live="polite">${note || ''}</p>`;

const band = () => `<section class="band" id="signup" aria-labelledby="signup-h">
<img src="/assets/blog/signup_wine_sunset_soft.jpg" alt="" loading="lazy">
<div class="band-copy wrap">
<h2 id="signup-h">Get the emails.<br>Stay curious.</h2>
<p>Every weekday at 10:00 IST: a linked summary, five reads, three videos and the meetups in Bengaluru and online.</p>
${signupForm('email-band')}
</div></section>`;

const footer = () => `<footer class="foot wrap">${logo(true)}
<ul><li><a href="/archive">Archive</a></li><li><a href="/about">About</a></li><li><a href="mailto:${SIGNUP_TO}?subject=Ctrl%2BCurious%20link%20suggestion">Suggest a link</a></li><li><a href="/feed.xml">RSS</a></li></ul>
<small>A daily design digest from Bengaluru.</small><div class="grain-d"></div></footer>`;

function page({ title, desc, body, canonical, image }) {
  const t = title ? `${title} · Ctrl+Curious` : 'Ctrl+Curious · Catch the next wave in design';
  const d = desc || "A daily design digest. Spot what's rising in design before everyone's talking about it. Five reads, three videos, every weekday.";
  const og = SITE + (image || '/assets/blog/banner_swell_wave_mountain_sun_tall.jpg');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(t)}</title>
<meta name="description" content="${esc(d)}">
<link rel="canonical" href="${SITE}${canonical || '/'}">
<meta property="og:title" content="${esc(t)}">
<meta property="og:description" content="${esc(d)}">
<meta property="og:image" content="${esc(og)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F4EEE8">
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/static/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Ctrl+Curious" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
${body}
${footer()}
<script src="/static/site.js" defer></script>
</body>
</html>
`;
}

// ---------- pieces ----------
const tag = (i) => `<span class="tag" style="background:${i.day.color}">${esc(i.day.name)}</span>`;
const countsLine = (i) =>
  [plural(i.reads.length, 'read'), plural(i.watch.length, 'video'), i.meetups.length ? plural(i.meetups.length, 'meetup') : ''].filter(Boolean);

function row(i, h = 'h3') {
  return `<li class="row">
<span class="num" aria-hidden="true">${i.num}</span>
<a class="pic" href="${i.href}" tabindex="-1" aria-hidden="true"><img src="${esc(i.heroSrc)}" alt="" loading="lazy"><span class="grain"></span></a>
<div class="txt"><div class="meta">${tag(i)}<span>${esc(i.long)}</span></div><${h}><a href="${i.href}">${esc(i.title)}</a></${h}><p>${esc(i.dek || '')}</p></div>
</li>`;
}

// ---------- home ----------
function home() {
  const latest = issues[0];
  const latestHtml = latest
    ? `<section class="latest wrap" aria-labelledby="latest-h"><h2 class="h" id="latest-h">Latest issue</h2>
<div class="latest-grid">
<a class="pic" href="${latest.href}" tabindex="-1" aria-hidden="true"><img src="${esc(latest.heroSrc)}" alt=""><span class="grain"></span></a>
<div class="latest-body">
<div class="meta">${tag(latest)}<span>Issue ${latest.num} · ${latest.p.d} ${MONTHS[latest.p.m - 1]} ${latest.p.y}</span></div>
<h2><a href="${latest.href}">${esc(latest.title)}</a></h2>
<p class="clamp">${linkify(latest.summary)}</p>
<a class="more" href="${latest.href}">Read the issue →</a>
</div></div></section>`
    : '';
  const days = Object.entries(DAYS)
    .map(([wd, d]) => {
      const last = issues.find((i) => i.p.wd === Number(wd));
      const inner = `<span class="pic"><img src="/${d.art}" alt="" loading="lazy"><span class="grain"></span></span><span><b>${d.name}</b><span>${d.theme}</span></span><i style="background:${d.color}"></i>`;
      return last
        ? `<a class="day" href="${last.href}" style="text-decoration:none" aria-label="${d.name}, ${d.theme}: latest ${d.name} issue">${inner}</a>`
        : `<div class="day">${inner}</div>`;
    })
    .join('');
  const recent = issues.slice(0, 8).map((i) => row(i)).join('');
  const body = `<main id="main">
<section class="hero" aria-labelledby="hero-h">
<div class="art-ext" aria-hidden="true"><img src="/assets/blog/hero/bg.webp" alt=""><img class="band b1" src="/assets/blog/hero/band1.webp" alt=""><img class="band b2" src="/assets/blog/hero/band2.webp" alt=""><img class="band b3" src="/assets/blog/hero/band3.webp" alt=""><img class="band b4" src="/assets/blog/hero/band4.webp" alt=""><img class="band b5" src="/assets/blog/hero/band5.webp" alt=""><img class="band b6" src="/assets/blog/hero/band6.webp" alt=""></div>
<div class="art" role="img" aria-label="A great wave rising and falling over moving swell lines, a small plum mountain under its curl and a wine sun high in the sky"><img src="/assets/blog/hero/bg.webp" alt="" fetchpriority="high"><img class="wave" src="/assets/blog/hero/wave.webp" alt=""><img class="band b1" src="/assets/blog/hero/band1.webp" alt=""><img class="band b2" src="/assets/blog/hero/band2.webp" alt=""><img class="band b3" src="/assets/blog/hero/band3.webp" alt=""><img class="band b4" src="/assets/blog/hero/band4.webp" alt=""><img class="band b5" src="/assets/blog/hero/band5.webp" alt=""><img class="band b6" src="/assets/blog/hero/band6.webp" alt=""></div>
${nav('home', false)}
<div class="hero-copy">
<div class="kicker">A daily design digest · weekdays at 10:00 IST</div>
<h1 id="hero-h">Catch the next wave in design.</h1>
<p class="lede">Spot what&rsquo;s rising in design before everyone&rsquo;s talking about it. Five reads, three videos, every weekday.</p>
${signupForm('email-hero')}
</div>
<span class="grain"></span>
</section>
<div class="strip" aria-hidden="true"></div>
${latestHtml}
<section class="week wrap" id="week" aria-labelledby="week-h">
<div class="week-head"><h2 class="h" id="week-h">The week, by day</h2><p>Every weekday has its own look and its own rotating artwork, so Tuesday never feels like Monday.</p></div>
<div class="days">${days}</div><span class="grain"></span>
</section>
<section class="recent wrap" aria-labelledby="recent-h">
<div class="recent-head"><h2 class="h" id="recent-h">Recent issues</h2><a href="/archive">View all issues →</a></div>
<ul class="rows">${recent}</ul>
<div class="center"><a class="btn-ghost" href="/archive">View all issues</a></div>
</section>
${band()}
</main>`;
  return page({ body, canonical: '/' });
}

// ---------- archive ----------
function archive() {
  const data = issues.map((i) => ({
    n: i.num,
    issue: i.issue,
    y: i.p.y,
    m: i.p.m,
    long: i.long,
    href: i.href,
    img: i.heroSrc,
    day: i.day.name,
    theme: i.day.theme,
    color: i.day.color,
    title: i.title,
    dek: i.dek || '',
    counts: countsLine(i).slice(0, 2),
    text: [i.title, i.dek, plain(i.summary), ...i.reads.flatMap((r) => [r.title, r.source, r.note]), ...i.watch.flatMap((w) => [w.title, w.channel, w.note]), ...i.meetups.map((m) => m.name)]
      .join(' ')
      .toLowerCase(),
  }));
  const years = [...new Set(issues.map((i) => i.p.y))].sort((a, b) => b - a);
  // server-rendered first page (works without JavaScript)
  const groups = [];
  for (const i of issues.slice(0, 10)) {
    const key = `${MONTHS[i.p.m - 1]} ${i.p.y}`;
    let g = groups.find((x) => x.key === key);
    if (!g) groups.push((g = { key, items: [] }));
    g.items.push(i);
  }
  const listHtml = groups
    .map((g) => `<section class="month"><div class="month-head"><h2>${g.key}</h2><span>${plural(g.items.length, 'issue')}</span></div><ul class="rows">${g.items.map((i) => row(i)).join('')}</ul></section>`)
    .join('');
  const body = `${nav('archive')}
<main id="main" class="archive">
<div class="page-head wrap">
<div class="crumb"><a href="/">Home</a> &nbsp;/&nbsp; Archive</div>
<h1>All issues</h1>
<p>Every Ctrl+Curious issue since the first one, with all its reads, videos and meetups. Search for a story you remember, or browse by month.</p>
</div>
<form class="filters" role="search" onsubmit="return false">
<div class="field grow"><label for="q">Search</label><div class="search"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="7.5" cy="7.5" r="5.5" fill="none" stroke="#2E1F25" stroke-width="1.8"/><path d="M11.5 11.5l4.5 4.5" stroke="#2E1F25" stroke-width="1.8"/></svg><input id="q" type="search" placeholder="Search stories, sources and summaries" autocomplete="off"></div></div>
<div class="field"><label for="month">Month</label><select id="month" class="wide"><option value="">All months</option>${MONTHS.map((m, k) => `<option value="${k + 1}">${m}</option>`).join('')}</select></div>
<div class="field"><label for="year">Year</label><select id="year"><option value="">All years</option>${years.map((y) => `<option value="${y}">${y}</option>`).join('')}</select></div>
<div class="field"><label for="sort">Sort</label><select id="sort" class="wide"><option value="new">Newest first</option><option value="old">Oldest first</option></select></div>
<span class="grain"></span>
</form>
<div class="showing wrap" id="showing" aria-live="polite">Showing ${plural(issues.length, 'issue')}</div>
<div class="wrap" id="list">${listHtml}</div>
<div class="pager wrap" id="pager"><span>Page 1 of ${Math.max(1, Math.ceil(issues.length / 10))}</span></div>
${band()}
</main>
<script type="application/json" id="issues-data">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>
<script src="/static/archive.js" defer></script>`;
  return page({ title: 'All issues', desc: 'Every Ctrl+Curious issue, searchable by story, source and month.', body, canonical: '/archive' });
}

// ---------- issue ----------
const PLAY = '<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><circle cx="17" cy="17" r="17" fill="#F4EEE8"/><path d="M13 10.5v13l11-6.5z" fill="#8A2E3B"/></svg>';
function issuePage(i, idx) {
  const newer = issues[idx - 1];
  const older = issues[idx + 1];
  const reads = i.reads
    .map((r, k) => `<li><span class="n">${String(k + 1).padStart(2, '0')}</span><a class="rimg" href="${esc(safeUrl(r.url))}" tabindex="-1" aria-hidden="true"><img src="/api/og?url=${encodeURIComponent(safeUrl(r.url))}" alt="" loading="lazy"></a><div><a href="${esc(safeUrl(r.url))}">${esc(r.title)}</a><span class="d">${esc(r.source)} · ${esc(r.note)}</span></div></li>`)
    .join('');
  const vids = i.watch
    .map((w) => {
      const u = `https://www.youtube.com/watch?v=${encodeURIComponent(w.id)}`;
      return `<li><a class="thumb" href="${u}" tabindex="-1" aria-hidden="true"><img src="https://img.youtube.com/vi/${encodeURIComponent(w.id)}/mqdefault.jpg" alt="" loading="lazy">${PLAY}</a><div><a class="t" href="${u}">${esc(w.title)}</a><span class="d">${esc(w.channel)} · ${esc(w.note)}</span></div></li>`;
    })
    .join('');
  const meets = i.meetups
    .map((m) => {
      const p = parseDate(m.date);
      return `<div class="event"><div class="dt"><b>${p.d}</b><span>${MONTHS[p.m - 1].slice(0, 3)}</span></div><div class="info"><b>${esc(m.name)}</b><span>${m.place ? `<span class="place">${esc(m.place)}</span>` : ''}${esc(m.details || '')}</span></div><a href="${esc(safeUrl(m.url))}">Details →</a></div>`;
    })
    .join('');
  const pn = (x, label, cls) =>
    x
      ? `<a class="${cls}" href="${x.href}"><small>${label}</small><b>Issue ${x.num} · ${x.long.replace(/ \d{4}$/, '')}</b></a>`
      : `<div class="off ${cls}"><small>${label}</small><b>${cls === 'r' ? 'This is the latest issue' : 'This is the first issue'}</b></div>`;
  const body = `${nav('', false)}
<main id="main" class="issue">
<div class="col issue-top">
<div class="crumb"><a href="/archive">All issues</a> &nbsp;/&nbsp; Issue ${i.num}</div>
<div class="meta">${tag(i)}<span>${esc(i.long)} · Issue ${i.num}</span></div>
<h1>${esc(i.title)}</h1>
</div>
<div class="issue-hero"><div class="pic"><img src="${esc(i.heroSrc)}" alt="${esc(i.hero_alt || "Today's Ctrl+Curious artwork")}"><span class="grain"></span></div><div class="strip" aria-hidden="true"></div></div>
<div class="col issue-body">
<section class="sec" aria-labelledby="brief-h"><h2 class="h" id="brief-h">Today, in brief</h2><p class="brief">${linkify(i.summary)}</p></section>
${reads ? `<section class="sec" aria-labelledby="read-h" style="gap:12px"><h2 class="h" id="read-h">Read</h2><ol class="reads">${reads}</ol></section>` : ''}
${vids ? `<section class="sec" aria-labelledby="watch-h" style="gap:24px"><h2 class="h" id="watch-h">Watch</h2><ul class="vids">${vids}</ul></section>` : ''}
${meets ? `<section class="meet" aria-labelledby="meet-h"><h2 class="h" id="meet-h">Meet up</h2>${meets}<span class="grain"></span></section>` : ''}
<nav class="prevnext" aria-label="More issues">${pn(older, '← Previous', 'l')}${pn(newer, 'Next →', 'r')}</nav>
</div>
${band()}
</main>`;
  return page({ title: `Issue ${i.num}: ${i.title}`, desc: i.dek || plain(i.summary).slice(0, 160), body, canonical: i.href, image: i.heroSrc.startsWith('/') ? i.heroSrc : undefined });
}

// ---------- about ----------
function about() {
  const body = `${nav('about')}
<main id="main">
<div class="page-head wrap"><div class="crumb"><a href="/">Home</a> &nbsp;/&nbsp; About</div><h1>About Ctrl+Curious</h1></div>
<div class="wrap prose">
<p>Ctrl+Curious is a small daily design digest put together in Bengaluru. Every weekday at 10:00 IST it gathers what's moving in design: a short linked summary of the day, five reads worth your time, three videos, and the meetups happening in Bengaluru and online.</p>
<p>Each weekday has its own grainy woodblock artwork inspired by the great wave, rotating through a set of scenes so no two days in a month look the same. Every issue lands here too, so you can search back through everything.</p>
<p>Spotted something that belongs in an issue? <a class="link" href="mailto:${SIGNUP_TO}?subject=Ctrl%2BCurious%20link%20suggestion">Suggest a link</a>.</p>
</div>
${band()}
</main>`;
  return page({ title: 'About', body, canonical: '/about' });
}

function notFound() {
  const body = `${nav('')}
<main id="main"><div class="page-head wrap"><h1>This wave has passed.</h1><p>The page you were looking for isn't here. Try the <a class="link" href="/archive">archive</a> or head back <a class="link" href="/">home</a>.</p></div><div style="height:80px"></div></main>`;
  return page({ title: 'Not found', body });
}

function feed() {
  const items = issues
    .slice(0, 30)
    .map(
      (i) => `<item><title>${esc(`Issue ${i.num}: ${i.title}`)}</title><link>${SITE}${i.href}</link><guid>${SITE}${i.href}</guid><pubDate>${new Date(Date.UTC(i.p.y, i.p.m - 1, i.p.d, 4, 30)).toUTCString()}</pubDate><description>${esc(plain(i.summary))}</description></item>`
    )
    .join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Ctrl+Curious</title><link>${SITE}/</link><description>A daily design digest, weekdays at 10:00 IST.</description><language>en</language>
${items}
</channel></rss>
`;
}

// ---------- write ----------
function write(rel, content) {
  const f = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, content);
}
function copy(rel, dest = rel) {
  const s = path.join(ROOT, rel);
  const d = path.join(OUT, dest);
  fs.mkdirSync(path.dirname(d), { recursive: true });
  fs.cpSync(s, d, { recursive: true });
}

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });
copy('site/static', 'static');
copy('assets/email/days');
copy('assets/blog/hero');
for (const f of ['assets/blog/seigaiha_tile.jpg', 'assets/email/wave_hero.jpg', 'assets/blog/banner_swell_wave_mountain_sun_tall.jpg', 'assets/blog/signup_wine_sunset_soft.jpg']) copy(f);

write('index.html', home());
write('archive.html', archive());
write('about.html', about());
write('404.html', notFound());
write('feed.xml', feed());
issues.forEach((i, idx) => write(`issues/${i.num}.html`, issuePage(i, idx)));
console.log(`Built ${issues.length} issue(s) into public/`);

// Article preview image for Ctrl+Curious.
// GET /api/og?url=<article url>  ->  the article's own share image (og:image / twitter:image),
// fetched server side and cached on Vercel's CDN, so it works in emails and on the site.
// If the article has no image or blocks the request, a Ctrl+Curious artwork is returned instead.

const FALLBACK = '/assets/email/days/thu/thu_02.jpg';
const MAX_BYTES = 5 * 1024 * 1024;
const UA = 'Mozilla/5.0 (compatible; CtrlCuriousBot/1.0; +https://ctrl-curious.vercel.app/about)';

function isPublicHttps(u) {
  try {
    const x = new URL(u);
    if (x.protocol !== 'https:') return false;
    const h = x.hostname.toLowerCase();
    if (h === 'localhost' || h.endsWith('.local') || h.endsWith('.internal')) return false;
    if (/^\d+\.\d+\.\d+\.\d+$/.test(h) || h.includes(':')) return false; // no raw IPs
    return true;
  } catch {
    return false;
  }
}

async function get(url, accept, ms = 6000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { headers: { 'user-agent': UA, accept }, redirect: 'follow', signal: ctrl.signal });
  } finally {
    clearTimeout(t);
  }
}

function findImage(html, base) {
  const head = html.slice(0, 400000);
  const metas = head.match(/<meta\b[^>]*>/gi) || [];
  const want = ['og:image:secure_url', 'og:image', 'twitter:image', 'twitter:image:src'];
  const found = {};
  for (const m of metas) {
    const key = (m.match(/\b(?:property|name)\s*=\s*["']([^"']+)["']/i) || [])[1];
    const val = (m.match(/\bcontent\s*=\s*["']([^"']+)["']/i) || [])[1];
    if (key && val && want.includes(key.toLowerCase()) && !found[key.toLowerCase()]) found[key.toLowerCase()] = val;
  }
  let src = want.map((k) => found[k]).find(Boolean);
  if (!src) {
    const link = head.match(/<link\b[^>]*rel=["']image_src["'][^>]*>/i);
    if (link) src = (link[0].match(/href=["']([^"']+)["']/i) || [])[1];
  }
  if (!src) return null;
  src = src.replace(/&amp;/g, '&').trim();
  try {
    return new URL(src, base).toString();
  } catch {
    return null;
  }
}

function fallback(request) {
  const r = Response.redirect(new URL(FALLBACK, request.url).toString(), 302);
  const h = new Headers(r.headers);
  h.set('cache-control', 'public, max-age=3600, s-maxage=86400');
  return new Response(null, { status: 302, headers: h });
}

export async function GET(request) {
  const target = new URL(request.url).searchParams.get('url') || '';
  if (!isPublicHttps(target)) return fallback(request);
  try {
    const page = await get(target, 'text/html,application/xhtml+xml');
    if (!page.ok || !(page.headers.get('content-type') || '').includes('html')) return fallback(request);
    const imgUrl = findImage(await page.text(), page.url || target);
    if (!imgUrl || !isPublicHttps(imgUrl)) return fallback(request);
    const img = await get(imgUrl, 'image/avif,image/webp,image/png,image/jpeg,image/*');
    const type = img.headers.get('content-type') || '';
    if (!img.ok || !type.startsWith('image/') || type.includes('svg')) return fallback(request);
    const buf = await img.arrayBuffer();
    if (buf.byteLength > MAX_BYTES || buf.byteLength < 200) return fallback(request);
    return new Response(buf, {
      status: 200,
      headers: {
        'content-type': type,
        'cache-control': 'public, max-age=86400, s-maxage=2592000, stale-while-revalidate=604800',
        'x-content-type-options': 'nosniff',
      },
    });
  } catch {
    return fallback(request);
  }
}

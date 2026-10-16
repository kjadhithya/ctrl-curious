// Large YouTube thumbnail for the Weekend watchlist feature video.
// GET /api/yt?id=<video id>  ->  maxresdefault.jpg when the video has one, otherwise mqdefault.jpg
// (both 16:9, no letterbox bars). Cached on Vercel's CDN for a week.
export async function GET(request) {
  const id = new URL(request.url).searchParams.get('id') || '';
  if (!/^[A-Za-z0-9_-]{6,20}$/.test(id)) return new Response('bad id', { status: 400 });
  let src = `https://img.youtube.com/vi/${id}/mqdefault.jpg`;
  try {
    const r = await fetch(`https://img.youtube.com/vi/${id}/maxresdefault.jpg`, { method: 'HEAD' });
    if (r.ok) src = `https://img.youtube.com/vi/${id}/maxresdefault.jpg`;
  } catch {}
  return new Response(null, {
    status: 302,
    headers: { location: src, 'cache-control': 'public, max-age=86400, s-maxage=604800' },
  });
}

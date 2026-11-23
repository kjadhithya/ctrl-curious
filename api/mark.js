import { resendKey } from './_notify.js';
// Jobs desk: one tap from the private jobs email marks a role as applied (or undoes it).
// It emails a short note to the owner through Resend; the daily jobs run reads these notes
// to show the "Applied so far" list. Nothing is stored here.
const OWNER = 'kjadhithya05@gmail.com';
const clip = (s, n) => String(s || '').replace(/[\r\n<>]/g, ' ').trim().slice(0, n);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function page(title, body) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,700&display=swap" rel="stylesheet">
<style>
body{margin:0;min-height:100vh;display:grid;place-items:center;background:#E9E1D9;font-family:'Source Serif 4',Georgia,serif;color:#2E1F25}
.card{width:min(520px,calc(100vw - 32px));background:#F4EEE8;border-radius:12px;overflow:hidden;box-shadow:0 1px 0 #D9C3B7}
.top{background:#2E1F25;color:#F4EEE8;padding:22px 26px;font-weight:700;font-size:15px}
.top span{color:#C8902F}
.in{padding:28px 26px 30px}
.box{display:inline-grid;place-items:center;width:28px;height:28px;border:2px solid #2E1F25;border-radius:6px;vertical-align:middle;margin-right:12px;font-size:18px;font-weight:700}
.box.on{background:#8A2E3B;border-color:#8A2E3B;color:#F4EEE8}
h1{font-size:26px;line-height:1.2;margin:0 0 16px;display:flex;align-items:center}
.co{color:#8A2E3B;font-weight:700;font-size:14px}
.ti{font-size:20px;font-weight:700;margin:4px 0 18px}
p{font-size:15px;line-height:1.55;color:#4A3540;margin:0 0 14px}
.strip{display:flex;justify-content:space-between;align-items:center;border-radius:8px;padding:14px 16px;font-size:16px;font-weight:700;margin:18px 0 18px}
.strip>span:first-child{display:inline-flex;align-items:center}
.strip.on{background:#E1EEE6;color:#1F5A3D;border:1px solid #B9D6C4}
.strip.off{background:#FFFFFF;color:#2E1F25;border:1px solid #D9C3B7}
.strip .b{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:4px;margin-right:10px;font-size:13px;box-sizing:border-box}
.strip.on .b{background:#1F5A3D;color:#FFFFFF;border:2px solid #1F5A3D}
.strip.off .b{background:#FFFFFF;border:2px solid #8C7A82}
a.k{display:inline-block;margin-top:6px;margin-right:10px;padding:8px 14px;border:1.5px solid #2E1F25;border-bottom-width:3px;border-radius:6px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;font-weight:700;color:#2E1F25;text-decoration:none}
</style></head><body><main class="card"><div class="top">Ctrl+Curious <span>·</span> Jobs desk</div><div class="in">${body}</div></main></body></html>`;
}

async function note(subject, text) {
  const key = resendKey();
  if (!key) throw new Error('RESEND_API_KEY is not set');
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: 'Ctrl+Curious <onboarding@resend.dev>', to: [OWNER], subject, text }),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}`);
}

const html = (s, status = 200) => new Response(s, { status, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' } });

export async function GET(request) {
  const q = Object.fromEntries(new URL(request.url).searchParams.entries());
  const company = clip(q.c, 80), title = clip(q.t, 140), url = clip(q.u, 600), sent = clip(q.d, 40);
  const undo = q.undo === '1';
  if (!company || !title) return html(page('Jobs desk', '<h1>Nothing to mark</h1><p>This link is missing the role details.</p>'), 400);
  const action = undo ? 'not applied' : 'applied';
  try {
    await note(`Jobs desk: ${action} · ${company} · ${title}`,
      `${action}: ${company} · ${title}\nlink: ${url}\nfrom the jobs email of: ${sent}\nwhen: ${new Date().toISOString()}\nThe daily jobs run reads these notes so it never suggests a role you've applied to. Keep them (archiving is fine).`);
  } catch (e) {
    console.error(e);
    return html(page('Jobs desk', '<h1>Couldn\'t save that</h1><p>Please try the link again in a minute.</p>'), 502);
  }
  const base = `/api/mark?c=${encodeURIComponent(company)}&t=${encodeURIComponent(title)}&u=${encodeURIComponent(url)}&d=${encodeURIComponent(sent)}`;
  const body = undo
    ? `<div class="co">${esc(company)}</div><div class="ti">${esc(title)}</div>
       <div class="strip off"><span><span class="b"></span>Mark applied</span></div>
       <p>Unmarked. The daily search can suggest it again if it's still open.</p><a class="k" href="${esc(base)}">Mark applied again &#8250;</a>`
    : `<div class="co">${esc(company)}</div><div class="ti">${esc(title)}</div>
       <div class="strip on"><span><span class="b">&#10003;</span>Applied</span><span style="font-weight:400;font-size:14px;">Saved</span></div>
       <p>Saved. The daily search won't suggest this role again. Good work finds good people.</p>
       ${url ? `<a class="k" href="${esc(url)}" target="_blank" rel="noopener">Open the listing &#8250;</a>` : ''}<a class="k" href="${esc(base)}&amp;undo=1">Undo</a>`;
  return html(page(undo ? 'Unmarked · Jobs desk' : 'Applied · Jobs desk', body));
}

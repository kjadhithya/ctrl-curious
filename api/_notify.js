// Shared helper: tells the editor's Gmail about a subscribe or unsubscribe, through Resend.
// The daily run reads these notes from Gmail to build the subscriber list.
// Resend's free plan can only send to the account owner, which is exactly who these go to.
const OWNER = 'kjadhithya05@gmail.com';
const EMAIL_RE = /^(?!\.)(?!.*\.\.)[^\s@<>()[\]\\,;:"]{1,64}(?<!\.)@(?!-)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,24}$/;

export function cleanEmail(raw) {
  const e = String(raw || '').trim().toLowerCase();
  return EMAIL_RE.test(e) && e.length <= 254 ? e : null;
}

export async function readBody(request) {
  const type = request.headers.get('content-type') || '';
  if (type.includes('application/json')) return await request.json().catch(() => ({}));
  const form = await request.formData().catch(() => null);
  return form ? Object.fromEntries(form.entries()) : {};
}

// The key as pasted into Vercel, minus stray spaces, quotes or a "Bearer " prefix.
export function resendKey() {
  return String(process.env.RESEND_API_KEY || '').trim().replace(/^["']|["']$/g, '').replace(/^Bearer\s+/i, '').trim();
}

export async function notify(action, email, extra = '') {
  const key = resendKey();
  if (!key) throw new Error('RESEND_API_KEY is not set');
  const when = new Date().toISOString();
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'Ctrl+Curious <onboarding@resend.dev>',
      to: [OWNER],
      subject: `Ctrl+Curious list: ${action} ${email}`,
      text: `${action}: ${email}\nwhen: ${when}\n${extra}\nThe daily run reads these notes to build the subscriber list. Keep them (archiving is fine).`,
    }),
  });
  if (!res.ok) throw new Error(`Resend ${res.status}: ${(await res.text()).slice(0, 200)}`);
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}

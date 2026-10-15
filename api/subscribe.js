import { cleanEmail, readBody, notify, json, resendKey } from './_notify.js';

export async function POST(request) {
  const body = await readBody(request);
  if (body.website) return json({ ok: true }); // honeypot: bots fill the hidden field
  const email = cleanEmail(body.email);
  if (!email) return json({ ok: false, error: 'Please enter a valid email address.' }, 400);
  try {
    await notify('subscribe', email, `source: ${String(body.source || 'website').slice(0, 40)}`);
    return json({ ok: true });
  } catch (e) {
    console.error(e);
    const detail = String(e.message || e).slice(0, 240);
    const code = /RESEND_API_KEY/.test(e.message) ? 'no_key' : /Resend 4\d\d/.test(e.message) ? 'resend_rejected' : 'send_failed';
    return json({ ok: false, code, detail, error: 'Something went wrong. Please try again in a minute.' }, 502);
  }
}

// Health check: GET /api/subscribe says whether the Resend key is configured (never its value).
// GET /api/subscribe?check=1 also asks Resend whether it accepts the key, and shows Resend's reply.
export async function GET(request) {
  const key = resendKey();
  const out = { ok: true, keyConfigured: Boolean(key), keyLooksRight: key.startsWith('re_'), keyLength: key.length, runtime: 'node' };
  if (new URL(request.url).searchParams.get('check') && key) {
    try {
      const r = await fetch('https://api.resend.com/domains', { headers: { Authorization: `Bearer ${key}` } });
      const t = (await r.text()).slice(0, 300);
      // A sending-only key answers 401 "restricted_api_key" here, which still means the key is valid.
      out.resend = { status: r.status, keyValid: r.ok || /restricted_api_key/.test(t), reply: t };
    } catch (e) { out.resend = { error: String(e.message || e).slice(0, 200) }; }
  }
  return json(out);
}

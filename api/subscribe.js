import { cleanEmail, readBody, notify, json } from './_notify.js';

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
    const code = /RESEND_API_KEY/.test(e.message) ? 'no_key' : /Resend 4\d\d/.test(e.message) ? 'resend_rejected' : 'send_failed';
    return json({ ok: false, code, error: 'Something went wrong. Please try again in a minute.' }, 502);
  }
}

// Health check: GET /api/subscribe says whether the Resend key is configured (never its value).
export function GET() {
  return json({ ok: true, keyConfigured: Boolean(process.env.RESEND_API_KEY), runtime: 'node' });
}

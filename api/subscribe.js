import { cleanEmail, readBody, notify, json, resendKey } from './_notify.js';
import { welcome } from './_welcome.js';
import { promises as dns } from 'node:dns';

// Catch typos like name@company.asd: the domain must be able to receive email.
async function domainTakesMail(email) {
  const domain = email.split('@')[1];
  try {
    const mx = await Promise.race([dns.resolveMx(domain), new Promise((_, no) => setTimeout(() => no(new Error('timeout')), 2500))]);
    return mx.length > 0;
  } catch (e) {
    return !['ENOTFOUND', 'ENODATA', 'ESERVFAIL'].includes(e.code); // unsure (timeout etc.): let it through
  }
}

export async function POST(request) {
  const body = await readBody(request);
  if (body.website) return json({ ok: true }); // honeypot: bots fill the hidden field
  const email = cleanEmail(body.email);
  if (!email) return json({ ok: false, error: 'Please enter a valid email address.' }, 400);
  if (!(await domainTakesMail(email))) return json({ ok: false, error: `Check the address: ${email.split('@')[1]} can't receive email.` }, 400);
  try {
    // Welcome first, so the note to the editor can say whether it went out.
    const w = await welcome(email);
    await notify('subscribe', email, `source: ${String(body.source || 'website').slice(0, 40)}\nwelcome: ${w}`);
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
  const out = { ok: true, welcomeHook: Boolean(process.env.WELCOME_HOOK_URL && process.env.WELCOME_HOOK_SECRET), keyConfigured: Boolean(key), keyLooksRight: key.startsWith('re_'), keyLength: key.length, runtime: 'node' };
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

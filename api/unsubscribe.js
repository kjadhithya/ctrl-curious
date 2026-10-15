import { cleanEmail, readBody, notify, json } from './_notify.js';

export async function POST(request) {
  const body = await readBody(request);
  if (body.website) return json({ ok: true });
  const email = cleanEmail(body.email);
  if (!email) return json({ ok: false, error: 'Please enter the email address you subscribed with.' }, 400);
  try {
    await notify('unsubscribe', email);
    return json({ ok: true });
  } catch (e) {
    console.error(e);
    return json({ ok: false, error: 'Something went wrong. Please try again in a minute.' }, 502);
  }
}

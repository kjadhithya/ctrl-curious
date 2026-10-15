// Instant welcome: hands a new subscriber to the Google Apps Script web app that sends
// the "Welcome to Ctrl+Curious" email from the editor's Gmail. Optional: if the two
// environment variables are not set, nothing happens and the daily run sends the welcome.
export async function welcome(email) {
  const url = String(process.env.WELCOME_HOOK_URL || '').trim();
  const secret = String(process.env.WELCOME_HOOK_SECRET || '').trim();
  if (!url || !secret) return 'off';
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 9000);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify({ email, secret }),
      redirect: 'follow',
      signal: ctrl.signal,
    });
    const text = (await r.text()).slice(0, 200);
    return /"ok":true/.test(text) ? 'sent' : 'failed: ' + text;
  } catch (e) {
    return 'failed: ' + String(e.message || e).slice(0, 120);
  } finally {
    clearTimeout(t);
  }
}

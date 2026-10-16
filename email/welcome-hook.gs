// Ctrl+Curious · instant welcome email.
// A Google Apps Script web app. The website calls it when someone signs up, and it sends
// the "Welcome to Ctrl+Curious" email from your Gmail straight away (once per address).
// Paste this into script.google.com, set SECRET to the same value as WELCOME_HOOK_SECRET
// in Vercel, then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).

const SECRET = 'PASTE_THE_SECRET_HERE';
const SITE = 'https://ctrl-curious.vercel.app';
const SUBJECT = 'Welcome to Ctrl+Curious';

function doPost(e) {
  let data = {};
  try { data = JSON.parse(e.postData.contents); } catch (err) { return reply({ ok: false, error: 'bad json' }); }
  if (data.secret !== SECRET) return reply({ ok: false, error: 'forbidden' });
  const email = String(data.email || '').trim().toLowerCase();
  if (!/^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,24}$/.test(email)) return reply({ ok: false, error: 'bad email' });

  // Never welcome anyone twice (the daily run checks Sent the same way).
  if (GmailApp.search('in:sent to:' + email + ' subject:"' + SUBJECT + '"', 0, 1).length) return reply({ ok: true, already: true });

  const unsub = SITE + '/unsubscribe?e=' + encodeURIComponent(email);
  const html = UrlFetchApp.fetch(SITE + '/email/welcome.html').getContentText().replace(/\{\{UNSUB_URL\}\}/g, unsub);
  const text = [
    "You're in.", '',
    "Thanks for subscribing to Ctrl+Curious. From the next weekday, every morning at 9:00 IST, you'll get one short email with what's moving in product and UX/UI design.", '',
    'In every issue',
    "01 Today, in brief: the day's stories in a few sentences, every claim linked to its source.",
    '02 Five reads: research, launches and lessons from real teams. No beginner guides.',
    '03 Three videos: fresh talks and interviews from people who build products.',
    '04 Meetups: design events in Bengaluru and online that are worth your evening.', '',
    "Can't wait until tomorrow? Every past issue is at " + SITE + '/archive', '',
    'See you at 9. Stay curious.',
    'Unsubscribe: ' + unsub,
  ].join('\n');
  GmailApp.sendEmail(email, SUBJECT, text, { htmlBody: html, name: 'Ctrl+Curious' });
  return reply({ ok: true });
}

// Opening the web app URL in a browser just shows that it is running.
function doGet() { return reply({ ok: true, service: 'ctrl-curious welcome' }); }

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

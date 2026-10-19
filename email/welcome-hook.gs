// Ctrl+Curious · sender, running in the editor's Google account (script.google.com).
//
// 1. Instant welcome: the website calls doPost when someone signs up, and the "Welcome to
//    Ctrl+Curious" email goes out from Gmail straight away (once per address).
// 2. Daily issue: every 5 minutes sendIssue() checks the website for a new issue. When one
//    appears it emails every subscriber their own copy, with images and a personal
//    unsubscribe link, and welcomes anyone who hasn't been welcomed yet.
//
// Setup: paste this file, set SECRET (same value as WELCOME_HOOK_SECRET in Vercel), Save, run
// setup() once from the toolbar, then Deploy > New deployment > Web app
// (Execute as: Me, Who has access: Anyone).

const SECRET = 'PASTE_THE_SECRET_HERE';
const SITE = 'https://ctrl-curious.vercel.app';
const EDITOR = 'kjadhithya05@gmail.com';
const WELCOME = 'Welcome to Ctrl+Curious';
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,24}$/;

// ---------- run once ----------
function setup() {
  ScriptApp.getProjectTriggers().forEach(t => { if (t.getHandlerFunction() === 'sendIssue') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('sendIssue').timeBased().everyMinutes(5).create();
  // Don't resend whatever issue is already out today.
  const latest = getLatest();
  if (latest) PropertiesService.getScriptProperties().setProperty('lastIssue', String(latest.issue));
  Logger.log('Ready. Subscribers: ' + subscribers().length + '. Emails left today: ' + MailApp.getRemainingDailyQuota());
}

// Optional: send the latest issue again to everyone (for example after fixing something).
function resendLatest() {
  const p = PropertiesService.getScriptProperties();
  const latest = getLatest();
  if (!latest) return;
  p.deleteProperty('sent_' + latest.issue);
  p.setProperty('lastIssue', '0');
  sendIssue();
}

// ---------- instant welcome ----------
function doPost(e) {
  let data = {};
  try { data = JSON.parse(e.postData.contents); } catch (err) { return reply({ ok: false, error: 'bad json' }); }
  if (data.secret !== SECRET) return reply({ ok: false, error: 'forbidden' });
  const email = String(data.email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(email)) return reply({ ok: false, error: 'bad email' });
  return reply({ ok: true, welcomed: welcome(email) });
}

function doGet() { return reply({ ok: true, service: 'ctrl-curious sender' }); }

function welcome(email) {
  if (GmailApp.search('in:sent to:' + email + ' subject:"' + WELCOME + '"', 0, 1).length) return false;
  const unsub = unsubUrl(email);
  const html = UrlFetchApp.fetch(SITE + '/email/welcome.html').getContentText().replace(/\{\{UNSUB_URL\}\}/g, unsub);
  const text = "You're in.\n\nThanks for subscribing to Ctrl+Curious. From the next weekday, every morning at 9:00 IST, you'll get one short email with what's moving in product and UX/UI design.\n\nEvery past issue is at " + SITE + "/archive\n\nSee you at 9. Stay curious.\nUnsubscribe: " + unsub;
  GmailApp.sendEmail(email, WELCOME, text, { htmlBody: html, name: 'Ctrl+Curious' });
  return true;
}

// ---------- daily issue ----------
function sendIssue() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;               // a previous run is still sending
  try {
    const p = PropertiesService.getScriptProperties();
    const latest = getLatest();
    if (!latest || String(latest.issue) === p.getProperty('lastIssue')) return;

    const key = 'sent_' + latest.issue;
    const done = JSON.parse(p.getProperty(key) || '[]');
    const html = UrlFetchApp.fetch(SITE + latest.html).getContentText();
    const tr = UrlFetchApp.fetch(SITE + latest.text, { muteHttpExceptions: true });
    const text = tr.getResponseCode() === 200 ? tr.getContentText() : latest.subject + '\n\nRead it online: ' + SITE + latest.web + '\n\nUnsubscribe: ' + SITE + '/unsubscribe\n';
    const started = Date.now();

    for (const email of subscribers()) {
      if (done.indexOf(email) !== -1) continue;
      if (MailApp.getRemainingDailyQuota() < 2 || Date.now() - started > 4.5 * 60 * 1000) {
        p.setProperty(key, JSON.stringify(done));  // carry on in the next run
        return;
      }
      welcome(email);
      const unsub = unsubUrl(email);
      GmailApp.sendEmail(email, latest.subject, text.split(SITE + '/unsubscribe\n').join(unsub + '\n'), {
        htmlBody: html.split('href="' + SITE + '/unsubscribe"').join('href="' + unsub + '"'),
        name: 'Ctrl+Curious',
      });
      done.push(email);
      p.setProperty(key, JSON.stringify(done));
    }
    p.setProperty('lastIssue', String(latest.issue));
    p.deleteProperty(key);
  } finally {
    lock.releaseLock();
  }
}

// The newest issue the website has published an email for, if it is from the last day.
function getLatest() {
  const r = UrlFetchApp.fetch(SITE + '/email/latest.json?t=' + Date.now(), { muteHttpExceptions: true });
  if (r.getResponseCode() !== 200) return null;
  const j = JSON.parse(r.getContentText());
  if (!j.issue || !j.html) return null;
  if (j.date) {
    const today = Utilities.formatDate(new Date(), 'Asia/Kolkata', 'yyyy-MM-dd');
    if (j.date !== today) return null;          // never send an old issue late
  }
  return j;
}

// Everyone whose latest "Ctrl+Curious list" note says subscribe (the website sends these notes).
function subscribers() {
  const latest = {};
  for (let start = 0; ; start += 100) {
    const threads = GmailApp.search('from:onboarding@resend.dev subject:"Ctrl+Curious list"', start, 100);
    threads.forEach(t => t.getMessages().forEach(m => {
      const s = m.getSubject().match(/Ctrl\+Curious list:\s*(subscribe|unsubscribe)\s+(\S+)/i);
      if (!s) return;
      const email = s[2].toLowerCase(), when = m.getDate().getTime();
      if (!latest[email] || latest[email].when < when) latest[email] = { action: s[1].toLowerCase(), when: when };
    }));
    if (threads.length < 100) break;
  }
  const dead = bounced();
  return Object.keys(latest).filter(e => latest[e].action === 'subscribe' && e !== EDITOR && EMAIL_RE.test(e) && !dead[e]);
}

// Addresses that bounced ("Address not found") when we emailed them, so typos stop getting mail.
function bounced() {
  const dead = {};
  GmailApp.search('from:mailer-daemon subject:"Delivery Status Notification" newer_than:180d', 0, 100).forEach(t => {
    const msgs = t.getMessages();
    if (!msgs.some(m => /Ctrl\+Curious/.test(m.getSubject()))) return;
    msgs.forEach(m => {
      if (/mailer-daemon/i.test(m.getFrom())) return;
      m.getTo().split(',').forEach(a => { const x = (a.match(/[^<\s]+@[^>\s]+/) || [])[0]; if (x) dead[x.toLowerCase()] = true; });
    });
  });
  return dead;
}

function unsubUrl(email) { return SITE + '/unsubscribe?e=' + encodeURIComponent(email); }

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

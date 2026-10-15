"""Fill email/template.html from an issue JSON file, using the row snippets in RUN.md.

    python3 email/build_issue.py issues/001.json out.html [hero_url]

Handy for previews and samples; the daily run can use it too."""
import html, json, re, sys, urllib.parse, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
tpl = (ROOT / 'email/template.html').read_text()
run = (ROOT / 'email/RUN.md').read_text()
issue = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = pathlib.Path(sys.argv[2])
hero = sys.argv[3] if len(sys.argv) > 3 else issue.get('hero')

def block(title):
    return re.search(r'## ' + re.escape(title) + r'.*?```html\n(.*?)\n```', run, re.S).group(1)

SUM = block('Summary link format')
READ = block('Read row')
WATCH = block('Watch row')
EVENT = block('Event card')

e = lambda t: html.escape(t, quote=False)
def summary(md):
    parts, last = [], 0
    for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', md):
        parts.append(e(md[last:m.start()]))
        parts.append(SUM.replace('URL', m.group(2)).replace('linked phrase', e(m.group(1))))
        last = m.end()
    return ''.join(parts) + e(md[last:])

rows = []
for k, r in enumerate(issue['reads']):
    x = READ.replace('>01<', f'>{k+1:02d}<').replace('URL_ENCODED', urllib.parse.quote(r['url'], safe=''))
    x = x.replace('href="URL"', f'href="{r["url"]}"').replace('Title in sentence case', e(r['title']))
    x = x.replace('Source name · One-line summary.', f"{e(r['source'])} · {e(r['note'])}")
    if k == len(issue['reads']) - 1:
        x = x.replace('padding:4px 16px 24px 0;', 'padding:4px 16px 0 0;').replace('padding-bottom:24px;', '')
    rows.append(x)

vids = []
for k, w in enumerate(issue['watch']):
    x = WATCH.replace('VIDEO_ID', w['id']).replace('Video title', e(w['title']))
    x = re.sub(r'Channel name · [^<]*', f"{e(w['channel'])} · {e(w['note'])}", x)
    if k == len(issue['watch']) - 1:
        x = x.replace('padding:0 18px 24px 0;', 'padding:0 18px 0 0;').replace(' style="padding-bottom:24px;"', '')
    vids.append(x)

MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
cards = []
for k, m in enumerate(issue.get('meetups', [])):
    d = datetime.date.fromisoformat(m['date'])
    online = m.get('place', '').lower() == 'online'
    tag = ('<span style="background-color:#C9A7B5;color:#2E1F25;padding:0 7px;">Online</span>' if online
           else f'<span style="background-color:#7E4B6B;color:#F4EEE8;padding:0 7px;">{e(m.get("place") or "Bengaluru")}</span>')
    x = EVENT.replace('>DD<', f'>{d.day}<').replace('>Mon<', f'>{MON[d.month-1]}<').replace('Event name', e(m['name']))
    x = re.sub(r'TAG&nbsp; [^<]*', f"{tag}&nbsp; {e(m.get('details', ''))}", x).replace('href="URL"', f'href="{m["url"]}"')
    if k == len(issue['meetups']) - 1:
        x = x.replace('margin-bottom:12px;', '')
    cards.append(x)

d = datetime.date.fromisoformat(issue['date'])
date_long = f"{d.strftime('%A')}, {d.day} {d.strftime('%B')} {d.year}"
page = (tpl.replace('{{DATE_LONG}}', date_long).replace('{{ISSUE}}', f"{issue['issue']:03d}")
        .replace('{{PREHEADER}}', e(issue.get('preheader') or issue.get('dek', '')))
        .replace('{{HERO_URL}}', hero).replace('{{SUMMARY_HTML}}', summary(issue['summary']))
        .replace('{{UNSUB_URL}}', 'https://ctrl-curious.vercel.app/unsubscribe').replace('{{READ_ROWS}}', '\n'.join(rows)).replace('{{WATCH_ROWS}}', '\n'.join(vids)))
if cards:
    page = page.replace('{{EVENT_CARDS}}', '\n'.join(cards))
else:
    page = re.sub(r'<!-- MEETUP_START -->.*?<!-- MEETUP_END -->', '', page, flags=re.S)
assert '{{' not in page, 'unfilled placeholder'
out.write_text(page)
print('wrote', out)

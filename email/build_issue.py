"""Fill email/template.html from an issue JSON file, using the row snippets in RUN.md.

    python3 email/build_issue.py issues/001.json out.html [hero_url]

Handy for previews and samples; the daily run can use it too."""
import html, json, re, sys, urllib.parse, datetime, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sections_v2 as V2

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

# ---------- edition sections (one per weekday; each is optional) ----------
SITE = 'https://ctrl-curious.vercel.app'
ed = issue.get('edition') or {}
og = lambda u: f"{SITE}/api/og?url={urllib.parse.quote(u, safe='')}"
A = lambda u, t, st: f'<a href="{html.escape(u)}" target="_blank" style="{st}">{e(t)}</a>'
def head(t, mark='#8A2E3B', col='#2E1F25'):
    return f'<div style="font-size:30px;line-height:33px;font-weight:700;color:{col};"><span style="color:{mark};">&gt;</span>&nbsp; {t}</div>'
RULE = '<tr><td class="pad" style="padding:0 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-top:2px solid #2E1F25;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>\n'
STRIP = f'<tr><td bgcolor="#EDE4DD" style="background-color:#EDE4DD;"><img src="{SITE}/assets/email/seigaiha_strip.jpg" width="600" height="10" alt="" style="display:block;border:0;width:100%;max-width:600px;height:10px;"></td></tr>\n'
top, mid = '', ''

if ed.get('tool'):   # Tuesday: tool of the day, right under the summary
    t = ed['tool']
    top = (f'<tr><td class="pad" style="padding:0 36px 48px 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#C9A7B5" style="background-color:#C9A7B5;"><tr><td style="padding:26px 28px 28px 28px;color:#2E1F25;">'
           + V2.heading('Tool of the day', 'New this fortnight' + (' · ' + t['meta'] if t.get('meta') else ''))
           + A(t['url'], t['name'], 'display:block;padding-top:14px;font-size:22px;line-height:29px;font-weight:700;color:#2E1F25;text-decoration:underline;text-decoration-color:#8A2E3B;text-underline-offset:3px;')
           + f'<div style="font-size:17px;line-height:26px;padding-top:8px;">{e(t["what"])}</div>'
           + '</td></tr></table></td></tr>\n')

LEARN_TITLES = {'skill': 'Skill of the week', 'install': 'Power-up', 'pattern': 'Pattern breakdown', 'method': 'Research method in practice',
                'principle': 'One principle, three examples', 'teardown': 'Teardown', 'tool': 'Tool to master', 'craft': 'Career and craft',
                'workflow': 'Workflow upgrade', 'steal': 'Steal this', 'people': 'How they work', 'prompt': 'Prompt of the week',
                'brief': '10-minute brief', 'decision': 'Decision toolkit'}
learns = ed.get('learn') or []
if isinstance(learns, dict): learns = [learns]
learn_html = ''   # rendered below, once we know what the practical sections follow
if ed.get('week'):   # Monday: three things happening this week
    cols = [('#2E1F25', '#C9A7B5', '#F4EEE8'), ('#7E4B6B', '#E9D7DE', '#F4EEE8'), ('#C9A7B5', '#5E4B53', '#2E1F25')]
    cells = []
    for k, w in enumerate(ed['week'][:3]):
        bg, lab, fg = cols[k]
        cells.append(f'<td class="wk" width="33%" valign="top" bgcolor="{bg}" style="background-color:{bg};padding:16px;"><div style="font-size:14px;line-height:20px;color:{lab};">{e(w["when"])}</div>'
                     + A(w['url'], w['title'], f'display:block;padding-top:8px;font-size:17px;line-height:23px;font-weight:600;color:{fg};text-decoration:none;') + '</td>')
    mid += RULE + (f'<tr><td class="pad" style="padding:40px 36px 22px 36px;">{V2.heading('This week in design', 'Three dates for your calendar')}</td></tr>\n'
                   f'<tr><td class="pad" style="padding:0 36px 52px 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
                   + '<td class="wks" width="12" style="font-size:0;line-height:0;">&nbsp;</td>'.join(cells) + '</tr></table></td></tr>\n')

if ed.get('typeface'):   # Wednesday: typeface spotlight
    t = ed['typeface']
    lab = lambda k, v: f'<td valign="top" width="50%" style="padding:0 12px 16px 0;"><div style="font-size:14px;line-height:20px;color:#C9A7B5;">{k}</div><div style="font-size:16px;line-height:24px;color:#F4EEE8;">{v}</div></td>'
    mid += (f'<tr><td class="pad" bgcolor="#2E1F25" background="{SITE}/assets/email/grain_dark.jpg" style="background-color:#2E1F25;background-image:url(\'{SITE}/assets/email/grain_dark.jpg\');background-repeat:repeat;padding:48px 36px 36px 36px;color:#F4EEE8;">'
            + V2.heading('Typeface spotlight', 'New in type · ' + t.get('get', 'foundry page'), dark=True)
            + A(t['url'], t['name'], 'display:block;padding-top:20px;font-size:40px;line-height:44px;font-weight:700;color:#F4EEE8;text-decoration:none;letter-spacing:-0.5px;')
            + (f'<div style="font-size:17px;line-height:26px;color:#E9DFE3;padding-top:10px;">{e(t["note"])}</div>' if t.get('note') else '')
            # A real specimen: t['image'] (rendered from the font files when the font is free, or the foundry's own image),
            # otherwise the foundry page's share image.
            + f'<a href="{html.escape(t["url"])}" target="_blank"><img class="spec" src="{html.escape(t.get("image") or og(t["url"]))}" width="528" alt="{e(t["name"])} specimen" style="display:block;border:0;width:100%;max-width:528px;height:auto;margin-top:22px;"></a>'
            + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:22px;"><tr>'
            + lab('Made by', e(t['by'])) + lab('Get it', A(t['url'], t.get('get', 'Foundry page'), 'color:#F4EEE8;text-decoration:underline;text-underline-offset:2px;')) + '</tr><tr>'
            + lab('Pair it with', e(t.get('pair', ''))) + lab('Good for', e(t.get('good_for', ''))) + '</tr></table></td></tr>\n')

if ed.get('case'):   # Thursday: case study
    c = ed['case']
    mid += STRIP + (f'<tr><td class="pad" bgcolor="#EDE4DD" background="{SITE}/assets/email/grain_band.jpg" style="background-color:#EDE4DD;background-image:url(\'{SITE}/assets/email/grain_band.jpg\');background-repeat:repeat;padding:42px 36px 52px 36px;">'
            + V2.heading('Case study', 'How a real team solved it') + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:22px;"><tr>'
            + f'<td class="ed-img" valign="top" width="200" style="padding:0 20px 0 0;"><a href="{html.escape(c["url"])}" target="_blank"><img src="{og(c["url"])}" width="200" alt="" style="display:block;border:0;width:200px;height:auto;"></a></td>'
            + f'<td valign="top"><div style="font-size:14px;line-height:20px;color:#5E4B53;">{e(c["studio"])}{" · " + e(c["client"]) if c.get("client") else ""}</div>'
            + A(c['url'], c['title'], 'display:block;padding-top:6px;font-size:20px;line-height:27px;font-weight:600;color:#2E1F25;text-decoration:none;')
            + f'<div style="font-size:15px;line-height:23px;color:#5E4B53;padding-top:6px;">{e(c["note"])}</div></td></tr></table></td></tr>\n')
prev = 'band' if ed.get('case') else ('dark' if ed.get('typeface') else 'paper')
learn_html, last = V2.render(learns, prev)
mid += learn_html   # practical sections come after the day's edition section
if len(issue['watch']) <= 3 and ((learns and last != 'paper') or (not learns and (ed.get('case') or ed.get('typeface')))):
    mid += '<tr><td style="height:48px;font-size:0;line-height:0;">&nbsp;</td></tr>\n'   # breathing room before the Watch rule
watch_title = 'Weekend watchlist' if len(issue['watch']) > 3 else 'Watch'

# Friday: the Weekend watchlist replaces the Watch section with a dark feature block
# (one big video, then a two-by-two grid), and the Inspiration shelf follows it.
weekend = ''
if len(issue['watch']) > 3:
    yt = lambda i: f"https://www.youtube.com/watch?v={i}"
    v0 = issue['watch'][0]
    def small(w):
        return (f'<td class="wk" width="50%" valign="top" style="padding:0 0 22px 0;"><a href="{yt(w["id"])}" target="_blank"><img src="https://img.youtube.com/vi/{w["id"]}/mqdefault.jpg" width="256" alt="" style="display:block;border:0;width:100%;max-width:256px;height:auto;"></a>'
                + A(yt(w['id']), w['title'], 'display:block;padding-top:10px;font-size:17px;line-height:23px;font-weight:600;color:#F4EEE8;text-decoration:none;') + '</td>')
    rest = issue['watch'][1:5]
    grid = ''
    for k in range(0, len(rest), 2):
        pair = rest[k:k+2]
        grid += '<tr>' + small(pair[0]) + '<td class="wks" width="16" style="font-size:0;line-height:0;">&nbsp;</td>' + (small(pair[1]) if len(pair) > 1 else '<td></td>') + '</tr>'
    weekend = (f'<tr><td class="pad" bgcolor="#2E1F25" background="{SITE}/assets/email/grain_dark.jpg" style="background-color:#2E1F25;background-image:url(\'{SITE}/assets/email/grain_dark.jpg\');background-repeat:repeat;padding:48px 36px 30px 36px;color:#F4EEE8;">'
               + V2.heading('Weekend watchlist', 'Five to watch with a slow coffee', dark=True)
               + f'<a href="{yt(v0["id"])}" target="_blank"><img src="{SITE}/api/yt?id={v0["id"]}" width="528" alt="" style="display:block;border:0;width:100%;max-width:528px;height:auto;margin-top:24px;"></a>'
               + A(yt(v0['id']), v0['title'], 'display:block;padding-top:16px;font-size:22px;line-height:29px;font-weight:700;color:#F4EEE8;text-decoration:none;')
               + f'<div style="font-size:15px;line-height:23px;color:#C9A7B5;padding-top:4px;">{e(v0["channel"])} · {e(v0["note"])}</div>'
               + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:26px;">{grid}</table></td></tr>\n')
    if ed.get('shelf'):
        items = ed['shelf'][:3]
        sp = '<td width="12" style="width:12px;min-width:12px;font-size:0;line-height:0;">&nbsp;</td>'
        # Images sit in fixed 1.91:1 boxes (the shape of most share images) so the row stays even,
        # and titles get their own row so they line up whatever the images do. Three columns on phones too.
        imgs = sp.join(f'<td width="33%" valign="top"><a href="{html.escape(it["url"])}" target="_blank" class="sh" style="display:block;height:88px;overflow:hidden;background-color:#7E4B6B;"><img src="{og(it["url"])}" width="168" alt="" style="display:block;border:0;width:100%;height:auto;min-height:88px;"></a></td>' for it in items)
        caps = sp.join(f'<td width="33%" valign="top" style="padding:10px 0 8px 0;">' + A(it['url'], it['title'], 'display:block;font-size:16px;line-height:22px;font-weight:600;color:#2E1F25;text-decoration:none;') + f'<div style="font-size:14px;line-height:20px;color:#5E4B53;padding-top:4px;">{e(it["credit"])}</div></td>' for it in items)
        weekend += (f'<tr><td class="pad" style="padding:48px 36px 48px 36px;">{V2.heading('Inspiration shelf', 'Three things worth a closer look')}'
                    + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:24px;"><tr>{imgs}</tr><tr>{caps}</tr></table></td></tr>\n')

d = datetime.date.fromisoformat(issue['date'])
date_long = f"{d.strftime('%A')}, {d.day} {d.strftime('%B')} {d.year}"
page = (tpl.replace('{{DATE_LONG}}', date_long).replace('{{ISSUE}}', f"{issue['issue']:03d}")
        .replace('{{PREHEADER}}', e(issue.get('preheader') or issue.get('dek', '')))
        .replace('{{HERO_URL}}', hero).replace('{{SUMMARY_HTML}}', summary(issue['summary']))
        .replace('{{EDITION_TOP}}', top).replace('{{EDITION_MID}}', mid).replace('{{WATCH_TITLE}}', watch_title)
        .replace('{{UNSUB_URL}}', 'https://ctrl-curious.vercel.app/unsubscribe').replace('{{READ_ROWS}}', '\n'.join(rows)).replace('{{WATCH_ROWS}}', '\n'.join(vids)))
if weekend:
    page = re.sub(r'<!-- WATCH_START -->.*?<!-- WATCH_END -->\n', lambda m: weekend, page, count=1, flags=re.S)
else:
    page = page.replace('<!-- WATCH_START -->', '').replace('<!-- WATCH_END -->\n', '')
if weekend:   # Friday: a bigger weekend sign-off replaces the usual footer art
    page = re.sub(r'<tr><td><img src="https://ctrl-curious\.vercel\.app/assets/email/footer_b3\.jpg"[^>]*></td></tr>',
                  f'<tr><td><img src="{SITE}/assets/email/weekend_footer.jpg" width="600" alt="The weekend’s here. Rest up. See you on Monday." style="display:block;border:0;width:100%;max-width:600px;height:auto;"></td></tr>', page, count=1)
if cards:
    page = page.replace('{{EVENT_CARDS}}', '\n'.join(cards))
else:
    page = re.sub(r'<!-- MEETUP_START -->.*?<!-- MEETUP_END -->', '', page, flags=re.S)
assert '{{' not in page, 'unfilled placeholder'
def night_shift(page):
    """Tuesday's dark 'Night shift' look: swap the light palette for the dark one above the footer
    (the footer art and bar are already dark). The Tool of the day card and small mauve or plum
    labels keep their own colours."""
    cut = page.find('<tr><td><img src="https://ctrl-curious.vercel.app/assets/email/footer_b3.jpg"')
    head, foot = (page[:cut], page[cut:]) if cut > 0 else (page, '')
    keep = {}
    def protect(m):
        keep[f'@@K{len(keep)}@@'] = m.group(0); return f'@@K{len(keep)-1}@@'
    head = re.sub(r'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#C9A7B5".*?</table>', protect, head, flags=re.S)
    head = re.sub(r'background-color:#(?:C9A7B5|7E4B6B);color:#(?:2E1F25|F4EEE8)', protect, head)
    head = re.sub(r'background="[^"]*grain_page\.jpg"', 'background="https://ctrl-curious.vercel.app/assets/email/grain_page_dark.jpg"', head)
    head = head.replace('grain_dark.jpg', 'grain_dark_soft.jpg').replace('grain_page.jpg', 'grain_page_dark.jpg').replace('grain_paper.jpg', 'grain_dark_soft.jpg').replace('grain_band.jpg', 'grain_dark_soft.jpg')
    head = head.replace('logo_light.png', 'logo_dark.png').replace('seigaiha_strip.jpg', 'seigaiha_strip_dark.jpg')
    swap = {'E9E1D9': '1E1418', 'F4EEE8': '2E1F25', '2E1F25': 'F4EEE8', 'EDE4DD': '3A2830', '5E4B53': 'C9A7B5',
            '4A3540': 'E9DFE3', '8A2E3B': 'C9A7B5', 'D9C3B7': '5E4B53'}
    head = re.sub(r'#([0-9A-Fa-f]{6})\b', lambda m: '#' + swap.get(m.group(1).upper(), m.group(1)), head)
    for k, v in keep.items():
        head = head.replace(k, v)
    return head + foot.replace('grain_dark.jpg', 'grain_dark_soft.jpg')

if datetime.date.fromisoformat(issue['date']).weekday() == 1:   # Tuesday
    page = night_shift(page)
out.write_text(page)
print('wrote', out)

# Plain-text version next to it (same name, .txt)
txt = [f"Ctrl+Curious · {date_long} · Issue {issue['issue']:03d}", f"View online: {SITE}/issues/{issue['issue']:03d}", '',
       'Today, in brief', re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'\1 (\2)', issue['summary']), '']
if ed.get('tool'): txt += ['Tool of the day', f"{ed['tool']['name']}: {ed['tool']['url']}", '']
txt += ['Read'] + [f"{r['title']}: {r['url']}" for r in issue['reads']] + ['']
for l in learns: txt += [LEARN_TITLES.get(l.get('kind'), 'Learn this week'), f"{l['title']}: {l['url']}", '']
if ed.get('week'): txt += ['This week in design'] + [f"{w['when']} · {w['title']}: {w['url']}" for w in ed['week']] + ['']
if ed.get('typeface'): txt += ['Typeface spotlight', f"{ed['typeface']['name']}: {ed['typeface']['url']}", '']
if ed.get('case'): txt += ['Case study', f"{ed['case']['title']}: {ed['case']['url']}", '']
if ed.get('shelf'): txt += ['Inspiration shelf'] + [f"{x['title']} ({x['credit']}): {x['url']}" for x in ed['shelf']] + ['']
txt += [watch_title] + [f"{w['title']}: https://www.youtube.com/watch?v={w['id']}" for w in issue['watch']] + ['']
if issue.get('meetups'): txt += ['Meet up'] + [f"{m['name']} ({m['date']}): {m['url']}" for m in issue['meetups']] + ['']
txt += ["That's all for today. Stay curious.", '', f'Unsubscribe: {SITE}/unsubscribe', '']
out.with_suffix('.txt').write_text('\n'.join(txt))
print('wrote', out.with_suffix('.txt'))

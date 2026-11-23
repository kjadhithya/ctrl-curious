# Option A · "Keycap board": dark masthead with big count, chip tags, keycap apply buttons, plum big-tech band
import json, sys, html
d = json.load(open(sys.argv[1])); out = sys.argv[2]; BASE = sys.argv[3] if len(sys.argv) > 3 else 'https://ctrl-curious.vercel.app'
e = html.escape
INK, PAPER, WINE, MUTED, CLAY, BAND, PLUM, MAUVE, OCHRE = '#2E1F25', '#F4EEE8', '#8A2E3B', '#5E4B53', '#D9C3B7', '#EDE4DD', '#7E4B6B', '#C9A7B5', '#C8902F'
T = '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
def chip(t, bg=BAND, fg=INK):
    return f'<span style="display:inline-block;margin:0 6px 6px 0;padding:3px 10px;border-radius:999px;background-color:{bg};color:{fg};font-size:12px;line-height:18px;font-weight:600;">{e(t)}</span>'
def key(url, label):
    return (f'<a href="{e(url)}" target="_blank" style="display:inline-block;padding:7px 12px;background-color:{PAPER};border:1.5px solid {INK};border-bottom-width:3px;border-radius:6px;'
            f'font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;line-height:16px;font-weight:700;color:{INK};text-decoration:none;white-space:nowrap;">{e(label)} &#8250;</a>')
from urllib.parse import quote
TEAL = '#24585C'
GREEN, GREEN_BG, GREEN_TXT = '#1F5A3D', '#E1EEE6', '#3F6B54'
def mark(j):
    href = ('https://ctrl-curious.vercel.app/api/mark?c=' + quote(j['company']) + '&t=' + quote(j['title'])
            + '&u=' + quote(j['url'], safe='') + '&d=' + quote(d.get('iso', '')))
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px;"><tr>'
            f'<td bgcolor="#EDE4DD" style="background-color:#EDE4DD;border-radius:8px;padding:10px 14px;font-size:14px;line-height:20px;font-weight:400;">'
            f'<a href="{e(href)}" target="_blank" style="display:block;color:#5E4B53;text-decoration:none;"><span style="display:inline-block;width:14px;height:14px;border:2px solid #5E4B53;border-radius:4px;vertical-align:-3px;margin-right:10px;background-color:#FFFFFF;"></span>Mark applied</a></td></tr></table>')
def rows(jobs, card):
    r = ''
    for k, j in enumerate(jobs):
        p = j['posted'].lower()
        fresh = any(w in p for w in ('hour', 'yesterday', '1 day', 'today', 'minute'))
        chips = chip(j['location']) + (chip(j['mode']) if j.get('mode') else '') + chip(j['posted'].replace('Posted ', ''), WINE if fresh else BAND, PAPER if fresh else INK)
        dom = (j.get('domain') or '').strip()
        if dom:
            logo = f'<img src="https://www.google.com/s2/favicons?domain={e(dom)}&amp;sz=128" width="28" height="28" alt="{e(j["company"])} logo" style="display:block;border:0;width:28px;height:28px;border-radius:4px;">'
            tile = f'<td width="44" height="44" align="center" valign="middle" bgcolor="#FFFFFF" style="width:44px;height:44px;background-color:#FFFFFF;border:1px solid {CLAY};border-radius:10px;">{logo}</td>'
        else:
            tile = f'<td width="44" height="44" align="center" valign="middle" bgcolor="{PLUM}" style="width:44px;height:44px;background-color:{PLUM};border-radius:10px;font-size:20px;line-height:44px;font-weight:700;color:{PAPER};">{e(j["company"][:1].upper())}</td>'
        logo_cell = f'<td valign="top" width="58" style="width:58px;padding-top:2px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{tile}</tr></table></td>'
        inner = (f'{T}><tr>{logo_cell}<td valign="top">'
                 f'<div style="font-size:13px;line-height:18px;font-weight:700;color:{WINE};">{k+1:02d}&nbsp;&nbsp;{e(j["company"])}</div>'
                 f'<a href="{e(j["url"])}" target="_blank" style="display:block;padding-top:4px;font-size:21px;line-height:27px;font-weight:700;color:{INK};text-decoration:none;">{e(j["title"])}</a>'
                 f'<div style="padding-top:10px;">{chips}</div>'
                 f'<div style="font-size:15px;line-height:23px;color:#4A3540;padding-top:4px;">{e(j["note"])}</div>'
                 f''
                 f'<div class="apm" style="display:none;max-height:0;overflow:hidden;padding-top:12px;">{key(j["url"], "Apply")}</div>'
                 f'</td><td class="apc" valign="top" align="right" width="96" style="padding-left:14px;padding-top:2px;">{key(j["url"], "Apply")}</td></tr></table>')
        if card:
            r += f'<tr><td style="padding:0 0 12px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAPER}" style="background-color:{PAPER};border-radius:8px;"><tr><td style="padding:18px 18px 16px 18px;">{inner}</td></tr></table></td></tr>'
        else:
            r += f'<tr><td style="border-top:1px solid {CLAY};padding:20px 0 18px 0;">{inner}</td></tr>'
    return r
n1, n2 = len(d['jobs']), len(d.get('bigtech') or [])
big = ''
if n2:
    big = (f'<tr><td bgcolor="{PLUM}" style="background-color:{PLUM};padding:40px 36px 28px 36px;" class="pad">'
           f'{T}><tr><td style="font-size:28px;line-height:32px;font-weight:700;color:{PAPER};"><span style="color:{MAUVE};">&gt;</span>&nbsp; Big tech hiring</td>'
           f'<td align="right" style="font-size:14px;color:#F1E3E9;">{n2} role{'' if n2 == 1 else 's'} · {e(d.get('bigtech_window') or 'last 5 days')}</td></tr></table>'
           f'<div style="height:20px;line-height:20px;font-size:0;">&nbsp;</div>{T}>{rows(d["bigtech"], True)}</table></td></tr>')
opps = d.get('opportunities') or []
opp = ''
if opps:
    items = ''
    for k, o in enumerate(opps):
        chips = chip(o['kind'], TEAL, PAPER) + (chip(o['when']) if o.get('when') else '')
        items += (f'<tr><td style="border-top:1px solid {CLAY};padding:18px 0 16px 0;">{T}><tr><td valign="top">'
                  f'<div style="font-size:13px;line-height:18px;font-weight:700;color:{TEAL};">{e(o["org"])}</div>'
                  f'<a href="{e(o["url"])}" target="_blank" style="display:block;padding-top:4px;font-size:20px;line-height:26px;font-weight:700;color:{INK};text-decoration:none;">{e(o["title"])}</a>'
                  f'<div style="padding-top:10px;">{chips}</div>'
                  f'<div style="font-size:15px;line-height:23px;color:#4A3540;padding-top:4px;">{e(o["note"])}</div>'
                  f'<div style="padding-top:12px;">{key(o["url"], "Take a look")}</div></td></tr></table></td></tr>')
    opp = (f'<tr><td class="pad" style="padding:40px 36px 6px 36px;">{T}><tr><td style="font-size:28px;line-height:32px;font-weight:700;"><span style="color:{TEAL};">&gt;</span>&nbsp; Beyond the job hunt</td>'
           f'<td align="right" style="font-size:14px;color:{MUTED};">{len(opps)} picks</td></tr></table></td></tr>'
           f'<tr><td class="pad" style="padding:12px 36px 26px 36px;">{T}>{items}</table></td></tr>')
done = d.get('applied') or []
app = ''
if done:
    li = ''.join(f'<tr><td style="padding:6px 0;font-size:15px;line-height:22px;color:{INK};"><span style="display:inline-block;width:16px;height:16px;line-height:16px;text-align:center;border-radius:4px;background-color:{WINE};color:{PAPER};font-size:12px;font-weight:700;vertical-align:-2px;margin-right:10px;">&#10003;</span>'
                 f'<b>{e(a["company"])}</b> · {e(a["title"])}<span style="color:{MUTED};font-size:13px;">&nbsp;&nbsp;{e(a.get("date",""))}</span></td></tr>' for a in done)
    app = (f'<tr><td class="pad" style="padding:10px 36px 30px 36px;">{T} bgcolor="{BAND}" style="background-color:{BAND};border-radius:8px;"><tr><td style="padding:18px 20px;">'
           f'<div style="font-size:16px;line-height:22px;font-weight:700;color:{INK};padding-bottom:6px;">Applied so far · {len(done)}</div>{T}>{li}</table></td></tr></table></td></tr>')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light only">
<title>Ctrl+Curious jobs · {e(d["date"])}</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>@media (max-width:620px){{.wrap{{width:100% !important}}.pad{{padding-left:20px !important;padding-right:20px !important}}.big{{font-size:64px !important;line-height:60px !important}}.apc{{display:none !important;width:0 !important}}.sbig{{font-size:24px !important;line-height:31px !important}}.apm{{display:block !important;max-height:none !important;overflow:visible !important}}}}</style></head>
<body style="margin:0;padding:0;background-color:#E9E1D9;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{e(d["preheader"])}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#E9E1D9" background="{BASE}/assets/email/grain_page.jpg" style="background-color:#E9E1D9;background-image:url('{BASE}/assets/email/grain_page.jpg');"><tr><td align="center" style="padding:24px 10px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAPER}" style="width:600px;background-color:{PAPER};font-family:'Source Serif 4',Georgia,serif;color:{INK};">
<tr><td class="pad" bgcolor="{INK}" background="{BASE}/assets/email/grain_dark.jpg" style="background-color:{INK};background-image:url('{BASE}/assets/email/grain_dark.jpg');padding:30px 36px 34px 36px;">
{T}><tr><td valign="middle"><img src="{BASE}/assets/email/logo_dark.png" width="132" alt="Ctrl+Curious" style="display:block;border:0;width:132px;height:auto;"></td>
<td valign="middle" align="right">{chip("Jobs desk · just for you", WINE, PAPER)}</td></tr></table>
<div style="height:34px;line-height:34px;font-size:0;">&nbsp;</div>
{T}><tr><td valign="bottom" width="150" class="big" style="font-size:96px;line-height:84px;font-weight:700;color:{OCHRE};">{n1 + n2:02d}</td>
<td valign="bottom" style="padding-left:10px;padding-bottom:6px;font-size:24px;line-height:30px;font-weight:700;color:{PAPER};">design roles worth a look<div style="font-size:15px;line-height:22px;font-weight:400;color:#D9C3B7;padding-top:6px;">{e(d["date"])}</div></td></tr></table>
</td></tr>
<tr><td><img src="{BASE}/assets/email/seigaiha_strip.jpg" width="600" height="16" alt="" style="display:block;border:0;width:100%;height:16px;"></td></tr>
<tr><td class="pad" style="padding:40px 36px 6px 36px;">{T}><tr><td style="font-size:28px;line-height:32px;font-weight:700;"><span style="color:{WINE};">&gt;</span>&nbsp; New design roles</td><td align="right" style="font-size:14px;color:{MUTED};">{n1} role{"" if n1 == 1 else "s"}</td></tr></table></td></tr>
<tr><td style="height:14px;line-height:14px;font-size:0;">&nbsp;</td></tr>
<tr><td class="pad" style="padding:0 36px 34px 36px;">{T}>{rows(d["jobs"], False)}</table></td></tr>
{big}
{opp}
<tr><td><img src="https://ctrl-curious.vercel.app/assets/email/seigaiha_strip.jpg" width="600" height="16" alt="" style="display:block;border:0;width:100%;height:16px;"></td></tr>
<tr><td class="pad" bgcolor="#2E1F25" background="https://ctrl-curious.vercel.app/assets/email/grain_dark.jpg" style="background-color:#2E1F25;background-image:url('https://ctrl-curious.vercel.app/assets/email/grain_dark.jpg');padding:40px 36px 36px 36px;">
<div style="font-size:15px;line-height:20px;font-weight:700;color:#C8902F;">&gt;&nbsp; Signing off</div>
<div class="sbig" style="padding-top:14px;font-size:30px;line-height:38px;font-weight:700;color:#F4EEE8;">Good work finds good people. Keep putting yours out there.</div>
<div style="padding-top:12px;font-size:16px;line-height:24px;color:#D9C3B7;">See you tomorrow with a fresh list.</div>
<div style="padding-top:22px;"><a href="https://docs.google.com/spreadsheets/d/19eTo6n1v2sfQNHmysYS4W20qSDQo5u_qj-IXorNSnuk/edit" target="_blank" style="display:inline-block;padding:8px 13px;background-color:#C8902F;border:1.5px solid #C8902F;border-bottom:3px solid #8C6420;border-radius:6px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;line-height:16px;font-weight:700;color:#2E1F25;text-decoration:none;white-space:nowrap;">Open your jobs tracker &#8250;</a></div>
<div style="height:28px;line-height:28px;font-size:0;">&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #5A4650;"><tr>
<td valign="middle" style="padding-top:20px;"><img src="https://ctrl-curious.vercel.app/assets/email/logo_dark.png" width="104" alt="Ctrl+Curious" style="display:block;border:0;width:104px;height:auto;"></td>
<td valign="middle" align="right" style="padding-top:20px;"><span style="display:inline-block;padding:6px 11px;background-color:#3A2A31;border:1.5px solid #C8902F;border-bottom-width:3px;border-radius:6px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;line-height:14px;font-weight:700;color:#F4EEE8;white-space:nowrap;">Next list · 9:00</span></td>
</tr></table>
</td></tr>
</table></td></tr></table></body></html>'''
txt = [f"Ctrl+Curious jobs · {d['date']}", '']
for label, jobs in (('New design roles', d['jobs']), ('Big tech hiring', d.get('bigtech') or [])):
    if not jobs: continue
    txt += [label, '']
    for k, j in enumerate(jobs):
        meta = ' · '.join(x for x in [j['location'], j.get('mode'), j['posted']] if x)
        txt += [f"{k+1:02d}. {j['company']} · {j['title']}", f"    {meta}", f"    {j['note']}", f"    {j['url']}", '']
if opps:
    txt += ['Beyond the job hunt', '']
    for o in opps:
        txt += [f"- {o['org']} · {o['title']} ({o['kind']}{', ' + o['when'] if o.get('when') else ''})", f"    {o['note']}", f"    {o['url']}", '']
if False:
    txt += [f'Applied so far ({len(done)})'] + [f"  [x] {a['company']} · {a['title']} {a.get('date','')}" for a in done] + ['']
txt += ["Good work finds good people. Keep putting yours out there.", "See you tomorrow with a fresh list.", "", "Your jobs tracker: https://docs.google.com/spreadsheets/d/19eTo6n1v2sfQNHmysYS4W20qSDQo5u_qj-IXorNSnuk/edit"]
open(out, 'w').write(page); open(out.rsplit('.', 1)[0] + '.txt', 'w').write('\n'.join(txt))
print('ok', n1, '+', n2, 'jobs')

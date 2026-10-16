"""Practical sections for the Ctrl+Curious email, version 2 (designed set).

Every section shares the same skeleton so the email reads as one system:
  - the usual '> Heading' in 30px bold with a wine chevron,
  - no subtitle under the heading (standing rule: no section subtitles),
  - a 24px bold title that links to the source,
  - one shared 'Our take' note and one shared 'Go deeper' link row.
What changes from section to section is the body, so each has its own recognisable shape:
  skill     big mauve numerals down the side, like the Read list on Wednesdays
  prompt    a dark prompt card with a tool tab, then 'Use it for / Not for'
  tool      keycap-numbered moves, a nod to the Ctrl in Ctrl+Curious
  steal     a file card with a plum file-name tab and a dashed edge
  brief     a one-line definition with an ochre rule, then three numbered sightings
  people    a monogram badge and 'habits worth copying'
  decision  two option cards with filled headers, then a 'rule of thumb' bar
All of it is table-based, inline-styled HTML that holds up in Gmail, Apple Mail and Outlook.
"""
import html
from urllib.parse import quote

SITE = 'https://ctrl-curious.vercel.app'
INK, PAPER, BAND, CLAY, MAUVE, PLUM, WINE, OCHRE, TEAL, MUTED = (
    '#2E1F25', '#F4EEE8', '#EDE4DD', '#D9C3B7', '#C9A7B5', '#7E4B6B', '#8A2E3B', '#C8902F', '#24585C', '#5E4B53')
MONO = "Menlo,Consolas,'Courier New',monospace"

e = lambda t: html.escape(str(t), quote=False)
TABLE = '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'


def a(url, text, style):
    return f'<a href="{html.escape(url)}" target="_blank" style="{style}">{e(text)}</a>'


def heading(title, meta=None, dark=False):  # meta kept for compatibility; no subtitles
    col, mark, mcol = (PAPER, MAUVE, MAUVE) if dark else (INK, WINE, MUTED)
    return (f'<div style="font-size:30px;line-height:33px;font-weight:700;color:{col};"><span style="color:{mark};">&gt;</span>&nbsp; {e(title)}</div>')


def title(l, dark=False):
    col = PAPER if dark else INK
    return a(l['url'], l['title'], f'display:block;padding-top:18px;font-size:24px;line-height:31px;font-weight:700;color:{col};text-decoration:none;')


def intro(l, dark=False):
    col = '#E9DFE3' if dark else '#4A3540'
    return f'<div style="font-size:17px;line-height:27px;color:{col};padding-top:8px;">{e(l["intro"])}</div>'


def take(l):
    if not l.get('take'):
        return ''
    return (f'{TABLE} style="margin-top:22px;"><tr><td width="4" bgcolor="{WINE}" style="background-color:{WINE};font-size:0;line-height:0;">&nbsp;</td>'
            f'<td bgcolor="{BAND}" style="background-color:{BAND};padding:12px 16px;font-size:15px;line-height:23px;color:{INK};"><b style="color:{WINE};">Our take</b>&nbsp; {e(l["take"])}</td></tr></table>')


def deeper(l, dark=False):
    links = l.get('links') or []
    if not links:
        return ''
    lc, sc = (PAPER, MAUVE) if dark else (INK, MUTED)
    rows = ''.join(
        f'<div style="padding-top:6px;"><span style="color:{WINE if not dark else MAUVE};">&rarr;</span>&nbsp; '
        + a(x['url'], x['title'], f'color:{lc};text-decoration:underline;text-decoration-color:{WINE if not dark else MAUVE};text-underline-offset:3px;')
        + (f' <span style="color:{sc};">· {e(x["source"])}</span>' if x.get('source') else '') + '</div>' for x in links)
    return f'<div style="font-size:15px;line-height:23px;padding-top:20px;"><div style="font-size:13px;line-height:18px;color:{sc};">Go deeper</div>{rows}</div>'


def rule():
    return (f'<tr><td class="pad" style="padding:0 36px;">{TABLE}><tr><td style="border-top:2px solid {INK};font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>\n')


def paper_row(inner):
    return f'<tr><td class="pad" style="padding:48px 36px 52px 36px;">{inner}</td></tr>\n'


def band_row(inner):
    strip = f'<tr><td bgcolor="{BAND}" style="background-color:{BAND};"><img src="{SITE}/assets/email/seigaiha_strip.jpg" width="600" height="10" alt="" style="display:block;border:0;width:100%;max-width:600px;height:10px;"></td></tr>\n'
    return strip + (f'<tr><td class="pad" bgcolor="{BAND}" background="{SITE}/assets/email/grain_band.jpg" style="background-color:{BAND};'
                    f'background-image:url(\'{SITE}/assets/email/grain_band.jpg\');background-repeat:repeat;padding:42px 36px 50px 36px;">{inner}</td></tr>\n')


# ---------- Skill of the week ----------
def skill(l):
    steps = l.get('steps') or []
    rows = ''.join(
        f'<tr><td valign="top" width="64" style="border-top:1px solid {CLAY};padding:16px 0;font-size:40px;line-height:40px;font-weight:700;color:{MAUVE};">{k+1:02d}</td>'
        f'<td valign="top" style="border-top:1px solid {CLAY};padding:18px 0 16px 0;font-size:17px;line-height:26px;color:{INK};">{e(s)}</td></tr>'
        for k, s in enumerate(steps))
    body = f'{TABLE} style="margin-top:22px;border-bottom:1px solid {CLAY};">{rows}</table>'
    meta = f'{len(steps)} steps to try this week'
    return 'paper', heading('Skill of the week', meta) + title(l) + intro(l) + body + take(l) + deeper(l)


# ---------- Prompt of the week ----------
def prompt(l):
    tool = l.get('tool') or 'Any AI assistant'
    card = (f'{TABLE} style="margin-top:22px;"><tr><td bgcolor="{PLUM}" style="background-color:{PLUM};padding:9px 16px;font-size:13px;line-height:18px;color:{PAPER};">'
            f'<b>Prompt</b>&nbsp; · &nbsp;{e(tool)}</td></tr>'
            f'<tr><td bgcolor="{INK}" background="{SITE}/assets/email/grain_dark.jpg" style="background-color:{INK};background-image:url(\'{SITE}/assets/email/grain_dark.jpg\');padding:18px 18px 20px 18px;'
            f'font-family:{MONO};font-size:14px;line-height:22px;color:{PAPER};white-space:pre-wrap;word-break:break-word;"><span style="color:{OCHRE};">&gt;</span> {e(l["code"])}</td></tr></table>')
    note = f'<div style="font-size:14px;line-height:21px;color:{MUTED};padding-top:8px;">{e(l["code_note"])}</div>' if l.get('code_note') else ''
    cols = ''
    if l.get('columns'):
        cells = []
        for c in l['columns'][:2]:
            items = ''.join(f'<div style="font-size:15px;line-height:23px;color:{INK};padding-top:6px;">&#8212;&nbsp; {e(x)}</div>' for x in c['items'])
            cells.append(f'<td class="wk" width="50%" valign="top"><div style="font-size:14px;line-height:20px;font-weight:700;color:{WINE};">{e(c["label"])}</div>{items}</td>')
        cols = f'{TABLE} style="margin-top:20px;"><tr>' + '<td class="wks" width="20" style="font-size:0;line-height:0;">&nbsp;</td>'.join(cells) + '</tr></table>'
    return 'paper', heading('Prompt of the week', f'Ready to copy · for {tool}') + title(l) + intro(l) + card + note + cols + take(l) + deeper(l)


# ---------- Tool to master ----------
def tool(l):
    steps = l.get('steps') or []
    key = lambda n: (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="30" height="30" align="center" valign="middle" bgcolor="{PAPER}" '
                     f'style="width:30px;height:30px;background-color:{PAPER};border:1.5px solid {INK};border-bottom-width:3px;border-radius:5px;font-family:{MONO};font-size:14px;line-height:30px;font-weight:700;color:{INK};">{n}</td></tr></table>')
    rows = ''.join(f'<tr><td valign="top" width="48" style="padding:0 0 16px 0;">{key(k+1)}</td>'
                   f'<td valign="top" style="padding:3px 0 16px 0;font-size:17px;line-height:26px;color:{INK};">{e(s)}</td></tr>' for k, s in enumerate(steps))
    body = f'{TABLE} style="margin-top:24px;">{rows}</table>'
    meta = f'{len(steps)} moves that save real time'
    return 'band', heading('Tool to master', meta) + title(l) + intro(l) + body + take(l) + deeper(l)


# ---------- Steal this ----------
def steal(l):
    fname = l.get('file') or 'starter'
    tab = (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:22px;"><tr>'
           f'<td bgcolor="{PLUM}" style="background-color:{PLUM};padding:7px 14px;font-family:{MONO};font-size:13px;line-height:18px;color:{PAPER};border-radius:4px 4px 0 0;">{e(fname)}</td></tr></table>')
    box = (f'{TABLE}><tr><td bgcolor="{PAPER}" style="background-color:{PAPER};border:1.5px dashed {PLUM};padding:18px 18px 20px 18px;'
           f'font-family:{MONO};font-size:13px;line-height:21px;color:{INK};white-space:pre-wrap;word-break:break-word;">{e(l["code"])}</td></tr></table>')
    note = f'<div style="font-size:14px;line-height:21px;color:{MUTED};padding-top:10px;">{e(l["code_note"])}</div>' if l.get('code_note') else ''
    get = a(l['url'], 'Get the original', f'display:inline-block;margin-top:16px;padding:10px 16px;background-color:{PLUM};color:{PAPER};font-size:15px;font-weight:600;text-decoration:none;')
    return 'paper', heading('Steal this', l.get('meta') or 'Free · ready to use today') + title(l) + intro(l) + tab + box + note + get + take(l) + deeper(l)


# ---------- 10-minute brief ----------
def brief(l):
    define = ''
    if l.get('define'):
        define = (f'{TABLE} style="margin-top:22px;"><tr><td width="4" bgcolor="{OCHRE}" style="background-color:{OCHRE};font-size:0;line-height:0;">&nbsp;</td>'
                  f'<td style="padding:4px 0 4px 18px;font-size:21px;line-height:31px;font-weight:600;color:{INK};">{e(l["define"])}</td></tr></table>')
    ex = l.get('examples') or []
    cells = []
    for k, x in enumerate(ex[:3]):
        cells.append(f'<td class="wk" width="33%" valign="top" bgcolor="{PAPER}" style="background-color:{PAPER};padding:16px;">'
                     f'<div style="font-size:28px;line-height:28px;font-weight:700;color:{MAUVE};">{k+1}</div>'
                     + a(x['url'], x['name'], f'display:block;padding-top:10px;font-size:16px;line-height:22px;font-weight:700;color:{INK};text-decoration:none;')
                     + f'<div style="font-size:14px;line-height:21px;color:{MUTED};padding-top:6px;">{e(x["text"])}</div></td>')
    grid = ''
    if cells:
        grid = (f'<div style="font-size:14px;line-height:20px;font-weight:700;color:{WINE};padding-top:26px;">Where it showed up this week</div>'
                f'{TABLE} style="margin-top:10px;"><tr>' + '<td class="wks" width="10" style="font-size:0;line-height:0;">&nbsp;</td>'.join(cells) + '</tr></table>')
    why = ''
    if l.get('why'):
        why = (f'<div style="font-size:14px;line-height:20px;font-weight:700;color:{WINE};padding-top:24px;">Why it matters to you</div>'
               f'<div style="font-size:17px;line-height:27px;color:{INK};padding-top:6px;">{e(l["why"])}</div>')
    return 'band', heading('10-minute brief', l.get('meta') or 'About a 10-minute read, explained plainly') + title(l) + intro(l) + define + grid + why + take(l) + deeper(l)


# ---------- How they work ----------
def people(l):
    p = l.get('person') or {}
    initials = p.get('initials') or ''.join(w[0] for w in p.get('name', '').split()[:2])
    badge = (f'{TABLE} style="margin-top:22px;"><tr>'
             f'<td width="64" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="56" height="56" align="center" valign="middle" bgcolor="{PLUM}" '
             f'style="width:56px;height:56px;background-color:{PLUM};border-radius:28px;font-size:20px;line-height:56px;font-weight:700;color:{PAPER};">{e(initials)}</td></tr></table></td>'
             f'<td valign="middle" style="padding-left:14px;">' + a(l['url'], p.get('name', l['title']), f'display:block;font-size:22px;line-height:28px;font-weight:700;color:{INK};text-decoration:none;')
             + f'<div style="font-size:15px;line-height:22px;color:{MUTED};padding-top:2px;">{e(p.get("role", ""))}</div></td></tr></table>')
    steps = l.get('steps') or []
    rows = ''.join(f'<tr><td valign="top" width="26" style="padding:17px 0 0 0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="10" height="10" bgcolor="{OCHRE}" style="width:10px;height:10px;background-color:{OCHRE};border-radius:5px;font-size:0;line-height:0;">&nbsp;</td></tr></table></td>'
                   f'<td valign="top" style="padding:10px 0;font-size:17px;line-height:26px;color:{INK};">{e(s)}</td></tr>' for s in steps)
    habits = (f'<div style="font-size:14px;line-height:20px;font-weight:700;color:{WINE};padding-top:24px;">Habits worth copying</div>'
              f'{TABLE} style="margin-top:4px;">{rows}</table>') if rows else ''
    src = l.get('source_line') or ''
    return 'paper', heading('How they work', src or 'Inside a respected designer\'s workflow') + badge + intro(l) + habits + take(l) + deeper(l)


# ---------- Decision toolkit ----------
def decision(l):
    cols = l.get('columns') or []
    heads = [INK, PLUM]
    cells = []
    for k, c in enumerate(cols[:2]):
        items = ''.join(f'<div style="font-size:15px;line-height:23px;color:{INK};padding-top:8px;">&#8212;&nbsp; {e(x)}</div>' for x in c['items'])
        cells.append(f'<td class="wk" width="50%" valign="top" bgcolor="{PAPER}" style="background-color:{PAPER};border:1px solid {CLAY};">'
                     f'<div style="background-color:{heads[k]};padding:12px 16px;font-size:16px;line-height:22px;font-weight:700;color:{PAPER};">{e(c["label"])}</div>'
                     f'<div style="padding:6px 16px 16px 16px;">{items}</div></td>')
    grid = f'{TABLE} style="margin-top:22px;"><tr>' + '<td class="wks" width="12" style="font-size:0;line-height:0;">&nbsp;</td>'.join(cells) + '</tr></table>'
    ex = ''
    for x in (l.get('examples') or [])[:1]:
        ex = (f'<div style="font-size:14px;line-height:20px;font-weight:700;color:{WINE};padding-top:24px;">Seen in the wild</div>'
              + a(x['url'], x['name'], f'display:block;padding-top:6px;font-size:17px;line-height:24px;font-weight:700;color:{INK};text-decoration:none;')
              + f'<div style="font-size:15px;line-height:23px;color:{MUTED};padding-top:2px;">{e(x["text"])}</div>')
    rule_of_thumb = ''
    if l.get('rule'):
        rule_of_thumb = (f'{TABLE} style="margin-top:22px;"><tr><td bgcolor="{WINE}" style="background-color:{WINE};padding:14px 18px;font-size:17px;line-height:25px;color:{PAPER};">'
                         f'<b>Rule of thumb</b>&nbsp; {e(l["rule"])}</td></tr></table>')
    return 'paper', heading('Decision toolkit', l.get('meta') or 'A framework for a call you make often') + title(l) + intro(l) + grid + ex + rule_of_thumb + take(l) + deeper(l)


RENDER = {'skill': skill, 'prompt': prompt, 'tool': tool, 'steal': steal, 'brief': brief, 'people': people, 'decision': decision}


def render(learns, prev_surface='paper'):
    """Render a list of practical sections. Paper sections are separated by the usual 2px rule;
    band sections bring their own wave strip. Returns (html, surface_of_last_section)."""
    out, last = '', prev_surface
    for l in learns:
        fn = RENDER.get(l.get('kind'))
        if not fn:
            continue
        surface, inner = fn(l)
        if surface == 'band':
            out += band_row(inner)
        else:
            if last == 'paper':
                out += rule()
            out += paper_row(inner)
        last = surface
    return out, last

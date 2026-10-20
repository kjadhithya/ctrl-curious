"""Website-only hero art for issues 001, 003 and 004, redrawn in each weekday's new style and tied to the issue's story."""
import sys, os
os.environ['VIBES_SET'] = 'site_issues'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vibes'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vhelp import *
import lib
OUT = '/home/claude/ctrl-curious/assets/blog/issues/'
os.makedirs(OUT, exist_ok=True)
MIX = lambda a, b, t: tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))

def dotted(top, bottom=None, dot=None):
    im = canvas(top, bottom or top, 1); d = ImageDraw.Draw(im)
    for x in range(14, 1200, 28):
        for y in range(14, 600, 28):
            d.ellipse([(x-1.6)*S, (y-1.6)*S, (x+1.6)*S, (y+1.6)*S], fill=dot or c['clay'])
    return im

def sticky(im, x, y, s, col, lc, ang=0):
    st = Image.new('RGBA', (int(s*S*1.6), int(s*S*1.6)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); o = s*S*0.3
    sd.rectangle([o + 6*S, o + 8*S, o + s*S + 6*S, o + s*S + 8*S], fill=c['clay'] + (255,))
    sd.polygon([(o, o), (o + s*S, o), (o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S), (o, o + s*S)], fill=col + (255,))
    sd.polygon([(o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S*0.8), (o + s*S*0.8, o + s*S)], fill=tuple(int(v*0.8) for v in col) + (255,))
    for k in range(3):
        yy = o + s*S*(0.26 + k*0.17); sd.line([(o + s*S*0.14, yy), (o + s*S*(0.8 - k*0.17), yy)], fill=lc + (255,), width=max(3, int(s*S*0.035)))
    st = st.rotate(ang, resample=Image.BICUBIC); im.paste(st, (int(x*S - st.width/2), int(y*S - st.height/2)), st)

def cursor(im, x, y, col, name, sc=1.2, tcol=None):
    cur = [(0, 0), (0, 52), (13, 40), (22, 61), (32, 57), (23, 37), (40, 37)]
    poly(im, [(x + p*sc, y + q*sc) for p, q in cur], col)
    w_ = 18 + len(name) * 12
    rr(im, x + 34*sc, y + 46*sc, x + 34*sc + w_*sc, y + 80*sc, 9*sc, col)
    text(im, x + 44*sc, y + 49*sc, name, int(21*sc), tcol or c['paper'], 700)

# 001 · Thursday (FigJam): Specs, a design rulebook agents can read — an open rulebook of checklist rules,
# stickies pinned to its pages, an agent's cursor reading along
im = dotted(c['mist'], c['paper'], c['skyb'])
disc(im, 1070, 100, 48, c['wine'])
cx = 600
rr(im, cx - 336, 128, cx + 336, 520, 22, c['ink'])                               # cover
poly(im, [(cx - 316, 112), (cx - 8, 132), (cx - 8, 500), (cx - 316, 484)], c['paper'])   # left page
poly(im, [(cx + 316, 112), (cx + 8, 132), (cx + 8, 500), (cx + 316, 484)], c['paper'])   # right page
rr(im, cx - 8, 132, cx + 8, 500, 0, c['clay'])                                   # spine
for k in range(5):                                                               # rules: a tick box and a line each
    y = 176 + k * 60
    rr(im, cx - 286, y, cx - 258, y + 28, 6, c['teal'] if k != 3 else c['paper'], c['teal'], 3)
    if k != 3: line(im, [(cx - 280, y + 14), (cx - 273, y + 22), (cx - 262, y + 6)], c['paper'], 4)
    rr(im, cx - 240, y + 9, cx - 240 + [190, 150, 210, 170, 120][k], y + 19, 5, c['indigo'] if k != 3 else c['mauve'])
for k in range(4):                                                               # right page: tokens as swatches
    rr(im, cx + 42 + k * 64, 176, cx + 92 + k * 64, 226, 10, [c['wine'], c['teal'], c['ochre'], c['plum']][k])
for k in range(3):
    rr(im, cx + 42, 260 + k * 34, cx + 42 + [230, 190, 210][k], 272 + k * 34, 6, c['skyb'])
sticky(im, cx + 210, 410, 120, c['ochre'], c['deep'], ang=-6)
sticky(im, cx - 400, 390, 110, c['mauve'], c['plum'], ang=5)
cursor(im, cx - 120, 330, c['plum'], 'agent')
finish(im, OUT + 'issue_001.jpg', seed=71)

# 003 · Monday (Nature + UI): synthetic users agree with humans but flatten their answers —
# a jagged human ridge and a smooth synthetic ridge charted against each other under the sun
im = canvas(c['ochre'], c['paper'], 0.9)
for k in range(1, 5): line(im, [(70, 90 * k + 40), (1130, 90 * k + 40)], MIX(c['ochre'], c['paper'], 0.55), 1.5)
disc(im, 860, 140, 64, c['wine'])
xs = list(range(70, 1131, 106))
hum = [430, 300, 380, 210, 330, 180, 290, 240, 360, 260, 410]
syn = [400, 360, 340, 320, 310, 300, 305, 315, 330, 345, 380]
poly(im, list(zip(xs, hum)) + [(1130, 600), (70, 600)], c['plum'])
poly(im, [(x, y + 80) for x, y in zip(xs, hum)] + [(1130, 600), (70, 600)], c['deep'])
for x, y in zip(xs, hum):
    if y < 260: poly(im, [(x, y), (x + 26, y + 26), (x + 10, y + 32), (x, y + 22), (x - 10, y + 32), (x - 26, y + 26)], c['paper'])
line(im, list(zip(xs, hum)), c['wine'], 5)
for x, y in zip(xs, hum): disc(im, x, y, 9, c['paper']); ring(im, x, y, 9, c['wine'], 3)
syn_pts = list(map(tuple, np.vstack([bez((xs[i], syn[i]), (xs[i] + 35, syn[i]), (xs[i + 1] - 35, syn[i + 1]), (xs[i + 1], syn[i + 1]), 12) for i in range(len(xs) - 1)])))
line(im, syn_pts, c['skyb'], 6)
for x, y in zip(xs, syn): disc(im, x, y, 8, c['indigo']); ring(im, x, y, 8, c['skyb'], 3)
for (lx, ly, col, w_) in [(70, 50, c['wine'], 58), (70, 86, c['skyb'], 44)]:
    disc(im, lx + 10, ly + 8, 7, col); rr(im, lx + 26, ly + 3, lx + 26 + w_ * 2, ly + 13, 5, c['ink'])
sea(im, 540, c['teal'], c['foamb'], gap=16, amp=3)
finish(im, OUT + 'issue_003.jpg', seed=73)

# 004 · Tuesday (Tech): a touchscreen MacBook Pro — a laptop whose screen ripples where a fingertip taps,
# and a download that shows time left instead of a percentage
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 40, 260, c['mist'], seed=74)
disc(im, 1060, 100, 46, c['clay'])
rr(im, 300, 90, 900, 440, 22, c['ink'])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([322*S, 112*S, 878*S, 418*S], radius=8*S, fill=255)
scr = canvas(c['skyb'], c['mist'], 1); sea(scr, 330, c['teal'], c['foamb'], gap=14, amp=3, freq=24)
tx, ty = 520, 240
for k, r in enumerate([30, 58, 86, 114]):
    ring(scr, tx, ty, r, [c['paper'], c['foamb'], c['paper'], c['foamb']][k], 4 - k * 0.6)
disc(scr, tx, ty, 16, c['wine'])
rr(scr, 600, 150, 850, 214, 14, c['paper'])                                     # the download card
rr(scr, 620, 192, 830, 202, 5, c['clay']); rr(scr, 620, 192, 752, 202, 5, c['teal'])
rr(scr, 620, 164, 736, 178, 7, c['clay'])                                     # wireframe text block in place of a label
im.paste(scr, (0, 0), m)
poly(im, [(230, 440), (970, 440), (1030, 482), (170, 482)], c['prussian'])
rr(im, 520, 440, 680, 452, 5, c['indigo'])
for k in range(3): line(im, [(x, 454 + k * 8 + math.sin(x / 14 + k) * 1.2) for x in range(240 - k*16, 960 + k*16, 4)], c['skyb'], 1.6)
poly(im, [(170, 482), (1030, 482), (1024, 492), (176, 492)], c['ink'])
sea(im, 520, c['navy'], c['prussian'], gap=14, amp=3)
finish(im, OUT + 'issue_004.jpg', amt=15, seed=74)
print('done')

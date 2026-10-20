"""Vibes exploration, FigJam shapes set: 8 illustrations built from stickies, connectors, stamps and shapes."""
import sys, os
os.environ['VIBES_SET'] = 'vibes_figjam'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vhelp import *

def board(top, bottom=None, dot=None):
    im = canvas(top, bottom or top, 1); d = ImageDraw.Draw(im)
    for x in range(14, 1200, 28):
        for y in range(14, 600, 28):
            d.ellipse([(x-1.6)*S, (y-1.6)*S, (x+1.6)*S, (y+1.6)*S], fill=dot or c['clay'])
    return im

def sticky(im, x, y, s, col, ang=0, lines=None, shadow=None, nlines=3):
    st = Image.new('RGBA', (int(s*S*1.6), int(s*S*1.6)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    o = s*S*0.3
    sd.rectangle([o + 6*S, o + 8*S, o + s*S + 6*S, o + s*S + 8*S], fill=(shadow or c['clay']) + (255,))
    sd.polygon([(o, o), (o + s*S, o), (o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S), (o, o + s*S)], fill=col + (255,))
    sd.polygon([(o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S*0.8), (o + s*S*0.8, o + s*S)], fill=tuple(int(v*0.8) for v in col) + (255,))
    if lines:
        for k in range(nlines):
            yy = o + s*S*(0.26 + k*0.17); sd.line([(o + s*S*0.14, yy), (o + s*S*(0.8 - k*0.17), yy)], fill=lines + (255,), width=max(3, int(s*S*0.03)))
    st = st.rotate(ang, resample=Image.BICUBIC)
    im.paste(st, (int(x*S - st.width/2), int(y*S - st.height/2)), st)

def arrow(im, pts, col, w=4, head=18):
    line(im, [tuple(p) for p in pts], col, w)
    tip = np.array(pts[-1]); dx, dy = tip - np.array(pts[-5]); a = math.atan2(dy, dx)
    poly(im, [(tip[0] + head*math.cos(a), tip[1] + head*math.sin(a)), (tip[0] + head*0.85*math.cos(a + 2.4), tip[1] + head*0.85*math.sin(a + 2.4)), (tip[0] + head*0.85*math.cos(a - 2.4), tip[1] + head*0.85*math.sin(a - 2.4))], col)

def cursor(im, x, y, col, name, sc=1.0, tcol=None):
    cur = [(0, 0), (0, 52), (13, 40), (22, 61), (32, 57), (23, 37), (40, 37)]
    poly(im, [(x + p*sc, y + q*sc) for p, q in cur], col)
    w_ = 18 + len(name) * 12
    rr(im, x + 34*sc, y + 46*sc, x + 34*sc + w_*sc, y + 80*sc, 9*sc, col)
    text(im, x + 44*sc, y + 49*sc, name, int(21*sc), tcol or c['paper'], 700)

def star(im, cx, cy, r, col, n=5, inner=0.45):
    pts = [(cx + (r if k % 2 == 0 else r*inner) * math.cos(-math.pi/2 + k*math.pi/n), cy + (r if k % 2 == 0 else r*inner) * math.sin(-math.pi/2 + k*math.pi/n)) for k in range(2*n)]
    poly(im, pts, col)

# 1 Affinity map: three clusters of stickies, each grouped under a circle label
im = board(c['paper'])
groups = [(220, c['ochre'], c['deep']), (600, c['skyb'], c['indigo']), (980, c['mauve'], c['plum'])]
rng = np.random.default_rng(31)
for gx, col, lc in groups:
    disc(im, gx, 92, 30, lc)
    for k, (dx, dy) in enumerate([(-62, 205), (62, 210), (-58, 335), (64, 330), (0, 462)]):
        sticky(im, gx + dx, dy, 104, col, ang=float(rng.normal(0, 3)), lines=lc)
finish(im, OUT + 'figjam_01_affinity.jpg', seed=31)

# 2 Flowchart: circle, diamond and rounded rectangle joined by swelling connectors, ending in the sun
im = board(c['mist'], c['paper'], c['skyb'])
rr(im, 80, 230, 300, 360, 26, c['indigo']); text(im, 132, 274, 'idea', 36, c['paper'], 700)
poly(im, [(520, 175), (640, 295), (520, 415), (400, 295)], c['teal']); text(im, 487, 274, 'test', 32, c['paper'], 700)
rr(im, 720, 230, 920, 360, 65, c['plum']); text(im, 768, 274, 'ship', 36, c['paper'], 700)
disc(im, 1080, 295, 70, c['wine'])
arrow(im, bez((300, 295), (340, 250), (360, 340), (392, 295), 40), c['ink'], 4)
arrow(im, bez((640, 295), (670, 245), (690, 345), (712, 295), 40), c['ink'], 4)
arrow(im, bez((920, 295), (950, 245), (975, 345), (1002, 295), 40), c['ink'], 4)
arrow(im, bez((520, 415), (560, 540), (300, 560), (190, 368), 80), c['plum'], 3, 14)
finish(im, OUT + 'figjam_02_flowchart.jpg', seed=32)

# 3 Stamps: a sticky covered in reaction stamps, a big +1 landing like a sun
im = board(c['clay'], c['paper'])
sticky(im, 470, 320, 330, c['ochre'], ang=-3, lines=c['deep'], shadow=c['mauve'])
for (x, y, r, col, kind) in [(780, 170, 74, c['wine'], 'plus'), (700, 400, 46, c['teal'], 'check'), (860, 330, 40, c['plum'], 'star'), (300, 470, 36, c['indigo'], 'heart')]:
    disc(im, x + 4, y + 6, r, c['mauve']); disc(im, x, y, r, col); ring(im, x, y, r - 7, c['paper'], 2)
    if kind == 'plus': text(im, x - r*0.52, y - r*0.6, '+1', int(r*0.95), c['paper'], 800)
    if kind == 'check': line(im, [(x - r*0.4, y), (x - r*0.1, y + r*0.32), (x + r*0.45, y - r*0.35)], c['paper'], 6)
    if kind == 'star': star(im, x, y, r*0.55, c['paper'])
    if kind == 'heart':
        disc(im, x - r*0.2, y - r*0.1, r*0.24, c['paper']); disc(im, x + r*0.2, y - r*0.1, r*0.24, c['paper'])
        poly(im, [(x - r*0.43, y - r*0.02), (x + r*0.43, y - r*0.02), (x, y + r*0.45)], c['paper'])
for k, r in enumerate(range(100, 260, 34)):
    ImageDraw.Draw(im).arc([(780-r)*S, (170-r)*S, (780+r)*S, (170+r)*S], 290, 360, fill=c['wine'], width=2*S)
finish(im, OUT + 'figjam_03_stamps.jpg', seed=33)

# 4 Section: a labelled section frame holding a tidy grid of shapes, one shape being dragged out
im = board(c['paper'])
rr(im, 120, 110, 820, 520, 18, c['mist'], c['skyb'], 2)
rr(im, 120, 72, 290, 108, 10, c['skyb']); text(im, 136, 76, 'sunday', 22, c['indigo'], 700)
shapes = [('circle', c['wine']), ('tri', c['plum']), ('rect', c['teal']), ('diamond', c['ochre']), ('pill', c['indigo']), ('circle', c['moss'])]
for k, (sh, col) in enumerate(shapes):
    x = 230 + (k % 3) * 230; y = 210 + (k // 3) * 200
    if sh == 'circle': disc(im, x, y, 62, col)
    if sh == 'tri': poly(im, [(x, y - 64), (x + 70, y + 56), (x - 70, y + 56)], col)
    if sh == 'rect': rr(im, x - 62, y - 62, x + 62, y + 62, 12, col)
    if sh == 'diamond': poly(im, [(x, y - 70), (x + 70, y), (x, y + 70), (x - 70, y)], col)
    if sh == 'pill': rr(im, x - 80, y - 36, x + 80, y + 36, 36, col)
star(im, 1000, 300, 90, c['ochre'])
line(im, [(870, 300), (895, 300)], c['skyb'], 2); line(im, [(845, 300), (858, 300)], c['skyb'], 2)
for (a, b) in [(905, 205), (1095, 205), (1095, 395), (905, 395)]: rr(im, a - 7, b - 7, a + 7, b + 7, 2, c['paper'], c['skyb'], 2)
line(im, [(905, 205), (1095, 205), (1095, 395), (905, 395), (905, 205)], c['skyb'], 2)
cursor(im, 1040, 360, c['plum'], 'mei')
finish(im, OUT + 'figjam_04_section.jpg', seed=34)

# 5 Marker: a thick marker stroke drawing a swell across the board, the marker still in hand
im = board(c['paper'])
sticky(im, 190, 150, 150, c['skyb'], ang=-4, lines=c['indigo'])
sticky(im, 840, 470, 140, c['mauve'], ang=3, lines=c['plum'])
path = bez((80, 420), (300, 120), (520, 560), (760, 260), 140)
path2 = bez((760, 260), (860, 150), (960, 300), (1010, 250), 60)
full = np.vstack([path, path2])
line(im, [tuple(p) for p in full], c['wine'], 18)
line(im, [(p[0], p[1] + 34) for p in full[:150]], c['ochre'], 8)
mx, my = 1010, 250
mk = Image.new('RGBA', (360*S, 360*S), (0, 0, 0, 0)); md = ImageDraw.Draw(mk)
md.rounded_rectangle([150*S, 40*S, 210*S, 250*S], radius=14*S, fill=c['ink'] + (255,))
md.rectangle([150*S, 200*S, 210*S, 250*S], fill=c['clay'] + (255,))
md.polygon([(155*S, 250*S), (205*S, 250*S), (190*S, 300*S), (170*S, 300*S)], fill=c['clay'] + (255,))
md.polygon([(170*S, 300*S), (190*S, 300*S), (180*S, 320*S)], fill=c['wine'] + (255,))
md.rounded_rectangle([150*S, 40*S, 210*S, 90*S], radius=14*S, fill=c['wine'] + (255,))
mk = mk.rotate(-35, resample=Image.BICUBIC, center=(180*S, 320*S))
im.paste(mk, (int(mx*S - 180*S), int(my*S - 320*S)), mk)
finish(im, OUT + 'figjam_05_marker.jpg', seed=35)

# 6 Multiplayer: four teammates' cursors converging on one circle
im = board(c['indigo'], c['navy'], c['prussian'])
disc(im, 600, 300, 110, c['ochre'])
for k, r in enumerate([150, 190, 230]): ring(im, 600, 300, r, [c['prussian'], c['teal'], c['prussian']][k], 2)
for (x, y, col, n) in [(200, 80, c['wine'], 'ana'), (860, 70, c['skyb'], 'ravi'), (240, 400, c['mauve'], 'mei'), (840, 390, c['moss'], 'you')]:
    cursor(im, x, y, col, n, sc=1.7, tcol=c['ink'] if col in (c['skyb'], c['mauve']) else c['paper'])
finish(im, OUT + 'figjam_06_multiplayer.jpg', amt=15, seed=36)

# 7 Voting: a row of stickies with dot votes, one clearly winning
im = board(c['paper'])
cols = [c['skyb'], c['mauve'], c['ochre'], c['mist'], c['clay']]
votes = [2, 1, 9, 3, 0]
for k, (col, v) in enumerate(zip(cols, votes)):
    x = 150 + k * 225; y = 330
    sticky(im, x, y, 175, col, ang=[-2, 2, 0, -1, 3][k], lines=c['deep'] if k != 2 else c['ink'], nlines=2)
    for j in range(v):
        disc(im, x - 60 + (j % 4) * 38, y + 10 + (j // 4) * 36, 14, c['wine'] if k == 2 else c['plum'])
star(im, 600, 150, 40, c['wine'])
finish(im, OUT + 'figjam_07_voting.jpg', seed=37)

# 8 Balancing act: the basic shapes stacked into a tower under a circle sun
im = board(c['mist'], c['paper'], c['skyb'])
disc(im, 960, 140, 70, c['wine'])
rr(im, 380, 470, 820, 520, 25, c['indigo'])
rr(im, 470, 360, 730, 470, 14, c['teal'])
poly(im, [(600, 230), (690, 360), (510, 360)], c['plum'])
disc(im, 600, 182, 50, c['ochre'])
poly(im, [(600, 70), (640, 110), (600, 150), (560, 110)], c['wine'])
rr(im, 0, 520, 1200, 600, 0, c['clay'])
for k in range(3): line(im, [(x, 545 + k*16 + math.sin(x/40 + k)*3) for x in range(0, 1201, 5)], c['paper'], 2)
finish(im, OUT + 'figjam_08_balance.jpg', seed=38)
print('done')

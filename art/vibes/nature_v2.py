"""Vibes exploration, nature + UI set, v2 with alignment fixes: 8 landscapes built from interface pieces, in the house style."""
import sys, os
os.environ['VIBES_SET'] = 'vibes_nature_v2'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vhelp import *

def check(im, x, y, s, col, on, mark=None):
    rr(im, x - s/2, y - s/2, x + s/2, y + s/2, s*0.22, col)
    if on: line(im, [(x - s*0.25, y), (x - s*0.05, y + s*0.2), (x + s*0.28, y - s*0.22)], mark or c['paper'], max(3, s*0.1))
    else: rr(im, x - s/2 + 4, y - s/2 + 4, x + s/2 - 4, y + s/2 - 4, s*0.18, c['paper'])

# 1 Toggle sunrise: a giant toggle on the horizon, the sun its knob, the sea its track
im = canvas(c['ochre'], c['paper'], 0.9)
rr(im, 250, 270, 950, 470, 100, c['teal'])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([250*S, 270*S, 950*S, 470*S], radius=100*S, fill=255)
tr = Image.new('RGB', (W, H), c['teal']); sea(tr, 260, c['teal'], c['foamb'], gap=16, amp=3, freq=30)
im.paste(tr, (0, 0), m)
disc(im, 850, 370, 82, c['paper']); disc(im, 850, 370, 74, c['wine'])
ridge(im, 520, 10, 120, c['moss'], seed=2, jag=0.3); ridge(im, 555, 8, 80, c['pine'], seed=4, jag=0.3)
finish(im, OUT + 'nature2_01_toggle.jpg', seed=51)

# 2 Tree diagram: a tree whose branches are a node hierarchy, leaves as dots
im = canvas(c['mist'], c['paper'], 1)
disc(im, 1080, 110, 52, c['wine'])
nodes = {0: (600, 470)}
edges = []
lv = [(600, 470)]; k = 1
rng = np.random.default_rng(52)
levels = [[(600, 470)]]
for depth, (n, dy, spread) in enumerate([(2, 110, 300), (4, 90, 160), (8, 70, 80)]):
    nxt = []
    for (px, py) in levels[-1]:
        for j in range(2):
            x = px + (j - 0.5) * spread; y = py - dy
            edges.append(((px, py), (x, y))); nxt.append((x, y))
    levels.append(nxt)
for (a, b) in edges:
    line(im, list(map(tuple, bez(a, (a[0], (a[1] + b[1]) / 2), (b[0], (a[1] + b[1]) / 2), b, 30))), c['deep'], 5)
line(im, [(600, 470), (600, 560)], c['deep'], 12)
for lvl, pts in enumerate(levels):
    for (x, y) in pts:
        disc(im, x, y, [16, 14, 12, 26][lvl], [c['deep'], c['plum'], c['teal'], c['moss']][lvl])
for (x, y) in levels[-1]:
    for j, (dx, dy, r) in enumerate([(-24, -14, 22), (24, -14, 22), (0, -40, 24), (0, -8, 20)]):
        disc(im, x + dx, y + dy, r, [c['moss'], c['pine'], c['teal'], c['moss']][j])
    disc(im, x, y, 10, c['deep'])
rr(im, 0, 560, 1200, 600, 0, c['clay'])
finish(im, OUT + 'nature2_02_tree_diagram.jpg', seed=52)

# 3 Speech cloud: a cloud-shaped chat bubble raining lines onto hills, all on one centre line
im = canvas(c['skyb'], c['mist'], 1)
CX = 600
for (dx, y, r) in [(-110, 190, 78), (-15, 150, 102), (95, 182, 84), (170, 212, 60)]: disc(im, CX + dx - 30, y, r, c['paper'])
rr(im, CX - 215, 190, CX + 215, 275, 42, c['paper'])
poly(im, [(CX - 40, 262), (CX + 10, 262), (CX - 52, 320)], c['paper'])
for k in (-1, 0, 1): disc(im, CX + k * 55, 222, 12, c['indigo'])
for k in range(-5, 6):
    x = CX + k * 30
    line(im, [(x + 7, 300), (x - 7, 360)], c['indigo'], 3)
ridge(im, 410, 26, 140, c['moss'], seed=6, jag=0.3); ridge(im, 470, 20, 100, c['pine'], seed=8, jag=0.3)
sea(im, 540, c['teal'], c['foamb'], gap=16, amp=3)
finish(im, OUT + 'nature2_03_speech_cloud.jpg', seed=53)

# 4 Line chart ridge: mountains drawn as a line chart, data points, the sun a tooltip at the peak
im = canvas(c['paper'], c['clay'], 1.2)
for k in range(1, 6): line(im, [(60, 90 * k + 40), (1140, 90 * k + 40)], c['clay'], 2)
pts = [(60, 470), (190, 380), (300, 420), (420, 260), (530, 330), (650, 170), (760, 300), (880, 240), (1000, 360), (1140, 300)]
poly(im, pts + [(1140, 600), (60, 600)], c['plum'])
pts2 = [(x, y + 90 + 20 * math.sin(x / 90)) for x, y in pts]
poly(im, pts2 + [(1140, 600), (60, 600)], c['deep'])
line(im, pts, c['wine'], 5)
for x, y in pts: disc(im, x, y, 9, c['paper']); ring(im, x, y, 9, c['wine'], 3)
poly(im, [(650, 170), (690, 205), (668, 215), (650, 200), (632, 215), (610, 205)], c['paper'])
disc(im, 650, 80, 40, c['ochre'])
rr(im, 700, 58, 820, 100, 10, c['ink']); text(im, 716, 64, '4,810 m', 22, c['paper'], 700)
finish(im, OUT + 'nature2_04_line_chart.jpg', seed=54)

# 5 Checkbox meadow: a field of flowers whose heads are checkboxes, most of them ticked
im = canvas(c['mist'], c['paper'], 1)
disc(im, 200, 120, 60, c['ochre'])
rng = np.random.default_rng(55)
ridge(im, 420, 14, 160, c['moss'], seed=9, jag=0.2)
for k in range(26):
    x = 40 + k * 44 + rng.normal(0, 8); top = 300 + rng.integers(0, 120)
    line(im, [(x, 600), (x, top)], c['pine'], 4)
    side = 1 if k % 2 else -1
    ly = top + 80 + (k % 3) * 18
    poly(im, [(x, ly), (x + side * 26, ly - 18), (x + side * 8, ly + 6)], c['pine'])
    on = rng.random() > 0.25
    check(im, x, top, 32, [c['wine'], c['plum'], c['indigo'], c['ochre']][k % 4] if on else c['deep'], on)
rr(im, 0, 560, 1200, 600, 0, c['pine'])
finish(im, OUT + 'nature2_05_checkbox_meadow.jpg', seed=55)

# 6 Moon pagination: the phases of the moon as page dots over a night sea, mirrored around the full moon
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 60, 300, c['mist'], seed=56)
def phase(im, x, y, r, f, waxing, lit, dark):
    """f = lit fraction 0..1; waxing lights the right side."""
    disc(im, x, y, r, dark)
    if f <= 0: return
    m = Image.new('L', (W, H), 0); dm = ImageDraw.Draw(m)
    box = [(x - r)*S, (y - r)*S, (x + r)*S, (y + r)*S]
    dm.pieslice(box, -90, 90, fill=255) if waxing else dm.pieslice(box, 90, 270, fill=255)
    tw = abs(1 - 2 * f) * r
    tb = [(x - tw)*S, (y - r)*S, (x + tw)*S, (y + r)*S]
    dm.ellipse(tb, fill=255 if f > 0.5 else 0)
    im.paste(Image.new('RGB', (W, H), lit), (0, 0), m)
fr = [0, 0.25, 0.5, 1, 0.5, 0.25, 0]
for k, f in enumerate(fr):
    x = 600 + (k - 3) * 140; y = 230
    phase(im, x, y, 42, f if k != 0 and k != 6 else 0, k < 3, c['clay'], c['prussian'])
    if k == 3: ring(im, x, y, 58, c['ochre'], 4)
sea(im, 380, c['navy'], c['prussian'], gap=16)
for k in range(9):
    w_ = 120 - k * 11
    rr(im, 600 - w_/2, 400 + k * 20, 600 + w_/2, 406 + k * 20, 3, c['clay'])
finish(im, OUT + 'nature2_06_moon_pagination.jpg', amt=16, seed=56)

# 7 Leaf grid: one big leaf whose veins are a layout grid with guides
im = canvas(c['paper'], c['clay'], 1)
for x in range(80, 1200, 80): line(im, [(x, 0), (x, 600)], c['clay'], 1)
leaf = np.vstack([bez((300, 470), (420, 120), (800, 80), (950, 130), 80), bez((950, 130), (900, 330), (620, 560), (300, 470), 80)])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(x*S, y*S) for x, y in leaf], fill=255)
lay = Image.new('RGB', (W, H), c['moss']); ld = ImageDraw.Draw(lay)
for k in range(-6, 12):
    ld.line([((300 + k * 60)*S, 600*S), ((300 + k * 60 + 380)*S, 0)], fill=c['pine'], width=3*S)
for k in range(0, 12):
    ld.line([(0, (k * 55)*S), (1200*S, (k * 55 + 120)*S)], fill=tuple(min(255, v + 25) for v in c['moss']), width=2*S)
im.paste(lay, (0, 0), m)
line(im, list(map(tuple, bez((260, 500), (420, 380), (700, 200), (950, 130), 60))), c['pine'], 6)
for (a, b) in [(300, 470), (950, 130)]: rr(im, a - 8, b - 8, a + 8, b + 8, 2, c['paper'], c['wine'], 2)
line(im, [(300, 60), (300, 560)], c['wine'], 1.5); line(im, [(950, 60), (950, 560)], c['wine'], 1.5)
line(im, [(300, 536), (950, 536)], c['wine'], 1.5)
for xx in (300, 950): line(im, [(xx, 528), (xx, 544)], c['wine'], 1.5)
rr(im, 560, 520, 690, 552, 8, c['wine']); text(im, 574, 524, '650 px', 20, c['paper'], 700)
disc(im, 1060, 110, 46, c['wine'])
finish(im, OUT + 'nature2_07_leaf_grid.jpg', seed=57)

# 8 Layer stack: a landscape pulled apart into named layers, each label level with its layer
im = canvas(c['mist'], c['paper'], 1)
layers = [(c['ochre'], 'sky'), (c['wine'], 'sun'), (c['plum'], 'mountains'), (c['teal'], 'sea'), (c['pine'], 'hills')]
CW, CH = 520, 110          # card width and depth of the parallelogram
for k, (col, name) in enumerate(layers):
    ox, oy = 440 + k * 40, 70 + k * 92
    card = [(ox, oy + CH/2), (ox + CW/2, oy), (ox + CW, oy + CH/2), (ox + CW/2, oy + CH)]
    poly(im, [(x + 5, y + 8) for x, y in card], c['clay'])
    poly(im, card, col if name == 'sky' else c['paper'])
    cx_, cy_ = ox + CW/2, oy + CH/2
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(x*S, y*S) for x, y in card], fill=255)
    lay = im.copy()
    if name == 'sun': disc(lay, cx_, cy_, 28, col)
    if name == 'mountains': poly(lay, [(cx_ - 120, cy_ + 30), (cx_, cy_ - 34), (cx_ + 120, cy_ + 30)], col)
    if name == 'sea':
        for j in (-1, 0, 1): line(lay, [(cx_ - 130 + t, cy_ + j * 14 + math.sin(t / 18) * 4) for t in range(0, 261, 6)], col, 3)
    if name == 'hills': poly(lay, [(cx_ - 200, cy_ + 6), (cx_ - 60, cy_ - 30), (cx_ + 80, cy_ - 8), (cx_ + 200, cy_ + 6), (cx_, cy_ + 50)], col)
    im.paste(lay, (0, 0), m)
    lx = 150
    rr(im, lx, cy_ - 16, lx + 130, cy_ + 16, 8, c['wine'] if name == 'sun' else c['ink']); text(im, lx + 14, cy_ - 12, name, 20, c['paper'], 700)
    line(im, [(lx + 138, cy_), (ox - 12, cy_)], c['skyb'], 1.5); disc(im, ox - 12, cy_, 3, c['skyb'])
finish(im, OUT + 'nature2_08_layers.jpg', seed=58)
print('done')

"""Vibes exploration, nature + UI set: 8 landscapes built from interface pieces, in the house style."""
import sys, os
os.environ['VIBES_SET'] = 'vibes_nature'
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
disc(im, 858, 378, 84, c['plum']); disc(im, 850, 370, 84, c['wine'])
ridge(im, 520, 10, 120, c['moss'], seed=2, jag=0.3); ridge(im, 555, 8, 80, c['pine'], seed=4, jag=0.3)
finish(im, OUT + 'nature_01_toggle.jpg', seed=51)

# 2 Tree diagram: a tree whose branches are a node hierarchy, leaves as dots
im = canvas(c['mist'], c['paper'], 1)
disc(im, 1000, 120, 56, c['wine'])
nodes = {0: (600, 470)}
edges = []
lv = [(600, 470)]; k = 1
rng = np.random.default_rng(52)
levels = [[(600, 470)]]
for depth, (n, dy, spread) in enumerate([(2, 110, 300), (4, 90, 160), (8, 70, 80)]):
    nxt = []
    for (px, py) in levels[-1]:
        for j in range(2):
            x = px + (j - 0.5) * spread + rng.normal(0, 10); y = py - dy
            edges.append(((px, py), (x, y))); nxt.append((x, y))
    levels.append(nxt)
for (a, b) in edges:
    line(im, list(map(tuple, bez(a, (a[0], (a[1] + b[1]) / 2), (b[0], (a[1] + b[1]) / 2), b, 30))), c['deep'], 5)
line(im, [(600, 470), (600, 560)], c['deep'], 12)
for lvl, pts in enumerate(levels):
    for (x, y) in pts:
        disc(im, x, y, [16, 14, 12, 26][lvl], [c['deep'], c['plum'], c['teal'], c['moss']][lvl])
for (x, y) in levels[-1]:
    for _ in range(7): disc(im, x + rng.normal(0, 30), y - 26 + rng.normal(0, 22), 18 + rng.integers(0, 10), [c['moss'], c['pine'], c['teal'], c['moss']][int(rng.integers(0, 4))])
    disc(im, x, y, 12, c['deep'])
rr(im, 0, 560, 1200, 600, 0, c['clay'])
finish(im, OUT + 'nature_02_tree_diagram.jpg', seed=52)

# 3 Speech cloud: a cloud-shaped chat bubble raining lines onto hills
im = canvas(c['skyb'], c['mist'], 1)
for (x, y, r) in [(480, 190, 80), (580, 150, 105), (690, 185, 85), (770, 215, 62)]: disc(im, x, y, r, c['paper'])
rr(im, 400, 190, 830, 275, 42, c['paper'])
poly(im, [(470, 262), (520, 262), (455, 320)], c['paper'])
for k in range(3): disc(im, 545 + k * 55, 220, 12, c['indigo'])
for x in range(470, 800, 30):
    line(im, [(x, 300), (x - 14, 360)], c['indigo'], 3)
ridge(im, 410, 26, 140, c['moss'], seed=6, jag=0.3); ridge(im, 470, 20, 100, c['pine'], seed=8, jag=0.3)
sea(im, 540, c['teal'], c['foamb'], gap=16, amp=3)
finish(im, OUT + 'nature_03_speech_cloud.jpg', seed=53)

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
finish(im, OUT + 'nature_04_line_chart.jpg', seed=54)

# 5 Checkbox meadow: a field of flowers whose heads are checkboxes, most of them ticked
im = canvas(c['mist'], c['paper'], 1)
disc(im, 200, 120, 60, c['ochre'])
rng = np.random.default_rng(55)
ridge(im, 420, 14, 160, c['moss'], seed=9, jag=0.2)
for k in range(26):
    x = 40 + k * 44 + rng.normal(0, 8); top = 300 + rng.integers(0, 120)
    line(im, list(map(tuple, bez((x, 600), (x + rng.normal(0, 14), 520), (x + rng.normal(0, 14), top + 60), (x, top), 20))), c['pine'], 4)
    poly(im, [(x, top + 90), (x + 24, top + 70), (x + 4, top + 100)], c['pine'])
    on = rng.random() > 0.25
    check(im, x, top, 32, [c['wine'], c['plum'], c['indigo'], c['ochre']][k % 4] if on else c['deep'], on)
rr(im, 0, 560, 1200, 600, 0, c['pine'])
finish(im, OUT + 'nature_05_checkbox_meadow.jpg', seed=55)

# 6 Moon pagination: the phases of the moon as page dots over a night sea, one active
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 60, 300, c['mist'], seed=56)
for k in range(7):
    x = 180 + k * 140; y = 230
    disc(im, x, y, 42, c['prussian'])
    f = k / 6
    if 0 < f < 1:
        m = Image.new('L', (W, H), 0); dm = ImageDraw.Draw(m)
        dm.ellipse([(x - 42)*S, (y - 42)*S, (x + 42)*S, (y + 42)*S], fill=255)
        off = (f * 2 - 1) * 84
        dm.ellipse([(x - 42 + off)*S, (y - 42)*S, (x + 42 + off)*S, (y + 42)*S], fill=0)
        im.paste(Image.new('RGB', (W, H), c['clay']), (0, 0), m)
    if k == 3:
        disc(im, x, y, 42, c['clay']); ring(im, x, y, 58, c['ochre'], 4)
sea(im, 380, c['navy'], c['prussian'], gap=16)
for k in range(9):
    w_ = 120 - k * 11
    rr(im, 600 - w_/2, 400 + k * 20, 600 + w_/2, 406 + k * 20, 3, c['clay'])
finish(im, OUT + 'nature_06_moon_pagination.jpg', amt=16, seed=56)

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
rr(im, 560, 520, 690, 552, 8, c['wine']); text(im, 574, 524, '650 px', 20, c['paper'], 700)
disc(im, 1060, 110, 46, c['wine'])
finish(im, OUT + 'nature_07_leaf_grid.jpg', seed=57)

# 8 Layer stack: a landscape pulled apart into stacked layers, like a layers panel in 3D
im = canvas(c['mist'], c['paper'], 1)
layers = [(c['ochre'], 'sky'), (c['wine'], 'sun'), (c['plum'], 'mountains'), (c['teal'], 'sea'), (c['pine'], 'hills')]
for k, (col, name) in enumerate(layers):
    ox, oy = 300 + k * 60, 70 + k * 80
    card = [(ox, oy + 60), (ox + 420, oy), (ox + 620, oy + 60), (ox + 200, oy + 120)]
    poly(im, [(x + 6, y + 10) for x, y in card], c['clay'])
    poly(im, card, c['paper'] if name != 'sky' else col)
    cx_, cy_ = ox + 310, oy + 60
    if name == 'sun': disc(im, cx_, cy_, 32, col)
    if name == 'mountains': poly(im, [(ox + 180, oy + 95), (ox + 300, oy + 20), (ox + 430, oy + 75)], col)
    if name == 'sea':
        for j in range(3): line(im, [(ox + 120 + t, oy + 70 + j * 12 - t * 0.14 + math.sin(t / 18) * 3) for t in range(0, 360, 6)], col, 3)
    if name == 'hills': poly(im, [(ox + 60, oy + 82), (ox + 250, oy + 40), (ox + 470, oy + 70), (ox + 200, oy + 116)], col)
    rr(im, 120, oy + 40, 240, oy + 72, 8, c['ink'] if k != 1 else c['wine']); text(im, 134, oy + 44, name, 20, c['paper'], 700)
finish(im, OUT + 'nature_08_layers.jpg', seed=58)
print('done')

"""Vibes exploration, humans set: 8 illustrations of people in the house style."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vhelp import *

def figure(im, x, base, h, body, head, legs=True, stride=0):
    """A tiny standing person: round head, pill body, two leg lines."""
    hr = h * 0.13
    disc(im, x, base - h + hr, hr, head)
    rr(im, x - h*0.14, base - h + hr*2.3, x + h*0.14, base - h*0.38, h*0.14, body)
    if legs:
        line(im, [(x - h*0.05, base - h*0.42), (x - h*0.07 - stride, base)], body, max(2, h*0.06))
        line(im, [(x + h*0.05, base - h*0.42), (x + h*0.07 + stride, base)], body, max(2, h*0.06))

def bust(im, x, y, r, body, head, ring_col=None):
    """Head and shoulders seen from behind or front: an arch with a head on top."""
    d = ImageDraw.Draw(im)
    d.ellipse([(x-r)*S, (y-r*0.5)*S, (x+r)*S, (y+r*1.5)*S], fill=body)
    if ring_col: d.ellipse([(x-r*0.6)*S, (y+r*0.05)*S, (x+r*0.6)*S, (y+r*1.3)*S], outline=ring_col, width=2*S)
    hr = r * 0.4
    d.ellipse([(x-hr)*S, (y-r*0.5-hr*1.75)*S, (x+hr)*S, (y-r*0.5+hr*0.25)*S], fill=head)

def profile_mask(pts, edge_x):
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon([(x*S, y*S) for x, y in pts] + [(edge_x*S, 660*S)], fill=255)
    return m

# 1 Two faces, one vase: profiles nose to nose, the space between them is a vase holding the sun
im = canvas(c['ochre'], c['paper'], 0.9)
L_ = profile(1.0, (130, 40)); R_ = profile(1.0, (1070, 40), flip=True)
for pts, edge, body, stripe, ph, half in [(L_, 130, c['indigo'], c['prussian'], 0, (0, 598)), (R_, 1070, c['plum'], c['deep'], 2, (602, 1200))]:
    def shape(d, pts=pts, edge=edge, half=half):
        d.polygon([(x*S, y*S) for x, y in pts] + [(edge*S, 660*S)], fill=255)
        d.rectangle([0 if half[0] else half[1]*S, 0, half[0]*S if half[0] else W, H], fill=0)
    clip_stripes(im, shape, body, stripe, gap=15, phase=ph)
disc(im, 600, 150, 40, c['wine'])
finish(im, OUT + 'humans_01_two_faces.jpg', seed=21)

# 2 The thinker: one profile whose head is full of seigaiha, a sun rising from the crown
im = canvas(c['mist'], c['paper'], 1)
disc(im, 700, 95, 62, c['wine'])
P_ = profile(1.05, (330, 40))
mask = profile_mask(P_, 330)
layer = Image.new('RGB', (W, H), c['indigo'])
seigaiha(layer, 80, [c['indigo'], c['teal'], c['prussian'], c['pine']], r=30, line=c['paper'])
body = Image.new('RGB', (W, H), c['indigo'])
cut = Image.new('L', (W, H), 0); ImageDraw.Draw(cut).rectangle([0, 0, W, 395*S], fill=255)
body.paste(layer, (0, 0), cut)
im.paste(body, (0, 0), mask)
finish(im, OUT + 'humans_02_thinker.jpg', seed=22)

# 3 Listening: a profile turned toward rings of sound arriving from the right
im = canvas(c['paper'], c['clay'], 1.4)
P_ = profile(1.0, (120, 40))
clip_stripes(im, lambda d: d.polygon([(x*S, y*S) for x, y in P_] + [(120*S, 660*S)], fill=255), c['teal'], c['pine'], gap=15)
ex, ey = 350, 250
for k, r in enumerate(range(70, 440, 36)):
    d = ImageDraw.Draw(im)
    d.arc([(ex + 640 - r)*S, (ey - r)*S, (ex + 640 + r)*S, (ey + r)*S], 140, 220, fill=[c['plum'], c['mauve'], c['wine']][k % 3], width=3*S)
disc(im, ex + 640, ey, 34, c['wine'])
finish(im, OUT + 'humans_03_listening.jpg', seed=23)

# 4 Pair at a screen: two people from behind, looking at a big screen with a sunrise on it
im = canvas(c['indigo'], c['navy'], 1)
rr(im, 260, 60, 940, 420, 18, c['ink'])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([280*S, 80*S, 920*S, 400*S], radius=8*S, fill=255)
scr = canvas(c['ochre'], c['paper'], 0.8); disc(scr, 600, 300, 70, c['wine']); sea(scr, 300, c['teal'], c['foamb'], gap=14, amp=3, freq=22)
im.paste(scr, (0, 0), m)
glow(im, 600, 250, 320, c['skyb'], strength=0.18)
bust(im, 470, 520, 120, c['plum'], c['deep'])
bust(im, 740, 535, 120, c['prussian'], c['ink'])
finish(im, OUT + 'humans_04_pair_screen.jpg', amt=15, seed=24)

# 5 Critique circle: seen from above, people around a round table of sticky notes
im = canvas(c['clay'], c['paper'], 1)
cx, cy = 600, 300
disc(im, cx, cy, 150, c['paper'])
for k in range(4):
    a = k * 1.4 + 0.3
    rr(im, cx - 90 + k*48, cy - 60 + (k % 2)*50, cx - 40 + k*48, cy - 10 + (k % 2)*50, 4, [c['ochre'], c['skyb'], c['mauve'], c['ochre']][k])
cols = [(c['indigo'], c['ink']), (c['plum'], c['deep']), (c['teal'], c['pine']), (c['wine'], c['deep']), (c['prussian'], c['navy']), (c['moss'], c['pine'])]
d = ImageDraw.Draw(im)
for k, (b, h_) in enumerate(cols):
    a = k / len(cols) * 2 * math.pi - math.pi / 2
    px, py = cx + 225 * math.cos(a), cy + 225 * math.sin(a)
    sh = Image.new('RGBA', (300*S, 300*S), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse([50*S, 115*S, 250*S, 185*S], fill=b + (255,)); sd.ellipse([110*S, 110*S, 190*S, 190*S], fill=h_ + (255,))
    sh = sh.rotate(-math.degrees(a) - 90, resample=Image.BICUBIC)
    im.paste(sh, (int(px*S - sh.width/2), int(py*S - sh.height/2)), sh)
finish(im, OUT + 'humans_05_critique_circle.jpg', seed=25)

# 6 The crowd at night: shoulders as seigaiha scales under a moon, one person in ochre
im = canvas(c['navy'], c['indigo'], 1)
disc(im, 980, 110, 52, c['clay']); stars(im, 40, 230, c['mist'], seed=26, avoid=(980, 110, 52))
rows = [(300, c['skyb'], c['prussian']), (375, c['teal'], c['pine']), (450, c['prussian'], c['indigo']), (525, c['pine'], c['teal']), (600, c['indigo'], c['navy'])]
for i, (y, b, h_) in enumerate(rows):
    off = 62 if i % 2 else 0
    for j, x in enumerate(range(-124 + off, 1300, 124)):
        hl = (i == 1 and j == 3)
        bust(im, x, y, 62, c['ochre'] if hl else b, c['wine'] if hl else h_, ring_col=c['navy'])
finish(im, OUT + 'humans_06_crowd_night.jpg', amt=16, seed=26)

# 7 Walker: a small figure on a long horizon under a huge sun, footprints behind
im = canvas(c['paper'], c['clay'], 1.2)
disc(im, 600, 330, 210, c['wine'])
sea(im, 430, c['mauve'], c['clay'], gap=22, amp=3, freq=50)
for k in range(9): disc(im, 300 + k*36, 448 + (k % 2)*6, 4, c['plum'])
figure(im, 650, 432, 96, c['ink'], c['ink'], stride=10)
finish(im, OUT + 'humans_07_walker.jpg', seed=27)

# 8 Steps up: figures climbing stacked steps, each step striped with swell lines, toward the sun
im = canvas(c['skyb'], c['mist'], 1)
disc(im, 1030, 110, 58, c['ochre'])
steps = [(0, 520, c['pine']), (230, 450, c['teal']), (460, 380, c['prussian']), (690, 310, c['indigo']), (920, 240, c['plum'])]
for x, y, col in steps:
    clip_stripes(im, (lambda x, y: (lambda d: d.rectangle([x*S, y*S, 1200*S, 600*S], fill=255)))(x, y), col, tuple(min(255, v + 30) for v in col), gap=16, amp=3, freq=30)
for (x, y, _), col in zip(steps[:4], [c['ochre'], c['wine'], c['clay'], c['paper']]):
    figure(im, x + 150, y, 70, col, col, stride=4)
figure(im, 1060, 240, 80, c['wine'], c['wine'])
finish(im, OUT + 'humans_08_steps.jpg', seed=28)
print('done')

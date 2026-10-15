import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
OUT = '/home/claude/ctrl-curious/assets/email/days/tue/'
c = C
rng = np.random.default_rng(42)

# 01 Moonlit water: full moon, long broken reflection on still indigo water
im = canvas(c['navy'], c['prussian'], 1.3)
stars(im, 60, 330, c['paper'], seed=11, avoid=(760, 150, 70))
glow(im, 760, 150, 140, c['skyb'], 0.35)
disc(im, 760, 150, 70, c['clay'])
ridge(im, 350, 14, 120, c['indigo'], seed=2, jag=0.6)
d = ImageDraw.Draw(im); d.rectangle([0, 380*S, W, H], fill=c['navy'])
for k in range(16):
    y = 392 + k*13; w = 150 - k*5 + rng.normal(0, 10)
    for j in range(rng.integers(2, 4)):
        x = 760 + rng.normal(0, 18) - w/2; ww = w * rng.uniform(0.3, 0.7)
        d.rounded_rectangle([x*S, y*S, (x+ww)*S, (y+5)*S], radius=2*S, fill=c['clay'] if k < 9 else c['mauve'])
finish(im, OUT + 'tue_01.jpg', seed=21)

# 02 Blue hour harbour: moored boats, ochre lanterns, reflections
im = canvas(c['prussian'], c['skyb'], 1.1)
disc(im, 980, 110, 34, c['paper'])
ridge(im, 300, 26, 160, c['indigo'], seed=4)
d = ImageDraw.Draw(im); d.rectangle([0, 395*S, W, H], fill=c['indigo'])
for i, (x, L) in enumerate([(90, 260), (420, 220), (720, 280), (1010, 170)]):
    y = 395
    boat(im, x, y - 6, L, c['ink'])
    mx = x + L*0.45
    d.line([(mx*S, (y-150 + i*12)*S), (mx*S, (y-8)*S)], fill=c['ink'], width=3*S)
    d.line([(mx*S, (y-150 + i*12)*S), ((x+L*0.95)*S, (y-14)*S)], fill=c['ink'], width=S)
    glow(im, mx + 18, y - 40, 22, c['ochre'], 0.8, blur=10)
    disc(im, mx + 18, y - 40, 5, c['ochre'])
    for k in range(8):
        yy = 412 + k*20; ww = 26 - k*2
        d.rectangle([(mx+18-ww/2 + rng.normal(0, 3))*S, yy*S, (mx+18+ww/2)*S, (yy+3)*S], fill=c['ochre'])
    for k in range(5):
        yy = 420 + k*28
        d.line([((x+20)*S, yy*S), ((x+L-20)*S, (yy+2)*S)], fill=c['prussian'], width=2*S)
finish(im, OUT + 'tue_02.jpg', seed=22)

# 03 Firefly forest: rows of pines, ochre fireflies, crescent moon
im = canvas(c['navy'], c['teal'], 1.4)
crescent(im, 230, 120, 48, c['clay'], tuple(int(v) for v in np.array(c['navy'])*0.85 + np.array(c['teal'])*0.15))
stars(im, 40, 260, c['paper'], seed=13, avoid=(230, 120, 60))
for row, (base, h, col, step) in enumerate([(380, 170, c['teal'], 70), (460, 210, c['pine'], 90), (600, 260, (24, 44, 40), 120)]):
    r2 = np.random.default_rng(row)
    for x in range(-40, 1260, step):
        pine_tree(im, x + r2.normal(0, 12), base + r2.normal(0, 10), h * r2.uniform(0.8, 1.1), col)
    if row < 2:
        ImageDraw.Draw(im).rectangle([0, base*S, W, H], fill=col)
for _ in range(55):
    x, y = rng.integers(20, 1180), rng.integers(260, 580)
    glow(im, x, y, 10, c['ochre'], 0.9, blur=6); disc(im, x, y, 2.5, (240, 210, 140))
finish(im, OUT + 'tue_03.jpg', seed=23)

# 04 City night shift: skyline with lit windows, crescent moon
im = canvas(c['indigo'], c['plum'], 1.2)
crescent(im, 960, 110, 44, c['clay'], tuple(int(v) for v in np.array(c['indigo'])*0.9 + np.array(c['plum'])*0.1))
stars(im, 35, 250, c['paper'], seed=14, avoid=(960, 110, 60))
d = ImageDraw.Draw(im)
x = -10
for layer, (col, hmin, hmax, ybase) in enumerate([(c['prussian'], 140, 260, 600), (c['navy'], 180, 360, 600)]):
    x = -10 + layer*30
    r2 = np.random.default_rng(layer + 7)
    while x < 1210:
        w = r2.integers(60, 130); h = r2.integers(hmin, hmax); top = ybase - h
        d.rectangle([x*S, top*S, (x+w)*S, H], fill=col)
        if r2.random() < 0.3:
            d.rectangle([(x+w/2-3)*S, (top-40)*S, (x+w/2+3)*S, top*S], fill=col)
        if layer == 1:
            for wy in range(int(top) + 16, 590, 22):
                for wx in range(int(x) + 10, int(x + w) - 12, 18):
                    if r2.random() < 0.28:
                        d.rectangle([wx*S, wy*S, (wx+8)*S, (wy+10)*S], fill=c['ochre'] if r2.random() < 0.7 else c['clay'])
        x += w + r2.integers(4, 16)
finish(im, OUT + 'tue_04.jpg', seed=24)

# 05 Desk by the window: interior, window frame with moon and hills, lamp glow, plant
im = canvas(c['plum'], c['ink'], 1)
d = ImageDraw.Draw(im)
wx0, wy0, wx1, wy1 = 470, 70, 1050, 440
win = canvas(c['navy'], c['prussian'], 1)
disc(win, 860, 160, 50, c['clay']); stars(win, 30, 300, c['paper'], seed=15, avoid=(860, 160, 55))
ridge(win, 340, 22, 110, c['teal'], seed=5); ridge(win, 380, 18, 80, c['pine'], seed=6)
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rectangle([wx0*S, wy0*S, wx1*S, wy1*S], fill=255)
im.paste(win, (0, 0), mask)
d.rectangle([wx0*S, wy0*S, wx1*S, wy1*S], outline=c['clay'], width=14*S)
d.line([((wx0+wx1)/2*S, wy0*S), ((wx0+wx1)/2*S, wy1*S)], fill=c['clay'], width=10*S)
d.line([(wx0*S, (wy0+wy1)/2*S), (wx1*S, (wy0+wy1)/2*S)], fill=c['clay'], width=10*S)
d.rectangle([0, 450*S, W, H], fill=c['ink'])
d.rectangle([0, 440*S, W, 456*S], fill=c['deep'])
glow(im, 260, 470, 220, c['ochre'], 0.35)
d = ImageDraw.Draw(im)
d.polygon([(180*S, 250*S), (340*S, 250*S), (300*S, 180*S), (220*S, 180*S)], fill=c['wine'])
d.line([(260*S, 250*S), (260*S, 440*S)], fill=c['clay'], width=6*S)
d.ellipse([200*S, 432*S, 320*S, 452*S], fill=c['clay'])
d.rectangle([520*S, 400*S, 760*S, 440*S], fill=c['clay']); d.rectangle([540*S, 380*S, 740*S, 400*S], fill=c['mauve'])
d.rectangle([1080*S, 360*S, 1150*S, 440*S], fill=c['wine'])
for a in range(-60, 61, 20):
    ang = math.radians(a - 90); L = 110
    d.ellipse([(1115 + math.cos(ang)*L*0.6 - 18)*S, (360 + math.sin(ang)*L*0.6 - 40)*S, (1115 + math.cos(ang)*L*0.6 + 18)*S, (360 + math.sin(ang)*L*0.6 + 40)*S], fill=c['moss'])
finish(im, OUT + 'tue_05.jpg', seed=25)

# 06 Lighthouse: beam across a dark teal sea, rocky island
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 50, 380, c['paper'], seed=16)
beam = Image.new('L', (W, H), 0)
ImageDraw.Draw(beam).polygon([(300*S, 205*S), (1250*S, 60*S), (1250*S, 330*S)], fill=110)
beam = beam.filter(ImageFilter.GaussianBlur(18*S))
im.paste(Image.new('RGB', (W, H), c['mist']), (0, 0), beam)
sea(im, 420, c['teal'], c['skyb'], gap=20)
d = ImageDraw.Draw(im)
d.polygon([(120*S, 430*S), (200*S, 370*S), (430*S, 380*S), (520*S, 440*S)], fill=c['ink'])
d.polygon([(270*S, 380*S), (285*S, 215*S), (315*S, 215*S), (330*S, 380*S)], fill=c['paper'])
for y in (250, 300, 345):
    d.polygon([(281*S - (y-215)*0.09*S, y*S), (319*S + (y-215)*0.09*S, y*S), (320*S + (y+18-215)*0.09*S, (y+18)*S), (280*S - (y+18-215)*0.09*S, (y+18)*S)], fill=c['wine'])
d.rectangle([278*S, 190*S, 322*S, 215*S], fill=c['ochre'])
d.polygon([(272*S, 190*S), (300*S, 165*S), (328*S, 190*S)], fill=c['wine'])
glow(im, 300, 202, 40, c['ochre'], 0.8, blur=16)
finish(im, OUT + 'tue_06.jpg', seed=26)

# 07 Aurora: green and teal curtains over snowy peaks
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 90, 420, c['paper'], seed=17)
for k, (col, y0, amp) in enumerate([(c['moss'], 150, 40), (c['teal'], 200, 50), ((110, 170, 140), 120, 30)]):
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for x in range(0, 1200, 4):
        top = y0 + amp*math.sin(x/140 + k*2) + 20*math.sin(x/47 + k)
        md.line([(x*S, top*S), (x*S, (top + 120 + 50*math.sin(x/90 + k))*S)], fill=int(60 + 150*math.sin(x/26 + k*1.7)**4), width=3*S)
    m = m.filter(ImageFilter.GaussianBlur(2*S))
    im.paste(Image.new('RGB', (W, H), col), (0, 0), m)
mountain(im, 0, 640, 300, 300, 600, c['prussian'], snow=c['paper'])
mountain(im, 450, 1200, 840, 260, 600, c['indigo'], snow=c['paper'])
ridge(im, 520, 18, 90, c['navy'], seed=8)
finish(im, OUT + 'tue_07.jpg', seed=27)

# 08 Woodblock clouds: stylised curling clouds, crescent moon, wine and indigo bands
im = canvas(c['indigo'], c['navy'], 1)
crescent(im, 820, 210, 90, c['clay'], dx=0.32, dy=-0.12)
d = ImageDraw.Draw(im)
def cloud(cx, cy, s, col, line):
    for (ox, oy, r) in [(-60, 10, 34), (-20, -18, 44), (30, -6, 38), (70, 12, 28)]:
        d.ellipse([(cx + ox*s - r*s)*S, (cy + oy*s - r*s)*S, (cx + ox*s + r*s)*S, (cy + oy*s + r*s)*S], fill=col)
    d.rectangle([(cx - 94*s)*S, (cy + 10*s)*S, (cx + 98*s)*S, (cy + 40*s)*S], fill=col)
    for (ox, oy, r) in [(-20, -18, 30), (-20, -18, 16), (30, -6, 24)]:
        d.arc([(cx + ox*s - r*s)*S, (cy + oy*s - r*s)*S, (cx + ox*s + r*s)*S, (cy + oy*s + r*s)*S], 180, 360, fill=line, width=int(3*S*s))
    d.line([((cx - 94*s)*S, (cy + 40*s)*S), ((cx + 98*s)*S, (cy + 40*s)*S)], fill=line, width=int(3*S*s))
cloud(300, 160, 1.6, c['plum'], c['mauve'])
cloud(1040, 360, 1.5, c['prussian'], c['skyb'])
cloud(560, 430, 1.9, c['teal'], c['foamb'])
cloud(160, 500, 1.4, c['wine'], c['mauve'])
stars(im, 40, 600, c['paper'], seed=18, avoid=(820, 210, 100))
finish(im, OUT + 'tue_08.jpg', seed=28)
print('done')

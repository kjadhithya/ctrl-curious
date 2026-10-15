"""Tuesday · Night shift — refined set: more detail, and the wave theme woven through every scene."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
OUT = '/home/claude/ctrl-curious/assets/email/days/tue/'
c = C
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))

def moon(im, x, y, r, col=None, glow_col=None):
    col = col or c['clay']
    if glow_col: glow(im, x, y, r*2, glow_col, 0.35)
    disc(im, x, y, r, col)
    rng = np.random.default_rng(int(x))
    for _ in range(6):
        a = rng.uniform(0, 6.28); dd = rng.uniform(0, r*0.6); rr = rng.uniform(r*0.08, r*0.18)
        disc(im, x + math.cos(a)*dd, y + math.sin(a)*dd, rr, mixc(col, c['mauve'], 0.45))

def windows_house(d, x, base, w, h, wall, roof, lit):
    d.rectangle([x*S, (base-h)*S, (x+w)*S, base*S], fill=wall)
    d.polygon([((x-6)*S, (base-h)*S), ((x+w/2)*S, (base-h-h*0.6)*S), ((x+w+6)*S, (base-h)*S)], fill=roof)
    d.rectangle([(x+w*0.3)*S, (base-h*0.7)*S, (x+w*0.6)*S, (base-h*0.35)*S], fill=lit)

# ---------- 01 Moonlit sea: moon, wave-cloud, rowing boat, curling waves, seigaiha shore ----------
rng = np.random.default_rng(101)
im = canvas(c['navy'], c['prussian'], 1.3)
twilight(im, 360, c['orchid'], 240, 0.55)
stars(im, 80, 330, c['paper'], seed=11, avoid=(820, 140, 80))
for p in [(140, 70), (320, 160), (1100, 60)]: sparkle(im, *p, 7, c['paper'])
moon(im, 820, 140, 70, glow_col=c['skyb'])
curl_cloud(im, 700, 205, 0.75, c['indigo'], c['skyb'])
curl_cloud(im, 1080, 250, 0.5, c['prussian'], c['skyb'])
birds(im, [(600, 110), (630, 95), (655, 120)], c['mist'], 9)
ridge(im, 335, 16, 120, c['indigo'], seed=2, jag=0.6)
d = ImageDraw.Draw(im)
for hx_ in (180, 230, 410, 990):
    disc(im, hx_, 332 + rng.normal(0, 4), 3, c['ochre'])
d.rectangle([0, 360*S, W, H], fill=c['navy'])
for k in range(18):
    y = 368 + k*11; w = 160 - k*5 + rng.normal(0, 10)
    for j in range(rng.integers(2, 4)):
        x = 820 + rng.normal(0, 20) - w/2; ww = w*rng.uniform(0.3, 0.7)
        d.rounded_rectangle([x*S, y*S, (x+ww)*S, (y+4)*S], radius=2*S, fill=c['clay'] if k < 10 else c['mauve'])
ripple_lines(im, 365, 560, c['prussian'], gap=12, seed=3, frac=0.45)
boat(im, 700, 440, 170, c['ink'], tilt=4)
d = ImageDraw.Draw(im)
d.ellipse([782*S, 404*S, 800*S, 422*S], fill=c['ink']); d.rectangle([780*S, 418*S, 802*S, 440*S], fill=c['ink'])
d.line([(760*S, 452*S), (720*S, 470*S)], fill=c['ink'], width=3*S)
d.line([(845*S, 420*S), (845*S, 400*S)], fill=c['ink'], width=2*S)
glow(im, 845, 396, 14, c['ochre'], 0.9, blur=7); disc(im, 845, 396, 4, c['ochre'])
wave(im, -80, 250, 0.42, c['prussian'], c['skyb'], c['paper'], seed=61)
wave(im, 980, 345, 0.27, c['teal'], c['foamb'], c['paper'], seed=62)
front_sea(im, 520, c['indigo'], c['prussian'], foam=c['skyb'], seed=1)
seigaiha(im, 560, [c['prussian'], c['indigo']], r=26, line=c['navy'])
finish(im, OUT + 'tue_01.jpg', seed=21)

# ---------- 02 Blue-hour harbour: hill village, pier and lamp, boats with cabins, wave at the harbour mouth ----------
rng = np.random.default_rng(102)
im = canvas(c['prussian'], c['skyb'], 1.1)
twilight(im, 300, c['orchid'], 230, 0.6)
stars(im, 30, 200, c['mist'], seed=12, avoid=(950, 100, 40))
moon(im, 950, 100, 34, col=c['paper'], glow_col=c['mist'])
curl_cloud(im, 300, 110, 0.55, mixc(c['prussian'], c['skyb'], 0.35), c['mist'])
ridge(im, 270, 30, 160, c['indigo'], seed=4)
d = ImageDraw.Draw(im)
for i, x in enumerate(range(40, 1160, 64)):
    if rng.random() < 0.75:
        base = 300 + 25*math.sin(x/160) + rng.normal(0, 6); w = rng.integers(26, 40)
        windows_house(d, x, base + 30, w, rng.integers(18, 28), mixc(c['indigo'], c['prussian'], 0.4), c['wine'] if i % 3 == 0 else c['navy'],
                      c['ochre'] if rng.random() < 0.7 else c['clay'])
d.rectangle([0, 360*S, W, 395*S], fill=c['indigo'])
d.rectangle([0, 352*S, 520*S, 364*S], fill=c['ink'])
for x in range(20, 520, 46): d.rectangle([x*S, 364*S, (x+7)*S, 395*S], fill=c['ink'])
d.rectangle([496*S, 270*S, 501*S, 352*S], fill=c['ink']); d.rectangle([486*S, 262*S, 511*S, 272*S], fill=c['ink'])
glow(im, 498, 278, 30, c['ochre'], 0.85, blur=14); disc(im, 498, 278, 6, c['ochre'])
d = ImageDraw.Draw(im)
for i, (x, L) in enumerate([(60, 220), (380, 200), (650, 260), (950, 180)]):
    y = 395
    boat(im, x, y - 6, L, c['ink'], tilt=0)
    d.rectangle([(x+L*0.55)*S, (y-34)*S, (x+L*0.78)*S, (y-12)*S], fill=c['clay'])
    d.rectangle([(x+L*0.6)*S, (y-28)*S, (x+L*0.66)*S, (y-20)*S], fill=c['ochre'])
    mx = x + L*0.35; top = y - 160 + i*10
    d.line([(mx*S, top*S), (mx*S, (y-10)*S)], fill=c['ink'], width=3*S)
    d.line([(mx*S, top*S), ((x+L*0.95)*S, (y-14)*S)], fill=c['ink'], width=S)
    d.line([(mx*S, top*S), ((x+4)*S, (y-14)*S)], fill=c['ink'], width=S)
    d.polygon([(mx*S, top*S), ((mx+22)*S, (top+7)*S), (mx*S, (top+14)*S)], fill=c['wine'])
    glow(im, mx + 16, y - 50, 18, c['ochre'], 0.8, blur=9); disc(im, mx + 16, y - 50, 4, c['ochre'])
    d = ImageDraw.Draw(im)
reflect(im, 395, 600, darken=0.5, tint=c['indigo'], wobble=4)
ripple_lines(im, 395, 600, c['skyb'], gap=13, seed=5, frac=0.35)
d = ImageDraw.Draw(im)
for (x, L) in [(60, 220), (380, 200), (650, 260), (950, 180)]:
    mx = x + L*0.35 + 16
    for k in range(9):
        yy = 405 + k*20; ww = 22 - k*2
        d.rectangle([(mx-ww/2 + rng.normal(0, 3))*S, yy*S, (mx+ww/2)*S, (yy+3)*S], fill=c['ochre'])
birds(im, [(700, 160), (725, 148), (748, 170)], c['indigo'], 9)
d.polygon([(1080*S, 600*S), (1120*S, 470*S), (1200*S, 440*S), (1200*S, 600*S)], fill=c['ink'])
wave(im, 870, 300, 0.33, c['teal'], c['foamb'], c['paper'], seed=63)
front_sea(im, 545, c['indigo'], c['prussian'], foam=c['skyb'], seed=2)
finish(im, OUT + 'tue_02.jpg', seed=22)

# ---------- 03 Firefly lake: cabin with smoke, pines, snowy peak, lake reflections, wave crests ----------
rng = np.random.default_rng(103)
sky_top, sky_bot = c['navy'], mixc(c['navy'], c['teal'], 0.6)
im = canvas(sky_top, sky_bot, 1.4)
twilight(im, 420, c['orchid'], 300, 0.66)
sky_bot = tuple(int(v) for v in np.asarray(im.getpixel((10, 380*S))))
stars(im, 70, 240, c['paper'], seed=13, avoid=(230, 110, 60))
glow(im, 230, 110, 90, c['skyb'], 0.3)
crescent(im, 230, 110, 46, c['clay'])
mountain(im, 520, 1040, 780, 150, 430, c['prussian'], snow=c['paper'])
curl_cloud(im, 980, 170, 0.55, mixc(c['navy'], c['teal'], 0.35), c['skyb'])
for row, (base, h, col, step) in enumerate([(400, 150, c['teal'], 60), (440, 190, c['pine'], 80)]):
    r2 = np.random.default_rng(row)
    for x in range(-40, 1260, step):
        pine_tree(im, x + r2.normal(0, 12), base + r2.normal(0, 8), h * r2.uniform(0.75, 1.1), col)
    ImageDraw.Draw(im).rectangle([0, base*S, W, 450*S], fill=col)
d = ImageDraw.Draw(im)
windows_house(d, 150, 448, 90, 56, c['wine'], c['ink'], c['ochre'])
d.rectangle([215*S, 360*S, 228*S, 392*S], fill=c['ink'])
glow(im, 180, 410, 50, c['ochre'], 0.4)
for k in range(7):
    disc(im, 222 + k*9 + math.sin(k)*6, 350 - k*18, 7 + k*1.6, mixc(c['mist'], sky_bot, 0.25 + k*0.09))
reflect(im, 450, 600, darken=0.45, tint=c['navy'], wobble=3)
ripple_lines(im, 452, 560, c['teal'], gap=12, seed=6, frac=0.4)
for x in range(30, 1200, 140):
    wave(im, x, 455 + (x // 140 % 2)*14, 0.12, c['teal'], c['foamb'], c['foamb'], claws=False, seed=x)
front_sea(im, 545, c['navy'], None, foam=c['teal'], seed=3)
d = ImageDraw.Draw(im)
for x in range(0, 1200, 9):
    h = rng.integers(10, 34)
    d.line([(x*S, 600*S), ((x + rng.normal(0, 4))*S, (600-h)*S)], fill=mixc(c['pine'], c['ink'], 0.5), width=2*S)
for _ in range(60):
    x, y = rng.integers(20, 1180), rng.integers(250, 560); r = rng.choice([1.8, 2.5, 3.2])
    glow(im, x, y, r*4, c['ochre'], 0.9, blur=r*2.5); disc(im, x, y, r, (240, 210, 140))
finish(im, OUT + 'tue_03.jpg', seed=23)

# ---------- 04 City by the bay: skyline with tanks, antennas, neon; reflections; great wave in front ----------
rng = np.random.default_rng(104)
im = canvas(c['indigo'], c['plum'], 1.2)
twilight(im, 470, c['orchid'], 300, 0.55)
stars(im, 40, 220, c['paper'], seed=14, avoid=(960, 100, 60))
glow(im, 960, 100, 80, c['mauve'], 0.25)
crescent(im, 960, 100, 42, c['clay'])
curl_cloud(im, 380, 130, 0.6, mixc(c['indigo'], c['plum'], 0.45), c['mauve'])
curl_cloud(im, 760, 210, 0.45, mixc(c['indigo'], c['plum'], 0.6), c['mauve'])
d = ImageDraw.Draw(im)
for p in [(150, 80), (162, 80)]: disc(im, *p, 2, c['wine'])
for layer, (col, hmin, hmax) in enumerate([(mixc(c['prussian'], c['plum'], 0.3), 120, 220), (c['navy'], 150, 300)]):
    x = -10 + layer*25; r2 = np.random.default_rng(layer + 7)
    while x < 1210:
        w = int(r2.integers(60, 130)); h = int(r2.integers(hmin, hmax)); top = 470 - h
        d.rectangle([x*S, top*S, (x+w)*S, 470*S], fill=col)
        roll = r2.random()
        if roll < 0.25:
            d.rectangle([(x+w*0.2)*S, (top-26)*S, (x+w*0.2+22)*S, top*S], fill=col)
            d.polygon([((x+w*0.2-3)*S, (top-26)*S), ((x+w*0.2+11)*S, (top-36)*S), ((x+w*0.2+25)*S, (top-26)*S)], fill=col)
        elif roll < 0.5:
            d.line([((x+w/2)*S, (top-60)*S), ((x+w/2)*S, top*S)], fill=col, width=3*S)
            if layer == 1: disc(im, x+w/2, top-60, 3, c['wine'])
        if layer == 1:
            for wy in range(top + 14, 460, 20):
                for wx in range(int(x) + 9, int(x + w) - 12, 16):
                    if r2.random() < 0.3:
                        d.rectangle([wx*S, wy*S, (wx+7)*S, (wy+9)*S], fill=c['ochre'] if r2.random() < 0.7 else c['clay'])
            if r2.random() < 0.18 and w > 90:
                d.rectangle([(x+12)*S, (top+20)*S, (x+w-12)*S, (top+40)*S], fill=c['wine'])
                d.rectangle([(x+18)*S, (top+27)*S, (x+w-18)*S, (top+31)*S], fill=c['mauve'])
        x += w + int(r2.integers(4, 14))
d.rectangle([0, 466*S, W, 474*S], fill=c['ink'])
reflect(im, 474, 600, darken=0.45, tint=c['indigo'], wobble=4)
ripple_lines(im, 474, 600, c['plum'], gap=11, seed=7, frac=0.4)
wave(im, -70, 225, 0.5, c['indigo'], c['skyb'], c['paper'], seed=64)
wave(im, 930, 380, 0.24, c['teal'], c['foamb'], c['paper'], seed=65)
front_sea(im, 548, c['navy'], c['prussian'], foam=c['skyb'], seed=4)
finish(im, OUT + 'tue_04.jpg', seed=24)

# ---------- 05 Night shift desk: window onto a moonlit great wave, curtains, laptop, mug, books, cat ----------
rng = np.random.default_rng(105)
im = canvas(c['plum'], mixc(c['plum'], c['ink'], 0.6), 1)
d = ImageDraw.Draw(im)
for x in range(0, 1200, 46): d.line([(x*S, 0), (x*S, 450*S)], fill=mixc(c['plum'], c['deep'], 0.35), width=2*S)
wx0, wy0, wx1, wy1 = 470, 60, 1000, 400
win = canvas(c['navy'], c['prussian'], 1)
twilight(win, 300, c['orchid'], 220, 0.55)
stars(win, 40, 300, c['paper'], seed=15, avoid=(880, 130, 50))
glow(win, 880, 130, 70, c['skyb'], 0.3); disc(win, 880, 130, 40, c['clay'])
sea(win, 300, c['indigo'], c['prussian'], gap=14)
wave(win, 470, 20, 0.42, c['prussian'], c['skyb'], c['paper'], seed=66)
wave(win, 690, 205, 0.18, c['teal'], c['foamb'], c['paper'], seed=67)
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rectangle([wx0*S, wy0*S, wx1*S, wy1*S], fill=255)
im.paste(win, (0, 0), mask)
d = ImageDraw.Draw(im)
d.rectangle([wx0*S, wy0*S, wx1*S, wy1*S], outline=c['clay'], width=14*S)
d.line([((wx0+wx1)/2*S, wy0*S), ((wx0+wx1)/2*S, wy1*S)], fill=c['clay'], width=9*S)
d.line([(wx0*S, (wy0+wy1)/2*S), (wx1*S, (wy0+wy1)/2*S)], fill=c['clay'], width=9*S)
for side in (0, 1):
    x0 = wx0 - 70 if side == 0 else wx1 - 10; x1 = x0 + 80
    d.polygon([(x0*S, 40*S), (x1*S, 40*S), ((x1 - (20 if side == 0 else -20))*S, 300*S), ((x0 + (10 if side == 0 else 30))*S, 430*S), (x0*S, 430*S)], fill=c['wine'])
    for k in range(1, 4): d.line([((x0 + k*20)*S, 44*S), ((x0 + k*20 - (6 if side == 0 else -6))*S, 420*S)], fill=c['deep'], width=3*S)
d.rectangle([(wx0-90)*S, 30*S, (wx1+90)*S, 40*S], fill=c['clay'])
d.rectangle([90*S, 90*S, 260*S, 230*S], fill=c['clay']); d.rectangle([102*S, 102*S, 248*S, 218*S], fill=c['paper'])
seig = canvas(c['paper']); seigaiha(seig, 150, [c['prussian'], c['teal']], r=16, line=c['paper'])
m2 = Image.new('L', (W, H), 0); ImageDraw.Draw(m2).rectangle([108*S, 150*S, 242*S, 212*S], fill=255); im.paste(seig, (0, 0), m2)
d = ImageDraw.Draw(im)
disc(im, 200, 128, 14, c['wine'])
d = ImageDraw.Draw(im)
d.rectangle([wx0*S, 400*S, wx1*S, 416*S], fill=c['clay'])
cx = 920
d.ellipse([(cx-30)*S, 350*S, (cx+30)*S, 402*S], fill=c['ink']); d.ellipse([(cx+10)*S, 330*S, (cx+44)*S, 362*S], fill=c['ink'])
d.polygon([((cx+14)*S, 338*S), ((cx+18)*S, 320*S), ((cx+26)*S, 334*S)], fill=c['ink']); d.polygon([((cx+30)*S, 334*S), ((cx+40)*S, 320*S), ((cx+42)*S, 338*S)], fill=c['ink'])
d.line([((cx-28)*S, 392*S), ((cx-60)*S, 400*S)], fill=c['ink'], width=6*S)
d.rectangle([0, 450*S, W, H], fill=c['ink']); d.rectangle([0, 444*S, W, 458*S], fill=c['deep'])
cone = Image.new('L', (W, H), 0)
ImageDraw.Draw(cone).polygon([(190*S, 250*S), (330*S, 250*S), (470*S, 450*S), (60*S, 450*S)], fill=70)
cone = cone.filter(ImageFilter.GaussianBlur(12*S)); im.paste(Image.new('RGB', (W, H), c['ochre']), (0, 0), cone)
d = ImageDraw.Draw(im)
d.polygon([(180*S, 250*S), (340*S, 250*S), (300*S, 180*S), (220*S, 180*S)], fill=c['wine'])
d.line([(260*S, 250*S), (260*S, 300*S), (300*S, 380*S), (270*S, 444*S)], fill=c['clay'], width=6*S, joint='curve')
d.ellipse([220*S, 436*S, 320*S, 452*S], fill=c['clay'])
d.polygon([(560*S, 444*S), (760*S, 444*S), (790*S, 456*S), (530*S, 456*S)], fill=c['clay'])
d.polygon([(585*S, 444*S), (735*S, 444*S), (720*S, 330*S), (600*S, 330*S)], fill=c['clay'])
d.polygon([(593*S, 438*S), (727*S, 438*S), (714*S, 338*S), (606*S, 338*S)], fill=c['skyb'])
for k in range(5): d.line([(616*S, (352 + k*16)*S), ((690 - (k % 2)*30)*S, (352 + k*16)*S)], fill=c['indigo'], width=3*S)
glow(im, 660, 390, 80, c['skyb'], 0.2)
d = ImageDraw.Draw(im)
d.rounded_rectangle([830*S, 396*S, 880*S, 448*S], radius=6*S, fill=c['paper'])
for k in range(3): d.arc([(836 + k*13)*S, 408*S, (850 + k*13)*S, 422*S], 180, 360, fill=c['prussian'], width=2*S)
d.arc([872*S, 408*S, 896*S, 432*S], 270, 90, fill=c['paper'], width=5*S)
for k, ox in enumerate((842, 858)):
    pts = [((ox + 6*math.sin(t/6 + k))*S, (388 - t)*S) for t in range(0, 44, 2)]
    d.line(pts, fill=c['mauve'], width=3*S)
for k, (col, h) in enumerate([(c['teal'], 18), (c['wine'], 14), (c['ochre'], 16), (c['prussian'], 12)]):
    y1 = 444 - sum([18, 14, 16, 12][:k]); d.rectangle([(960 + k*3)*S, (y1-h)*S, (1080 - k*4)*S, y1*S], fill=col)
d.rectangle([1100*S, 380*S, 1160*S, 444*S], fill=c['clay'])
for a in range(-70, 71, 20):
    ang = math.radians(a - 90)
    d.ellipse([(1130 + math.cos(ang)*50 - 14)*S, (380 + math.sin(ang)*60 - 34)*S, (1130 + math.cos(ang)*50 + 14)*S, (380 + math.sin(ang)*60 + 34)*S], fill=c['moss'] if a % 40 else c['pine'])
finish(im, OUT + 'tue_05.jpg', seed=25)

# ---------- 06 Lighthouse and the great wave: beam, keeper's cottage, ship, wave crashing on rocks ----------
rng = np.random.default_rng(106)
im = canvas(c['navy'], c['indigo'], 1)
twilight(im, 410, c['orchid'], 260, 0.5)
stars(im, 70, 380, c['paper'], seed=16, avoid=(160, 90, 50))
crescent(im, 160, 90, 36, c['clay'])
beam = Image.new('L', (W, H), 0)
ImageDraw.Draw(beam).polygon([(880*S, 200*S), (-60*S, 30*S), (-60*S, 330*S)], fill=120)
beam = beam.filter(ImageFilter.GaussianBlur(16*S)); im.paste(Image.new('RGB', (W, H), c['mist']), (0, 0), beam)
curl_cloud(im, 560, 120, 0.55, mixc(c['navy'], c['indigo'], 0.5), c['skyb'])
sea(im, 410, c['teal'], c['skyb'], gap=18)
d = ImageDraw.Draw(im)
boat(im, 420, 404, 90, c['ink']); d.rectangle([450*S, 384*S, 480*S, 400*S], fill=c['ink'])
for xx in (455, 468): disc(im, xx, 392, 2.5, c['ochre'])
d = ImageDraw.Draw(im)
rocks = [(720, 600), (760, 430), (840, 395), (960, 400), (1040, 420), (1120, 470), (1200, 470), (1200, 600)]
d.polygon([(x*S, y*S) for x, y in rocks], fill=c['ink'])
for k in range(10):
    x = rng.integers(760, 1180); y = rng.integers(430, 590)
    d.polygon([(x*S, y*S), ((x+30)*S, (y-12)*S), ((x+52)*S, (y+8)*S)], fill=mixc(c['ink'], c['plum'], 0.35))
windows_house(d, 960, 420, 80, 46, c['clay'], c['wine'], c['ochre'])
lx = 880
d.polygon([((lx-26)*S, 410*S), ((lx-15)*S, 215*S), ((lx+15)*S, 215*S), ((lx+26)*S, 410*S)], fill=c['paper'])
for y in (250, 300, 350):
    k1 = (y-215)/195; k2 = (y+20-215)/195
    d.polygon([((lx-15-11*k1)*S, y*S), ((lx+15+11*k1)*S, y*S), ((lx+15+11*k2)*S, (y+20)*S), ((lx-15-11*k2)*S, (y+20)*S)], fill=c['wine'])
d.rectangle([(lx-30)*S, 210*S, (lx+30)*S, 218*S], fill=c['ink'])
d.rectangle([(lx-18)*S, 182*S, (lx+18)*S, 210*S], fill=c['ochre'])
for xx in (lx-8, lx+8): d.line([(xx*S, 182*S), (xx*S, 210*S)], fill=c['ink'], width=2*S)
d.polygon([((lx-24)*S, 182*S), (lx*S, 156*S), ((lx+24)*S, 182*S)], fill=c['wine'])
glow(im, lx, 196, 46, c['ochre'], 0.75, blur=18)
birds(im, [(620, 230), (648, 214), (672, 238), (700, 222)], c['mist'], 9)
wave(im, -60, 40, 0.68, c['prussian'], c['skyb'], c['paper'], seed=68)
wave(im, 420, 300, 0.3, c['teal'], c['foamb'], c['paper'], seed=69)
front_sea(im, 520, c['indigo'], c['prussian'], foam=c['skyb'], seed=5)
d = ImageDraw.Draw(im)
for _ in range(40):
    x = rng.normal(720, 30); y = rng.normal(430, 30); r = rng.uniform(4, 11)
    d.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=c['paper'])
finish(im, OUT + 'tue_06.jpg', seed=26)

# ---------- 07 Aurora lake: wave-curled aurora, peaks, mirrored lake, pines, glowing tent, shooting star ----------
rng = np.random.default_rng(107)
im = canvas(c['navy'], c['indigo'], 1)
twilight(im, 400, c['orchid'], 260, 0.62)
stars(im, 140, 330, c['paper'], seed=17)
for p in [(90, 50), (1120, 80), (700, 40)]: sparkle(im, *p, 6, c['paper'])
d = ImageDraw.Draw(im); d.line([(860*S, 40*S), (980*S, 90*S)], fill=c['paper'], width=2*S); disc(im, 980, 90, 3, c['paper'])
for k, (col, y0, amp) in enumerate([(c['moss'], 120, 40), (c['teal'], 170, 46), ((120, 180, 150), 95, 28)]):
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for x in range(0, 1200, 4):
        ph = x/150 + k*2
        top = y0 + amp*math.sin(ph) + 18*math.sin(x/47 + k) - 26*max(0, math.sin(ph*2.0))**8
        md.line([(x*S, top*S), (x*S, (top + 110 + 40*math.sin(x/90 + k))*S)], fill=int(60 + 150*math.sin(x/26 + k*1.7)**4), width=3*S)
    m = m.filter(ImageFilter.GaussianBlur(2*S)); im.paste(Image.new('RGB', (W, H), col), (0, 0), m)
mountain(im, -60, 560, 250, 230, 400, c['prussian'], snow=c['paper'])
mountain(im, 380, 1000, 700, 190, 400, c['indigo'], snow=c['paper'])
mountain(im, 820, 1300, 1060, 260, 400, c['prussian'], snow=c['paper'])
d = ImageDraw.Draw(im); d.rectangle([0, 392*S, W, 400*S], fill=c['navy'])
for x in list(range(-20, 260, 34)) + list(range(940, 1240, 34)):
    pine_tree(im, x + rng.normal(0, 6), 400, rng.uniform(80, 130), c['ink'])
d = ImageDraw.Draw(im)
d.polygon([(330*S, 400*S), (370*S, 350*S), (410*S, 400*S)], fill=c['ochre'])
d.polygon([(362*S, 400*S), (370*S, 372*S), (378*S, 400*S)], fill=c['wine'])
glow(im, 370, 385, 50, c['ochre'], 0.4)
reflect(im, 400, 600, darken=0.55, tint=c['navy'], wobble=2)
ripple_lines(im, 402, 600, c['prussian'], gap=12, seed=8, frac=0.35)
front_sea(im, 560, c['navy'], None, foam=c['prussian'], seed=6)
seigaiha(im, 575, [c['indigo'], c['prussian']], r=22, line=c['navy'])
finish(im, OUT + 'tue_07.jpg', seed=27)

# ---------- 08 Woodblock night: curling clouds, cranes, pagoda on a hill, great wave and seigaiha sea ----------
rng = np.random.default_rng(108)
im = canvas(c['indigo'], c['navy'], 1)
twilight(im, 470, c['orchid'], 300, 0.5)
glow(im, 820, 170, 150, c['mauve'], 0.25)
crescent(im, 820, 170, 82, c['clay'], dx=0.32, dy=-0.12)
for _ in range(26):
    sparkle(im, rng.integers(10, 1190), rng.integers(10, 360), rng.choice([4, 5, 7]), c['paper'])
stars(im, 40, 360, c['paper'], seed=18, avoid=(820, 170, 90))
curl_cloud(im, 270, 120, 1.15, c['plum'], c['mauve'])
curl_cloud(im, 1060, 300, 0.95, c['prussian'], c['skyb'])
curl_cloud(im, 560, 300, 0.8, c['wine'], c['mauve'])
d = ImageDraw.Draw(im)
for (x, y, s) in [(470, 90, 1.0), (540, 70, 0.8), (600, 110, 0.9)]:
    d.polygon([((x-34*s)*S, (y-6*s)*S), (x*S, (y+4*s)*S), ((x+34*s)*S, (y-6*s)*S), ((x+4*s)*S, (y+10*s)*S), ((x-4*s)*S, (y+10*s)*S)], fill=c['paper'])
    d.line([((x+4*s)*S, (y+6*s)*S), ((x+24*s)*S, (y+2*s)*S)], fill=c['paper'], width=max(2, int(3*s*S)))
    disc(im, x + 24*s, y + 2*s, 3*s, c['wine'])
d = ImageDraw.Draw(im)
d.polygon([(0*S, 600*S), (0*S, 420*S), (140*S, 380*S), (300*S, 410*S), (420*S, 600*S)], fill=c['pine'])
px, base = 170, 386
for k, (w, h) in enumerate([(84, 30), (70, 28), (56, 26), (42, 24)]):
    y1 = base - k*34
    d.rectangle([(px - w*0.32)*S, (y1-h)*S, (px + w*0.32)*S, y1*S], fill=c['ink'])
    d.polygon([((px - w/2 - 10)*S, (y1-h)*S), ((px + w/2 + 10)*S, (y1-h)*S), ((px + w*0.3)*S, (y1-h-12)*S), ((px - w*0.3)*S, (y1-h-12)*S)], fill=c['wine'])
    d.rectangle([(px-5)*S, (y1-h+8)*S, (px+5)*S, (y1-6)*S], fill=c['ochre'])
d.line([(px*S, (base-4*34-40)*S), (px*S, (base-4*34-10)*S)], fill=c['ink'], width=4*S)
glow(im, px, 330, 40, c['ochre'], 0.25)
sea(im, 470, c['indigo'], None)
wave(im, 470, 110, 0.55, c['prussian'], c['skyb'], c['paper'], seed=70)
wave(im, 330, 330, 0.24, c['teal'], c['foamb'], c['paper'], seed=71)
seigaiha(im, 500, [c['prussian'], c['teal'], c['indigo']], r=28, line=c['navy'])
finish(im, OUT + 'tue_08.jpg', seed=28)
print('done')

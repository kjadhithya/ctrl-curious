"""Four background options for the blog's bottom signup band (1440x460). Text sits on the left, art on the right."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 384 * lib.S          # 1200 x 384, roughly 1440 x 460
from lib import *
from PIL import ImageOps
H = lib.H
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/'
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
def save(im, name, amt=16, seed=3):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), dtype=float) + rng.normal(0, amt, (H, W, 1))
    Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 614), Image.LANCZOS).save(OUT + name, quality=86)

# 1 Night wave: navy sky, a small great wave on the right with the moon in its curl
im = canvas(c['navy'], c['indigo'], 1.2)
stars(im, 70, 280, c['paper'], seed=21, avoid=(965, 180, 40))
disc(im, 235, 182, 30, c['clay'])
sea(im, 300, c['navy'], c['prussian'], gap=14)
wave(im, 20, 80, 0.33, c['prussian'], c['skyb'], c['foamb'], seed=9, soft=True)
front_sea(im, 330, c['navy'], c['prussian'], foam=c['skyb'], seed=3)
save(ImageOps.mirror(im), 'signup_night_wave.jpg', seed=21)

# 2 Wine moon: the current wine night, with a crescent moon, its reflection and a wave-scale shore
im = canvas(mixc(c['wine'], c['ink'], 0.55), mixc(c['wine'], c['ink'], 0.25), 1)
stars(im, 60, 270, c['paper'], seed=22, avoid=(920, 130, 80))
crescent(im, 920, 130, 70, c['clay'], dx=0.3, dy=-0.15)
d = ImageDraw.Draw(im); d.rectangle([0, 290*S, W, H], fill=mixc(c['wine'], c['ink'], 0.7))
rng = np.random.default_rng(5)
for k in range(5):
    y = 298 + k*9; w = 120 - k*16
    d.rounded_rectangle([(905 - w/2 + rng.normal(0, 6))*S, y*S, (905 + w/2)*S, (y+3)*S], radius=2*S, fill=c['clay'] if k < 3 else c['mauve'])
seigaiha(im, 340, [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=18, line=mixc(c['wine'], c['ink'], 0.7))
save(im, 'signup_wine_moon.jpg', seed=22)

# 3 Dusk tide: deep plum sky, an ochre sun sinking into dark swell lines
im = canvas(mixc(c['plum'], c['ink'], 0.6), mixc(c['wine'], c['plum'], 0.4), 1.1)
disc(im, 900, 300, 92, c['ochre'])
cols = [c['prussian'], c['indigo'], c['teal'], c['navy'], c['pine']]
d = ImageDraw.Draw(im)
for i, col in enumerate(cols):
    y0 = 288 + i*20
    top = [(x*S, (y0 + math.sin(x/(80 - i*6) + i) * (12 - i))*S) for x in range(0, 1210, 6)]
    d.polygon(top + [(W, H), (0, H)], fill=col)
    lt = [(x*S, (y0 + 8 + math.sin(x/(80 - i*6) + i) * (12 - i))*S) for x in range(0, 1210, 6)]
    d.line(lt, fill=c['mauve'] if i % 2 else c['skyb'], width=2*S)
save(im, 'signup_dusk_tide.jpg', seed=23)

# 4 Moonlit swell: navy sky, a pale moon and soft blue swell lines across the bottom
im = canvas(c['navy'], mixc(c['navy'], c['prussian'], 0.6), 1)
stars(im, 90, 260, c['paper'], seed=24, avoid=(1010, 100, 46))
glow(im, 1010, 100, 90, c['skyb'], 0.25)
disc(im, 1010, 100, 40, c['mist'])
cols = [c['skyb'], c['prussian'], c['teal'], c['indigo'], c['navy']]
d = ImageDraw.Draw(im)
for i, col in enumerate(cols):
    y0 = 270 + i*22
    top = [(x*S, (y0 + math.sin(x/(90 - i*6) + i*1.3) * (14 - i*1.5))*S) for x in range(0, 1210, 6)]
    d.polygon(top + [(W, H), (0, H)], fill=col)
    lt = [(x*S, (y0 + 9 + math.sin(x/(90 - i*6) + i*1.3) * (14 - i*1.5))*S) for x in range(0, 1210, 6)]
    d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2*S)
save(im, 'signup_moonlit_swell.jpg', seed=24)
print('done')

# 5 Wine sunset: option 2's wine sky and wave-scale shore with option 3's ochre sun sinking at the horizon
# the original footer's background: wine fading to warm dark brown, mottled, as in the moon artwork
rng_bg = np.random.default_rng(7)
def _blur_noise(r):
    n = Image.fromarray((rng_bg.random((H, W)) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(r*S))
    a = np.asarray(n, dtype=float); return (a - a.min()) / (a.max() - a.min() + 1e-6)
fbm = 0.5*_blur_noise(18) + 0.3*_blur_noise(6) + 0.2*_blur_noise(2)
t = np.clip(fbm*0.6 + np.linspace(0.12, 0.55, H)[:, None], 0, 1)
wine85 = np.array(c['wine'], float)*0.85; ink_rw = np.array(hx('2A1C18'), float)
base = wine85[None, None]*(1 - t[..., None]) + ink_rw[None, None]*t[..., None]
im = Image.fromarray(np.clip(base, 0, 255).astype('uint8'))
disc(im, 900, 290, 92, c['ochre'])
d = ImageDraw.Draw(im); d.rectangle([0, 290*S, W, H], fill=mixc(c['wine'], c['ink'], 0.7))
rng = np.random.default_rng(5)
for k in range(5):
    y = 298 + k*9; w = 170 - k*24
    d.rounded_rectangle([(900 - w/2 + rng.normal(0, 6))*S, y*S, (900 + w/2)*S, (y+3)*S], radius=2*S, fill=c['ochre'] if k < 3 else mixc(c['ochre'], c['wine'], 0.4))
seigaiha(im, 340, [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=18, line=mixc(c['wine'], c['ink'], 0.7))
small = im.resize((1100, 352), Image.LANCZOS)
rng5 = np.random.default_rng(25)
a5 = np.asarray(small, dtype=float) + rng5.normal(0, 30, (352, 1100, 1))
Image.fromarray(np.clip(a5, 0, 255).astype('uint8')).resize((1920, 614), Image.BICUBIC).save(OUT + 'signup_wine_sunset.jpg', quality=88)
print('done 5')

# 7 Wine sunset with the moon's colour: option 5, but the sun takes the blush moon colour of the original band
im = Image.fromarray(np.clip(base, 0, 255).astype('uint8'))
moon_mauve = np.array(hx('E3B9A6'), float); moon_paper = np.array(hx('F5EEE3'), float)
tone = moon_mauve[None, None]*(1 - (fbm*0.6)[..., None]) + moon_paper[None, None]*(fbm*0.6)[..., None]
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([(900-92)*S, (290-92)*S, (900+92)*S, (290+92)*S], fill=255)
im.paste(Image.fromarray(np.clip(tone, 0, 255).astype('uint8')), (0, 0), mask)
d = ImageDraw.Draw(im); d.rectangle([0, 290*S, W, H], fill=mixc(c['wine'], c['ink'], 0.7))
blush = (229, 202, 186)
rng = np.random.default_rng(5)
for k in range(5):
    y = 298 + k*9; w = 170 - k*24
    d.rounded_rectangle([(900 - w/2 + rng.normal(0, 6))*S, y*S, (900 + w/2)*S, (y+3)*S], radius=2*S, fill=blush if k < 3 else mixc(blush, c['wine'], 0.4))
seigaiha(im, 340, [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=18, line=mixc(c['wine'], c['ink'], 0.7))
small = im.resize((1100, 352), Image.LANCZOS)
rng7 = np.random.default_rng(27)
a7 = np.asarray(small, dtype=float) + rng7.normal(0, 30, (352, 1100, 1))
Image.fromarray(np.clip(a7, 0, 255).astype('uint8')).resize((1920, 614), Image.BICUBIC).save(OUT + 'signup_wine_sunset_blush.jpg', quality=88)
print('done 7')

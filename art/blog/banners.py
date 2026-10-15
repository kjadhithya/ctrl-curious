"""Three more wide wave banners for the blog home (options 2-4). Option 1 is banner_wave.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
from PIL import ImageOps
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/'
def save(im, name, amt=14, seed=3):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), dtype=float) + rng.normal(0, amt, (H, W, 1))
    Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 960), Image.LANCZOS).save(OUT + name, quality=86)
    from heavy_grain import heavy; heavy(OUT + name)

# 2 Seigaiha sunrise: a big half sun rising over a sea of wave scales, open sky for the headline
im = canvas(c['paper'], c['clay'], 1.6)
disc(im, 860, 440, 170, c['wine'])
seigaiha(im, 440, [c['indigo'], c['teal'], c['prussian'], c['pine']], r=38, line=c['paper'])
save(im, 'banner_seigaiha.jpg', seed=4)

# 3 Night wave: navy sky, blush moon inside the curl of a prussian wave
im = canvas(c['navy'], c['indigo'], 1.2)
stars(im, 90, 420, c['paper'], seed=9, avoid=(500, 250, 60))
disc(im, 500, 262, 48, c['clay'])
sea(im, 455, c['navy'], c['prussian'], gap=18)
wave(im, 30, -95, 0.8, c['prussian'], c['skyb'], c['foamb'], seed=5)
front_sea(im, 515, c['navy'], c['prussian'], foam=c['skyb'], seed=2)
seigaiha(im, 560, [c['indigo'], c['prussian']], r=22, line=c['navy'])
im = ImageOps.mirror(im)
save(im, 'banner_night.jpg', amt=16, seed=5)

# 4 Swell lines: rolling bands of blue and green, ochre sun, calm sky above
im = canvas(c['paper'], c['clay'], 2)
disc(im, 900, 170, 80, c['ochre'])
d = ImageDraw.Draw(im)
cols = [c['skyb'], c['prussian'], c['teal'], c['pine'], c['indigo'], c['moss'], c['navy']]
for i, col in enumerate(cols):
    y0 = 430 + i*26
    top = [(x*S, (y0 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
    d.polygon(top + [(W, H), (0, H)], fill=col)
    lt = [(x*S, (y0 + 10 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
    d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2*S)
save(im, 'banner_swell.jpg', seed=6)
print('done')

# 5 Swell lines with a wave: the rolling bands, a great wave rising out of them, ochre sun in its curl
def bands(im, start=0):
    d = ImageDraw.Draw(im)
    for i, col in enumerate(cols):
        if i < start: continue
        y0 = 430 + i*26
        top = [(x*S, (y0 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
        d.polygon(top + [(W, H), (0, H)], fill=col)
        lt = [(x*S, (y0 + 10 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
        d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2*S)
im = canvas(c['paper'], c['clay'], 2)
disc(im, 500, 262, 52, c['ochre'])
bands(im)
wave(im, 30, -95, 0.8, c['indigo'], c['skyb'], c['mist'], seed=5)
bands(im, start=1)
im = ImageOps.mirror(im)
save(im, 'banner_swell_wave.jpg', seed=7)
print('done 5')

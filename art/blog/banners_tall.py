"""Blog home banners, 16:9 with headroom so the menu can sit directly on the art (no bar).
Waves sit lower so their crests stay clear of the menu links."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 675 * lib.S          # 1200 x 675 canvas
from lib import *
from PIL import ImageOps
H = lib.H
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/'
def save(im, name, amt=14, seed=3):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGB'), dtype=float) + rng.normal(0, amt, (H, W, 1))
    Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 1080), Image.LANCZOS).save(OUT + name, quality=86)
D = 115   # vertical shift for the wave scenes

# 1 Great wave
im = canvas(c['paper'], c['clay'], 2.2)
disc(im, 400, 300, 40, c['wine'])
mountain(im, 335, 465, 400, 480, 455 + D, c['plum'], snow=c['paper'])
sea(im, 455 + D, c['teal'], c['skyb'], gap=18)
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True)
front_sea(im, 515 + D, c['teal'], c['skyb'], foam=c['foamb'], seed=2)
seigaiha(im, 560 + D, [c['prussian'], c['indigo']], r=22, line=c['teal'])
save(ImageOps.mirror(im), 'banner_wave_tall.jpg', seed=3)

# 2 Seigaiha sunrise
im = canvas(c['paper'], c['clay'], 1.6)
disc(im, 860, 440 + 80, 170, c['wine'])
seigaiha(im, 440 + 80, [c['indigo'], c['teal'], c['prussian'], c['pine']], r=38, line=c['paper'])
save(im, 'banner_seigaiha_tall.jpg', seed=4)

# 3 Night wave
im = canvas(c['navy'], c['indigo'], 1.2)
stars(im, 110, 470, c['paper'], seed=9, avoid=(400, 300, 52))
disc(im, 400, 300, 42, c['clay'])
sea(im, 455 + D, c['navy'], c['prussian'], gap=18)
wave(im, 10, 110, 0.6, c['prussian'], c['skyb'], c['foamb'], seed=5, soft=True)
front_sea(im, 515 + D, c['navy'], c['prussian'], foam=c['skyb'], seed=2)
seigaiha(im, 560 + D, [c['indigo'], c['prussian']], r=22, line=c['navy'])
save(ImageOps.mirror(im), 'banner_night_tall.jpg', amt=16, seed=5)

# 4 + 5 Swell lines (5 adds the wave)
cols = [c['skyb'], c['prussian'], c['teal'], c['pine'], c['indigo'], c['moss'], c['navy']]
def bands(im, start=0, base=430 + D):
    d = ImageDraw.Draw(im)
    for i, col in enumerate(cols):
        if i < start: continue
        y0 = base + i*26
        top = [(x*S, (y0 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
        d.polygon(top + [(W, H), (0, H)], fill=col)
        lt = [(x*S, (y0 + 10 + math.sin(x/(90 - i*6) + i) * (18 - i*1.5))*S) for x in range(0, 1210, 6)]
        d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2*S)
im = canvas(c['paper'], c['clay'], 2)
disc(im, 900, 170 + 80, 80, c['ochre'])
bands(im)
save(im, 'banner_swell_tall.jpg', seed=6)
im = canvas(c['paper'], c['clay'], 2)
disc(im, 400, 300, 44, c['ochre'])
bands(im)
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True)
bands(im, start=1)
save(ImageOps.mirror(im), 'banner_swell_wave_tall.jpg', seed=7)
print('done')

# 6 Swell lines with two waves: option 5 plus a smaller teal wave in front of the big one
im = canvas(c['paper'], c['clay'], 2)
disc(im, 400, 300, 44, c['ochre'])
bands(im)
wave(im, 10, 110, 0.6, c['prussian'], c['skyb'], c['mist'], seed=5, soft=True)
wave(im, 300, 437, 0.28, hx('4F7BA3'), c['foamb'], c['mist'], seed=8, soft=True)
bands(im, start=2)
save(ImageOps.mirror(im), 'banner_two_waves_tall.jpg', seed=8)
print('done 6')

# 5b Swell lines with a wave, sun high in the open sky above the back of the wave
im = canvas(c['paper'], c['clay'], 2)
disc(im, 1200 - 1110, 160, 50, c['ochre'])
bands(im)
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True)
bands(im, start=1)
save(ImageOps.mirror(im), 'banner_swell_wave_sun_tall.jpg', seed=7)
print('done 5b')

# 7 Swell lines with a wave, wine sun in the curl and a small snow-capped plum mountain behind
im = canvas(c['paper'], c['clay'], 2)
disc(im, 400, 300, 44, c['wine'])
mountain(im, 350, 570, 460, 425, 575, c['plum'], snow=c['paper'])
bands(im)
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True)
bands(im, start=1)
save(ImageOps.mirror(im), 'banner_swell_wave_mountain_tall.jpg', seed=7)
print('done 7')

# 7b Option 7 with the sun placed like 5b: wine sun high in the open sky, plum mountain under the curl
im = canvas(c['paper'], c['clay'], 2)
disc(im, 1200 - 1110, 160, 50, c['wine'])
mountain(im, 350, 570, 460, 425, 575, c['plum'], snow=c['paper'])
bands(im)
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True)
bands(im, start=1)
save(ImageOps.mirror(im), 'banner_swell_wave_mountain_sun_tall.jpg', seed=7)
print('done 7b')

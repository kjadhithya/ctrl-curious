import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
from PIL import ImageOps
OUT = '/home/claude/ctrl-curious/assets/email/days/mon/'
c = C

# 01 Classic: indigo great wave, teal sea, plum mountain, wine sun
im = canvas(c['paper'], c['clay'], 2)
disc(im, 1020, 85, 50, c['wine'])
mountain(im, 760, 980, 870, 330, 445, c['plum'])
sea(im, 445, c['teal'], c['skyb'])
wave(im, 0, -110, 0.86, c['indigo'], c['skyb'], c['paper'])
wave(im, 650, 175, 0.47, c['prussian'], c['foamb'], c['paper'], seed=6)
wave(im, -100, 295, 0.36, c['pine'], c['skyb'], c['paper'], claws=False, seed=7)
front_sea(im, 500, c['teal'], c['skyb'], seed=1)
finish(im, OUT + 'mon_01.jpg')

# 02 Dusk: mirrored wave curling left, mauve dusk sky, blush moon, pine sea
im = canvas(c['skyb'], c['mauve'], 1.2)
disc(im, 1040, 120, 62, c['paper'])
sea(im, 470, c['pine'], c['mauve'], gap=22)
wave(im, 120, -60, 0.78, c['prussian'], c['mist'], c['paper'], seed=11)
wave(im, -60, 280, 0.38, c['teal'], c['foamb'], c['paper'], claws=False, seed=12)
front_sea(im, 505, c['pine'], c['mauve'], gap=22, seed=2)
im = ImageOps.mirror(im)
finish(im, OUT + 'mon_02.jpg', seed=2)

# 03 Fuji: big snow-capped mountain behind a low row of waves, wine sun
im = canvas(c['mist'], c['paper'], 1)
disc(im, 600, 150, 95, c['wine'])
mountain(im, 230, 970, 600, 175, 470, c['indigo'], snow=c['paper'])
sea(im, 450, c['prussian'], c['skyb'], gap=18)
for i, x in enumerate(range(-80, 1200, 230)):
    wave(im, x, 330 + (i % 2) * 18, 0.3, c['teal'] if i % 2 else c['pine'], c['foamb'], c['paper'], seed=20 + i)
front_sea(im, 535, c['prussian'], c['skyb'], seed=3)
finish(im, OUT + 'mon_03.jpg', seed=3)

# 04 Night tide: navy sky with stars, blush moon, prussian wave
im = canvas(c['navy'], c['indigo'], 1)
disc(im, 950, 140, 70, c['clay'])
stars(im, 70, 380, c['paper'], avoid=(950, 140, 70))
sea(im, 450, c['navy'], c['prussian'], gap=18)
wave(im, 40, -45, 0.8, c['prussian'], c['skyb'], c['foamb'], seed=31)
wave(im, 700, 210, 0.42, c['teal'], c['skyb'], c['foamb'], seed=32)
front_sea(im, 495, c['navy'], c['prussian'], seed=4)
finish(im, OUT + 'mon_04.jpg', amt=16, seed=4)

# 05 Seigaiha sunrise: half sun on the horizon over a field of wave scales
im = canvas(c['paper'], c['clay'], 1)
disc(im, 600, 330, 150, c['wine'])
seigaiha(im, 330, [c['indigo'], c['teal'], c['prussian'], c['pine']], r=40, line=c['paper'])
finish(im, OUT + 'mon_05.jpg', seed=5)

# 06 Swell lines: stacked bands of rolling lines, ochre sun
im = canvas(c['paper'])
disc(im, 860, 120, 70, c['ochre'])
cols = [c['skyb'], c['prussian'], c['teal'], c['pine'], c['indigo'], c['moss'], c['navy']]
d = ImageDraw.Draw(im)
for i, col in enumerate(cols):
    y0 = 230 + i * 55
    top = [(x*S, (y0 + math.sin(x / (70 - i*4) + i) * (16 - i))*S) for x in range(0, 1210, 6)]
    d.polygon(top + [(W, H), (0, H)], fill=col)
    lt = [(x*S, (y0 + 14 + math.sin(x / (70 - i*4) + i) * (16 - i))*S) for x in range(0, 1210, 6)]
    d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2*S)
finish(im, OUT + 'mon_06.jpg', seed=6)

# 07 Ochre dawn: warm sky, green waves, low wine sun
im = canvas(c['ochre'], c['paper'], 0.8)
disc(im, 320, 380, 80, c['wine'])
sea(im, 450, c['pine'], c['ochre'], gap=24)
wave(im, 420, -60, 0.78, c['teal'], c['foamb'], c['paper'], seed=41)
wave(im, -40, 230, 0.45, c['moss'], c['foamb'], c['paper'], seed=42)
front_sea(im, 510, c['pine'], c['ochre'], gap=24, seed=5)
finish(im, OUT + 'mon_07.jpg', seed=7)

# 08 Rain and boats: grey-blue sky, rain, boats under a dark teal wave
im = canvas(c['skyb'], c['mist'], 1)
mountain(im, 820, 1080, 950, 330, 450, c['plum'], snow=c['paper'])
sea(im, 450, c['indigo'], c['skyb'], gap=18)
wave(im, -30, -100, 0.85, c['teal'], c['foamb'], c['paper'], seed=51)
front_sea(im, 500, c['indigo'], c['skyb'], seed=6)
boat(im, 520, 470, 300, c['clay'], rowers=c['ink'], tilt=10)
boat(im, 800, 515, 260, c['clay'], rowers=c['ink'], tilt=-8)
rain(im, c['paper'])
finish(im, OUT + 'mon_08.jpg', seed=8)
print('done')

"""Wednesday · Type specimen — 8 letterform hero images, each in a different typeface, with the wave theme."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
OUT = '/home/claude/ctrl-curious/assets/email/days/wed/'
c = C
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
def hline(im, y, col, x0=0, x1=1200, w=1):
    ImageDraw.Draw(im).line([(x0*S, y*S), (x1*S, y*S)], fill=col, width=max(1, int(w*S)))

# 01 Aa · Fraunces — paper letters on plum, specimen guide lines, seigaiha shore
im = canvas(c['plum'], mixc(c['plum'], c['deep'], 0.5), 1)
f = font('Fraunces', 400, wght=600, opsz=144, soft=0)
for y, col in [(470, c['mauve']), (285, mixc(c['plum'], c['mauve'], 0.5)), (155, mixc(c['plum'], c['mauve'], 0.5))]:
    hline(im, y, col, 60, 1140, 1.5)
text(im, (600, 470), 'Aa', f, c['paper'], anchor='ms')
seigaiha(im, 520, [c['prussian'], c['teal']], r=26, line=c['plum'])
finish(im, OUT + 'wed_01.jpg', seed=31)

# 02 Ww · DM Serif Display — letters filled with great-wave stripes, wine sun behind
im = canvas(c['paper'], c['clay'], 1.5)
disc(im, 860, 190, 120, c['wine'])
f = font('DMSerifDisplay', 430)
m = text_mask('Ww', f, (600, 500), anchor='ms')
fill = canvas(c['indigo']); fd = ImageDraw.Draw(fill)
for k in range(0, 60):
    y0 = 40 + k*18
    pts = [(x*S, (y0 + 30*math.sin(x/90 + k*0.35))*S) for x in range(0, 1210, 6)]
    fd.line(pts, fill=c['skyb'] if k % 2 else c['prussian'], width=3*S)
im.paste(fill, (0, 0), m)
sea(im, 520, c['teal'], c['skyb'], gap=16)
finish(im, OUT + 'wed_02.jpg', seed=32)

# 03 & · Abril Fatface — a teal ampersand with a curling wave breaking through it
im = canvas(c['clay'], c['paper'], 1)
f = font('AbrilFatface', 470)
text(im, (360, 470), '&', f, c['teal'], anchor='ms')
sea(im, 500, c['indigo'], c['skyb'], gap=18)
wave(im, 720, 170, 0.44, c['prussian'], c['skyb'], c['paper'], seed=81)
front_sea(im, 540, c['indigo'], c['prussian'], foam=c['skyb'], seed=8)
disc(im, 1080, 110, 36, c['wine'])
finish(im, OUT + 'wed_03.jpg', seed=33)

# 04 Glyph grid · Young Serif — a specimen sheet of coloured tiles, one letter each
im = canvas(c['paper'])
cols = [c['prussian'], c['teal'], c['plum'], c['pine'], c['wine'], c['indigo'],
        c['skyb'], c['moss'], c['mauve'], c['navy'], c['ochre'], c['deep']]
letters = 'agrekfmotyws'
f = font('YoungSerif', 150)
tw, th, gap, x0, y0 = 176, 236, 12, 60, 50
d = ImageDraw.Draw(im)
for i, ch in enumerate(letters):
    r, q = divmod(i, 6)
    x = x0 + q*(tw + gap); y = y0 + r*(th + gap)
    d.rectangle([x*S, y*S, (x+tw)*S, (y+th)*S], fill=cols[i])
    light = cols[i] in (c['skyb'], c['mauve'], c['ochre'])
    text(im, (x + tw/2, y + th*0.7), ch, f, c['ink'] if light else c['paper'], anchor='ms')
    hline(im, y + th*0.7, mixc(cols[i], c['paper'], 0.35), x + 10, x + tw - 10, 1)
finish(im, OUT + 'wed_04.jpg', seed=34)

# 05 Blueprint g · Playfair Display — outline letter with construction lines on navy
im = canvas(c['navy'], c['indigo'], 1)
d = ImageDraw.Draw(im)
for x in range(0, 1200, 40): d.line([(x*S, 0), (x*S, H)], fill=mixc(c['navy'], c['prussian'], 0.45), width=S)
for y in range(0, 600, 40): d.line([(0, y*S), (W, y*S)], fill=mixc(c['navy'], c['prussian'], 0.45), width=S)
f = font('PlayfairDisplay', 520, wght=700)
base = 400
text(im, (560, base), 'g', f, c['navy'], anchor='ms', stroke_width=3*S, stroke_fill=c['foamb'])
bb = d.textbbox((560*S, base*S), 'g', font=f, anchor='ms')
xh = font('PlayfairDisplay', 520, wght=700).getbbox('x', anchor='ls')
xh_y = base + xh[1]/S
for y, lab in [(base, 'baseline'), (xh_y, 'x-height'), (bb[3]/S, 'descender')]:
    hline(im, y, c['skyb'], 120, 1080, 1.5)
    text(im, (1085, y - 6), lab, font('SourceSerif4', 20, wght=400), c['skyb'], anchor='ls')
cx = (bb[0] + bb[2]) / 2 / S
d.ellipse([(cx-130)*S, (xh_y+4)*S, (cx+120)*S, (base+10)*S], outline=c['ochre'], width=2*S)
disc(im, 940, 120, 34, c['clay'])
finish(im, OUT + 'wed_05.jpg', seed=35)

# 06 Letter stack · Instrument Serif, Space Grotesk, Syne — three pairs, three voices, wave rules between
im = canvas(c['mist'], c['paper'], 1)
rows = [('Rr', font('InstrumentSerif', 210), c['indigo'], 'Instrument Serif'),
        ('Gg', font('SpaceGrotesk', 170, wght=700), c['teal'], 'Space Grotesk'),
        ('Qq', font('Syne', 160, wght=800), c['wine'], 'Syne')]
lab = font('SourceSerif4', 22, wght=600)
for i, (s_, f_, col, name) in enumerate(rows):
    y = 165 + i*172
    text(im, (80, y), s_, f_, col, anchor='ls')
    text(im, (1120, y - 10), name, lab, c['ink'], anchor='rs')
    if i < 2:
        pts = [(x*S, (y + 22 + 6*math.sin(x/22))*S) for x in range(60, 1141, 3)]
        ImageDraw.Draw(im).line(pts, fill=c['skyb'], width=2*S)
finish(im, OUT + 'wed_06.jpg', seed=36)

# 07 Moon o · Fraunces — the letter o as a moon rising over a woodblock sea
im = canvas(c['navy'], c['prussian'], 1.2)
stars(im, 70, 380, c['paper'], seed=37, avoid=(600, 230, 170))
f = font('Fraunces', 480, wght=800, opsz=144, soft=100)
glow(im, 600, 250, 230, c['skyb'], 0.25)
text(im, (600, 420), 'o', f, c['clay'], anchor='ms')
sea(im, 420, c['indigo'], c['prussian'], gap=16)
d = ImageDraw.Draw(im)
rng = np.random.default_rng(7)
for k in range(10):
    y = 430 + k*12; w = 220 - k*14
    d.rounded_rectangle([(600 - w/2 + rng.normal(0, 10))*S, y*S, (600 + w/2)*S, (y+4)*S], radius=2*S, fill=c['clay'] if k < 6 else c['mauve'])
wave(im, -60, 300, 0.34, c['prussian'], c['skyb'], c['paper'], seed=82)
wave(im, 960, 340, 0.28, c['teal'], c['foamb'], c['paper'], seed=83)
front_sea(im, 545, c['navy'], c['prussian'], foam=c['skyb'], seed=9)
finish(im, OUT + 'wed_07.jpg', seed=37)

# 08 Hamburgefonstiv · Bricolage Grotesque — the classic specimen word across three weights
im = canvas(c['teal'], mixc(c['teal'], c['pine'], 0.6), 1)
for i, (wt, sz, col) in enumerate([(800, 124, c['paper']), (500, 88, c['foamb']), (300, 60, c['skyb'])]):
    f = font('BricolageGrotesque', sz, wght=wt, opsz=96, wdth=100)
    y = [190, 330, 430][i]
    text(im, (70, y), 'Hamburgefonstiv', f, col, anchor='ls')
    text(im, (1130, y - 4), str(wt), font('SourceSerif4', 20, wght=600), c['mist'], anchor='rs')
seigaiha(im, 500, [c['indigo'], c['prussian']], r=26, line=mixc(c['teal'], c['pine'], 0.6))
finish(im, OUT + 'wed_08.jpg', seed=38)
print('done')

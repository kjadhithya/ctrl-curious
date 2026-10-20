"""Wednesday · Type specimen — two more hero options (09, 10), same style as make.py. Not in the rotation yet."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
OUT = '/home/claude/ctrl-curious/assets/explore/wed_more/'
os.makedirs(OUT, exist_ok=True)
c = C
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
def hline(im, y, col, x0=0, x1=1200, w=1):
    ImageDraw.Draw(im).line([(x0*S, y*S), (x1*S, y*S)], fill=col, width=max(1, int(w*S)))
def vline(im, x, y0, y1, col, w=1):
    ImageDraw.Draw(im).line([(x*S, y0*S), (x*S, y1*S)], fill=col, width=max(1, int(w*S)))

# 09 Kerning · Syne — the pair AV tucked together, kern bracket and value, sea at the foot
im = canvas(c['ochre'], mixc(c['ochre'], c['clay'], 0.6), 1)
f = font('Syne', 330, wght=800)
base = 430
d = ImageDraw.Draw(im)
wA = d.textlength('A', font=f) / S
kern = -70
total = wA + kern + d.textlength('V', font=f) / S
x0 = 600 - total / 2
text(im, (x0, base), 'A', f, c['indigo'], anchor='ls')
text(im, (x0 + wA + kern, base), 'V', f, c['wine'], anchor='ls')
hline(im, base, mixc(c['ochre'], c['ink'], 0.35), 60, 1140, 1.5)
kx0, kx1 = x0 + wA + kern, x0 + wA
for x in (kx0, kx1): vline(im, x, 120, base + 14, c['ink'], 1.5)
hline(im, 128, c['ink'], kx0, kx1, 1.5)
lab = font('SourceSerif4', 24, wght=600)
text(im, ((kx0 + kx1) / 2, 112), '−70', lab, c['ink'], anchor='ms')
sea(im, 470, c['teal'], c['foamb'], gap=16)
finish(im, OUT + 'wed_09.jpg', seed=39)

# 10 Type scale · DM Serif Display — Aa rising in size like a swell building, sizes marked below
im = canvas(c['mist'], c['paper'], 1)
sizes = [24, 36, 54, 80, 120, 180]
cols = [c['skyb'], c['prussian'], c['teal'], c['indigo'], c['plum'], c['wine']]
base = 400
x = 70
lab = font('SourceSerif4', 18, wght=600)
d = ImageDraw.Draw(im)
for sz, col in zip(sizes, cols):
    f = font('DMSerifDisplay', sz * 1.25)
    w_ = d.textlength('Aa', font=f) / S
    text(im, (x, base), 'Aa', f, col, anchor='ls')
    text(im, (x + w_ / 2, base + 34), f'{sz}', lab, c['ink'], anchor='ms')
    x += w_ + 34
hline(im, base, c['skyb'], 60, 1140, 1.5)
disc(im, 1090, 110, 40, c['ochre'])
front_sea(im, 470, c['indigo'], c['prussian'], foam=c['skyb'], seed=10)
finish(im, OUT + 'wed_10.jpg', seed=40)
print('done')

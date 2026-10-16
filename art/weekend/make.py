"""Friday sign-off art for the email (1200 x 420): bunting, a low sun and a little sailboat
heading out over wave scales, with "The weekend’s here." Same grainy woodblock style."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 420 * lib.S
from lib import *
H = lib.H
c = C
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
OUT = '/home/claude/ctrl-curious/assets/email/'

im = canvas(c['paper'], mixc(c['clay'], c['ochre'], 0.35), 1.4)
glow(im, 905, 250, 210, c['ochre'], 0.35)
disc(im, 905, 250, 92, mixc(c['ochre'], c['paper'], 0.15))
d = ImageDraw.Draw(im)
# bunting across the top
cols = [c['wine'], c['teal'], c['ochre'], c['plum'], c['skyb'], c['moss']]
for row, (y0, sag, off, step) in enumerate([(-6, 46, 0, 76), (30, 38, 3, 92)]):
    pts = [(x, y0 + sag*math.sin(math.pi*x/1200)) for x in range(-20, 1230, 10)]
    d.line([(px*S, py*S) for px, py in pts], fill=c['ink'], width=2*S)
    for k, x in enumerate(range(26 + row*38, 1200, step)):
        y = y0 + sag*math.sin(math.pi*x/1200)
        d.polygon([((x-16)*S, y*S), ((x+16)*S, y*S), (x*S, (y+32)*S)], fill=cols[(k + off) % len(cols)])
birds(im, [(700, 150), (728, 136), (752, 158)], c['ink'], size=9)
# sea of wave scales
seigaiha(im, 318, [c['teal'], c['prussian']], r=20, line=c['navy'])
# a small sailboat sitting on the first row of scales
boat(im, 760, 312, 110, c['wine'])
d = ImageDraw.Draw(im)
d.line([(815*S, 300*S), (815*S, 214*S)], fill=c['ink'], width=3*S)
d.polygon([(819*S, 220*S), (819*S, 296*S), (870*S, 296*S)], fill=c['paper'])
d.polygon([(811*S, 228*S), (811*S, 296*S), (772*S, 296*S)], fill=c['mauve'])
d.polygon([(815*S, 214*S), (836*S, 220*S), (815*S, 226*S)], fill=c['ochre'])
# words
text(im, (64, 210), "The weekend’s here.", font('SourceSerif4', 52, wght=650, opsz=40), c['ink'])
text(im, (66, 254), "Rest up. See you on Monday.", font('SourceSerif4', 24, wght=420, opsz=20), mixc(c['ink'], c['paper'], 0.25))

small = im.resize((1200, 420), Image.LANCZOS)
a = np.asarray(small, dtype=float) + np.random.default_rng(23).normal(0, 12, (420, 1200, 1))
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(OUT + 'weekend_signoff.jpg', quality=86)
print('weekend_signoff.jpg')

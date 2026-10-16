"""Friday footer art (1200 x 640): a bigger version of the weekend sign-off that replaces the
usual footer art on Fridays. Bunting, a low sun, a sailboat over wave scales, large words."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 640 * lib.S
from lib import *
H = lib.H
c = C
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
OUT = '/home/claude/ctrl-curious/assets/email/'

im = canvas(c['paper'], mixc(c['clay'], c['ochre'], 0.35), 1.4)
glow(im, 930, 420, 280, c['ochre'], 0.35)
disc(im, 930, 420, 130, mixc(c['ochre'], c['paper'], 0.15))
d = ImageDraw.Draw(im)
cols = [c['wine'], c['teal'], c['ochre'], c['plum'], c['skyb'], c['moss']]
for row, (y0, sag, off, step) in enumerate([(-8, 60, 0, 92), (38, 50, 3, 110)]):
    pts = [(x, y0 + sag*math.sin(math.pi*x/1200)) for x in range(-20, 1230, 10)]
    d.line([(px*S, py*S) for px, py in pts], fill=c['ink'], width=3*S)
    for k, x in enumerate(range(30 + row*46, 1200, step)):
        y = y0 + sag*math.sin(math.pi*x/1200)
        d.polygon([((x-21)*S, y*S), ((x+21)*S, y*S), (x*S, (y+42)*S)], fill=cols[(k + off) % len(cols)])
birds(im, [(690, 230), (726, 212), (758, 240)], c['ink'], size=12)
seigaiha(im, 500, [c['teal'], c['prussian']], r=24, line=c['navy'])
boat(im, 740, 494, 150, c['wine'])
d = ImageDraw.Draw(im)
d.line([(815*S, 480*S), (815*S, 360*S)], fill=c['ink'], width=4*S)
d.polygon([(820*S, 368*S), (820*S, 474*S), (892*S, 474*S)], fill=c['paper'])
d.polygon([(810*S, 380*S), (810*S, 474*S), (756*S, 474*S)], fill=c['mauve'])
d.polygon([(815*S, 360*S), (844*S, 368*S), (815*S, 376*S)], fill=c['ochre'])
text(im, (60, 330), "The weekend’s here.", font('SourceSerif4', 86, wght=650, opsz=60), c['ink'])
text(im, (64, 400), "Rest up. See you on Monday.", font('SourceSerif4', 38, wght=420, opsz=30), mixc(c['ink'], c['paper'], 0.25))

small = im.resize((1200, 640), Image.LANCZOS)
a = np.asarray(small, dtype=float) + np.random.default_rng(23).normal(0, 12, (640, 1200, 1))
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(OUT + 'weekend_footer.jpg', quality=86)
print('weekend_footer.jpg')

"""Four celebratory hero images for the welcome email (1200 x 600), in the woodblock style."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
c = C
OUT = '/home/claude/ctrl-curious/assets/email/welcome/'
os.makedirs(OUT, exist_ok=True)
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))


def firework(im, cx, cy, r, col, tip, n=18, seed=0):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(im)
    for k in range(n):
        a = 2*math.pi*k/n + rng.normal(0, .04)
        r0, r1 = r*0.28, r*(0.85 + 0.15*rng.random())
        p0 = (cx + math.cos(a)*r0, cy + math.sin(a)*r0); p1 = (cx + math.cos(a)*r1, cy + math.sin(a)*r1)
        d.line([(p0[0]*S, p0[1]*S), (p1[0]*S, p1[1]*S)], fill=col, width=3*S)
        d.ellipse([(p1[0]-4)*S, (p1[1]-4)*S, (p1[0]+4)*S, (p1[1]+4)*S], fill=tip)
    for k in range(n):
        a = 2*math.pi*(k+.5)/n; rr = r*0.55
        x, y = cx + math.cos(a)*rr, cy + math.sin(a)*rr
        d.ellipse([(x-2.5)*S, (y-2.5)*S, (x+2.5)*S, (y+2.5)*S], fill=tip)


def confetti(im, n, box, cols, seed=1, size=(6, 14)):
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        w, h = rng.uniform(*size), rng.uniform(size[0]*0.45, size[0]*0.8)
        ang = rng.uniform(0, math.pi)
        col = cols[rng.integers(len(cols))]
        pts = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        pts = [((x + px*math.cos(ang) - py*math.sin(ang))*S, (y + px*math.sin(ang) + py*math.cos(ang))*S) for px, py in pts]
        if rng.random() < 0.25:
            r = w*0.35; ImageDraw.Draw(im).ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=col)
        else:
            ImageDraw.Draw(im).polygon(pts, fill=col)


def swell(im, base, cols, lines):
    d = ImageDraw.Draw(im)
    for i, col in enumerate(cols):
        y0 = base + i*24
        top = [(x*S, (y0 + math.sin(x/(90 - i*6) + i) * (14 - i))*S) for x in range(0, 1210, 6)]
        d.polygon(top + [(W, H), (0, H)], fill=col)
        lt = [(x*S, (y0 + 9 + math.sin(x/(90 - i*6) + i) * (14 - i))*S) for x in range(0, 1210, 6)]
        d.line(lt, fill=lines[i % len(lines)], width=2*S)


# A · Fireworks over the night sea
im = canvas(c['navy'], c['indigo'], 1.2)
stars(im, 60, 330, c['paper'], seed=4)
for (x, y, r, col, tip, s) in [(330, 170, 110, c['ochre'], c['paper'], 1), (720, 120, 80, c['mauve'], c['paper'], 2),
                               (960, 230, 120, c['skyb'], c['mist'], 3), (560, 300, 60, c['wine'], c['mauve'], 4)]:
    glow(im, x, y, r*0.9, col, 0.22)
    firework(im, x, y, r, col, tip, seed=s)
swell(im, 430, [c['prussian'], c['teal'], c['indigo'], c['pine'], c['navy']], [c['skyb'], c['mauve']])
finish(im, OUT + 'welcome_fireworks.jpg', seed=11)

# B · Confetti wave: the great wave throwing palette confetti instead of foam
im = canvas(c['paper'], c['clay'], 2)
disc(im, 1040, 120, 46, c['wine'])
confetti(im, 260, (180, 30, 1180, 420), [c['wine'], c['plum'], c['ochre'], c['teal'], c['skyb'], c['mauve'], c['moss']], seed=7)
sea(im, 470, c['navy'], c['prussian'], gap=16)
wave(im, 0, 30, 0.62, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True, parallel=True)
front_sea(im, 500, c['navy'], c['prussian'], foam=c['skyb'], seed=3)
finish(im, OUT + 'welcome_confetti.jpg', seed=12)

# C · Lanterns rising at dusk over the water
im = canvas(mixc(c['plum'], c['ink'], 0.55), mixc(c['wine'], c['plum'], 0.35), 1.1)
stars(im, 40, 260, c['paper'], seed=9)
rng = np.random.default_rng(5)
d = ImageDraw.Draw(im)
for k in range(14):
    x = 120 + k*75 + rng.normal(0, 18); y = 70 + rng.uniform(0, 300); s_ = rng.uniform(0.6, 1.25)
    glow(im, x, y, 46*s_, c['ochre'], 0.35)
    w0, w1, h = 26*s_, 18*s_, 40*s_
    d = ImageDraw.Draw(im)
    d.polygon([((x-w0/2)*S, (y-h/2)*S), ((x+w0/2)*S, (y-h/2)*S), ((x+w1/2)*S, (y+h/2)*S), ((x-w1/2)*S, (y+h/2)*S)], fill=mixc(c['ochre'], c['paper'], 0.25))
    d.rectangle([((x-w1/2)*S, (y+h/2-4*s_)*S), ((x+w1/2)*S, (y+h/2)*S)], fill=c['wine'])
sea(im, 440, mixc(c['wine'], c['ink'], 0.6))
seigaiha(im, 470, [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=20, line=mixc(c['wine'], c['ink'], 0.7))
finish(im, OUT + 'welcome_lanterns.jpg', seed=13)

# D · Bunting over a little boat sailing out on the swell
im = canvas(c['paper'], c['clay'], 2)
disc(im, 980, 190, 70, c['ochre'])
d = ImageDraw.Draw(im)
cols = [c['wine'], c['teal'], c['ochre'], c['plum'], c['skyb'], c['moss']]
for row, (y0, sag, off) in enumerate([(40, 70, 0), (95, 55, 3)]):
    pts = [(x, y0 + sag*math.sin(math.pi*x/1200)) for x in range(-20, 1230, 10)]
    d.line([(px*S, py*S) for px, py in pts], fill=c['ink'], width=2*S)
    for k, x in enumerate(range(30 + row*40, 1200, 80)):
        y = y0 + sag*math.sin(math.pi*x/1200)
        d.polygon([((x-18)*S, y*S), ((x+18)*S, y*S), (x*S, (y+36)*S)], fill=cols[(k + off) % len(cols)])
swell(im, 430, [c['skyb'], c['prussian'], c['teal'], c['indigo'], c['navy']], [c['foamb'], c['mauve']])
boat(im, 470, 420, 150, c['wine'])
d = ImageDraw.Draw(im)
d.line([(545*S, 402*S), (545*S, 300*S)], fill=c['ink'], width=3*S)
d.polygon([(549*S, 305*S), (549*S, 395*S), (610*S, 395*S)], fill=c['paper'])
d.polygon([(541*S, 315*S), (541*S, 395*S), (495*S, 395*S)], fill=c['mauve'])
d.polygon([(545*S, 300*S), (570*S, 307*S), (545*S, 314*S)], fill=c['ochre'])
swell(im, 470, [c['teal'], c['indigo'], c['navy']], [c['foamb'], c['mauve']])
finish(im, OUT + 'welcome_bunting.jpg', seed=14)
print('done')

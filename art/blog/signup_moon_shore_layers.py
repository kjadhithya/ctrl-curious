"""Moon shore signup band (option 9) split into layers so the wave scales can drift on the website:
  signup_moon_shore_bg.jpg   sky, stars and moon, with a dark shore fill where the scales sit
  signup_moon_shore_waves.png  a seamless, horizontally tiling strip of the wave scales (transparent above the arcs)
The artwork matches signup_moon_shore.jpg (same colours, moon, stars and grain)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 384 * lib.S
from lib import *
H = lib.H
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/'
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))

SCALES = [c['plum'], mixc(c['wine'], c['ink'], 0.4)]
LINE = mixc(c['wine'], c['ink'], 0.7)
R, Y0 = 18, 340

def save(im, name, seed):
    small = im.resize((1500, 480), Image.LANCZOS)
    a = np.asarray(small, dtype=float) + np.random.default_rng(seed).normal(0, 17, (480, 1500, 1))
    Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 614), Image.BICUBIC).save(OUT + name, quality=88)
    print(name)

# Background: identical to option 9 up to the scales, then a solid shore fill behind them
MX, MY, MR = 806, 123, 223
im = canvas(mixc(c['wine'], c['ink'], 0.55), mixc(c['wine'], c['ink'], 0.25), 1)
stars(im, 60, 330, c['paper'], seed=22, avoid=(MX, MY, MR + 10))
rng9 = np.random.default_rng(7)
def blur_noise9(r):
    n = Image.fromarray((rng9.random((H, W)) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(r*S))
    a = np.asarray(n, dtype=float); return (a - a.min()) / (a.max() - a.min() + 1e-6)
n = 0.5*blur_noise9(31) + 0.3*blur_noise9(10) + 0.2*blur_noise9(3.4)
moon_mauve = np.array(hx('E3B9A6'), float); moon_paper = np.array(hx('F5EEE3'), float)
tone = moon_mauve[None, None]*(1 - (n*0.6)[..., None]) + moon_paper[None, None]*(n*0.6)[..., None]
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([(MX-MR)*S, (MY-MR)*S, (MX+MR)*S, (MY+MR)*S], fill=255)
im.paste(Image.fromarray(np.clip(tone, 0, 255).astype('uint8')), (0, 0), mask)
ImageDraw.Draw(im).rectangle([0, (Y0 + 6)*S, W, H], fill=LINE)
save(im, 'signup_moon_shore_bg.jpg', 39)

# Wave strip: 10 periods wide (one period = 2R units), from the top of the first arcs to the bottom
PER = 10 * 2 * R
TOP = Y0 - R
HU = 384 - TOP                     # strip height in units
K = 10                             # supersample: px per unit while drawing
strip = Image.new('RGBA', (PER*K, HU*K), (0, 0, 0, 0))
d = ImageDraw.Draw(strip)
row, y = 0, Y0
while y < 384 + R:
    off = R if row % 2 else 0
    for x in range(-2*R + off, PER + 2*R, 2*R):
        for k, rr in enumerate(np.linspace(R, R*0.2, 4)):
            col = SCALES[(k + row) % len(SCALES)] if k % 2 == 0 else LINE
            d.ellipse([(x - rr)*K, (y - TOP - rr)*K, (x + rr)*K, (y - TOP + rr)*K], fill=col + (255,))
    y += R*0.5; row += 1
# grain at the same scale as the band (1.25 px per unit, sd 17), then shown at 2.5 px per unit
small = strip.resize((int(PER*1.25), int(HU*1.25)), Image.LANCZOS)
a = np.asarray(small, dtype=float)
rgb = a[..., :3] + np.random.default_rng(41).normal(0, 17, a.shape[:2])[..., None]
out = np.dstack([np.clip(rgb, 0, 255), a[..., 3:]]).astype('uint8')
Image.fromarray(out, 'RGBA').resize((PER*5//2, HU*5//2), Image.BICUBIC).save(OUT + 'signup_moon_shore_waves.png', optimize=True)
print('signup_moon_shore_waves.png', PER*5//2, HU*5//2)

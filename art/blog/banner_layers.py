"""Banner 7b split into layers so the website hero can animate the wave and the swell.
Same drawing as banners_tall.py option 7b, rendered as:
  bg.webp        sky, wine sun, plum mountain and every swell band (what shows behind moving parts)
  wave.webp      the great wave on transparency
  band1..6.webp  each front swell band on transparency (drawn over the wave base, front-most last)
All layers are mirrored like the original and share its 1920 x 1080 frame."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 675 * lib.S
from lib import *
from PIL import ImageOps
H = lib.H
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/hero/'
os.makedirs(OUT, exist_ok=True)
cols = [c['skyb'], c['prussian'], c['teal'], c['pine'], c['indigo'], c['moss'], c['navy']]
BASE = 430 + 115


def band(im, i):
    d = ImageDraw.Draw(im)
    Hc = im.size[1]
    col = cols[i]
    y0 = BASE + i * 26
    top = [(x * S, (y0 + math.sin(x / (90 - i * 6) + i) * (18 - i * 1.5)) * S) for x in range(0, 1210, 6)]
    d.polygon(top + [(W, Hc), (0, Hc)], fill=col)
    lt = [(x * S, (y0 + 10 + math.sin(x / (90 - i * 6) + i) * (18 - i * 1.5)) * S) for x in range(0, 1210, 6)]
    d.line(lt, fill=c['foamb'] if i % 2 == 0 else c['mauve'], width=2 * S)


def save(im, name, seed, amt=14, alpha=False, size=(1920, 1080)):
    im = ImageOps.mirror(im)
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert('RGBA' if alpha else 'RGB'), dtype=float)
    a[..., :3] += rng.normal(0, amt, a.shape[:2])[..., None]
    out = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    if alpha:  # resize premultiplied so edges don't pick up dark fringes
        out = out.convert('RGBa').resize(size, Image.LANCZOS).convert('RGBA')
    else:
        out = out.resize(size, Image.LANCZOS)
    out.save(OUT + name, quality=82, method=6)
    print(name, os.path.getsize(OUT + name) // 1024, 'KB')


# background: the full static scene minus the wave
im = canvas(c['paper'], c['clay'], 2)
disc(im, 1200 - 1110, 160, 50, c['wine'])
mountain(im, 350, 570, 460, 425, 575, c['mauve'], snow=c['paper'])
for i in range(len(cols)):
    band(im, i)
save(im, 'bg.webp', 7)

# the wave alone
im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
wave(im, 10, 110, 0.6, c['indigo'], c['skyb'], c['mist'], seed=5, soft=True, parallel=True)
save(im, 'wave.webp', 8, alpha=True)

# front bands, one per layer
# each band runs 60px past the bottom of the frame, so lifting it never opens a gap underneath
EXT = 60
for i in range(1, len(cols)):
    im = Image.new('RGBA', (W, H + EXT * S), (0, 0, 0, 0))
    band(im, i)
    save(im, f'band{i}.webp', 10 + i, alpha=True, size=(1920, round(1080 * (H + EXT * S) / H)))

"""Signup band options 8 and 9 (1920 x 614), text sits on the left, art on the right.
8 Ochre dawn: a plum night lifting into an ochre glow, a pale sun rising out of the wave-scale sea.
9 Moon shore: option 2's wine night sky and stars, the original blush full moon, and the
  wine sunset's horizon, reflection and wave-scale shore underneath."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib
lib.H = 384 * lib.S
from lib import *
H = lib.H
c = C
OUT = '/home/claude/ctrl-curious/assets/blog/'
def mixc(a, b, t): return tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))

def fbm(seed):
    rng = np.random.default_rng(seed)
    def blur_noise(r):
        n = Image.fromarray((rng.random((H, W)) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(r*S))
        a = np.asarray(n, dtype=float); return (a - a.min()) / (a.max() - a.min() + 1e-6)
    return 0.5*blur_noise(18) + 0.3*blur_noise(6) + 0.2*blur_noise(2)

def save(im, name, seed):
    small = im.resize((1500, 480), Image.LANCZOS)
    a = np.asarray(small, dtype=float) + np.random.default_rng(seed).normal(0, 17, (480, 1500, 1))
    Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 614), Image.BICUBIC).save(OUT + name, quality=88)
    print(name)

def shore(im, bar_col, bar_fade, x=900, w0=170, scale_cols=None, line=None):
    """The wine sunset's lower half: dark horizon water, short reflection bars, wave-scale shore."""
    d = ImageDraw.Draw(im)
    d.rectangle([0, 290*S, W, H], fill=mixc(c['wine'], c['ink'], 0.7))
    rng = np.random.default_rng(5)
    for k in range(5):
        y = 298 + k*9; w = w0 - k*(w0 // 7)
        d.rounded_rectangle([(x - w/2 + rng.normal(0, 6))*S, y*S, (x + w/2)*S, (y+3)*S], radius=2*S,
                            fill=bar_col if k < 3 else bar_fade)
    seigaiha(im, 340, scale_cols or [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=18,
             line=line or mixc(c['wine'], c['ink'], 0.7))

# 8 Ochre dawn
yy, xx = np.mgrid[0:H, 0:W].astype(float)
t = (yy / (290*S)).clip(0, 1) ** 1.6                       # 0 at top, 1 at the horizon
top = np.array(mixc(c['ink'], c['plum'], 0.35), float)
low = np.array(mixc(c['wine'], c['plum'], 0.35), float)
sky = top[None, None]*(1 - t[..., None]) + low[None, None]*t[..., None]
# ochre glow around the rising sun, kept to the right so the text side stays dark
r = np.hypot((xx - 900*S) / (520*S), (yy - 300*S) / (300*S))
g = np.clip(1 - r, 0, 1) ** 1.8
sky = sky*(1 - g[..., None]*0.85) + np.array(c['ochre'], float)[None, None]*g[..., None]*0.85
n = fbm(31)[..., None]
sky = sky*(0.94 + 0.12*n)                                   # soft mottling, like the other bands
im = Image.fromarray(np.clip(sky, 0, 255).astype('uint8'))
sun = mixc(c['ochre'], c['paper'], 0.55)
disc(im, 900, 290, 78, sun)
shore(im, sun, mixc(sun, c['wine'], 0.45), w0=150,
      scale_cols=[mixc(c['ochre'], c['wine'], 0.45), mixc(c['wine'], c['ink'], 0.45)])
stars(im, 18, 120, mixc(c['paper'], c['ochre'], 0.3), seed=8, avoid=(900, 290, 260))
save(im, 'signup_ochre_dawn.jpg', 38)

# 9 Moon shore: the original band's big blush moon, placed and sized as it shows in option 6,
# on option 2's wine night, with the wave-scale shore straight below (no water or reflection)
MX, MY, MR = 806, 123, 223
im = canvas(mixc(c['wine'], c['ink'], 0.55), mixc(c['wine'], c['ink'], 0.25), 1)
stars(im, 60, 330, c['paper'], seed=22, avoid=(MX, MY, MR + 10))
rng9 = np.random.default_rng(7)
def blur_noise9(r):
    n = Image.fromarray((rng9.random((H, W)) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(r*S))
    a = np.asarray(n, dtype=float); return (a - a.min()) / (a.max() - a.min() + 1e-6)
n = 0.5*blur_noise9(31) + 0.3*blur_noise9(10) + 0.2*blur_noise9(3.4)   # same mottling scale as the original moon
moon_mauve = np.array(hx('E3B9A6'), float); moon_paper = np.array(hx('F5EEE3'), float)
tone = moon_mauve[None, None]*(1 - (n*0.6)[..., None]) + moon_paper[None, None]*(n*0.6)[..., None]
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([(MX-MR)*S, (MY-MR)*S, (MX+MR)*S, (MY+MR)*S], fill=255)
im.paste(Image.fromarray(np.clip(tone, 0, 255).astype('uint8')), (0, 0), mask)
seigaiha(im, 340, [c['plum'], mixc(c['wine'], c['ink'], 0.4)], r=18, line=mixc(c['wine'], c['ink'], 0.7))
save(im, 'signup_moon_shore.jpg', 39)

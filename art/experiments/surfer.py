"""Experiment: a figure catching the big hero wave. Draws over the current hero composite."""
import math
from PIL import Image, ImageDraw
import numpy as np
A = '/home/claude/ctrl-curious/assets/blog/hero/'
OUT = '/home/claude/ctrl-curious/assets/blog/experiments/'
import os; os.makedirs(OUT, exist_ok=True)
INK=(46,31,37); WINE=(138,46,59); OCHRE=(200,144,47); PAPER=(244,238,232); CLAY=(217,195,183); MIST=(201,214,220); FOAM=(214,226,230); PLUM=(126,75,107)

def base():
    bg = Image.open(A + 'bg.webp').convert('RGBA')
    for f in ['wave'] + ['band%d' % i for i in range(1, 7)]:
        bg.alpha_composite(Image.open(A + f + '.webp').convert('RGBA').crop((0, 0, 1920, 1080)))
    return bg

K = 4  # supersample
def layer():
    return Image.new('RGBA', (1920*K, 1080*K), (0, 0, 0, 0))

def T(pts, cx, cy, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [((cx + (x*ca - y*sa)*s)*K, (cy + (x*sa + y*ca)*s)*K) for x, y in pts]

def limb(d, a, b, w, col):
    d.line([a, b], fill=col, width=int(w*K)); 
    for p in (a, b): d.ellipse([p[0]-w*K/2, p[1]-w*K/2, p[0]+w*K/2, p[1]+w*K/2], fill=col)

def surfer(im, cx, cy, s, ang, flip=False):
    """Standing surfer on a board; local units ~ 1 = 1px at s=1. Board centred at (0,0), rider above."""
    L = layer(); d = ImageDraw.Draw(L)
    f = -1 if flip else 1
    P = lambda x, y: T([(x*f, y)], cx, cy, s, ang)[0]
    # spray behind the board
    rng = np.random.default_rng(3)
    for k in range(26):
        x = (70 + rng.uniform(0, 70))*f; y = rng.uniform(-30, 8); r = rng.uniform(2, 6)
        p = P(x, y); d.ellipse([p[0]-r*s*K, p[1]-r*s*K, p[0]+r*s*K, p[1]+r*s*K], fill=FOAM)
    # board
    board = [(-78, 0), (-60, -7), (40, -8), (72, -3), (78, 2), (60, 7), (-60, 6)]
    d.polygon([P(x, y) for x, y in board], fill=OCHRE)
    d.line([P(-62, 0), P(66, -1)], fill=PAPER, width=int(2.2*s*K))
    # legs (bent, surf stance)
    hip = (6, -58)
    limb(d, P(-28, -7), P(-22, -32), 9*s, INK); limb(d, P(-22, -32), P(*hip), 9*s, INK)
    limb(d, P(34, -7), P(30, -30), 9*s, INK); limb(d, P(30, -30), P(*hip), 9*s, INK)
    # torso leaning forward
    sh = (-8, -96)
    limb(d, P(*hip), P(*sh), 15*s, WINE)
    # arms out for balance
    limb(d, P(*sh), P(-40, -92), 7*s, WINE); limb(d, P(-40, -92), P(-66, -80), 6*s, CLAY)
    limb(d, P(*sh), P(26, -104), 7*s, WINE); limb(d, P(26, -104), P(54, -112), 6*s, CLAY)
    # head with hair
    hp = P(-14, -116); r = 10*s*K
    d.ellipse([hp[0]-r, hp[1]-r, hp[0]+r, hp[1]+r], fill=CLAY)
    hh = P(-10, -121); d.ellipse([hh[0]-r*0.95, hh[1]-r*0.75, hh[0]+r*0.95, hh[1]+r*0.55], fill=INK)
    im.alpha_composite(L.resize((1920, 1080), Image.LANCZOS))

def paddler(im, cx, cy, s, ang, flip=False):
    """Figure lying on a board, paddling towards the wave."""
    L = layer(); d = ImageDraw.Draw(L)
    f = -1 if flip else 1
    P = lambda x, y: T([(x*f, y)], cx, cy, s, ang)[0]
    board = [(-80, 0), (-60, -6), (40, -7), (74, -2), (80, 2), (60, 7), (-60, 6)]
    d.polygon([P(x, y) for x, y in board], fill=OCHRE)
    d.line([P(-62, 0), P(66, -1)], fill=PAPER, width=int(2*s*K))
    limb(d, P(-56, -10), P(-10, -14), 9*s, INK)      # legs
    limb(d, P(-10, -14), P(34, -16), 15*s, WINE)     # torso
    hp = P(48, -22); r = 10*s*K
    d.ellipse([hp[0]-r, hp[1]-r, hp[0]+r, hp[1]+r], fill=CLAY)
    hh = P(44, -25); d.ellipse([hh[0]-r*0.9, hh[1]-r*0.8, hh[0]+r*0.7, hh[1]+r*0.5], fill=INK)
    limb(d, P(30, -14), P(52, 4), 6*s, CLAY)          # paddling arm, in the water
    limb(d, P(28, -16), P(10, -38), 6*s, CLAY)        # recovering arm
    rng = np.random.default_rng(5)
    for k in range(12):
        p = P(56 + rng.uniform(-6, 14), 6 + rng.uniform(-4, 4)); rr = rng.uniform(2, 4.5)*s*K
        d.ellipse([p[0]-rr, p[1]-rr, p[0]+rr, p[1]+rr], fill=FOAM)
    im.alpha_composite(L.resize((1920, 1080), Image.LANCZOS))

def grain(im, seed):
    a = np.asarray(im.convert('RGB'), dtype=float) + np.random.default_rng(seed).normal(0, 6, (1080, 1920, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))

# A: riding the face of the big wave, carving down and left
im = base(); surfer(im, 1335, 735, 1.0, math.radians(-28), flip=True)
grain(im, 1).save(OUT + 'hero_surfer_ride.jpg', quality=88)
# B: paddling hard to catch it, in the swell at the foot of the wave
im = base(); paddler(im, 1215, 872, 1.35, math.radians(4), flip=True)
grain(im, 2).save(OUT + 'hero_surfer_paddle.jpg', quality=88)
print('ok')

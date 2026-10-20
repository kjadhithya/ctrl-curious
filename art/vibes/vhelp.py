"""Vibes exploration: 8 trial illustrations in the house style (flat shapes, swell lines, grain),
but about people, tech, FigJam shapes and nature+UI instead of literal waves."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
from PIL import ImageFont
OUT = '/home/claude/ctrl-curious/assets/explore/' + os.environ.get('VIBES_SET', 'vibes_humans') + '/'
os.makedirs(OUT, exist_ok=True)
c = C
FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts', 'Figtree.ttf')

def rr(im, x0, y0, x1, y1, r, col, outline=None, w=0):
    ImageDraw.Draw(im).rounded_rectangle([x0*S, y0*S, x1*S, y1*S], radius=r*S, fill=col, outline=outline, width=w*S)

def poly(im, pts, col):
    ImageDraw.Draw(im).polygon([(x*S, y*S) for x, y in pts], fill=col)

def line(im, pts, col, w=2):
    ImageDraw.Draw(im).line([(x*S, y*S) for x, y in pts], fill=col, width=int(w*S), joint='curve')

def ring(im, cx, cy, r, col, w):
    ImageDraw.Draw(im).ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], outline=col, width=int(w*S))

def clip_stripes(im, shape_fn, body, stripe, gap=16, amp=5, freq=40, w=2, phase=0):
    """Fill a shape with body colour and gentle swell lines, clipped to the shape."""
    mask = Image.new('L', (W, H), 0); shape_fn(ImageDraw.Draw(mask))
    layer = Image.new('RGB', (W, H), body); d = ImageDraw.Draw(layer)
    for k, y0 in enumerate(range(-20, 640, gap)):
        d.line([(x*S, (y0 + math.sin(x/freq + k*0.7 + phase)*amp)*S) for x in range(0, 1210, 5)], fill=stripe, width=w*S)
    im.paste(layer, (0, 0), mask)

def text(im, x, y, s, size, col, weight=600):
    f = ImageFont.truetype(FONT, size*S)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    ImageDraw.Draw(im).text((x*S, y*S), s, font=f, fill=col)

def profile(sx, oy, flip=False):
    """A calm head-and-shoulders profile facing right (or left), as a list of points."""
    pts = np.vstack([
        bez((0, 600), (40, 520), (150, 470), (190, 455)),       # back of shoulder
        bez((190, 455), (215, 445), (205, 400), (175, 370)),    # back of neck to nape
        bez((175, 370), (90, 300), (110, 120), (250, 95)),      # back of head
        bez((250, 95), (360, 75), (420, 160), (405, 215)),      # crown to brow
        bez((405, 215), (402, 232), (440, 262), (432, 278)),    # nose
        bez((432, 278), (425, 290), (412, 292), (412, 300)),    # lips
        bez((412, 300), (418, 318), (400, 330), (398, 345)),    # chin
        bez((398, 345), (360, 360), (310, 365), (300, 400)),    # jaw to throat
        bez((300, 400), (300, 440), (330, 470), (420, 500)),    # front of neck
        bez((420, 500), (480, 520), (520, 560), (530, 600)),    # chest
    ])
    pts = pts * sx
    if flip: pts[:, 0] = -pts[:, 0]
    return pts + np.array(oy)


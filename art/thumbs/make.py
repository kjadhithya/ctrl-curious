"""Thumbnails for the home page's 'The week, by day' cards: one emblem per weekday, in that day's illustration style.
Bold, simple shapes so they read at card size (about 240x120)."""
import sys, os
os.environ['VIBES_SET'] = 'thumbs'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'vibes'))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vhelp import *
import lib
OUT = '/home/claude/ctrl-curious/assets/explore/thumbs/'
os.makedirs(OUT, exist_ok=True)
MIX = lambda a, b, t: tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))

# Monday · Week ahead (nature + UI): the sun rising over the sea, the week's five days as page dots, Monday active
im = canvas(c['ochre'], c['paper'], 0.9)
disc(im, 600, 360, 130, c['wine'])
sea(im, 360, c['teal'], c['foamb'], gap=18, amp=4, freq=34)
rr(im, 380, 470, 820, 530, 30, c['paper'])
for k in range(5):
    x = 430 + k * 85
    if k == 0: rr(im, x - 26, 488, x + 26, 512, 12, c['wine'])
    else: disc(im, x, 500, 11, c['mauve'])
finish(im, OUT + 'thumb_mon.jpg', seed=61)

# Tuesday · Tools (tech): a floating design toolbar over a night sea — cursor, frame, pen, text, hand
im = canvas(c['plum'], c['deep'], 1)
disc(im, 1010, 120, 60, c['wine'])
sea(im, 430, c['navy'], c['prussian'], gap=16, amp=3, freq=30)
rr(im, 186, 216, 1026, 386, 40, c['ink'])
rr(im, 180, 208, 1020, 378, 40, c['navy'])
xs = [270, 410, 550, 690, 830, 950]
rr(im, xs[0] - 52, 240, xs[0] + 52, 346, 22, c['wine'])                 # active tool
cur = [(0, 0), (0, 64), (16, 49), (27, 75), (39, 70), (28, 45), (50, 45)]
poly(im, [(xs[0] - 18 + x, 258 + y) for x, y in cur], c['paper'])
rr(im, xs[1] - 34, 260, xs[1] + 34, 328, 4, None, c['foamb'], 6)        # frame
line(im, [(xs[1] - 46, 276), (xs[1] + 46, 276)], c['foamb'], 5); line(im, [(xs[1] - 46, 312), (xs[1] + 46, 312)], c['foamb'], 5)
line(im, [(xs[1] - 18, 248), (xs[1] - 18, 340)], c['foamb'], 5); line(im, [(xs[1] + 18, 248), (xs[1] + 18, 340)], c['foamb'], 5)
poly(im, [(xs[2], 248), (xs[2] + 26, 300), (xs[2], 340), (xs[2] - 26, 300)], c['foamb'])   # pen nib
disc(im, xs[2], 300, 7, c['navy'])
lib.text(im, (xs[3], 334), 'T', lib.font('SourceSerif4', 96, wght=700), c['foamb'], anchor='ms')   # text
for k, (dx, h) in enumerate([(-24, 46), (-8, 62), (8, 60), (24, 48)]):                       # hand
    rr(im, xs[4] + dx - 7, 300 - h, xs[4] + dx + 7, 320, 7, c['foamb'])
rr(im, xs[4] - 32, 290, xs[4] + 32, 340, 22, c['foamb'])
disc(im, xs[5], 293, 34, c['ochre']); disc(im, xs[5], 293, 20, c['navy'])                  # colour picker
finish(im, OUT + 'thumb_tue.jpg', amt=15, seed=62)

# Wednesday · Type: a single lowercase a with its real metrics, a seigaiha shore
im = canvas(c['plum'], MIX(c['plum'], c['deep'], 0.5), 1)
f = lib.font('Fraunces', 470, wght=650, opsz=144, soft=0)
base = 450
bb = ImageDraw.Draw(im).textbbox((560*S, base*S), 'a', font=f, anchor='ms')
xh = bb[1] / S + 6            # top of the bowl, near the x-height
lab = lib.font('SourceSerif4', 22, wght=600)
for y, name in [(base, 'baseline'), (xh, 'x-height')]:
    ImageDraw.Draw(im).line([(80*S, y*S), (1120*S, y*S)], fill=c['mauve'], width=2*S)
    lib.text(im, (1120, y - 10), name, lab, c['mauve'], anchor='rs')
lib.text(im, (560, base), 'a', f, c['paper'], anchor='ms')
disc(im, 980, 110, 44, c['wine'])
seigaiha(im, 500, [c['prussian'], c['teal']], r=26, line=c['plum'])
finish(im, OUT + 'thumb_wed.jpg', seed=63)

# Thursday · Case study (FigJam): a magnifying glass over a board of stickies, one sticky enlarged inside the lens
im = canvas(c['mist'], c['paper'], 1)
d = ImageDraw.Draw(im)
for x in range(14, 1200, 28):
    for y in range(14, 600, 28):
        d.ellipse([(x-1.6)*S, (y-1.6)*S, (x+1.6)*S, (y+1.6)*S], fill=c['skyb'])
def sticky(x, y, s, col, lc):
    rr(im, x + 6, y + 8, x + s + 6, y + s + 8, 2, c['clay'])
    poly(im, [(x, y), (x + s, y), (x + s, y + s*0.8), (x + s*0.8, y + s), (x, y + s)], col)
    poly(im, [(x + s, y + s*0.8), (x + s*0.8, y + s*0.8), (x + s*0.8, y + s)], tuple(int(v*0.8) for v in col))
    for k in range(3): rr(im, x + s*0.14, y + s*(0.24 + k*0.18), x + s*(0.8 - k*0.16), y + s*(0.24 + k*0.18) + s*0.05, 2, lc)
for (x, y, col, lc) in [(150, 120, c['ochre'], c['deep']), (330, 300, c['mauve'], c['plum']), (900, 110, c['skyb'], c['indigo']), (960, 330, c['ochre'], c['deep'])]:
    sticky(x, y, 130, col, lc)
cx, cy, r = 620, 270, 165
line(im, [(cx + r*0.68, cy + r*0.68), (cx + r*1.32, cy + r*1.42)], c['ink'], 30)
disc(im, cx, cy, r + 16, c['ink']); disc(im, cx, cy, r, c['paper'])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=255)
lens = canvas(c['paper']); sticky_im = im
im2 = lens
def sticky2(img, x, y, s, col, lc):
    rr(img, x + 8, y + 10, x + s + 8, y + s + 10, 3, c['clay'])
    poly(img, [(x, y), (x + s, y), (x + s, y + s*0.8), (x + s*0.8, y + s), (x, y + s)], col)
    poly(img, [(x + s, y + s*0.8), (x + s*0.8, y + s*0.8), (x + s*0.8, y + s)], tuple(int(v*0.8) for v in col))
    for k in range(3): rr(img, x + s*0.14, y + s*(0.24 + k*0.18), x + s*(0.8 - k*0.16), y + s*(0.24 + k*0.18) + s*0.06, 3, lc)
sticky2(lens, cx - 105, cy - 105, 210, c['teal'], c['foamb'])
im.paste(lens, (0, 0), m)
finish(im, OUT + 'thumb_thu.jpg', seed=64)
print('vector thumbs done')

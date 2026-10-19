"""Vibes exploration: 8 trial illustrations in the house style (flat shapes, swell lines, grain),
but about people, tech, FigJam shapes and nature+UI instead of literal waves."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
from PIL import ImageFont
OUT = '/home/claude/ctrl-curious/assets/explore/vibes/'
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

# 1 Humans: two profiles in conversation, swell lines flowing between them, wine sun above
im = canvas(c['paper'], c['clay'], 1.6)
disc(im, 600, 150, 62, c['wine'])
L_ = profile(0.92, (40, 52)); R_ = profile(0.92, (1160, 52), flip=True)
for k in range(9):
    y = 300 + k * 14
    pts = [(x, y + math.sin(x / 34 + k * .6) * 7 * math.sin((x - 400) / 400 * math.pi)) for x in range(400, 801, 4)]
    line(im, pts, [c['teal'], c['prussian'], c['skyb']][k % 3], 2.5)
clip_stripes(im, lambda d: d.polygon([(x*S, y*S) for x, y in L_] + [(40*S, 660*S)], fill=255), c['indigo'], c['prussian'], gap=15)
clip_stripes(im, lambda d: d.polygon([(x*S, y*S) for x, y in R_] + [(1160*S, 660*S)], fill=255), c['plum'], c['deep'], gap=15, phase=2)
finish(im, OUT + 'vibes_01_people_talk.jpg', seed=11)

# 2 Humans: a crowd drawn like seigaiha scales, every arc a pair of shoulders, one person in ochre
im = canvas(c['mist'], c['paper'], 1)
disc(im, 960, 130, 58, c['wine'])
d = ImageDraw.Draw(im)
rows = [(300, c['skyb'], c['prussian']), (375, c['teal'], c['pine']), (450, c['prussian'], c['indigo']), (525, c['pine'], c['teal']), (600, c['indigo'], c['navy'])]
r = 62
for i, (y, body, head) in enumerate(rows):
    off = r if i % 2 else 0
    for j, x in enumerate(range(-2*r + off, 1300, 2*r)):
        hl = (i == 2 and j == 6)
        b_ = c['ochre'] if hl else body; h = c['wine'] if hl else head
        d.ellipse([(x-r)*S, (y-r*0.5)*S, (x+r)*S, (y+r*1.5)*S], fill=b_)
        d.ellipse([(x-r*0.6)*S, (y+r*0.05)*S, (x+r*0.6)*S, (y+r*1.3)*S], outline=c['paper'], width=2*S)
        hr = 24
        d.ellipse([(x-hr)*S, (y-r*0.5-hr*1.75)*S, (x+hr)*S, (y-r*0.5+hr*0.25)*S], fill=h)
finish(im, OUT + 'vibes_02_crowd.jpg', seed=12)

# 3 Tech: an open laptop whose screen holds a sunrise over swell lines
im = canvas(c['clay'], c['paper'], 1)
rr(im, 0, 470, 1200, 600, 0, c['mauve'])
line(im, [(0, 470), (1200, 470)], c['plum'], 2)
rr(im, 330, 110, 870, 455, 22, c['ink'])                       # lid
def screen(dr): dr.rounded_rectangle([352*S, 132*S, 848*S, 433*S], radius=8*S, fill=255)
m = Image.new('L', (W, H), 0); screen(ImageDraw.Draw(m))
scr = canvas(c['ochre'], c['paper'], 0.8)
disc(scr, 600, 330, 70, c['wine'])
sea(scr, 330, c['teal'], c['foamb'], gap=14, amp=3, freq=22)
im.paste(scr, (0, 0), m)
poly(im, [(250, 455), (950, 455), (1010, 492), (190, 492)], c['indigo'])   # base
rr(im, 520, 455, 680, 466, 5, c['prussian'])                               # hinge notch
for k in range(3):                                                           # key rows as swell texture
    y = 466 + k * 8
    line(im, [(x, y + math.sin(x / 14 + k) * 1.2) for x in range(262 - k*16, 940 + k*16, 4)], c['skyb'], 1.6)
poly(im, [(190, 492), (1010, 492), (1004, 502), (196, 502)], c['navy'])
finish(im, OUT + 'vibes_03_laptop.jpg', seed=13)

# 4 Tech: a big cursor mid-click, the click rippling out in concentric arcs
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 40, 600, c['skyb'], seed=8)
cx, cy = 520, 300
for k, r in enumerate(range(60, 760, 46)):
    ring(im, cx, cy, r, [c['prussian'], c['teal'], c['skyb']][k % 3], 3 if k % 3 == 2 else 2)
disc(im, cx, cy, 34, c['wine'])
cur = [(0, 0), (0, 168), (40, 130), (68, 194), (96, 182), (68, 120), (122, 120)]
poly(im, [(cx + 6 + x + 8, cy + 6 + y + 8) for x, y in cur], c['navy'])                 # shadow
poly(im, [(cx + 6 + x, cy + 6 + y) for x, y in cur], c['paper'])
inner = [(10, 22), (10, 142), (40, 112), (70, 176), (84, 170), (54, 108), (96, 110)]
poly(im, [(cx + 6 + x, cy + 6 + y) for x, y in inner], c['clay'])
finish(im, OUT + 'vibes_04_click.jpg', amt=16, seed=14)

# 5 FigJam: stickies, a wavy connector, and a stamp, on a dotted board
im = canvas(c['paper'])
d = ImageDraw.Draw(im)
for x in range(20, 1200, 28):
    for y in range(20, 600, 28):
        d.ellipse([(x-1.6)*S, (y-1.6)*S, (x+1.6)*S, (y+1.6)*S], fill=c['clay'])
def sticky(x, y, s, col, ang, lines_col):
    st = Image.new('RGBA', (int(s*S*1.6), int(s*S*1.6)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    o = s*S*0.3
    sd.rectangle([o + 8*S, o + 10*S, o + s*S + 8*S, o + s*S + 10*S], fill=c['clay'] + (255,))
    sd.polygon([(o, o), (o + s*S, o), (o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S), (o, o + s*S)], fill=col + (255,))
    sd.polygon([(o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S*0.8), (o + s*S*0.8, o + s*S)], fill=tuple(int(v*0.8) for v in col) + (255,))
    for k in range(3):
        yy = o + s*S*(0.28 + k*0.16); sd.line([(o + s*S*0.14, yy), (o + s*S*(0.8 - k*0.18), yy)], fill=lines_col + (255,), width=5*S)
    st = st.rotate(ang, resample=Image.BICUBIC)
    im.paste(st, (int(x*S - st.width/2), int(y*S - st.height/2)), st)
path = bez((300, 250), (420, 520), (640, 60), (860, 300), 120)
line(im, [tuple(p) for p in path], c['plum'], 5)
for k in range(1, 4):
    line(im, [(p[0], p[1] + k*14) for p in path[10:110]], c['mauve'], 2)
tip = path[-1]; dx, dy = path[-1] - path[-6]; a = math.atan2(dy, dx)
poly(im, [(tip[0] + 22*math.cos(a), tip[1] + 22*math.sin(a)), (tip[0] + 18*math.cos(a + 2.3), tip[1] + 18*math.sin(a + 2.3)), (tip[0] + 18*math.cos(a - 2.3), tip[1] + 18*math.sin(a - 2.3))], c['plum'])
sticky(250, 230, 190, c['ochre'], 6, c['deep'])
sticky(930, 330, 210, c['skyb'], -5, c['indigo'])
sticky(620, 470, 150, c['mauve'], 3, c['plum'])
disc(im, 1060, 110, 46, c['wine']); text(im, 1043, 84, '+1', 34, c['paper'], 800)
finish(im, OUT + 'vibes_05_stickies.jpg', seed=15)

# 6 FigJam: a landscape built from the basic shapes, with a teammate's cursor and name tag
im = canvas(c['mist'], c['paper'], 1)
disc(im, 860, 150, 90, c['wine'])                                             # circle shape = sun
for (x0, x1, px, py, col) in [(120, 640, 380, 140, c['plum']), (420, 900, 650, 240, c['deep'])]:
    poly(im, [(x0, 470), (px, py), (x1, 470)], col)                              # triangle shapes = mountains
d = ImageDraw.Draw(im)
d.polygon([(380*S, 140*S), (420*S, 200*S), (340*S, 200*S)], fill=c['paper'])
rr(im, -40, 468, 1240, 640, 0, c['prussian'])
for i, (y, col) in enumerate([(482, c['teal']), (518, c['skyb']), (554, c['teal']), (590, c['skyb'])]):
    for k, x0 in enumerate(range(-60 + (i % 2) * 90, 1200, 180)):
        rr(im, x0, y, x0 + 150, y + 18, 9, col)                                  # pill shapes = swell
sparkle(im, 1050, 300, 26, c['ochre']); sparkle(im, 1100, 250, 13, c['ochre'])
poly(im, [(200, 300), (230, 330), (200, 360), (170, 330)], c['ochre'])         # diamond
mx, my = 690, 330                                                              # selection box around the sun-mountain
for (a0, b0, a1, b1) in [(560, 130, 960, 470)]:
    line(im, [(a0, b0), (a1, b0), (a1, b1), (a0, b1), (a0, b0)], c['skyb'], 2)
    for hx_, hy_ in [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]:
        rr(im, hx_-7, hy_-7, hx_+7, hy_+7, 2, c['paper'], c['skyb'], 2)
cur = [(0, 0), (0, 66), (17, 51), (28, 78), (41, 72), (29, 47), (51, 47)]
poly(im, [(985 + x, 380 + y) for x, y in cur], c['wine'])
rr(im, 1036, 432, 1140, 474, 12, c['wine']); text(im, 1053, 436, 'you', 26, c['paper'], 700)
finish(im, OUT + 'vibes_06_shapes.jpg', seed=16)

# 7 Nature + UI: the sun is a slider thumb travelling a dotted arc over layered hills
im = canvas(c['ochre'], c['paper'], 0.9)
arc = [(600 + 420*math.cos(t), 430 - 300*math.sin(t)) for t in np.linspace(math.pi, 0, 54)]
for i, (x, y) in enumerate(arc):
    if i % 2 == 0: disc(im, x, y, 4, c['wine'] if i < 22 else c['paper'])
sx_, sy_ = arc[22]
disc(im, sx_, sy_, 70, c['paper']); disc(im, sx_, sy_, 54, c['wine'])
rr(im, sx_ - 52, sy_ - 132, sx_ + 52, sy_ - 92, 12, c['ink']); text(im, sx_ - 35, sy_ - 128, '7:42', 26, c['paper'], 700)
ridge(im, 370, 30, 120, c['moss'], seed=3, jag=0.4)
ridge(im, 450, 18, 90, c['pine'], seed=5, jag=0.4)
xs, ys = ridge(im, 505, 14, 70, c['teal'], seed=7, jag=0.3)
sea(im, 545, c['indigo'], c['skyb'], gap=16)
for x in range(60, 1200, 110): pine_tree(im, x + 20, 470 + 10*math.sin(x/90), 80 + (x % 3)*12, c['pine'])
finish(im, OUT + 'vibes_07_sun_slider.jpg', seed=17)

# 8 Nature + UI: mountains as a bar chart, the moon a radio button, clouds as chips
im = canvas(c['navy'], c['indigo'], 1)
stars(im, 50, 330, c['mist'], seed=21, avoid=(930, 120, 60))
ring(im, 930, 120, 48, c['clay'], 6); disc(im, 930, 120, 26, c['clay'])
rr(im, 140, 120, 360, 168, 24, c['prussian']); disc(im, 166, 144, 10, c['skyb'])
rr(im, 420, 190, 590, 232, 21, c['prussian']); disc(im, 444, 211, 9, c['skyb'])
for k, r in enumerate([150, 120, 90]): pass
bars = [(80, 330), (190, 240), (300, 180), (410, 270), (520, 210), (630, 300), (740, 230), (850, 330), (960, 260), (1070, 350)]
cols = [c['teal'], c['prussian'], c['plum'], c['teal'], c['deep'], c['prussian'], c['plum'], c['teal'], c['prussian'], c['deep']]
for (x, top), col in zip(bars, cols):
    rr(im, x, top, x + 90, 640, 14, col)
    rr(im, x, top, x + 90, top + 26, 13, c['paper'])                            # snow cap
    poly(im, [(x, top + 13), (x + 90, top + 13), (x + 90, top + 30), (x + 70, top + 22), (x + 45, top + 34), (x + 20, top + 24), (x, top + 32)], c['paper'])
sea(im, 500, c['navy'], c['prussian'], gap=16)
line(im, [(60, 500), (1180, 500)], c['skyb'], 2)
finish(im, OUT + 'vibes_08_bar_peaks.jpg', amt=16, seed=18)
print('done')

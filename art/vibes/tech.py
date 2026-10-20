"""Vibes exploration, tech set: 8 illustrations of devices and computing in the house style."""
import sys, os
os.environ['VIBES_SET'] = 'vibes_tech'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vhelp import *

def arcband(im, cx, cy, r, w, a0, a1, col):
    ImageDraw.Draw(im).arc([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], a0, a1, fill=col, width=int(w*S))

# 1 Notifications: a phone on a desk, notification pills rising off it like bubbles toward a sun
im = canvas(c['mist'], c['paper'], 1)
disc(im, 1060, 100, 52, c['wine'])
rr(im, 0, 500, 1200, 600, 0, c['clay'])
rr(im, 470, 150, 730, 560, 36, c['ink'])
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([486*S, 166*S, 714*S, 544*S], radius=26*S, fill=255)
scr = canvas(c['indigo'], c['teal'], 1); seigaiha(scr, 430, [c['teal'], c['prussian'], c['pine']], r=22, line=c['skyb'])
im.paste(scr, (0, 0), m)
rr(im, 560, 180, 640, 196, 8, c['ink'])
for k, (x, y, w_, col) in enumerate([(505, 230, 190, c['paper']), (505, 290, 190, c['clay']), (720, 120, 230, c['paper']), (240, 200, 210, c['mauve']), (770, 300, 170, c['skyb']), (250, 340, 160, c['paper'])]):
    rr(im, x, y, x + w_, y + 46, 23, col)
    disc(im, x + 24, y + 23, 12, [c['wine'], c['teal'], c['ochre'], c['plum'], c['indigo'], c['ochre']][k])
    rr(im, x + 46, y + 18, x + w_ - 24, y + 28, 5, c['deep'] if col != c['skyb'] else c['indigo'])
finish(im, OUT + 'tech_01_notifications.jpg', seed=41)

# 2 Keyboard: rows of keycaps rolling like swell, one wine key pressed
im = canvas(c['indigo'], c['navy'], 1)
for row in range(5):
    y = 120 + row * 92
    for col in range(-1, 14):
        x = col * 92 + (row % 2) * 46 + 10 + 18 * math.sin(row)
        dy = 14 * math.sin(col / 1.8 + row * 0.9)
        hot = (row == 2 and col == 6)
        top = c['wine'] if hot else [c['prussian'], c['teal'], c['skyb'], c['prussian'], c['pine']][row]
        side = tuple(int(v * 0.65) for v in top)
        press = 8 if hot else 0
        rr(im, x, y + dy + 10, x + 80, y + dy + 82, 14, side)
        rr(im, x + 5, y + dy + press, x + 75, y + dy + 66 + press, 12, top)
        if hot: disc(im, x + 40, y + dy + 33 + press, 9, c['paper'])
finish(im, OUT + 'tech_02_keyboard.jpg', amt=15, seed=42)

# 3 Headphones: a pair of headphones over an equaliser that rises like a skyline of swell
im = canvas(c['ochre'], c['paper'], 0.9)
arcband(im, 600, 330, 230, 34, 180, 360, c['ink'])
rr(im, 330, 300, 420, 470, 30, c['plum']); rr(im, 780, 300, 870, 470, 30, c['plum'])
rr(im, 350, 320, 400, 450, 22, c['deep']); rr(im, 800, 320, 850, 450, 22, c['deep'])
for k, x in enumerate(range(450, 760, 26)):
    h_ = 40 + 90 * abs(math.sin(k * 0.7 + 0.4)) * (1 - abs(x - 605) / 300)
    rr(im, x, 470 - h_, x + 16, 470, 8, [c['teal'], c['wine'], c['prussian']][k % 3])
rr(im, 0, 470, 1200, 600, 0, c['teal'])
sea(im, 470, c['teal'], c['foamb'], gap=16, amp=3, freq=30)
finish(im, OUT + 'tech_03_headphones.jpg', seed=43)

# 4 Code window: an editor at night, code as coloured bars, a blinking caret
im = canvas(c['plum'], c['deep'], 1)
rr(im, 170, 70, 1030, 530, 18, c['navy'])
rr(im, 170, 70, 1030, 118, 18, c['indigo']); rr(im, 170, 100, 1030, 118, 0, c['indigo'])
for k, col in enumerate([c['wine'], c['ochre'], c['moss']]): disc(im, 202 + k*28, 94, 8, col)
rng = np.random.default_rng(44)
y = 150
for ln in range(11):
    disc(im, 215, y + 8, 3, c['prussian'])
    x = 250 + (ln in (2, 3, 4, 7, 8)) * 40 + (ln in (3, 8)) * 40
    for seg in range(rng.integers(2, 5)):
        w_ = int(rng.integers(40, 150))
        rr(im, x, y, x + w_, y + 16, 8, [c['skyb'], c['mauve'], c['ochre'], c['teal'], c['clay']][int(rng.integers(0, 5))])
        x += w_ + 14
    if ln == 6: rr(im, x + 4, y - 4, x + 10, y + 20, 2, c['paper'])
    y += 34
disc(im, 1040, 120, 0, c['wine'])
finish(im, OUT + 'tech_04_code.jpg', amt=15, seed=44)

# 5 Loading: a progress ring eclipsing the sun, a progress bar for a horizon
im = canvas(c['paper'], c['clay'], 1.2)
disc(im, 600, 250, 150, c['wine'])
arcband(im, 600, 250, 190, 18, 0, 360, c['mauve'])
arcband(im, 600, 250, 190, 18, -90, 160, c['plum'])
rc = 190 - 9                                   # the arc is drawn inward from r, so its centre line is r - width/2
disc(im, 600 + rc * math.cos(math.radians(160)), 250 + rc * math.sin(math.radians(160)), 9, c['plum'])
text(im, 545, 215, '72%', 56, c['paper'], 800)
sea(im, 500, c['teal'], c['foamb'], gap=16, amp=3, freq=30)            # real sea below the horizon
for k in range(6):                                                         # the sun's reflection
    w_ = 150 - k * 22
    rr(im, 600 - w_/2, 528 + k * 12, 600 + w_/2, 533 + k * 12, 2, c['wine'])
rr(im, 120, 482, 1080, 500, 9, c['mauve'])                               # progress bar on the horizon
rr(im, 120, 482, 812, 500, 9, c['plum'])
finish(im, OUT + 'tech_05_loading.jpg', seed=45)

# 6 Signal: wifi arcs rising off a little router like a sunrise over the sea
im = canvas(c['skyb'], c['mist'], 1)
cx, cy = 600, 430
for k, r in enumerate([90, 160, 230, 300]):
    arcband(im, cx, cy, r, 26, 220, 320, [c['wine'], c['plum'], c['indigo'], c['prussian']][k])
sea(im, 430, c['indigo'], c['skyb'], gap=18)
rr(im, 520, 400, 680, 450, 14, c['ink'])
for k in range(3): disc(im, 560 + k * 30, 425, 6, [c['moss'], c['ochre'], c['wine']][k])
line(im, [(540, 400), (520, 330)], c['ink'], 6); line(im, [(660, 400), (680, 330)], c['ink'], 6)
front_sea(im, 470, c['indigo'], c['skyb'], seed=6)
finish(im, OUT + 'tech_06_signal.jpg', seed=46)

# 7 Chip: a microchip with circuit traces flowing out like rivers, a sun-dot at the core
im = canvas(c['pine'], c['teal'], 1)
cx, cy = 600, 300
rng = np.random.default_rng(47)
for side in range(4):
    for k in range(-3, 4):
        if side in (0, 1):
            sx = cx + (k * 30); sy = cy + (-110 if side == 0 else 110); ex = sx + rng.integers(-200, 200); ey = (0 if side == 0 else 600)
            pts = [(sx, sy), (sx, sy + (ey - sy) * 0.4), (ex, sy + (ey - sy) * 0.7), (ex, ey)]
        else:
            sx = cx + (-110 if side == 2 else 110); sy = cy + k * 30; ex = (0 if side == 2 else 1200); ey = sy + rng.integers(-150, 150)
            pts = [(sx, sy), (sx + (ex - sx) * 0.4, sy), (sx + (ex - sx) * 0.7, ey), (ex, ey)]
        line(im, pts, [c['moss'], c['foamb'], c['ochre']][abs(k) % 3], 3)
        disc(im, pts[1][0], pts[1][1], 5, c['ochre'])
rr(im, cx - 120, cy - 120, cx + 120, cy + 120, 18, c['ink'])
rr(im, cx - 90, cy - 90, cx + 90, cy + 90, 10, c['deep'])
disc(im, cx, cy, 52, c['wine'])
finish(im, OUT + 'tech_07_chip.jpg', seed=47)

# 8 Server rack: a tower of servers under the moon, little status lights like a city at night
im = canvas(c['navy'], c['indigo'], 1)
disc(im, 940, 110, 54, c['clay']); stars(im, 50, 300, c['mist'], seed=48, avoid=(940, 110, 54))
for t, (x0, top, w_) in enumerate([(240, 220, 200), (500, 120, 220), (780, 260, 180)]):
    rr(im, x0, top, x0 + w_, 560, 12, c['ink'])
    for k, y in enumerate(range(top + 20, 540, 46)):
        rr(im, x0 + 14, y, x0 + w_ - 14, y + 34, 6, c['prussian'] if (k + t) % 2 else c['indigo'])
        for j in range(3): disc(im, x0 + 34 + j * 18, y + 17, 4, [c['moss'], c['ochre'], c['wine'], c['skyb']][(k + j + t) % 4])
        rr(im, x0 + w_ - 80, y + 13, x0 + w_ - 30, y + 21, 4, c['navy'])
sea(im, 560, c['navy'], c['prussian'], gap=14)
finish(im, OUT + 'tech_08_servers.jpg', amt=16, seed=48)
print('done')

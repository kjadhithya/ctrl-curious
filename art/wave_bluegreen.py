import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = '/home/claude/art2/'
INK = (46, 31, 37); PAPER = (244, 238, 232); MAUVE = (201, 167, 181); PLUM = (126, 75, 107)
WINE = (138, 46, 59); CLAY = (217, 195, 183); DEEP = (88, 52, 74)
INDIGO=(28,48,80); PRUSSIAN=(43,76,111); SKYB=(124,158,184); TEAL=(36,88,92); PINE=(38,74,62); FOAMB=(214,226,230)
rng = np.random.default_rng(5)
S = 2; W, H = 1400 * S, 820 * S

def bez(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return ((1-t)**3)*p0 + 3*((1-t)**2)*t*p1 + 3*(1-t)*t**2*p2 + t**3*p3

def grain(im, amt=14):
    a = np.asarray(im.convert('RGB'), dtype=float)
    a = a + rng.normal(0, amt, a.shape[:2])[..., None]
    m = Image.fromarray((rng.random(a.shape[:2]) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(14))
    m = (np.asarray(m, dtype=float) - 127) / 127 * 7
    return Image.fromarray(np.clip(a + m[..., None], 0, 255).astype('uint8'))

# sky
t = np.linspace(0, 1, H)[:, None, None]
sky = np.array(CLAY) * (1 - t) * 0.35 + np.array(PAPER) * (1 - (1 - t) * 0.35)
im = Image.fromarray(np.broadcast_to(sky, (H, W, 3)).astype('uint8').copy())
d = ImageDraw.Draw(im)

# wine sun + mountain
d.ellipse([1130*S, 140*S, 1250*S, 260*S], fill=WINE)
sea_y = 620 * S
d.polygon([(900*S, sea_y), (1040*S, 465*S), (1180*S, sea_y)], fill=PLUM)
d.polygon([(990*S, 512*S), (1040*S, 465*S), (1090*S, 512*S), (1070*S, 504*S), (1054*S, 520*S), (1036*S, 506*S), (1018*S, 521*S)], fill=PAPER)

# sea band
d.rectangle([0, sea_y, W, H], fill=TEAL)
for k, y0 in enumerate(range(sea_y + 18*S, H, 22*S)):
    pts = [(x, y0 + math.sin(x / (40*S) + k) * 5*S) for x in range(0, W + 10, 6*S)]
    d.line(pts, fill=SKYB, width=2*S)

def wave(ox, oy, sc, body, stripe, foam, claws=True):
    P = lambda x, y: (ox + x * sc * S, oy + y * sc * S)
    outer = np.vstack([bez(P(0, 640), P(180, 600), P(300, 140), P(600, 110)),
                       bez(P(600, 110), P(770, 90), P(850, 260), P(760, 340))])
    inner = np.vstack([bez(P(760, 340), P(745, 255), P(670, 205), P(590, 220)),
                       bez(P(590, 220), P(470, 245), P(430, 460), P(480, 640))])
    poly = [tuple(p) for p in outer] + [tuple(p) for p in inner] + [P(480, 700), P(0, 700)]
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    layer = Image.new('RGB', (W, H), body); ld = ImageDraw.Draw(layer)
    # woodblock stripes: copies of the inner face, stepped outward toward the back of the wave
    for k in range(1, 12):
        off = np.array([-k * 26 * sc * S, -k * 11 * sc * S])
        ld.line([tuple(p + off) for p in inner], fill=stripe, width=int(3 * S * max(sc, .6)))
    im.paste(layer, (0, 0), mask)
    # foam claws hanging off the curl, from crest round to the tip
    for i, p in enumerate(outer[70:120:2]):
        nx, ny = p[0] - P(640, 230)[0], p[1] - P(640, 230)[1]
        L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        for j in range(3):
            rad = (9 + 7 * rng.random()) * S * sc
            cx = p[0] + nx * j * 12 * S * sc + rng.normal(0, 3*S*sc); cy = p[1] + ny * j * 12 * S * sc + rng.normal(0, 3*S*sc)
            d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=foam)
        if claws:
            # claw fingers curling down and out
            for f in (-0.5, 0, 0.5):
                tx = p[0] + (nx + f * ny) * 44 * S * sc; ty = p[1] + (ny - f * nx) * 44 * S * sc + 18 * S * sc
                d.line([tuple(p), (tx, ty)], fill=foam, width=int(4 * S * sc) or 1)
    # spray along the top of the crest
    for p in outer[40:80:2]:
        for _ in range(2):
            rad = (4 + 6 * rng.random()) * S * sc
            cx = p[0] + rng.normal(0, 8*S*sc); cy = p[1] - abs(rng.normal(8, 8)) * S * sc
            d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=foam)

wave(0, -20, 1.0, INDIGO, SKYB, PAPER)
wave(760*S, 330*S, 0.55, PRUSSIAN, FOAMB, PAPER)
wave(-120*S, 470*S, 0.42, PINE, SKYB, PAPER, claws=False)

im = im.resize((1400, 820), Image.LANCZOS)
grain(im).crop((0,110,1400,810)).resize((1200,600), Image.LANCZOS).save(OUT + 'wave_hero_bg.jpg', quality=84)
print('wave')
print('done')

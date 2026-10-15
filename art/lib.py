"""Shared drawing helpers for Ctrl+Curious hero art (1200x600, grainy woodblock style)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def hx(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

C = {k: hx(v) for k, v in dict(
    ink='2E1F25', paper='F4EEE8', mauve='C9A7B5', plum='7E4B6B', wine='8A2E3B', clay='D9C3B7', ochre='C8902F',
    deep='58344A', indigo='1C3050', prussian='2B4C6F', skyb='7C9EB8', mist='C9D6DC', teal='24585C',
    pine='264A3E', moss='4F6A3A', navy='172338', foamb='D6E2E6').items()}

S = 2
W, H = 1200 * S, 600 * S

def canvas(top, bottom=None, power=1.0):
    bottom = bottom or top
    t = (np.linspace(0, 1, H) ** power)[:, None, None]
    a = np.array(top) * (1 - t) + np.array(bottom) * t
    return Image.fromarray(np.broadcast_to(a, (H, W, 3)).astype('uint8').copy())

def bez(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return ((1-t)**3)*p0 + 3*((1-t)**2)*t*p1 + 3*(1-t)*t**2*p2 + t**3*p3

def disc(im, cx, cy, r, col):
    ImageDraw.Draw(im).ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=col)

def mountain(im, x0, x1, peak_x, peak_y, base_y, col, snow=None):
    d = ImageDraw.Draw(im)
    d.polygon([(x0*S, base_y*S), (peak_x*S, peak_y*S), (x1*S, base_y*S)], fill=col)
    if snow:
        h = (base_y - peak_y) * 0.28
        lx = peak_x - (peak_x - x0) * h / (base_y - peak_y); rx = peak_x + (x1 - peak_x) * h / (base_y - peak_y)
        y = peak_y + h; pts = [(lx, y)]
        n = 6
        for i in range(1, n):
            px = lx + (rx - lx) * i / n
            pts.append((px, y + (10 if i % 2 else -2)))
        pts += [(rx, y), (peak_x, peak_y)]
        d.polygon([(a*S, b*S) for a, b in pts], fill=snow)

def sea(im, y, col, line=None, gap=20, amp=4, freq=36, top=0):
    d = ImageDraw.Draw(im)
    d.rectangle([0, y*S, W, H], fill=col)
    if line:
        for k, y0 in enumerate(range(int(y + 14), 600, gap)):
            pts = [(x*S, (y0 + math.sin(x / freq + k) * amp)*S) for x in range(0, 1210, 5)]
            d.line(pts, fill=line, width=2*S)

def wave(im, ox, oy, sc, body, stripe, foam, claws=True, seed=5):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(im)
    P = lambda x, y: ((ox + x * sc) * S, (oy + y * sc) * S)
    outer = np.vstack([bez(P(0, 640), P(180, 600), P(300, 140), P(600, 110)),
                       bez(P(600, 110), P(770, 90), P(850, 260), P(760, 340))])
    inner = np.vstack([bez(P(760, 340), P(745, 255), P(670, 205), P(590, 220)),
                       bez(P(590, 220), P(470, 245), P(430, 460), P(480, 640))])
    poly = [tuple(p) for p in outer] + [tuple(p) for p in inner] + [P(480, 900), P(0, 900)]
    mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon(poly, fill=255)
    layer = Image.new('RGB', (W, H), body); ld = ImageDraw.Draw(layer)
    for k in range(1, 12):
        off = np.array([-k * 26 * sc * S, -k * 11 * sc * S])
        ld.line([tuple(p + off) for p in inner], fill=stripe, width=max(2, int(3 * S * max(sc, .6))))
    im.paste(layer, (0, 0), mask)
    c = P(640, 230)
    for p in outer[70:120:2]:
        nx, ny = p[0] - c[0], p[1] - c[1]; L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        for j in range(3):
            r = (9 + 7 * rng.random()) * S * sc
            cx = p[0] + nx * j * 12 * S * sc + rng.normal(0, 3*S*sc); cy = p[1] + ny * j * 12 * S * sc + rng.normal(0, 3*S*sc)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=foam)
        if claws:
            for f in (-0.5, 0, 0.5):
                tx = p[0] + (nx + f * ny) * 44 * S * sc; ty = p[1] + (ny - f * nx) * 44 * S * sc + 18 * S * sc
                d.line([tuple(p), (tx, ty)], fill=foam, width=max(1, int(4 * S * sc)))
    for p in outer[40:80:2]:
        for _ in range(2):
            r = (4 + 6 * rng.random()) * S * sc
            cx = p[0] + rng.normal(0, 8*S*sc); cy = p[1] - abs(rng.normal(8, 8)) * S * sc
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=foam)

def seigaiha(im, y0, cols, r=34, line=None):
    """Fill from y0 to bottom with overlapping concentric-arc scales."""
    d = ImageDraw.Draw(im)
    row = 0; y = y0
    while y < 600 + r:
        off = (r if row % 2 else 0)
        for x in range(-2*r + off, 1200 + 2*r, 2*r):
            for k, rr in enumerate(np.linspace(r, r * 0.2, 4)):
                col = cols[(k + row) % len(cols)] if k % 2 == 0 else (line or cols[-1])
                d.ellipse([(x - rr)*S, (y - rr)*S, (x + rr)*S, (y + rr)*S], fill=col)
        y += r * 0.5; row += 1

def stars(im, n, ymax, col, seed=3, avoid=None):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rng.integers(0, 1200), rng.integers(0, ymax)
        if avoid and (x - avoid[0])**2 + (y - avoid[1])**2 < (avoid[2] + 8)**2: continue
        s = rng.choice([1.5, 2, 2.5]); d.ellipse([(x-s)*S, (y-s)*S, (x+s)*S, (y+s)*S], fill=col)

def boat(im, x, y, length, col, rowers=None, tilt=0):
    d = ImageDraw.Draw(im)
    pts = bez((x - 10, y - 14), (x + length*0.25, y + 34 + tilt), (x + length*0.75, y + 34 - tilt), (x + length + 10, y - 22 - tilt), 40)
    top = bez((x + length + 10, y - 22 - tilt), (x + length*0.7, y + 4 - tilt), (x + length*0.3, y + 4 + tilt), (x - 10, y - 14), 40)
    d.polygon([(a*S, b*S) for a, b in np.vstack([pts, top])], fill=col)
    if rowers:
        for i in range(1, 7):
            px = x + length * i / 7.5; py = y + 10 + tilt * (0.5 - i / 7)
            d.ellipse([(px-7)*S, (py-18)*S, (px+7)*S, (py-4)*S], fill=rowers)

def rain(im, col, n=260, seed=9, angle=0.35, length=36):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rng.integers(-100, 1200), rng.integers(-40, 600)
        d.line([(x*S, y*S), ((x + length*angle)*S, (y + length)*S)], fill=col, width=S)

def finish(im, path, amt=13, seed=1):
    rng = np.random.default_rng(seed)
    im = im.resize((1200, 600), Image.LANCZOS)
    a = np.asarray(im.convert('RGB'), dtype=float)
    a = a + rng.normal(0, amt, a.shape[:2])[..., None]
    m = Image.fromarray((rng.random(a.shape[:2]) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(14))
    m = (np.asarray(m, dtype=float) - 127) / 127 * 7
    Image.fromarray(np.clip(a + m[..., None], 0, 255).astype('uint8')).save(path, quality=84)

def front_sea(im, y, col, line=None, foam=None, gap=18, amp=5, freq=30, seed=0):
    """Water in front of the waves, with a wavy top edge, so wave bodies rise out of it."""
    d = ImageDraw.Draw(im)
    top = [(x*S, (y + math.sin(x / freq + seed) * amp + math.sin(x / (freq * 0.37) + seed) * amp * 0.4)*S) for x in range(0, 1210, 4)]
    d.polygon(top + [(W, H), (0, H)], fill=col)
    if foam:
        d.line(top, fill=foam, width=3*S)
    if line:
        for k, y0 in enumerate(range(int(y + 12), 600, gap)):
            pts = [(x*S, (y0 + math.sin(x / freq + k + seed) * 4)*S) for x in range(0, 1210, 5)]
            d.line(pts, fill=line, width=2*S)

def glow(im, x, y, r, col, strength=0.55, blur=None):
    """Soft light: a blurred disc blended over the image."""
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=int(255*strength))
    m = m.filter(ImageFilter.GaussianBlur((blur or r*0.6)*S))
    im.paste(Image.new('RGB', (W, H), col), (0, 0), m)

def crescent(im, cx, cy, r, col, sky=None, dx=0.38, dy=-0.18):
    bx, by = cx + r*dx*2, cy + r*dy*2
    snap = im.copy()
    disc(im, cx, cy, r, col)
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).ellipse([(bx - r*0.92)*S, (by - r*0.92)*S, (bx + r*0.92)*S, (by + r*0.92)*S], fill=255)
    im.paste(snap, (0, 0), m)

def ridge(im, y0, amp, freq, col, seed=0, jag=1.0):
    rng = np.random.default_rng(seed); xs = np.arange(0, 1201, 3)
    y = y0 + amp*np.sin(xs/freq + rng.random()*6) + 0.4*amp*np.sin(xs/(freq/2.6) + rng.random()*6)
    y = y + np.cumsum(rng.normal(0, jag, len(xs))); y -= np.linspace(0, y[-1]-y[0], len(xs))*0.5
    ImageDraw.Draw(im).polygon([(x*S, v*S) for x, v in zip(xs, y)] + [(W, H), (0, H)], fill=col)
    return xs, y

def pine_tree(im, x, base, h, col):
    d = ImageDraw.Draw(im); w = h*0.36
    for k in range(4):
        top = base - h + k*h*0.2; bot = base - h*0.55 + k*h*0.17; ww = w*(0.45 + k*0.2)
        d.polygon([(x*S, top*S), ((x-ww)*S, bot*S), ((x+ww)*S, bot*S)], fill=col)
    d.rectangle([(x-w*0.07)*S, (base-h*0.1)*S, (x+w*0.07)*S, base*S], fill=col)

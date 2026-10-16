"""Typeface spotlight specimen for Redaction (OFL, Google Fonts), rendered with the real font files.
Usage: python3 redaction.py <dir with ofl/redaction* folders> <out.jpg>"""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
G, OUT = sys.argv[1], sys.argv[2]
W, H = 1056, 760
PAPER, INK, MUTED, WINE = (244, 238, 232), (46, 31, 37), (122, 104, 112), (138, 46, 59)
im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
f = lambda fam, style, size: ImageFont.truetype(f'{G}/ofl/{fam.lower()}/{fam}-{style}.ttf', size)
d.text((56, 40), 'Redaction', font=f('Redaction', 'Regular', 150), fill=INK)
d.text((60, 222), 'Soft round terminals, razor-thin strokes.', font=f('Redaction', 'Italic', 40), fill=INK)
d.text((60, 282), 'Aa Bb Cc Gg Qq Rr  &  0123456789', font=f('Redaction', 'Bold', 40), fill=WINE)
d.line([(60, 350), (W - 60, 350)], fill=(205, 192, 184), width=2)
y = 372
for n in ['10', '20', '35', '50', '70', '100']:
    d.text((60, y + 10), n, font=ImageFont.truetype(f'{G}/ofl/redaction/Redaction-Regular.ttf', 22), fill=MUTED)
    d.text((130, y), 'Redaction ' + n + ': the same letters, rougher', font=f('Redaction' + n, 'Regular', 38), fill=INK)
    y += 62
a = np.asarray(im, dtype=float) + np.random.default_rng(7).normal(0, 7, (H, W, 1))
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(OUT, quality=88)
print(OUT)

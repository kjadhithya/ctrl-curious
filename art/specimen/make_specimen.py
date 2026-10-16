"""Typeface spotlight specimen, rendered with the real font files (for free fonts, e.g. Google Fonts).
python3 make_specimen.py --name "Redaction" --regular R.ttf [--italic I.ttf] [--bold B.ttf] --line "Short line" --out out.jpg
Draws the name large, a line in the italic (or regular), the alphabet and figures in bold (or regular),
then one line per style available, on paper with light grain. 1056 x 640, shown at 528 wide in the email."""
import argparse, numpy as np
from PIL import Image, ImageDraw, ImageFont
p = argparse.ArgumentParser()
p.add_argument('--name', required=True); p.add_argument('--regular', required=True)
p.add_argument('--italic'); p.add_argument('--bold'); p.add_argument('--line', default='')
p.add_argument('--out', required=True)
a = p.parse_args()
W, H = 1056, 640
PAPER, INK, MUTED, WINE, RULE = (244, 238, 232), (46, 31, 37), (122, 104, 112), (138, 46, 59), (205, 192, 184)
im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
F = lambda path, size: ImageFont.truetype(path, size)
size = 150
while size > 60 and d.textlength(a.name, font=F(a.regular, size)) > W - 112:
    size -= 6
d.text((56, 40), a.name, font=F(a.regular, size), fill=INK)
y = 40 + int(size * 1.22)
if a.line:
    d.text((60, y), a.line, font=F(a.italic or a.regular, 40), fill=INK); y += 60
d.text((60, y), 'Aa Bb Cc Gg Qq Rr  &  0123456789', font=F(a.bold or a.regular, 40), fill=WINE); y += 74
d.line([(60, y), (W - 60, y)], fill=RULE, width=2); y += 26
label = F(a.regular, 22)
for nm, path in [('Regular', a.regular), ('Italic', a.italic), ('Bold', a.bold)]:
    if not path or y > H - 70:
        continue
    d.text((60, y + 10), nm, font=label, fill=MUTED)
    d.text((170, y), 'Sphinx of black quartz, judge my vow.', font=F(path, 38), fill=INK)
    y += 62
im = im.crop((0, 0, W, min(H, y + 30)))
arr = np.asarray(im, dtype=float) + np.random.default_rng(7).normal(0, 7, (im.size[1], W, 1))
Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).save(a.out, quality=88)
print(a.out)

"""Wide wave banner for the blog home (option C): big wave on the right curling toward the headline."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
from PIL import ImageOps
c = C
im = canvas(c['paper'], c['clay'], 2.2)
disc(im, 500, 262, 46, c['wine'])
mountain(im, 410, 590, 500, 360, 455, c['plum'], snow=c['paper'])
sea(im, 455, c['teal'], c['skyb'], gap=18)
wave(im, 30, -95, 0.8, c['indigo'], c['skyb'], c['mist'], seed=5)
front_sea(im, 515, c['teal'], c['skyb'], foam=c['foamb'], seed=2)
seigaiha(im, 560, [c['prussian'], c['indigo']], r=22, line=c['teal'])
im = ImageOps.mirror(im)
rng = np.random.default_rng(3)
a = np.asarray(im.convert('RGB'), dtype=float) + rng.normal(0, 14, (H, W, 1))
out = '/home/claude/ctrl-curious/assets/blog/banner_wave.jpg'
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).resize((1920, 960), Image.LANCZOS).save(out, quality=86)
print(out)

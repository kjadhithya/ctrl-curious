"""Re-grain images with the coarse, heavy grain of the original moon artwork.
The original was drawn at ~700px wide with strong noise (sigma 30) and then shown larger,
so the grain is coarse. We match that: shrink to ~58%, add monochrome noise, scale back up."""
import sys, numpy as np
from PIL import Image
def heavy(path, sigma=28, scale=0.58, seed=0):
    im = Image.open(path).convert('RGB'); w, h = im.size
    sw, sh = max(1, int(w*scale)), max(1, int(h*scale))
    small = np.asarray(im.resize((sw, sh), Image.LANCZOS), dtype=float)
    rng = np.random.default_rng(seed)
    small = small + rng.normal(0, sigma, (sh, sw, 1))
    out = Image.fromarray(np.clip(small, 0, 255).astype('uint8')).resize((w, h), Image.BICUBIC)
    out.save(path, quality=88)
if __name__ == '__main__':
    for i, p in enumerate(sys.argv[1:]):
        heavy(p, seed=i); print('grained', p)

"""Dark (Tuesday 'Night shift') versions of shared email assets: the wave strip with its paper
turned to the dark band colour, and a darker page grain for the outer background."""
import numpy as np
from PIL import Image
A = '/home/claude/ctrl-curious/assets/email/'
im = np.asarray(Image.open(A + 'seigaiha_strip.jpg').convert('RGB'), dtype=float)
L = im.mean(axis=2, keepdims=True)
t = np.clip((L - 165) / 70, 0, 1)
dark = np.array([46, 31, 37], dtype=float)
out = im * (1 - t) + dark * t
Image.fromarray(np.clip(out, 0, 255).astype('uint8')).save(A + 'seigaiha_strip_dark.jpg', quality=90)
g = np.asarray(Image.open(A + 'grain_dark.jpg').convert('RGB'), dtype=float) * (30 / 48)
g = g.mean(axis=(0, 1), keepdims=True) + (g - g.mean(axis=(0, 1), keepdims=True)) * 0.7   # softer grain
Image.fromarray(np.clip(g, 0, 255).astype('uint8')).save(A + 'grain_page_dark.jpg', quality=90)
print('ok')
# Softer grain for Tuesday's dark sections (30% less contrast than grain_dark.jpg)
d = np.asarray(Image.open(A + 'grain_dark.jpg').convert('RGB'), dtype=float)
Image.fromarray(np.clip(d.mean(axis=(0, 1), keepdims=True) + (d - d.mean(axis=(0, 1), keepdims=True)) * 0.7, 0, 255).astype('uint8')).save(A + 'grain_dark_soft.jpg', quality=92)

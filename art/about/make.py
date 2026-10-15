"""About page art: Monday's Ochre dawn redrawn with soft wave bases and evenly spaced lines."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import *
c = C
im = canvas(c['ochre'], c['paper'], 0.8)
disc(im, 320, 380, 80, c['wine'])
sea(im, 450, c['pine'], c['ochre'], gap=24)
wave(im, 470, 40, 0.62, c['teal'], c['foamb'], c['paper'], seed=41, soft=True, parallel=True)
wave(im, -20, 270, 0.34, c['moss'], c['foamb'], c['paper'], seed=42, soft=True, parallel=True)
front_sea(im, 458, c['pine'], c['ochre'], gap=24, seed=5)
finish(im, '/home/claude/ctrl-curious/assets/blog/about_ochre_dawn.jpg', seed=7)

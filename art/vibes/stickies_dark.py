"""Dark version of the FigJam stickies illustration (09 on the Thursday board)."""
import sys, os
os.environ['VIBES_SET'] = 'vibes_figjam'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vhelp import *

# Dark FigJam: stickies, a wavy connector, and a stamp, on a dotted board
MIX = lambda a, b, t: tuple(int(x*(1-t) + y*t) for x, y in zip(a, b))
TOP, BOT = MIX(c['teal'], c['foamb'], 0.30), MIX(c['teal'], c['foamb'], 0.18)
im = canvas(c['teal'], c['pine'], 1)
d = ImageDraw.Draw(im)
for x in range(20, 1200, 28):
    for y in range(20, 600, 28):
        d.ellipse([(x-1.8)*S, (y-1.8)*S, (x+1.8)*S, (y+1.8)*S], fill=MIX(c['teal'], c['foamb'], 0.6))
def sticky(x, y, s, col, ang, lines_col):
    st = Image.new('RGBA', (int(s*S*1.6), int(s*S*1.6)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    o = s*S*0.3
    sd.rectangle([o + 8*S, o + 10*S, o + s*S + 8*S, o + s*S + 10*S], fill=c['pine'] + (255,))
    sd.polygon([(o, o), (o + s*S, o), (o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S), (o, o + s*S)], fill=col + (255,))
    sd.polygon([(o + s*S, o + s*S*0.8), (o + s*S*0.8, o + s*S*0.8), (o + s*S*0.8, o + s*S)], fill=tuple(int(v*0.8) for v in col) + (255,))
    for k in range(3):
        yy = o + s*S*(0.28 + k*0.16); sd.line([(o + s*S*0.14, yy), (o + s*S*(0.8 - k*0.18), yy)], fill=lines_col + (255,), width=5*S)
    st = st.rotate(ang, resample=Image.BICUBIC)
    im.paste(st, (int(x*S - st.width/2), int(y*S - st.height/2)), st)
path = bez((300, 250), (420, 520), (640, 60), (860, 300), 120)
line(im, [tuple(p) for p in path], c['ochre'], 5)
for k in range(1, 4):
    line(im, [(p[0], p[1] + k*14) for p in path[10:110]], c['foamb'], 2)
tip = path[-1]; dx, dy = path[-1] - path[-6]; a = math.atan2(dy, dx)
poly(im, [(tip[0] + 22*math.cos(a), tip[1] + 22*math.sin(a)), (tip[0] + 18*math.cos(a + 2.3), tip[1] + 18*math.sin(a + 2.3)), (tip[0] + 18*math.cos(a - 2.3), tip[1] + 18*math.sin(a - 2.3))], c['ochre'])
sticky(250, 230, 190, c['ochre'], 6, c['deep'])
sticky(930, 330, 210, c['skyb'], -5, c['indigo'])
sticky(620, 470, 150, c['mauve'], 3, c['plum'])
disc(im, 1060, 110, 46, c['wine']); text(im, 1043, 84, '+1', 34, c['paper'], 800)
finish(im, OUT + 'stickies_dark.jpg', amt=15, seed=15)


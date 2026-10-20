"""Friday thumbnail for the week-by-day cards: a pixel deck chair facing a sunset."""
import os, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/ctrl-curious/assets/explore/thumbs/'
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
C={k:hx(v) for k,v in dict(ink='2E1F25',paper='F4EEE8',mauve='C9A7B5',plum='7E4B6B',wine='8A2E3B',clay='D9C3B7',ochre='C8902F',
   indigo='1C3050',prussian='2B4C6F',skyb='7C9EB8',mist='C9D6DC',teal='24585C',pine='264A3E',moss='4F6A3A',navy='172338',foamb='D6E2E6',dark='4A3540').items()}
c=C
GW,GH=150,75   # pixel grid; each cell = 8px in the 1200x600 output

def grid(bg): return Image.new('RGB',(GW,GH),bg)
def R(im,x,y,w,h,col):
    if w>0 and h>0: ImageDraw.Draw(im).rectangle([x,y,x+w-1,y+h-1],fill=col)
def P(im,pts,col):
    for x,y in pts: R(im,x,y,1,1,col)
def pdisc(im,cx,cy,r,col):
    for y in range(int(cy-r),int(cy+r)+1):
        for x in range(int(cx-r),int(cx+r)+1):
            if (x-cx)**2+(y-cy)**2<=r*r and 0<=x<GW and 0<=y<GH: im.putpixel((x,y),col)
def sparkle(im,x,y,col=None):
    col=col or c['ochre']; R(im,x,y-3,1,7,col); R(im,x-3,y,7,1,col); R(im,x-1,y-1,3,3,col)
def finish(small,name,amt=12,seed=0):
    big=small.resize((1200,600),Image.NEAREST)
    rng=np.random.default_rng(seed); a=np.asarray(big,float)+rng.normal(0,amt,(600,1200,1))
    Image.fromarray(np.clip(a,0,255).astype('uint8')).save(OUT+name,quality=88)
def wave_rows(im,y0,cols,period=12,amp=2):
    for y in range(y0,GH):
        for x in range(GW):
            k=(y-y0+amp*round(np.sin(2*np.pi*x/period)))//3
            im.putpixel((x,y),cols[k%len(cols)])


def line_px(im,x0,y0,x1,y1,col):
    n=max(abs(x1-x0),abs(y1-y0),1)
    for i in range(n+1): R(im,round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),1,1,col)
im=grid(c['mauve'])
for y,col in [(0,c['plum']),(8,c['mauve']),(18,c['clay']),(28,c['ochre'])]: R(im,0,y,GW,10,col)
pdisc(im,95,38,12,c['wine'])
wave_rows(im,38,[c['plum'],c['prussian'],c['indigo']],period=16)
R(im,0,56,GW,19,c['clay']); R(im,0,56,GW,1,c['paper'])
# umbrella
R(im,40,22,2,36,c['ink'])
for k,col in enumerate([c['wine'],c['paper'],c['wine'],c['paper'],c['wine']]):
    R(im,26+k*6,20-(2 if k in (1,2,3) else 0)-(1 if k==2 else 0),6,3+(2 if k in (1,2,3) else 0)+(1 if k==2 else 0),col)
# deck chair (side view), drawn large: A-frame legs, a thick striped sling, an arm rest
def thick(x0,y0,x1,y1,col,t=2):
    n=max(abs(x1-x0),abs(y1-y0),1)
    for i in range(n+1): R(im,round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n),t,t,col)
thick(58,46,72,73,c['ink'])            # back leg
thick(86,58,74,73,c['ink'])            # front leg
for i in range(30):                     # sling from the top of the back down to the front edge
    x=58+i; y=46+round(i*0.42)
    R(im,x,y,2,5,c['teal'] if (i//4)%2 else c['paper'])
thick(64,60,84,60,c['ink'],1)           # arm rest
# drink on the sand
R(im,94,64,4,7,c['paper']); R(im,94,64,4,2,c['ochre']); R(im,97,60,1,4,c['wine'])
sparkle(im,128,9,c['paper'])
finish(im,'thumb_fri.jpg',seed=65)
print('fri done')

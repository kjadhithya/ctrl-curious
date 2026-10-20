"""Friday · Weekend tabs — three more pixel-art hero options (09–11), same style as make.py. Not in the rotation yet."""
import os, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/ctrl-curious/assets/explore/fri_more/'
os.makedirs(OUT, exist_ok=True)
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
def ring_px(im,cx,cy,r,col,t=1.2):
    for y in range(int(cy-r-2),int(cy+r+3)):
        for x in range(int(cx-r-2),int(cx+r+3)):
            d=((x-cx)**2+(y-cy)**2)**0.5
            if abs(d-r)<=t and 0<=x<GW and 0<=y<GH: im.putpixel((x,y),col)

# 09 Bike ride: a pixel bicycle on the sea path at sunset
im=grid(c['ochre'])
for y in range(0,40): R(im,0,y,GW,1,c['ochre'] if y<14 else (c['clay'] if y<28 else c['mauve']))
pdisc(im,112,30,10,c['wine'])
wave_rows(im,38,[c['plum'],c['prussian'],c['indigo']],period=16)
R(im,0,56,GW,19,c['clay']); R(im,0,56,GW,1,c['paper'])
for x in range(0,GW,10): R(im,x,71,5,1,c['paper'])
bx,by=52,63
ring_px(im,bx,by,6,c['ink']); ring_px(im,bx+20,by,6,c['ink'])
R(im,bx,by,1,1,c['ink']); R(im,bx+20,by,1,1,c['ink'])
line_px(im,bx,by,bx+8,by-9,c['wine']); line_px(im,bx+8,by-9,bx+18,by-9,c['wine'])
line_px(im,bx+18,by-9,bx+20,by,c['wine']); line_px(im,bx+8,by-9,bx+11,by,c['wine']); line_px(im,bx,by,bx+11,by,c['wine'])
R(im,bx+6,by-11,5,1,c['ink']); line_px(im,bx+18,by-9,bx+17,by-13,c['ink']); R(im,bx+15,by-14,4,1,c['ink'])
R(im,bx+11,by-12,3,2,c['teal'])
sparkle(im,24,9,c['paper'])
finish(im,'fri_09.jpg',seed=9)

# 10 Rainy reading: an open book and a mug by a window with pixel rain
im=grid(c['plum'])
R(im,20,6,70,42,c['dark']); R(im,23,9,64,36,c['prussian'])
rng=np.random.default_rng(10)
for _ in range(60):
    x=int(rng.integers(24,86)); y=int(rng.integers(10,42)); R(im,x,y,1,3,c['skyb'])
R(im,54,9,2,36,c['dark']); R(im,23,26,64,2,c['dark'])
R(im,0,52,GW,23,c['wine']); R(im,0,52,GW,2,c['dark'])
R(im,34,44,30,9,c['paper']); R(im,64,44,30,9,c['foamb']); R(im,63,44,2,9,c['clay'])
for k in range(3): R(im,38,46+k*2,22,1,c['mauve']); R(im,68,46+k*2,22,1,c['skyb'])
R(im,108,40,12,13,c['paper']); R(im,120,43,3,1,c['paper']); R(im,122,43,1,6,c['paper']); R(im,120,48,3,1,c['paper'])
R(im,110,42,8,2,c['teal'])
P(im,[(111,36),(112,35),(112,34),(113,33),(114,36),(115,35),(115,34),(116,33)],c['mauve'])
R(im,128,44,10,9,c['clay']); R(im,128,44,10,2,c['paper'])
for dx,dy,h in [(-2,-8,10),(3,-12,12),(8,-7,9)]: R(im,128+dx+1,44+dy,3,h-2,c['moss'] if dx!=3 else c['pine'])
finish(im,'fri_10.jpg',seed=10)

# 11 Film night: a big screen with a pixel wave, a row of heads in the dark
im=grid(c['navy'])
R(im,30,6,90,40,c['dark']); R(im,33,9,84,34,c['mist'])
scr=grid(c['mist'])
for y in range(9,26): R(im,33,y,84,1,c['mist'] if y<17 else c['foamb'])
pdisc(im,98,17,5,c['wine'])
for y in range(26,43):
    for x in range(33,117):
        k=(y-26+2*round(np.sin(2*np.pi*x/14)))//3
        im.putpixel((x,y),[c['skyb'],c['teal'],c['prussian']][k%3])
for k in range(10): R(im,30+k*9,47+(k%2),9,1,c['indigo'])
R(im,0,58,GW,17,c['ink'])
for x in range(8,GW,16):
    pdisc(im,x,56,4,c['indigo']); R(im,x-7,60,15,15,c['indigo'])
pdisc(im,72,55,4,c['plum']); R(im,65,59,15,16,c['plum'])
finish(im,'fri_11.jpg',seed=11)
print('done')

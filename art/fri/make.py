"""Friday · Weekend tabs — 8 pixel-art hero images. 01 is the current template's pixel browser."""
import os, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/ctrl-curious/assets/email/days/fri/'
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
    import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.dirname(_o.path.abspath(__file__)))); from heavy_grain import heavy; heavy(OUT+name)
def wave_rows(im,y0,cols,period=12,amp=2):
    for y in range(y0,GH):
        for x in range(GW):
            k=(y-y0+amp*round(np.sin(2*np.pi*x/period)))//3
            im.putpixel((x,y),cols[k%len(cols)])

# 01 The current pixel browser, framed on prussian blue
small=Image.new('RGB',(132,76),c['prussian']); d=ImageDraw.Draw(small)
for line in open(os.path.join(HERE,'browser_rects.txt')):
    x,y,w,h,col=line.split(); d.rectangle([int(x),int(y),int(x)+int(w)-1,int(y)+int(h)-1],fill=hx(col))
big=Image.new('RGB',(1200,600),c['prussian']); big.paste(small.resize((924,532),Image.NEAREST),(138,34))
rng=np.random.default_rng(1); a=np.asarray(big,float)+rng.normal(0,12,(600,1200,1))
Image.fromarray(np.clip(a,0,255).astype('uint8')).save(OUT+'fri_01.jpg',quality=88)

# 02 Pixel wave: the great wave drawn smooth, then reduced to pixels and snapped to the palette
import sys; sys.path.insert(0, os.path.dirname(HERE)); import lib
L=lib.C
hi=lib.canvas(L['paper'])
lib.disc(hi, 1010, 110, 60, L['ochre'])
lib.sea(hi, 430, L['teal'])
lib.wave(hi, 60, -100, 0.86, L['indigo'], L['skyb'], L['paper'], seed=5)
lib.wave(hi, 720, 190, 0.42, L['prussian'], L['foamb'], L['paper'], seed=6)
lib.front_sea(hi, 480, L['teal'], None, seed=1)
lo=hi.resize((GW,GH),Image.BOX)
pal=[c[k] for k in ('paper','clay','ochre','teal','indigo','skyb','prussian','foamb','pine')]
pimg=Image.new('P',(1,1)); pimg.putpalette(sum(pal,())+(0,0,0)*(256-len(pal)))
im=lo.quantize(palette=pimg,dither=Image.Dither.NONE).convert('RGB')
for y in range(62,GH):
    for x in range(GW):
        if (x+(y//3)*4)%12<4 and (y%3==0): im.putpixel((x,y),c['skyb'])
finish(im,'fri_02.jpg',seed=2)

# 03 Laptop closing for the weekend: a pixel laptop with a wave wallpaper, a mug, a plant
im=grid(c['mauve'])
R(im,0,58,GW,17,c['plum'])
R(im,40,14,70,42,c['ink']); R(im,43,17,64,36,c['skyb'])
wave_sm=Image.new('RGB',(64,36),c['skyb']); wd=ImageDraw.Draw(wave_sm)
for y in range(20,36):
    for x in range(64):
        k=(y-20+round(1.5*np.sin(2*np.pi*x/10)))//3; wave_sm.putpixel((x,y),[c['teal'],c['prussian'],c['indigo']][k%3])
wd.rectangle([46,5,53,12],fill=c['wine'])
im.paste(wave_sm,(43,17))
R(im,34,56,82,3,c['clay']); R(im,30,59,90,2,c['dark'])
R(im,122,46,10,12,c['paper']); R(im,132,49,3,6,c['paper']); R(im,124,49,6,2,c['teal'])
P(im,[(125,42),(126,41),(126,40),(127,39),(129,42),(128,41),(128,40),(129,39)],c['paper'])
R(im,14,46,10,12,c['wine']); R(im,12,36,4,8,c['moss']); R(im,17,32,4,12,c['pine']); R(im,22,36,4,8,c['moss'])
sparkle(im,136,18)
finish(im,'fri_03.jpg',seed=3)

# 04 Too many tabs: a cascade of pixel browser windows
im=grid(c['teal'])
for i,(col,acc) in enumerate([(c['indigo'],c['wine']),(c['prussian'],c['ochre']),(c['pine'],c['mauve']),(c['plum'],c['skyb']),(c['paper'],c['wine'])]):
    x=16+i*14; y=6+i*8
    R(im,x,y,74,40,c['ink']); R(im,x+1,y+1,72,5,c['dark'])
    for k,cc in enumerate([c['wine'],c['ochre'],c['mauve']]): R(im,x+3+k*4,y+3,2,2,cc)
    R(im,x+1,y+6,72,33,col)
    if i==4:
        R(im,x+5,y+10,28,18,c['skyb']); R(im,x+12,y+20,8,8,c['teal']); R(im,x+20,y+16,10,12,c['prussian']); R(im,x+27,y+12,4,4,c['wine'])
        for k,w in enumerate([30,24,30,18]): R(im,x+38,y+11+k*5,w,2,c['plum'])
        R(im,x+38,y+31,12,4,c['wine'])
sparkle(im,132,12); sparkle(im,140,30,c['paper'])
finish(im,'fri_04.jpg',seed=4)

# 05 Pixel beach: umbrella, towel, blocky waves and a big sun
im=grid(c['mist'])
for y in range(0,34): R(im,0,y,GW,1,c['mist'] if y<18 else c['foamb'])
pdisc(im,110,14,9,c['ochre'])
wave_rows(im,34,[c['skyb'],c['teal'],c['prussian']],period=14)
for y in range(56,GH): R(im,0,y,GW,1,c['clay'])
for x in range(0,GW,14): R(im,x,55,8,1,c['paper'])
R(im,46,30,1,26,c['ink'])
for k,col in enumerate([c['wine'],c['paper'],c['wine'],c['paper'],c['wine']]):
    R(im,30+k*7,26-(2 if k in (1,2,3) else 0)-(1 if k==2 else 0),7,4+(2 if k in (1,2,3) else 0)+(1 if k==2 else 0),col)
R(im,56,62,26,8,c['teal']); R(im,56,64,26,2,c['paper'])
finish(im,'fri_05.jpg',seed=5)

# 06 Weekend camp: a tent, a campfire and a pixel moon over pine silhouettes
im=grid(c['navy'])
for y in range(30,52): R(im,0,y,GW,1,c['indigo'])
rng=np.random.default_rng(6)
for _ in range(40): R(im,int(rng.integers(0,GW)),int(rng.integers(0,30)),1,1,c['paper'])
pdisc(im,28,13,6,c['clay']); pdisc(im,31,11,5,c['navy'])
for x0,h in [(0,22),(10,28),(118,26),(128,32),(140,24)]:
    for k in range(h):
        w=max(1,(k*7)//h); R(im,x0+5-w,52-h+k,2*w+1,1,c['pine'])
R(im,0,52,GW,23,c['ink'])
for k in range(18): R(im,60-k,34+k,2*k+1,1,c['teal'])
R(im,59,40,3,12,c['navy'])
R(im,88,48,10,2,c['dark']); R(im,90,44,6,4,c['wine']); R(im,91,41,4,4,c['ochre']); R(im,92,39,2,2,c['paper'])
sparkle(im,120,10,c['paper'])
finish(im,'fri_06.jpg',seed=6)

# 07 Retro computer: a beige pixel monitor showing a wave, keyboard and mouse
im=grid(c['skyb'])
R(im,0,60,GW,15,c['prussian'])
R(im,44,8,62,44,c['clay']); R(im,48,12,54,34,c['ink']); R(im,50,14,50,30,c['navy'])
for y in range(30,44):
    for x in range(50,100):
        k=(y-30+round(1.5*np.sin(2*np.pi*x/9)))//3; im.putpixel((x,y),[c['teal'],c['prussian'],c['skyb']][k%3])
R(im,88,17,6,6,c['ochre'])
R(im,62,52,26,4,c['clay']); R(im,54,56,42,4,c['clay'])
R(im,40,62,64,8,c['paper']); 
for k in range(10): R(im,43+k*6,64,4,2,c['mist']); R(im,43+k*6,67,4,1,c['mist'])
R(im,112,62,8,10,c['paper']); R(im,115,62,2,4,c['mist'])
R(im,98,54,3,1,c['ochre']); R(im,102,54,2,1,c['moss'])
sparkle(im,22,16)
finish(im,'fri_07.jpg',seed=7)

# 08 The weekend calendar: a pixel calendar page with the last two days lit up
im=grid(c['pine'])
R(im,35,6,80,64,c['paper']); R(im,35,6,80,10,c['wine'])
for x in (48,100): R(im,x,3,3,7,c['ink'])
for row in range(5):
    for col in range(7):
        x=39+col*11; y=19+row*10
        if row==4 and col>2: continue
        weekend=col>=5
        R(im,x,y,9,8,c['ochre'] if weekend and row==2 else (c['mist'] if not weekend else c['foamb']))

sparkle(im,128,14); sparkle(im,20,58,c['skyb'])
for x in range(0,GW):
    yy=70+round(1.5*np.sin(2*np.pi*x/12)); R(im,x,yy,1,GH-yy,c['teal'])
finish(im,'fri_08.jpg',seed=8)
print('done')

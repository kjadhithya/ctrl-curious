"""Thursday · Field notes — 8 quiet stippled landscapes. 01 is the current template image."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
OUT = '/home/claude/ctrl-curious/assets/email/days/thu/'
rng = np.random.default_rng(7)
def hx(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
INK,PAPER,MAUVE,PLUM,WINE,CLAY,OCHRE=map(hx,['2E1F25','F4EEE8','C9A7B5','7E4B6B','8A2E3B','D9C3B7','C8902F'])
INDIGO,PRUSSIAN,SKYB,TEAL,PINE,MOSS,NAVY,MIST=map(hx,['1C3050','2B4C6F','7C9EB8','24585C','264A3E','4F6A3A','172338','C9D6DC'])
W,H=1200,600
X,Y=np.meshgrid(np.arange(W),np.arange(H))
def bn(r):
    n=Image.fromarray((rng.random((H,W))*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r)); a=np.asarray(n,float); return (a-a.min())/(a.max()-a.min()+1e-6)
def fbm(): return .5*bn(18)+.3*bn(6)+.2*bn(2)
def mix(a,b,t): return a[None,None]*(1-t[...,None])+b[None,None]*t[...,None]
def sky(top,bot,power=1.0,amt=0.3):
    t=np.clip((np.linspace(0,1,H)[:,None]**power)*np.ones((1,W))*0.9+fbm()*amt-amt/2,0,1); return mix(top,bot,t)
def stip(img,mask,col,dens=0.9):
    dots=rng.random((H,W))<dens; img[mask&dots]=col; img[mask&~dots]=col*.7+PAPER*.3
def sun(img,cx,cy,r,col=WINE,dens=None):
    m=((X-cx)**2+(Y-cy)**2)<r**2; st=rng.random((H,W))<(0.86+0.12*fbm())
    img[m&st]=col; img[m&~st]=col*.6+PAPER*.4; return m
def ridge(y0,amp,seed,freq,jag=1.4):
    r=np.random.default_rng(seed); xs=np.arange(W)
    y=y0+amp*np.sin(xs/freq+r.random()*6)+.45*amp*np.sin(xs/(freq/2.7)+r.random()*6)
    y+=np.cumsum(r.normal(0,jag,W)); y-=np.linspace(0,y[-1]-y[0],W)*.5; return y
def below(y): return Y>y[None,:]
def save(img,name,amt=26):
    a=img+rng.normal(0,amt,img.shape[:2])[...,None]
    Image.fromarray(np.clip(a,0,255).astype('uint8')).save(OUT+name,quality=86)

# 01 current template image: wine sun over teal, moss and indigo ridges (kept as is, framed to 1200x600)
im=Image.open('/home/claude/ctrl-curious/assets/email/sun_bluegreen.jpg').convert('RGB')
im=im.resize((1200,744),Image.LANCZOS); top=int(744*0.55-300); im.crop((0,top,1200,top+600)).save(OUT+'thu_01.jpg',quality=86)

# 02 Terraces: curved green terraces stepping down, low ochre sun
img=sky(MIST*0.5+PAPER*0.5,PAPER,1.0); sun(img,300,300,90,OCHRE)
cols=[TEAL,PINE,MOSS,TEAL*0.8+PINE*0.2,PINE*0.9,MOSS*0.85]
for i,col in enumerate(cols):
    y0=300+i*52; yy=y0+40*np.sin(np.arange(W)/260+i*0.5)+10*np.sin(np.arange(W)/70+i)
    stip(img,below(yy),col,0.9+i*0.01)
    edge=(np.abs(Y-yy[None,:])<2); img[edge]=SKYB*0.6+PAPER*0.4
save(img,'thu_02.jpg')

# 03 River valley: a winding pale river through layered hills, wine sun
img=sky(SKYB*0.35+PAPER*0.65,PAPER,1.0); sun(img,820,210,110)
for y0,amp,seed,freq,col,d in [(300,40,11,140,PRUSSIAN,.9),(370,34,12,100,TEAL,.92),(440,28,13,80,PINE,.94)]:
    stip(img,below(ridge(y0,amp,seed,freq)),col,d)
t=np.linspace(0,1,H); cx=600+260*np.sin(t*7+1)*t; wdt=2+60*t**1.6
riv=(np.abs(X-cx[:,None])<wdt[:,None])&(Y>330)
img[riv]=MIST*0.8+PAPER*0.2
save(img,'thu_03.jpg')

# 04 Still lake: one mountain and the sun, mirrored in calm water
img=sky(PAPER,MIST*0.6+PAPER*0.4,1.0); m=sun(img,760,170,80)
xs=np.arange(W)
ml=140+0.78*np.abs(xs-560)+10*np.sin(xs/28)*(np.abs(xs-560)>40)
mt=below(ml); stip(img,mt,INDIGO,0.93)
ml2=250+0.6*np.abs(xs-930)+8*np.sin(xs/22)
stip(img,below(ml2)&~mt,PRUSSIAN,0.92)
img[mt&(Y<ml[None,:]+34+8*np.sin(X/14))&(Y<200)]=SKYB*0.55+PAPER*0.45
hz=380; img[hz:]=img[hz-1::-1][:H-hz]*0.65+TEAL*0.35
for y in range(hz+8,H,14):
    x0=rng.integers(0,200)
    while x0<W:
        L=rng.integers(40,160); img[y:y+2,x0:x0+L]=img[y:y+2,x0:x0+L]*0.6+PAPER*0.4; x0+=L+rng.integers(40,140)
save(img,'thu_04.jpg')

# 05 Contour hills: hill layers drawn with woodblock contour lines, like slow waves of land
img=sky(PAPER,CLAY,1.2); sun(img,600,250,120)
for i,(y0,amp,seed,freq,col,line) in enumerate([(320,40,21,160,PRUSSIAN,SKYB),(400,34,22,120,TEAL,MIST),(480,26,23,90,PINE,MOSS*0.6+PAPER*0.4)]):
    yy=ridge(y0,amp,seed,freq,1.0); mk=below(yy); stip(img,mk,col,0.94)
    for k in range(1,8):
        e=mk&(np.abs(Y-(yy[None,:]+k*14))<1.2); img[e]=line
save(img,'thu_05.jpg')

# 06 Cliff coast: a dark cliff, a calm sea with one small wave, a low wine sun
img=sky(SKYB*0.3+PAPER*0.7,PAPER,1.0); sun(img,420,330,100)
sea=Y>380; stip(img,sea,PRUSSIAN,0.92)
for y in range(392,H,16):
    row=(np.abs(Y-(y+4*np.sin(X/40+y)))<1.2)&sea; img[row]=SKYB
yy=Y.astype(float); xx=X.astype(float)
hz=380
face=800 - 95*np.clip((yy-240)/(hz-240),0,1)**1.8 + 4*np.sin(yy/9) + 2*np.sin(yy/3.3)
top=242 - 82*np.clip((xx-795)/405,0,1)**0.55 + 3*np.sin(xx/23)
cl=(xx>face)&(yy>top)&(yy<=hz)
stip(img,cl,PINE,0.94)
grass=cl&(yy<top+7); img[grass]=MOSS
ref=(yy>hz)&(yy<hz+70)&(xx>800-95-30*((yy-hz)/70))
img[ref]=img[ref]*0.55+PINE*0.45
for rx,ry,rr in [(690,hz+2,12),(668,hz+3,7)]:
    rock=((xx-rx)**2/(rr*1.5)**2+(yy-ry)**2/rr**2<1)&(yy<=hz+2)
    img[rock]=PINE*0.8+INK*0.2
save(img,'thu_06.jpg')

# 07 Rain over hills: soft mist bands and slanted rain, muted sun
img=sky(MIST,PAPER,1.0); sun(img,860,180,80,WINE*0.8+MAUVE*0.2)
for y0,amp,seed,freq,col,d in [(300,30,31,150,SKYB*0.8+PRUSSIAN*0.2,.86),(380,30,32,110,TEAL*0.8+MIST*0.2,.9),(460,26,33,90,PINE,.94)]:
    stip(img,below(ridge(y0,amp,seed,freq)),col,d)
    wgt=np.exp(-((Y-(y0+20))/22.0)**2)[...,None]*0.35; img[:]=img*(1-wgt)+MIST[None,None]*wgt
pil=Image.fromarray(np.clip(img,0,255).astype('uint8')); d=ImageDraw.Draw(pil)
for _ in range(240):
    x,y=rng.integers(-100,1200),rng.integers(-30,600); d.line([(x,y),(x+10,y+30)],fill=(244,238,232),width=1)
img=np.asarray(pil,float)
save(img,'thu_07.jpg')

# 08 Open sea: a large wine sun, a calm indigo sea and one small sail
img=sky(PAPER,CLAY,1.3); sun(img,600,330,170)
sea=Y>360; stip(img,sea,INDIGO,0.93)
for y in range(370,H,13):
    x0=rng.integers(0,120)
    while x0<W:
        L=rng.integers(60,220); img[y:y+2,x0:x0+L]=PRUSSIAN*0.5+SKYB*0.5; x0+=L+rng.integers(30,120)
pil=Image.fromarray(np.clip(img,0,255).astype('uint8')); d=ImageDraw.Draw(pil)
d.polygon([(880,352),(900,300),(902,352)],fill=(46,31,37)); d.polygon([(905,350),(905,312),(930,350)],fill=(244,238,232))
d.polygon([(868,354),(940,354),(930,364),(876,364)],fill=(46,31,37))
img=np.asarray(pil,float)
save(img,'thu_08.jpg')
print('done')

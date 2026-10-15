import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
def hx(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
INK,PAPER,MAUVE,PLUM,WINE,CLAY=map(hx,['2E1F25','F4EEE8','C9A7B5','7E4B6B','8A2E3B','D9C3B7'])
INDIGO,PRUSSIAN,SKYB,TEAL,PINE,MOSS,NAVY=map(hx,['1C3050','2B4C6F','7C9EB8','24585C','264A3E','4F6A3A','172338'])
def bn(w,h,r):
    n=Image.fromarray((rng.random((h,w))*255).astype('uint8')).filter(ImageFilter.GaussianBlur(r)); a=np.asarray(n,float); return (a-a.min())/(a.max()-a.min()+1e-6)
def fbm(w,h): return .5*bn(w,h,18)+.3*bn(w,h,6)+.2*bn(w,h,2)
def mix(a,b,t): return a[None,None]*(1-t[...,None])+b[None,None]*t[...,None]
def grainy(i,a=28): return i+rng.normal(0,a,i.shape[:2])[...,None]
def save(a,n): Image.fromarray(np.clip(a,0,255).astype('uint8')).save(n,quality=86)

# sun over ridges: pale sky with a hint of blue, wine sun, teal / pine / indigo ridges
W,H=1000,620
base=mix(PAPER,SKYB*0.35+PAPER*0.65,np.clip(np.linspace(1,0,H)[:,None]*np.ones((1,W))*0.9+fbm(W,H)*0.3,0,1))
X,Y=np.meshgrid(np.arange(W),np.arange(H))
sun=((X-640)**2+(Y-250)**2)<190**2
st=rng.random((H,W))<(0.86+0.12*fbm(W,H))
img=base.copy(); img[sun&st]=WINE; img[sun&~st]=WINE*.6+PAPER*.4
def ridge(y0,amp,seed,freq):
    r=np.random.default_rng(seed); xs=np.arange(W)
    y=y0+amp*np.sin(xs/freq+r.random()*6)+.45*amp*np.sin(xs/(freq/2.7)+r.random()*6)
    y+=np.cumsum(r.normal(0,1.4,W)); y-=np.linspace(0,y[-1]-y[0],W)*.5; return y
for y0,amp,seed,freq,col,dens in [(380,50,1,120,TEAL,.9),(450,40,2,90,MOSS*.7+PINE*.3,.93),(520,30,3,70,INDIGO,.97)]:
    rr=ridge(y0,amp,seed,freq); m=Y>rr[None,:]; dots=rng.random((H,W))<dens
    img[m&dots]=col; img[m&~dots]=col*.7+PAPER*.3
save(grainy(img,26),'sun_bg.jpg')

# night: indigo sky warming to plum near the horizon, blush moon, pine ridge
W,H=700,520
t=np.clip(fbm(W,H)*.35+np.linspace(0,1,H)[:,None]*.9,0,1)
img=mix(NAVY,PLUM*.8,t)
X,Y=np.meshgrid(np.arange(W),np.arange(H))
moon=((X-470)**2+(Y-190)**2)<130**2
img[moon]=mix(MAUVE*.5+CLAY*.5,PAPER,fbm(W,H)*.6)[moon]
rr=400+50*np.sin(np.arange(W)/70)+20*np.sin(np.arange(W)/23)
rr2=440+30*np.sin(np.arange(W)/45+2)+12*np.sin(np.arange(W)/17)
img[Y>rr[None,:]]=PINE
img[Y>rr2[None,:]]=NAVY*.7+INK*.3
for _ in range(50):
    x,y=rng.integers(0,W),rng.integers(0,330)
    if not moon[y,x]: img[y:y+2,x:x+2]=PAPER
save(grainy(img,30),'night_bg.jpg')
print('ok')

"""ETOI cafe bed: original bossa-style piece, fully synthesised (no samples). seed fixed."""
import numpy as np
from scipy.signal import lfilter, butter, fftconvolve
SR=48000
rng=np.random.default_rng(11)
def m2f(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2):
    b,a=butter(o,fc/(SR/2)); return lfilter(b,a,x)
def hp(x,fc,o=2):
    b,a=butter(o,fc/(SR/2),'high'); return lfilter(b,a,x)
def nylon(f,dur,vel):
    n=int(dur*SR); D=SR/f; Di=int(D-.5); frac=D-.5-Di
    ex=np.zeros(n); L=Di+1
    burst=rng.uniform(-1,1,L); burst=lfilter([.6],[1,-.4],burst)
    # pluck-position comb gives a warmer nylon tone
    p=max(1,int(L*.22)); burst=burst-np.roll(burst,p)*.85
    ex[:L]=burst
    g=.9965 if f<250 else .9945
    a=np.zeros(Di+2); a[0]=1; a[Di]=-g*(1-frac)*.5; a[Di+1]=-g*(frac*.5+.5*(1-frac)); 
    y=lfilter([1],np.r_[a,-g*frac*.5],ex)
    y=lp(y,3200)
    env=np.minimum(1,np.arange(n)/(.002*SR))*np.exp(-np.arange(n)/SR/1.1)
    return y*env*vel*.7
def epiano(f,dur,vel):
    n=int(dur*SR); t=np.arange(n)/SR
    I=(.9+1.1*vel)*np.exp(-t/.7); tine=.12*vel*np.exp(-t/.09)*np.sin(2*np.pi*f*14*t)
    y=np.sin(2*np.pi*f*t+I*np.sin(2*np.pi*f*t))+.35*np.sin(2*np.pi*2*f*t)*np.exp(-t/.8)+tine
    env=np.minimum(1,t/.004)*np.exp(-t/1.5)*np.minimum(1,(dur-t)/.08)
    return y*env*vel*.34
def vibes(f,dur,vel):
    n=int(dur*SR); t=np.arange(n)/SR
    y=np.sin(2*np.pi*f*t)+.18*np.sin(2*np.pi*4*f*t)*np.exp(-t/.25)
    env=np.minimum(1,t/.003)*np.exp(-t/1.2)*np.minimum(1,(dur-t)/.1)*(1+.22*np.sin(2*np.pi*4.6*t))
    return y*env*vel*.3
def bass(f,dur,vel):
    n=int(dur*SR); t=np.arange(n)/SR
    y=np.sin(2*np.pi*f*t)+.45*np.sin(2*np.pi*2*f*t)*np.exp(-t/.5)+.16*np.sin(2*np.pi*3*f*t)*np.exp(-t/.2)
    env=np.minimum(1,t/.008)*np.exp(-t/.85)*np.minimum(1,(dur-t)/.05)
    return y*env*vel*.75
def shaker(dur,vel):
    n=int(dur*SR); x=rng.normal(0,1,n); x=hp(x,5200); t=np.arange(n)/SR
    return x*np.exp(-t/.022)*np.minimum(1,t/.004)*vel*.11
def rim(vel):
    n=int(.09*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*1700*t)*.6+hp(rng.normal(0,1,n),900)*.4)*np.exp(-t/.012)*vel*.16
def kick(vel):
    n=int(.22*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*(52*t+30*(1-np.exp(-t/.03))*.03))*np.exp(-t/.09)*vel*.34
# rootless, voice-led voicings
CH={'F9':(41,[57,60,64,67]),'F6':(41,[57,62,65,67]),'Dm9':(38,[57,60,64,65]),'Gm9':(43,[58,62,65,69]),
    'C13':(36,[58,62,64,69]),'Am7':(45,[55,60,64,67]),'D9':(38,[54,60,64,69]),'Bb7M':(46,[57,62,65,69]),
    'Eb9':(39,[55,61,65,70]),'C9s':(36,[58,62,65,67]),'E7':(40,[56,62,64,71])}
A=['F9','Dm9','Gm9','C13','Am7','D9','Gm9','C9s']
B=['Bb7M','Eb9','Am7','D9','Gm9','C13','F6','C13']
def build(T_end,T_total,T_guess_bpm=84):
    forms=A+A+B+A
    bars_target=max(8,round(T_end/(4*60/T_guess_bpm)))
    bpm=bars_target*4*60/T_end; bar=4*60/bpm; beat=bar/4
    seq=(forms*4)[:bars_target]
    # last bar before the end resolves to F
    seq=seq[:-1]+['C13'] if len(seq)>1 else seq
    N=int((T_total+3)*SR)
    tr={k:np.zeros((N,2)) for k in 'gebdvs'}
    def add(k,y,t,pan=0.):
        a=int(t*SR); 
        if a<0 or a>=N: return
        e=min(N,a+len(y)); l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
        tr[k][a:e,0]+=y[:e-a]*l; tr[k][a:e,1]+=y[:e-a]*r
    hum=lambda s=.009:float(rng.normal(0,s))
    # bossa guitar syncopation (beats), bass 1 & 3 with pickup
    GT=[0,.5*3,1.5*2,3.5]; 
    GT=[0,1.5,3,3.5+.0]
    for b,name in enumerate(seq):
        t0=b*bar; root,voice=CH[name]; nxt=CH[seq[b+1]] if b+1<len(seq) else CH['F9']
        # bass
        add('b',bass(m2f(root+12 if root<40 else root),beat*1.6,.95),t0+hum(.004),0)
        add('b',bass(m2f((root+7)+12 if root<40 else root+7),beat*1.4,.72),t0+2*beat+hum(.004),0)
        add('b',bass(m2f(nxt[0]+12 if nxt[0]<40 else nxt[0]),beat*.8,.55),t0+3.5*beat+hum(.004),0)
        # guitar comp: strummed with small rake
        for i,g in enumerate([0,1.5,3,3.5]):
            v=[.8,.62,.66,.55][i]; notes=voice if g<3.5 else nxt[1]
            for j,m in enumerate(notes):
                add('g',nylon(m2f(m),1.9,v*(.85+.15*j/3)),t0+g*beat+j*.012+hum(.005),-.28)
        # electric piano: soft colour on 1 only, every chord
        for m in voice[1:]:
            add('e',epiano(m2f(m+12),bar*.9,.42),t0+hum(.006),.34)
        # percussion
        for s in range(8):
            add('s',shaker(.12,[.9,.5,.7,.5][s%4]*.9),t0+s*beat/2+hum(.004),.2)
        add('s',rim(.55),t0+1.5*beat+hum(.003),-.1); add('s',rim(.45),t0+3*beat+hum(.003),-.1)
        add('d',kick(.8),t0+hum(.003),0); add('d',kick(.55),t0+2*beat+hum(.003),0)
    # melody: sparse, pentatonic, stays high and out of the voice's way
    mel={3:[(0,76),(1.5,74),(2.5,72)],7:[(0,74),(1,77),(2.5,76)],
         11:[(0,81),(1.5,79)],15:[(0,76),(1,74),(2,72),(3,69)],19:[(0,77),(2,76)],23:[(.5,74),(2.5,72)],27:[(0,72),(1.5,76),(3,74)]}
    for b,ph in mel.items():
        if b<len(seq):
            for g,m in ph: add('v',vibes(m2f(m+12),2.2,.55),b*bar+g*beat+hum(.008),.1)
    # final chord rings over the logo
    te=len(seq)*bar
    add('b',bass(m2f(53),3.5,.9),te,0)
    for j,m in enumerate(CH['F9'][1]+[72]):
        add('g',nylon(m2f(m),3.6,.8),te+j*.03,-.28); add('e',epiano(m2f(m+12),3.4,.45),te+j*.01,.34)
    add('v',vibes(m2f(84),3.2,.5),te+.15,.1)
    g={'g':.55,'e':.42,'b':.52,'d':.36,'v':.3,'s':.5}
    dry=sum(tr[k]*g[k] for k in tr)
    # small room
    L=int(1.5*SR); ir=np.exp(-np.arange(L)/SR/.42)
    irL=lp(rng.normal(0,1,L),5200)*ir; irR=lp(rng.normal(0,1,L),5200)*ir
    irL/=np.sqrt((irL**2).sum()); irR/=np.sqrt((irR**2).sum())
    wet=np.c_[fftconvolve(dry[:,0],irL)[:N],fftconvolve(dry[:,1],irR)[:N]]
    x=dry+wet*.28
    x[:,0]=hp(x[:,0],45); x[:,1]=hp(x[:,1],45)
    x=x[:int(T_total*SR)]
    x/=np.max(np.abs(x)); print('bpm',round(bpm,1),'bars',len(seq),'bar',round(bar,3),'end chord at',round(te,2))
    return x,bpm

"""SFX simples por corte para vídeos virais (sintetizados, sem arquivos de terceiros).
Uso: python mix_viral.py tempo.js narracao.wav saida.wav [sino_beats] [impacto=beat:palavra]
"""
import json, sys, re, numpy as np, soundfile as sf
tempo_js, voz_p, saida = sys.argv[1:4]
T = json.loads(re.sub(r'^window\.TEMPO=|;\s*$', '', open(tempo_js).read().strip()))
voz, SR = sf.read(voz_p)
rng = np.random.default_rng(2)
def whoosh(d=.35):
    n=int(d*SR); x=np.convolve(rng.normal(0,1,n),np.ones(24)/24,'same'); return x*np.sin(np.linspace(0,np.pi,n))**2*1.4
def sino(f=1320,d=1.1):
    t=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*4)
def crunch(d=.25):
    t=np.arange(int(d*SR))/SR; return rng.normal(0,1,len(t))*np.exp(-t*18)*(1+np.sin(2*np.pi*90*t))
mix=np.zeros(len(voz)+SR)
def add(sig,t,g):
    i=int(t*SR); j=min(len(mix),i+len(sig)); mix[i:j]+=sig[:j-i]*g
B=T['beats']
for i,b in enumerate(B[1:],1): add(whoosh(),max(0,b['t0']-.12),.05)
sinos=[int(x) for x in (sys.argv[4].split(',') if len(sys.argv)>4 else [])]
for i in sinos: add(sino(),B[i]['t0'],.12)
for arg in sys.argv[5:]:
    bi,pal=arg.split(':'); bi=int(bi)
    w=next(x for x in B[bi]['words'] if x['w'].lower().startswith(pal)); add(crunch(),w['t0'],.35)
v=voz/np.max(np.abs(voz))*.85; out=np.zeros(len(mix)); out[:len(v)]+=v; out+=mix; out=out[:len(v)]
sf.write(saida,out/max(1,np.max(np.abs(out))/.95),SR); print('ok',round(len(out)/SR,1),'s')

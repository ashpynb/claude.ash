"""Mistura narração + SFX sintetizados (clique de giro, whoosh de x/y).

Uso: python mixar.py eventos.json narracao.wav saida.wav
SFX gerados por código (sem arquivos de terceiros), ~16 dB abaixo da voz.
"""
import json, sys, numpy as np, soundfile as sf
ev, voz_p, saida = sys.argv[1:4]
voz, SR = sf.read(voz_p)
if voz.ndim > 1: voz = voz.mean(1)
rng = np.random.default_rng(1)
def clique(f=1800, d=.035):
    t = np.arange(int(d*SR))/SR
    return np.sin(2*np.pi*f*t)*np.exp(-t*90) + rng.normal(0,.3,len(t))*np.exp(-t*160)
def whoosh(d=.6):
    n = int(d*SR); x = rng.normal(0,1,n)
    env = np.sin(np.linspace(0,np.pi,n))**2
    # passa-baixa móvel simples (média de janela variável)
    y = np.convolve(x, np.ones(18)/18, mode='same')
    return y*env*1.6
mix = np.zeros(len(voz)+SR)
def add(sig, t, g):
    i = int(t*SR); j = min(len(mix), i+len(sig)); mix[i:j] += sig[:j-i]*g
E = json.load(open(ev))
DUR = {1:.62, 2:.95}
for e in E["EV"]:
    if e["tipo"] != "mov": continue
    m = e["m"]
    if m[0] in "xy":
        add(whoosh(.7), e["t"], .10)
    else:
        d = e.get("dur") or (.95 if m.endswith("2") else .62)
        add(clique(1900), e["t"], .16); add(clique(1300), e["t"]+d-.02, .22)
voz_n = voz/np.max(np.abs(voz))*0.85
out = np.zeros(len(mix)); out[:len(voz_n)] += voz_n; out += mix
out = out[:len(voz_n)]
out = out/max(1, np.max(np.abs(out))/0.95)
sf.write(saida, out, SR)
print("ok", round(len(out)/SR,2), "s")

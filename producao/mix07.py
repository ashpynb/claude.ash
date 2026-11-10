"""Som do viral 07 (Sérgio): efeitos sintetizados por evento da página (eventos.json). SEM MÚSICA.
Uso: python mix07.py narracao.wav eventos.json saida.wav
Tipos: whoosh boing boing2 pop pipoca buzz tic marreta flip tchan queda queda2 tum zum sino
"""
import json, sys, numpy as np, soundfile as sf
voz, SR = sf.read(sys.argv[1]); voz = voz if voz.ndim == 1 else voz.mean(1)
EV = json.load(open(sys.argv[2]))['EV']
rng = np.random.default_rng(7); N = len(voz) + SR; mix = np.zeros(N)
def add(sig, t, g):
    i = max(0, int(t * SR)); j = min(N, i + len(sig)); mix[i:j] += sig[:j - i] * g
def tt(d): return np.arange(int(d * SR)) / SR
def env(t, a=.005, d=.2): return np.minimum(1, t / a) * np.exp(-t / d)
def lp(x, k): return np.convolve(x, np.ones(k) / k, 'same')
def tom(fr, t): return np.sin(2 * np.pi * np.cumsum(fr) / SR)
def whoosh(d=.32): t = tt(d); return lp(rng.normal(0, 1, len(t)), 18) * np.sin(np.linspace(0, np.pi, len(t))) ** 2 * 1.6
def pop(f=900, d=.12): t = tt(d); return tom(f * (1 + 2 * np.exp(-t * 40)), t) * env(t, .002, .04)
def boing(d=.55, f=260): t = tt(d); return tom(f + 140 * np.sin(2 * np.pi * 8 * t) * np.exp(-t * 3), t) * env(t, .003, .2)
def boing2(): return boing(.45, 420)
def pipoca():
    s = np.zeros(int(1.4 * SR))
    for k in range(9):
        b = pop(700 + rng.random() * 700, .07); i = int(rng.random() * (len(s) - len(b))); s[i:i + len(b)] += b * (.5 + rng.random() * .5)
    return s
def buzz(): t = tt(.35); return np.sign(np.sin(2 * np.pi * 140 * t)) * .5 * env(t, .005, .3)
def tic(): t = tt(.06); return rng.normal(0, 1, len(t)) * env(t, .001, .008) + np.sin(2 * np.pi * 2400 * t) * env(t, .001, .02)
def marreta(): t = tt(.4); return (np.sin(2 * np.pi * 90 * t) + lp(rng.normal(0, 1, len(t)), 4) * .6) * env(t, .002, .07)
def flip():
    s = np.zeros(int(1.0 * SR))
    for k in range(9): b = lp(rng.normal(0, 1, int(.05 * SR)), 3) * np.hanning(int(.05 * SR)); i = int(k * .1 * SR); s[i:i + len(b)] += b
    return s
def tchan(): t = tt(.9); return sum(np.sin(2 * np.pi * f * t) for f in (392, 494, 587)) / 3 * env(t, .01, .35)
def queda(d=.7, f0=900, f1=180): t = tt(d); return tom(f0 * (f1 / f0) ** (t / d), t) * env(t, .01, .5) * .8
def queda2(): return queda(.5, 700, 300)
def tum(): t = tt(.6); return tom(120 * np.exp(-t * 3) + 50, t) * env(t, .003, .25)
def zum(): t = tt(1.4); return (np.sin(2 * np.pi * 70 * t) + .4 * np.sin(2 * np.pi * 73 * t)) * np.minimum(1, t / .6) * np.minimum(1, (1.4 - t) / .3)
def sino(): t = tt(1.1); return (np.sin(2 * np.pi * 1320 * t) + .5 * np.sin(2 * np.pi * 2650 * t)) * np.exp(-t * 4)
GAN = dict(whoosh=.05, boing=.22, boing2=.18, pop=.2, pipoca=.12, buzz=.08, tic=.18, marreta=.3, flip=.12, tchan=.12, queda=.13, queda2=.12, tum=.3, zum=.1, sino=.08)
for e in EV:
    f = globals()[e['tipo']]; add(f(), e['t'], GAN[e['tipo']])
v = voz / np.max(np.abs(voz)) * .85; out = np.zeros(N); out[:len(v)] += v; out += mix; out = out[:len(v)]
sf.write(sys.argv[3], out / max(1, np.max(np.abs(out)) / .95), SR); print('ok', round(len(out) / SR, 1), 's', len(EV), 'efeitos')

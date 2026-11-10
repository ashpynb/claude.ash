"""Som do viral 04 (ouriço): ambiente subaquático + efeitos por ação. SEM MÚSICA (regra da usuária).
Todos os sons sintetizados aqui (sem arquivos de terceiros). Hit cai na pausa DEPOIS da palavra (ficha 03).
Uso: python mix_v4.py tempo.js narracao.wav saida.wav
"""
import json, re, sys, numpy as np, soundfile as sf
T = json.loads(re.sub(r'^window\.TEMPO=|;\s*$', '', open(sys.argv[1]).read().strip()))
voz, SR = sf.read(sys.argv[2]); voz = voz if voz.ndim == 1 else voz.mean(1)
rng = np.random.default_rng(4); N = len(voz) + SR
mix = np.zeros(N)
def add(sig, t, g):
    i = max(0, int(t * SR)); j = min(N, i + len(sig)); mix[i:j] += sig[:j - i] * g
def env(n, a=.005, d=.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def lowpass(x, k): return np.convolve(x, np.ones(k) / k, 'same')
def whoosh(d=.35): n = int(d * SR); return lowpass(rng.normal(0, 1, n), 24) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.5
def pop(f=900, d=.12):
    n = int(d * SR); t = np.arange(n) / SR; fr = f * (1 + 2 * np.exp(-t * 40)); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, .002, .04)
def boing(d=.5):
    n = int(d * SR); t = np.arange(n) / SR; fr = 300 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 3); return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, .003, .18)
def rrrip(d=.45):
    n = int(d * SR); t = np.arange(n) / SR; x = rng.normal(0, 1, n) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 70 * t))); return lowpass(x, 3) * np.minimum(1, t / .01) * np.exp(-t / .3)
def moedor(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; x = np.sin(2 * np.pi * 95 * t) * .6 + np.sign(np.sin(2 * np.pi * 47 * t)) * .25 + rng.normal(0, .3, n)
    return lowpass(x, 6) * np.minimum(1, t / .08) * np.minimum(1, (d - t) / .2)
def bolhas(d=.8):
    s = np.zeros(int(d * SR))
    for k in range(7):
        b = pop(500 + rng.random() * 900, .06); i = int(rng.random() * (len(s) - len(b))); s[i:i + len(b)] += b * (.5 + rng.random() * .5)
    return s
def ambiente(n):
    x = lowpass(rng.normal(0, 1, n), 120); x = x / np.max(np.abs(x)); return x
B = T['beats']
def palavra(bi, a, n=1):
    c = 0
    for w in B[bi]['words']:
        if w['w'].lower().startswith(a):
            c += 1
            if c == n: return w
    return None
add(ambiente(N), 0, .05)
for i, b in enumerate(B[1:], 1): add(whoosh(), max(0, b['t0'] - .12), .05)
CART = {3: 'armadura', 5: 'triturador', 7: 'vulcão', 9: 'velcro', 11: 'câmera', 13: 'boné', 16: 'aposentadoria'}
for bi, pal in CART.items():
    w = palavra(bi, pal)
    if w: add(pop(1100), w['t1'] + .05, .22)
for bi in (0, len(B) - 1): add(boing(), B[bi]['t0'] + 1.6, .16); add(bolhas(), B[bi]['t0'] + .2, .08)
w = palavra(5, 'triturador');  add(moedor(), B[5]['t0'], .07)
w = palavra(9, 'velcro');      add(rrrip(), (w['t1'] if w else B[9]['t0']) + .02, .2)
w = palavra(7, 'vulcão');      add(bolhas(1.2), (w['t1'] if w else B[7]['t0']) + .05, .12)
v = voz / np.max(np.abs(voz)) * .85; out = np.zeros(N); out[:len(v)] += v; out += mix; out = out[:len(v)]
sf.write(sys.argv[3], out / max(1, np.max(np.abs(out)) / .95), SR); print('ok', round(len(out) / SR, 1), 's')

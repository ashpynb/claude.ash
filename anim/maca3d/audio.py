"""Trilha + efeitos sintetizados (sem samples externos) a partir de timeline.json.
Uso: python3 audio.py saida.wav
"""
import json, sys, wave, pathlib
import numpy as np

SR = 48000
AQUI = pathlib.Path(__file__).parent
TL = json.loads((AQUI / "timeline.json").read_text())
DUR = TL["duracao"]
N = int(SR * DUR)
rng = np.random.default_rng(7)


def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)


def tom(freq, dur, a=0.005, r=0.2, forma="sin"):
    n = int(SR * dur); t = np.arange(n) / SR
    if forma == "sin": w = np.sin(2 * np.pi * freq * t)
    elif forma == "tri": w = 2 * np.abs(2 * ((freq * t) % 1) - 1) - 1
    else: w = np.sign(np.sin(2 * np.pi * freq * t)) * .6
    return w * env(n, a, r)


def ruido(dur, r=0.1):
    n = int(SR * dur); return rng.standard_normal(n) * env(n, .002, r)


def passa_baixa(x, k):
    y = np.copy(x)
    for i in range(1, len(y)): y[i] = y[i - 1] + k * (y[i] - y[i - 1])
    return y


def J(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o


def soma(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[: j - i] * g


# ---------- Música: 112 bpm, Dó maior, I–V–vi–IV ----------
mus = np.zeros(N)
BPM = 112; b = 60 / BPM
acordes = [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]
baixos = [65.4, 49.0, 55.0, 43.7]
kick = J(tom(55, .35, .001, .12), tom(110, .05, .001, .02) * .5)
snare = J(passa_baixa(ruido(.25, .08), .5) * .6, tom(190, .12, .001, .05) * .3)
hat = ruido(.05, .015) - passa_baixa(ruido(.05, .015), .3)
t = 0.0; nbeat = 0
while t < DUR:
    compasso = int(nbeat // 4) % 4
    intro = t < 3.0  # gancho: só batida seca
    soma(mus, kick, t, .9)
    if nbeat % 4 in (1, 3) and not intro: soma(mus, snare, t, .55)
    for h in (0, .5): soma(mus, hat, t + h * b, .18)
    if not intro:
        soma(mus, tom(baixos[compasso], b * .9, .01, .35, "tri"), t, .5)
        nota = acordes[compasso][nbeat % 3] * 2
        soma(mus, tom(nota, b * .45, .003, .12, "sq"), t + b * .5, .12)
        if nbeat % 4 == 0:
            for f in acordes[compasso]: soma(mus, tom(f, b * 4, .25, 1.4, "tri"), t, .07)
    t += b; nbeat += 1
# fim: corte seco no último segundo para emendar o loop
mus[int((DUR - .15) * SR):] *= np.linspace(1, 0, N - int((DUR - .15) * SR))

# ---------- Efeitos ----------
fx = np.zeros(N)
def whoosh(d=.45):
    x = ruido(d, d); n = len(x); k = np.linspace(.02, .4, n)
    y = np.zeros(n)
    for i in range(1, n): y[i] = y[i - 1] + k[i] * (x[i] - y[i - 1])
    return y * np.sin(np.linspace(0, np.pi, n)) * 1.4
SFX = {
    "impacto": lambda: J(tom(48, .6, .001, .25) * 1.2, passa_baixa(ruido(.4, .12), .2) * .8),
    "whoosh": whoosh,
    "pop": lambda: J(tom(880, .12, .001, .04), tom(1320, .1, .001, .03) * .5),
    "ding": lambda: J(tom(1568, .9, .001, .35) * .6, tom(2093, .7, .001, .25) * .3),
    "alerta": lambda: np.concatenate([tom(740, .18, .002, .2, "sq"), tom(554, .22, .002, .2, "sq")]) * .5,
}
for bt in TL["beats"]:
    s = bt.get("sfx")
    if s == "contagem":
        for tt in (59.5, 60.5, 61.5): soma(fx, tom(1046, .15, .001, .05, "sq"), tt, .35)
        soma(fx, SFX["impacto"](), 62.6, 1.0)
    elif s in SFX:
        soma(fx, SFX[s](), bt["t"], .8)
    soma(fx, SFX["pop"](), bt["t"] + .02, .25)  # pop do texto de cada beat
# queda dos paus e encaixe do segundo pau
for tt in (18.8, 19.6, 34.6): soma(fx, J(tom(140, .25, .001, .08), passa_baixa(ruido(.15, .05), .3) * .5), tt, .7)
# dobras do pano
for tt in (28.0, 39.0): soma(fx, whoosh(.9), tt, .6)

mix = mus * .32 + fx * .55
mix /= max(1e-9, np.max(np.abs(mix))) / .89
est = np.stack([mix, mix], axis=1)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else "trilha.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((est * 32767).astype("<i2").tobytes())
print("ok", DUR, "s")

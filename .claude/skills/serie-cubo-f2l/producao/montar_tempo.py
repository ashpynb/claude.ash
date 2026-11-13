"""Junta as falas por beat num áudio só e escreve o tempo de cada beat/palavra.

Uso: python montar_tempo.py ep01 dir_voz
Respiro depois de cada beat: 0,22s; depois de beat com algoritmo: 0,5s (regra da série F2L).
"""
import json, sys, numpy as np, soundfile as sf, pathlib
ep, voz = sys.argv[1], pathlib.Path(sys.argv[2])
AQUI = pathlib.Path(__file__).parent
roteiro = json.load(open(AQUI.parent / "roteiro" / f"{ep}.json"))
beats = [b for c in roteiro["clipes"] for b in c["beats"]]
tempos = json.load(open(voz / "tempos.json"))
falas = {f["id"]: f for f in json.load(open(AQUI / f"{ep}_falas.json"))}
SR = 24000
partes, out, t = [], [], 0.0
for i, b in enumerate(beats):
    k = "b%02d" % i
    a, _ = sf.read(voz / f"{k}.wav")
    resp = falas[k].get("resp", 0.5 if "CUBO" in b["visual"] or i == 0 else 0.22)
    dur = len(a) / SR + resp
    out.append({"t0": round(t, 3), "t1": round(t + dur, 3), "fala": b["fala"],
                "words": [{"w": w["w"], "t0": round(t + w["t0"], 3), "t1": round(t + w["t1"], 3)} for w in tempos[k]["palavras"]]})
    partes += [a, np.zeros(int(resp * SR))]
    t += dur
total = round(t + 0.6, 3)
partes.append(np.zeros(int(0.6 * SR)))
sf.write(voz / "narracao.wav", np.concatenate(partes), SR)
(AQUI / f"{ep}_tempo.js").write_text("window.TEMPO=" + json.dumps({"total": total, "beats": out}, ensure_ascii=False) + ";\n")
n = sum(len(b["fala"].split()) for b in beats)
print(f"{ep}: {total:.1f}s  {n} palavras  {n/total:.2f} p/s")

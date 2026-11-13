"""Gera a narração por beat com Edge TTS (Antônio) e o tempo de cada palavra.

Uso: python narrar.py entrada.json saida_dir RATE GAP_MAX
entrada.json: [{"id":..., "texto":..., "rate"?:"+0%", "gap"?:0.2, "resp"?:0.2}, ...]
(rate/gap por beat sobrescrevem os da linha de comando; resp é usado por montar_tempo.py)
Saída: saida_dir/<id>.wav e saida_dir/tempos.json com
  {id: {"dur": s, "palavras": [{"w":..., "t0":..., "t1":...}]}}
As pausas entre palavras maiores que GAP_MAX são encurtadas para GAP_MAX
(o Antônio faz ~0,85s entre frases; isso arrastava a fala).
"""
import asyncio, io, json, os, subprocess, sys
import numpy as np, soundfile as sf, edge_tts

VOZ = "pt-BR-AntonioNeural"
SR = 24000

async def tts(texto, rate):
    c = edge_tts.Communicate(texto, VOZ, rate=rate, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    mp3, pal = b"", []
    async for ch in c.stream():
        if ch["type"] == "audio":
            mp3 += ch["data"]
        elif ch["type"] == "WordBoundary":
            t0 = ch["offset"] / 1e7
            pal.append({"w": ch["text"], "t0": t0, "t1": t0 + ch["duration"] / 1e7})
    wav = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "pipe:0", "-ac", "1", "-ar", str(SR),
                          "-f", "wav", "pipe:1"], input=mp3, capture_output=True, check=True).stdout
    a, _ = sf.read(io.BytesIO(wav))
    return a, pal

def comprimir(a, pal, gap_max, borda=0.04):
    """Corta silêncio: início/fim aparados e pausas entre palavras limitadas a gap_max."""
    segs, novas, t_out = [], [], 0.0
    ini = max(0.0, pal[0]["t0"] - borda)
    for i, p in enumerate(pal):
        fim = p["t1"] if i == len(pal) - 1 else p["t1"]
        if i == len(pal) - 1:
            fim = min(len(a) / SR, p["t1"] + 0.12)
        seg = a[int(ini * SR):int(fim * SR)]
        desloc = t_out - ini
        novas.append({"w": p["w"], "t0": round(p["t0"] + desloc, 3), "t1": round(p["t1"] + desloc, 3)})
        segs.append(seg); t_out += len(seg) / SR
        if i + 1 < len(pal):
            gap = pal[i + 1]["t0"] - p["t1"]
            g = min(gap, gap_max)
            # mantém o som real do começo da pausa (respiração/cauda) e corta o resto
            segs.append(a[int(p["t1"] * SR):int((p["t1"] + g) * SR)]); t_out += g
            ini = pal[i + 1]["t0"]
    return np.concatenate(segs), novas

async def main():
    entrada, saida, rate, gap_max = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    os.makedirs(saida, exist_ok=True)
    out, tw, tt = {}, 0, 0.0
    for b in json.load(open(entrada)):
        a, pal = await tts(b["texto"], b.get("rate", rate))
        a2, pal2 = comprimir(a, pal, b.get("gap", gap_max))
        sf.write(os.path.join(saida, b["id"] + ".wav"), a2, SR)
        d = len(a2) / SR
        out[b["id"]] = {"dur": round(d, 3), "palavras": pal2}
        tw += len(b["texto"].split()); tt += d
        print(f'{b["id"]}  {len(b["texto"].split()):2d} pal  {d:5.2f}s  {len(b["texto"].split())/d:4.2f} p/s')
    json.dump(out, open(os.path.join(saida, "tempos.json"), "w"), ensure_ascii=False, indent=1)
    print(f"TOTAL {tw} pal {tt:.1f}s {tw/tt:.2f} p/s (só fala, sem respiros entre beats)")

asyncio.run(main())

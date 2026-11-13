#!/usr/bin/env python3
"""qa.py - checagem automática do MP4 final (todo quadro), antes de enviar à usuária.

  python3 qa.py trabalho/SLUG/SLUG.mp4 [--tempo trabalho/SLUG/tempo.js] [--saida trabalho/SLUG/qa] [--folhas]

Confere: formato (1080x1920, 30 fps), duração 1:00–1:30, áudio, loudness (alvo -14 LUFS, pico <= -1 dBTP),
silêncio morto no meio da fala, quadro preto, quadro branco não planejado, imagem congelada, "pulo" de quadro
fora dos cortes planejados e, com --tempo, se legenda/tempo.js batem com o vídeo (ordem, sobreposição, ritmo).
Gera qa/relatorio.md e qa/visao_geral.jpg (1 quadro por segundo, com o segundo escrito, só pra revisão).
--folhas também gera folhas de 2 s (60 quadros cada), como no original.

Adaptado de templates/scripts/short_qa.py de mromidev/claude-animated-shorts (MIT, commit e3b817b):
mesma ideia de detecção (preto/branco/congelado/pulos, loudness, folhas), reescrito pra ler o vídeo em
fluxo (memória constante) e pras regras da fábrica. Assertivas de alinhamento inspiradas em
liyupi/niulai-video-generator (MIT). Saída: código 0 = passou, 1 = erro duro, 2 = não deu pra ler.
"""
import argparse, json, os, re, subprocess, sys

import numpy as np
from PIL import Image, ImageDraw

W, H = 90, 160          # quadro reduzido pra análise
FPS_ALVO = 30
LUFS_ALVO, LUFS_TOL = -14.0, 2.0


def rodar(*a):
    return subprocess.run(a, capture_output=True, text=True)


def ler_tempo(caminho):
    txt = open(caminho, encoding="utf-8").read().strip()
    txt = re.sub(r"^\s*window\.TEMPO\s*=\s*", "", txt)
    txt = re.sub(r";\s*$", "", txt)
    return json.loads(txt)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--tempo")
    ap.add_argument("--saida")
    ap.add_argument("--folhas", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(a.video):
        print(f"não achei {a.video}"); sys.exit(2)
    out = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.video)), "qa")
    os.makedirs(out, exist_ok=True)
    duros, avisos, R = [], [], []

    # ---------------- formato
    pr = rodar("ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration", "-of", "json", a.video)
    try:
        pr = json.loads(pr.stdout)
        v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    except Exception:
        print("ffprobe não conseguiu ler o vídeo"); sys.exit(2)
    au = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    dur = float(pr["format"]["duration"])
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    fps = num / den if den else 0
    R.append(f"FORMATO {v['width']}x{v['height']} · {fps:.2f} fps · {dur:.2f} s · áudio: "
             + (", ".join(f"{s['codec_name']} {s.get('sample_rate')} Hz {s.get('channels')}ch" for s in au) or "NENHUM"))
    if (int(v["width"]), int(v["height"])) != (1080, 1920):
        duros.append(f"resolução {v['width']}x{v['height']} (tem que ser 1080x1920)")
    if abs(fps - FPS_ALVO) > 0.01:
        avisos.append(f"{fps:.2f} fps (padrão da fábrica: 30)")
    if dur < 60.0:
        duros.append(f"duração {dur:.1f}s: abaixo do mínimo exato de 1:00")
    elif dur > 90.5:
        duros.append(f"duração {dur:.1f}s: acima de 1:30")
    if not au:
        duros.append("vídeo sem áudio")

    # ---------------- áudio
    if au:
        e = rodar("ffmpeg", "-nostats", "-i", a.video, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-").stderr
        resumo = e[e.rfind("Summary:"):]
        m_i = re.search(r"I:\s*(-?[\d.]+) LUFS", resumo)
        m_p = re.search(r"Peak:\s*(-?[\d.]+|-inf) dBFS", resumo)
        lufs = float(m_i.group(1)) if m_i else None
        pico = float(m_p.group(1)) if m_p and m_p.group(1) != "-inf" else None
        R.append(f"LOUDNESS integrado {lufs} LUFS · pico {pico} dBTP (alvo {LUFS_ALVO:g} ±{LUFS_TOL:g} LUFS, pico <= -1)")
        if lufs is None:
            avisos.append("não consegui medir a loudness")
        elif lufs < LUFS_ALVO - 6 or lufs > LUFS_ALVO + 4:
            duros.append(f"volume {lufs} LUFS: muito longe de -14 (vai soar baixo/estourado perto dos outros vídeos)")
        elif abs(lufs - LUFS_ALVO) > LUFS_TOL:
            avisos.append(f"volume {lufs} LUFS (alvo -14 ±2)")
        if pico is not None and pico > -0.5:
            avisos.append(f"pico {pico} dBTP: risco de distorção depois da compressão da plataforma")
        e = rodar("ffmpeg", "-nostats", "-i", a.video, "-map", "0:a:0", "-af", "silencedetect=n=-40dB:d=0.5", "-f", "null", "-").stderr
        sil = []
        ini = None
        for l in e.splitlines():
            m = re.search(r"silence_start: (-?[\d.]+)", l)
            if m: ini = float(m.group(1))
            m = re.search(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", l)
            if m and ini is not None:
                sil.append((ini, float(m.group(1)), float(m.group(2)))); ini = None
        if ini is not None:
            sil.append((ini, dur, dur - ini))
        meio = [s for s in sil if s[0] > 0.3 and s[1] < dur - 1.0]   # ignora começo e cauda planejada
        R.append("SILÊNCIOS no meio (>0,5 s): " + ("; ".join(f"{s[0]:.1f}–{s[1]:.1f}s" for s in meio) or "nenhum"))
        for s in meio:
            (duros if s[2] > 1.2 else avisos).append(f"silêncio morto de {s[2]:.1f}s em {s[0]:.1f}s (a pessoa rola a tela)")

    # ---------------- tempo.js (legenda e beats)
    planejados = set()
    if a.tempo:
        try:
            T = ler_tempo(a.tempo)
            beats = T["beats"]
            ok_ordem, n_pal, fala_s = True, 0, 0.0
            ant = -1.0
            for i, b in enumerate(beats):
                planejados.update(range(int(b["t0"] * FPS_ALVO) - 1, int(b["t0"] * FPS_ALVO) + 3))
                if b["t0"] < ant - 1e-6 or b["t1"] <= b["t0"]:
                    ok_ordem = False
                ant = b["t1"]
                ws = b.get("words", [])
                n_pal += len(ws)
                if ws:
                    fala_s += ws[-1]["t1"] - ws[0]["t0"]
                for w0, w1 in zip(ws, ws[1:]):
                    if w1["t0"] + 1e-6 < w0["t0"]:
                        ok_ordem = False
                for w in ws:
                    if w["t0"] < b["t0"] - 0.05 or w["t1"] > b["t1"] + 0.05:
                        ok_ordem = False
            if not ok_ordem:
                duros.append("tempo.js fora de ordem ou com sobreposição (legenda vai dessincronizar)")
            dif = abs(T["total"] - dur)
            R.append(f"TEMPO.JS {len(beats)} beats · {n_pal} palavras · total {T['total']:.2f}s vs vídeo {dur:.2f}s (dif {dif:.2f}s)"
                     + (f" · ritmo {n_pal / T['total']:.2f} p/s no vídeo" if T["total"] else ""))
            if dif > 0.25:
                duros.append(f"tempo.js ({T['total']:.2f}s) e vídeo ({dur:.2f}s) não batem: render incompleto ou tempo velho")
            ritmo = n_pal / T["total"] if T["total"] else 0
            if ritmo and abs(ritmo - 3.2) > 0.2:
                avisos.append(f"ritmo {ritmo:.2f} p/s (regra: 3,2)")
        except Exception as ex:
            duros.append(f"não consegui ler {a.tempo}: {ex}")

    # ---------------- quadros (fluxo, memória constante)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H}:flags=area",
                             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    tam = W * H * 3
    medias, difs, sats = [], [], []
    ant = None
    miniaturas = {}       # 1 por segundo pra visão geral
    folha_buf, nfolha = [], 0
    i = 0
    while True:
        buf = proc.stdout.read(tam)
        if len(buf) < tam:
            break
        q = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        f = q.astype(np.float32) / 255
        lum = f @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        medias.append(float(lum.mean()))
        mx, mn = f.max(-1), f.min(-1)
        sats.append(float(np.where(mx > 0.06, (mx - mn) / np.maximum(mx, 1e-6), 0).mean()))
        if ant is not None:
            difs.append(float(np.abs(q.astype(np.int16) - ant).mean()))
        ant = q.astype(np.int16)
        if i % FPS_ALVO == 15:
            miniaturas[i // FPS_ALVO] = Image.fromarray(q)
        if a.folhas:
            folha_buf.append(q.copy())
            if len(folha_buf) == 60:
                salvar_folha(folha_buf, nfolha * 60, out); folha_buf, nfolha = [], nfolha + 1
        i += 1
    proc.wait()
    if a.folhas and folha_buf:
        salvar_folha(folha_buf, nfolha * 60, out)
    n = len(medias)
    if n == 0:
        print("não consegui decodificar quadros"); sys.exit(2)
    difs = np.array(difs) if difs else np.zeros(1)
    med = np.array([np.median(difs[max(0, k - 8):k + 9]) for k in range(len(difs))])
    pulos = [k + 1 for k in range(len(difs)) if difs[k] > 3 * med[k] + 6.0 and (k + 1) not in planejados]
    pretos = [k for k in range(n) if medias[k] < 0.04 and 1 < k < n - 2]
    brancos = [k for k in range(n) if medias[k] > 0.93]
    congelados, ini = [], None
    for k in range(len(difs)):
        if difs[k] < 0.05:
            ini = k if ini is None else ini
        else:
            if ini is not None and k - ini >= 15: congelados.append((ini, k))
            ini = None
    if ini is not None and len(difs) - ini >= 15:
        congelados.append((ini, len(difs)))
    R.append(f"QUADROS {n} · pretos {fmt(pretos)} · brancos {fmt(brancos)} · congelados >=0,5s "
             + (", ".join(f"{x / 30:.1f}–{y / 30:.1f}s" for x, y in congelados[:12]) or "nenhum"))
    R.append(f"PULOS fora dos cortes planejados: {fmt(pulos)}")
    R.append(f"MOVIMENTO diferença média {difs.mean():.2f} · quadros quase parados {(difs < 0.3).mean() * 100:.0f}% · "
             f"luz média {np.median(medias):.2f} · saturação média {np.median(sats):.2f}")
    if pretos:
        duros.append(f"{len(pretos)} quadro(s) preto(s) no meio (ex.: {pretos[0] / 30:.1f}s): cena não carregou")
    if len(brancos) > 3:
        avisos.append(f"{len(brancos)} quadros quase brancos (flash longo demais?) ex.: {brancos[0] / 30:.1f}s")
    for x, y in congelados:
        (duros if y - x >= 45 else avisos).append(
            f"imagem parada {(y - x) / 30:.1f}s em {x / 30:.1f}s (regra: algo sempre se movendo; push-in lento resolve)")
    if len(pulos) > 3:
        avisos.append(f"{len(pulos)} pulos de quadro fora dos cortes (ex.: {pulos[0] / 30:.1f}s): olhe esses pontos na folha")

    # ---------------- visão geral (1 quadro por segundo)
    if miniaturas:
        cols, cw, ch = 10, 108, 192
        segs = sorted(miniaturas)
        S = Image.new("RGB", (cw * cols, ch * ((len(segs) + cols - 1) // cols)), "black")
        d = ImageDraw.Draw(S)
        for j, s in enumerate(segs):
            x, y = (j % cols) * cw, (j // cols) * ch
            S.paste(miniaturas[s].resize((cw, ch)), (x, y))
            d.rectangle([x, y, x + 30, y + 12], fill="black"); d.text((x + 2, y + 1), f"{s}s", fill="yellow")
        S.save(os.path.join(out, "visao_geral.jpg"), quality=85)

    R.append("")
    R += [f"✗ DURO  {x}" for x in duros] + [f"⚠ aviso {x}" for x in avisos]
    R.append("RESULTADO: " + ("PASSOU no QA automático" if not duros else f"REPROVADO ({len(duros)} erro(s) duro(s))"))
    R.append(f"Olhe {os.path.join(out, 'visao_geral.jpg')} antes de enviar.")
    open(os.path.join(out, "relatorio.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")
    print("\n".join(R))
    sys.exit(0 if not duros else 1)


def fmt(lst):
    return "nenhum" if not lst else f"{len(lst)} (ex.: " + ", ".join(f"{k / 30:.1f}s" for k in lst[:6]) + ")"


def salvar_folha(quadros, inicio, out):
    cw, ch = 108, 192
    S = Image.new("RGB", (cw * 10, ch * 6), "black"); d = ImageDraw.Draw(S)
    for j, q in enumerate(quadros):
        x, y = (j % 10) * cw, (j // 10) * ch
        S.paste(Image.fromarray(q).resize((cw, ch)), (x, y))
        d.rectangle([x, y, x + 34, y + 12], fill="black"); d.text((x + 2, y + 1), str(inicio + j), fill="yellow")
    S.save(os.path.join(out, f"folha_{inicio:05d}.jpg"), quality=85)


if __name__ == "__main__":
    main()

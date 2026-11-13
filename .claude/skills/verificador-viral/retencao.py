#!/usr/bin/env python3
"""retencao.py - depois de postar: lê a curva de retenção do Reels/TikTok/Shorts e diz ONDE a pessoa saiu
e O QUE estava sendo falado naquele segundo (com o tempo.js do vídeo).

  python3 retencao.py curva.csv --tempo trabalho/SLUG/tempo.js
  python3 retencao.py curva.csv --duracao 72 --json
  python3 retencao.py curva.csv --pct --duracao 72      # 1ª coluna em % do vídeo (YouTube Studio)

curva.csv: duas colunas, segundo (ou % do vídeo) e % de pessoas ainda assistindo. Instagram e TikTok
mostram a curva no app; anote uns 10–20 pontos à mão (ex.: 0,100 / 1,82 / 3,61 / 10,48 / ...) ou
exporte do YouTube Studio. Uma linha por ponto, vírgula, ponto-e-vírgula ou tab.

Relata três problemas diferentes, com consertos diferentes:
  GANCHO   quanto saiu nos 3 primeiros segundos   -> reescrever a 1ª frase e o 1º quadro
  QUEDAS   saídas bruscas num momento             -> o que estava sendo dito/mostrado ali
  LADEIRA  perda constante no meio                -> ritmo: cortar, não reescrever

Adaptado de skills/yt-retention/retention.py de Jakeschincariol/youtube-agent-skill (MIT, commit a2feb21):
mesma divisão gancho/quedas/ladeira; trocado para vídeo curto (gancho = 3 s, não 30 s), leitura do
tempo.js da fábrica e saída em português.
"""
import csv, json, os, re, sys


def ler_csv(caminho):
    pts = []
    with open(caminho, newline="", encoding="utf-8-sig", errors="replace") as fh:
        amostra = fh.read(2048); fh.seek(0)
        sep = ";" if amostra.count(";") > amostra.count(",") else ("\t" if "\t" in amostra else ",")
        for r in csv.reader(fh, delimiter=sep):
            nums = []
            for c in r:
                c = c.strip().replace("%", "").replace("s", "")
                if sep == ";":
                    c = c.replace(",", ".")
                try:
                    nums.append(float(c))
                except ValueError:
                    pass
            if len(nums) >= 2:
                pts.append((nums[0], nums[1]))
    pts.sort()
    return pts


def ler_tempo(caminho):
    t = open(caminho, encoding="utf-8").read().strip()
    t = re.sub(r"^\s*window\.TEMPO\s*=\s*", "", t); t = re.sub(r";\s*$", "", t)
    return json.loads(t)


def fala_em(T, seg):
    for i, b in enumerate(T["beats"]):
        if b["t0"] <= seg < b["t1"] + 0.12:
            return i + 1, b["fala"]
    return None, ""


def main():
    a = sys.argv[1:]
    js = "--json" in a; pct = "--pct" in a
    a = [x for x in a if x not in ("--json", "--pct")]
    tempo = a[a.index("--tempo") + 1] if "--tempo" in a else None
    dur = float(a[a.index("--duracao") + 1]) if "--duracao" in a else None
    arqs = [x for x in a if not x.startswith("--") and x not in (tempo, str(dur) if dur else None)]
    arqs = [x for x in arqs if x != (a[a.index("--duracao") + 1] if "--duracao" in a else None)]
    if not arqs or not os.path.exists(arqs[0]):
        print(__doc__); sys.exit(1)
    pts = ler_csv(arqs[0])
    if len(pts) < 5:
        print("preciso de pelo menos 5 pontos (segundo, %) no csv"); sys.exit(1)
    T = ler_tempo(tempo) if tempo and os.path.exists(tempo) else None
    if T and not dur:
        dur = T["total"]
    if pct and not dur:
        print("com --pct preciso de --duracao (ou --tempo)"); sys.exit(1)
    eixo_pct = pct
    seg = (lambda x: x / 100.0 * dur) if eixo_pct else (lambda x: x)
    P = [(seg(x), y) for x, y in pts]
    ini = P[0][1] or 100.0

    def em(t):  # % assistindo no segundo t (interpolação linear)
        for (x0, y0), (x1, y1) in zip(P, P[1:]):
            if x0 <= t <= x1:
                return y0 + (y1 - y0) * ((t - x0) / (x1 - x0) if x1 > x0 else 0)
        return P[-1][1] if t > P[-1][0] else P[0][1]

    g3 = ini - em(3.0)
    metade = em((dur or P[-1][0]) / 2)
    fim = P[-1][1]
    quedas = []
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        if x0 < 3.0:
            continue
        perda = y0 - y1
        if perda > 0 and perda / max(x1 - x0, 0.5) >= 2.0:   # >= 2 pontos por segundo
            b, f = fala_em(T, x0) if T else (None, "")
            quedas.append({"de": round(x0, 1), "ate": round(x1, 1), "perdeu": round(perda, 1), "beat": b, "fala": f})
    quedas.sort(key=lambda q: -q["perdeu"])
    meio = [(y0 - y1) / max(x1 - x0, 0.5) for (x0, y0), (x1, y1) in zip(P, P[1:]) if x0 >= 3.0]
    ladeira = sum(meio) / len(meio) if meio else 0
    res = {"pontos": len(P), "gancho_perda_3s": round(g3, 1), "na_metade": round(metade, 1), "no_fim": round(fim, 1),
           "quedas": quedas[:5], "ladeira_por_s": round(ladeira, 2)}
    if js:
        print(json.dumps(res, ensure_ascii=False, indent=1)); return
    veredito = "bom" if g3 < 30 else "vazando" if g3 < 45 else "grave"
    print(f"\nRETENÇÃO {arqs[0]} · {len(P)} pontos · {ini:.0f}% → {fim:.0f}% no fim · {metade:.0f}% na metade\n")
    print(f"GANCHO  saíram {g3:.0f}% nos 3 primeiros segundos [{veredito}]")
    print("        abaixo de 30% é bom pra vídeo curto. Se vazou, conserte a 1ª frase e o 1º quadro antes de tudo.\n")
    print("QUEDAS  os momentos em que as pessoas saíram")
    for q in quedas[:5]:
        print(f"   -{q['perdeu']:4.1f} pts  {q['de']:.0f}–{q['ate']:.0f}s" + (f"  beat {q['beat']}: \"{q['fala']}\"" if q["fala"] else ""))
    if not quedas:
        print("   nenhuma queda brusca: a perda é só ladeira (ritmo), não um momento ruim")
    print(f"\nLADEIRA {ladeira:.2f} pts por segundo no meio")
    print("        ladeira alta e sem quedas = ritmo lento. Corte frases, não reescreva o vídeo.\n")
    print("Leve a lição mais clara (uma só) pro fabrica-viral/regras.md, na seção 'Medido nos NOSSOS vídeos'.")


if __name__ == "__main__":
    main()

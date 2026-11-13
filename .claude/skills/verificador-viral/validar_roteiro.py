#!/usr/bin/env python3
"""validar_roteiro.py - checagem OBJETIVA de um roteiro da fábrica viral (falas.txt, uma fala por linha).

  python3 validar_roteiro.py trabalho/SLUG/falas.txt --molde voce
  python3 validar_roteiro.py falas.txt --molde construiu --json

Moldes: voce | construiu | ese | passo | flat2d | livre (padrão).

Erro DURO = o roteiro volta pra reescrita, sem exceção. AVISO = pode passar, mas pesa na nota.
Ideia dos "hard/soft asserts" de liyupi/niulai-video-generator (MIT), reescrita do zero para as
regras da usuária (fabrica-viral/regras.md). Só lê o arquivo; não usa rede.
Saída: código 0 se não houver erro duro, 1 se houver, 2 se o arquivo não puder ser lido.
"""
import argparse, json, re, sys, unicodedata

RITMO = 3.2        # palavras por segundo (regra da usuária)
RESPIRO = 0.12     # segundos entre beats (video.py narrar)
CAUDA = 0.6        # silêncio no fim (video.py narrar)
DUR_MIN, DUR_MAX = 60.0, 90.0

PALAVRA = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][0-9A-Za-zÀ-ÖØ-öø-ÿ]+)*")
ABERTURA_LENTA = re.compile(r"^(ol[áa]|oi|e a[íi]|fala,? galera|hoje (eu )?vou|hoje vamos|neste v[íi]deo|nesse v[íi]deo|"
                            r"bem[- ]vindos?|no v[íi]deo de hoje)\b", re.I)
CTA_FALADO = re.compile(r"\b(comenta|comente|se inscrev|segue (a|o) |me segue|siga |curte|curta |compartilha|"
                        r"marca (aquele|um|uma|o seu|a sua|quem)|link na bio|ativa o sininho)\b", re.I)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def palavras(s):
    # "pepino-do-mar" é lido como 3 palavras pela voz: conta as partes do hífen
    return [p for w in PALAVRA.findall(s) for p in w.split("-") if p]


def checar(falas, molde):
    duros, avisos, info = [], [], {}
    if not falas:
        return ["falas.txt vazio"], [], {}
    n_pal = [len(palavras(f)) for f in falas]
    total = sum(n_pal)
    dur = total / RITMO + RESPIRO * len(falas) + CAUDA
    info.update(beats=len(falas), palavras=total, duracao_estimada_s=round(dur, 1),
                palavras_por_beat=round(total / len(falas), 1))

    # --- duração (regra: mínimo exato 1:00, máximo 1:30)
    if dur < DUR_MIN:
        faltam = int((DUR_MIN - dur) * RITMO) + 1
        duros.append(f"curto demais: ~{dur:.0f}s (mínimo 60s). Acrescente ~{faltam} palavras de fato conferido ou piada, nunca fale mais devagar")
    elif dur > DUR_MAX:
        duros.append(f"longo demais: ~{dur:.0f}s (máximo 90s). Corte ~{int((dur - DUR_MAX) * RITMO) + 1} palavras")
    elif dur < 64:
        avisos.append(f"~{dur:.0f}s: perto do mínimo. Se a voz sair um pouco rápida, fica abaixo de 1:00")

    for i, f in enumerate(falas, 1):
        if re.search(r"\d", f):
            duros.append(f"linha {i}: tem algarismo ({f[:40]}…). Na fala, número vai por extenso; algarismo só na tela")
        if re.search(r"\(|\)|\.\.\.|…|—|–", f):
            duros.append(f"linha {i}: parênteses, reticências ou travessão travam a voz. Reescreva em frase curta")
        if n_pal[i - 1] > 20:
            duros.append(f"linha {i}: {n_pal[i - 1]} palavras (máx. 20 por beat). Quebre em duas linhas")
        elif n_pal[i - 1] > 16:
            avisos.append(f"linha {i}: {n_pal[i - 1]} palavras (roteiro.md pede até ~16 por linha)")
        if CTA_FALADO.search(f):
            duros.append(f"linha {i}: pedido de engajamento na fala ('{CTA_FALADO.search(f).group(0)}'). Vai só na legenda do post")

    gancho = re.split(r"(?<=[.?!])\s+", falas[0].strip())[0]   # 1ª frase da 1ª linha
    info["gancho"] = gancho
    if ABERTURA_LENTA.search(gancho.strip()):
        duros.append("gancho começa com saudação/introdução. A 1ª palavra já tem que ser o gancho")
    if len(palavras(gancho)) > 14:
        duros.append(f"gancho com {len(palavras(gancho))} palavras: não cabe em 3s a 3,2 p/s (máx. ~12–14)")
    elif len(palavras(gancho)) > 11:
        avisos.append("gancho com mais de 11 palavras: tente caber em ~3s (a 3,2 p/s, 3s = ~10 palavras)")

    # --- variedade: começo de frase repetido em sequência (sensação de lista)
    inicios = [sem_acento(" ".join(palavras(f)[:2])) for f in falas]
    for i in range(2, len(inicios)):
        if inicios[i] and inicios[i] == inicios[i - 1] == inicios[i - 2] and not inicios[i].startswith("esse e"):
            avisos.append(f"linhas {i - 1}–{i + 1} começam igual ('{inicios[i]}'): varie a construção")

    perguntas = sum("?" in f for f in falas)
    info["perguntas"] = perguntas
    if perguntas == 0:
        avisos.append("nenhuma pergunta retórica: uma 'Pera…?' ou 'Sabe por quê?' no meio segura a retenção")

    # --- molde
    norm = [sem_acento(f) for f in falas]
    if molde == "voce":
        refrao = sum(bool(re.search(r"\besse e (o )?seu\b|\bessa e (a )?sua\b|\besses sao (os )?seus\b", f)) for f in norm)
        info["refroes"] = refrao
        if refrao < 4:
            duros.append(f"molde 'Você é…': só {refrao} refrões 'Esse é seu…' (mínimo 4)")
        if not re.search(r"\bvoce\b", norm[0]):
            duros.append("molde 'Você é…': o gancho tem que estar em 2ª pessoa ('Você…')")
        if norm[-1].strip(" .!?") != norm[0].strip(" .!?"):
            duros.append("molde 'Você é…': a última fala tem que repetir a 1ª (loop)")
        if not any(re.search(r"\bchamam de\b", f) for f in norm[-4:]):
            avisos.append("molde 'Você é…': falta o fecho 'Chamam de [nome] quem…' antes do loop")
    elif molde == "construiu":
        if not norm[-1].startswith("parabens"):
            duros.append("molde 'Você construiu': a última fala tem que ser 'Parabéns. Você construiu um…'")
        if sum(f.startswith("mas ") for f in norm) < 3:
            avisos.append("molde 'Você construiu': poucos 'Mas…' (problema → peça). Mínimo 3")
    elif molde == "ese":
        if not re.search(r"^e se (tu|voce)\b", norm[0]):
            duros.append("molde 'E se tu…': o gancho tem que começar com 'E se tu…'")
        if not re.search(r"parte dois", " ".join(norm[-2:])):
            duros.append("molde 'E se tu…': fecha com 'Na parte dois…?' (cliffhanger)")
    elif molde == "flat2d":
        if not falas[-1].strip().endswith("?"):
            avisos.append("molde 2D flat: fecha com pergunta pro público ('E você, já…?')")
    elif molde == "passo":
        if not any(re.search(r"\bpasso (um|1)\b", f) for f in norm):
            duros.append("molde Passo a passo: falta 'Passo um…'")

    return duros, avisos, info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("falas")
    ap.add_argument("--molde", default="livre", choices=["voce", "construiu", "ese", "passo", "flat2d", "livre"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        linhas = open(a.falas, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"não consegui ler {a.falas}: {e}"); sys.exit(2)
    falas = [l.strip() for l in linhas if l.strip() and not l.startswith("Uma frase por linha")]
    duros, avisos, info = checar(falas, a.molde)
    if a.json:
        print(json.dumps({"ok": not duros, "duros": duros, "avisos": avisos, "info": info}, ensure_ascii=False, indent=1))
    else:
        print(f"ROTEIRO {a.falas}  ({a.molde})")
        print(f"  {info.get('beats', 0)} beats · {info.get('palavras', 0)} palavras · ~{info.get('duracao_estimada_s', 0)} s "
              f"a {RITMO} p/s · {info.get('palavras_por_beat', 0)} palavras/beat · {info.get('perguntas', 0)} perguntas")
        for d in duros: print("  ✗ DURO  " + d)
        for w in avisos: print("  ⚠ aviso " + w)
        print("  RESULTADO: " + ("PASSA nas regras objetivas" if not duros else f"VOLTA PRA REESCRITA ({len(duros)} erro(s) duro(s))"))
    sys.exit(0 if not duros else 1)


if __name__ == "__main__":
    main()

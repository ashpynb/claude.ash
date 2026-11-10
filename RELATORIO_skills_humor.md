# Relatório pra outra sessão: achar e instalar skills de ROTEIRO ENGRAÇADO

## Contexto (ler antes)
- Repo `ashpynb/claude.ash`, branch `claude/videos-economia-reverse-eng-e5yftd`.
- Leia `referencias/aprendizados.md` (regras da usuária) e as fichas `referencias/01–05_*.md`.
- O formato atual é **"Você é…"** (ficha 05): 2ª pessoa, cada fato vira "Esse é seu [objeto do dia a dia]",
  fecho que ressignifica o nome e volta à 1ª frase. Vídeos de ~1 min, 3D cartoon, narração Edge TTS
  (pt-BR-AntonioNeural) a 3,2 palavras/s, **sem música**, legenda de 1–3 palavras.
- Já instaladas em `.claude/skills/`: `viral-hooks`, `ig-*` (ig-reel, ig-human, ig-caption...), `watch`,
  `assistir-youtube`. Não duplicar.

## O que procurar
Skills (Claude Code / Agent Skills, `SKILL.md`) ou guias que ensinem a escrever **humor curto pra vídeo**,
de preferência com regras concretas:
1. Estrutura de piada: setup → punchline, regra de três com quebra, callback, exagero, comparação absurda,
   personificação ("você é um bicho com problemas de adulto").
2. Humor pra fatos de ciência sem distorcer o fato (o fato continua verdadeiro; a piada é na comparação).
3. Timing pra narração: onde pausar, frase curta antes do punchline, punchline na última palavra.
4. Como testar se a piada funciona (checklist ou nota), e humor que não ofende (sem piada com grupo de pessoas).
5. Humor em **português do Brasil** (gírias leves, memes que envelhecem bem).

Pontos de partida achados (poucas estrelas, avaliar antes):
- `vkorost/claude-standup-skills` (estruturas de 7 comediantes de stand-up)
- `SpencerRaw/hermes-comedy-writing` (Atitude → Insight → Explicação → Desfamiliarização → Cena)
- `l8ntlabs/agent-skills` (tem "comedy writing")
- Buscar também: "comedy writing skill", "humor copywriting skill", "funny script prompt", "sketch writing",
  "punchline", e canais de humor + ciência (ex.: análise de roteiros de canais virais de "você é um animal").

## Regras pra instalar
- Só licença aberta (MIT, Apache, CC-BY). Ler o código inteiro antes; sem scripts que mandem dados pra fora.
- Instalar em `.claude/skills/<nome>/` com um `ORIGEM.md` (repo, commit, licença).
- Se a skill for genérica, **adaptar**: escrever `.claude/skills/roteiro-humor/SKILL.md` próprio, juntando
  as regras úteis + o molde "Você é…" + as regras do `aprendizados.md`.
- Testar: reescrever o roteiro mais recente (`roteiro/viral02_*.md`, se existir) com a skill e comparar.
- Commit + push na branch acima. Mostrar à usuária o que foi instalado e por quê.

## Mensagem pronta pra colar na outra sessão
> Puxa a branch `claude/videos-economia-reverse-eng-e5yftd` do `ashpynb/claude.ash` e lê o
> `RELATORIO_skills_humor.md`. Quero que você pesquise e instale skills de como escrever roteiros engraçados
> pros meus vídeos curtos, seguindo o relatório. Antes de instalar qualquer coisa, me mostra a lista do que
> achou e por quê.

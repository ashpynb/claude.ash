---
name: roteiro-humor
description: Escreve roteiros curtos (Reels/TikTok/Shorts, ~1 min) engraçados, sensacionalistas e besteirol, mas que ensinam um fato verdadeiro, em português do Brasil. Molde padrão "Você é…" (2ª pessoa + refrão "Esse é seu [objeto]"). Use quando a usuária pedir vídeo engraçado, besteirol, curiosidade absurda, "você é um [bicho/coisa]", ou um roteiro viral de humor sobre ciência, história, corpo humano, objetos ou animais.
---

# Roteiro de humor (besteirol que ensina)

Junta três fontes:
- `comedy-writer` (técnicas: detalhe concreto, punchline na última palavra, regra de três, callback, status);
- `clean-comedy-rewrite` (só como filtro de ofensa, ver regra 6);
- as regras em `.claude/skills/fabrica-viral/regras.md` e o molde "Você é…" em `fabrica-viral/moldes.md`, que **têm prioridade**.

## Antes de escrever
1. Leia `.claude/skills/fabrica-viral/regras.md` e `fabrica-viral/fichas/05_voce_e.md`.
2. Escolha o tema. Não precisa ser bicho: pode ser objeto, órgão, planeta, comida, invenção, fenômeno.
   O tema precisa de **3 a 6 fatos verdadeiros e visuais**, e pelo menos um tem que soar absurdo.
3. **Confira cada fato** (estudo, museu, universidade, enciclopédia). O que não conseguir confirmar
   vai para "⚠️ Conferir" ou sai do roteiro. **A piada está na comparação, nunca no fato.**
4. Se o tema já foi feito por uma referência analisada, não copie as falas nem os objetos do refrão.
   Use outros fatos ou outras comparações.

## O molde "Você é…"
1. **Gancho (0–3s):** 2ª pessoa + a coisa mais absurda e verdadeira, sem rodeio.
   Ex.: "Você é um pepino-do-mar. E você respira pelo cu."
2. **Logo em seguida, a prova:** uma frase que mostra que é sério ("Sim. É sério.") + o mecanismo em 1 frase.
3. **Blocos de fato:** fato curto → exagero ou pergunta retórica → **"Esse é seu [objeto do dia a dia]."**
   - O objeto tem que ser **específico e visual** (não "sua defesa", e sim "seu spray de pimenta").
   - Bônus de piada: um complemento depois do objeto ("Esse é seu snorkel. Só que do lado errado.").
   - Varie a construção a cada 2 blocos (pergunta, "E o pior:", "Ninguém te contou?").
4. **Escalada:** do mais estranho pro **mais absurdo**. O fato mais chocante fica no 4º ou 5º bloco (segundo gancho).
5. **Fecho que ressignifica o nome:** "Chamam de [nome] quem [sentido ruim]. Mas você [3 feitos, o 3º o mais absurdo]."
6. **Loop:** repete a 1ª frase, sem CTA falado. O pedido ("comenta…", "marca quem…") vai na legenda do post.

## Regras de piada (de `comedy-writer`, adaptadas)
- **A palavra engraçada fica no FIM da frase.** Leia em voz alta: o riso cai na última palavra.
- **Detalhe concreto ganha de adjetivo:** "Airbnb sem avaliação" é mais engraçado que "casa estranha".
- **Regra de três com quebra** no fecho: dois feitos normais + o terceiro absurdo.
- **Callback:** retome no fim uma palavra do gancho ("cu", "pepino") num sentido novo.
- **Sensacionalismo de manchete, conteúdo honesto:** "ISSO É REAL", "e o pior…", "ninguém te contou", tudo
  sustentado por fato conferido. Nunca prometa o que o vídeo não mostra.
- **Nunca explique a piada.**

## Limites
- Palavrão leve e anatomia ("cu", "bumbum", "pum", "cocô") são permitidos quando **são o fato científico**.
  Nada sexual, nada de piada com grupo de pessoas (gênero, etnia, religião, corpo de alguém real).
- Use `clean-comedy-rewrite` só para checar se alguma frase ofende alguém. Não use para tirar o besteirol.

## Formato e ritmo
- ~1:00 a 1:10. **3,2 palavras/s** (decisão da usuária): 190–220 palavras.
- Frases curtas (máx. 12 palavras), números por extenso pra TTS, sem parênteses nem reticências.
- Cada frase = um beat (~2s) com algo novo na tela: o objeto do refrão aparece; cartão amarelo curto
  ("ESSE É SEU SNORKEL"); nome científico pequeno no topo; número grande quando houver.
- Título grande só no gancho. Legenda de 1–3 palavras, palavra-chave em amarelo.

## Checklist antes de entregar (nota 0–10; refazer se < 8)
1. O gancho é verdadeiro, absurdo e cabe em 3s?
2. Cada bloco tem fato conferido + objeto específico + piada na última palavra?
3. Escalada até um pico no meio, e segundo gancho?
4. O fecho ressignifica o nome com regra de três e volta à 1ª frase?
5. Nenhuma frase ofende grupo de pessoas? Nada copiado de referência?
6. Contagem de palavras ÷ 3,2 dá ≥ 60s?

## Saída
`trabalho/<slug>/roteiro.md` com: ganchos alternativos (pontue com `ig-reel/hookscore.py` na versão em inglês),
tabela de beats (tempo, fala, visual, cartão), base científica com fontes, "⚠️ Conferir" e a nota do checklist.

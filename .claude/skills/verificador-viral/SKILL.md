---
name: verificador-viral
description: Portão de qualidade automático da fábrica viral, que SUBSTITUI a aprovação manual do roteiro. Dá nota ao roteiro (regras objetivas + gancho + rubrica de viralização) e, se passar, libera a produção sem esperar a usuária; depois confere o MP4 (QA quadro a quadro + rubrica de vídeo) antes de enviar; e, depois de postar, lê a curva de retenção pra aprender. Use sempre que a fabrica-viral terminar um roteiro ou um render, quando a usuária perguntar "isso viraliza?", pedir pra verificar/avaliar/dar nota a um roteiro ou vídeo, ou mandar a retenção de um vídeo postado.
---

# Verificador viral

A usuária pediu: **em vez de ela aprovar o roteiro, esta skill verifica tudo e confirma se viralizaria.**
Então ela é rigorosa: na dúvida, reprova e reescreve. Seja honesto: **nenhuma ferramenta garante
viralizar** (capa, horário, constância e algoritmo também pesam). O que este portão faz é eliminar os
motivos conhecidos de um vídeo curto ser pulado, medidos nas referências (`fabrica-viral/fichas/`)
e nos repositórios estudados (`ORIGEM.md`).

Pasta das ferramentas: `V=.claude/skills/verificador-viral` · `F=.claude/skills/fabrica-viral/ferramentas`

## Portão 1: ROTEIRO (antes de produzir, no lugar do "ok" da usuária)

1. **Regras objetivas.** Salve as falas em `trabalho/SLUG/falas.txt` (uma por linha) e rode:
   `python3 -I $V/validar_roteiro.py trabalho/SLUG/falas.txt --molde voce|construiu|ese|passo|flat2d`
   Qualquer **✗ DURO** = reescreva e rode de novo. Avisos entram na nota.
2. **Gancho (3 s).** Escreva 3 ganchos de fórmulas diferentes (skill `viral-hooks`), traduza cada um pro
   inglês e rode `python3 -I $V/hookscore.py ganchos_en.txt`. O script é calibrado pra inglês e
   desconta qualquer frase que começa com "You" (FRONTLOAD). Por isso:
   - mínimo **70** nos moldes sem "Você" no começo;
   - mínimo **60** no molde "Você é…".

   Abaixo de 50 em todos = nenhum serve, escreva outros. O **1º quadro** tem que mostrar o gancho (o
   bicho, a coisa absurda), não um cenário vazio.
3. **Rubrica de viralização.** Dê nota de 0 a 10 a cada critério, **citando a linha do roteiro** que
   justifica a nota. Seja o espectador impaciente, não o autor.

   | critério | peso | 10 = |
   |---|---|---|
   | Gancho | 20% | fato verdadeiro e absurdo/curioso na 1ª frase, sem introdução; dá vontade de saber o resto |
   | Loop aberto | 10% | uma pergunta ou promessa no começo que só se resolve depois da metade |
   | Escalada + 2º gancho | 15% | cada bloco mais estranho que o anterior; um pico/virada entre 40% e 60% do vídeo |
   | Densidade | 10% | algo novo em toda frase; nenhuma frase que só repete ou enrola |
   | Humor / emoção | 15% | comparação concreta, piada na última palavra (skills `roteiro-humor`, `comedy-writer`) |
   | Ensina algo verdadeiro | 15% | todo fato da fala com fonte; nada de "⚠️ Conferir" dentro da fala |
   | Final que prende | 10% | loop pra 1ª frase / "Na parte dois…?" / "Parabéns. Você construiu…" |
   | Compartilhável | 5% | dá vontade de mandar pra alguém ou comentar; pedido só na legenda do post |

4. **Advogado do diabo.** Liste os 3 momentos mais prováveis de a pessoa rolar a tela (ex.: segundo 0–3,
   frase de explicação longa, final previsível) e conserte cada um. Leia as falas em voz alta mentalmente
   a 3,2 palavras/s procurando trava de pronúncia (siglas, nomes estrangeiros).
5. **Decisão.**
   - **PASSA** se: nenhum ✗ DURO; gancho no mínimo do passo 2; **nota ponderada ≥ 8,5**; nenhum critério
     abaixo de 7; nenhum fato sem fonte na fala.
   - Passou: salve `trabalho/SLUG/verificacao.md` (notas, citações, ganchos pontuados, o que foi
     consertado) e **siga direto pra produção, sem esperar o ok**. Mostre à usuária um resumo de 3 linhas
     (gancho, nota, link das fontes) enquanto produz.
   - Não passou: reescreva só o que tirou nota baixa e repita do passo 1. **Até 3 voltas.** Na 3ª
     reprovação, mostre à usuária o roteiro, as notas e o motivo, e pergunte.
6. **Ainda pede o ok da usuária, mesmo passando:**
   - gastar crédito pago;
   - tema sensível: saúde/remédio, política, tragédia, pessoa real viva, criança;
   - fato que só existe como ⚠️ Conferir e o vídeo depende dele;
   - quando ela mesma pedir pra ver antes.

## Portão 2: VÍDEO (depois do render, antes de enviar)

1. **QA automático:** o `video.py render` já roda; à mão:
   `python3 -I $F/qa.py trabalho/SLUG/SLUG.mp4 --tempo trabalho/SLUG/tempo.js`
   Ele confere:
   - formato 1080×1920, duração 1:00–1:30 e loudness −14 LUFS;
   - silêncio morto, quadro preto, imagem parada ≥ 0,5 s e pulos fora dos cortes;
   - se o `tempo.js` bate com o vídeo.

   **✗ DURO = conserte e re-renderize só os beats afetados** (apague os quadros deles em `quadros/`).
2. **Olhe `trabalho/SLUG/qa/visao_geral.jpg`** (1 quadro por segundo) e dê nota de 1 a 10:
   - gancho visual (o 1º quadro já mostra o assunto?);
   - ritmo (muda algo a cada 2–4 s?);
   - composição (câmera aberta, nada cortado);
   - legibilidade (legenda de 1–3 palavras, contraste, área segura);
   - transições;
   - sincronia (objeto aparece quando a palavra é dita);
   - mix (voz clara, efeito sem abafar);
   - final (fecha o loop).

   Liste cada conserto com o segundo e a gravidade (crítico/maior/menor). **Passa com média ≥ 8 e nenhum
   crítico.** Conserte os maiores que forem baratos (um beat), re-renderize e rode o QA de novo.
   Rubrica adaptada do `review-video` de DojoCodingLabs/remotion-superpowers.
3. Passou: envie o MP4 (SendUserFile) com a legenda do post (`ig-caption`) e uma linha:
   "Verificador: roteiro X/10, vídeo Y/10, QA sem erros."

## Portão 3: DEPOIS DE POSTAR (aprender com os números)

Peça à usuária uns 10–20 pontos da curva de retenção do app (segundo, % assistindo) e rode:
`python3 -I $V/retencao.py curva.csv --tempo trabalho/SLUG/tempo.js`
Ele mostra três coisas:
- quanto saiu nos 3 primeiros segundos;
- as quedas, **com a fala que estava tocando**;
- a ladeira do meio.

Leve **uma** lição concreta pro `fabrica-viral/regras.md`, na seção "Medido nos NOSSOS vídeos". Ex.:
"beat com explicação de mais de 16 palavras perdeu 9 pontos no viral09".

## Dicas que aumentam a chance (fora do vídeo)
- **Capa e primeira imagem** iguais ao gancho; texto da capa ≤ 4 palavras.
- **Legenda do post:** primeira linha = segunda frase de gancho, depois o pedido ("marca aquele
  amigo…") e as fontes.
- **Postar sempre no mesmo ritmo** (ex.: 1 por dia) vale mais do que acertar um vídeo isolado.
- No Instagram, os **Reels de teste** (mostrados primeiro a quem não segue a conta) servem pra comparar
  dois ganchos do mesmo vídeo. Se a opção não aparecer na conta, ignore.

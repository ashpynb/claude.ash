# Os 5 tipos de vídeo (moldes)

Cada um tem um exemplo nosso em `exemplos/` e referências medidas em `fichas/`.
**Personagem só em "E se tu…" e "2D flat"** (pedido da usuária); nos outros, o protagonista é a coisa
(o bicho, a obra, a montagem). **Acabamento cinema** (luz de cinema + malha bem feita) é opção pra
qualquer tipo 3D: ver `visual-3d.md`.

## 1. "Você é um…" (bichos e coisas vivas)
- **Estrutura:** gancho em 2ª pessoa com o fato mais absurdo ("Você tem o corpo inteiro coberto de
  paus duros.") → "Você é um [bicho]." → 5–7 vezes: fato (+ "Por isso…") → **"Esse é seu [objeto do
  dia a dia]."** (o objeto aparece na tela com cartão amarelo curto) → fecho "Chamam de [nome] quem
  [sentido ruim]. Mas você [feitos]." → repete a 1ª frase (loop).
- **Estilo:** 3D cartoon com luz de cena (fundo do mar, floresta) ou low-poly em dia claro.
- **Referências:** Maria-sem-vergonha 200 mil curtidas; porco 450 mil (fichas 05, 07).
- **Nosso:** `exemplos/viral04_voce_e` (ouriço-do-mar).

## 2. "Você construiu um…" (como as coisas funcionam)
- **Estrutura:** gancho "a coisa sem nada não funciona" ("Se você empilhar pedra no meio de um rio, a
  correnteza leva tudo.") → repetir: **"Mas…" (problema) → "Então você…" (peça entra) → "Esse é o
  [nome técnico]."** (etiqueta presa na peça) + um número real → **"Parabéns. Você construiu um…"**
- Toda peça escondida aparece **em corte transversal**; a câmera **voa** entre as peças.
- **Estilo:** 3D low-poly, dia claro (`exemplos/viral08` represa, `exemplos/corte_transversal`,
  `exemplos/viral06_lowpoly_modelos` avião).
- **Referências:** pedágio 943 mil, casa x tornado 608 mil, avião 193 mil (fichas 08, 10).

## 3. "E se tu…" (história com personagem)
- **Estrutura:** "E se tu [situação]?" + título grande → "Esse é o [nome]." → linha do tempo com
  número na tela (dia 1, semana 1, mês 1 · ou o relógio da prova 13:30, 14:00…) → dados com fonte
  ("Num estudo…") → **virada inesperada** → "Na parte dois: [pergunta]?" + cartão PARTE 2.
- **Estilo:** 3D boneco de primitivas (Sérgio). Cenário com objetos texturizados, coisas caindo com física.
- **Referências:** 500 mil a 1,7 mi views (ficha 06); boneco de primitivas (ficha 09).
- **Nossos:** `exemplos/viral07` (1 mês sem se mexer, cama com colcha que se molda),
  `exemplos/viral09` (redação do Enem, sala de prova).
- **Personagem fixo da série:** Sérgio. Padrão: pele clara, cabelo curto castanho, óculos, pijama
  azul listrado. A usuária pode mudar no Estúdio (no viral 09: topete preto, magro, pijama roxo,
  boné virado pra trás, cara de cansado).

## 4. Passo a passo (montagem de uma coisa real)
- **Estrutura:** "Um [coisa] tem N camadas." → "Passo um: [peça]." + explicação curta + medida na
  tela → cada camada desce no lugar → resumo dos passos.
- **Estilo:** isométrico técnico (papel claro, peças cinza com contorno, cartão "FIG 1"). Skill
  `anatomy` ajuda nas figuras.
- **Nosso:** `exemplos/viral05_passo_iso` (telhado).

## 5. 2D flat engraçado (coisa do dia a dia explicada com piada visual)
- **Estrutura:** gancho com pergunta do dia a dia + piada visual ("Por que o gato derruba tudo da
  mesa?") → "Esse é o [nome]." → 3 a 5 passos, cada um com uma metáfora desenhada e um número com
  fonte → virada engraçada → pergunta pro público ("E você, já…?").
- **Estilo:** 2D flat: vetor plano, cores chapadas, contorno escuro, personagem com expressão
  exagerada (piscar, bocão, olhos girando, gotinha de suor), objetos com contorno. Escala absurda
  (pilha, balança, contador, calendário correndo) entra aqui quando o tema tem número grande.
- **Personagem:** sim (Sérgio 2D ou outro desenhado no Estúdio).
- **Referência:** "1 trilhão" 690 mil views, 2D flat (ficha 10).
- **Nosso:** `exemplos/flat2d_sergio` (o Sérgio "1 mês sem se mexer" em 2D, canvas puro, antes da
  versão 3D): quarto, cama, cérebro com placa, operários, barras, balança, osso, coração, estrelinhas.

## Ganchos que funcionam (pra variar)
"E se tu…?" · "Você é um…" · "Sabe quando você…?" · "Imagina se…" · "Fulano só quer X, mas existe
um problema." · "Se você [fizer o óbvio], [desastre]." · número absurdo com prova social.
Skill `viral-hooks` gera mais variações.

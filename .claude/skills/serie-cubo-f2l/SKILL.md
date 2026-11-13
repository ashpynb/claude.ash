---
name: serie-cubo-f2l
description: Série "Cubo mágico: F2L em 5 vídeos" (cubo 3D em CSS animado sincronizado com a narração do Antônio). Use quando a usuária pedir o próximo episódio do cubo mágico, F2L, notação do cubo (R, U, L, F, x, y), ou correções nos episódios 1–5.
---

# Série cubo mágico: F2L em 5 vídeos

Regras desta série têm prioridade sobre as da `fabrica-viral` (ritmo mais calmo, notação na tela).

## Situação
| Ep. | Título | Estado |
|---|---|---|
| 1 | A língua do cubo (U, R, L, F, D, ', 2, x, y) | produzido (MP4 no histórico do git, commit "ep01") |
| 2 | Camadas × F2L (pares quina+aresta, 4 slots) | produzido |
| 3 | Primeiros casos (`R U R'`, `U R U' R'`, `F' U' F`) | produzido |
| 4 | Peças presas e branco pra cima (`y` + `R U R'`, `R U2 R'`) | **roteiro pronto, falta produzir** |
| 5 | Juntando tudo + treino de 3 semanas | **roteiro pronto, falta produzir** |
⚠️ Conferir no ep. 4: depois do `R U2 R'`, a aresta pode precisar de ajuste antes de cair num caso do ep. 3.

## Arquivos (caminhos relativos a esta pasta)
- `roteiro/gerar.py`: **fonte única** dos roteiros. Edite e rode `python3 roteiro/gerar.py` (gera
  `roteiro/epNN.md/.json` e confere 60–90 s). Use `|` no texto pra dividir beats.
- `anim/cubo.html`: cubo 3D em CSS/JS puro (API `window.CUBO`, cenas prontas `ep1-R`, `ep3-caso1`,
  `ep4-branco`…). Gravar: `anim/cubo.html?cena=ep3-caso1&auto=1&gravar=1&vel=900`.
- `producao/`: `narrar.py` (voz por beat), `montar_tempo.py epNN dir_voz`, `epNN.html` (motor
  `motor.js`/`motor.css`), `render.js` (file://), `mixar.py`. `epNN_falas.json` guarda `rate`, `gap`
  e `resp` de cada beat.
- `README.md` e `HANDOFF.md`: histórico da série (pedido original, decisões).

## Regras da série (pedidas pela usuária)
- **Duração:** mínimo exato 1:00, máximo 1:30. Acessível, a usuária aprende junto.
- **Ritmo:** gancho/introdução ~3,1–3,2 p/s; explicação ~2,9 p/s (2,5 foi "lento demais").
  Medido no ep. 1: intro `rate +24%`, pausas ≤0,10 s, respiro 0,08 s (0,2 s após algoritmo) → 3,15 p/s;
  explicação `rate -4%`, pausas ≤0,20 s, respiro 0,18 s (0,38 s após algoritmo) → 2,92 p/s.
  Giros seguidos ("érre, u, érre linha") precisam de ~0,33 s cada.
- **Algoritmo falado = cubo girando no mesmo instante** (o giro começa no início da palavra, pelo
  `WordBoundary`), com a notação grande na tela (exceção à regra de "sem texto grande").
- Cada algoritmo aparece **2 vezes**: explicando e só mostrando.
- **Legenda mostra a notação**: a voz fala "érre linha", a legenda escreve **R'** ("u dois" → U2,
  "éfe dois éle" → F2L, "xis/ípsilon" → x/y). Karaokê: palavra em amarelo, notação em ciano
  (`motor.js`, `gruposLegenda`).
- Narração pro TTS com letras por extenso: "érre", "éle", "u", "éfe", "dê", "xis", "ípsilon",
  "linha" (pra '), "dois" (pra 2). Nenhum algarismo.
- Cores: branco embaixo (D), amarelo em cima (U), verde na frente (F), vermelho à direita (R).
  Casos conferidos no simulador pro slot frente-direita.
- CSS 3D: destaque de adesivo só com borda branca por dentro; `box-shadow` externo e
  `backface-visibility:hidden` fazem buracos pretos no Chromium.
- Peças "voando" pra explicar conceito sobem BEM acima do cubo; cruz/slots se mostram por baixo.
- Sem música; voz Antônio; imagens de IA só com custo mostrado e ok da usuária.

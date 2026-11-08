# Passagem de bastão — Série "Cubo mágico: F2L em 5 vídeos"

## Pedido original da usuária
- Série de **5 vídeos** ensinando a resolver o cubo pelo **F2L**.
- **Vídeo 1:** revisar a notação (y, x, U, L, R…) mostrando o cubo **em CSS, animado**.
- Depois: explicar **o que muda do método de camadas pro F2L** (resolve as duas camadas de uma vez).
- **Duração:** mais de 1:00, idealmente entre **1:05 e 1:30**.
- Seguir os **requisitos de vídeo viral** das skills (`diretor-video-aula`, `produtor-video-aula`, `analisar-video-referencia`).
- **Acessível e NÃO rápido demais:** a usuária quer aprender junto.

## O que já está pronto (branch `claude/cubo-magico-f2l-videos-0r1398`)
| Arquivo | O que é |
|---|---|
| `roteiro/gerar.py` | **Fonte única** dos roteiros. Edite aqui e rode `python3 roteiro/gerar.py`. Ele confere se cada episódio fica entre 65 e 90s. |
| `roteiro/ep01–05.md` / `.json` | Roteiros gerados: ficha, narração por clipe, beats (tempo, fala, visual, movimento, texto, SFX, ⭐ vídeo IA), prompts e kit de estudo. |
| `anim/cubo.html` | Cubo 3D em CSS/JS puro: notação, sequência, velocidade, modo foco F2L e 12 cenas prontas. Para gravar: `?cena=ep3-caso1&auto=1&gravar=1&vel=900`. API em `window.CUBO`. |
| `referencias/aprendizados.md` | Regras específicas da série (veja abaixo). |

## Episódios
1. **A língua do cubo** (1:17): faces U, R, L, F, D; regra do sentido horário (R sobe, L desce); linha ('); 2; x e y.
2. **Camadas × F2L** (1:12): as 8 peças soltas do método de camadas viram 4 pares (quina + aresta) em 4 slots, depois da cruz branca.
3. **Primeiros casos** (1:14): `R U R'` (quina em UFR com branco pra direita, aresta em UB); `U R U' R'` (par pronto em UFR+UR, branco pra frente); espelho `F' U' F` (branco pra frente, aresta em UL).
4. **Casos chatos** (1:14): peça presa em outro slot (`y` até frente-direita + `R U R'`); branco pra cima (`R U2 R'`); a cruz se mantém porque R/R' andam em dupla.
5. **Juntando tudo** (1:15): ordem completa; look ahead; treino de 3 semanas com 10 min/dia; gancho para OLL/PLL.

As durações são só da fala, a 2,5 palavras por segundo. Com os respiros depois dos algoritmos, cada vídeo fica em torno de 1:20.

## Decisões tomadas (não desfazer sem motivo)
- **Ritmo da fala: 2,4–2,6 p/s**, abaixo do padrão da skill (2,8–3,3), a pedido da usuária. Sem pausas arrastadas: o tempo extra vem de frases curtas e de respiros de ~0,25s depois de cada algoritmo. No TTS: `speed` 1,0–1,05; silenceremove com `stop_duration=0.25`.
- **Algoritmo falado = cubo girando no mesmo instante**, com a notação grande na tela. Cada algoritmo aparece 2× (uma explicando, outra só mostrando).
- **Visual principal = cubo CSS** (sem gasto de créditos). Imagens de IA só para `bg_arena`, `hero`, `chefao` e `bg_mapa`, reaproveitadas nos 5 episódios. ⭐ = 1 vídeo de IA por episódio, no gancho.
- **Narração pronta pra TTS:** letras por extenso ("érre", "u", "éle", "éfe", "dê", "xis", "ípsilon", "linha", "dois"), nenhum algarismo. Para dividir os beats na mão, use `|` no texto do `gerar.py`.
- **Esquema de cores:** branco embaixo (D), amarelo em cima, verde na frente, vermelho à direita.
- **Algoritmos verificados no simulador** (`anim/cubo.html`): as cenas dos eps. 2, 3 e 5 resolvem o par no slot frente-direita. A `ep4-preso` tira o par do slot de trás-esquerda (DBL/BL) pro topo, e a `ep4-branco` tira o branco de cima.

## Pendente
1. **Juntar com o `referencias/aprendizados.md` desta sessão**, se existir. Mesclar, não sobrescrever. Se as regras daqui forem de outra série, elas valem para todo vídeo (são métricas de vídeos virais), mas o **ritmo mais calmo** é pedido explícito da usuária para esta série.
2. Revisar os roteiros com esses aprendizados e regenerar com `gerar.py`.
3. **Produção** (`produtor-video-aula`): integrar o `cubo.html` ao projeto de animação (gravar com Playwright ou portar a lógica para Remotion), gerar voz por clipe, legendas, SFX e render `out/epNN.mp4`.
4. **Créditos:** mostrar a quantidade e o custo de imagens e vídeos de IA e **esperar o "ok"** antes de gerar.
5. Pontos a conferir (estão em "⚠️ Conferir" em cada `.md`): no ep. 4, depois do `R U2 R'`, a aresta pode precisar de um ajuste extra antes de cair num caso do ep. 3.

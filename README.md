# Série "Cubo mágico: F2L em 5 vídeos"

Roteiros feitos com a skill `diretor-video-aula`, prontos pro `produtor-video-aula`.
Cada vídeo dura ~1:12–1:17 só de fala (com os respiros depois dos algoritmos: ~1:20).

| Ep. | Título | O que você aprende |
|---|---|---|
| [1](roteiro/ep01.md) | A língua do cubo | U, R, L, F, D · linha (') · dois (2) · rotações x e y |
| [2](roteiro/ep02.md) | Camadas × F2L | por que o F2L junta quina + aresta em **pares** e usa 4 **slots** |
| [3](roteiro/ep03.md) | Seus 2 primeiros casos | `R U R'` · `U R U' R'` · espelho `F' U' F` |
| [4](roteiro/ep04.md) | Peças presas e branco pra cima | tirar peça presa com `y` + `R U R'` · `R U2 R'` |
| [5](roteiro/ep05.md) | Juntando tudo + treino | ordem completa · look ahead · plano de 3 semanas |

## Arquivos
- `roteiro/epNN.md` — roteiro legível: narração, tabela de cortes (beats), prompts, kit de estudo.
- `roteiro/epNN.json` — o mesmo em JSON, para a animação ler.
- `roteiro/gerar.py` — fonte de tudo. Editou o texto? `python3 roteiro/gerar.py` regenera os .md/.json.
- `anim/cubo.html` — cubo 3D em CSS puro (sem biblioteca). Abra no navegador:
  - botões de movimento, campo de sequência, velocidade (padrão devagar), **modo foco F2L**;
  - cenas prontas da série (`ep1-R`, `ep3-caso1`, `ep4-branco`…);
  - para gravar: `anim/cubo.html?cena=ep3-caso1&auto=1&gravar=1&vel=900`.
- `referencias/aprendizados.md` — regras desta série (ritmo mais calmo, algoritmo falado = cubo na tela).

## Notação usada
Cores: branco embaixo (D), amarelo em cima (U), verde na frente (F), vermelho à direita (R).
Os casos foram conferidos no simulador para o slot frente-direita.

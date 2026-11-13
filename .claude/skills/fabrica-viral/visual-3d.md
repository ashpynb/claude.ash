# Visual 3D: kit, câmera, receitas e erros conhecidos

Toda cena é uma página `cena.html` (1080×1920) com `window.renderAt(t)` determinística, renderizada
quadro a quadro pelo Playwright (WebGL SwiftShader) e montada no ffmpeg. Comece de
`ferramentas/modelo_cena.html` (`video.py novo SLUG`) ou de um exemplo (`--de viral09`).

## kit3d.js (em `ferramentas/`, importado como `./kit3d.js`)
| Função | Pra quê |
|---|---|
| `criarRender(W,H)` | renderer com sombra macia, ACES, ambiente RoomEnvironment |
| `lin('#hex')` | cor sRGB → linear (sem isso fica lavado) |
| `mat(cor,{rough,metal,map,transp,op,emis,ei,side,envI})` | material padrão (com cache) |
| `T.madeira/papel/colcha/tapete/piso/listras/grad(...)` | texturas procedurais (canvas) |
| `tex(w,h,draw,rep)` | textura própria desenhada em canvas (placas, capas, telas) |
| `G.cx(w,h,d,r)` caixa arredondada · `G.cap(r,l)` cápsula · `G.esf(r)` · `G.cil(rt,rb,h)` | geometrias |
| `malha(geo,mat,{sombra,recebe})` | mesh com sombra |
| `boneco(P)` | personagem de primitivas. `P={pele,cab:'curto'|'cacheado'|'topete'|'lados'|'careca',cabCor,roupa:'pijama'|'camiseta'|'jaleco'|'traje',cor,calca,corpo:'magro'|'normal'|'fofo',oculos,bone:'#cor'}` |
| `pose(b,o,t)` | `o.cara`: feliz, feliz2, confiante, surpreso, assustado, triste, preocupado, cansado, relax, tonto · braços `bE/bD` (abre, rad) e `bEx/bDx` (pra frente, negativo) · `joinha` · `olhar:[x,y]` · `sentado` · `perna` (espessura) · `pEx/pDx` (andar) · `cabX/Y/Z` · `inclina` · `escuros` · `capacete` · `bigode:'#cor'` · `rugas` · `tremor` · `pisca` |
| `simular(objs,{chaoY,estaticos,dur})` | física cannon-es **pré-calculada**; devolve `(meshes,tempo)=>…` |
| `poeira(n)` + `animaPoeira(pts,t)` | poeirinha brilhante dos insertos |
| `corte(r,grupo,plano)` / `faceCorte(w,h,'terra'|'parede',furos)` | corte transversal + tampa com furo |
| `etiqueta(txt,alvo,{cor,dy})` (+ `o.t0/o.t1`) e `atualizaEtiquetas(cam,t,W,H)` | pílula presa no objeto |
| `trilha(pontos,alvos)` | câmera voando numa curva |
| `copias(geo,mat,lista)` | InstancedMesh (fila de carros, floresta) |
Também há modelos CC0 (Quaternius/Kenney) em `ferramentas/modelos/` (GLTFLoader em `vendor/jsm`).
Mais modelos: `git clone --filter=blob:none` de `trebeljahr/quaternius-showcase` ou `shorepine/kenney`.

## Acabamento "cinema" (opção do Estúdio: luz de cinema e malha bem feita)
Quando o pedido trouxer "Acabamento cinema":
- `luzCinema(cena,{alvo,quente,fria,forca,neblina})` no lugar do sol + hemisfério: principal quente
  (spot com sombra macia), **contraluz fria forte** desenhando a silhueta, preenchimento frio baixo,
  neblina exponencial. Mude a mira por plano com `.mira([x,y,z])`. Exposição ~0.9.
- Fundo nunca preto vazio: parede/cenário ao fundo pegando a neblina, ou fundo em degradê escuro.
- Vinheta em CSS (`radial-gradient` escurecendo as bordas) por cima do canvas.
- Malha: `G.esfFina`, `G.capFina`, `G.cxFina` (bordas arredondadas, 8 segmentos), `G.extrusaoFina`
  (bisel 8, curva 48). Materiais com `rough` 0.25–0.5 em objetos de destaque pra brilhar na contraluz.
- Custo: ~30% mais tempo de render (spot + mais polígonos).

## 2D flat (tipo "2D flat engraçado")
Canvas 2D puro (sem three.js), mesmo esquema de `renderAt(t)`, legendas e `video.py`.
Base: `exemplos/flat2d_sergio/cena.html` (personagem `boneco()` 2D com contorno, sombra chapada,
cabelos, roupas, acessórios e expressões; `quarto()`, `cama()`, insertos com fundo de raios).
Regras: cor chapada + contorno escuro de 4–6 px, no máximo 1 tom de sombra por cor, expressão
exagerada a cada beat, uma piada visual por frase, câmera = `cam(cx,cy,zoom,…)` com push-in.
Não use `ctx.filter` (blur/sepia travam no render); faça desfoque reduzindo e ampliando um canvas.

## Câmera (regra da usuária: aberta)
- Vertical, fov 32. Boneco tem ~2,6 de altura: **distância 10–16** pra corpo inteiro; cenário 14–18;
  vista aérea de terreno 50–75. Close (≤6) só em 1–2 reações no vídeo inteiro.
- Use `camOrbit(alvo, dist, azimute, elevação)`; varie o tamanho do plano a cada beat; push-in lento
  dentro do beat (`lerp(d, d*0.93, ease(u))`).
- Em paisagem, câmera ao longo do vale (azimute ~0–25°) e acima do relevo; senão fica dentro do morro.
- Corte transversal: plano `x<=0` mantido, câmera do lado `+x` olhando pra `-x`; tudo que deve
  aparecer no corte fica em `x<0` (setas, gotas, etiquetas).

## Movimento e acabamento medidos (claude-animated-shorts, MIT: 20 shorts de referência, 4 rodadas de verificador)
Números medidos por quadro em `mromidev/claude-animated-shorts` (references/STYLE_BIBLE.md e SKILL.md).
Valem pra qualquer estilo 3D nosso; o `qa.py` cobra os itens marcados com ✓.
- ✓ **Nunca parado:** todo plano "parado" faz push-in de **0,15–0,35% por quadro** (0,6%/quadro na
  palavra de impacto). Imagem igual por ≥ 0,5 s o QA aponta; ≥ 1,5 s reprova.
- **Movimento em rajada que freia:** quando a câmera anda, a velocidade máxima é no 1º quadro e cai em
  ~8–10 quadros (`easeOutCubic`/`easeOutExpo`), não `easeInOut` simétrico. Deslizes longos: 18–40 quadros.
- **Corte seco só em salto grande** (lugar/tempo); o resto é câmera seguindo um objeto, whip-pan com
  borrão ou dissolve de 6–8 quadros.
- **Tremida de impacto:** troca de sinal a cada quadro e some em **7 quadros**
  (`d*(-1)**f*exp(-f/2.5)`). Inclinação (roll) de 4–5° em queda/susto.
- **Reação visual 0–3 quadros ANTES da palavra** que ela ilustra (o olho chega antes do ouvido).
- **Profundidade:** desfoque de fundo em ~1/3 do tempo (closes e insertos), foco nos olhos; planos
  abertos nítidos. Neblina = cor do horizonte. Brilho (bloom) só em coisa que emite luz.
- **Contorno escuro** (`vendor/jsm/effects/OutlineEffect.js`) ~3 px em 1080 px, quase preto, em
  silhueta e quina, nunca na linha do horizonte. Personagem 2D sobre cenário 3D leva contorno próprio.
- **Cor de dia:** luz média ~0,55, sem preto esmagado; sombra fria (azulada), luz quente. O QA mostra
  "luz média" e "saturação média" pra comparar entre vídeos.
- **Armadilhas de leitura** (o verificador deles pegou): objeto a menos de ~2 m da lente vira borrão
  cortado na borda; arbusto cortado pela borda vira "bola verde"; placa pintada fica ilegível com sol de
  lado (use material sem luz); bandeira inventada pode parecer de um país real.

## Receitas que já funcionaram
- **Quarto com cama** (viral07): colchão + travesseiro que afunda no "plof" + **colcha que se molda
  ao corpo** (malha deformada pelas cápsulas do corpo deitado). Deitar: grupo externo rot.x −90° +
  interno rot.z +90°.
- **Sala de prova** (viral09): carteiras (mesa + cadeira), lousa com texto, relógio com ponteiros 3D
  que andam com a história, folha que enche linha a linha, colegas de costas.
- **Inserto**: fundo `T.grad` + disco de chão + `poeira`, um objeto grande no centro (coração
  extrudado com bevel, balança, barras, troféu, pote de moedas com física).
- **Vale + barragem** (viral08): terreno low-poly com `flatShading` e cor por altura, água com ondas
  por vértice, árvores em `copias`, perfil extrudado, tampas de corte com textura de terra/rocha.
- **HUD/cartões** como HTML por cima (`#num`, `#card`, `#tema`, chips): mais nítido que texto 3D.

## Erros que já cometemos (não repita)
- Câmera perto demais / dentro do morro / atrás de árvore → `video.py testar` e olhe a folha.
- **Personagem na frente da cadeira** em vez de sentado nela (viral 09): a carteira girada 180°
  inverte o lado da cadeira; posicione o quadril em cima do assento.
- Boné cobrindo os olhos: aba pra trás (`rotation.x` negativo) e topete saindo na testa.
- Texto pintado em textura antes da fonte carregar → `await document.fonts.load(...)` no topo do módulo.
- Coisas posicionadas do lado cortado (`x>0`) somem no corte.
- `ctx.filter` (blur/sepia) no canvas 2D e filtros caros travam o SwiftShader: use CSS `filter` no
  `<canvas>` ou sobreposição.
- `Object.assign(mesh,{position:…})` quebra (position é só leitura): use `mesh.position.set`.
- Estado que um beat muda (escala, posição do sol) precisa ser resetado no começo do `renderAt`,
  porque os 4 processos renderizam trechos diferentes.
- Cores lavadas: exposição ~0.8–0.9, `envMapIntensity` baixo (0.15–0.35) em terreno e concreto.

## Desempenho
~1–1,5 s por quadro com sombra macia; 4 processos ≈ 70 quadros/min → 1:20 leva ~35 min.

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

## Câmera (regra da usuária: aberta)
- Vertical, fov 32. Boneco tem ~2,6 de altura: **distância 10–16** pra corpo inteiro; cenário 14–18;
  vista aérea de terreno 50–75. Close (≤6) só em 1–2 reações no vídeo inteiro.
- Use `camOrbit(alvo, dist, azimute, elevação)`; varie o tamanho do plano a cada beat; push-in lento
  dentro do beat (`lerp(d, d*0.93, ease(u))`).
- Em paisagem, câmera ao longo do vale (azimute ~0–25°) e acima do relevo; senão fica dentro do morro.
- Corte transversal: plano `x<=0` mantido, câmera do lado `+x` olhando pra `-x`; tudo que deve
  aparecer no corte fica em `x<0` (setas, gotas, etiquetas).

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

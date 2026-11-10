# Ficha 09: 3D "boneco de primitivas" (reel Dfil9zGuebq, série "Axé do dia · parte 15")

Link: https://www.instagram.com/reel/Dfil9zGuebq/ · enviado pela usuária ("tenta criar esse tipo de modelo de animação").
Medido aqui: 58,1 s, 1080×1920, 60 fps, 17 cortes (1 a cada ~3,4 s; planos de 1,5 a 5,5 s).
Quadros: `img/09_boneco_primitivas.jpg` (1 a cada 2 s) e `img/09_boneco_primitivas_detalhe.jpg`.

## Como os objetos são feitos (o que faltava nos nossos)
- **Personagem montado de primitivas**: tronco em cápsula levemente afunilada, braços em cápsula
  única com mão de esfera (sem cotovelo/dedos), pernas em cápsula, tênis de esfera achatada,
  cabeça de esfera grande, cabelo como calota de esfera, orelhas e nariz de esferinhas.
- **Rosto pintado** (olhos de ponto com brilho, sobrancelha de traço, boca simples) sobre a
  esfera, não modelado. Expressão muda trocando o desenho (triste, sorriso, surpresa).
- **Material com textura de verdade**, não cor chapada: cesto de palha trançada, toalha com
  estampa de florzinha, piso de lajota, paredes lisas. Os objetos "contam" pela textura.
- **Luz suave de estúdio**: sem contorno preto, sombra macia de contato no chão, tons quentes,
  pouca saturação na parede, cor forte só no personagem e no objeto principal.
- **Física**: os búzios caem, quicam e se espalham no cesto (simulação, não animação à mão).
- **Insertos**: fundo em degradê de uma cor (roxo, azul, marrom, vermelho) com chão em disco
  mais escuro e **poeirinha brilhante** flutuando; um objeto grande no centro (búzio com olhos).
- **Câmera**: alterna plano aberto do cenário, close no objeto e plano médio do personagem;
  push-in lento dentro do plano.

## Texto e som
- Legenda: **1 palavra por vez**, fonte arredondada grossa (tipo Lilita One), amarela com
  contorno marrom escuro, no meio da tela. (Nossa regra continua 1–3 palavras, chave amarela.)
- Selo fixo pequeno no topo: "AXÉ DO DIA · PARTE 15" (série numerada).
- Pergunta curta no topo nos insertos ("SÓ CONTAR?", "JÁ JOGOU?").
- CTA final em cartão (consulta paga, link na bio). Não copiamos o CTA comercial.

## O que eu apliquei no viral 07 (Sérgio)
- `producao/kit3d.js`: boneco de cápsulas e esferas com rosto pintado em textura (casca esférica),
  óculos 3D, capacete, expressões; texturas procedurais (madeira, papel de parede, colcha
  xadrez acolchoada, listras do pijama, tapete, piso); luz com ambiente RoomEnvironment +
  sombra PCF macia; física **cannon-es** pré-calculada (determinística no render).
- Cama simulada: colchão, travesseiro que afunda no "plof", e **colcha que se molda ao corpo**
  (malha deformada pelas cápsulas do corpo: tronco, pernas, pés e braços; a perna afinando
  abaixa a colcha) e cai pelas bordas.
- Fonte Lilita One (OFL) nas legendas, insertos com degradê + disco + poeirinha.

## Ferramentas novas (GitHub/npm, licenças abertas)
- `cannon-es` 0.20 (MIT, pmndrs) — física. `vendor/cannon-es.js`.
- three r149 `examples/jsm`: `RoomEnvironment` (luz ambiente bonita sem HDR), `RoundedBoxGeometry`
  (caixas arredondadas pra móveis), `OutlineEffect` (contorno cartoon, se quiser).
- Custo do render aqui: ~1,5 s/quadro com sombra macia (SwiftShader); 4 processos em paralelo
  (`producao/render_par.js`) → ~1 h por vídeo de 1:20.

## ⚠️ A conferir
- Ritmo de fala da referência não medido ainda (transcrição pendente).

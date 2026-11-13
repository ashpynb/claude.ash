# Ficha 10: três TikToks (pedágio, 1 trilhão, casa contra tornado)

Enviados pela usuária: "consegue através de ver esses vídeos melhorar a criação de vídeo 3d?"
Medido aqui (yt-dlp + ffprobe + cortes + faster-whisper tiny, que conta um pouco a menos).

| | Pedágio (@agoraeuseicomo) | 1 trilhão (@22clipsx) | Casa x tornado (@batdetetctive) |
|---|---|---|---|
| Views / curtidas | 943 mil / 97 mil | 690 mil / 99 mil | 608 mil / 33 mil |
| Duração | 2:32 | 1:13 | 1:17 |
| Molde | "Você construiu um…" | "Imagina…" + escala absurda | "Você construiu um…" |
| Estilo | 3D low-poly, dia claro | 2D vetorial plano | 3D low-poly com **corte do terreno** |
| Ritmo da fala | ~3,0 p/s | ~2,5 p/s (muito número) | ~3,1 p/s |
| Cortes detectados | 14 (câmera voa sem cortar) | 18 (~1 a cada 4 s) | poucos (câmera contínua) |
| Legenda | 1 palavra, branca, pequena | 1–3 palavras, MAIÚSCULA, chave amarela/vermelha | frase curta minúscula |
Quadros: `img/10_pedagio.jpg`, `img/10_trilhao.jpg`, `img/10_casa_tornado.jpg`.

## O que os 3D fazem que o nosso ainda não fazia
1. **Corte transversal (vista em corte)**: o terreno é cortado como bolo pra mostrar o que tem
   embaixo (pistões, bunker, cofre do dinheiro do pedágio, escada da cabine). É o que faz o
   "como funciona" ficar claro. → `corte()` no kit (planos de recorte do three.js + tampa de terra).
2. **Etiquetas presas no objeto** ("• PAGOU", "• SANFONA", "• AR LIMPO", "• DEVAGAR"): pílula
   branca com ponto colorido, acompanha o objeto na tela, aparece quando o nome é falado.
   → `etiqueta()` no kit (projeta a posição 3D na tela).
3. **Câmera que voa sem cortar** entre os pontos (plano aéreo → desce até a cabine → entra no
   corte) e **borrão de movimento** nas passagens rápidas. → `trilha()` (curva Catmull-Rom) e
   borrão por sub-quadros no `render_par.js` (`--borrao`).
4. **Muitas cópias baratas** (fila de carros por quilômetros, árvores) com InstancedMesh.
5. **Escala de mundo**: plano aberto mostrando a estrada inteira, o tamanho real das coisas.

## O que o 2D de escala ensina (1 trilhão)
- Gancho "Imagina acordar e ver isso" + tela de celular com o número absurdo.
- **Comparação de escala visual**: pilha de notas até a Estação Espacial (1.000 km), balança com
  peso em kg, grade de 1.000 quadradinhos, contador LED, calendário correndo, personagem envelhecendo.
- Cada número vira um objeto/contador na tela; fecha com "E você?" (pergunta pro público).
- Esse molde ("escala absurda") ainda não estava no Estúdio: entrou como tipo novo.

## Regras novas
- Em "Você construiu um…": **toda peça escondida aparece em corte** e ganha etiqueta quando é nomeada.
- Câmera contínua entre peças (voo) vale tanto quanto corte seco; use voo quando a peça seguinte
  está no mesmo cenário.
- Ritmo das três: 2,5–3,1 p/s. Nossa regra de 3,2 p/s continua (fica no topo da faixa).

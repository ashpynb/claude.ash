# Aprendizados (lidos pelo diretor e pelo produtor antes de cada vídeo)

Só entram aqui regras medidas em vídeos ou pedidas pela usuária. Quando uma regra de série
conflita com uma regra geral, vale a da série (está marcada).

## Regras gerais (todos os vídeos)

### Decisões da usuária (valem pra TODO vídeo, salvo pedido explícito)
- **Só vídeos virais em 3D cartoon** (como o EP01 abelhas e o low-poly da ficha 04). No máximo, **2D
  explicativo** no estilo do Traço Curioso (ficha 04). **Sem pixel art. Plano de economia cancelado.**
- **Nenhum vídeo tem música.** Só narração (Edge TTS Antônio, já configurada) + efeitos sonoros.
- **Título grande SÓ nos primeiros segundos (gancho, ~0–3s), depois some.** No resto do vídeo, sem
  texto grande: só legenda + números/notação que ensinam algo (ex.: "25 cm", "12:00", "R U R'").
  (Corrigido pela usuária após a ficha 01: o título grande fixo da referência era o problema, não o
  título no gancho.)
- **Ritmo viral (~3,2–3,3 p/s) em todos os vídeos, menos na série do cubo** (cubo: intro ~3,15,
  explicação ~2,9). Se o ritmo viral deixar o vídeo abaixo do mínimo de duração, acrescentar
  frases (só fatos conferidos ou piadas), nunca falar mais devagar.

### Texto na tela (pedido da usuária, EP01 abelhas)
- **Nada de texto grande no topo repetindo a fala.** No vídeo das abelhas, a palavra-chave
  gigante em cima + legenda embaixo foi "muita informação"; ficou só a legenda.
- Elementos no meio da tela só quando ensinam algo que a fala sozinha não mostra
  (contador, quiz, notação do cubo).

### Gancho e CTA (ficha 01, 1 referência — confirmar em mais vídeos)
- Gancho de **dor do espectador em pergunta** nos primeiros ~3,5s ("Sabe quando você…?").
- CTA de **palavra-chave nos comentários** ("comenta X") funciona melhor que "me segue" no fim.
- Ritmo da referência: 3,4 p/s (confirma o ritmo viral ~3,2–3,4).

### Roteiro e processo (ficha 02, descrita pelo Gemini — 1 referência)
- Fórmula viral: **gancho com paradoxo → cenário → escalada → virada**.
- Gancho de **prova social com número grande** ("29 milhões de views") também funciona.
- Antes do render final, um **verificador dá nota 0–10** contra estes aprendizados; refazer se < 8.
- Ritmo do exemplo: imagem muda a cada frase, cortes sincronizados com a fala, câmera deslizando no 3D.

### Visual, câmera e som (ficha 03: what-if-animation, MEDIDO em vídeo de 4,2M views)
- **Cortes por mudança de tamanho de plano** (aberto → inserto → médio → close → reação), ~27/min na
  abertura, plano 0,7–3s. Nunca dois planos vizinhos iguais.
- **Luz de entardecer com fonte visível + rim light quente + neblina + grão/vinheta.** Meio-tons escuros.
- **Modelos 3D CC0 prontos (Quaternius/Kenney) em vez de primitivas.** Ver ficha 03 §8.
- **Som: um efeito por ação, ambiente por lugar; hit na pausa DEPOIS da palavra.** (Sem música, por decisão
  da usuária; a "trilha que corta na virada" da referência NÃO se aplica.)
- Rodar o **checklist de 11 pontos** (ficha 03 §6) numa folha de quadros antes do render final.

### Ficha 04: 3 reels virais (medidos: cortes, transcrição, quadros)
- **Legenda de 2–3 palavras por vez, centro da tela, palavra-chave em amarelo** (3 de 3 reels: regra estável).
- **Animação contínua** (câmera/objetos se movendo) em vez de muitos cortes secos: 4–11 cortes detectados em
  66–77s. O que muda a cada frase é um elemento novo entrando (ícone, número, objeto), não o plano.
- Ritmo 2,5–3,2 p/s (o viral de 1,9M curtidas: 3,22 p/s).
- Ganchos: "Imagina se…" (cenário hipotético) · "Fulano quer X, mas existe um problema" · "Vocês pediram…
  notícia boa e ruim". Fim: "Marca aquele amigo que…" ou "próximo vídeo: X vs Y".
- Estrutura "problema → solução → novo problema → nova solução" (Além do Óbvio) prende sem precisar de virada.

### Ficha 05: molde "Você é…" (2 referências com o mesmo molde; 1 com 200 mil curtidas)
- Abrir em **2ª pessoa com o nome chocante/engraçado** ("Você é uma Maria-sem-vergonha…").
- Cada fato → **"Esse é seu [objeto do dia a dia]."**, e o objeto **aparece na tela** (+ cartão amarelo curto).
- Fecho: **"Chamam de [nome] quem [sentido ruim]. Mas você [feitos]."** → repete a 1ª frase (loop).
- Ritmo: as referências falam a 2,4–2,6 p/s, mas **a usuária decidiu 3,2 p/s também neste molde**. Cortes a cada ~2 s.
- Credibilidade: nome científico e estudo em letra pequena; cartão de número ("6 kg por ano").

### Voz / TTS (medido no EP01 abelhas)
- Voz escolhida pela usuária: **Edge TTS `pt-BR-AntonioNeural`** (preferida às vozes do
  OmniVoice/VoiceStudio e às femininas do Edge).
- Antônio cru fala ~2,1 p/s porque faz **pausas de ~0,85s entre frases**. O que acerta o
  ritmo é cortar pausas, não acelerar a voz:
  - `rate +0%` + `silenceremove ... stop_duration=0.09:stop_silence=0.13` → **3,3 p/s** (padrão viral).
  - `rate +25%` → 4,2 p/s: rápido demais.
- Gerar **um áudio por beat** e fazer a **cena durar o tempo real da fala** (+0,08s de respiro):
  a legenda e o corte ficam sincronizados sem esticar a voz.
- Edge TTS nesta nuvem: precisa de `--proxy "$HTTPS_PROXY"` e `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt`.

### Formatos (pedido da usuária, 2026-11-10)
| Formato | Estilo | Referências |
|---|---|---|
| viral 3D (padrão) | 3D cartoon / low-poly, engraçado ou curioso | EP01 abelhas, viral01 formiga, ficha 04 (Além do Óbvio) |
| 2D explicativo (no máximo) | 2D plano com mascotes, fundo de cor por cena | ficha 04 (Traço Curioso) |
| mapa explicativo | mapa de satélite + ícones/heatmaps | ficha 04 (GeoGlobeTales) |

## Série "Cubo mágico: F2L" (regras pedidas pela usuária, têm prioridade nesta série)
- **Duração:** mínimo **exato 1:00** (pedido da usuária), máximo 1:30.
- **Ritmo da fala (ATUALIZADO pela usuária depois do ep. 1):** 2,5 p/s ficou "lento demais".
  Agora: **gancho/introdução no ritmo viral (~3,1–3,2 p/s)** e **explicação ~2,9 p/s**.
  Medido no ep. 1: intro `rate +24%`, pausas ≤0,10s, respiro 0,08s (0,2s após algoritmo) → 3,15 p/s;
  explicação `rate -4%`, pausas ≤0,20s, respiro 0,18s (0,38s após algoritmo) → 2,92 p/s; total 1:05,7.
  Configuração por beat em `producao/epNN_falas.json` (`rate`, `gap`, `resp`).
  Cuidado: com fala rápida, giros seguidos ("érre, u, érre linha") precisam durar ~0,33s, senão se atropelam.
- Ritmo antigo (2,4–2,6 p/s) foi descartado pela usuária. Continua valendo: sem pausas
  arrastadas; o respiro maior fica depois de cada algoritmo.
- **Algoritmo falado = algoritmo na tela:** sempre que a narração disser um movimento, o cubo
  em CSS executa o MESMO movimento no MESMO instante, e a notação aparece grande (ex.: `R'`).
  (Exceção à regra geral de "sem texto grande": aqui a notação É o conteúdo.)
- **Repetir o algoritmo 2 vezes:** uma explicando, outra só mostrando (em velocidade normal).
- **Visual principal = cubo 3D em CSS** (`anim/cubo.html`), não imagem gerada. Imagens de IA só
  para fundo/Hero/Chefão (reaproveitados nos 5 episódios) → quase zero crédito por episódio.
- **Medido no ep. 1 (Antônio):** `rate -12%` + pausas entre palavras limitadas a 0,28s + respiro
  de 0,22s entre beats e 0,5s depois de beat com algoritmo → **2,54 p/s, 1:16**. Com `rate 0%`
  ficava em 3,2 p/s (rápido demais pra série). O Antônio é rápido por natureza, então aqui o
  "speed 1,0–1,05" da regra vira `rate -12%`.
- **Sincronia por palavra:** o Edge TTS devolve o tempo de cada palavra (`boundary="WordBoundary"`);
  o giro começa no início da palavra do movimento ("érre", "éle", "xis"...). Ferramentas em
  `producao/` (`narrar.py`, `montar_tempo.py`, `epNN.html`, `render.js`, `mixar.py`).
- Destaque de adesivo no CSS 3D: só borda branca por dentro. Brilho externo (box-shadow de fora)
  e `backface-visibility:hidden` causam buracos pretos no cubo no Chromium.
- **Legenda mostra a notação, não a letra por extenso** (pedido da usuária após o ep. 1):
  a voz fala "érre linha", a legenda escreve **R'**; "u dois" → **U2**; "éfe dois éle" → **F2L**;
  "xis"/"ípsilon" → **x**/**y**. Feito em `producao/motor.js` (`gruposLegenda`). Karaokê continua:
  palavra falada em amarelo, notação em ciano.
- Peças "voando" (deslocamento visual `v.off`) explicam conceito sem algoritmo: o par sobe BEM acima
  do cubo (senão parece colado nele). Slots/cruz se mostram por BAIXO (a cruz fica na face D).
- Letras faladas por extenso na narração (TTS): "érre", "éle", "u", "éfe", "dê", "xis",
  "ípsilon", "linha" (para `'`), "dois" (para `2`).

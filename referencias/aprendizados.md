# Aprendizados (lidos pelo diretor e pelo produtor antes de cada vídeo)

Só entram aqui regras medidas em vídeos ou pedidas pela usuária. Quando uma regra de série
conflita com uma regra geral, vale a da série (está marcada).

## Regras gerais (todos os vídeos)

### Texto na tela (pedido da usuária, EP01 abelhas)
- **Nada de texto grande no topo repetindo a fala.** No vídeo das abelhas, a palavra-chave
  gigante em cima + legenda embaixo foi "muita informação"; ficou só a legenda.
- Elementos no meio da tela só quando ensinam algo que a fala sozinha não mostra
  (contador, quiz, notação do cubo).

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

### Categorias de vídeo (pedido da usuária)
| Pedido | Estilo | Referências | Status |
|---|---|---|---|
| "vídeo de economia" | tópico 2D de economia | 5 reels em `pendentes.md` | aguardando análise (download bloqueado) |
| "fatos gerais" | 3D cartoon, engraçado (ex.: EP01 abelhas) | — | 1 vídeo feito |
Nunca misturar as regras de "economia" com as de "fatos gerais".

## Série "Cubo mágico: F2L" (regras pedidas pela usuária, têm prioridade nesta série)
- **Duração:** cada vídeo entre 1:05 e 1:30 (alvo 1:15–1:25).
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
- Letras faladas por extenso na narração (TTS): "érre", "éle", "u", "éfe", "dê", "xis",
  "ípsilon", "linha" (para `'`), "dois" (para `2`).

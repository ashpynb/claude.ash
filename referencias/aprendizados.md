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
- **Ritmo da fala mais calmo que o padrão:** 2,4–2,6 palavras/s (o padrão das skills é 2,8–3,3).
  Motivo: a própria usuária está aprendendo junto. Continua sem pausas arrastadas: o ritmo
  mais calmo vem de frases curtas e de um respiro de ~0,25s depois de cada algoritmo, não de
  voz lenta. No produtor: `speed` 1,0–1,05 e `stop_duration` 0,25 no silenceremove.
- **Algoritmo falado = algoritmo na tela:** sempre que a narração disser um movimento, o cubo
  em CSS executa o MESMO movimento no MESMO instante, e a notação aparece grande (ex.: `R'`).
  (Exceção à regra geral de "sem texto grande": aqui a notação É o conteúdo.)
- **Repetir o algoritmo 2 vezes:** uma explicando, outra só mostrando (em velocidade normal).
- **Visual principal = cubo 3D em CSS** (`anim/cubo.html`), não imagem gerada. Imagens de IA só
  para fundo/Hero/Chefão (reaproveitados nos 5 episódios) → quase zero crédito por episódio.
- Letras faladas por extenso na narração (TTS): "érre", "éle", "u", "éfe", "dê", "xis",
  "ípsilon", "linha" (para `'`), "dois" (para `2`).

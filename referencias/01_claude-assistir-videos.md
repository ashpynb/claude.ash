# Ficha 01: "Como fazer o Claude assistir vídeos" (TikTok, @_bizutti)

Analisado em 2026-11-10 com `analisar-video-referencia` (download + folhas de contato + faster-whisper local).
Só técnica: não copiar fala, pessoa nem imagens.

## Métricas
| item | valor |
|---|---|
| duração | 72,9 s · 576×1024 · 30 fps |
| visualizações / curtidas | 1.370 / 56 (no download) |
| palavras / ritmo | 248 palavras · **3,4 p/s** |
| cortes | 10 · plano médio **~7,3 s** · **1 corte** nos 3 s iniciais (só o de 0,1 s) |
| pausas > 0,2 s | 23 |
| formato | pessoa falando pra câmera + gravações de tela do GitHub (B-roll de mão apontando) |

## Gancho (0–3,6 s)
"Sabe quando você cola um vídeo no Claude e ele diz que não consegue acessar?" → **dor do espectador**
em forma de pergunta, seguido de "Vem comigo!". Na tela: título grande fixo + logos de Claude, TikTok,
Instagram e YouTube.

## Estrutura
1. dor (0–4 s) → 2. crédito/autoridade de quem fez a ferramenta (4–15 s) → 3. como funciona, com tela do
repositório (15–54 s) → 4. como usar: "/watch + link" (49–58 s) → 5. benefício: "nunca mais destrinchar
palavra por palavra" (58–68 s) → 6. CTA: "comenta repo" + "me segue".

## O que dá pra reproduzir no nosso estilo
- Gancho de **dor do espectador em pergunta** ("Sabe quando…?") nos primeiros ~3,5 s.
- Fala corrida ~3,4 p/s (bate com o nosso ritmo viral).
- CTA de palavra-chave nos comentários ("comenta X") em vez de "segue".
- Título grande **só nos primeiros segundos** (no gancho), depois some. Não deixar fixo como na referência e plano longo de 7 s (no nosso
  3D cartoon os cortes são a cada 1,5–2,5 s).

## O que o vídeo ensina (método)
Skill `/watch` do repositório `bradautomates/claude-video`: cola o link → `yt-dlp` tenta a legenda
primeiro → se não houver, transcreve com Whisper (ele usa o pago; aqui usamos faster-whisper local,
grátis) → extrai quadros pra o Claude "ver". É o mesmo caminho que a `analisar-video-referencia` já faz.

## Transcrição (faster-whisper small, pt)
```
[  0.0-  3.6] Sabe quando você cola um vídeo no cloud e ele diz que não consegue acessar?
[  3.6-  4.6] Vem comigo!
[  4.6-  8.4] Lembrando que é de graça e os cretos vão para Bradley Banana, um engenheiro de software
[  8.4- 13.0] que passou 5 anos da sua vida trabalhando em algumas das maiores empresas e ele se comprometeu
[ 13.0- 15.6] a transformar o cloud em uma super ferramenta.
[ 15.6- 20.6] O repositor, esse daqui, cloud vídeo do Brad Automates, ele basicamente vai ler as
[ 20.6- 25.3] legendas dos vídeos, então sempre no YouTube vai funcionar, porque todos os vídeos
[ 25.3- 29.1] tem legenda, o YouTube já disponibiliza uma ferramenta externa também, para
[ 29.1- 33.7] captar as legendas, comenta a repou que a gente vai te mandar o link do repositor.
[ 33.7- 38.9] E os vídeos se tiveram em legenda do Instagram e do TikTok, e para vídeos que não tem legenda
[ 38.9- 45.2] você vai conectar no Whisper, aí você vai pagar alguns centavos né, pouca coisa, não
[ 45.2- 49.4] vai dar nenhum real por vídeo, vai ter a tradução do vídeo e aí você pode criar
[ 49.4- 53.6] novos roteiros em cima disso, e para usar você só precisa dar o barra watch e o
[ 53.6- 54.6] link do vídeo.
[ 54.6- 58.5] Seja TikTok, YouTube ou Reels, o cloud vai conseguir achar o vídeo para você.
[ 58.5- 61.9] Então agora quando sou com a gente bomba aquele vídeo, você nunca mais vai precisar ficar
[ 61.9- 66.4] destrinxando palavra por palavra para colocar na inteligência artificial e tentar criar
[ 66.4- 68.8] algo semelhante ou entender por que bombou.
[ 68.8- 72.8] Agora você só vai dar o barra watch no cloud e não esquece de me seguir.
```

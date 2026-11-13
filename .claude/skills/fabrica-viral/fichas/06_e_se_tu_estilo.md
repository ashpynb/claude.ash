# Ficha 06: o estilo "E se tu…" + ferramentas (TikTok, 2026-11-10)

A usuária: **"quero vídeos assim, com essa qualidade de desenho, de estilo de pessoa"** (vídeos 4–7) e
"veja, aprenda e use" (vídeos 1–3, ferramentas). Medidos com ffmpeg + faster-whisper local.

## Vídeos de estilo (o alvo)
| # | perfil | tema | views / curtidas | duração | cortes | ritmo |
|---|---|---|---|---|---|---|
| 4 | @mano_wolf | E se um ar-condicionado caísse na tua cabeça? | 512 mil / 69 mil | 86,8 s | 36 | 2,64 p/s |
| 5 | @jackdl01 | Apocalipse nuclear, ep. 1 | **1,7 mi** / 133 mil | 84,8 s | 21 | 2,71 p/s |
| 6 | @toonscartoons00 | E se tu acordasse nível 1 no jogo que zerou 400× | 173 mil / 17 mil | 108,6 s | 43 | 2,70 p/s |
| 7 | @histoutromundo | E se tu acordasse num mundo medieval com um poder | **1,5 mi** / 245 mil | 122,3 s | 44 | 3,24 p/s |

Quadros: `referencias/img/ficha06_ref4.jpg` … `ref7.jpg`.

### Visual (o que dá a "qualidade de desenho")
- **Personagem 2D "cabeça de feijão"**: cabeça redonda grande, olhos de ponto, sobrancelha simples, boca
  pequena, corpo de formas simples e cores chapadas com leve sombreado; **sempre o mesmo rig** (não muda).
- **Cenários com luz de cena**: entardecer roxo/laranja, luz que vem de janela/lâmpada/vela/poste,
  meio-tons escuros, desfoque de fundo (bokeh), poeira/partículas no feixe, profundidade.
- **Mistura 2D + 2,5D**: personagem 2D em cenário com perspectiva (prédios, ruas de pedra, bunker).
- **Planos variados**: aberto (cidade), médio, close no rosto, inserto de objeto (capacete, suporte quebrando),
  vista de cima, contra-plongée.
- **"HUD" de números** (o que mais se repete): 30 km/h, 17 t, 393×, 00:23:02, 0,15 s, NÍVEL 2, 10 %, 9 s,
  "DIA 1 · 19:00", contador de átomos. Números grandes, limpos, com rótulo pequeno.
- Legenda 2–3 palavras MAIÚSCULAS, branco + **palavra-chave amarela** (confirma a regra: 8 de 8 referências).
- Selo pequeno de série no canto ("IN · T1 · EP1") nos que são série.

### Roteiro (o molde "E se tu…")
1. **Pergunta hipotética em 2ª pessoa** no gancho: "E se tu estivesse andando por São Paulo e, do nada, um
   ar-condicionado caísse na tua cabeça?" / "Se uma bomba nuclear caísse hoje, você teria só 15 minutos."
2. **Personagem com nome** logo depois ("O Vitor só estava passando na calçada." / "Esse é o Jack. E esse é o Tufão.").
3. **Escalada com número concreto a cada frase** (35 km/h → 65 → 80 → 17 toneladas), que vira HUD na tela.
4. Pergunta do espectador dita em voz alta ("Tá, mas e o peso?") e respondida.
5. **Virada** e **cliffhanger**: "Parte 2", "E lá em cima, alguém bate na porta.", "Segue aí pra ver".
6. Ritmo 2,6–3,2 p/s; corte a cada ~2–2,5 s.

## Ferramentas citadas (vídeos 1–3) — avaliar antes de instalar
- **Anatomy** (`npx skills add wheresryan22/anatomy`): animações isométricas, explicações visuais, bento grids.
- **HyperFrames**: cenas em HTML → vídeo. **onetake**: movimento contínuo sem cortes (grátis só não comercial).
- **Collage B-roll** (recorte de papel; usa IA do Google), **Claude Animation Base** (aparência de pintura,
  mascote), **Lemo-Opuscar** (43 estilos de filme por código, sem modelo de vídeo).
- Lista de 14 open source: Remotion (+ Remotion skills), Blender (+ Blender MCP), faster-whisper, **Chatterbox**
  (voz neural local), GSAP, Chrome DevTools MCP, ffmpeg, Impeccable (revisão de design), three.js, ComfyUI,
  yt-dlp, HyperFrames.
- Já usamos: ffmpeg, three.js, faster-whisper, yt-dlp. **O mais alinhado ao estilo-alvo é o
  `what-if-animation` (ficha 03): rig 2D em SVG + Remotion, feito exatamente pra esse gênero.**

## Transcrições
### vídeo 1
```
[  0.0] Uns dias atrás eu encontrei essa skill chamada Anatomy, e muita gente está dizendo que ela
[  3.7] pode ser a melhor skill já criada.
[  5.3] Ela cria animações isométricas de literalmente tudo que você quiser.
[  8.8] Dá pra criar explicações visuais, wireframes isométricos, bento grids ou até fazer engenharia
[ 13.8] reversa visual de qualquer coisa.
[ 15.6] O pessoal já está construindo coisas incríveis com ela e fica muito mais fácil construir
[ 19.4] coisas parecidas usando essa skill.
[ 22.2] Primeiro é só instalar essa skill gratuita no Cloud Code, Codex, OpenCode e Antigravity.
[ 27.0] Hoje instalar você dá pra ela uma referência dos exemplos que já vêm prontos e pede pra ela
[ 30.9] construir o que você quiser.
[ 32.4] É simples assim.```
### vídeo 2
```
[  0.0] Montar um estúdio de vídeo com um programa pago passa de 9 mil reais por ano.
[  4.8] SSTera leva 14 projetos open source que fazem o mesmo trabalho.
[  9.3] Remotions skills, para o agente programar vídeo.
[ 12.6] Blender, modelagem 3D.
[ 14.8] Faster Whisper, transcrição palavra por palavra.
[ 18.4] Chatterbox, voz neural no seu computador.
[ 21.5] GSAPK, animação na web.
[ 24.2] MCP for Blender, o cloud controlando Blender.
[ 27.5] Chrome DevTools MCP,
[ 29.6] o agente vendo navegador.
[ 31.5] FFMPG, corte conversão.
[ 34.3] Remotion, video in react.
[ 36.5] Impecable, revisão de design.
[ 38.8] 3JS, 3D no navegador.
[ 41.4] ConfioI, imagem e vídeo generativos.
[ 44.6] YT DLP, download de referências.
[ 48.2] E Hyperframes, animação em HTML.
[ 51.3] Na loja paga, essa conta chega a 9.480 reais por ano.
[ 56.1] Com o código aberto, a mesma esteira sai por zero.
[ 59.5] O link e o comando de instalação de cada um estão num guia.
[ 62.7] Copia o link deste vídeo e cola no site da view.```
### vídeo 3
```
[  0.0] Cinco ferramentas para você criar vídeos com o cloud, cada um com um estilo diferente.
[  5.0] A primeira é o Hyper Frames, da Ray Jane.
[  7.5] Você cria as cenas em HTML e transforma esse código em um vídeo com textos, imagens e animações.
[ 14.4] A segunda é o One Take.
[ 16.0] A proposta é um movimento contínuo.
[ 18.0] Uma cena se transforma na próxima, sem cortes, e tem versão gratuita para você utilizar.
[ 23.3] A terceira é o Collage B-Roll.
[ 25.3] São recortes de papel, imagens, que entram na tela e se montam.
[ 29.2] Peça por peça.
[ 30.2] A animação usa a inteligência artificial do Google.
[ 33.2] A quarta é o Cloud Animation Base.
[ 36.2] Ela cria desenhos com aparências de pintura à mão, incluindo o mascote do Cloud Code, com diferentes expressões e movimentos.
[ 43.2] E a quinta é o Lemo Opuskar.
[ 45.2] O projeto reúne 43 estilos de filmes, criado por código, sem usar um modelo de geração de vídeo.
[ 52.2] Os cinco já estão no GitHub.
[ 54.2] Escolha o estilo que combina com a sua ideia e adapte para o seu conteúdo.
[ 58.2] E se você quer receber conteúdo como esse, clica aqui e já me segue.```
### vídeo 4
```
[  0.0] E se tu estivesse andando pelas ruas de São Paulo e, do nada, um ar condicionado caísse
[  5.1] na tua cabeça?
[  6.1] O Victor só estava passando na calçada.
[  8.8] Dez andares acima, dois caras faziam a manutenção da máquina.
[ 12.9] Daí, o suporte soltou da parede, 35 quilos no ar.
[ 17.7] No primeiro segundo, ela já está a 35 por hora.
[ 20.8] No segundo seguinte, 65.
[ 23.5] Isso é a gravidade somando velocidade o caminho inteiro.
[ 27.0] O ar freia um pouco, mas não salva ninguém.
[ 29.8] Dois segundos e meio depois, ela chega lá embaixo a uns 80 por hora.
[ 34.1] Tá, mas e o peso?
[ 36.1] Parada?
[ 37.1] A máquina pesa 35 quilos, só que ela não estava parada.
[ 40.8] Pra zerar 80 por hora em uns 5 centímetros, o impacto chega a umas 17 toneladas na cabeça
[ 47.6] do Victor.
[ 48.6] Tá, mas e se ele tivesse de capacete?
[ 51.6] Capacete de obra é testado com 5 quilos caindo de 1 metro.
[ 55.4] Essa máquina chega com mais 170 vezes mais energia.
[ 59.6] Daí fudeu.
[ 60.6] Muita gente acha que isso seria o fim, mas não pro Victor.
[ 64.7] Ele renasceu num mundo totalmente diferente, ainda na época medieval.
[ 69.1] Lá, todo mundo nasce com uma marca nas costas da mão.
[ 72.6] É ela que diz pra qual magia tu tem aptidão.
[ 75.6] Terra, fogo, ar ou água.
[ 78.2] Só que o Victor nasceu com uma marca diferente.
[ 81.2] Uma marca que, pra eles, era maldiçoada.
[ 85.0] Parte 2```
### vídeo 5
```
[  0.0] Se uma bomba nuclear caísse hoje, você teria só 15 minutos pra se salvar.
[  5.4] Esse é o Jack.
[  6.4] E esse é o Tufão.
[  8.1] Terça, sete da noite.
[ 10.0] O Jack janta no sofá e o Tufão espera cair alguma coisa.
[ 14.0] Aí, a TV sai do ar.
[ 15.9] Tela vermelha.
[ 17.0] Um apito que não para.
[ 18.8] Alerta nacional.
[ 20.1] Mício detectado.
[ 21.4] Procure abrigo agora.
[ 23.3] Ao mesmo tempo, todos os celulares da rua tocam.
[ 26.3] Os vizinhos saem pra calçada, olhando pro céu.
[ 29.2] O primeiro instinto do Jack é pegar o carro e fugir da cidade.
[ 32.9] Não faça isso.
[ 34.3] Em cinco minutos, todas as ruas estão travadas.
[ 37.4] E ninguém sai do lugar.
[ 39.0] Primeiro, a mochila.
[ 40.4] Água, lanterna, rádio.
[ 42.5] Ela está pronta atrás da porta faz dois anos.
[ 45.2] Depois, o Tufão.
[ 46.7] A guia no pescoço e nada de soltar.
[ 49.3] E por último, o quintal.
[ 51.0] Embaixo da casinha do Tufão tem uma tampa de ferro.
[ 53.9] O bunker que o Jack cavou sozinho e que todo mundo chamava de loucura.
[ 58.2] Dez degraus pra baixo.
[ 59.8] A porta pesada se fecha e a roda trava.
[ 62.8] Aí, o céu fica branco.
[ 64.7] Primeiro vem a luz.
[ 66.1] Depois, o silêncio.
[ 67.9] E então, a onda.
[ 69.6] A terra trem.
[ 70.8] A lâmpada do bunker balança e apaga.
[ 74.2] No escuro, o Tufão encosta no Jack.
[ 76.6] E lá em cima, alguém bate na porta.```
### vídeo 6
```
[  0.0] E se tu acordasse nível 1 no jogo que já zerou 400 vezes?
[  4.7] O Beto acordou e correu direto para a parede.
[  7.8] No jogo, ali tem um bug que pula 3 horas de história.
[ 11.5] Batendo de cara.
[ 12.9] Aqui, parede é parede.
[ 15.2] A melhor espada do jogo tava atrás da cachoeira, ali do lado.
[ 19.0] 2 metros de aço.
[ 20.8] No menu, quase não pesava.
[ 22.8] Não saiu do chão.
[ 24.4] Aço pesa quase 8 vezes mais que água.
[ 27.4] Aquilo dava 140kg, duas geladeiras num cabo.
[ 31.8] O Beto saiu com a faca de pão do tutorial.
[ 34.5] Primeiro inimigo, um rato, o mais fraco do jogo.
[ 38.0] O Beto deu o primeiro golpe e errou.
[ 40.4] Aqui, a mira não é automática.
[ 42.8] Aí bateu sem parar, como sempre fez.
[ 45.7] 10 segundos depois, o braço não levantava.
[ 48.8] Teu corpo guarda força máxima por poucos segundos.
[ 52.0] Para encher de novo, leva minutos.
[ 54.3] Que nem celular velho.
[ 55.6] Cai rápido e demora na tomada.
[ 58.0] O rato não esperou, mordeu a canela.
[ 60.8] A vida caiu para menos da metade.
[ 63.2] O Beto conhecia esse rato de cor.
[ 65.3] Pulinho, pulinho, pulão.
[ 67.1] Sempre na perna esquerda.
[ 68.8] Gente leva um quarto de segundo para reagir.
[ 71.4] A mordida é mais rápida.
[ 73.2] Então ele parou de reagir e passou a adivinhar.
[ 76.4] Na primeira, errou o tempo e levou outra mordida.
[ 79.5] Na segunda, tirou a perna antes.
[ 81.8] O rato passou reto.
[ 83.3] Faka, nível 2.
[ 85.5] Para curar, bebeu 6 poções de uma vez, como no jogo.
[ 89.1] Aqui, poção é líquido e estômago tem limite.
[ 92.4] Vumitou tudo em cima do rato.
[ 94.5] Poção de cura.
[ 95.8] O rato levantou.
[ 97.0] Só que o rato nem olhou para o Beto.
[ 99.2] Fugia do portão do chefe final, que só abre no fim do jogo.
[103.0] Tava aberto, de dentro.
[105.1] Segue aí para ver o Beto descobrir quem abriu na parte 2.```
### vídeo 7
```
[  0.0] E se tu acordasse num mundo medieval com um poder apelão que ninguém entende?
[  4.3] O Caio era químico.
[  5.9] Três da manhã balançou a máquina de refrie do laboratório pra soltar uma lata.
[  9.9] 400 quilos em cima dele.
[ 12.2] Protagonista de anime morre de caminhão.
[ 14.5] Ele foi de máquina de refrie.
[ 16.2] E acordou bebê num mundo onde todo mundo nasce com uma magia.
[ 19.8] A primeira coisa que ele viu não foi a mãe.
[ 22.0] Foram letras.
[ 23.1] Em tudo.
[ 24.0] H e O na água.
[ 25.7] N e O no ar.
[ 27.2] Ele tava enxergando a tabela periódica.
[ 29.3] E quando ele pensava num elemento, o elemento se mexia.
[ 32.4] Com dois anos, ele tirou o sal da sopa que odiava.
[ 35.1] Sal na água fica desmontado em sódio e cloro, soltinhos.
[ 38.6] Ele só montou de volta.
[ 39.8] A mãe viu o montinho branco no prato e benzeu a casa inteira.
[ 43.1] Daí ele aprendeu a esconder.
[ 44.8] Com cinco, tentou fazer uma espada do ar.
[ 47.2] Nada, no ar não tem ferro.
[ 49.0] Ele não cria átomo, só reorganiza o que já tá ali.
[ 51.9] Mas a areia preta do rio tem ferro.
[ 54.2] Com oito, ele consertava as ferramentas do pai com ela.
[ 57.2] Aos dez, todo mundo descobre a sua magia.
[ 60.0] O cristal do Caio encheu de letras e a sala ficou quieta.
[ 64.1] Maldição do louco.
[ 65.6] Na história desse mundo, só três pessoas tiveram ela.
[ 68.7] As três enlouqueceram.
[ 70.4] Viam símbolo em tudo e não entendiam nada.
[ 72.9] Pro Caio era só quínica.
[ 74.5] Toda magia desse mundo é um pedacinho dela.
[ 77.2] A maldição do louco é ela inteira.
[ 79.4] E o filho do mais rico chamou ele pro duelo.
[ 81.7] Pra provar que era só um louco.
[ 83.4] A magia dele era o bafo do dragão.
[ 85.6] Pra eles, fogo saindo do nada.
[ 87.8] Pra gente, metano.
[ 89.1] O gás do pântano e do arroto da vaca.
[ 91.3] O ar quase não tem metano.
[ 93.0] Então, o goripo chava o gás de um prédio inteiro de ar.
[ 96.0] E o estalo dos dedos soltava um choquinho.
[ 98.3] Igual da maçaneta.
[ 99.5] Já basta pra acender.
[100.8] O goripo cercou o Caio de gás e juntou os dedos pra estalar.
[104.2] Um estalo e tudo em volta dele virava fogo.
[107.3] Só que fogo precisa de três coisas.
[109.5] Gás, faísca e oxigênio.
[111.7] O goripo tinha o gás e a faísca.
[113.6] Mas o oxigênio é uma letra da tabela.
[115.9] E a tabela inteira é do Caio.
[118.0] Quem é mais rápido?
[119.1] O estalo ou o Caio?
[120.7] Parte 2.```

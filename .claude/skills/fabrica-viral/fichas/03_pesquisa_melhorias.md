# Ficha 03: pesquisa pra melhorar os vídeos (2026-11-10)

Fontes: repositório `kelano86/what-if-animation` (MIT; regras **medidas quadro a quadro** do episódio mais
visto, 4,2M views, de um canal "What If"), dois tutoriais do YouTube **vistos pelo Gemini**
(`_fIoJ_ywGfY` "Ultra-Realistic 3D Shorts Using Claude"; `NFF-RyxnJDY` "2D animations for free"),
e as bibliotecas CC0 Quaternius e Kenney. Só técnica: personagens e histórias continuam nossos.

## 1. Ritmo e câmera (what-if-animation, medido)
- **~27 cortes/min na abertura**, plano mediano 2,7s (alvo 0,7–3s); nada parado > ~3s.
- **O corte vem da mudança de TAMANHO de plano**, não do movimento: aberto → inserto macro → médio → close →
  reação. Dois planos vizinhos nunca têm o mesmo tamanho e ângulo.
- Abertura ~2× mais rápida que o resto. Corte 2 quadros antes da palavra.
- Pelo menos 1 plano de cima (high/top-down) ou de baixo (low angle) por vídeo.

## 2. Luz (o que mais pesa no "profissional")
- Paleta de entardecer: céu roxo → laranja, sol baixo atrás do personagem.
- **Toda luz vem de algo visível** (janela, lâmpada, sol); poças de luz e cantos escuros; meio-tons escuros.
- **Luz de contorno quente (rim) no lado iluminado** de todo personagem.
- Neblina/poeira no feixe, fundo desfocado nos closes, primeiro plano escuro desfocado em ~1/3 dos planos.
- Granulação leve + vinheta. Render "limpo demais" parece falso (tutorial 1: glare, grão, motion blur).

## 3. Personagens e cenário
- Mais de perfil / 3/4 do que de frente. Animam pouco; a vida vem do entorno (poeira, luz balançando, push-in).
- Expressão troca num piscar, não "derrete".
- **Usar modelos prontos em vez de modelar à mão** (tutorial 1: evita o "AI slop"). → bibliotecas CC0 abaixo.
- Mundo cheio: planos abertos com 20+ objetos; tudo que fica em pé tem sombra de contato.

## 4. Texto na tela
- Quase nenhum: título só no gancho + pequenos números/rótulos. (Bate com a regra da usuária.)

## 5. Som (o que mais falta nos nossos)
- **Um efeito por ação visível**, ambiente por lugar, **trilha leve** na abertura que **corta na virada**.
- **O "hit" que ilustra uma palavra cai na pausa DEPOIS dela**, nunca em cima (senão cobre a palavra).
- Alinhar pelo ataque do som (onde ele começa a soar), não pelo início do arquivo.
- Silêncio como ferramenta: cortar a música um tempo antes do impacto.
- Masterizar em **-14 LUFS**, pico < -1 dBTP (já fazemos -14).

## 6. Checklist de 11 pontos antes de animar (storyboard)
1 leitura em 1s no tamanho do celular · 2 tamanhos de plano variam · 3 luz de uma fonte visível ·
4 personagem é o mais claro/nítido da área · 5 profundidade (primeiro plano desfocado) · 6 mundo cheio ·
7 perspectiva/escala corretas · 8 pose diz a fala sem voz · 9 continuidade · 10 só título/rótulos como texto ·
11 nada parecido com personagem famoso/marca.

## 7. Roteiro (what-if, 7 batidas — formato curto)
Abertura no meio da ação (3 demos rápidas) → premissa → diversão → **virada com 1 fato real com número**
("Isso é real.") → termina numa pergunta/ameaça, nunca numa resolução. Frases de 3–8 palavras, 2ª pessoa.

## 8. Modelos 3D grátis (CC0, uso comercial sem crédito) — testado
- **Quaternius** (1.545 .glb): animais animados (raposa, lobo, veado, cavalo...), natureza (150), interior de
  casa (123), comida/plantações, peixes, dinossauros, espaço, cidade, pessoas modulares.
  Via `git clone --filter=blob:none` de `github.com/trebeljahr/quaternius-showcase` (só baixa o que usar).
- **Kenney** (4.812 .glb): personagens fofos animados (andar, acenar, sentar, cair), comida (200), móveis,
  cidade, natureza (329), espaço, cemitério... Via `github.com/shorepine/kenney`.
- Funciona no nosso three.js com `GLTFLoader` (módulo, servido por `python3 -m http.server`).
  Prova: `referencias/img/teste_modelos_cc0.jpg` (raposa andando + personagem acenando, luz de entardecer,
  sombras, 4 tamanhos de plano). Faltou: insetos (formiga/abelha) não existem nesses pacotes.

## 9. O que NÃO vale pra nós
- Blender + Renderpeople + 52 blend shapes faciais (tutorial 1): pesado demais pra esta nuvem e pago.
- Skill "Faceless Shorts" de site de terceiros (tutorial 2): .zip fechado; o que ela faz já fazemos.

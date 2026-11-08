"""Gera roteiro/epNN.md e roteiro/epNN.json da série F2L.

Cada clipe = narração dividida em frases; cada frase vira um beat.
Tempo dos beats é proporcional ao nº de palavras (ritmo-alvo RITMO p/s).
Rodar: python3 roteiro/gerar.py
"""
import json, re, pathlib

RITMO = 2.9  # p/s médio (intro ~3,15, explicação ~2,9 — pedido da usuária após o ep. 1)
AQUI = pathlib.Path(__file__).parent

ESTILO = ("2D pixel art, 16-bit retro RPG, crisp pixel clusters, clean outlines, no blur, "
          "vertical 9:16, deep navy, dark purple, neon cyan and magenta palette, no text")
HERO = ("a small adventurer whose head is a tiny 3x3 colorful puzzle cube, cyan scarf, "
        "big expressive eyes, purple tunic")
CHEFAO = ("a giant floating scrambled 3x3 puzzle cube monster with mixed colored tiles, "
          "glowing magenta eyes between the tiles, chains around it")

IMAGENS = {
    "bg_arena": f"Empty pixel-art arena floor seen from the front, glowing cyan grid on the ground, "
                f"dark purple sky with stars, large empty space in the center for a 3D object, {ESTILO}",
    "hero": f"{HERO}, full body, idle pose, plain flat magenta-free green background for chroma key, {ESTILO}",
    "chefao": f"{CHEFAO}, menacing pose, plain flat green background for chroma key, {ESTILO}",
    "bg_mapa": f"Top-down pixel-art world map with five glowing level nodes connected by a dotted path, "
               f"each node a small cube-shaped tower, {ESTILO}",
}

# ---------------------------------------------------------------------------
# Cada beat: (visual, movimento, texto_tela, sfx[, video_ia])
# "CUBO: seq" = o cubo CSS executa a sequência sincronizada com a fala.
# ---------------------------------------------------------------------------
EPS = [
 {
  "n": 1, "titulo": "A língua do cubo (notação)",
  "objetivo": "Ler U, R, L, F, D, a linha ('), o dois (2) e as rotações x e y.",
  "clipes": [
   {"narracao": "Todo tutorial de cubo fala érre, u, érre linha. Parece código secreto né? "
                "Hoje você aprende essa língua. É só uma letra pra cada face.",
    "beats": [
     ("Chefão (cubo embaralhado) surge gigante; letras R U R' orbitam ele", "zoom-out rápido + tremida", "R U R'", "whoosh grave", True),
     ("Hero coça a cabeça, interrogação pixel pisca", "personagem entra pela esquerda + bob", "???", "blip confuso"),
     ("Cubo CSS limpo aparece no centro da arena girando devagar", "punch-in 100→115%", "LÍNGUA DO CUBO", "power-up"),
     ("Seis faces acendem uma a uma com a letra em cima", "texto cinético em cada face", "1 LETRA = 1 FACE", "6 bipes ascendentes"),
    ]},
   {"narracao": "Segura o cubo olhando pra frente. A face de cima é o u. "
                "A da direita é o érre. A da esquerda é o éle. A frente é o éfe e embaixo é o dê.",
    "beats": [
     ("Cubo CSS de frente, câmera em leve deriva", "parallax fundo × cubo", "FRENTE", "tique"),
     ("Face de cima pisca ciano; selo 'U = up'", "pop da letra U", "U", "bipe"),
     ("Face direita pisca; selo 'R = right'", "whip-pan curto pra direita", "R", "bipe"),
     ("Face esquerda pisca; selo 'L = left'", "whip-pan pra esquerda", "L", "bipe"),
     ("Frente e baixo piscam juntas (cubo inclina pra mostrar D)", "cubo tomba 25° + volta", "F · D", "bipe duplo"),
    ]},
   {"narracao": "Agora a regra de ouro. Letra sozinha gira no sentido do relógio olhando pra aquela face. "
                "Por isso o érre sobe a coluna da direita. E o éle desce a coluna da esquerda.",
    "beats": [
     ("Moldura dourada 'REGRA DE OURO' cai na tela", "queda + tremida de impacto", "REGRA DE OURO", "gongo 8-bit"),
     ("Relógio pixel aparece colado na face direita, ponteiro girando", "rotação do relógio", "SENTIDO HORÁRIO", "tique-taque"),
     ("CUBO: R — coluna da direita sobe, seta ciano pra cima", "câmera fixa, só o cubo move", "R ↑", "click de giro"),
     ("Corte seco: cubo volta resolvido. CUBO: L no 'éle' — coluna da esquerda desce, seta magenta", "punch-in na coluna", "L ↓", "click de giro"),
    ]},
   {"narracao": "Viu um tracinho do lado? Lê linha. Érre linha gira ao contrário e a coluna desce. "
                "Se tiver um dois, é meia volta. U dois.",
    "beats": [
     ("Close no apóstrofo de R' crescendo na tela", "punch-in + glitch", "R' = linha", "glitch"),
     ("CUBO: R' — coluna da direita desce", "câmera acompanha a coluna", "AO CONTRÁRIO", "click reverso"),
     ("Número 2 cai e quica ao lado da letra U", "quique squash & stretch", "2 = MEIA VOLTA", "boing"),
     ("CUBO: U2 — topo dá meia volta", "pico: flash branco 2 quadros no fim", "U2", "click duplo"),
    ]},
   {"narracao": "Por último o xis e o ípsilon. Eles giram o cubo inteiro na sua mão. "
                "Xis vira tudo igual o érre. Ípsilon vira tudo igual o u. Nada se desfaz.",
    "beats": [
     ("Duas mãos pixel aparecem segurando o cubo", "mãos entram de baixo", "x · y", "whoosh"),
     ("Cubo balança de leve nas mãos (sem girar camada nenhuma)", "bob suave + mãos apertam", "", "whoosh"),
     ("CUBO: x no 'xis' — cubo inteiro tomba pra trás (frente sobe)", "giro completo + rastro ciano", "x", "whoosh longo"),
     ("Corte seco: cubo volta à vista normal. CUBO: y no 'ípsilon' — cubo inteiro gira pra esquerda; selo verde 'nada se desfaz'", "giro completo + carimbo", "y", "whoosh longo + carimbo"),
    ]},
   {"narracao": "Resumo. Letra gira a face, linha é ao contrário, dois é meia volta, xis e ípsilon viram o cubo. "
                "Teste: em érre, a coluna da direita sobe ou desce? No próximo vídeo, por que o éfe dois éle resolve duas camadas de uma vez.",
    "beats": [
     ("Painel HUD com 4 linhas de resumo entrando uma a uma", "texto cinético em cascata", "RESUMO", "4 bipes"),
     ("Quiz: cubo parado com setas ↑ e ↓ piscando alternadas", "pulse das setas", "SOBE OU DESCE?", "tique de quiz"),
     ("Mapa de fases: nó 1 acende, câmera voa até o nó 2 com o Chefão na sombra", "zoom-through no mapa", "PRÓXIMO: F2L", "fanfarra curta"),
    ]},
  ],
  "kit": {
   "resumo": ["Cada letra (U R L F D B) gira uma face no sentido horário, olhando de frente pra ela.",
              "Linha (') = ao contrário; 2 = meia volta (180°).",
              "x e y giram o cubo inteiro (x como R, y como U): muda a vista, não desfaz nada."],
   "quiz": [("Em R, a coluna da direita (vista de frente) sobe ou desce?", "Sobe."),
            ("O que significa L'?", "Girar a face esquerda no sentido anti-horário: a coluna da esquerda sobe."),
            ("Depois de um y, a cor da frente muda?", "Muda: a face da direita vem pra frente, mas nenhuma peça sai do lugar relativo.")],
   "flashcards": [("U", "face de cima, horário visto de cima (frente vai pra esquerda)"),
                  ("R / R'", "direita sobe / direita desce"), ("L / L'", "esquerda desce / esquerda sobe"),
                  ("U2", "meia volta no topo"), ("x / y", "cubo inteiro como R / como U")],
   "metafora": "A 'língua do cubo' é só convenção de escrita; o Chefão é o cubo embaralhado, mas a notação não 'derrota' nada, só permite ler os algoritmos.",
   "conferir": ["Alguns tutoriais usam letras minúsculas (r, u) para giros de duas camadas; aqui não usamos."],
  },
 },
 {
  "n": 2, "titulo": "Camadas × F2L: o que muda",
  "objetivo": "Entender que o F2L junta quina + aresta em pares e resolve as duas primeiras camadas em 4 etapas.",
  "clipes": [
   {"narracao": "No método de iniciante as duas primeiras camadas levam oito etapas. "
                "O éfe dois éle faz em quatro. E não é mágica. É só uma ideia diferente: trabalhar em pares.",
    "beats": [
     ("Contador '8' gigante em vermelho com 8 peças voando", "zoom-out + partículas", "8 ETAPAS", "alarme 8-bit", True),
     ("O 8 é cortado por uma espada do Hero e vira '4' ciano", "golpe + flash + tremida (pico)", "4 ETAPAS", "espadada"),
     ("Hero dá de ombros, faíscas de 'mágica' apagam", "personagem bob", "NÃO É MÁGICA", "puf"),
     ("Lâmpada pixel acende acima do cubo CSS", "pop + brilho", "IDEIA NOVA", "ding"),
    ]},
   {"narracao": "Éfe dois éle vem do inglês, first two layers. As duas primeiras camadas. "
                "Você começa igual, com a cruz branca embaixo. A diferença vem depois da cruz.",
    "beats": [
     ("Letras F-2-L se expandem em 'First 2 Layers'", "texto cinético expande", "FIRST 2 LAYERS", "whoosh"),
     ("CUBO (modo foco): duas camadas de baixo acendem, topo fica cinza", "punch-in no cubo", "2 CAMADAS", "bipe"),
     ("CUBO: x2 pra mostrar a face de baixo com a cruz branca", "giro completo", "CRUZ BRANCA", "click"),
    ]},
   {"narracao": "No método de camadas você coloca uma quina branca, depois outra, depois as arestas do meio. "
                "São oito peças viajando sozinhas. E cada viagem desmonta e remonta um pedaço do cubo.",
    "beats": [
     ("CUBO: quina branca destacada sobe e desce sozinha pro slot", "câmera acompanha a peça", "1 QUINA", "click"),
     ("Contador de peças 1→4 enquanto quinas piscam nos cantos", "número subindo", "4 QUINAS", "bipes"),
     ("Arestas do meio piscam uma a uma, contador 5→8", "número subindo + tremida no 8", "+ 4 ARESTAS", "bipes"),
     ("8 sprites de peça andando em fila indiana cansados", "pan lateral", "8 VIAGENS", "passos"),
    ]},
   {"narracao": "No éfe dois éle você junta a quina com a aresta que fica em cima dela. "
                "Vira um par, um bloquinho de duas peças. E coloca o par inteiro de uma vez no espaço dele, o slot.",
    "beats": [
     ("CUBO (modo foco): só uma quina e uma aresta coloridas, resto cinza", "punch-in", "QUINA + ARESTA", "bipe"),
     ("As duas peças se aproximam e encaixam com faísca", "pico: ímã + flash", "= PAR", "clack metálico"),
     ("CUBO: R U R' — o par desce junto pro canto", "câmera fixa, cubo move", "PAR ENTRA", "click ×3"),
     ("Buraco do canto contornado em neon, legenda SLOT", "contorno desenhando", "SLOT", "ding"),
    ]},
   {"narracao": "A cruz deixa quatro buracos nos cantos. São os quatro slots. "
                "Quatro pares, quatro slots, duas camadas prontas. Menos movimentos e menos pausa pra pensar.",
    "beats": [
     ("CUBO visto de baixo: 4 cantos vazios piscam", "giro lento + pulso", "4 SLOTS", "4 bipes"),
     ("4 pares entram um por um (corte rápido entre slots)", "whip-pan entre cantos", "4 PARES", "click ×4"),
     ("Barra de HP do Chefão cai pela metade", "HP caindo + tremida", "-50% HP", "dano"),
    ]},
   {"narracao": "Resumo: mesma cruz, mas em vez de oito peças soltas são quatro pares. "
                "Pergunta: quantas peças formam um par? Pausa e pensa. No próximo vídeo, os primeiros casos com três movimentos.",
    "beats": [
     ("Comparação lado a lado: 8 peças soltas × 4 pares", "split-screen deslizando", "8 → 4", "whoosh"),
     ("Quiz: '? peças = 1 par' piscando", "pulse", "QUANTAS?", "tique de quiz"),
     ("Mapa: nó 2 acende, câmera voa ao nó 3", "zoom-through", "PRÓXIMO: 1º CASO", "fanfarra"),
    ]},
  ],
  "kit": {
   "resumo": ["F2L = First Two Layers: as duas primeiras camadas.",
              "Começa igual ao iniciante: cruz branca embaixo.",
              "Em vez de 4 quinas + 4 arestas separadas, monta 4 pares (quina + aresta) e insere cada par no seu slot."],
   "quiz": [("O que significa F2L?", "First Two Layers, as duas primeiras camadas."),
            ("Quantas peças formam um par?", "Duas: uma quina e uma aresta."),
            ("Quantos slots existem depois da cruz?", "Quatro, um em cada canto de baixo.")],
   "flashcards": [("F2L", "resolve as 2 primeiras camadas por pares"), ("Par", "quina + aresta do mesmo slot"),
                  ("Slot", "espaço de um par: canto de baixo + aresta do meio acima dele"),
                  ("Cruz", "4 arestas brancas embaixo, feita antes do F2L")],
   "metafora": "'8 etapas × 4 etapas' simplifica: cada par do F2L também pode exigir vários movimentos. O ganho real é inserir 2 peças juntas, gastando menos movimentos no total.",
   "conferir": ["Contagem 'oito etapas' supõe o método de camadas clássico (4 quinas + 4 arestas do meio)."],
  },
 },
 {
  "n": 3, "titulo": "Seus 2 primeiros casos",
  "objetivo": "Resolver os casos básicos: R U R', U R U' R' e o espelho F' U' F.",
  "clipes": [
   {"narracao": "Três movimentos. É isso que você precisa pro caso mais fácil do éfe dois éle. "
                "E você já conhece os três.",
    "beats": [
     ("Três cartas de jogo viram: R, U, R'", "cartas giram 3D + flash", "3 MOVIMENTOS", "carta ×3", True),
     ("Chefão rosna, Hero levanta as três cartas", "personagem entra + tremida", "CASO FÁCIL", "rugido curto"),
     ("Check verde em cima de cada carta", "pop sequencial", "JÁ CONHECE", "ding ×3"),
    ]},
   {"narracao": "Prepara assim. Cruz branca embaixo. | O slot que você vai resolver fica na frente, à direita. | "
                "Se não estiver, gira o cubo com ípsilon até ele chegar ali. | O slot de trabalho é sempre esse.",
    "beats": [
     ("CUBO de frente, cruz embaixo visível pela inclinação", "deriva lenta", "CRUZ EMBAIXO", "tique"),
     ("Slot frente-direita contornado em neon", "punch-in no canto", "FRENTE-DIREITA", "bipe"),
     ("CUBO: y — cubo inteiro gira trazendo outro slot pra frente-direita", "giro completo", "USE y", "whoosh"),
     ("Seta circular ao redor do cubo", "rotação da seta", "ATÉ CHEGAR", "click"),
    ]},
   {"narracao": "Caso um. A quina está em cima do slot com o branco olhando pra direita. | A aresta está lá atrás. | "
                "Faz érre, u, érre linha. | Elas se encontram e descem juntas. Mais uma vez: érre, u, érre linha.",
    "beats": [
     ("CUBO (modo foco, setup do caso 1): branco da quina na face direita brilhando", "punch-in na quina", "BRANCO → DIREITA", "bipe"),
     ("Aresta no topo-trás pisca (câmera inclina pra mostrar)", "pan pra trás", "ARESTA ATRÁS", "bipe"),
     ("CUBO: R U R' em velocidade de aula, letra grande a cada giro", "câmera fixa", "R  U  R'", "click ×3"),
     ("Par encaixado no slot brilha; HP do Chefão cai", "pico: flash + tremida", "ENCAIXOU!", "clack + dano"),
    ]},
   {"narracao": "Caso dois. O par já está pronto no topo, em cima do slot, | com o branco olhando pra frente. | "
                "Faz u, érre, u linha, érre linha.",
    "beats": [
     ("CUBO (setup do caso 2): par pronto em cima do slot, contorno ao redor do par", "punch-in", "PAR PRONTO", "bipe"),
     ("Branco da quina na frente pisca", "pulse", "BRANCO → FRENTE", "bipe"),
     ("CUBO: U R U' R' devagar, letra grande a cada giro", "câmera fixa", "U R U' R'", "click ×4"),
    ]},
   {"narracao": "Viu? O u tira o par do caminho e o érre abre o slot. Agora o espelho do caso um. "
                "Branco olhando pra frente e aresta na esquerda. Faz éfe linha, u linha, éfe.",
    "beats": [
     ("Replay rápido do caso 2 com setas mostrando o U 'abrindo espaço'", "replay 2x + setas", "ABRE ESPAÇO", "rewind"),
     ("Espelho pixel divide a tela ao meio", "wipe espelhado", "ESPELHO", "shimmer"),
     ("CUBO (setup espelho): branco na frente, aresta topo-esquerda", "punch-in", "ARESTA ESQUERDA", "bipe"),
     ("CUBO: F' U' F", "câmera fixa", "F' U' F", "click ×3"),
    ]},
   {"narracao": "Resumo. Branco pra direita é érre u érre linha. Par pronto é u érre u linha érre linha. "
                "Pergunta: e se o branco estiver olhando pra cima? Isso é o próximo vídeo.",
    "beats": [
     ("Duas cartas de golpe lado a lado com os algoritmos", "cartas deslizam", "R U R'  ·  U R U' R'", "carta ×2"),
     ("CUBO: quina com branco pra cima, ponto de interrogação", "pulse + glitch", "BRANCO EM CIMA?", "glitch"),
     ("Mapa: nó 3 acende, voo ao nó 4", "zoom-through", "PRÓXIMO: CASOS CHATOS", "fanfarra"),
    ]},
  ],
  "kit": {
   "resumo": ["Sempre trabalhe o slot da frente-direita; use y para trazer o slot certo.",
              "Quina com branco pra direita + aresta atrás no topo: R U R'.",
              "Par pronto em cima do slot, branco pra frente: U R U' R'. Espelho do caso 1 (branco pra frente, aresta à esquerda): F' U' F."],
   "quiz": [("Qual algoritmo para quina com branco pra direita e aresta atrás?", "R U R'."),
            ("O que o U faz no U R U' R'?", "Tira o par de cima do slot pra o R poder subir o slot sem desmontar o par."),
            ("Qual o espelho de R U R'?", "F' U' F.")],
   "flashcards": [("R U R'", "quina UFR branco→direita, aresta em UB"),
                  ("U R U' R'", "par pronto em UFR+UR, branco→frente"),
                  ("F' U' F", "quina UFR branco→frente, aresta em UL"), ("Slot de trabalho", "frente-direita")],
   "metafora": "As 'cartas de golpe' sugerem decorar; o ideal é entender por que cada movimento funciona (o U tira o par do caminho, o R abre e fecha o slot).",
   "conferir": ["Os algoritmos foram verificados para o slot frente-direita, com a quina em cima do slot (posição UFR) e o resto do cubo resolvido.",
                "Na animação, montar cada caso aplicando o inverso do algoritmo no cubo resolvido (já feito nos presets do cubo.html)."],
  },
 },
 {
  "n": 4, "titulo": "Peças presas e branco pra cima",
  "objetivo": "Tirar peças presas de slots errados e reorientar a quina com branco pra cima, transformando em caso conhecido.",
  "clipes": [
   {"narracao": "E quando a peça que você precisa está presa no lugar errado? "
                "Calma. Ninguém resolve esse caso direto. Você transforma num caso que já sabe.",
    "beats": [
     ("Quina presa atrás de grades pixel dentro de um slot", "zoom-in + tremida", "PEÇA PRESA", "corrente", True),
     ("Hero respira fundo, ícone de calma", "bob lento", "CALMA", "respiro"),
     ("Quebra-cabeça: peça difícil vira peça fácil", "morph pixelado", "DIFÍCIL → FÁCIL", "transform"),
    ]},
   {"narracao": "Essa é a grande sacada do éfe dois éle intuitivo. Todo caso chato vira um caso fácil. "
                "Primeiro leva as peças pro topo. Depois usa os casos do vídeo passado.",
    "beats": [
     ("Pergaminho 'GRANDE SACADA' desenrola", "pergaminho abre", "GRANDE SACADA", "papel"),
     ("Seta de 'chato' pra 'fácil' com brilho", "seta desliza", "CHATO → FÁCIL", "whoosh"),
     ("CUBO: peças sobem pro topo (foco)", "punch-in", "1. TOPO", "click"),
     ("Cartas R U R' e U R U' R' do ep. 3 reaparecem", "cartas entram", "2. CASO CONHECIDO", "carta ×2"),
    ]},
   {"narracao": "Peça presa em outro slot? | Gira com ípsilon até esse slot ficar na frente à direita. | "
                "Faz érre, u, érre linha. A peça sobe pro topo. | Agora é caso conhecido.",
    "beats": [
     ("CUBO (foco): quina presa no slot de trás piscando vermelho", "pulse vermelho", "SLOT ERRADO", "alarme"),
     ("CUBO: y2 — slot preso vem pra frente-direita", "giro completo", "y", "whoosh"),
     ("CUBO: R U R' — quina sai do slot e vai pro topo", "câmera fixa + grades quebrando", "R U R'", "click ×3 + vidro"),
     ("Grade quebra, quina livre no topo", "pico: flash + partículas", "LIVRE!", "fanfarra curta"),
    ]},
   {"narracao": "Branco olhando pra cima? Esse é o vilão. | Coloca a quina em cima do slot | e faz érre, u dois, érre linha. | "
                "Pronto, o branco saiu de cima. Mais uma vez: érre, u dois, érre linha.",
    "beats": [
     ("CUBO (foco): quina no topo com branco pra cima, olhos de vilão desenhados", "zoom + glitch", "BRANCO EM CIMA", "risada 8-bit"),
     ("CUBO: U até a quina ficar em UFR (em cima do slot)", "câmera fixa", "EM CIMA DO SLOT", "click"),
     ("CUBO: R U2 R' devagar", "câmera fixa", "R U2 R'", "click ×3"),
     ("Branco agora de lado brilha verde", "pop + check", "SAIU DE CIMA", "ding"),
    ]},
   {"narracao": "Repara. Érre e érre linha sempre andam em dupla. | Por isso a cruz nunca se desfaz. | "
                "Ajusta com u, acha a aresta | e cai num caso do vídeo três.",
    "beats": [
     ("CUBO: replay de R … R' com a cruz branca brilhando e intacta", "câmera em baixo, cruz em destaque", "R … R'", "rewind"),
     ("Escudo pixel em volta da cruz", "escudo surge + brilho", "CRUZ SEGURA", "escudo"),
     ("CUBO: U' traz a quina pra frente-direita; aresta procurada com lupa", "lupa passeando", "ACHA A ARESTA", "tique"),
     ("Carta do ep. 3 cai encaixando", "queda + tremida", "CASO CONHECIDO", "carta"),
    ]},
   {"narracao": "Resumo. Peça presa sai com érre u érre linha. Branco pra cima sai com érre u dois érre linha. | "
                "Pergunta: por que a cruz não se desfaz? | No último vídeo, juntando tudo pra ficar rápido.",
    "beats": [
     ("Duas cartas novas: 'tirar peça' e 'virar branco'", "cartas deslizam", "R U R' · R U2 R'", "carta ×2"),
     ("Quiz: cruz com '?' em cima", "pulse", "POR QUÊ?", "tique de quiz"),
     ("Mapa: nó 4 acende, câmera voa ao castelo final (nó 5)", "zoom-through", "FINAL", "fanfarra"),
    ]},
  ],
  "kit": {
   "resumo": ["Caso difícil = transformar em caso fácil: primeiro levar as peças pro topo.",
              "Peça presa em outro slot: traga o slot pra frente-direita (y) e faça R U R'.",
              "Quina com branco pra cima, em cima do slot: R U2 R' tira o branco de cima; ajuste com U e caia num caso do ep. 3."],
   "quiz": [("Como tirar uma peça presa no slot errado?", "Leve o slot pra frente-direita com y e faça R U R'."),
            ("Qual algoritmo tira o branco de cima da quina?", "R U2 R' (com a quina em cima do slot frente-direita)."),
            ("Por que a cruz não se desfaz com R U R'?", "Porque o R' devolve tudo o que o R tirou da camada de baixo; o U só mexe no topo.")],
   "flashcards": [("Peça presa", "y até o slot + R U R'"), ("Branco pra cima", "quina em UFR + R U2 R'"),
                  ("Regra da cruz", "R e R' em dupla com U no meio = cruz intacta")],
   "metafora": "'Vilão' e 'grades' são só ênfase visual; nenhum caso é impossível, só leva mais movimentos.",
   "conferir": ["Depois do R U2 R' a aresta pode estar em vários lugares; às vezes é preciso mais um ajuste antes de cair exatamente num caso do ep. 3.",
                "Ao tirar peça presa com R U R', o slot frente-direita recebe outras peças: isso é normal, ele ainda não estava resolvido."],
  },
 },
 {
  "n": 5, "titulo": "Juntando tudo + treino",
  "objetivo": "Ordem completa do F2L, look ahead e plano de treino.",
  "clipes": [
   {"narracao": "Você já sabe tudo pra fazer o éfe dois éle completo. Agora é só juntar as peças. | "
                "Só que o segredo de quem é rápido não é a mão. | É o olho.",
    "beats": [
     ("Castelo final; Chefão com meia barra de HP", "zoom-out dramático", "FASE FINAL", "trovão 8-bit", True),
     ("Mãos pixel girando rápido, depois um X em cima", "tremida + X carimba", "NÃO É A MÃO", "buzzer"),
     ("Olho pixel abre gigante brilhando ciano", "punch-in no olho", "É O OLHO", "brilho"),
    ]},
   {"narracao": "A ordem é sempre a mesma. | Faz a cruz. | Escolhe um par. | "
                "Leva o slot pra frente à direita com ípsilon. | Resolve o caso. | Repete até os quatro slots fecharem.",
    "beats": [
     ("Checklist HUD com 5 linhas vazias", "painel desliza", "A ORDEM", "painel"),
     ("CUBO: cruz branca embaixo destaca", "check na linha 1", "1. CRUZ", "ding"),
     ("CUBO (foco): um par pisca", "check na linha 2", "2. PAR", "ding"),
     ("CUBO: y no 'ípsilon' — slot do par vem pra frente-direita", "giro + check linha 3", "y", "whoosh"),
     ("CUBO: R U R' insere o par", "check linha 4", "R U R'", "click ×3"),
     ("4 pares entrando em corte rápido; contador ×4", "cortes rápidos + check linha 5", "×4", "click ×4"),
    ]},
   {"narracao": "Enquanto resolve um par, olha onde está o próximo. Isso se chama look ahead, olhar adiante. "
                "Seus olhos trabalham um par na frente das mãos. Melhor girar devagar sem parar do que rápido e travar.",
    "beats": [
     ("CUBO girando R U R' devagar; olho pixel procura outra peça em volta", "câmera orbita", "OLHA O PRÓXIMO", "tique"),
     ("Letreiro LOOK AHEAD em neon", "texto cinético", "LOOK AHEAD", "neon zumbindo"),
     ("Corrida: tartaruga constante passa coelho parado com '...'", "pan lateral", "DEVAGAR > TRAVAR", "passos"),
    ]},
   {"narracao": "Plano de treino. Semana um, só os casos básicos devagar. Semana dois, peças presas e branco pra cima. "
                "Semana três, cronômetro e look ahead. Dez minutos por dia.",
    "beats": [
     ("Calendário pixel com 3 semanas", "páginas virando", "PLANO", "papel"),
     ("Semana 1 marcada com carta R U R'", "carimbo", "SEMANA 1", "carimbo"),
     ("Semana 2 marcada com carta R U2 R'", "carimbo", "SEMANA 2", "carimbo"),
     ("Semana 3: cronômetro pixel correndo", "número subindo", "SEMANA 3", "tique-taque"),
     ("Ampulheta '10 min'", "pop", "10 MIN/DIA", "ding"),
    ]},
   {"narracao": "Recapitulando a série. Notação, ideia de par, casos básicos e como transformar caso chato em fácil. "
                "Com isso, as duas primeiras camadas saem em quatro pares. Travou? Revê o episódio daquela parte.",
    "beats": [
     ("Mapa com os 4 nós anteriores acendendo em sequência", "pan pelo mapa", "SÉRIE", "4 bipes"),
     ("CUBO: 4 pares entrando em corte rápido, duas camadas completas", "whip-pan entre slots", "4 PARES", "click ×4"),
     ("Chefão perde a barra de HP inteira e explode em pixels", "pico: flash + tremida + partículas", "F2L COMPLETO", "explosão 8-bit"),
    ]},
   {"narracao": "Pergunta final: o que é look ahead? Responde nos comentários com suas palavras. "
                "Depois disso falta só a última camada, com o ó éle éle e o pê éle éle.",
    "beats": [
     ("Quiz: olho com '?'", "pulse", "LOOK AHEAD = ?", "tique de quiz"),
     ("Balão de comentário pixel aparece", "pop", "COMENTA", "blip"),
     ("Portão novo no mapa com 'OLL · PLL' trancado", "zoom-through no portão", "PRÓXIMO ARCO", "porta rangendo"),
    ]},
  ],
  "kit": {
   "resumo": ["Ordem: cruz → escolher par → y até frente-direita → resolver caso → repetir 4×.",
              "Look ahead: procurar o próximo par enquanto resolve o atual.",
              "Treino: semana 1 casos básicos, semana 2 casos chatos, semana 3 cronômetro; 10 min/dia."],
   "quiz": [("Qual a ordem do F2L completo?", "Cruz, escolher par, trazer o slot pra frente-direita, resolver o caso, repetir 4 vezes."),
            ("O que é look ahead?", "Olhar e procurar o próximo par enquanto ainda resolve o atual."),
            ("O que vem depois do F2L?", "A última camada: OLL (orientar) e PLL (permutar).")],
   "flashcards": [("Look ahead", "olhar adiante, achar o próximo par"), ("OLL", "orienta a última camada"),
                  ("PLL", "permuta a última camada"), ("Regra de treino", "devagar sem parar > rápido travando")],
   "metafora": "'Derrotar o Chefão' = terminar o F2L, mas o cubo só fica resolvido depois da última camada.",
   "conferir": ["Plano de 3 semanas é sugestão didática, não regra oficial."],
  },
 },
]


def frases(txt):
    if "|" in txt:  # divisão manual de beats
        return [f.strip() for f in txt.split("|") if f.strip()]
    return [f.strip() for f in re.split(r"(?<=[.?!])\s+", txt.strip()) if f.strip()]


def palavras(txt):
    return len(re.findall(r"[\wÀ-ÿ']+", txt))


NOTACAO = re.compile(r"^[RLUDFBMxyz2'’ ↑↓·]+$")
def so_notacao(txt):
    """Aprendizado (EP01 abelhas): texto grande repetindo a fala é 'muita informação'.
    Na tela só fica a notação do cubo (R, U2, R' ↑...). O resto vira ''."""
    return txt if txt and NOTACAO.match(txt.strip()) else ""

def montar(ep):
    t = 0.0
    clipes = []
    for i, c in enumerate(ep["clipes"], 1):
        fs = frases(c["narracao"])
        bs = c["beats"]
        # Agrupa frases nos beats: se houver mais frases que beats, junta as menores.
        while len(fs) > len(bs):
            j = min(range(len(fs) - 1), key=lambda k: palavras(fs[k]) + palavras(fs[k + 1]))
            fs[j:j + 2] = [fs[j] + " " + fs[j + 1]]
        while len(fs) < len(bs):  # divide a maior frase na vírgula
            j = max(range(len(fs)), key=lambda k: palavras(fs[k]))
            partes = fs[j].split(", ", 1)
            if len(partes) < 2:
                partes = fs[j].split(" ", len(fs[j].split()) // 2)
                partes = [" ".join(partes[:-1]), partes[-1]] if len(partes) > 1 else partes
            fs[j:j + 1] = [partes[0] + ("," if not partes[0].endswith((",", ".")) else ""), partes[1]]
        n = palavras(c["narracao"].replace("|", ""))
        dur = n / RITMO
        beats = []
        ini_clip = t
        for f, b in zip(fs, bs):
            d = palavras(f) / RITMO
            visual, mov, txt, sfx = b[:4]
            beats.append({"t_ini": round(t, 1), "t_fim": round(t + d, 1), "fala": f,
                          "visual": visual, "imagem": "cubo.html" if visual.startswith("CUBO") else "bg_arena/hero/chefao (reuso)",
                          "movimento": mov, "texto_tela": so_notacao(txt), "sfx": sfx,
                          "video_ia": bool(b[4]) if len(b) > 4 else False})
            t += d
        clipes.append({"id": f"ep{ep['n']:02d}_clip{i:02d}", "narracao": c["narracao"].replace(" | ", " "),
                       "palavras": n, "duracao_s": round(dur, 1), "t_ini": round(ini_clip, 1), "beats": beats})
    return clipes, t


def mmss(s):
    return f"{int(s // 60)}:{int(round(s % 60)):02d}"


def md(ep, clipes, total):
    L = [f"# Episódio {ep['n']} de 5 — {ep['titulo']}", ""]
    L += ["## Ficha",
          f"- **Tema/nível:** cubo mágico 3×3, método F2L intuitivo, iniciante que já sabe o método de camadas.",
          f"- **Objetivo:** {ep['objetivo']}",
          f"- **Duração estimada:** {mmss(total)} ({sum(c['palavras'] for c in clipes)} palavras a {RITMO} p/s) — alvo 1:00–1:30 (mínimo exato 1:00).",
          "- **Legenda do Jogo:** Chefão = cubo embaralhado · HP do Chefão = quanto falta resolver · "
          "cartas de golpe = algoritmos · mapa de fases = os 5 episódios · slot = casa do par.",
          f"- **Hero (token fixo):** `{HERO}`",
          f"- **Chefão (token fixo):** `{CHEFAO}`",
          f"- **Style tokens:** `{ESTILO}`",
          "- **Visual principal:** cubo 3D em CSS (`anim/cubo.html`). Linhas com `CUBO:` = o cubo executa a "
          "sequência no mesmo instante da fala, com a notação grande na tela.", ""]
    for c in clipes:
        L += [f"## {c['id']} · {mmss(c['t_ini'])} → {mmss(c['t_ini'] + c['duracao_s'])} ({c['palavras']} palavras, ~{c['duracao_s']}s)",
              "", f"> {c['narracao']}", "",
              "| tempo | fala | visual | movimento | texto | SFX |", "|---|---|---|---|---|---|"]
        for b in c["beats"]:
            star = "⭐ " if b["video_ia"] else ""
            L.append(f"| {b['t_ini']}–{b['t_fim']}s | {b['fala']} | {star}{b['visual']} | {b['movimento']} | **{b['texto_tela']}** | {b['sfx']} |")
        L.append("")
    k = ep["kit"]
    L += ["## Prompts de imagem (gerar só uma vez, reaproveitar nos 5 episódios)", ""]
    L += [f"- **{nome}:** `{p}`" for nome, p in IMAGENS.items()]
    L += ["", "## Kit de estudo", "", "**Resumo**", ""] + [f"- {r}" for r in k["resumo"]]
    L += ["", "**Quiz**", ""] + [f"{i}. {q}" for i, (q, _) in enumerate(k["quiz"], 1)]
    L += ["", "<details><summary>Gabarito</summary>", ""] + [f"{i}. {a}" for i, (_, a) in enumerate(k["quiz"], 1)] + ["", "</details>"]
    L += ["", "**Flashcards**", "", "| frente | verso |", "|---|---|"] + [f"| {a} | {b} |" for a, b in k["flashcards"]]
    L += ["", f"**Onde a metáfora falha:** {k['metafora']}", "", "**⚠️ Conferir**", ""] + [f"- {c}" for c in k["conferir"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    resumo = []
    for ep in EPS:
        clipes, total = montar(ep)
        assert 60 <= total <= 90, (ep["n"], total)
        (AQUI / f"ep{ep['n']:02d}.md").write_text(md(ep, clipes, total), encoding="utf-8")
        (AQUI / f"ep{ep['n']:02d}.json").write_text(json.dumps(
            {"ep": ep["n"], "titulo": ep["titulo"], "ritmo_pps": RITMO, "duracao_s": round(total, 1),
             "imagens": IMAGENS, "clipes": clipes, "kit": ep["kit"]}, ensure_ascii=False, indent=2), encoding="utf-8")
        resumo.append(f"ep{ep['n']:02d}  {mmss(total)}  {sum(c['palavras'] for c in clipes)} palavras  {ep['titulo']}")
    print("\n".join(resumo))

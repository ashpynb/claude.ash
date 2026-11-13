# O que mudou na Fábrica Viral e no Estúdio Viral — guia de atualização do Content Factory

Para a sessão do Claude que mantém o **Content Factory**. Leia inteiro antes de mexer.
Fonte: repositório `ashpynb/claude.ash`, branch `claude/videos-economia-reverse-eng-e5yftd`,
commits `bbd9c93` (Estúdio v5) até `ed74a8a` (pacote). Data: 13/11/2026.

Resumo em uma frase: **o Estúdio deixou de ser um simulador que pedia fatos à usuária e virou um
formulário de 4 etapas que só escolhe tipo, ideia, acabamento e personagem; o roteiro e a produção
inteira agora moram numa skill única (`fabrica-viral`) com um script (`video.py`) que vai do texto
aprovado ao MP4; e o Estúdio passou a entregar os dados em JSON pra integração.**

---

## 1. Estúdio Viral (a página)

Link do artifact: https://claude.ai/artifact/G1kStDLJTDJhSj6JFHefvj (versão 8, privado).
Arquivo fonte: `.claude/skills/fabrica-viral/ferramentas/estudio_viral.html`
(versão autônoma com `<!doctype>` em `pacote-content-factory/estudio-viral/index.html` do zip).

### 1.1 O que saiu (se o Content Factory ainda tem, remova)
| Removido | Por quê |
|---|---|
| Campos **Gancho**, **Fatos** (`fato \| destaque`) e **Fecho** obrigatórios | A usuária pediu: "eu só decido a ideia, o desenho; o roteiro é do Claude". Viraram um bloco opcional "Quer sugerir algo?" na v3 e **sumiram de vez na v5**. |
| **Nota viral 0–100** (checklist com pesos) | Confundia; o roteiro é avaliado pelo Claude contra `regras.md`. |
| **Rascunho de ritmo** (tabela tempo/fala/tela) e a **prévia animada em canvas** do vídeo | A prévia em canvas não parecia com o vídeo 3D real. Trocada por **quadros reais** dos nossos vídeos em cada cartão. |
| Opção **"Música de fundo"** | Regra fixa: nenhum vídeo tem música. |
| Tipo **"Problema → solução"** e o seletor separado de **6 estilos** (feijão, low-poly, iso, cartoon3d, mascote, mapa) | O estilo agora vem amarrado ao tipo. |
| Tipo **"Escala absurda"** (v5–v6) | **Substituído por "2D flat engraçado"** na v7. Escala (pilha, balança, contador) virou recurso dentro do 2D flat. |

### 1.2 Como ficou (v8): 4 etapas
1. **Que tipo de vídeo?** 5 cartões, cada um com: 3 quadros reais que alternam (miniatura de celular),
   nome, explicação em uma frase, a **estrutura numerada** do roteiro, o estilo e a prova (views das
   referências). Tipos e chaves:

   | chave (`tipo`) | Nome | Estilo | Personagem? | Duração-alvo |
   |---|---|---|---|---|
   | `voce` | Você é um… | 3D cartoon com luz de cena | não | 1:10 |
   | `construiu` | Você construiu um… | 3D low-poly, dia claro, com corte transversal | não | 1:20 |
   | `ese` | E se tu… | 3D boneco de primitivas | **sim** | 1:15 |
   | `passo` | Passo a passo | Isométrico técnico | não | 1:05 |
   | `flat2d` | 2D flat engraçado (**novo**) | 2D flat (vetor plano, cores chapadas, contorno) | **sim** | 1:10 |

   Logo abaixo dos cartões: **Acabamento do 3D** (novo na v7) com dois botões, "Padrão do tipo" e
   **"Cinema: luz de cinema e malha bem feita"**. Aparece só nos 4 tipos 3D (some no `flat2d`).
2. **Sua ideia**: prefixo fixo do tipo ("Você é um", "Você construiu um", "E se tu", "Como se faz",
   "Por que") + campo de uma frase + 5 sugestões clicáveis + botão "Sortear uma ideia".
3. **O personagem**: **só aparece em `ese` e `flat2d`** (regra da usuária, v7). Nome + escolhas de
   pele, cabelo (curto, topete, cacheado, rabo de cavalo, careca), cor do cabelo, corpo (magro,
   normal, fofinho), roupa (camiseta, moletom, pijama, jaleco), cor da roupa, acessório (nenhum,
   óculos, óculos escuros, boné, fone), expressão. Esboço 2D animado ao lado; a nota embaixo muda
   conforme o tipo ("vira 3D de primitivas" ou "fica assim, 2D flat").
4. **O que eu vou entregar**: 4 blocos (tipo · estilo [+ "· cinema"] · ~duração · "roteiro primeiro"),
   botões **Copiar pedido** e **Copiar como JSON** (novo na v8) e a caixa com o texto do pedido.

Faixa fixa no topo com as regras: voz Antônio · 3,2 palavras/s · 1:00 a 1:30 · sem música · título
grande só nos 3 s iniciais · legenda de 1 a 3 palavras · todo número com fonte.

### 1.3 O texto do pedido (formato exato, v8)
```
Faz um vídeo viral do tipo "<nome do tipo>": <prefixo> <ideia>
Estilo: <estilo do tipo>.
[se cinema e tipo 3D] Acabamento cinema: luz de cinema (luz principal quente, contraluz, preenchimento frio, neblina, sombras suaves) e malha bem feita (mais polígonos, bordas arredondadas, sombreamento liso).
[se ese/flat2d] Personagem: <nome> (<descrição>), em 3D de primitivas com rosto pintado e expressões que mudam com a história.   ← ou "em 2D flat, com expressões exageradas…"
Estrutura: <passo 1> → <passo 2> → … .
<instrução extra do tipo (corte transversal + etiquetas / objetos texturizados e física / 2D flat …)>

Escreve você o roteiro, com humor e um fato conferido em fonte por frase; o que não tiver fonte vai pra "⚠️ Conferir".
Usa a skill fabrica-viral (regras.md): voz Antônio a 3,2 palavras/s, de 1:00 a 1:30, sem música, título grande só no gancho, legenda de 1 a 3 palavras com a palavra-chave amarela.
Me mostra o roteiro antes de produzir.
```
**Mudança importante:** versões antigas diziam `Segue o referencias/aprendizados.md…`. Esse arquivo
**não existe mais**; agora é `Usa a skill fabrica-viral (regras.md)`. Se o Content Factory monta o
pedido sozinho, atualize essa linha.

### 1.4 Integração (novo na v8)
Ao clicar em **Copiar pedido** ou **Copiar como JSON**, o Estúdio:
- dispara `document` → `CustomEvent('estudio-viral:pedido', {detail: dados})`;
- se estiver num iframe, faz `window.parent.postMessage({tipo:'estudio-viral:pedido', dados}, '*')`
  (o Content Factory deve conferir `event.origin`);
- expõe `window.estudioViral.dados()` (leitura a qualquer momento) e `window.estudioViral.versao === 1`.

Formato de `dados` (versão 1):
```json
{"versao":1,"origem":"estudio-viral","tipo":"ese","tipo_nome":"E se tu…",
 "ideia":"ficasse 11 dias sem dormir","frase":"E se tu ficasse 11 dias sem dormir",
 "estilo":"3D boneco de primitivas","acabamento":"padrao",
 "estrutura":["Gancho: \"E se tu…?\" + título grande","\"Esse é o [nome].\"","Linha do tempo: dia 1, semana 1, mês 1 (número na tela)","Virada inesperada","\"Na parte dois…\""],
 "duracao_alvo":"1:15",
 "personagem":{"nome":"Sérgio","pele":"#f1c08f","cabelo":"curto","corCabelo":"#3a2416","roupa":"pijama","corRoupa":"#3f6df2","acessorio":"oculos","cara":"feliz","corpo":"normal","descricao":"pele clara, cabelo curto castanho escuro, corpo normal, pijama azul, óculos, expressão feliz"},
 "skill":"fabrica-viral","pedido":"Faz um vídeo viral do tipo …"}
```
- `acabamento`: `padrao` | `cinema` | `2d` (sempre `2d` no tipo `flat2d`).
- `personagem`: `null` nos tipos `voce`, `construiu`, `passo`.
- Valores de `cabelo`: curto, topete, cacheado, rabo, careca · `roupa`: camiseta, moletom, pijama,
  jaleco · `acessorio`: nenhum, oculos, escuros, bone, fone · `cara`: feliz, surpreso, confiante,
  cansado · `corpo`: magro, normal, fofo. Cores em hex.

### 1.5 Compatibilidade
- **localStorage**: a chave mudou de `estudioViral` (v1–v2) → `estudioViral2` (v3–v4) →
  **`estudioViral3`** (v5+). Dados antigos são ignorados (não há migração; o padrão abre em "E se tu…").
- Um `tipo: "escala"` salvo é ignorado (a página volta ao padrão). Se o Content Factory guardou
  pedidos com `escala`, trate como `flat2d`.
- A página não depende de servidor; só carrega Google Fonts (tem fallback). Imagens embutidas em data URI (~230 KB).

---

## 2. Skills: de pastas soltas para um pacote

### 2.1 Antes → depois
| Antes (some, não procure) | Agora |
|---|---|
| `referencias/aprendizados.md` + `referencias/NN_*.md` + `estilos.md` | `.claude/skills/fabrica-viral/regras.md` (regras), `moldes.md` (tipos), `fichas/01–10` (referências) |
| `producao/*.html`, `narrar.py`, `montar_tempo.py`, `render_http.js`, `render_par.js`, `mix_viral.py`, `mix07.py` | `fabrica-viral/ferramentas/` (`narrar.py`, `render.js`, `mix.py`, `teste_css.js`, `kit3d.js`, **`video.py`**) |
| `roteiro/viralNN_*.md` | `fabrica-viral/exemplos/<pasta>/roteiro.md` (um exemplo por tipo) |
| `simulador/estudio_viral.html` | `fabrica-viral/ferramentas/estudio_viral.html` |
| `out/*.mp4`, `videos/`, `audio/`, `referencias/img/` | fora do repo (no histórico do git); MP4 novo vai pra usuária pelo chat, não é comitado |
| série do cubo (`anim/`, `roteiro/ep01–05`, `HANDOFF.md`) | skill própria `serie-cubo-f2l` (não vai pro Content Factory) |

### 2.2 Conjunto exato que o Content Factory precisa (7 skills)
`fabrica-viral` (obrigatória) · `roteiro-humor` · `comedy-writer` · `clean-comedy-rewrite` ·
`viral-hooks` · `ig-caption` · `assistir-youtube` (opcional, precisa de chave do Gemini como segredo).
Nenhuma depende de `publicar-no-estudio`, `serie-cubo-f2l`, `anatomy`, `watch` ou outras `ig-*`.
O `roteiro-humor` agora aponta pra `fabrica-viral/regras.md` e trata o `ig-reel/hookscore.py` como opcional.

### 2.3 Estrutura da `fabrica-viral`
```
SKILL.md          fluxo: pedido → roteiro com fontes → aprovação → video.py → conferir → entregar
regras.md         decisões da usuária + o que foi medido nas referências + checklist da folha de contato
moldes.md         os 5 tipos (estrutura, estilo, referências, exemplo nosso)
roteiro.md        conta de palavras, fatos e fontes, ⚠️ Conferir, humor, formato de entrega
visual-3d.md      API do kit3d, câmera, acabamento cinema, 2D flat, receitas, erros conhecidos
som-e-voz.md      Antônio, ajuste de ritmo, 25 efeitos sintetizados
fichas/01–10      referências medidas (transcrições, cortes, views)
exemplos/         viral07 (cama), viral09 (sala de prova), viral08 (represa em corte),
                  corte_transversal, flat2d_sergio (2D), viral04 (Você é), viral05 (isométrico), viral06 (modelos CC0)
ferramentas/      video.py, narrar.py, render.js, teste_css.js, mix.py, kit3d.js, modelo_cena.html,
                  vendor/ (three r149, cannon-es, Lilita One), modelos/ (CC0), estudio_viral.html,
                  empacotar.sh, INSTALAR_content_factory.md, este arquivo
```

---

## 3. Produção: o que melhorou

### 3.1 `video.py` (novo): um comando por etapa
```
python .claude/skills/fabrica-viral/ferramentas/video.py novo   SLUG [--de viral09]
python …/video.py narrar SLUG [--alvo 3.2]
python …/video.py testar SLUG
python …/video.py render SLUG [-j 4] [--limpar]
```
- `novo`: cria `trabalho/SLUG/` com `cena.html` (do modelo ou de um exemplo), `falas.txt` e links pro kit.
- `narrar`: lê `falas.txt` (uma linha = um beat), gera a voz por beat, junta com 0,12 s de respiro e
  **ajusta o `rate` sozinho até 3,2 ± 0,05 palavras/s** (antes era tentativa manual). Avisa se ficou
  fora de 1:00–1:30 ("ajuste o roteiro, nunca a velocidade").
- `testar`: sobe um servidor, renderiza **2 quadros por beat** e **confere as camadas HTML/CSS**
  (texto fora da tela, sobreposição entre legenda/número/cartões/etiquetas, legenda com mais de 2
  linhas) e monta a **folha de contato** pra olhar antes do render. Já pegou um erro real no modelo.
- `render`: 4 processos em paralelo (~70 quadros/min, ~35 min pra 1:20), pula quadros prontos
  (dá pra re-renderizar só os beats corrigidos apagando os quadros deles), mixa os efeitos a partir
  dos eventos da própria cena e gera o MP4 (H.264, crf 23, ≤9 Mb/s) + folha final.
- `trabalho/` tem `.gitignore`: quadros, áudio e MP4 não vão pro git.

### 3.2 kit3d.js: o que entrou desde a v5
| Recurso | Pra quê |
|---|---|
| `boneco(P)` com `cab:'topete'` e `bone:'#cor'` (boné virado pra trás, topete aparecendo) | personagem do Enem; antes o boné cobria os olhos |
| `luzCinema(cena,{alvo,quente,fria,forca,neblina})` | **acabamento cinema**: principal quente com sombra macia, contraluz fria, preenchimento frio, neblina; `.mira([x,y,z])` por plano |
| `G.esfFina`, `G.capFina`, `G.cxFina`, `G.extrusaoFina` | **malha bem feita**: mais segmentos, bordas arredondadas, bisel |
| `corte`, `faceCorte(w,h,tipo,furos)` | corte transversal com tampa de terra/parede e furo pra ver dentro |
| `etiqueta` + `atualizaEtiquetas` | pílula presa na peça, aparece quando o nome é falado |
| `trilha(pontos,alvos)` | câmera voando numa curva |
| `copias(geo,mat,lista)` | InstancedMesh (floresta, fila de carros) |
| `simular(...)` (cannon-es pré-calculada) | coisas caindo determinísticas no render paralelo |
| `modelo_cena.html` | cena inicial pronta: legendas 1–3 palavras com chave amarela, número, título só no gancho, cartão PARTE 2, efeitos, câmera aberta, `CENAS` por beat |

### 3.3 Regras novas (estão no `regras.md`)
- **Câmera aberta**: personagem de corpo inteiro (distância 10–16 pro boneco de 2,6), close só em 1–2 reações.
- **Testar as camadas CSS antes do render** (`video.py testar`).
- **Coerência física**: personagem sentado NA cadeira, atrás da mesa; nada flutuando ou atravessando
  (erro real corrigido no vídeo do Enem).
- **Texto pintado em objeto 3D só depois da fonte carregar** (`await document.fonts.load(...)`).
- **Personagem só em "E se tu…" e "2D flat"**; nos outros, o protagonista é a coisa.
- **Estilos**: 3D (primitivas, low-poly, cartoon com luz de cena, isométrico) com acabamento cinema
  opcional, ou 2D flat engraçado. Sem pixel art, sem música.
- MP4 não é comitado; vai pro chat. Pedido de engajamento só na legenda do post.

### 3.4 Vídeos feitos nesta fase (referência de qualidade)
| Vídeo | Tipo / estilo | Duração |
|---|---|---|
| viral07 "E se tu ficasse 1 mês sem se mexer?" | E se tu… / 3D primitivas (cama com colcha que se molda) | 1:19 |
| viral08 "Você construiu uma represa" | Você construiu… / low-poly + corte transversal + etiquetas | 1:25 |
| viral09 "E se tu fizesse a redação do Enem hoje?" (tema 2026: SUS) | E se tu… / 3D primitivas, sala de prova | 1:24 |
Os MP4 estão no histórico do git (commits `0035349`, `6d31bfd`, `54d2e4d`); cenas em `exemplos/`.

---

## 4. Checklist pra sessão do Content Factory
1. **Substitua** a página do Estúdio pela v8 (`estudio-viral/index.html` do zip ou o arquivo fonte).
2. **Remova** do Content Factory qualquer UI antiga de fatos/gancho/fecho, nota viral, prévia em
   canvas, música e o tipo "Escala absurda".
3. **Ligue a integração**: ouça `estudio-viral:pedido` (evento ou `postMessage`, conferindo a origem)
   e leia `dados.pedido` (texto pro Claude) e os campos estruturados (tipo, acabamento, personagem).
4. **Instale as 7 skills** em `.claude/skills/` (substituindo versões antigas de `roteiro-humor` etc.).
   Apague referências a `referencias/aprendizados.md` e `producao/` em prompts e docs.
5. **Ambiente** de quem produz: `pip install edge-tts soundfile numpy pillow`, Node 18+ com
   Playwright/Chromium, ffmpeg, internet (voz e pesquisa). Gemini só pro `assistir-youtube`.
6. **Fluxo**: Content Factory manda `pedido` → Claude escreve roteiro e espera aprovação → `video.py`
   novo/narrar/testar/render → MP4 entregue.
7. Pra gerar o pacote de novo depois de mudanças: `bash .claude/skills/fabrica-viral/ferramentas/empacotar.sh`.

## 5. O que ainda NÃO está feito (sugestões aceitas como ideia, não implementadas)
- Tipos novos pesquisados: **Conversa no WhatsApp**, **Recorte de papel (estilo Vox)**,
  **Quadro branco/desenho à mão**, **Tipografia cinética**.
- Técnicas pra todos os tipos: **pausa de quiz** (~2,5 s antes da revelação) e **loop perfeito**
  (último quadro = primeiro).
- Nenhum vídeo inteiro ainda no tipo **2D flat engraçado** nem com **acabamento cinema** (só o teste de luz).

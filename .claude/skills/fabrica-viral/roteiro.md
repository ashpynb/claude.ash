# Como escrever o roteiro

## Conta
- 3,2 palavras/s → **1:00 = 192 palavras, 1:30 = 288**. Mire **230–270** (dá ~1:15–1:25 com respiros).
- Frases curtas: até ~16 palavras por linha. **Cada linha = um beat = uma cena** (algo novo na tela).
- Números por extenso na fala ("sessenta e dois mil"); na tela, em algarismo ("62.200 m³/s").
- Conte: `wc -w falas.txt`. O `video.py narrar` mede de verdade e ajusta a velocidade.

## Fatos
- **Um fato conferido por frase.** Pesquise (WebSearch) e guarde o link. Duas fontes quando o número
  é surpreendente. Prefira fonte oficial (governo, universidade, artigo) a blog.
- Se o número varia entre fontes, use a forma vaga e honesta ("uns", "quase", "até") e explique no
  ⚠️ Conferir (ex.: "umas quarenta Cataratas" — a conta muda com a vazão usada).
- O que não achou fonte: **fora da fala** ou no ⚠️ Conferir. Exemplos e opiniões no roteiro: marque
  como exemplo ("Tipo: o governo aumenta…" é exemplo de redação, não fato).
- Tema da atualidade (prova, notícia): confira a data e o enunciado exato.

## Fórmula medida (20 de 20 shorts da referência do claude-animated-shorts, MIT)
Serve pros moldes de história e de "como funciona"; nos moldes fixos ("Você é…", "construiu") use como tempero.
1. **Gancho = paradoxo dito como fato**, 1ª frase, sem preparação ("Setenta e quatro soldados derrubaram
   uma ponte de ferro só andando nela.").
2. **Cenário** em 1–2 frases concretas (hora, lugar, um nome comum, um número).
3. **Escalada** em 3–6 beats, cada um maior; 1–2 piadas de exagero.
4. **Beat de mistério:** uma pergunta no meio ("Pera. Como assim?").
5. **Virada com "Sabe por quê?"** (na referência, "You see," em 14 de 20) → o mecanismo real com uma
   **analogia do dia a dia** ("Sabe quando você empurra alguém no balanço?").
6. **Fecho irônico** em 1–2 frases curtas; o vídeo acaba na última palavra.
- Dupla seca que funciona: "Por sorte… / Por azar…". Nunca descreva o que a imagem já mostra.

## Antes de produzir: verificador
Roteiro pronto → skill **`verificador-viral`** (portão 1). Ela roda `validar_roteiro.py`, pontua o gancho
e dá a nota de viralização. Se passar (≥ 8,5), segue pra produção **sem esperar o ok** (pedido da usuária).

## Humor (skills `roteiro-humor`, `comedy-writer`)
- Personificar ("a água é espertinha"), contraste absurdo ("três semanas de cama fizeram mais
  estrago que trinta anos de vida"), reação do personagem, objeto do dia a dia como metáfora.
- Humor limpo; nunca piada às custas de grupo de pessoas.

## Entrega pra aprovação (`trabalho/SLUG/roteiro.md`)
1. Cabeçalho: tipo, estilo, personagem, nº de palavras e duração estimada, título do gancho.
2. Tabela: # | Fala | Cena | Na tela (número/etiqueta).
3. Legenda do post (com o "marca aquele amigo…").
4. **Fontes** (com link por fato) e **⚠️ Conferir**.
No chat: mostre as falas numeradas, a nota do verificador, as fontes principais e o ⚠️ Conferir.
Não pergunte "me dá o ok": o `verificador-viral` aprova (ver as exceções que ainda pedem ok na skill).

## Depois da aprovação do verificador
Copie as falas, uma por linha, pra `trabalho/SLUG/falas.txt` (sem numeração) e siga o SKILL.md.

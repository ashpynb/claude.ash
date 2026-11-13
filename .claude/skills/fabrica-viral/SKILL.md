---
name: fabrica-viral
description: Fábrica de vídeos virais curtos (9:16, ~1:00–1:30) em português com a voz do Antônio, do pedido ao MP4. Use quando a usuária pedir um vídeo viral, colar um pedido do Estúdio Viral ("Faz um vídeo viral do tipo…"), pedir roteiro de "Você é um…", "Você construiu um…", "E se tu…", "Passo a passo" ou "Escala absurda", mandar um vídeo de referência pra engenharia reversa, ou pedir pra corrigir/regerar um vídeo já feito. Contém as regras dela, os moldes de roteiro, o kit 3D (boneco de primitivas, corte transversal, física), e o script video.py que narra, testa, renderiza e mixa.
---

# Fábrica viral

Tudo que aprendemos em ~10 vídeos e 10 fichas de referência, num pacote só. Leia nesta ordem,
só o que a etapa precisar:

| Arquivo | Quando ler |
|---|---|
| `regras.md` | **Sempre, antes de tudo.** Decisões da usuária que valem pra todo vídeo. |
| `moldes.md` | Ao escrever o roteiro: os 5 tipos de vídeo, estrutura, exemplos e números das referências. |
| `roteiro.md` | Ao escrever o roteiro: fatos com fonte, ⚠️ Conferir, conta de palavras, formato de entrega. |
| `visual-3d.md` | Ao montar as cenas: kit3d, câmera, estilos, receitas de cena, erros que já cometemos. |
| `som-e-voz.md` | Narração, ritmo e efeitos. |
| `fichas/01–10` | Só se precisar do detalhe de uma referência (transcrições, medições). |
| `exemplos/` | Cenas completas que funcionaram: copie padrões em vez de reinventar. |

## Fluxo (siga sempre)

1. **Entender o pedido.** Se veio do Estúdio Viral, ele já traz tipo, estilo, ideia e personagem.
   Se for tema da atualidade (ex.: tema do Enem do ano), pesquise antes de escrever.
2. **Roteiro** (`roteiro.md` + `moldes.md`): um fato conferido em fonte por frase, humor, o que não
   tiver fonte vai pra "⚠️ Conferir". Conte as palavras: alvo 3,2 palavras/s e 1:00–1:30.
   Salve em `trabalho/SLUG/roteiro.md` (com fontes) e **mostre à usuária e espere o ok**.
3. **Produção** (depois do ok), com `ferramentas/video.py`:
   ```
   F=.claude/skills/fabrica-viral/ferramentas
   python $F/video.py novo SLUG [--de viral09]   # pasta trabalho/SLUG com cena.html + links do kit
   # escreva as falas aprovadas em trabalho/SLUG/falas.txt (uma por linha = um beat)
   python $F/video.py narrar SLUG                # voz + ajuste automático do ritmo pra 3,2 p/s
   # monte as cenas em trabalho/SLUG/cena.html (visual-3d.md)
   python $F/video.py testar SLUG                # camadas CSS + folha de contato: OLHE a folha
   python $F/video.py render SLUG                # 4 processos, ~25–40 min pra 1:20
   ```
   Rode o render em segundo plano e avise a usuária do tempo estimado.
4. **Conferir** a `folha_final.jpg` (câmera aberta, personagem inteiro, nada cortado, texto legível).
5. **Entregar**: envie o MP4 pelo chat (SendUserFile) com a legenda do post (pedido de "marca um amigo"
   só na legenda, com as fontes). **Não comite MP4 nem quadros** (o repo fica leve; `trabalho/` é ignorado).
   Comite `trabalho/SLUG/{roteiro.md,falas.txt,cena.html}` só se a usuária quiser guardar.
6. **Registrar**: se a skill `publicar-no-estudio` existir, grave o vídeo e a regra nova no Estúdio.
   Regra nova (pedida pela usuária ou medida em referência) vai também pro `regras.md` desta skill.

## Correções pedidas depois de pronto
Mexa só no que ela apontou. Pra re-renderizar só parte: apague os quadros dos beats afetados em
`trabalho/SLUG/quadros/` e rode `render` de novo (quadros existentes são pulados), sem `--limpar`.

## Engenharia reversa de referência
Baixe com yt-dlp (TikTok/Instagram) ou use a skill `assistir-youtube` (YouTube bloqueia download aqui).
Meça: duração, cortes (`ffmpeg … select='gt(scene,0.3)'`), transcrição (faster-whisper → palavras/s),
folha de contato. Escreva `fichas/NN_nome.md` e leve só as regras novas pro `regras.md`.

## Ambiente
- Nuvem: `pip install edge-tts soundfile numpy pillow` (somem quando o container reinicia).
  Playwright/Chromium e ffmpeg já vêm instalados. three.js r149, cannon-es e a fonte Lilita One
  estão em `ferramentas/vendor/` (licenças junto).
- Edge TTS precisa do proxy (o `narrar.py` já usa `$HTTPS_PROXY`).
- Créditos pagos (imagem/vídeo de IA): mostrar custo e esperar ok. Hoje não usamos.
- Outras skills úteis aqui: `roteiro-humor`, `comedy-writer`, `viral-hooks`, `assistir-youtube`,
  `watch`, `anatomy` (figuras isométricas), `ig-caption` (legenda do post), `publicar-no-estudio`.
- Estúdio Viral (artifact onde a usuária escolhe tipo/ideia/personagem):
  https://claude.ai/artifact/G1kStDLJTDJhSj6JFHefvj — fonte em `ferramentas/estudio_viral.html`.

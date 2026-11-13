# Ficha 11: 7 repositórios de automação comparados com a fábrica (2026-11-13)

Lido o código de cada um (clone raso). Lista completa de 262 repositórios: `referencias/06_repos_automacao_viral.md`
(fora do pacote). Só técnica; nada de conteúdo, personagem ou imagem deles.

| # | repo (licença, commit) | o que a fábrica JÁ tinha igual | o que entrou agora | o que ficou de fora e por quê |
|---|---|---|---|---|
| 1 | mromidev/claude-animated-shorts (MIT, e3b817b): three.js + Remotion, 2D em mundo 3D | cena por código quadro a quadro, som sintetizado, folha de contato, regras medidas em referência, verificador com nota (ficha 02) | **`qa.py`** (adaptado do `short_qa.py`: preto/branco/parado/pulos/loudness/folhas, agora em fluxo); **volume −14 LUFS** no render; números de câmera, tremida, contorno, profundidade e armadilhas em `visual-3d.md`; **fórmula de roteiro** em `roteiro.md` | Remotion (trocaria todo o nosso motor; licença paga pra empresa > 3 pessoas); grão de filme (eles mesmos desligaram); música (regra: sem música) |
| 2 | liyupi/niulai-video-generator (MIT, cc60adb): Three.js procedural + TTS + FFmpeg | mesmo método (3D por código, sem IA de vídeo), tempo da legenda = tempo do áudio | **asserts duros** no `qa.py` (tempo.js em ordem, sem sobreposição, total = vídeo) e no `validar_roteiro.py` (roteiro volta pra reescrita se falhar) | o estilo deles é de um filme específico; TTS `say` só existe no macOS |
| 3 | gyoridavid/short-video-maker (MIT, 9bb9a21): servidor MCP + REST, Kokoro TTS, Remotion | pedido estruturado em JSON (Estúdio Viral → `estudio-viral:pedido`), legenda por palavra | nada de código | expor a fábrica como MCP só vale quando o Content Factory chamar sem um Claude no meio; hoje o pedido já vai em JSON pra uma sessão. Kokoro não tem a voz do Antônio |
| 4 | nicolaigaina/ai-video-captions (MIT, bd87ac7) e sebetancurch/auto-caption (MIT, b4e7cf6): legendas ASS animadas | **igual ou melhor**: legenda em HTML por cima da cena (Lilita One, contorno, palavra-chave amarela, pop por grupo de 1–3 palavras), sincronizada pelo WordBoundary exato do Edge (eles estimam com Whisper) | nada | ASS/FFmpeg seria um 2º sistema de legenda pra manter |
| 5 | DojoCodingLabs/remotion-superpowers (MIT, 970efd2): plugin com revisão por IA | folha de contato + checklist de 11 pontos | **rubrica de vídeo** (gancho, ritmo, composição, legibilidade, transições, sincronia, mix, final; consertos com segundo e gravidade) no portão 2 do `verificador-viral` | a revisão deles sobe o vídeo pra TwelveLabs (outra conta e chave); aqui o Claude lê a `visao_geral.jpg` do QA |
| 6 | harry0703/MoneyPrinterTurbo (MIT, ce289ff): tema → stock footage → voz → legenda → música | **mesmo Edge TTS** com tempo por palavra; roteiro por LLM; legenda branca com contorno; várias vozes | nada de código | ver tabela abaixo |
| 7 | Jakeschincariol/youtube-agent-skill (MIT, a2feb21): 11 skills de YouTube | `hookscore.py` (já usado) e as `ig-*` do mesmo autor | **`retencao.py`** (adaptado do `yt-retention`: gancho 3 s / quedas com a fala do tempo.js / ladeira) no portão 3; `hookscore.py` copiado pra dentro do verificador (o pacote não leva `ig-reel`) | `yt-seo`, `yt-package` etc. são de YouTube longo |

## MoneyPrinterTurbo (6): o que é igual, o que é diferente, o que dá pra mudar
| tema | MoneyPrinterTurbo | fábrica | mudar? |
|---|---|---|---|
| voz | Edge TTS + 10 outros (Azure, ElevenLabs, Kokoro, SiliconFlow…) | Edge TTS `pt-BR-AntonioNeural` (escolha da usuária) | não. Se o Edge cair um dia, o código deles mostra como plugar outra voz |
| legenda | SubMaker do Edge, corrigida por Whisper + distância de Levenshtein contra o roteiro | WordBoundary do Edge por beat (um áudio por fala, então não acumula erro) | não precisa: o nosso já é exato por beat |
| visual | vídeos de banco (Pexels/Pixabay) ou IA paga | 3D/2D desenhado por código | não (estilo pedido) |
| música | trilha de fundo | **sem música** (regra) | não |
| quantidade | `video_count` 1–5 versões por tema | 1 vídeo por pedido | **dá pra adaptar**: gerar 2 ganchos/capas do mesmo vídeo pra testar nos Reels de teste (verificador, "Dicas") |
| publicar | Upload-Post (API paga de terceiros) pra TikTok/Instagram/YouTube | não publica (a usuária posta) | opcional futuro: só por API oficial (Instagram Graph / TikTok Content Posting), nunca login da usuária |
| interface | WebUI + API REST | Estúdio Viral (artifact) + JSON | não |

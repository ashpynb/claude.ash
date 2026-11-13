# claude.ash — fábrica de vídeos virais

Tudo mora em skills (`.claude/skills/`), que carregam sozinhas em qualquer chat novo com este repo:

| Skill | O que faz |
|---|---|
| **fabrica-viral** | Do pedido ao MP4: regras da usuária, 5 moldes de roteiro, kit 3D, voz do Antônio, `video.py` (narrar → testar → render). Comece pelo `SKILL.md`. |
| serie-cubo-f2l | Série "Cubo mágico: F2L" (cubo em CSS sincronizado com a fala). |
| publicar-no-estudio | Grava ideias, vídeos e regras no Estúdio de Ideias. |
| assistir-youtube, watch | Ver vídeos de referência (YouTube via Gemini; TikTok/Instagram via yt-dlp). |
| roteiro-humor, comedy-writer, clean-comedy-rewrite, viral-hooks | Escrita engraçada e ganchos. |
| ig-* | Instagram: legenda, carrossel, plano, perfil… |
| anatomy | Figuras isométricas técnicas. |

Trabalho de cada vídeo: `trabalho/SLUG/` (criado por `video.py novo`; quadros, áudio e MP4 não vão pro git).
Vídeos antigos e referências em imagem continuam no histórico do git (antes do commit "Limpeza").

Pra levar pra outro projeto (ex.: Content Factory): copie a pasta `.claude/skills/fabrica-viral/`
inteira; ela é autossuficiente (ferramentas, kit, fontes, bibliotecas e exemplos dentro).

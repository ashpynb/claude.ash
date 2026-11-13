# Origem dos arquivos

| arquivo | de onde veio | licença |
|---|---|---|
| `SKILL.md` | escrito pra fábrica (2026-11-13). Rubrica de vídeo adaptada de `skills/review-video` de [DojoCodingLabs/remotion-superpowers](https://github.com/DojoCodingLabs/remotion-superpowers) (commit 970efd2); portões e regras da usuária são nossos | MIT (ideia) |
| `validar_roteiro.py` | escrito pra fábrica. Ideia dos asserts "duro/aviso" de [liyupi/niulai-video-generator](https://github.com/liyupi/niulai-video-generator) (`src/script/validate.ts`, `src/assert.ts`, commit cc60adb) | nosso |
| `retencao.py` | adaptado de `skills/yt-retention/retention.py` de [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) (commit a2feb21) | MIT, ver `LICENSE-youtube-agent-skill` |
| `hookscore.py` | cópia sem mudança de `skills/ig-reel/hookscore.py` de [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill) | MIT, ver `LICENSE-instagram-agent-skill` |

Nenhum script usa rede. Todos rodam com `python3 -I` (só biblioteca padrão; `qa.py`, na fabrica-viral, usa numpy e pillow).

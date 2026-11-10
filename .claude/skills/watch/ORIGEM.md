Fonte: https://github.com/bradautomates/claude-video (v0.3.2, commit 03ceb42), MIT. Instalada só a skill, sem o hook SessionStart.

## Configuração usada nesta nuvem
- `setup.py --engine local` e `--backend none --detail balanced`: nada sai da máquina, sem chave.
- Quando o vídeo não tem legenda, transcrever com o faster-whisper local, que já foi usado na ficha 01
  (modelo `small`, pt, passando o áudio como array: o `av` daqui não aceita `metadata_errors`).
- Rede: cada site precisa estar liberado no ambiente (TikTok + `v19-webapp-prime.us.tiktok.com` já estão).
  O YouTube responde com captcha (`google.com/sorry`) pra IPs de nuvem, e o Instagram ainda não está liberado.

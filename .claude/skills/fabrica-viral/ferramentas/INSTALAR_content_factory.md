# Estúdio Viral + Fábrica Viral — pacote para o Content Factory

Dois pedaços que trabalham juntos:

1. **`estudio-viral/index.html`**: a página onde a pessoa escolhe o tipo de vídeo, a ideia, o
   acabamento do 3D e o personagem. Um arquivo só, sem servidor (só usa Google Fonts, com fallback).
   Gera o **pedido** (texto) e os mesmos dados em **JSON**.
2. **`skills/`**: as skills que um Claude precisa pra transformar esse pedido em vídeo
   (roteiro com fatos conferidos → aprovação → narração → cenas 3D/2D → MP4).

## Skills (copie as 8 pastas pra `.claude/skills/` do repositório do Content Factory)

| Skill | Papel | Obrigatória? |
|---|---|---|
| `fabrica-viral` | O fluxo inteiro: regras, 5 tipos de vídeo, kit 3D, exemplos, `ferramentas/video.py` e `ferramentas/qa.py` | **sim** |
| `verificador-viral` | **Aprova o roteiro no lugar da usuária** (regras objetivas + gancho + nota ≥ 8,5), confere o MP4 (QA + rubrica) e lê a retenção depois de postar | **sim** |
| `roteiro-humor` | Escrever o roteiro engraçado e verdadeiro | sim (o fluxo usa) |
| `comedy-writer` | Técnicas de piada (usada pelo roteiro-humor) | sim |
| `clean-comedy-rewrite` | Filtro pra não ofender ninguém (usada pelo roteiro-humor) | sim |
| `viral-hooks` | Variações de gancho dos 3 primeiros segundos | sim |
| `ig-caption` | Legenda do post (onde vai o "marca aquele amigo") | sim |
| `assistir-youtube` | Ver vídeo de referência do YouTube (engenharia reversa) | opcional (precisa de chave do Gemini) |

Não vão no pacote (são deste projeto): `publicar-no-estudio` (grava no "Estúdio de Ideias", um
artifact específico), `serie-cubo-f2l`, as outras `ig-*`, `watch` e `anatomy`. Nenhuma das 8 depende delas
(o `hookscore.py` que o verificador usa vai copiado dentro dele).

## O que a máquina precisa
- Python 3.10+ e `pip install edge-tts soundfile numpy pillow`
- Node 18+ com Playwright e Chromium: `npm i playwright && npx playwright install chromium`
- `ffmpeg` no PATH
- Rede: a voz usa o Edge TTS da Microsoft (serviço não oficial, sem chave); a pesquisa de fatos usa
  busca na web. Atrás de proxy, o `narrar.py` usa `$HTTPS_PROXY`.
- Só pra `assistir-youtube`: chave do Gemini guardada como segredo (Bearer, host
  `generativelanguage.googleapis.com`). Nunca colar a chave no chat.
- Tudo de 3D (three.js r149, cannon-es, fonte Lilita One, modelos CC0) já vem dentro de
  `skills/fabrica-viral/ferramentas/` com as licenças.

## Como roda
1. A pessoa monta o pedido no Estúdio.
2. O Content Factory entrega o `pedido` (texto) a uma sessão do Claude com as skills instaladas.
3. O Claude escreve o roteiro (`trabalho/SLUG/roteiro.md`, com fontes e ⚠️ Conferir) e passa pelo
   **`verificador-viral`** (`video.py validar` + gancho pontuado + rubrica). Nota ≥ 8,5 → produz sem esperar;
   só pergunta à pessoa em crédito pago, tema sensível ou após 3 reprovações.
4. Aprovado: `python .claude/skills/fabrica-viral/ferramentas/video.py novo|narrar|testar|render SLUG`
   → `trabalho/SLUG/SLUG.mp4` (1080×1920, ~1:00–1:30, −14 LUFS, ~35 min de render com 4 processos).
   O render termina rodando o QA (`trabalho/SLUG/qa/relatorio.md` + `visao_geral.jpg`); com ✗ DURO, não entregar.
5. Depois de postar: curva de retenção → `verificador-viral/retencao.py` → uma lição nova no `regras.md`.

## Integração com a página
O Estúdio avisa quando a pessoa clica em **Copiar pedido** ou **Copiar como JSON**, de três jeitos:
- **Evento no documento**: `document.addEventListener('estudio-viral:pedido', e => e.detail)`
- **postMessage pro pai** (se estiver num `<iframe>`):
  `window.addEventListener('message', e => { if (e.data?.tipo === 'estudio-viral:pedido') usar(e.data.dados) })`
  (confira `e.origin` do seu lado).
- **Leitura direta**: `window.estudioViral.dados()` a qualquer momento.

Formato dos dados (versão 1):
```json
{
 "versao": 1, "origem": "estudio-viral",
 "tipo": "voce | construiu | ese | passo | flat2d",
 "tipo_nome": "E se tu…",
 "ideia": "ficasse 11 dias sem dormir",
 "frase": "E se tu ficasse 11 dias sem dormir",
 "estilo": "3D boneco de primitivas",
 "acabamento": "padrao | cinema | 2d",
 "estrutura": ["Gancho: …", "…"],
 "duracao_alvo": "1:15",
 "personagem": {"nome": "Sérgio", "pele": "#f1c08f", "cabelo": "curto", "corCabelo": "#3a2416",
                "roupa": "pijama", "corRoupa": "#3f6df2", "acessorio": "oculos", "cara": "feliz",
                "corpo": "normal", "descricao": "pele clara, cabelo curto…"},
 "skill": "fabrica-viral",
 "pedido": "Faz um vídeo viral do tipo \"E se tu…\": … (texto pronto pro Claude)"
}
```
`personagem` vem `null` nos tipos sem personagem (só "E se tu…" e "2D flat" têm).
A página guarda a última escolha no `localStorage` (`estudioViral3`) de quem está usando.

## Regras que o Claude segue (resumo de `fabrica-viral/regras.md`)
Voz Antônio a 3,2 palavras/s · 1:00 a 1:30 · sem música · título grande só nos 3 s iniciais ·
legenda de 1–3 palavras com palavra-chave amarela · um fato com fonte por frase · roteiro aprovado
antes de produzir · câmera aberta · camadas de texto testadas antes do render.

## Licenças
Skills de terceiros mantêm o `LICENSE`/`ORIGEM.md` na própria pasta. Bibliotecas e fonte em
`fabrica-viral/ferramentas/vendor/` (three.js MIT, cannon-es MIT, Lilita One OFL); modelos CC0 em
`fabrica-viral/ferramentas/modelos/LICENCAS.md`.

Gerado por `skills/fabrica-viral/ferramentas/empacotar.sh` (rode de novo pra atualizar o pacote).

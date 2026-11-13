#!/usr/bin/env bash
# Gera o pacote pro Content Factory: Estúdio Viral (página única) + as 8 skills necessárias + INSTALAR.md.
# Uso (na raiz do repo): bash .claude/skills/fabrica-viral/ferramentas/empacotar.sh [saida.zip]
set -euo pipefail
RAIZ=$(git rev-parse --show-toplevel); cd "$RAIZ"
SK=.claude/skills; F=$SK/fabrica-viral/ferramentas; OUT=${1:-pacote-content-factory.zip}
TMP=$(mktemp -d); P=$TMP/pacote-content-factory; mkdir -p "$P/estudio-viral" "$P/skills"
{ printf '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  printf '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>\n</head><body>\n'
  cat "$F/estudio_viral.html"; printf '\n</body></html>\n'; } > "$P/estudio-viral/index.html"
for s in fabrica-viral verificador-viral roteiro-humor comedy-writer clean-comedy-rewrite viral-hooks ig-caption assistir-youtube; do cp -r "$SK/$s" "$P/skills/"; done
cp "$F/INSTALAR_content_factory.md" "$P/INSTALAR.md"; cp "$F/MUDANCAS_content_factory.md" "$P/MUDANCAS.md"
find "$P" -name __pycache__ -prune -exec rm -rf {} +
# confere antes de zipar: toda skill tem SKILL.md com name/description e todo .py compila
for d in "$P"/skills/*/; do head -5 "$d/SKILL.md" | grep -q '^name:' && head -8 "$d/SKILL.md" | grep -q '^description:' || { echo "SKILL.md inválido em $d"; exit 1; }; done
find "$P" -name '*.py' -print0 | xargs -0 -n1 python3 -m py_compile && find "$P" -name __pycache__ -prune -exec rm -rf {} +
(cd "$TMP" && zip -qr - pacote-content-factory) > "$OUT"; rm -rf "$TMP"
echo "Pacote: $OUT ($(du -h "$OUT" | cut -f1))"

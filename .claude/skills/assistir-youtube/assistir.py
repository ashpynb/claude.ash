"""Pede pro Gemini (Google) assistir um vídeo do YouTube e responder uma pergunta.

Uso: python3 assistir.py URL "pergunta" [--modelo gemini-3-flash-preview]

Por que existe: o YouTube bloqueia downloads vindos desta nuvem (captcha google.com/sorry).
Aqui quem busca o vídeo é o servidor do Google. Usa o endpoint compatível com OpenAI do Gemini
porque ele aceita a chave em "Authorization: Bearer", que é o formato da network secret salva
no ambiente para generativelanguage.googleapis.com. O proxy injeta a chave real; este script
manda só um marcador ("proxy-injected") e nunca vê a chave.
"""
import argparse, json, os, ssl, sys, urllib.request, urllib.error

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("pergunta")
    ap.add_argument("--modelo", default=os.environ.get("ASSISTIR_MODELO", "gemini-3-flash-preview"))
    a = ap.parse_args()
    corpo = {"model": a.modelo, "messages": [{"role": "user", "content": [
        {"type": "text", "text": a.pergunta},
        {"type": "image_url", "image_url": {"url": a.url}}]}]}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(corpo).encode(), method="POST", headers={
        "Content-Type": "application/json", "Authorization": "Bearer proxy-injected"})
    ca = os.environ.get("SSL_CERT_FILE") or ("/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
    ctx = ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=600, context=ctx) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Gemini HTTP {e.code}: {e.read().decode(errors='replace')[:600]}")
    d = d[0] if isinstance(d, list) else d
    print(d["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()

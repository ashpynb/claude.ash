#!/usr/bin/env python3
"""Fábrica viral: do roteiro aprovado ao MP4 com um comando por etapa.

  python video.py novo   SLUG [--de EXEMPLO]   cria trabalho/SLUG (cena.html, falas.txt, links pro kit)
  python video.py narrar SLUG [--alvo 3.2]     falas.txt -> voz do Antônio, acerta o ritmo, gera tempo.js
  python video.py testar SLUG                  2 quadros por beat + checagem das camadas CSS + folha de contato
  python video.py render SLUG [-j 4]           quadros em paralelo + efeitos sonoros + MP4 (-14 LUFS) + QA automático
  python video.py validar SLUG --molde voce    regras objetivas do roteiro (skill verificador-viral)
  python video.py qa SLUG                      QA do MP4: formato, volume, silêncio, quadro preto/parado, sincronia

SLUG: nome curto sem espaço (ex.: viral10_polvo). EXEMPLO: pasta em exemplos/ (ex.: viral09).
Tudo fica em <raiz do repo>/trabalho/SLUG (quadros, áudio e MP4 não vão pro git).
Dependências: pip install edge-tts soundfile numpy pillow ; node + playwright (já vêm na nuvem) ; ffmpeg.
"""
import argparse, functools, http.server, json, os, re, shutil, socketserver, subprocess, sys, threading
from pathlib import Path

FERR = Path(__file__).resolve().parent
SKILL = FERR.parent


def raiz():
    try:
        return Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True, stderr=subprocess.DEVNULL).strip())
    except Exception:
        return Path.cwd()


def pasta(slug):
    p = raiz() / 'trabalho' / slug
    if not p.exists():
        sys.exit(f'Não existe {p}. Rode: python video.py novo {slug}')
    return p


# ---------------------------------------------------------------- novo
def novo(a):
    p = raiz() / 'trabalho' / a.slug
    p.mkdir(parents=True, exist_ok=True)
    gi = raiz() / 'trabalho' / '.gitignore'
    if not gi.exists():
        gi.write_text('*/quadros/\n*/teste/\n*/voz/\n*.wav\n*.mp4\n*.jpg\n*/kit3d.js\n*/vendor\n*/modelos\n')
    for nome in ('kit3d.js', 'vendor', 'modelos'):
        dst = p / nome
        if not dst.exists():
            dst.symlink_to(os.path.relpath(FERR / nome, p))
    src = SKILL / 'exemplos' / a.de / 'cena.html' if a.de else FERR / 'modelo_cena.html'
    if not (p / 'cena.html').exists():
        shutil.copy(src, p / 'cena.html')
    if a.de and (SKILL / 'exemplos' / a.de / 'tempo.js').exists() and not (p / 'tempo.js').exists():
        shutil.copy(SKILL / 'exemplos' / a.de / 'tempo.js', p / 'tempo.js')
    if not (p / 'falas.txt').exists():
        (p / 'falas.txt').write_text('Uma frase por linha. Cada linha vira um beat (uma cena).\n')
    print(f'Pronto: {p}\n  1) escreva as falas aprovadas em falas.txt (uma por linha)\n  2) python video.py narrar {a.slug}\n  3) monte as cenas em cena.html\n  4) python video.py testar {a.slug}  5) python video.py render {a.slug}')


# ---------------------------------------------------------------- narrar
def montar_tempo(p, falas, resp=0.12, fim=0.6):
    import numpy as np, soundfile as sf
    voz = p / 'voz'
    tempos = json.load(open(voz / 'tempos.json'))
    SR = 24000
    partes, beats, t = [], [], 0.0
    for i, f in enumerate(falas):
        k = 'b%02d' % i
        x, _ = sf.read(voz / f'{k}.wav')
        d = len(x) / SR + resp
        beats.append({'t0': round(t, 3), 't1': round(t + d, 3), 'fala': f,
                      'words': [{'w': w['w'], 't0': round(t + w['t0'], 3), 't1': round(t + w['t1'], 3)} for w in tempos[k]['palavras']]})
        partes += [x, np.zeros(int(resp * SR))]
        t += d
    total = round(t + fim, 3)
    partes.append(np.zeros(int(fim * SR)))
    sf.write(p / 'narracao.wav', np.concatenate(partes), SR)
    (p / 'tempo.js').write_text('window.TEMPO=' + json.dumps({'total': total, 'beats': beats}, ensure_ascii=False) + ';\n')
    n = sum(len(f.split()) for f in falas)
    return total, n


def narrar(a):
    p = pasta(a.slug)
    falas = [l.strip() for l in (p / 'falas.txt').read_text().splitlines() if l.strip() and not l.startswith('Uma frase por linha')]
    if not falas:
        sys.exit('falas.txt está vazio.')
    rate = a.rate
    for tentativa in range(4):
        json.dump([{'id': 'b%02d' % i, 'texto': f, 'rate': f'{rate:+d}%', 'gap': 0.09} for i, f in enumerate(falas)],
                  open(p / 'falas.json', 'w'), ensure_ascii=False, indent=1)
        r = subprocess.run([sys.executable, str(FERR / 'narrar.py'), str(p / 'falas.json'), str(p / 'voz'), f'{rate:+d}%', '0.09'], capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stderr[-1500:])
        total, n = montar_tempo(p, falas)
        ps = n / total
        print(f'rate {rate:+d}%  ->  {n} palavras, {total:.1f} s, {ps:.2f} palavras/s')
        if abs(ps - a.alvo) <= 0.05:
            break
        rate = int(round(rate + (a.alvo / ps - 1) * 160))
    m, s = divmod(total, 60)
    aviso = '' if 60 <= total <= 90 else '   ⚠️ fora de 1:00–1:30: ajuste o roteiro (nunca a velocidade)'
    print(f'OK: {int(m)}:{s:04.1f} a {ps:.2f} p/s{aviso}\n  tempo.js e narracao.wav em {p}')


# ---------------------------------------------------------------- servidor + render
class _Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


def servir(p):
    h = functools.partial(_Quieto, directory=str(p))
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h)
    s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, f'http://127.0.0.1:{s.server_address[1]}/cena.html'


def folha(imgs, saida, colunas=7, w=180, h=320):
    from PIL import Image
    if not imgs:
        return
    linhas = (len(imgs) + colunas - 1) // colunas
    c = Image.new('RGB', (w * colunas, h * linhas))
    for i, f in enumerate(imgs):
        c.paste(Image.open(f).resize((w, h)), ((i % colunas) * w, (i // colunas) * h))
    c.save(saida, quality=85)


def testar(a):
    p = pasta(a.slug)
    (p / 'teste').mkdir(exist_ok=True)
    s, url = servir(p)
    try:
        r = subprocess.run(['node', str(FERR / 'teste_css.js'), url, str(p / 'teste' / 'b')], text=True, capture_output=True, timeout=1800)
    finally:
        s.shutdown()
    print((r.stdout + r.stderr).strip()[-3000:])
    imgs = sorted((p / 'teste').glob('b*.jpg'))
    folha(imgs, p / 'teste' / 'folha.jpg', colunas=6, w=270, h=480)
    print(f'Folha de contato: {p / "teste" / "folha.jpg"} (olhe ANTES do render: câmera aberta, personagem inteiro, nada cortado)')


def render(a):
    p = pasta(a.slug)
    q = p / 'quadros'
    if a.limpar and q.exists():
        shutil.rmtree(q)
    q.mkdir(exist_ok=True)
    total = json.loads(re.sub(r'^window\.TEMPO=|;\s*$', '', (p / 'tempo.js').read_text().strip()))['total']
    n = round(total * 30)
    s, url = servir(p)
    try:
        passo = (n + a.j - 1) // a.j
        procs = [subprocess.Popen(['node', str(FERR / 'render.js'), url, str(q), str(k * passo), str((k + 1) * passo)]) for k in range(a.j)]
        erros = [pr.wait() for pr in procs]
    finally:
        s.shutdown()
    if any(erros) or len(list(q.glob('f*.jpg'))) < n:
        sys.exit(f'Render incompleto ({len(list(q.glob("f*.jpg")))}/{n} quadros). Rode de novo: os quadros prontos são pulados.')
    subprocess.run([sys.executable, str(FERR / 'mix.py'), str(p / 'narracao.wav'), str(q / 'eventos.json'), str(p / 'mix.wav')], check=True)
    mp4 = p / f'{a.slug}.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '30', '-i', str(q / 'f%05d.jpg'), '-i', str(p / 'mix.wav'),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-maxrate', '9M', '-bufsize', '18M', '-pix_fmt', 'yuv420p',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=7', '-ar', '48000',
                    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(mp4)], check=True)
    folha([q / f'f{i:05d}.jpg' for i in range(15, n, max(1, n // 28))][:28], p / 'folha_final.jpg')
    print(f'MP4: {mp4} ({mp4.stat().st_size / 1e6:.1f} MB)\nFolha final: {p / "folha_final.jpg"} (confira antes de enviar)')
    qa(a)


# ---------------------------------------------------------------- verificador
def validar(a):
    p = pasta(a.slug)
    v = SKILL.parent / 'verificador-viral' / 'validar_roteiro.py'
    if not v.exists():
        sys.exit('Skill verificador-viral não instalada (falta validar_roteiro.py).')
    r = subprocess.run([sys.executable, '-I', str(v), str(p / 'falas.txt'), '--molde', a.molde])
    sys.exit(r.returncode)


def qa(a):
    p = pasta(a.slug)
    mp4 = p / f'{a.slug}.mp4'
    if not mp4.exists():
        sys.exit(f'Não achei {mp4}. Rode o render primeiro.')
    cmd = [sys.executable, '-I', str(FERR / 'qa.py'), str(mp4), '--saida', str(p / 'qa')]
    if (p / 'tempo.js').exists():
        cmd += ['--tempo', str(p / 'tempo.js')]
    r = subprocess.run(cmd)
    if r.returncode:
        print('⚠️  QA reprovou: conserte os erros duros antes de enviar (skill verificador-viral, portão 2).')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    x = sp.add_parser('novo'); x.add_argument('slug'); x.add_argument('--de', help='começar de um exemplo (pasta em exemplos/)'); x.set_defaults(f=novo)
    x = sp.add_parser('narrar'); x.add_argument('slug'); x.add_argument('--alvo', type=float, default=3.2); x.add_argument('--rate', type=int, default=10); x.set_defaults(f=narrar)
    x = sp.add_parser('testar'); x.add_argument('slug'); x.set_defaults(f=testar)
    x = sp.add_parser('render'); x.add_argument('slug'); x.add_argument('-j', type=int, default=4); x.add_argument('--limpar', action='store_true', help='apaga quadros antigos'); x.set_defaults(f=render)
    x = sp.add_parser('validar'); x.add_argument('slug'); x.add_argument('--molde', default='livre', choices=['voce', 'construiu', 'ese', 'passo', 'flat2d', 'livre']); x.set_defaults(f=validar)
    x = sp.add_parser('qa'); x.add_argument('slug'); x.set_defaults(f=qa)
    a = ap.parse_args(); a.f(a)

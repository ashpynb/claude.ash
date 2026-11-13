# Voz e som

## Voz (escolha da usuária)
- Edge TTS **`pt-BR-AntonioNeural`** (preferida a vozes clonadas e às femininas do Edge).
- O Antônio cru fala ~2,1 p/s porque faz pausas de ~0,85 s entre frases. O `narrar.py` gera **um
  áudio por beat**, corta as pausas internas pra no máximo 0,09 s e devolve o tempo de cada palavra
  (`WordBoundary`). O `video.py narrar` junta tudo com 0,12 s de respiro entre beats e ajusta o
  `rate` até dar **3,2 ± 0,05 p/s** (costuma ficar entre +7% e +22%).
- A cena dura o tempo real da fala de cada beat; a legenda acende palavra por palavra.
- A usuária confere a pronúncia (eu não ouço): avise quando houver palavra difícil (siglas, nomes
  estrangeiros, "megawatts").

## Efeitos (ferramentas/mix.py, todos sintetizados, sem arquivos de terceiros)
`whoosh` (todo corte, automático) · `pop` (algo aparece) · `boing`/`boing2` (queda, pulo) ·
`tic` (relógio, número) · `tchan` (virada, PARTE 2) · `sino` (descoberta) · `queda`/`queda2`
(número caindo) · `tum` (impacto) · `marreta` · `buzz` (erro/negação) · `flip` (folhas) ·
`pipoca` (várias coisas caindo) · `zum` (tontura) · `splash`/`splash2` (água) · `cava` · `tremor` ·
`chuva` · `alarme` · `motor` · `whoosh2` · `bolhas`.
Na cena: `ev(segundo,'tipo')`; o segundo de uma palavra é `palavra(beat,'palavra')`.
Hit na pausa logo depois da palavra. **Sem música.** Tipo novo: escreva a função e o ganho em `mix.py`.

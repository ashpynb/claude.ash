# Viral 02: Maca improvisada com 2 paus e 1 cobertor (1:11, 9:16, 3D)

Vídeo **sem voz**: a legenda conta tudo (texto grande + frase palavra a palavra), com trilha e efeitos.
A coluna "fala" serve para gravar narração depois, se quiser (o tempo já bate).

## Ganchos (hookscore.py, versão em inglês)
| nota | gancho (PT) | fórmula |
|---|---|---|
| 85,6 FORTE | "Nunca carregue um amigo machucado no colo. Faça isso." | Comando negativo. **Descartado:** "nunca" é forte demais, porque carregar no colo existe em primeiros socorros |
| **83,0 FORTE ✅** | "Calma. Dois paus e um cobertor carregam seu amigo." | Contradição + específico |
| 62,6 OK | "Sem corda, sem prego. Só um cobertor." | Negação. **Descartado:** a versão em inglês trazia um "80 kg" que não conferi |
| 57,0 OK | "Dois cabos de vassoura e um cobertor aguentam seu amigo." | Específico |
| 37,8 WEAK | "Se seu amigo desmaiar na trilha, você saberia carregar ele?" | Pergunta |

O pontuador foi feito pra inglês, então a nota vale só como referência.

## Posturas virais aplicadas
- **Primeiro quadro:** a maca já pronta, sendo erguida com 4 pessoas (começa no meio da ação), com o gancho na tela.
- **Começo sem enrolação:** nada de "oi"; o gancho é a primeira frase.
- **Corte e movimento:** muda o enquadramento a cada 3–6s, com punch-in, deriva contínua de câmera, tremida e flash nos impactos.
- **Texto na tela:** no máximo 6 palavras, dentro da área segura (y 230–1440, 250 px livres à direita). Legenda palavra a palavra, pra quem assiste sem som.
- **Barra de progresso** no topo e **passos 1/5 a 5/5**, que seguram a retenção.
- **Um pedido só:** "Manda pra quem faz trilha com você".
- **Loop:** termina com o mesmo texto e o mesmo enquadramento do gancho ("2 PAUS + 1 COBERTOR").

## Roteiro
| tempo | texto grande | fala / legenda | 3D |
|---|---|---|---|
| 0–3s | 2 PAUS + 1 COBERTOR | Calma. Dois paus e um cobertor carregam seu amigo. | maca pronta sendo erguida (cold open) |
| 3–7s | ANTES: REGRA DE OURO | Mas antes, uma regra que salva vidas. | pessoa caída no chão |
| 7–13s | COLUNA? NÃO MEXA | Se pode ter batida na cabeça, no pescoço ou na coluna, não mexa. Liga cento e noventa e dois. | close no pescoço com anel vermelho; card **192** e ✕ |
| 13–17s | SÓ SE FOR PERIGOSO | Só move se ficar ali for mais perigoso, ou se o socorro não consegue chegar. | câmera orbita |
| 17–22s | PASSO 1: DOIS PAUS | Passo um: dois paus fortes, mais compridos que a pessoa. | paus caem no chão |
| 22–27s | 1/3 DO COBERTOR | Abre o cobertor no chão e põe o primeiro pau a um terço da largura. | cobertor abre e linhas marcam os terços |
| 27–32s | DOBRA POR CIMA | Dobra esse terço por cima do pau. | 1ª dobra animada |
| 32–38s | 2º PAU NA DOBRA | Põe o segundo pau em cima da dobra, mais ou menos na largura dos ombros. | 2º pau cai na dobra |
| 38–43s | DOBRA O RESTO | Agora dobra o resto do cobertor por cima de tudo. | 2ª dobra |
| 43–49s | O PESO TRAVA O PANO | O segredo: o peso da pessoa prende o pano. Sem nó e sem prego. | pessoa deita, seta de peso |
| 49–53s | TESTA ANTES | Testa antes com alguém que não está machucado. | ✓ verde |
| 53–58s | SEM COBERTOR? JAQUETAS | Sem cobertor? Duas ou três jaquetas fechadas, mangas pra dentro, e os paus passam pelas mangas. | jaquetas caem, paus deslizam |
| 58–64s | LEVANTA NO 3 | Pra carregar: um em cada canto, costas retas, e todo mundo levanta junto na contagem. | 4 pessoas, contagem 1-2-3-JÁ!, maca sobe |
| 64–68s | MANDA PRO SEU GRUPO | Agora você sabe. Manda pra quem faz trilha com você. | caminham com a maca |
| 68–71s | 2 PAUS + 1 COBERTOR | E lembra: calma. Dois paus e um cobertor. | mesmo enquadramento do gancho (loop) |

## Base (primeiros socorros)
- Maca de cobertor: pau a 1/3, dobra por cima, 2º pau sobre a dobra, dobra o resto. O peso da vítima prende o pano por atrito. É o método clássico de maca improvisada dos manuais militares e de primeiros socorros.
- Maca de jaquetas/camisas: fechadas, mangas pra dentro, paus pelas mangas.
- Regra de segurança: suspeita de lesão na cabeça, no pescoço ou na coluna = não mover e chamar o SAMU (192), a menos que haja perigo imediato.

## ⚠️ Conferir antes de postar
- Distância entre os paus "na largura dos ombros": é uma aproximação didática. Ajuste ao tamanho da pessoa.
- O vídeo não ensina a imobilizar a coluna. Se quiser, coloque na legenda: "isso não substitui curso de primeiros socorros".
- Bombeiros = 193. O vídeo cita só o SAMU (192), pra não confundir.

## Arquivos
- `anim/maca3d/index.html`: cena 3D (three.js). Sem `?gravar`, toca a prévia ao vivo (precisa de servidor local: `python3 -m http.server` dentro de `anim/maca3d`).
- `anim/maca3d/timeline.json`: beats, textos e câmera.
- `anim/maca3d/audio.py`: trilha e efeitos sintetizados (sem samples de terceiros).
- `out/viral02_maca.mp4`: vídeo final.

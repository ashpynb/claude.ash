# Ficha 02: "Como Fazer Shorts Animados Virais com IA Usando o Claude" (YouTube, Matheus Celtic)

Analisado em 2026-11-10 pela skill `assistir-youtube` (**quem assistiu foi o Gemini do Google**;
métricas são a descrição dele, não medição por quadro). Só técnica: não copiar falas nem imagens.

## Básico
- ~5:01, tutorial. Gancho (0–5s): "Olha esses dois vídeos. Esse aqui tem 29 milhões de views. E o
  canal por trás dele ainda é novo." Na tela: dois Shorts lado a lado + "10M Views"/"29M Views" e a
  página do canal → **gancho de prova social com número grande**.

## Método que ele ensina (minutagem do Gemini)
- 00:36 **Treinar com referência**: dar ~20 vídeos do estilo e pedir regras EXATAS por quadro
  (ex.: contorno de 3px, personagem com 3,5 cabeças de altura).
- 01:27 **Roteiro na fórmula viral**: gancho com paradoxo → cenário → escalada → virada.
- 01:53 **Visual em 5 camadas**, cada uma com um "agente" e arquivo próprio: câmera, mundo,
  materiais, personagens, acabamento (`story.ts`, `world.ts`…). Um **verificador dá nota 0–10**
  comparando com a referência até ficar bom.
- 02:30 **Render** com Remotion (`npm install`, `npx remotion render`), GPU dedicada no Windows.

## O vídeo de exemplo (história de José no Egito)
- **Híbrido**: cenários 3D + personagens 2D "flat bean-head" com contorno preto grosso; cores
  saturadas; luz muda com a hora do dia.
- Ritmo muito rápido: imagem muda a cada frase; cortes secos sincronizados com a fala;
  câmera deslizando pelo cenário 3D (profundidade).
- Narração masculina de contação de história, direta, levemente sarcástica.

## Comparação com o que já fazemos
| ele | nós |
|---|---|
| Remotion (React → vídeo) | three.js / CSS 3D + Playwright + ffmpeg (mesma ideia: código → quadros) |
| regras exatas por quadro da referência | `analisar-video-referencia` + `aprendizados.md` |
| verificador com nota 0–10 | folhas de contato revisadas a olho (sem nota) |
| personagens 2D sobre cenário 3D | tudo 3D cartoon |

## Dá pra aplicar
1. **Verificador com nota 0–10** antes do render final (critérios do `aprendizados.md`).
2. Testar **personagem 2D com contorno grosso em cenário 3D** como variação do 3D cartoon (pedir à usuária).
3. Fórmula de roteiro **paradoxo → cenário → escalada → virada** nos vídeos de fatos gerais.
4. **Câmera deslizando** entre cenas em vez de só cortes secos.

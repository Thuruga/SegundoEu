---
status: complete
---

# Quick Task: Ênfase no Scriptwriter e Atualização de Estado

**Objetivo:** Adicionar tipagem para múltiplos caminhos de vídeo (`video_paths`) no estado global da aplicação e ensinar a IA a gerar guiões mais dinâmicos (com asteriscos para ênfase vocal) e com descrições de cenas ricas e distintas.

## Alterações Realizadas
- `src/state.py`: O campo `video_path` foi alterado de `Optional[str]` para `video_paths: Optional[List[str]]` a fim de suportar as múltiplas cenas solicitadas.
- `src/agents/scriptwriter.py`: 
  - Adicionada uma nova regra estrita exigindo a marcação de palavras de ênfase (ex: `*palavra*`). O exemplo embutido no prompt foi atualizado com itálicos/asteriscos pontuais para forçar este comportamento.
  - A geração da tag `<keywords>` foi reformulada. Agora exige explicitamente **3 a 4 conceitos visuais abstratos e totalmente distintos** em inglês para suportar diferentes cenas (B-rolls) num único vídeo (ex: `abandoned clock tower, stormy ocean waves, dying candle flame, cracked desert earth`).

---
status: complete
---

# Quick Task: Atualização Tipográfica no Video Editor

**Objetivo:** Ajustar as constantes de tipografia (`FONT_SIZE`, `STROKE_WIDTH` e `SUBTITLE_Y`) no topo do ficheiro `src/agents/video_editor.py` e garantir a importação de `ColorClip`.

## Alterações Realizadas
- Atualização da constante `FONT_SIZE` para `65`.
- Atualização da constante `STROKE_WIDTH` para `4`.
- Atualização da posição vertical das legendas (`SUBTITLE_Y`) para `int(OUTPUT_HEIGHT * 0.60)`, elevando a legenda para 60% da altura do ecrã.
- Verificou-se que `ColorClip` já estava corretamente importado do módulo `moviepy`.

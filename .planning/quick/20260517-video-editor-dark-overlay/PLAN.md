---
status: incomplete
---

<description>
Fazer duas alterações estéticas profundas em `src/agents/video_editor.py`:
1. Atualizar constantes de fonte (FONT_PATH='assets/fonts/Montserrat-Black.ttf', FONT_SIZE=90, STROKE_WIDTH=8).
2. Criar máscara de escurecimento (dark_overlay) com ColorClip preto, opacidade 0.35, e duração total, posicionada entre bg_cropped e subtitle_clips em all_layers.
</description>

<tasks>
1. Importar `ColorClip` de `moviepy`.
2. Verificar e garantir as constantes no topo do ficheiro.
3. Adicionar `dark_overlay` na função `assemble_video` logo após `bg_cropped.with_fps`.
4. Atualizar `all_layers = [bg_cropped, dark_overlay] + subtitle_clips`.
5. Verificar a sintaxe do ficheiro e atualizar o STATE.md.
</tasks>

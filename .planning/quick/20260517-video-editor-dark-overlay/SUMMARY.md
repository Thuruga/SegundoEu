---
status: complete
---

# Quick Task: Alterações Estéticas e Dark Overlay no Video Editor

**Objetivo:** Atualizar constantes de fonte para Montserrat-Black e adicionar máscara de escurecimento (dark overlay) entre o vídeo de fundo e as legendas.

## Alterações Realizadas
- Atualização e verificação das constantes no topo de `src/agents/video_editor.py` (`FONT_PATH = "./assets/fonts/Montserrat-Black.ttf"`, `FONT_SIZE = 90`, `STROKE_WIDTH = 8`).
- Importação da classe `ColorClip` da biblioteca `moviepy`.
- Criação da instância `dark_overlay` utilizando `ColorClip` na cor preta `[0, 0, 0]`, com opacidade `0.35` e duração igual à da locução.
- Inserção do `dark_overlay` na lista `all_layers`, posicionando-o entre o `bg_cropped` e os `subtitle_clips` para escurecer o fundo de forma elegante e manter o destaque brilhante das legendas.

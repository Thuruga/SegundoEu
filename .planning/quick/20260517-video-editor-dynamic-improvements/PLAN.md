---
status: incomplete
---

<description>
Implementar três melhorias dinâmicas de edição no `video_editor.py`:
1. Concatenar múltiplos vídeos (`video_paths`) sequencialmente e aplicar loop caso o vídeo resultante seja mais curto que o áudio.
2. Renderizar legendas palavra por palavra no Pillow, pintando a amarelo as palavras marcadas com `*asteriscos*` (e removendo os asteriscos).
3. Inserir efeitos sonoros (SFX) em momentos de ênfase (quando a legenda contém um asterisco), misturando-os no áudio final.
</description>

<tasks>
1. Atualizar a importação e o carregamento do vídeo para iterar sobre `state["video_paths"]`, aplicar `crop_to_fill` em cada um, usar `concatenate_videoclips` e, se necessário, `vfx.Loop`.
2. Reescrever `_render_subtitle_frame` no `video_editor.py` para calcular larguras palavra por palavra, desenhar de forma sequencial com controlo de cor e suporte a asteriscos.
3. Adicionar lógica de SFX: procurar `.mp3` em `assets/sfx/`. Ao ler o SRT, se houver um `*`, adicionar um AudioFileClip do SFX no mesmo `start_time`. Compor todos os SFX junto com a voz (e música, se houver) usando `CompositeAudioClip`.
4. Verificar sintaxe e testar (se aplicável).
5. Escrever SUMMARY.md, atualizar STATE.md e submeter (commit/push).
</tasks>

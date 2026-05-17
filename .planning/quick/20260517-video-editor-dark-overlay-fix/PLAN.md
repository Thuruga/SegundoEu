---
status: incomplete
---

<description>
Corrigir e centralizar a criação do `dark_overlay` e a composição de `all_layers` na função `assemble_video` de `src/agents/video_editor.py`, conforme solicitado pelo utilizador.
</description>

<tasks>
1. Remover as instâncias avulsas/deslocadas de `dark_overlay` e `all_layers` causadas por edições do utilizador no IDE.
2. Declarar `dark_overlay` logo acima da secção final 6 (onde as camadas são unidas para o `CompositeVideoClip`).
3. Atualizar a variável `all_layers` imediatamente a seguir para garantir a ordem correta: `[bg_cropped, dark_overlay] + subtitle_clips`.
4. Verificar a sintaxe com `py_compile`.
5. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>

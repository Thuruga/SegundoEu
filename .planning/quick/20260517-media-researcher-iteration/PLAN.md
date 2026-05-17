---
status: incomplete
---

<description>
Alterar a lógica do agente `media_researcher.py` para iterar sobre cada keyword fornecida, descarregando um vídeo HD vertical para *cada* uma delas, em vez de concatenar todas numa única pesquisa. Salvar os caminhos na nova propriedade `video_paths` do state.
</description>

<tasks>
1. Modificar o loop principal em `src/agents/media_researcher.py` para iterar sobre a lista `agent_keywords`.
2. Para cada keyword, testar o `search_chain` (incluindo fallbacks), fazer download do vídeo correspondente (adicionando um índice ao nome do ficheiro para não haver sobrescrita) e adicioná-lo à lista `downloaded_paths`.
3. Substituir `new_state["video_path"]` por `new_state["video_paths"] = downloaded_paths`.
4. Verificar sintaxe.
5. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>

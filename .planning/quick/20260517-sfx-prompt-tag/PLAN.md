---
status: incomplete
---

<description>
Adicionar campos `sfx_prompt` e `sfx_path` ao VideoState e ensinar o Scriptwriter a gerar uma tag `<sfx>` com um prompt para efeitos sonoros cinematográficos.
</description>

<tasks>
1. Adicionar `sfx_prompt: Optional[str]` e `sfx_path: Optional[str]` em `src/state.py`.
2. Atualizar as STRICT RULES no prompt do `src/agents/scriptwriter.py` para exigir a tag `<sfx>`.
3. Atualizar o EXEMPLO de In-Context Learning com a nova tag.
4. Adicionar regex para extrair `<sfx>` e guardar em `new_state["sfx_prompt"]`.
5. Verificar sintaxe.
6. Criar SUMMARY.md, atualizar STATE.md e commit/push.
</tasks>

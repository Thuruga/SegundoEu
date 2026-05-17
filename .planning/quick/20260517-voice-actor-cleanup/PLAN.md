---
status: incomplete
---

<description>
Remover o bloco de código legado/duplicado de geração de legendas em `src/agents/voice_actor.py` que estava a sobrescrever o novo ficheiro SRT gerado pela lógica baseada em silêncios (gaps).
</description>

<tasks>
1. Remover as linhas 124 a 155 de `src/agents/voice_actor.py` (lógica antiga de agrupamento por pontuação/contagem).
2. Verificar a sintaxe com `py_compile`.
3. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>

---
status: incomplete
---

<description>
Alterar as STRICT RULES em `src/agents/scriptwriter.py`:
1. Reforçar que o roteiro DEVE ter entre 120 a 140 palavras no total (Regra 3).
2. Ajustar as quebras de linha (Regra 5) para agrupar de 2 a 5 palavras sem encurtar o tamanho total da história.
</description>

<tasks>
1. Atualizar o `ChatPromptTemplate` em `src/agents/scriptwriter.py` para modificar a Regra 3 (120-140 palavras) e a Regra 5 (2-5 palavras sem encurtar a história).
2. Verificar a sintaxe do ficheiro com `py_compile`.
3. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>

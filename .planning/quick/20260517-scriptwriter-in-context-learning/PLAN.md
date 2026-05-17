---
status: incomplete
---

<description>
Implementar In-Context Learning no `src/agents/scriptwriter.py`. Substituir o 'system' prompt para:
1. Exigir idioma pt-BR.
2. Exigir tamanho entre 120 e 140 palavras.
3. Exigir uso frequente de vírgulas (a cada 3-4 palavras) para ditar o ritmo das legendas.
4. Adicionar 'EXEMPLO DO PADRÃO DE ESCRITA ESPERADO' mostrando um texto filosófico com muitas vírgulas e keywords dark/moody/minimalist.
</description>

<tasks>
1. Atualizar o `ChatPromptTemplate` em `src/agents/scriptwriter.py` com o novo system prompt e In-Context Learning.
2. Verificar a sintaxe do ficheiro com `py_compile`.
3. Criar SUMMARY.md, atualizar STATE.md e fazer commit/push.
</tasks>

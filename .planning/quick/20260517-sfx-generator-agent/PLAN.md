---
status: incomplete
---

<description>
Criar novo agente `src/agents/sfx_generator.py` que utiliza a API de inferência do HuggingFace (modelo `audioldm-s`) para gerar efeitos sonoros cinematográficos a partir do `sfx_prompt` gerado pelo Scriptwriter. Gracioso em caso de falha.
</description>

<tasks>
1. Criar `src/agents/sfx_generator.py` com a função `generate_sfx(state) -> VideoState`.
2. Ler `sfx_prompt` do state e `HF_API_KEY` do env.
3. POST para `https://api-inference.huggingface.co/models/cvssp/audioldm-s` com o prompt.
4. Gravar o áudio em `assets/sfx/` com timestamp.
5. Tratamento gracioso de erros (sem quebrar o pipeline).
6. Verificar sintaxe.
7. SUMMARY.md, STATE.md, commit/push.
</tasks>

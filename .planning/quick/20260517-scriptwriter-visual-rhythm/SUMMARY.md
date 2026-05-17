---
status: complete
---

# Quick Task: Atualização do Ritmo Visual e Keywords no Scriptwriter

**Objetivo:** Adicionar regra para quebras de linha (\n) ditando o ritmo visual das legendas (1 a 4 palavras) e exigir conceitos dark/moody/minimalist para a busca de B-roll.

## Alterações Realizadas
- Atualização da secção `STRICT RULES` no ficheiro `src/agents/scriptwriter.py`.
- Adição da regra 5 exigindo formatação com quebras de linha explícitas para ritmo visual das legendas.
- Modificação das instruções da tag `<keywords>` proibindo termos literais e solicitando conceitos fotográficos de estilo dark/moody/minimalist.

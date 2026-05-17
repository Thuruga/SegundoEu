---
status: complete
---

# Quick Task: Ajuste de Contagem de Palavras e Ritmo no Scriptwriter

**Objetivo:** Reforçar a exigência de 120 a 140 palavras no roteiro (Regra 3) e o agrupamento de 2 a 5 palavras por linha sem encurtar a história (Regra 5).

## Alterações Realizadas
- Atualização da secção `STRICT RULES` no ficheiro `src/agents/scriptwriter.py`.
- Modificação da Regra 3 para exigir explicitamente que o roteiro tenha entre 120 e 140 palavras no total.
- Modificação da Regra 5 para definir que as quebras de linha (`\n`) devem agrupar de 2 a 5 palavras por unidade de pensamento, sem que isso reduza o tamanho ou a profundidade total da história.

---
status: complete
---

# Quick Task: Limpeza da Lógica Duplicada no Voice Actor

**Objetivo:** Remover o bloco de código antigo de agrupamento de legendas que estava no final do ficheiro `src/agents/voice_actor.py` e que sobrescrevia indevidamente o ficheiro SRT gerado pela nova lógica baseada em silêncios (gaps).

## Alterações Realizadas
- Remoção completa das linhas 124 a 155 em `src/agents/voice_actor.py`.
- O ficheiro agora executa exclusivamente a nova e aprimorada lógica de agrupamento baseada em pausas de áudio (`gap > 0.15s`) e limite de 3 palavras, com compensação e extensão de tempo (`AUDIO_OFFSET`).

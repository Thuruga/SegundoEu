---
status: complete
---

# Quick Task: Tag SFX no Scriptwriter e novos campos no State

**Objetivo:** Ensinar a IA a gerar um prompt de efeito sonoro cinematográfico por tema, transportá-lo no estado do pipeline, e prepará-lo para uso futuro pelo editor de vídeo ou gerador de áudio.

## Alterações Realizadas
- `src/state.py`: Adicionados `sfx_prompt: Optional[str]` (prompt textual para SFX) e `sfx_path: Optional[str]` (caminho do ficheiro SFX gerado).
- `src/agents/scriptwriter.py`:
  - Nova regra no formato XML: `<sfx>` para gerar um prompt curto em inglês descrevendo efeitos sonoros cinematográficos (dark whoosh, bass drop, etc.).
  - Exemplo de In-Context Learning atualizado com a tag `<sfx>`.
  - Regex de extração adicionado para `<sfx>`, com resultado guardado em `new_state["sfx_prompt"]`.

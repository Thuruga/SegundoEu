---
status: complete
---

# Quick Task: Agente SFX Generator

**Objetivo:** Criar um novo agente no pipeline que gera efeitos sonoros cinematográficos usando a API de inferência do HuggingFace (modelo AudioLDM-S), a partir do prompt gerado pelo Scriptwriter.

## Alterações Realizadas
- **[NEW] `src/agents/sfx_generator.py`**:
  - Função `generate_sfx(state) -> VideoState` que lê `sfx_prompt` do state e `HF_API_KEY` do ambiente.
  - POST request para `https://api-inference.huggingface.co/models/cvssp/audioldm-s` com timeout de 120s.
  - Grava o áudio em `assets/sfx/{slug}_{timestamp}.mp3`.
  - Tratamento gracioso completo: chave ausente, timeout, HTTP errors, erros de rede, e respostas inesperadas — tudo resulta num warning sem quebrar o pipeline.
  - Resultado guardado em `new_state["sfx_path"]`.

---
status: complete
---

# Quick Task: Code Review Fixes — Commas, Keywords, Font

**Objetivo:** Corrigir três erros críticos identificados na revisão de código que degradavam a qualidade do vídeo final.

## Problemas Encontrados e Correções

### 1. Catástrofe das Vírgulas (Efeito "Asma")
- **Problema:** A Regra 3 forçava vírgulas a cada 3-4 palavras, fazendo o edge-tts soar ofegante e gerar 25+ clipes de legenda piscando.
- **Correção:** Removida a regra de vírgulas forçadas. Substituída por instruções para frases completas e fluídas de 8 a 12 palavras, com pontuação natural. O exemplo in-context foi totalmente reescrito sem vírgulas excessivas.

### 2. Keywords em Português (Perda da Estética Visual)
- **Problema:** A IA gerava keywords em português como 'tempo, reflexão, vida' — o Pexels retornava vídeos genéricos de lifestyle.
- **Correção:** Instrução de keywords reescrita com proibições explícitas: "NEVER use literal Portuguese words. NEVER use abstract concepts like 'time' or 'reflection'." O exemplo mostra keywords atmosféricos: `foggy night street, rain on window, abandoned hallway dark`.

### 3. Tipografia Genérica (Fallback Silencioso da Fonte)
- **Problema:** `FONT_PATH` usava caminho relativo (`./assets/fonts/...`) que falhava silenciosamente se o CWD fosse diferente, caindo para `ImageFont.load_default()` (Arial/sans-serif genérica).
- **Correção:** `FONT_PATH` agora é resolvido como caminho absoluto via `os.path.dirname(__file__)`. O bloco `except` agora emite um `WARNING` audível no console em vez de falhar silenciosamente.

## Ficheiros Alterados
- `src/agents/scriptwriter.py` — System prompt reescrito (regras + exemplo in-context)
- `src/agents/video_editor.py` — FONT_PATH absoluto + warning audível no fallback

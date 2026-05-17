---
status: complete
---

# Quick Task: Update Scriptwriter Prompt

**Goal:** Force Brazilian Portuguese (pt-BR) generation and forbid stage directions/annotations in the Gemini prompt.

## Changes Made
- Updated `ChatPromptTemplate` in `src/agents/scriptwriter.py`.
- Replaced the vague system instruction with a `STRICT RULES` section.
- Added explicit rules to enforce `pt-BR` for the spoken text.
- Added explicit rules to forbid `Timing check`, `(Pause)`, audio cues, or any other annotations.
- Retained the instruction to output `KEYWORDS:` in English.

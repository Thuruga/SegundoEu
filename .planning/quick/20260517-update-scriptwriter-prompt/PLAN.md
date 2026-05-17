---
status: incomplete
---

<description>
Update the system prompt in `src/agents/scriptwriter.py` to force Brazilian Portuguese (pt-BR) generation and strictly forbid annotations or stage directions.
</description>

<tasks>
1. Update `ChatPromptTemplate` in `src/agents/scriptwriter.py`.
2. Explicitly add a `STRICT RULE` for no stage directions or timing checks.
3. Ensure it outputs text in Brazilian Portuguese while keeping `KEYWORDS:` tag and words in English.
</tasks>

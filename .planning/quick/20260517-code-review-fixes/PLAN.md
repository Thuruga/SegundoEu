---
status: incomplete
---

<description>
Fix three critical issues found in code review:
1. **Comma Catastrophe**: Remove the "frequent commas" rule from scriptwriter prompt. Replace with natural sentence flow using complete, calm phrases of 8-12 words. Update the in-context example accordingly.
2. **Keywords in Portuguese**: Strengthen keyword instructions to absolutely enforce English-only dark/moody/minimalist photography concepts. Add explicit prohibition against Portuguese keywords.
3. **Font Fallback**: Fix FONT_PATH to use absolute path relative to the script file so the font loads regardless of working directory.
</description>

<tasks>
1. Rewrite the system prompt in `src/agents/scriptwriter.py` — remove comma rule, use natural sentences, enforce English keywords.
2. Fix FONT_PATH in `src/agents/video_editor.py` to use `os.path.dirname(__file__)` based absolute resolution.
3. Add a loud warning (not silent fallback) when font fails to load.
4. Verify syntax of both files with `py_compile`.
5. Create SUMMARY.md, update STATE.md, commit/push.
</tasks>

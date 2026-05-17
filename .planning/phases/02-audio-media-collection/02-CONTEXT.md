# Phase 2: Audio & Media Collection - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement Agent 2 (Voice Actor) to generate TTS audio and Agent 3 (Media Researcher) to fetch and download background vertical videos from Pexels based on script keywords.
</domain>

<decisions>
## Implementation Decisions

### TTS Voice & Styling (Edge-TTS Configuration)
- **D-01:** TTS configuration must be loaded from `.env` to support configurable language and voice settings.
- **D-02:** The default configured voice should be a deep, calm male voice in Brazilian Portuguese (`pt-BR`), specifically targeting voices like `pt-BR-AntonioNeural` or `pt-BR-JulioNeural`.
- **D-03:** The speaking rate remains `-10%` to ensure a reflective and paused tone.

### Pexels Keyword Extraction (Search Strategy)
- **D-04:** Modify the Scriptwriter (Agent 1) to return a list of 2-3 visually evocative search keywords/phrases in the LangGraph state alongside the generated script, utilizing Gemini Pro's semantic understanding.

### Video Selection & Downloader Constraints
- **D-05:** The Media Researcher (Agent 3) will fetch the first returned high-definition vertical video (`orientation=portrait`) from the Pexels API.
- **D-06:** If no exact matches are found, it must automatically fallback to generic calming keywords (e.g., `nature`, `space`, `abstract`).
- **D-07:** If the downloaded video is shorter than the voiceover audio, flag it in the state so the MoviePy node in Phase 3 can loop or extend it.

### Media Directory Structure & Storage
- **D-08:** Save downloaded media files under a persistent `assets/` directory at the project root (e.g., `assets/audio/` and `assets/video/`) using clean topic slugs or timestamped names to keep them readable for debugging.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Specs
- `.planning/REQUIREMENTS.md` — Requirements GEN-02 and GEN-03
- `.planning/ROADMAP.md` — Phase 2 definition

### Existing Code Context
- `src/state.py` — For the pipeline state definition (`VideoState`) where `audio_path`, `video_path` and `keywords` (to be added) will be stored.
- `src/agents/scriptwriter.py` — Upstream logic for Agent 1 that needs modification to produce keywords.
- `src/graph.py` — Orchestration file where Agents 2 and 3 will be integrated.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `VideoState` dictionary in `src/state.py`.
- `build_graph()` orchestration mechanism in `src/graph.py`.

### Established Patterns
- LangGraph application pattern using lightweight `TypedDict` for state.
- Modular agent setup located inside the `src/agents/` directory. Each agent takes the state, processes it, and returns an updated state copy.

### Integration Points
- Add `PEXELS_API_KEY` alongside `GROQ_API_KEY` via `dotenv` in `src/main.py`.
- Extend the LangGraph workflow in `src/graph.py` by adding nodes for `voice_actor` and `media_researcher`.

</code_context>

<specifics>
## Specific Ideas
- Support for Brazilian Portuguese (pt-BR) is prioritized for the voice actor. The `.env` structure should allow easy swapping of voice identifiers.
</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.
</deferred>

---

*Phase: 2-Audio & Media Collection*
*Context gathered: 2026-05-17*

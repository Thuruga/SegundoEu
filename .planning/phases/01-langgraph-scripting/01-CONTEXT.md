# Phase 1: LangGraph & Scripting - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Setup LangGraph state, orchestrator, and Agent 1 to generate scripts using Gemini Pro.
</domain>

<decisions>
## Implementation Decisions

### State Management
- **D-01:** Use a standard Python `TypedDict` for the LangGraph state.
- **D-02:** The state schema should track the progress of the video pipeline, including fields for `script`, `audio_path`, `video_path`, `final_video_path`, and pipeline `status`.

### Prompting Strategy
- **D-03:** Hardcode the "Shortsophy" style constraints (philosophical, reflective tone, ~1-minute duration) into a `ChatPromptTemplate` for Agent 1.
- **D-04:** Use `ChatGoogleGenerativeAI` from the `langchain-google-genai` package for calling the Gemini API.

### the agent's Discretion
- Module structure for agents (e.g. `agents.py` vs individual files per agent).
- How to structure the graph edges (direct vs conditional edges if needed).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Specs
- `.planning/REQUIREMENTS.md` — Requirement GEN-01 and GEN-05
- `.planning/ROADMAP.md` — Phase 1 definition

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None (Greenfield project).

### Established Patterns
- Standard Python 3 LangGraph application pattern.

### Integration Points
- Gemini API token setup via environment variables (`GOOGLE_API_KEY`).

</code_context>

<specifics>
## Specific Ideas

The scripts should have a philosophical and reflective tone, targeting about 1 minute when spoken at a -10% rate.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 1-LangGraph & Scripting*
*Context gathered: 2026-05-17*

# Phase 3: Video Assembly - Context

**Gathered:** 2026-05-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement Agent 4 (Video Editor) to composite the final vertical 9:16 video: merging the voice actor's voiceover audio with the fetched background video, applying custom sub-second transparent canvas subtitles, and optionally mixing background music with a configurable fallback.
</domain>

<decisions>
## Implementation Decisions

### Subtitle Pacing & Chunking
- **D-01:** Subtitles will be displayed in short phrases (2-3 words per screen) to match the calm, reflective, and paused locution rate of `edge-tts` without hyper-stimulating the viewer.

### Subtitle Visual Styling
- **D-02:** Subtitles will be styled on a clean transparent canvas, utilizing bold white text with a clean black drop shadow or stroke/outline. Text will be centered on the lower-middle portion of the screen.
- **D-03:** Visual styling must keep a minimalist focus, maintaining the cinematic aesthetic of the background video without background boxes (capsules) or karaoke active-word color highlights.

### Aspect Ratio & Fitting Strategy
- **D-04:** Aspect ratio normalization will use **Crop-to-Fill (Center Crop)** to ensure the final composite fills a 1080x1920 (9:16) vertical canvas with zero letterboxing (black bars) or visual stretching/distortions.

### Background Music Integration
- **D-05:** Background music will implement a **Configurable Mix (Fallback)** pattern. Agent 4 will scan `assets/music/` for `.mp3` files.
- **D-06:** If music files are found in `assets/music/`, the agent will choose one randomly, loop/clip it to cover the final video duration, apply audio ducking (reducing the music volume under the voice actor's voiceover, e.g., to 10% volume or -25dB), and merge it with the voiceover.
- **D-07:** If the directory is empty or missing, it will gracefully fallback to voiceover-only without failing.

### the agent's Discretion
- The exact layout, margins, and vertical offsets for centering the text on the lower-middle portion of the screen (typically 70-80% height level).
- The exact volume ducking level and transition timing.
- Specific font choice (e.g., standard readable sans-serif fonts like Arial, Montserrat, or Inter, depending on system availability).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Specs
- `.planning/REQUIREMENTS.md` — Requirement GEN-04 (Video Assembly)
- `.planning/ROADMAP.md` — Phase 3 details

### Codebase Abstractions
- `src/state.py` — The pipeline state definition (`VideoState`) where `audio_path`, `video_path`, `subtitles_path`, and `final_video_path` will be defined.
- `src/agents/voice_actor.py` — Upstream logic for Agent 2 where timing and subtitles generation (`.srt`) must be added using `edge_tts.SubMaker`.
- `src/graph.py` — Orchestration file where the new `video_editor` node will be registered.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `VideoState` dictionary in `src/state.py` for standard state tracking.
- `build_graph()` orchestration mechanism in `src/graph.py` to register the new video editor node.
- Stream-download function `_download_file` in `src/agents/media_researcher.py` as a reference for chunked IO.

### Established Patterns
- Modular agent setup located inside the `src/agents/` directory. Each agent takes the state, processes it, and returns an updated state copy.
- Edge-tts async execution wrapped synchronously in LangGraph nodes via `asyncio.run()`.

### Integration Points
- Add `moviepy` and `pillow` to `requirements.txt`.
- Extend `VideoState` in `src/state.py` with `subtitles_path: Optional[str]`.
- Update `src/agents/voice_actor.py` to use `edge_tts.SubMaker` for sub-second subtitle generation, saving files to `assets/subtitles/`.
- Create `src/agents/video_editor.py` to handle the cropping, looping, ducking, and subtitle overlay.
- Update `src/graph.py` to add `video_editor` as a node in the LangGraph workflow.

</code_context>

<specifics>
## Specific Ideas

- The final video must be fully ready for publishing to YouTube Shorts, meaning it should incorporate all audio and visual assets including subtitles and background music in a single compiled H.264/AAC `.mp4` file.
</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 3-Video Assembly*
*Context gathered: 2026-05-17*

---
phase: 2
plan: B
type: execute
wave: 1
depends_on: []
autonomous: true
requirements: [GEN-03]
files_modified:
  - src/agents/media_researcher.py
  - src/graph.py
  - src/main.py
---

<objective>
Implement Agent 3 (Media Researcher) that queries the Pexels API for a portrait-orientation HD video using keywords from state, downloads it to `assets/video/`, handles fallback keywords if no match is found, and flags `video_needs_loop` when the video is shorter than a reference audio duration. Then wire both Agent 2 and Agent 3 into the LangGraph graph after Agent 1.
</objective>

<read_first>
- src/graph.py — current graph definition (scriptwriter → END)
- src/main.py — current pipeline invocation and initial state construction
- src/state.py — VideoState definition (after Plan A adds keywords + video_needs_loop)
- .planning/phases/02-audio-media-collection/02-CONTEXT.md — decisions D-05, D-06, D-07, D-08
- .planning/phases/02-audio-media-collection/02-RESEARCH.md — Pexels API endpoint, auth header, response schema, download pattern, fallback keyword chain
</read_first>

<tasks>

<task id="B1" type="execute">
  <title>Create Agent 3 — Media Researcher (Pexels)</title>
  <action>
    Create `src/agents/media_researcher.py` implementing function `fetch_video(state: VideoState) -> VideoState`.

    Logic:
    1. Read `PEXELS_API_KEY` from env via `os.getenv("PEXELS_API_KEY")`. If missing, raise `EnvironmentError("PEXELS_API_KEY not set in .env")`.
    2. Build keyword query: join `state["keywords"]` with space if list is non-empty; otherwise use `"natureza calma"`.
    3. Define fallback chain: `[query, "natureza calma", "espaço universo", "abstrato minimalista"]`.
    4. For each keyword in fallback chain:
       - Call `GET https://api.pexels.com/videos/search` with params `query`, `orientation="portrait"`, `size="large"`, `per_page=1`.
       - Header: `Authorization: {PEXELS_API_KEY}`.
       - If response has `videos` with at least 1 item → break and use this video.
    5. If no video found after all fallbacks: raise `RuntimeError("No portrait video found on Pexels after all fallbacks")`.
    6. From `video["video_files"]`, select the file where `width <= 1080` and quality is `"hd"`. If none matches, take the first file.
    7. Download the video using `requests.get(url, stream=True)` writing in 8192-byte chunks.
    8. Output path: `assets/video/{slug}_{timestamp}.mp4` using same slug/timestamp pattern as Plan A.
    9. Duration flag: read `video["duration"]` (int, seconds) from API response. If `video["duration"] < 60` (our target audio length), set `new_state["video_needs_loop"] = True`; else `False`.
    10. Set `new_state["video_path"] = output_path`, `new_state["status"] = "video_fetched"`.
    11. Print: `--- Fetching video for keywords: '{query}' ---` and `--- Downloaded: {output_path} ({duration}s) ---`.
  </action>
  <acceptance_criteria>
    - `src/agents/media_researcher.py` exists and contains function `fetch_video(state: VideoState) -> VideoState`
    - Uses `requests.get` with `Authorization` header and `orientation=portrait`
    - Implements fallback chain with at least 3 generic keyword alternatives
    - Saves file to `assets/video/` directory with `.mp4` extension
    - `new_state["video_path"]` is a string ending in `.mp4`
    - `new_state["video_needs_loop"]` is set to `True` or `False`
    - `new_state["status"]` == `"video_fetched"`
  </acceptance_criteria>
</task>

<task id="B2" type="execute">
  <title>Wire Agents 2 and 3 into LangGraph graph</title>
  <action>
    In `src/graph.py`:
    1. Add imports: `from src.agents.voice_actor import generate_audio` and `from src.agents.media_researcher import fetch_video`.
    2. In `build_graph()`, add two new nodes:
       - `workflow.add_node("voice_actor", generate_audio)`
       - `workflow.add_node("media_researcher", fetch_video)`
    3. Update edges:
       - Remove `workflow.add_edge("scriptwriter", END)`.
       - Add `workflow.add_edge("scriptwriter", "voice_actor")`.
       - Add `workflow.add_edge("voice_actor", "media_researcher")`.
       - Add `workflow.add_edge("media_researcher", END)`.
    4. Update the inline comment to reflect all 3 agents are now wired.
  </action>
  <acceptance_criteria>
    - `src/graph.py` imports `generate_audio` and `fetch_video`
    - `build_graph()` adds nodes `voice_actor` and `media_researcher`
    - Edge chain is `scriptwriter → voice_actor → media_researcher → END`
    - `workflow.add_edge("scriptwriter", END)` is no longer present
  </acceptance_criteria>
</task>

<task id="B3" type="execute">
  <title>Update main.py to reflect new state fields and pipeline output</title>
  <action>
    In `src/main.py`:
    1. Add `PEXELS_API_KEY` guard: after the `GOOGLE_API_KEY` check, add a check for `os.getenv("PEXELS_API_KEY")` with error message `"Error: PEXELS_API_KEY not set. Please add it to your .env file."`.
    2. Extend `initial_state` with the new fields:
       ```python
       keywords=None,
       video_needs_loop=None,
       ```
    3. After pipeline runs, add output lines:
       ```python
       print(f"Audio Path: {result['audio_path']}")
       print(f"Video Path: {result['video_path']}")
       print(f"Video Needs Loop: {result['video_needs_loop']}")
       ```
  </action>
  <acceptance_criteria>
    - `src/main.py` checks for `PEXELS_API_KEY` env var and exits with error if missing
    - `initial_state` includes `keywords=None` and `video_needs_loop=None`
    - Pipeline output prints `audio_path` and `video_path`
  </acceptance_criteria>
</task>

</tasks>

<verification>
1. `python3 -c "from src.agents.media_researcher import fetch_video; print('ok')"` — exits 0
2. `python3 -c "from src.graph import build_graph; g = build_graph(); print('graph ok')"` — exits 0
3. `grep -n "voice_actor\|media_researcher" src/graph.py` — shows both nodes
4. `grep "video_path\|audio_path" src/main.py` — shows output lines
</verification>

<success_criteria>
- Agent 3 (`media_researcher.py`) is implemented with Pexels API integration and fallback logic
- LangGraph graph chains all three agents: scriptwriter → voice_actor → media_researcher → END
- main.py initializes and prints all new state fields
- Full pipeline can be imported without errors
</success_criteria>

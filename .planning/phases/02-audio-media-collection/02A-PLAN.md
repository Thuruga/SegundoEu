---
phase: 2
plan: A
type: execute
wave: 1
depends_on: []
autonomous: true
requirements: [GEN-02]
files_modified:
  - src/state.py
  - src/agents/scriptwriter.py
  - src/agents/voice_actor.py
  - assets/audio/.gitkeep
  - requirements.txt
  - .env
---

<objective>
Extend the LangGraph state schema with `keywords` and `video_needs_loop` fields, update Agent 1 (Scriptwriter) to extract and return TTS keywords, and implement Agent 2 (Voice Actor) that converts the script to a Brazilian Portuguese `.mp3` audio file using `edge-tts` with a -10% speaking rate. Voice and rate are configurable via `.env`.
</objective>

<read_first>
- src/state.py — current VideoState TypedDict definition
- src/agents/scriptwriter.py — current Agent 1 implementation and prompt structure
- .planning/phases/02-audio-media-collection/02-CONTEXT.md — locked decisions D-01 through D-08
- .planning/phases/02-audio-media-collection/02-RESEARCH.md — edge-tts API patterns, voice names, rate format
- .env — current env vars (GOOGLE_API_KEY)
- requirements.txt — current dependencies list
</read_first>

<tasks>

<task id="A1" type="execute">
  <title>Extend VideoState with new fields</title>
  <action>
    In `src/state.py`, add two new Optional fields to the `VideoState` TypedDict:
    - `keywords: Optional[List[str]]` — populated by Agent 1, consumed by Agent 3
    - `video_needs_loop: Optional[bool]` — flagged by Agent 3, consumed by Agent 4

    Import `List` from `typing` (add to existing import line).
  </action>
  <acceptance_criteria>
    - `src/state.py` contains `keywords: Optional[List[str]]`
    - `src/state.py` contains `video_needs_loop: Optional[bool]`
    - `from typing import TypedDict, Optional, List` is present
    - `python3 -c "from src.state import VideoState; s = VideoState(topic='t', script=None, audio_path=None, video_path=None, final_video_path=None, status='x', keywords=None, video_needs_loop=None); print('ok')"` exits 0
  </acceptance_criteria>
</task>

<task id="A2" type="execute">
  <title>Update Agent 1 Scriptwriter to extract keywords</title>
  <action>
    In `src/agents/scriptwriter.py`, update the system prompt to instruct Gemini Pro to append 3 visually evocative search keywords at the end of the script, in the format:

    `KEYWORDS: word1, word2, word3`

    After `chain.invoke(...)`, parse the response using `rsplit("KEYWORDS:", 1)`:
    - If "KEYWORDS:" is present: split into `script_text` and `keywords_raw`; strip and split `keywords_raw` by comma into a list; assign to `new_state["keywords"]`
    - If "KEYWORDS:" is absent: set `new_state["keywords"] = []`

    Assign only the script portion (before "KEYWORDS:") to `new_state["script"]`.
  </action>
  <acceptance_criteria>
    - `src/agents/scriptwriter.py` system prompt instructs the model to end with `KEYWORDS: word1, word2, word3`
    - `new_state["keywords"]` is a `List[str]` (3 items ideally, never crashes if absent)
    - `new_state["script"]` does not contain the KEYWORDS line
  </acceptance_criteria>
</task>

<task id="A3" type="execute">
  <title>Create Agent 2 — Voice Actor (edge-tts)</title>
  <action>
    Create `src/agents/voice_actor.py` implementing function `generate_audio(state: VideoState) -> VideoState`.

    Read from env (via `os.getenv`):
    - `TTS_VOICE` — default `"pt-BR-AntonioNeural"` if not set
    - `TTS_RATE` — default `"-10%"` if not set

    Use `asyncio.run(...)` to call the async `edge_tts.Communicate(text, voice, rate=rate).save(output_path)`.

    File output path: `assets/audio/{slug}_{timestamp}.mp3` where `slug` = first 30 chars of `state["topic"]` lowercased with spaces replaced by underscores, `timestamp` = `datetime.now().strftime("%Y%m%d_%H%M%S")`.

    Set:
    - `new_state["audio_path"] = output_path`
    - `new_state["status"] = "audio_generated"`

    Print progress: `--- Generating audio with voice: {voice}, rate: {rate} ---`
  </action>
  <acceptance_criteria>
    - `src/agents/voice_actor.py` exists and contains function `generate_audio(state: VideoState) -> VideoState`
    - File uses `edge_tts.Communicate` with `voice` and `rate` from env vars
    - Uses `asyncio.run(...)` to call the async save method
    - Saves output to `assets/audio/` directory
    - `new_state["audio_path"]` is a string ending in `.mp3`
    - `new_state["status"]` == `"audio_generated"`
  </acceptance_criteria>
</task>

<task id="A4" type="execute">
  <title>Create assets directories and update dependencies</title>
  <action>
    1. Create directories `assets/audio/` and `assets/video/` with `.gitkeep` placeholder files.

    2. In `requirements.txt`, add `edge-tts` and `requests` on new lines.

    3. In `.env`, add:
       ```
       PEXELS_API_KEY="your_pexels_api_key_here"
       TTS_VOICE="pt-BR-AntonioNeural"
       TTS_RATE="-10%"
       ```

    4. Check if `.gitignore` exists at project root; if so, add `assets/` to it. If not, create `.gitignore` with `assets/` and `__pycache__/` and `.venv/`.
  </action>
  <acceptance_criteria>
    - `assets/audio/.gitkeep` exists
    - `assets/video/.gitkeep` exists
    - `requirements.txt` contains `edge-tts`
    - `requirements.txt` contains `requests`
    - `.env` contains `TTS_VOICE=`
    - `.env` contains `TTS_RATE=`
    - `.env` contains `PEXELS_API_KEY=`
    - `.gitignore` contains `assets/`
  </acceptance_criteria>
</task>

<task id="A5" type="execute">
  <title>Install new dependencies in virtual environment</title>
  <action>
    Run `pip install edge-tts requests` inside the project's `.venv` virtual environment:
    ```
    .venv/bin/pip install edge-tts requests
    ```
    Verify installation by importing `edge_tts` from the venv Python.
  </action>
  <acceptance_criteria>
    - `.venv/bin/python -c "import edge_tts; print('ok')"` exits 0 and prints "ok"
    - `.venv/bin/python -c "import requests; print('ok')"` exits 0 and prints "ok"
  </acceptance_criteria>
</task>

</tasks>

<verification>
1. Run `python3 -c "from src.state import VideoState; print('state ok')"` — must print "state ok"
2. Run `.venv/bin/python -c "import edge_tts; print('edge-tts ok')"` — must print "edge-tts ok"
3. Check `src/agents/voice_actor.py` exists with `generate_audio` function
4. Check `requirements.txt` contains both `edge-tts` and `requests`
5. Check `.env` contains `TTS_VOICE`, `TTS_RATE`, and `PEXELS_API_KEY`
</verification>

<success_criteria>
- VideoState has `keywords` and `video_needs_loop` fields
- Agent 1 returns keywords in state alongside script
- Agent 2 (`voice_actor.py`) is implemented and reads voice/rate from `.env`
- Dependencies declared in `requirements.txt` and installed in `.venv`
- Asset directories created
</success_criteria>

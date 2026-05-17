---
wave: 1
depends_on: []
files_modified:
  - src/state.py
  - src/agents/voice_actor.py
  - src/agents/video_editor.py
  - src/graph.py
  - src/main.py
autonomous: true
must_haves:
  truths:
    - src/agents/video_editor.py exists and defines assemble_video()
    - voice_actor.py streams with boundary=WordBoundary and writes .srt to assets/subtitles/
    - graph.py routes media_researcher → video_editor → END
    - VideoState contains subtitles_path field
---

# Phase 3: Video Assembly - Plan

We will implement **Agent 4 (Video Editor)** to composite the final vertical portrait Shortsophy-style video at 1080x1920 (9:16). This includes:
1. Modifying **Agent 2 (Voice Actor)** to generate sub-second word boundaries, group them into natural 2-3 word phrases, and output a valid `.srt` file.
2. Implementing **Agent 4 (Video Editor)** to perform a seamless **Crop-to-Fill** center crop normalization, render crisp transparent outline subtitles using **Pillow**, and mix background music with a **Configurable Fallback** ducking system.
3. Updating **LangGraph Orchestrator** in `src/graph.py` to route the state through the new agent node.

---

## Proposed Changes

### Dependencies
Add `moviepy` and `pillow` to `requirements.txt`.

### Abstractions & State
#### `src/state.py`
- Extend `VideoState` to track `subtitles_path: Optional[str]`.

---

### Agent Updates

#### [MODIFY] `src/agents/voice_actor.py`(file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/agents/voice_actor.py)
* Update `generate_audio` to request `boundary="WordBoundary"` in `edge_tts.Communicate`.
* Collect all word timing metadata blocks yielded by the stream.
* Implement a grouping algorithm to chunk words into **2-3 word phrases** (completing a chunk if it reaches 3 words or if a word contains punctuation like `. , ! ? ; :`).
* Generate standard `.srt` format content using the phrase timestamps.
* Save the `.srt` subtitles under `assets/subtitles/{slug}_{timestamp}.srt`.
* Update the returned state with `new_state["subtitles_path"] = subtitles_path` and status `"audio_generated"`.

#### [NEW] `src/agents/video_editor.py`(file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/agents/video_editor.py)
Create the new Video Editor agent:
* Read `audio_path`, `video_path`, `subtitles_path`, and `video_needs_loop` from `VideoState`.
* Load the background video using `VideoFileClip`.
* **Crop-to-Fill Normalization:**
  * Compare the video's aspect ratio to 9:16 (1080x1920).
  * Scale the video so that it covers 1080x1920 entirely (ensuring no letterboxing/black bars).
  * Crop the scaled video centered horizontally and vertically to exactly 1080x1920.
* **Video Looping:** Loop/extend the background video using `.loop(duration=...)` if its duration is shorter than the voiceover audio clip.
* **Subtitle Rendering (Pillow):**
  * Parse the `.srt` file to extract phrase start, end, and text.
  * For each phrase, generate a transparent `RGBA` 1080x1920 canvas using `Pillow`.
  * Style subtitles: Bold white font with a thick black stroke/outline (e.g. `stroke_width=5`, `stroke_fill="black"`).
  * Center the text horizontally and offset it in the lower-middle portion of the screen (typically `y = 1400` of the 1920 height).
  * Convert PIL images directly to numpy arrays in-memory to initialize MoviePy `ImageClip`s, avoiding unnecessary disk writes.
* **Configurable Background Music:**
  * Scan `assets/music/` for `.mp3` files.
  * If found, select one randomly, apply volume ducking (e.g., `.volumex(0.1)`), loop/clip it to cover the full duration, and mix it under the voiceover clip using `CompositeAudioClip`.
  * If the folder is empty or doesn't exist, gracefully fallback to the voiceover audio track only.
* **Composite & Export:**
  * Overlay the subtitle image clips onto the normalized video.
  * Write the final composite vertical video to `assets/output/{slug}_{timestamp}.mp4` using H.264 video codec (`libx264`) and AAC audio codec (`aac`).
  * Return the state updated with `final_video_path` and `status="video_assembled"`.

---

### Pipeline Orchestration

#### [MODIFY] `src/graph.py`(file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/graph.py)
* Register the `video_editor` node.
* Update edges: `media_researcher` -> `video_editor` -> `END`.

#### [MODIFY] `src/main.py`(file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/main.py)
* Update output logging to display `final_video_path` on completion.

---

## Verification Plan

### Automated Tests
* Run `PYTHONPATH=. .venv/bin/python src/main.py` end-to-end.
* Assert that the generated file under `assets/output/` exists.
* Programmatically verify:
  - Video resolution is exactly 1080x1920.
  - Video duration matches the audio voiceover duration.
  - Video contains both valid video and audio tracks.

### Manual Verification
* Play the generated `.mp4` video locally.
* Verify:
  - Center crop is perfect (no distortion or letterboxing).
  - Subtitles appear in natural 2-3 word chunks centered in the lower-middle section.
  - Subtitles have perfect contrast (crisp white text with a solid black outline).
  - Background music is mixed at a calm, supportive volume without overpowering the voiceover.

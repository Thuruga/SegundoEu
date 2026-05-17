# Phase 3: Video Assembly Plan

We will implement **Agent 4 (Video Editor)** to composite the final Shortsophy-style video: merging the generated Voiceover (`.mp3`) and Background Video (`.mp4`), generating and parsing sub-second subtitles, and overlaying high-quality, auto-wrapped, styled subtitles onto the final video using `MoviePy` and `Pillow`.

---

## Proposed Changes

### Dependencies
Add `moviepy` and `pillow` to `requirements.txt`.

### Abstractions & State
Extend `VideoState` in `src/state.py` with `subtitles_path: Optional[str]`.

### Agent Updates

#### `src/agents/voice_actor.py`
* Collect `SentenceBoundary` frames using `edge_tts.SubMaker`.
* Save the generated `.srt` subtitles under `assets/subtitles/the_meaning_of_time_{timestamp}.srt`.
* Update the node state with `new_state["subtitles_path"] = subtitles_path`.

#### `src/agents/video_editor.py` [NEW]
Create the Video Editor agent node:
* Read `audio_path`, `video_path`, `subtitles_path`, and `video_needs_loop` from `VideoState`.
* Loop the background video using `moviepy.video.fx.all.loop` if `video_needs_loop` is True, matching the exact duration of the audio clip.
* Crop/resize the background video to vertical portrait format (1080x1920 or native aspect ratio) if needed.
* Parse the `.srt` subtitles file.
* Use **Pillow** to render high-contrast, wrapped, centered text frames (white font with a thin black border/shadow) on a transparent background.
* Overlay the subtitle image clips onto the video timeline at the exact timestamps.
* Render the final video with default codecs (`libx264` for video, `aac` for audio).
* Write the resulting vertical video to `assets/output/the_meaning_of_time_{timestamp}.mp4`.

---

## Verification Plan

### Automated Tests
- Run `PYTHONPATH=. .venv/bin/python src/main.py` end-to-end.
- Assert `final_video_path` exists in `assets/output/`.
- Verify the video file has valid duration, video track (portrait aspect ratio), and audio track.

### Manual Verification
- Play the generated video to verify subtitle centering, contrast, readability, and correct synchronization with the voice.

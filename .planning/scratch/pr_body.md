## Summary

**Phase 02: Audio & Media Collection**
**Goal:** As a content creator, I want to automatically generate voiceovers and download corresponding vertical videos, so that I have the audio and video assets ready for final video assembly.
**Status:** Verified ✓

This phase completes the audio synthesis and media asset retrieval pipeline for the Shortsophy vertical video generator. We successfully implemented two core LangGraph agents:
1. **Agent 2 (Voice Actor)**: Utilizes `edge-tts` to generate high-quality Brazilian Portuguese voiceovers from the script, configuring TTS rate (-10% slow speaking rate) and voice via environment variables.
2. **Agent 3 (Media Researcher)**: Uses Pexels Video Search API to fetch high-resolution, portrait-oriented videos based on parsed script keywords. Integrated a robust fallback chain of keywords, and a secondary fallback to the **Pixabay Video API** if Pexels results are exhausted. Calculates if the media needs looping (duration < 60s).

---

## Changes

### Agent 2 (Voice Actor)
- Created `src/agents/voice_actor.py` utilizing `edge-tts`.
- Saves `.mp3` voiceovers in `assets/audio/`.

### Agent 3 (Media Researcher)
- Created `src/agents/media_researcher.py` querying Pexels and Pixabay.
- Handles keyword fallback search.
- Computes `video_needs_loop` flag based on target duration (60 seconds).
- Saves `.mp4` background footage in `assets/video/`.

### State & Orchestration
- Extended `VideoState` in `src/state.py` with `keywords` and `video_needs_loop`.
- Updated LangGraph compilation in `src/graph.py` to route `scriptwriter` → `voice_actor` → `media_researcher`.
- Updated entry point `src/main.py` with API key checks and state output.

---

## Requirements Addressed
- **GEN-02**: Brazilian Portuguese slow voiceover generation.
- **GEN-03**: Vertical video download using keywords and fallback search.

---

## Verification
- [x] Automated UAT Verification: **7/7 checks passed** (narration audio generated, video searched and downloaded, fallback chain verified, loop flag computed, state integrity complete).
- [x] Disk assets generated successfully with valid content and size.

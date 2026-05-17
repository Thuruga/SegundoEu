## Summary

**Phase 02: Audio & Media Collection**
**Goal:** As a content creator, I want to automatically generate voiceovers and download corresponding vertical videos, so that I have the audio and video assets ready for final video assembly.
**Status:** Verified ✓

Phase 2 implements the automated voiceover generation (Voice Actor Agent) and background footage download (Media Researcher Agent). Voice Actor translates the philosophical script generated in Phase 1 into text-to-speech audio using `edge-tts`, parameterized by regional voice and speaking rates. Media Researcher performs portrait video searches via the Pexels API (with fallback query parsing and Pixabay API backups) to retrieve relevant high-quality background footage, determining if looping is needed. The two agents are compiled and choreographed sequentially within the LangGraph workflow (`scriptwriter → voice_actor → media_researcher → END`), with output assets generated and saved under `assets/audio/` and `assets/video/` respectively.

## Changes

### Plan A: Audio Generation (edge-tts Integration)
Extends the LangGraph state schema with `keywords` and `video_needs_loop` fields, updates Agent 1 (Scriptwriter) to extract and return TTS keywords, and implements Agent 2 (Voice Actor) that converts the script to a Brazilian Portuguese `.mp3` audio file using `edge-tts`.

**Key files modified/created:**
- [src/state.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/state.py)
- [src/agents/scriptwriter.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/agents/scriptwriter.py)
- [src/agents/voice_actor.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/agents/voice_actor.py)
- [requirements.txt](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/requirements.txt)
- [.env](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/.env)

### Plan B: Background Media Collection & Pipeline Integration
Implements Agent 3 (Media Researcher) that queries Pexels/Pixabay APIs for portrait-orientation videos based on script keywords, downloads them to `assets/video/`, and flags `video_needs_loop` when the video duration is shorter than a reference audio duration. Orchestrates Agent 2 and Agent 3 sequentially inside the LangGraph compilation.

**Key files modified/created:**
- [src/agents/media_researcher.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/agents/media_researcher.py)
- [src/graph.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/graph.py)
- [src/main.py](file:///home/zallu/Documentos/Projetos%20Zallu/Segundo%20eu/src/main.py)

## Requirements Addressed

- **GEN-02**: Agent 2 converts the script to audio using `edge-tts` with a -10% speaking rate.
- **GEN-03**: Agent 3 queries the Pexels API and downloads a vertical background video based on script keywords.

## Verification

- [x] Automated verification: Passed ✓
- [x] Voiceover generation works slow (-10%) in pt-BR
- [x] Background footage downloader fetches portrait HD video with fallback keywords & looping flag

## Key Decisions

- **D-01:** TTS configuration must be loaded from `.env` to support configurable language and voice settings.
- **D-02:** The default configured voice is `pt-BR-AntonioNeural` (calm male voice in Brazilian Portuguese).
- **D-03:** The speaking rate is set to `-10%` to ensure a reflective, philosophical tone.
- **D-04:** Modify Scriptwriter to append 3 visually evocative keywords at the end of the script in the format `KEYWORDS: word1, word2, word3`.
- **D-05:** Media Researcher fetches the first portrait video from Pexels API.
- **D-06:** Implemented fallbacks to generic calming keywords if no exact Pexels match is found, with backup to Pixabay Video API search.
- **D-07:** Flag `video_needs_loop` in the state if video is shorter than 60 seconds (the reference audio duration).
- **D-08:** Save media files under `assets/audio/` and `assets/video/` at the project root using timestamped names and slugs.

## User Stories & Acceptance Criteria

- Acceptance criteria are covered by the linked requirements and verification evidence.

## Risks & Dependencies

- No known high-risk rollout dependencies.

## Success Metrics & Release Criteria

- Release when automated verification and required manual checks pass.

## Stakeholder Review & Approval

- Product owner approval pending for audio-media-collection.

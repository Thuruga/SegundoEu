# Phase 2 Discussion Log

**Date:** 2026-05-17
**Mode:** Text (User Direct Input)

## Discussed Areas

### 1. TTS Voice & Styling (Edge-TTS Configuration)
**Options:**
- A) English calm male/female voice default.
- B) Configurable via `.env` to support both Portuguese (`pt-BR`) and English (`en-US`).
- C) Agent discretion.

**User Selection:** Option B.

**Notes:**
The user explicitly requested support for Brazilian Portuguese (`pt-BR`) voices through the `.env` file, specifically asking for a deep, calm male voice like `pt-BR-AntonioNeural` or `pt-BR-JulioNeural`.

### 2. Pexels Keyword Extraction (Search Strategy)
**Options:**
- A) Agent 1 returns keywords in LangGraph state (Recommended).
- B) NLP extraction directly inside Agent 3.
- C) Hardcoded thematic keywords.

**User Selection:** Option A.

**Notes:**
User approved the recommended approach of having Gemini Pro (Agent 1) identify and return visually evocative keywords.

### 3. Video Selection & Downloader Constraints
**Options:**
- A) Fetch first HD vertical video, fallback to generic keywords, and flag if shorter than audio (Recommended).
- B) Fail immediately if no exact match.
- C) Search horizontal videos as secondary fallback and crop.

**User Selection:** Option A.

**Notes:**
User approved the robust fallback methodology.

### 4. Media Directory Structure & Storage
**Options:**
- A) Persistent `assets/` directory at the project root with clean slugs/timestamps (Recommended).
- B) Temporary directories.

**User Selection:** Option A.

**Notes:**
User approved saving assets to a persistent directory for easy inspection.

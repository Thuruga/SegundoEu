# Automated Shortsophy Video Pipeline

## What This Is

An automated video generation pipeline built in Python using LangGraph. The system generates "Shortsophy-style" (philosophical, reflective short-form videos of ~1 minute length) end-to-end. It utilizes multiple specialized agents to write scripts, generate TTS audio, fetch background footage, composite the final video with subtitles, and present it for human review before publishing to YouTube Shorts.

## Core Value

- **Efficiency**: Automates the entire video creation process from ideation to upload.
- **Quality**: Uses advanced AI (Gemini Pro) for scripting and integrates with professional APIs (Pexels, YouTube v3) for media handling.
- **Control**: Includes a human-in-the-loop review step via a simple frontend before final publication.

## Target Audience

Creators of philosophical/reflective short-form content and their audience on platforms like YouTube Shorts.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **Agent 1 (Scriptwriter)**: Uses Gemini Pro to generate 1-minute reflective/philosophical scripts.
- [ ] **Agent 2 (Voice Actor)**: Uses `edge-tts` to generate audio from the script, applying a -10% speaking rate for a calmer, more reflective tone.
- [ ] **Agent 3 (Media Researcher)**: Queries the Pexels API to download vertical videos based on keywords extracted from the script.
- [ ] **Agent 4 (Video Editor)**: Uses `MoviePy` to combine the generated audio and downloaded background videos, and overlays the script as centered subtitles.
- [ ] **Review Interface**: A simple frontend web application displaying the generated `.mp4` with "Approve" and "Reject" buttons.
- [ ] **Publisher Module**: Automatically uploads approved videos to YouTube using the YouTube Data API v3.
- [ ] **Orchestration**: Uses LangGraph to manage the workflow and state between agents.

### Out of Scope

- [ ] Complex video transitions (beyond simple cuts or standard MoviePy capabilities)
- [ ] Direct publishing to TikTok/Instagram Reels (currently restricted to YouTube v3)
- [ ] Multi-language support (initially targeting a single language, presumably Portuguese based on the prompt)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| LangGraph for Orchestration | Provides robust state management and multi-agent coordination capabilities. | — Pending |
| edge-tts | Cost-effective and high-quality TTS that supports rate modification. | — Pending |
| Pexels API | Offers royalty-free vertical videos suitable for short-form content. | — Pending |
| MoviePy | Mature Python library for programmatic video composition and subtitling. | — Pending |

---
*Last updated: 2026-05-17 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

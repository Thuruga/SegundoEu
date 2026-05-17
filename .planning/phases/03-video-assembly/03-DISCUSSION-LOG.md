# Phase 3: Video Assembly - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-17
**Phase:** 3-video-assembly
**Areas discussed:** Subtitle Pacing & Chunking, Subtitle Visual Styling, Video Sizing & Aspect Ratio, Ambient Background Music

---

## Subtitle Pacing & Chunking

| Option | Description | Selected |
|--------|-------------|----------|
| Option A | Word-by-word (High Engagement - single word flashed on screen in sync) | |
| Option B | Short Phrases / 2-3 Words (Balanced & Dynamic - groups of 2-3 words) | ✓ |
| Option C | Full Sentences (Traditional - full grammatical sentences on screen) | |

**User's choice:** Option B (Short Phrases / 2-3 Words)
**Notes:** User chose this to maintain a minimalist and reflective aesthetic without hyper-stimulating the viewer, keeping the subtitles in perfect synchronization with the calm, paused locution of the voice actor.

---

## Subtitle Visual Styling & Highlighting

| Option | Description | Selected |
|--------|-------------|----------|
| Option A | Clean Transparent Canvas with drop shadow or outline (Elegant & Minimal) | ✓ |
| Option B | Semi-transparent Dark Capsule Box (Modern & High contrast) | |
| Option C | Active-Word Highlight / Karaoke Style (Dynamic Focus) | |

**User's choice:** Option A (Clean Transparent Canvas)
**Notes:** User wanted to keep a clean, transparent visual style utilizing bold white text with a clean drop shadow or stroke/outline. This focuses on the cinematic experience without blocking elements or karaoke-like distractions.

---

## Video Sizing, Fitting & Aspect Ratio

| Option | Description | Selected |
|--------|-------------|----------|
| Option A | Crop-to-Fill (Scale to cover the 1080x1920 screen, cropping as needed) | ✓ |
| Option B | Fit with Letterboxing (Preserve original frame, adding black bars) | |
| Option C | Direct Stretch / Scale (Force fit by scaling, potential distortion) | |

**User's choice:** Option A (Crop-to-Fill)
**Notes:** Center crop will be applied to cover the entire 1080x1920 (9:16) vertical canvas natively without black bars or visual stretch/distortions.

---

## Ambient Background Music

| Option | Description | Selected |
|--------|-------------|----------|
| Option A | Voiceover Only (Strictly voiceover, no background music) | |
| Option B | Low-Volume Ambient Music Mix (Fully self-contained, mixed at low volume) | |
| Option C | Configurable Mix / Fallback (Mix if audio tracks exist in assets/music/, else voiceover only) | ✓ |

**User's choice:** Option C (Configurable Mix - Fallback)
**Notes:** Since videos will be uploaded via the YouTube Data API v3 in Phase 4 (no consumer-facing interface to add music post-upload), they need to be 100% finished. Agent 4 will scan `assets/music/` for `.mp3` files, choose one randomly, loop it, reduce volume (audio ducking), and mix it with the voiceover. If the folder is empty/missing, it falls back to voiceover-only.

---

## the agent's Discretion

- Offsets for subtitle vertical position centering (lower-middle screen).
- Ducking levels and fade timing.
- Specific default sans-serif font selections depending on system availability.

## Deferred Ideas

None.

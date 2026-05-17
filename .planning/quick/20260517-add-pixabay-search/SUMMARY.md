---
status: complete
---

## Summary
Added Pixabay as a fallback media provider to `media_researcher`.

- Updated `.env` and `src/main.py` with `PIXABAY_API_KEY`.
- Modified `src/agents/media_researcher.py` to:
  - Attempt Pexels query first.
  - If Pexels returns no results, attempt to query the Pixabay Video API (`https://pixabay.com/api/videos/`).
  - Extract the medium-sized video URL (favoring portrait dimensions if available) and the duration.
  - Fail gracefully if `PIXABAY_API_KEY` is not set (it just issues a warning and proceeds without fallback).

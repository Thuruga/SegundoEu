---
status: incomplete
---

<description>
Add Pixabay as a secondary media search provider in Agent 3 (media_researcher) when Pexels fails to find a suitable video.
</description>

<tasks>
1. Update `.env` to include `PIXABAY_API_KEY`.
2. Update `src/main.py` to guard `PIXABAY_API_KEY` alongside Pexels.
3. Modify `src/agents/media_researcher.py` to query Pixabay API (`https://pixabay.com/api/videos/`) if Pexels returns no results.
</tasks>

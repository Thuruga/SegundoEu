# Phase 2: Audio & Media Collection — Research

**Phase:** 2 — Audio & Media Collection
**Requirements:** GEN-02, GEN-03
**Date:** 2026-05-17
**Status:** RESEARCH COMPLETE

---

## Agent 2 — Voice Actor (edge-tts)

### Library: `edge-tts`

`edge-tts` is a Python library that uses Microsoft Edge's online TTS service to generate high-quality neural voices — no API key required. It is async-native and supports rate/volume/pitch adjustments via SSML-style parameters.

**Installation:**
```
edge-tts
```

**Core API pattern (async):**
```python
import asyncio
import edge_tts

async def generate_audio(text: str, voice: str, rate: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
```

**Rate control:** The `-10%` speaking rate is applied via the `rate` parameter as the string `"-10%"`.

**Voice naming convention:** `{lang}-{region}-{Name}Neural`
- `pt-BR-AntonioNeural` — deep male Brazilian Portuguese ✓
- `pt-BR-JulioNeural` — alternative male Brazilian Portuguese ✓
- `en-US-BrianNeural` — deep male English (fallback)

**Listing available voices:**
```python
voices = await edge_tts.list_voices()
```

**Key constraint:** `edge-tts.Communicate` is async. Integrating it into a synchronous LangGraph node requires either:
1. `asyncio.run(generate_audio(...))` — simple and works well since LangGraph nodes are called synchronously.
2. Wrapping with `asyncio.get_event_loop().run_until_complete(...)` — same effect.

**Output format:** Saves directly to `.mp3` (default) or `.wav` depending on extension passed.

**File output path convention (from D-08):** `assets/audio/{topic_slug}_{timestamp}.mp3`

---

## Agent 3 — Media Researcher (Pexels API)

### Pexels API — Video Search

**Authentication:** `Authorization: {PEXELS_API_KEY}` header.

**Endpoint:** `GET https://api.pexels.com/videos/search`

**Key parameters:**
- `query` — search keywords (e.g., `"natureza silêncio"`)
- `orientation` — `"portrait"` for vertical videos (9:16)
- `size` — `"large"` for HD quality
- `per_page` — 1 is sufficient for MVP

**Response structure (simplified):**
```json
{
  "videos": [{
    "id": 12345,
    "duration": 30,
    "video_files": [
      { "quality": "hd", "width": 1080, "height": 1920, "link": "https://..." }
    ]
  }]
}
```

**Selecting the best video file:** Filter `video_files` for `width <= 1080` (standard vertical HD), pick the highest-quality link.

**Download pattern:** Stream download using `requests` with `stream=True` for large files:
```python
import requests

def download_video(url: str, output_path: str):
    r = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
```

**Fallback keyword chain (from D-06):**
1. Script keywords (from `state["keywords"]`)
2. `"natureza calma"` (calm nature)
3. `"espaço universo"` (space universe)
4. `"abstrato minimalista"` (abstract minimalist)

**Duration flag (from D-07):** After download, get video duration from API response and compare with audio duration (computed via `edge-tts` subtitle data or a separate `mutagen`/`ffprobe` call). If video shorter than audio: set `state["video_needs_loop"] = True`.

**File output path convention (from D-08):** `assets/video/{topic_slug}_{timestamp}.mp4`

---

## State Schema Changes (GEN-02, GEN-03)

The existing `VideoState` TypedDict (`src/state.py`) needs two new fields:

```python
keywords: Optional[List[str]]       # From Agent 1 — drives Agent 3's search
video_needs_loop: Optional[bool]    # Flagged by Agent 3 for Agent 4
```

---

## Agent 1 Modification (D-04)

The Scriptwriter (`src/agents/scriptwriter.py`) must return `keywords` alongside the `script`. The Gemini Pro prompt should be updated to return a structured response or the agent should make a second lightweight call to extract 2-3 visually evocative keywords from the generated script.

**Recommended approach (single call, structured output):**
Update the system prompt to request that the model appends keywords at the end of the response in a parseable format, then parse them in the agent. Example format:

```
[Script text here]

KEYWORDS: natureza, silêncio, tempo
```

Parse using `rsplit("KEYWORDS:", 1)` to separate script from keywords.

---

## Dependencies to Add to `requirements.txt`

```
edge-tts
requests
```

`requests` is already present in the system but should be declared in project requirements for reproducibility.

---

## `.env` Changes

Add the following keys:

```
PEXELS_API_KEY="your_pexels_api_key_here"
TTS_VOICE="pt-BR-AntonioNeural"
TTS_RATE="-10%"
```

---

## Asset Directory Setup

Create `assets/audio/` and `assets/video/` directories. Add `assets/` to `.gitignore` to avoid committing large binary files.

---

## Integration with LangGraph Graph (`src/graph.py`)

Current graph: `scriptwriter → END`

After Phase 2: `scriptwriter → voice_actor → media_researcher → END`

Both new nodes follow the same pattern as `scriptwriter`: take state, return updated state copy.

---

## RESEARCH COMPLETE

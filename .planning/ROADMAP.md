# Roadmap

**4 phases** | **8 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | LangGraph & Scripting | 1/1 | Complete   | 2026-05-17 |
| 2 | Audio & Media Collection | As a content creator, I want to automatically generate voiceovers and download corresponding vertical videos, so that I have the audio and video assets ready for final video assembly. | GEN-02, GEN-03 | 2 |
| 3 | Video Assembly | Implement Agent 4 to composite audio, video, and subtitles. | GEN-04 | 2 |
| 4 | Review UI & YouTube Upload | Build review frontend and YouTube publishing integration. | PUB-01, PUB-02, PUB-03 | 3 |

## Phase Details

### Phase 1: LangGraph & Scripting
**Goal:** Setup LangGraph state and Agent 1 to generate scripts.
**Mode:** mvp
**Requirements:** GEN-01, GEN-05
**Success Criteria:**
1. LangGraph state graph is defined and executable.
2. Agent 1 successfully queries Gemini Pro to generate a ~1-minute philosophical script.

### Phase 2: Audio & Media Collection
**Goal:** As a content creator, I want to automatically generate voiceovers and download corresponding vertical videos, so that I have the audio and video assets ready for final video assembly.
**Mode:** mvp
**Requirements:** GEN-02, GEN-03
**Success Criteria:**
1. Agent 2 converts the script to an audio file using edge-tts with a -10% rate.
2. Agent 3 successfully fetches and downloads a vertical video from Pexels using keywords.

### Phase 3: Video Assembly
**Goal:** Implement Agent 4 to composite audio, video, and subtitles.
**Mode:** mvp
**Requirements:** GEN-04
**Success Criteria:**
1. Agent 4 uses MoviePy to merge the downloaded video and generated audio.
2. The final video includes centered, readable subtitles corresponding to the script.

### Phase 4: Review UI & YouTube Upload
**Goal:** Build review frontend and YouTube publishing integration.
**Mode:** mvp
**Requirements:** PUB-01, PUB-02, PUB-03
**Success Criteria:**
1. A web frontend displays the generated video with "Approve" and "Reject" buttons.
2. Clicking "Approve" triggers the YouTube API v3 upload process.
3. Video is successfully published to YouTube Shorts as an unlisted/public video.

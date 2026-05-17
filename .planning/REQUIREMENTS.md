# v1 Requirements

## Video Generation
- [ ] **GEN-01**: Agent 1 generates a 1-minute reflective/philosophical script using Gemini Pro.
- [ ] **GEN-02**: Agent 2 converts the script to audio using `edge-tts` with a -10% speaking rate.
- [ ] **GEN-03**: Agent 3 queries the Pexels API and downloads a vertical background video based on script keywords.
- [ ] **GEN-04**: Agent 4 composites the audio and video, and overlays centered subtitles using `MoviePy`.
- [ ] **GEN-05**: The LangGraph orchestrator manages the state and flow between all four generation agents.

## Review and Publish
- [ ] **PUB-01**: The system presents the generated `.mp4` video in a simple frontend interface.
- [ ] **PUB-02**: The frontend allows the user to "Approve" or "Reject" the video.
- [ ] **PUB-03**: If approved, the system automatically uploads the video to YouTube using the YouTube Data API v3.

## Out of Scope
- [ ] Multi-platform publishing (only YouTube Shorts in v1).
- [ ] Advanced visual transitions and effects (only simple cuts and text overlays).

## Traceability
(To be updated by roadmap)

# Phase 3: Video Assembly Context

## Constraints and Requirements
* **Orientation:** Vertical portrait 9:16 aspect ratio (standard: 1080x1920).
* **Length:** Exactly matching the length of the voiceover audio (~1 minute).
* **Subtitles styling:** High readability on dynamic backgrounds (white font, black thin outline or shadow, centered on the lower-middle portion of the screen).
* **Codecs:** H.264 video codec and AAC audio codec for maximum compatibility (essential for YouTube uploads).

## Abstractions & Libraries
* **MoviePy:** Core library for video and audio clipping, looping, compositing, and rendering.
* **Pillow (PIL):** Used to programmatically render subtitle text frames onto high-resolution transparent canvases, side-stepping any reliance on `ImageMagick`.

from typing import TypedDict, Optional, List

class VideoState(TypedDict):
    """
    Represents the state of the Shortsophy video generation pipeline.
    """
    topic: str
    script: Optional[str]
    audio_path: Optional[str]
    video_paths: Optional[List[str]]
    final_video_path: Optional[str]
    keywords: Optional[List[str]]
    video_needs_loop: Optional[bool]
    subtitles_path: Optional[str]
    status: str

from typing import TypedDict, Optional

class VideoState(TypedDict):
    """
    Represents the state of the Shortsophy video generation pipeline.
    """
    topic: str
    script: Optional[str]
    audio_path: Optional[str]
    video_path: Optional[str]
    final_video_path: Optional[str]
    status: str

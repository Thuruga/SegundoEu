import os
import asyncio
from datetime import datetime
import edge_tts
from src.state import VideoState


def generate_audio(state: VideoState) -> VideoState:
    """
    Agent 2: Voice Actor.
    Converts the script to a Brazilian Portuguese audio file using edge-tts.
    Voice and rate are configured via environment variables:
      TTS_VOICE — defaults to pt-BR-AntonioNeural
      TTS_RATE  — defaults to -10%
    """
    voice = os.getenv("TTS_VOICE", "pt-BR-AntonioNeural")
    rate = os.getenv("TTS_RATE", "-10%")

    print(f"--- Generating audio with voice: {voice}, rate: {rate} ---")

    script = state.get("script", "")
    if not script:
        raise ValueError("No script found in state. Ensure Agent 1 ran successfully.")

    # Build output paths
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("assets/subtitles", exist_ok=True)
    
    slug = state["topic"][:30].lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"assets/audio/{slug}_{timestamp}.mp3"
    subtitles_path = f"assets/subtitles/{slug}_{timestamp}.srt"

    # edge-tts is async — run it synchronously from the LangGraph node
    asyncio.run(_save_audio_and_subtitles(script, voice, rate, output_path, subtitles_path))

    print(f"--- Audio saved: {output_path} ---")
    print(f"--- Subtitles saved: {subtitles_path} ---")

    new_state = state.copy()
    new_state["audio_path"] = output_path
    new_state["subtitles_path"] = subtitles_path
    new_state["status"] = "audio_generated"
    return new_state


def _format_timestamp(seconds: float) -> str:
    """Formats seconds into SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int(round((seconds % 1) * 1000))
    if milliseconds == 1000:
        secs += 1
        milliseconds = 0
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


async def _save_audio_and_subtitles(
    text: str, voice: str, rate: str, output_path: str, subtitles_path: str
) -> None:
    """Async helper that calls the edge-tts Communicate API, streams audio and generates grouped subtitles."""
    communicate = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words = []
    
    with open(output_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({
                    "text": chunk["text"],
                    "start": chunk["offset"] / 10000000.0,
                    "duration": chunk["duration"] / 10000000.0
                })
                
    # Group words into 2-3 word phrases
    phrases = []
    current_group = []
    
    for word in words:
        current_group.append(word)
        word_text = word["text"]
        # Check for punctuation to end the current phrase early
        has_punctuation = any(char in word_text for char in [".", ",", "!", "?", ";", ":"])
        
        if len(current_group) >= 3 or has_punctuation:
            phrases.append(current_group)
            current_group = []
            
    if current_group:
        phrases.append(current_group)
        
    # Generate SRT formatted lines
    srt_lines = []
    for i, phrase in enumerate(phrases, 1):
        phrase_text = " ".join(w["text"] for w in phrase)
        start_time = phrase[0]["start"]
        end_time = phrase[-1]["start"] + phrase[-1]["duration"]
        
        srt_lines.append(str(i))
        srt_lines.append(f"{_format_timestamp(start_time)} --> {_format_timestamp(end_time)}")
        srt_lines.append(phrase_text)
        srt_lines.append("")
        
    # Save the subtitle file
    with open(subtitles_path, "w", encoding="utf-8") as srt_file:
        srt_file.write("\n".join(srt_lines))

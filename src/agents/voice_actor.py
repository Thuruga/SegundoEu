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

    # Build output path: assets/audio/{slug}_{timestamp}.mp3
    os.makedirs("assets/audio", exist_ok=True)
    slug = state["topic"][:30].lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"assets/audio/{slug}_{timestamp}.mp3"

    # edge-tts is async — run it synchronously from the LangGraph node
    asyncio.run(_save_audio(script, voice, rate, output_path))

    print(f"--- Audio saved: {output_path} ---")

    new_state = state.copy()
    new_state["audio_path"] = output_path
    new_state["status"] = "audio_generated"
    return new_state


async def _save_audio(text: str, voice: str, rate: str, output_path: str) -> None:
    """Async helper that calls the edge-tts Communicate API."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

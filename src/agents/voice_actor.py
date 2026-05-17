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
                
    # Group words into logical phrases using time gaps (pauses) instead of missing punctuation
    phrases = []
    current_group = []
    
    for i, word in enumerate(words):
        current_group.append(word)
        
        break_phrase = False
        # Regra 1: Tamanho máximo de 3 palavras para ficar limpo na tela
        if len(current_group) >= 3:
            break_phrase = True
        # Regra 2: Se houver um silêncio (gap) maior que 0.15s, significa que houve uma vírgula/ponto! Corta a frase.
        elif i < len(words) - 1:
            next_word = words[i+1]
            word_end = word["start"] + word["duration"]
            gap = next_word["start"] - word_end
            if gap > 0.15: # 150ms de pausa
                break_phrase = True
                
        if break_phrase or i == len(words) - 1:
            phrases.append(current_group)
            current_group = []
            
    # Generate SRT formatted lines
    srt_lines = []
    AUDIO_OFFSET = 0.05 # Compensa o atraso de decodificação do MP3 no MoviePy
    
    for i, phrase in enumerate(phrases):
        phrase_text = " ".join(w["text"] for w in phrase)
        start_time = phrase[0]["start"] + AUDIO_OFFSET
        
        # Estica a legenda até a próxima começar. Isso mantém o texto na tela 
        # durante as pausas, evitando que ela "pisque" ou desapareça antes do tom acabar.
        if i < len(phrases) - 1:
            end_time = phrases[i+1][0]["start"] + AUDIO_OFFSET - 0.05
        else:
            end_time = phrase[-1]["start"] + phrase[-1]["duration"] + AUDIO_OFFSET + 0.5
            
        srt_lines.append(str(i + 1))
        srt_lines.append(f"{_format_timestamp(start_time)} --> {_format_timestamp(end_time)}")
        srt_lines.append(phrase_text)
        srt_lines.append("")
        
    # Save the subtitle file
    with open(subtitles_path, "w", encoding="utf-8") as srt_file:
        srt_file.write("\n".join(srt_lines))


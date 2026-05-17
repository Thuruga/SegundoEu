import asyncio
import edge_tts
import re

def format_timestamp(seconds: float) -> str:
    """Formats seconds into SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int(round((seconds % 1) * 1000))
    if milliseconds == 1000:
        secs += 1
        milliseconds = 0
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

async def main():
    text = "O tempo é uma ilusão criada pela nossa mente para dar ordem às nossas experiências."
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="-10%", boundary="WordBoundary")
    
    words = []
    
    with open("test.mp3", "wb") as f:
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
    # A group ends if it reaches 3 words, or if a word ends with punctuation (. , ! ? ; :)
    phrases = []
    current_group = []
    
    for word in words:
        current_group.append(word)
        word_text = word["text"]
        # Check for punctuation
        has_punctuation = any(char in word_text for char in [".", ",", "!", "?", ";", ":"])
        
        if len(current_group) >= 3 or has_punctuation:
            phrases.append(current_group)
            current_group = []
            
    if current_group:
        phrases.append(current_group)
        
    # Generate SRT content
    srt_lines = []
    for i, phrase in enumerate(phrases, 1):
        phrase_text = " ".join(w["text"] for w in phrase)
        start_time = phrase[0]["start"]
        end_time = phrase[-1]["start"] + phrase[-1]["duration"]
        
        srt_lines.append(str(i))
        srt_lines.append(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}")
        srt_lines.append(phrase_text)
        srt_lines.append("")
        
    srt_content = "\n".join(srt_lines)
    print("Grouped SRT generated:")
    print(srt_content[:500])

if __name__ == "__main__":
    asyncio.run(main())

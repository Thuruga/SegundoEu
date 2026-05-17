import asyncio
import edge_tts

async def main():
    text = "O tempo é uma ilusão criada pela nossa mente."
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="-10%", boundary="WordBoundary")
    submaker = edge_tts.SubMaker()
    
    with open("test.mp3", "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    print("SRT generated:")
    print(submaker.get_srt())

if __name__ == "__main__":
    asyncio.run(main())

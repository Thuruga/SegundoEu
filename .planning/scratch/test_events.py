import asyncio
import edge_tts

async def main():
    text = "O tempo é uma ilusão."
    communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural", rate="-10%")
    
    async for chunk in communicate.stream():
        if chunk["type"] != "audio":
            print(chunk)

if __name__ == "__main__":
    asyncio.run(main())

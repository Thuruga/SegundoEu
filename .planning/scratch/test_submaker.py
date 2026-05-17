import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate("Olá, este é um teste de legenda. E aqui está a segunda frase.", "pt-BR-AntonioNeural")
    submaker = edge_tts.SubMaker()
    async for chunk in communicate.stream():
        if chunk["type"] == "SentenceBoundary":
            submaker.feed(chunk)
    
    print("SRT Content:")
    print(submaker.get_srt())

if __name__ == "__main__":
    asyncio.run(main())

import os
from dotenv import load_dotenv
from src.graph import build_graph
from src.state import VideoState

def main():
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY is not set. Please create a .env file and add your API key.")
        return

    if not os.getenv("PEXELS_API_KEY"):
        print("Error: PEXELS_API_KEY is not set. Please add it to your .env file.")
        return

    if not os.getenv("PIXABAY_API_KEY"):
        print("Error: PIXABAY_API_KEY is not set. Please add it to your .env file.")
        return

    topic = "The meaning of time"
    print(f"Starting Shortsophy Pipeline for topic: {topic}\n")

    # Initialize pipeline
    app = build_graph()

    # Create initial state
    initial_state = VideoState(
        topic=topic,
        script=None,
        audio_path=None,
        video_paths=None,
        final_video_path=None,
        keywords=None,
        video_needs_loop=None,
        subtitles_path=None,
        sfx_prompt=None,
        sfx_path=None,
        status="started"
    )

    # Run pipeline
    result = app.invoke(initial_state)

    print("\n--- Pipeline Execution Complete ---")
    print(f"Final Status:    {result['status']}")
    print(f"Keywords:        {result.get('keywords', [])}")
    print(f"SFX Prompt:      {result.get('sfx_prompt', 'N/A')}")
    print(f"SFX Path:        {result.get('sfx_path', 'N/A')}")
    print(f"Audio Path:      {result.get('audio_path', 'N/A')}")
    print(f"Subtitles Path:  {result.get('subtitles_path', 'N/A')}")
    print(f"Video Paths:     {result.get('video_paths', 'N/A')}")
    print(f"Final Video:     {result.get('final_video_path', 'N/A')}")
    print("\nGenerated Script:")
    print("-" * 40)
    print(result["script"])
    print("-" * 40)

if __name__ == "__main__":
    main()

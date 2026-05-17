import os
from dotenv import load_dotenv
from src.graph import build_graph
from src.state import VideoState

def main():
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY is not set. Please create a .env file and add your API key.")
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
        video_path=None,
        final_video_path=None,
        status="started"
    )
    
    # Run pipeline
    result = app.invoke(initial_state)
    
    print("\n--- Pipeline Execution Complete ---")
    print(f"Final Status: {result['status']}")
    print("\nGenerated Script:")
    print("-" * 40)
    print(result["script"])
    print("-" * 40)

if __name__ == "__main__":
    main()

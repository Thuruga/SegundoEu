from langgraph.graph import StateGraph, END
from src.state import VideoState
from src.agents.scriptwriter import generate_script
from src.agents.voice_actor import generate_audio
from src.agents.media_researcher import fetch_video
from src.agents.video_editor import assemble_video

def build_graph():
    """
    Builds the LangGraph orchestration pipeline for Shortsophy.
    Phase 3: scriptwriter → voice_actor → media_researcher → video_editor → END
    """
    workflow = StateGraph(VideoState)

    # Add agent nodes
    workflow.add_node("scriptwriter",    generate_script)
    workflow.add_node("voice_actor",     generate_audio)
    workflow.add_node("media_researcher", fetch_video)
    workflow.add_node("video_editor",    assemble_video)

    # Define sequential pipeline edges
    workflow.set_entry_point("scriptwriter")
    workflow.add_edge("scriptwriter",    "voice_actor")
    workflow.add_edge("voice_actor",     "media_researcher")
    workflow.add_edge("media_researcher", "video_editor")
    workflow.add_edge("video_editor",    END)

    app = workflow.compile()
    return app

from langgraph.graph import StateGraph, END
from src.state import VideoState
from src.agents.scriptwriter import generate_script

def build_graph():
    """
    Builds the LangGraph orchestration pipeline for Shortsophy.
    """
    # Initialize the state graph
    workflow = StateGraph(VideoState)
    
    # Add nodes (agents)
    workflow.add_node("scriptwriter", generate_script)
    
    # Currently we only have Agent 1 implemented for Phase 1.
    # Future phases will add more nodes here.
    
    # Define edges
    workflow.set_entry_point("scriptwriter")
    workflow.add_edge("scriptwriter", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

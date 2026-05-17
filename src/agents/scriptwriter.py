import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import VideoState

def generate_script(state: VideoState) -> VideoState:
    """
    Agent 1: Scriptwriter.
    Generates a philosophical, reflective 1-minute script based on the topic.
    """
    print(f"--- Generating script for topic: '{state['topic']}' ---")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_tokens=300
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a 'Shortsophy' content creator. You write highly reflective, philosophical, and calm scripts for vertical short-form videos. The script should be designed to be spoken slowly and calmly (at a -10% speaking rate), meaning it should take exactly 1 minute to read aloud. Keep it concise, profound, and easy to understand. Only output the spoken script, without any stage directions or visual cues."),
        ("human", "Topic: {topic}\nPlease write the script.")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"topic": state["topic"]})
    
    new_state = state.copy()
    new_state["script"] = response.content
    new_state["status"] = "script_generated"
    
    return new_state

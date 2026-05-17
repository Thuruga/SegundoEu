import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import VideoState

def generate_script(state: VideoState) -> VideoState:
    """
    Agent 1: Scriptwriter.
    Generates a philosophical, reflective 1-minute script based on the topic,
    and extracts 3 visually evocative keywords for background video search.
    """
    print(f"--- Generating script for topic: '{state['topic']}' ---")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.7,
        max_tokens=400
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a 'Shortsophy' content creator. You write highly reflective, philosophical, "
            "and calm scripts for vertical short-form videos.\n\n"
            "STRICT RULES:\n"
            "1. The spoken script MUST be written entirely in Brazilian Portuguese (pt-BR).\n"
            "2. NEVER include stage directions, audio cues, 'Timing check', '(Pause)', or any annotations. Output ONLY the raw text to be spoken.\n"
            "3. The script should take exactly 1 minute to read aloud slowly and calmly.\n\n"
            "After the spoken script, on a new line, add exactly:\n"
            "KEYWORDS: word1, word2, word3\n"
            "where the 3 words are visually evocative English nouns suitable for searching "
            "royalty-free background footage (e.g. 'nature, ocean, stars')."
        )),
        ("human", "Topic: {topic}\nPlease write the script.")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"topic": state["topic"]})
    
    if isinstance(response.content, list):
        raw = "".join([chunk.get("text", "") if isinstance(chunk, dict) else str(chunk) for chunk in response.content])
    else:
        raw = str(response.content)

    # Parse script and keywords
    if "KEYWORDS:" in raw:
        script_part, keywords_raw = raw.rsplit("KEYWORDS:", 1)
        script_text = script_part.strip()
        keywords = [kw.strip() for kw in keywords_raw.strip().split(",") if kw.strip()]
    else:
        script_text = raw.strip()
        keywords = []

    print(f"--- Script generated. Keywords: {keywords} ---")
    
    new_state = state.copy()
    new_state["script"] = script_text
    new_state["keywords"] = keywords
    new_state["status"] = "script_generated"
    
    return new_state

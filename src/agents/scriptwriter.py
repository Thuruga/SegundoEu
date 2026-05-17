import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import VideoState

def generate_script(state: VideoState) -> VideoState:
    """
    Agent 1: Scriptwriter.
    Generates a philosophical, reflective 1-minute script based on the topic,
    and extracts 3 visually evocative keywords for background video search.
    Using Groq API for blazing fast Llama 3 generation.
    """
    print(f"--- Generating script for topic: '{state['topic']}' ---")
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=1024
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a 'Shortsophy' content creator. You write highly reflective, philosophical, "
            "and calm scripts for vertical short-form videos.\n\n"
            "STRICT RULES:\n"
            "1. Write the script entirely in BRAZILIAN PORTUGUESE (pt-BR).\n"
            "2. NO stage directions, notes, titles, or introductions.\n"
            "3. Length must be exactly around 120 words.\n"
            "4. Output your response STRICTLY in the following XML format:\n\n"
            "<script>\n[Insert the Brazilian Portuguese script here]\n</script>\n"
            "<keywords>\n[Insert 3 visually evocative English concepts for dark/moody/minimalist B-roll search, separated by commas. NO literal terms. Use moody photography concepts, e.g., foggy night, walking alone dark, coffee dripping]\n</keywords>\n\n"
            "5. You MUST format the script using line breaks (\\n) to dictate the visual rhythm of the subtitles. Each line must contain a strong thought unit (1 to 4 words max)."
        )),
        ("human", "Topic: {topic}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"topic": state["topic"]})
    
    raw = str(response.content)

    # Extração segura usando Regex para evitar que qualquer formatação quebre
    script_match = re.search(r"<script>(.*?)</script>", raw, re.DOTALL | re.IGNORECASE)
    keywords_match = re.search(r"<keywords>(.*?)</keywords>", raw, re.DOTALL | re.IGNORECASE)

    if script_match:
        script_text = script_match.group(1).strip()
    else:
        print("--- WARNING: API did not return <script> tags. Falling back to raw output. ---")
        print(f"RAW OUTPUT: {raw}")
        script_text = raw.strip()

    keywords = []
    if keywords_match:
        kw_text = keywords_match.group(1).strip()
        keywords = [k.strip() for k in kw_text.split(",") if k.strip()]

    print(f"--- Script generated. Keywords: {keywords} ---")
    
    new_state = state.copy()
    new_state["script"] = script_text
    new_state["keywords"] = keywords
    new_state["status"] = "script_generated"
    
    return new_state
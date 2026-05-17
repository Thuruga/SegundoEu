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
            "1. Write the script entirely in BRAZILIAN PORTUGUESE (pt-BR). NO stage directions, notes, or titles.\n"
            "2. Length MUST be strictly between 120 and 140 words in total.\n"
            "3. You MUST use frequent commas (maximum every 3 to 4 words) to dictate a slow, deliberate, and paused pacing for the subtitles.\n"
            "4. Output your response STRICTLY in the requested XML format (<script> and <keywords>).\n\n"
            "EXEMPLO DO PADRÃO DE ESCRITA ESPERADO:\n"
            "<script>\n"
            "O tempo, implacável e silencioso, não nos espera. "
            "Ele escorre, entre os nossos dedos, como areia fina. "
            "Nós corremos, sem saber para onde, apenas por hábito. "
            "Mas o que sobra, no fim do dia, quando o silêncio cai? "
            "Apenas o agora, frágil e breve, que ignoramos. "
            "Respira fundo, observa o vazio, e percebe a verdade. "
            "A pressa, cega e vazia, rouba-nos a própria essência. "
            "Somos pó, estrelas apagadas, a vagar no escuro. "
            "E ainda assim, carregamos o mundo, nos nossos ombros. "
            "Larga o peso, fecha os olhos, e apenas sente. "
            "A vida, crua e real, acontece no compasso de espera. "
            "Não corras mais, não busques fora, o que já tens. "
            "O universo, calmo e vasto, respira dentro de ti. "
            "Aceita o silêncio, abraça o nada, e sê livre.\n"
            "</script>\n"
            "<keywords>\n"
            "foggy night, empty street dark, fading candlelight\n"
            "</keywords>"
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
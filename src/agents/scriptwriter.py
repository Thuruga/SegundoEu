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
            "3. Write in complete, flowing sentences of 8 to 12 words each. Use natural punctuation — periods and occasional commas. Do NOT overuse commas. Each sentence should feel like one calm breath.\n"
            "4. You MUST use *asterisks* to mark words of emphasis (e.g., 'O tempo não é *dinheiro*'). Emphasize 1 or 2 key words per sentence to guide the voice actor's intonation and create dynamic subtitles.\n"
            "5. Output your response STRICTLY in the following XML format:\n"
            "<script>\n[Your pt-BR script here]\n</script>\n"
            "<keywords>\n[EXACTLY 3 to 4 completely DISTINCT and abstract visual concepts in ENGLISH, separated by commas. These will serve as different B-roll Scenes throughout the video. They MUST be dark, moody, cinematic photography concepts. NEVER use literal Portuguese words. NEVER use abstract nouns like 'time' or 'life'. Use atmospheric visual scenes like: 'rain on window', 'abandoned clock tower', 'flickering streetlight', 'distant mountain peak'.]\n</keywords>\n"
            "<sfx>\n[A SHORT prompt in ENGLISH describing a cinematic sound effect that matches the theme and mood of the script. Think: dark ambient textures, bass drops, whooshes, risers, reverb hits. Example: 'cinematic dark whoosh, heavy bass drop, suspense'.]\n</sfx>\n\n"
            "EXAMPLE OF THE EXPECTED OUTPUT FORMAT:\n"
            "<script>\n"
            "O tempo *não espera* por ninguém que se distraia. "
            "Ele escorre entre os dedos como *areia molhada*. "
            "Corremos sem saber para onde e sem *questionar* o porquê. "
            "No fim do dia apenas o *silêncio* permanece de pé. "
            "O agora é frágil e *breve* como um sopro de vento. "
            "Respira fundo e *observa* o vazio que te rodeia. "
            "A pressa cega nos rouba a *essência* de existir. "
            "Somos poeira de estrelas *vagando* pelo escuro infinito. "
            "Carregamos o *peso do mundo* sem ninguém nos pedir. "
            "Fecha os olhos e *sente* o pulso do universo dentro. "
            "A vida acontece nos segundos que escolhemos *ignorar*. "
            "Para de correr e *aceita* o que já mora em ti. "
            "O universo inteiro cabe num instante de *silêncio*. "
            "Sê *livre* e deixa o nada te mostrar o caminho.\n"
            "</script>\n"
            "<keywords>\n"
            "abandoned clock tower, stormy ocean waves, dying candle flame, cracked desert earth\n"
            "</keywords>\n"
            "<sfx>\n"
            "cinematic dark whoosh, heavy bass drop, suspense\n"
            "</sfx>"
        )),
        ("human", "Topic: {topic}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"topic": state["topic"]})
    
    raw = str(response.content)

    # Extração segura usando Regex para evitar que qualquer formatação quebre
    script_match = re.search(r"<script>(.*?)</script>", raw, re.DOTALL | re.IGNORECASE)
    keywords_match = re.search(r"<keywords>(.*?)</keywords>", raw, re.DOTALL | re.IGNORECASE)
    sfx_match = re.search(r"<sfx>(.*?)</sfx>", raw, re.DOTALL | re.IGNORECASE)

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

    sfx_prompt = ""
    if sfx_match:
        sfx_prompt = sfx_match.group(1).strip()

    print(f"--- Script generated. Keywords: {keywords} | SFX prompt: '{sfx_prompt}' ---")
    
    new_state = state.copy()
    new_state["script"] = script_text
    new_state["keywords"] = keywords
    new_state["sfx_prompt"] = sfx_prompt
    new_state["status"] = "script_generated"
    
    return new_state
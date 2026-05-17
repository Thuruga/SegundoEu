import os
from datetime import datetime
import requests
from src.state import VideoState

# Fallback keywords used when Pexels returns no portrait results
_FALLBACK_KEYWORDS = [
    "natureza calma",
    "espaço universo",
    "abstrato minimalista",
]


def fetch_video(state: VideoState) -> VideoState:
    """
    Agent 3: Media Researcher.
    Queries the Pexels API for a portrait-orientation HD video based on the
    keywords extracted by Agent 1. Falls back through a preset list of generic
    calm keywords if no match is found.

    Sets video_needs_loop=True in state when the downloaded video is shorter
    than 60 seconds (the target audio length), so Agent 4 knows to loop it.
    """
    pexels_api_key = os.getenv("PEXELS_API_KEY")
    if not pexels_api_key:
        raise EnvironmentError("PEXELS_API_KEY is not set. Please add it to your .env file.")

    pixabay_api_key = os.getenv("PIXABAY_API_KEY")
    if not pixabay_api_key:
        print("Warning: PIXABAY_API_KEY is not set, Pixabay fallback will be disabled.")

    # Build keyword query from Agent 1's extracted keywords, or use first fallback
    agent_keywords = state.get("keywords") or []
    primary_query = " ".join(agent_keywords) if agent_keywords else _FALLBACK_KEYWORDS[0]

    # Build full fallback chain: agent keywords first, then generic alternatives
    search_chain = [primary_query] + _FALLBACK_KEYWORDS

    download_url = None
    duration = 0

    for query in search_chain:
        print(f"--- Fetching video for keywords: '{query}' ---")
        
        # 1. Try Pexels
        params = {
            "query": query,
            "orientation": "portrait",
            "size": "large",
            "per_page": 1,
        }
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers={"Authorization": pexels_api_key},
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("videos"):
            video_data = data["videos"][0]
            video_files = video_data.get("video_files", [])
            hd_files = [f for f in video_files if f.get("quality") == "hd" and f.get("width", 9999) <= 1080]
            selected_file = hd_files[0] if hd_files else video_files[0]
            download_url = selected_file["link"]
            duration = video_data.get("duration", 0)
            print(f"--- Found on Pexels ---")
            break
            
        # 2. Try Pixabay if Pexels has no results
        if pixabay_api_key:
            print(f"--- Pexels empty, trying Pixabay for: '{query}' ---")
            pixabay_resp = requests.get(
                "https://pixabay.com/api/videos/",
                params={
                    "key": pixabay_api_key,
                    "q": query,
                    "video_type": "film"
                },
                timeout=15
            )
            pixabay_resp.raise_for_status()
            p_data = pixabay_resp.json()
            
            if p_data.get("hits"):
                hits = p_data["hits"]
                # Try to find a portrait video
                portrait_hits = [h for h in hits if h["videos"]["medium"]["width"] <= h["videos"]["medium"]["height"]]
                selected_hit = portrait_hits[0] if portrait_hits else hits[0]
                
                download_url = selected_hit["videos"]["medium"]["url"]
                duration = selected_hit.get("duration", 0)
                print(f"--- Found on Pixabay ---")
                break

    if not download_url:
        raise RuntimeError("No portrait video found on Pexels or Pixabay after exhausting all fallbacks.")

    # Download video to assets/video/
    os.makedirs("assets/video", exist_ok=True)
    slug = state["topic"][:30].lower().replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"assets/video/{slug}_{timestamp}.mp4"

    _download_file(download_url, output_path)

    print(f"--- Downloaded: {output_path} ({duration}s) ---")

    # Flag if video is shorter than our 60-second target so Agent 4 can loop it
    video_needs_loop = duration < 60

    new_state = state.copy()
    new_state["video_path"] = output_path
    new_state["video_needs_loop"] = video_needs_loop
    new_state["status"] = "video_fetched"
    return new_state


def _download_file(url: str, output_path: str) -> None:
    """Stream-download a file in 8 KB chunks."""
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

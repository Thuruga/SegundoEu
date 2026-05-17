import os
from datetime import datetime
import requests
from src.state import VideoState


# HuggingFace Inference API endpoint for AudioLDM-S
_HF_API_URL = "https://api-inference.huggingface.co/models/cvssp/audioldm-s"


def generate_sfx(state: VideoState) -> VideoState:
    """
    Agent 5: SFX Generator.
    Uses the HuggingFace Inference API (AudioLDM-S) to generate a cinematic
    sound effect from the sfx_prompt produced by Agent 1 (Scriptwriter).

    If HF_API_KEY is missing or the API call fails, the agent prints a warning
    and continues gracefully without breaking the pipeline.
    """
    sfx_prompt = state.get("sfx_prompt", "")
    if not sfx_prompt:
        print("--- [Agent 5] No sfx_prompt found in state. Skipping SFX generation. ---")
        new_state = state.copy()
        new_state["sfx_path"] = None
        new_state["status"] = "sfx_skipped"
        return new_state

    hf_api_key = os.getenv("HF_API_KEY")
    if not hf_api_key:
        print("--- [Agent 5] WARNING: HF_API_KEY is not set. Skipping SFX generation. ---")
        print("    Add HF_API_KEY to your .env file to enable AI-generated sound effects.")
        new_state = state.copy()
        new_state["sfx_path"] = None
        new_state["status"] = "sfx_skipped"
        return new_state

    print(f"--- [Agent 5] Generating SFX for prompt: '{sfx_prompt}' ---")

    try:
        response = requests.post(
            _HF_API_URL,
            headers={"Authorization": f"Bearer {hf_api_key}"},
            json={"inputs": sfx_prompt},
            timeout=120,
        )
        response.raise_for_status()

        # The API returns raw audio bytes on success
        audio_bytes = response.content

        # Verify we got actual audio data (not a JSON error)
        if len(audio_bytes) < 1000:
            # Likely a JSON error response, not audio
            print(f"--- [Agent 5] WARNING: API returned a small response ({len(audio_bytes)} bytes). ---")
            print(f"    Response: {audio_bytes[:500]}")
            new_state = state.copy()
            new_state["sfx_path"] = None
            new_state["status"] = "sfx_failed"
            return new_state

        # Save the generated audio to assets/sfx/
        os.makedirs("assets/sfx", exist_ok=True)
        slug = state["topic"][:30].lower().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"assets/sfx/{slug}_{timestamp}.mp3"

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        print(f"--- [Agent 5] SFX saved: {output_path} ({len(audio_bytes)} bytes) ---")

        new_state = state.copy()
        new_state["sfx_path"] = output_path
        new_state["status"] = "sfx_generated"
        return new_state

    except requests.exceptions.Timeout:
        print("--- [Agent 5] WARNING: HuggingFace API timed out (120s). Skipping SFX. ---")
    except requests.exceptions.HTTPError as e:
        print(f"--- [Agent 5] WARNING: HuggingFace API returned HTTP error: {e} ---")
        print(f"    Response body: {e.response.text[:300] if e.response else 'N/A'}")
    except requests.exceptions.RequestException as e:
        print(f"--- [Agent 5] WARNING: Network error contacting HuggingFace: {e} ---")
    except Exception as e:
        print(f"--- [Agent 5] WARNING: Unexpected error during SFX generation: {e} ---")

    # Graceful fallback — pipeline continues without SFX
    new_state = state.copy()
    new_state["sfx_path"] = None
    new_state["status"] = "sfx_failed"
    return new_state

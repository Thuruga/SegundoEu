import os
import re
import glob
import random
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    ColorClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.fx import Loop as vfx_Loop
from moviepy.audio.fx import AudioLoop as afx_AudioLoop
from src.state import VideoState

# ─── Constants ────────────────────────────────────────────────────────────────
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
TARGET_FPS = 30

# Resolve font path relative to project root (2 levels up from this file)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONT_PATH = os.path.join(_PROJECT_ROOT, "assets", "fonts", "Montserrat-Black.ttf")
FONT_SIZE = 65
STROKE_WIDTH = 4

# Subtitle position: middle (60% down the canvas)
SUBTITLE_Y = int(OUTPUT_HEIGHT * 0.60)

# Music ducking: keep music very low so voiceover dominates
MUSIC_VOLUME = 0.08


# ─── SRT Parsing ─────────────────────────────────────────────────────────────

def _parse_srt(path: str) -> list[dict]:
    """Parse an SRT file into a list of {start, end, text} dicts (times in seconds)."""
    pattern = re.compile(
        r"(\d+)\s*\n"
        r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n"
        r"([\s\S]*?)(?=\n\d+\n|\Z)",
        re.MULTILINE,
    )
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip() + "\n"  # ensure trailing newline for regex

    entries = []
    for m in pattern.finditer(content):
        text = m.group(4).strip()
        entries.append({
            "start": _srt_timestamp_to_seconds(m.group(2)),
            "end":   _srt_timestamp_to_seconds(m.group(3)),
            "text":  text,
        })
    return entries


def _srt_timestamp_to_seconds(ts: str) -> float:
    """Convert 'HH:MM:SS,mmm' to float seconds."""
    hh, mm, rest = ts.split(":")
    ss, ms = rest.split(",")
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000.0


# ─── Subtitle Rendering ───────────────────────────────────────────────────────

def _render_subtitle_frame(text: str, width: int, height: int, y_center: int) -> np.ndarray:
    """
    Render a single subtitle phrase onto a transparent RGBA canvas.
    Renders word by word. If a word contains an *asterisk*, it removes the asterisks 
    and paints it yellow to show emphasis.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except (IOError, OSError) as e:
        # LOUD warning — fallback font will look wrong
        print(f"    ⚠️  WARNING: Could not load font '{FONT_PATH}': {e}")
        print(f"    ⚠️  Falling back to default font — subtitles will look generic!")
        font = ImageFont.load_default()

    words = text.split()
    word_surfaces = []
    total_text_width = 0
    max_height = 0
    
    # Space width
    space_width = draw.textbbox((0, 0), " ", font=font, stroke_width=STROKE_WIDTH)[2]
    
    for word in words:
        is_emphasis = "*" in word
        clean_word = word.replace("*", "")
        
        color = (255, 215, 0, 255) if is_emphasis else (255, 255, 255, 255) # Yellow or White
        
        bbox = draw.textbbox((0, 0), clean_word, font=font, stroke_width=STROKE_WIDTH)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        word_surfaces.append({"text": clean_word, "width": w, "color": color})
        total_text_width += w
        if h > max_height:
            max_height = h
            
    total_text_width += space_width * (max(0, len(words) - 1))
    
    current_x = (width - total_text_width) // 2
    y = y_center - max_height // 2

    for ws in word_surfaces:
        draw.text(
            (current_x, y),
            ws["text"],
            font=font,
            fill=ws["color"],
            stroke_width=STROKE_WIDTH,
            stroke_fill=(0, 0, 0, 255),
        )
        current_x += ws["width"] + space_width

    return np.array(img)


# ─── Crop-to-Fill ────────────────────────────────────────────────────────────

def _crop_to_fill(clip: VideoFileClip, target_w: int, target_h: int) -> VideoFileClip:
    """
    Scale the clip so it fully covers (target_w × target_h) with no letterboxing,
    then crop the excess from the center.
    """
    src_w, src_h = clip.size
    scale_w = target_w / src_w
    scale_h = target_h / src_h
    scale   = max(scale_w, scale_h)           # must cover both dims

    new_w = int(src_w * scale)
    new_h = int(src_h * scale)

    resized = clip.resized((new_w, new_h))

    x1 = (new_w - target_w) // 2
    y1 = (new_h - target_h) // 2
    cropped = resized.cropped(x1=x1, y1=y1, x2=x1 + target_w, y2=y1 + target_h)
    return cropped


# ─── Agent Entry Point ────────────────────────────────────────────────────────

def assemble_video(state: VideoState) -> VideoState:
    """
    Agent 4: Video Editor.
    Composites background video + voiceover + subtitles + optional background music
    into a final 1080×1920 portrait MP4 (H.264 / AAC).
    """
    audio_path     = state.get("audio_path")
    video_paths    = state.get("video_paths")
    subtitles_path = state.get("subtitles_path")

    if not audio_path or not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not video_paths or len(video_paths) == 0:
        raise ValueError(f"No background videos found in state 'video_paths'.")
    if not subtitles_path or not os.path.exists(subtitles_path):
        raise FileNotFoundError(f"Subtitles file not found: {subtitles_path}")

    print("--- [Agent 4] Assembling final video ---")

    # 1. Load voiceover audio
    voiceover = AudioFileClip(audio_path)
    total_duration = voiceover.duration
    print(f"    Voiceover duration: {total_duration:.2f}s")

    # 2. Load, crop and concatenate all background videos
    bg_clips = []
    for vp in video_paths:
        if not os.path.exists(vp):
            print(f"    ⚠️ Warning: Video path not found {vp}")
            continue
        raw_clip = VideoFileClip(vp)
        cropped = _crop_to_fill(raw_clip, OUTPUT_WIDTH, OUTPUT_HEIGHT)
        bg_clips.append(cropped)
    
    if not bg_clips:
        raise FileNotFoundError("Could not load any of the background videos.")
        
    bg_sequence = concatenate_videoclips(bg_clips, method="compose")

    # 3. Loop if shorter than voiceover
    if bg_sequence.duration < total_duration:
        print(f"    Background sequence ({bg_sequence.duration:.1f}s) shorter than audio – looping")
        bg_cropped = bg_sequence.with_effects([vfx_Loop(duration=total_duration)])
    else:
        bg_cropped = bg_sequence.subclipped(0, total_duration)

    bg_cropped = bg_cropped.with_fps(TARGET_FPS)

    # 4. Parse subtitles, build ImageClip overlays, and add SFX
    subtitle_entries = _parse_srt(subtitles_path)
    subtitle_clips   = []
    sfx_clips        = []
    
    sfx_files = sorted(glob.glob("assets/sfx/*.mp3"))
    has_sfx = len(sfx_files) > 0

    for entry in subtitle_entries:
        text = entry["text"]
        has_asterisk = "*" in text
        
        frame  = _render_subtitle_frame(
            text, OUTPUT_WIDTH, OUTPUT_HEIGHT, SUBTITLE_Y
        )
        clip = (
            ImageClip(frame)
            .with_start(entry["start"])
            .with_duration(entry["end"] - entry["start"])
        )
        subtitle_clips.append(clip)
        
        if has_asterisk and has_sfx:
            # Pick a random SFX and add it at the start_time of this subtitle
            sfx_file = random.choice(sfx_files)
            sfx_clip = AudioFileClip(sfx_file).with_start(entry["start"])
            sfx_clips.append(sfx_clip)

    print(f"    Built {len(subtitle_clips)} subtitle overlay clips")
    if sfx_clips:
        print(f"    Built {len(sfx_clips)} SFX audio clips for emphasis")

    # 5. Configurable background music with ducking and SFX mix
    music_files = sorted(glob.glob("assets/music/*.mp3"))
    audio_layers = [voiceover]

    if music_files:
        music_file = random.choice(music_files)
        print(f"    Mixing background music: {music_file}")
        music_clip = AudioFileClip(music_file)
        music_clip = music_clip.with_volume_scaled(MUSIC_VOLUME)

        if music_clip.duration < total_duration:
            music_clip = music_clip.with_effects([afx_AudioLoop(duration=total_duration)])
        else:
            music_clip = music_clip.subclipped(0, total_duration)

        audio_layers.append(music_clip)
    else:
        print("    No music files found in assets/music/ – using voiceover only")
        
    if sfx_clips:
        audio_layers.extend(sfx_clips)
        
    final_audio = CompositeAudioClip(audio_layers)

    # 6. Composite all layers: background + subtitles
    dark_overlay = (
        ColorClip(size=(OUTPUT_WIDTH, OUTPUT_HEIGHT), color=[0, 0, 0])
        .with_duration(total_duration)
        .with_opacity(0.35)
    )
    all_layers = [bg_cropped, dark_overlay] + subtitle_clips
    final_video = CompositeVideoClip(all_layers, size=(OUTPUT_WIDTH, OUTPUT_HEIGHT))
    final_video = final_video.with_audio(final_audio)
    final_video = final_video.with_duration(total_duration)

    # 7. Export
    os.makedirs("assets/output", exist_ok=True)
    slug       = state["topic"][:30].lower().replace(" ", "_")
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"assets/output/{slug}_{timestamp}.mp4"

    print(f"    Writing final video → {output_path}")
    final_video.write_videofile(
        output_path,
        fps=TARGET_FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        logger=None,   # suppress per-frame progress spam; summary still printed
    )

    # 8. Clean up clip file handles
    bg_raw.close()
    voiceover.close()

    print(f"--- [Agent 4] Done: {output_path} ---")

    new_state = state.copy()
    new_state["final_video_path"] = output_path
    new_state["status"]           = "video_assembled"
    return new_state

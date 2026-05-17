import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ColorClip, ImageClip, CompositeVideoClip

def test_rgba_composite():
    # 1. Create a background clip (solid red)
    bg = ColorClip(size=(1080, 1920), color=[255, 0, 0]).with_duration(2)
    
    # 2. Create transparent overlay with text
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((100, 100), "Hello transparency!", font=font, fill=(255, 255, 255, 255))
    
    img_np = np.array(img)
    
    # 3. Create ImageClip from RGBA numpy array
    overlay = ImageClip(img_np).with_duration(2).with_start(0)
    
    # 4. Composite them
    final = CompositeVideoClip([bg, overlay])
    
    # 5. Export to make sure it doesn't crash
    final.write_videofile("test_rgba_out.mp4", fps=24, codec="libx264")
    print("Success! Composited and exported without error.")

if __name__ == "__main__":
    test_rgba_composite()

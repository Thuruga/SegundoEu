from PIL import Image, ImageDraw, ImageFont

def test_text_rendering():
    # Create transparent canvas (1080x1920)
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to load a default font
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except IOError:
        try:
            font = ImageFont.truetype("LiberationSans-Bold.ttf", 60)
        except IOError:
            font = ImageFont.load_default()
            print("Warning: Default font loaded, stroke might not look optimal.")
            
    text = "O tempo é uma ilusão"
    
    # Calculate text bounding box to center it horizontally and position lower-middle (e.g. y = 1400)
    # PIL 10 has getbbox or textbbox
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback for older PIL
        text_width, text_height = draw.textsize(text, font=font)
        
    x = (1080 - text_width) // 2
    y = 1400  # Lower-middle of the screen
    
    # Draw outline text
    draw.text(
        (x, y), 
        text, 
        font=font, 
        fill=(255, 255, 255, 255), 
        stroke_width=5, 
        stroke_fill=(0, 0, 0, 255)
    )
    
    # Save the transparent image
    img.save("text_canvas.png")
    print("Canvas saved successfully to text_canvas.png!")

if __name__ == "__main__":
    test_text_rendering()

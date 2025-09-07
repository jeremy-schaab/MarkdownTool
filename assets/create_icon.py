#!/usr/bin/env python3
"""
Create a simple icon for Markdown Manager if none exists.
This creates a basic icon with the 'MD' text.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    from pathlib import Path
    
    def create_icon():
        # Icon sizes to create
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for size in sizes:
            # Create a new image with transparent background
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Colors - nice blue gradient
            bg_color = (41, 98, 255, 255)  # Blue background
            text_color = (255, 255, 255, 255)  # White text
            border_color = (30, 73, 191, 255)  # Darker blue border
            
            # Draw rounded rectangle background
            margin = size // 8
            draw.rounded_rectangle(
                [margin, margin, size - margin, size - margin], 
                radius=size // 6, 
                fill=bg_color, 
                outline=border_color,
                width=max(1, size // 32)
            )
            
            # Calculate font size
            font_size = max(8, size // 3)
            
            # Try to use a nice font, fallback to default
            try:
                # Try system fonts
                if os.name == 'nt':  # Windows
                    font_path = "C:/Windows/Fonts/arial.ttf"
                else:  # Linux/Mac
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Draw text "MD" centered
            text = "MD"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 - bbox[1]
            
            # Add subtle shadow
            if size >= 32:
                shadow_offset = max(1, size // 32)
                draw.text((x + shadow_offset, y + shadow_offset), text, 
                         font=font, fill=(0, 0, 0, 128))
            
            # Draw main text
            draw.text((x, y), text, font=font, fill=text_color)
            
            images.append(img)
        
        # Save as ICO file
        icon_path = Path("assets/icon.ico")
        icon_path.parent.mkdir(exist_ok=True)
        
        # Save multi-resolution ICO
        images[0].save(
            str(icon_path), 
            format='ICO', 
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print(f"Created icon: {icon_path}")
        print(f"   Sizes: {[img.size for img in images]}")
        
        # Also create PNG versions for other uses
        for i, img in enumerate(images):
            png_path = icon_path.parent / f"icon_{sizes[i]}x{sizes[i]}.png"
            img.save(str(png_path), format='PNG')
        
        print(f"Created PNG versions in assets/ folder")
        
        return True
        
    if __name__ == "__main__":
        create_icon()
        
except ImportError:
    print("WARNING: Pillow not installed. Install with: pip install Pillow")
    print("   Creating simple placeholder icon instead...")
    
    # Create a very basic icon file
    icon_path = Path("assets/icon.ico")
    icon_path.parent.mkdir(exist_ok=True)
    
    # This creates a minimal 16x16 icon
    # In practice, you'd want to provide a proper icon file
    with open(icon_path, "wb") as f:
        # Minimal ICO file header and data
        ico_data = bytes([
            # ICO header
            0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
            # Image directory entry
            0x10, 0x10, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00,
            0x68, 0x04, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00,
        ])
        f.write(ico_data)
        # Add minimal bitmap data (would need proper implementation)
    
    print("WARNING: Created minimal placeholder icon")
    print("   For best results, replace with a proper .ico file")
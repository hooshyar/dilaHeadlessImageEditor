#!/usr/bin/env python3
"""
Create Pattern Image for Dimension Testing

This script creates a test pattern image with clear visual dimension indicators.
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

def create_pattern(width, height, output='pattern.png'):
    """Create a pattern image with clear dimension indicators"""
    # Create a white background
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Add a border
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(0, 0, 0), width=5)
    
    # Draw horizontal stripes every 100px (thicker ones every 500px)
    for y in range(0, height, 100):
        thickness = 5 if y % 500 == 0 else 1
        color = (255, 0, 0) if y % 500 == 0 else (200, 200, 200)
        draw.line([(0, y), (width, y)], fill=color, width=thickness)
        
        # Label the 500px marks
        if y % 500 == 0:
            draw.rectangle([(width//2-50, y-15), (width//2+50, y+15)], fill=(0, 0, 0))
            try:
                font = ImageFont.truetype("Arial", 24)
            except:
                font = ImageFont.load_default()
            draw.text((width//2-30, y-10), f'y={y}', fill=(255, 255, 255), font=font)
    
    # Draw vertical stripes every 100px (thicker ones every 500px)
    for x in range(0, width, 100):
        thickness = 5 if x % 500 == 0 else 1
        color = (0, 0, 255) if x % 500 == 0 else (200, 200, 200)
        draw.line([(x, 0), (x, height)], fill=color, width=thickness)
        
        # Label the 500px marks
        if x % 500 == 0:
            draw.rectangle([(x-50, 15), (x+50, 45)], fill=(0, 0, 0))
            try:
                font = ImageFont.truetype("Arial", 24)
            except:
                font = ImageFont.load_default()
            draw.text((x-30, 25), f'x={x}', fill=(255, 255, 255), font=font)
    
    # Add dimension text at the top
    draw.rectangle([(0, 0), (width, 70)], fill=(0, 0, 0))
    try:
        big_font = ImageFont.truetype("Arial", 36)
    except:
        big_font = ImageFont.load_default()
    draw.text((width//2-180, 20), f'PORTRAIT TEST: {width}x{height}', fill=(255, 255, 255), font=big_font)
    
    # Add additional markers at corners
    corner_size = 100
    
    # Top-left
    draw.rectangle([(0, 0), (corner_size, corner_size)], fill=(255, 0, 0))
    draw.text((10, 80), 'TOP-LEFT', fill=(0, 0, 0))
    
    # Top-right
    draw.rectangle([(width-corner_size, 0), (width, corner_size)], fill=(0, 255, 0))
    draw.text((width-100, 80), 'TOP-RIGHT', fill=(0, 0, 0))
    
    # Bottom-left
    draw.rectangle([(0, height-corner_size), (corner_size, height)], fill=(0, 0, 255))
    draw.text((10, height-50), 'BOTTOM-LEFT', fill=(255, 255, 255))
    
    # Bottom-right
    draw.rectangle([(width-corner_size, height-corner_size), (width, height)], fill=(255, 255, 0))
    draw.text((width-120, height-50), 'BOTTOM-RIGHT', fill=(255, 255, 255))
    
    # Save
    img.save(output)
    print(f'Created pattern image: {output} ({width}x{height})')
    return output

def main():
    if len(sys.argv) >= 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        if len(sys.argv) >= 4:
            output = sys.argv[3]
        else:
            output = f'pattern_{width}x{height}.png'
    else:
        width = 1080
        height = 1920
        output = 'portrait_pattern.png'
    
    create_pattern(width, height, output)
    
    print("\nNext steps:")
    print(f"1. Run: python fix_dimensions.py --url file:///{os.path.abspath(output)} --output fixed_pattern.png")
    print("2. Check that the output image has the correct dimensions")

if __name__ == "__main__":
    main() 
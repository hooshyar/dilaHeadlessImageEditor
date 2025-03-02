#!/usr/bin/env python3
"""
Local Dimension Testing Script for Dila Headless Image Editor

This script tests image dimension handling with visual verification
using the local image processing functions directly.
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
from image_processing import crop_to_fit, apply_custom_text

def create_dimension_test_image(width, height, output_path="dimension_test.jpg"):
    """Create a test image with gridlines to verify dimensions"""
    # Create a blank image with the specified dimensions
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Draw a border
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(0, 0, 0), width=2)
    
    # Draw horizontal and vertical gridlines
    grid_spacing = 100
    
    # Draw horizontal lines
    for y in range(grid_spacing, height, grid_spacing):
        line_color = (200, 0, 0) if y % 500 == 0 else (200, 200, 200)
        line_width = 2 if y % 500 == 0 else 1
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)
        # Label major gridlines
        if y % 500 == 0:
            font = ImageFont.load_default()
            draw.text((10, y+5), f"y={y}", fill=(0, 0, 0), font=font)
    
    # Draw vertical lines
    for x in range(grid_spacing, width, grid_spacing):
        line_color = (0, 0, 200) if x % 500 == 0 else (200, 200, 200)
        line_width = 2 if x % 500 == 0 else 1
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
        # Label major gridlines
        if x % 500 == 0:
            font = ImageFont.load_default()
            draw.text((x+5, 10), f"x={x}", fill=(0, 0, 0), font=font)
    
    # Add dimension information at the top
    draw.rectangle([(0, 0), (width, 40)], fill=(0, 0, 0))
    font = ImageFont.load_default()
    draw.text((10, 10), f"Dimensions: {width}x{height} px", fill=(255, 255, 255), font=font)
    
    # Save the image
    img.save(output_path)
    print(f"Created test image with dimensions {width}x{height} at {output_path}")
    return img

def test_dimensions_locally(width, height, text, language="ckb", container_width_percent=100):
    """Test the image processing directly with specific dimensions"""
    # Create a test image with gridlines
    test_img = create_dimension_test_image(width, height)
    print(f"Original image dimensions: {test_img.width}x{test_img.height}")
    
    # Apply text overlay using local functions
    # Create RGBA tuples for colors
    text_color = (255, 255, 255, 255)  # White
    bg_color = (0, 0, 0, int(0.7 * 255))  # Black with 70% opacity
    
    padding = {"top": 20, "right": 20, "bottom": 20, "left": 20}
    container_margin = 20
    bg_curve = 10
    
    # Apply text
    processed_img = apply_custom_text(
        test_img,
        text,
        language,
        "Noto Sans Arabic",
        40,
        text_color,
        bg_color,
        None,  # text_position
        "bottom-center",  # alignment
        padding,
        bg_curve,
        container_margin,
        container_width_percent
    )
    
    # Save the result
    output_filename = f"local_result_{width}x{height}.png"
    processed_img.save(output_filename)
    print(f"Processed image saved to {output_filename}")
    print(f"Final dimensions: {processed_img.width}x{processed_img.height}")
    
    # Now test with resizing to target dimensions
    resized_img = crop_to_fit(test_img, width, height)
    resized_output = f"resized_{width}x{height}.png"
    resized_img.save(resized_output)
    print(f"Resized image saved to {resized_output}")
    print(f"Resized dimensions: {resized_img.width}x{resized_img.height}")

def main():
    parser = argparse.ArgumentParser(description="Test image dimensions with visual verification")
    parser.add_argument("width", type=int, help="Width in pixels")
    parser.add_argument("height", type=int, help="Height in pixels")
    parser.add_argument("--text", default="بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت", 
                        help="Text to overlay on the image")
    parser.add_argument("--language", default="ckb", help="Language code")
    
    args = parser.parse_args()
    
    test_dimensions_locally(args.width, args.height, args.text, args.language)

if __name__ == "__main__":
    main() 
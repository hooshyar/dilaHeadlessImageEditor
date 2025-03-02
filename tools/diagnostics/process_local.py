#!/usr/bin/env python3
"""
Local Image Processing Script for Dila Headless Image Editor

This script directly processes local images with the image processing functions,
bypassing the API for testing purposes.
"""

import argparse
import os
from PIL import Image, ImageDraw, ImageFont
from image_processing import apply_custom_text

def process_local_image(image_path, text, language="ckb", output_path="local_processed.png"):
    """Process a local image with text overlay"""
    print(f"Loading image from: {image_path}")
    
    # Load the image
    img = Image.open(image_path)
    original_width, original_height = img.size
    print(f"Original image dimensions: {original_width}x{original_height}")
    
    # Create RGBA tuples for colors
    text_color = (255, 255, 255, 255)  # White
    bg_color = (0, 0, 0, int(0.7 * 255))  # Black with 70% opacity
    
    padding = {"top": 20, "right": 20, "bottom": 20, "left": 20}
    container_margin = 20
    bg_curve = 10
    container_width_percent = 100
    
    # Apply text
    processed_img = apply_custom_text(
        img,
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
    processed_img.save(output_path)
    print(f"Processed image saved to {output_path}")
    print(f"Final dimensions: {processed_img.width}x{processed_img.height}")
    
    # Add a verification overlay
    add_verification_overlay(output_path)
    
    return True

def add_verification_overlay(image_path, output_path=None):
    """Add a verification overlay to confirm dimensions"""
    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_verified{ext}"
    
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    # Create a new transparent overlay
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Add dimension text
    try:
        font = ImageFont.truetype("Arial", 36)
    except:
        font = ImageFont.load_default()
    
    # Add a semi-transparent header
    draw.rectangle([(0, 0), (width, 60)], fill=(0, 0, 0, 128))
    draw.text((20, 10), f"Dimensions: {width}x{height}", fill=(255, 255, 255), font=font)
    
    # Add corner markers
    marker_size = 50
    line_width = 3
    
    # Top-left
    draw.line([(0, 0), (marker_size, 0)], fill=(255, 0, 0), width=line_width)
    draw.line([(0, 0), (0, marker_size)], fill=(255, 0, 0), width=line_width)
    
    # Top-right
    draw.line([(width-1, 0), (width-marker_size-1, 0)], fill=(255, 0, 0), width=line_width)
    draw.line([(width-1, 0), (width-1, marker_size)], fill=(255, 0, 0), width=line_width)
    
    # Bottom-left
    draw.line([(0, height-1), (marker_size, height-1)], fill=(255, 0, 0), width=line_width)
    draw.line([(0, height-1), (0, height-marker_size-1)], fill=(255, 0, 0), width=line_width)
    
    # Bottom-right
    draw.line([(width-1, height-1), (width-marker_size-1, height-1)], fill=(255, 0, 0), width=line_width)
    draw.line([(width-1, height-1), (width-1, height-marker_size-1)], fill=(255, 0, 0), width=line_width)
    
    # Composite the original image and the overlay
    result = Image.alpha_composite(img.convert('RGBA'), overlay)
    
    # Save the result
    result.save(output_path)
    print(f"Added verification overlay: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Process a local image with text overlay")
    parser.add_argument("image_path", help="Path to the local image file")
    parser.add_argument("--text", default="بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت", 
                        help="Text to overlay on the image")
    parser.add_argument("--language", default="ckb", help="Language code (e.g., 'ckb' for Kurdish)")
    parser.add_argument("--output", default="local_processed.png", help="Output filename")
    
    args = parser.parse_args()
    
    process_local_image(args.image_path, args.text, args.language, args.output)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Supermarket Image Test Script

This script tests the processing of supermarket images with portrait dimensions.
"""

import os
import requests
import io
from PIL import Image, ImageDraw, ImageFont
from image_processing import apply_custom_text, crop_to_fit

def process_supermarket_image(url, width=1080, height=1920, output="supermarket_portrait.png"):
    """Process a supermarket image with portrait dimensions"""
    # Download the image
    print(f"Downloading image from: {url}")
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    print(f"Original image dimensions: {img.width}x{img.height}")
    
    # Save the original for reference
    original_path = "original_supermarket.jpg"
    img.save(original_path)
    print(f"Original image saved to: {original_path}")
    
    # Crop to target dimensions
    img = crop_to_fit(img, width, height)
    print(f"After cropping: {img.width}x{img.height}")
    
    # Create RGBA tuples for colors
    text_color = (255, 255, 255, 255)  # White
    bg_color = (0, 0, 0, int(0.7 * 255))  # Black with 70% opacity
    
    # Apply text
    text = "بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت"
    language = "ckb"
    padding = {"top": 20, "right": 20, "bottom": 20, "left": 20}
    container_margin = 20
    bg_curve = 10
    container_width_percent = 100
    
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
    processed_img.save(output)
    print(f"Processed image saved to {output}")
    print(f"Final dimensions: {processed_img.width}x{processed_img.height}")
    
    # Add verification overlay
    add_verification_overlay(output)
    
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
    # Use the supermarket image URL
    url = "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1074&auto=format&fit=crop"
    
    # Process with portrait dimensions
    process_supermarket_image(url, 1080, 1920, "supermarket_portrait_verified.png")

if __name__ == "__main__":
    main() 
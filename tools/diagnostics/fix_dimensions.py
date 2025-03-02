#!/usr/bin/env python3
"""
Fix Dimensions Script for Dila Headless Image Editor

This script processes an image with properly enforced dimensions and embedded
dimension information to help debug display issues.
"""

import argparse
import requests
import os
from PIL import Image, ImageDraw, ImageFont, ExifTags

def add_dimension_markers(img, width, height):
    """Add visual dimension markers to the image to verify size"""
    draw = ImageDraw.Draw(img)
    
    # Add dimension information at the top
    header_height = 50
    draw.rectangle([(0, 0), (width, header_height)], fill=(0, 0, 0, 180))
    
    try:
        font = ImageFont.truetype("Arial", 24)
    except:
        font = ImageFont.load_default()
        
    draw.text((20, 10), f"Dimensions: {width}x{height} px", fill=(255, 255, 255), font=font)
    
    # Add corner markers
    marker_size = 40
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
    
    return img

def set_dpi_metadata(img_path, dpi=300):
    """Set the DPI metadata in the image file"""
    img = Image.open(img_path)
    
    # Set DPI metadata
    img.info['dpi'] = (dpi, dpi)
    
    # Save with DPI information
    img.save(img_path, dpi=(dpi, dpi))
    
    print(f"Set DPI metadata to {dpi}")

def process_image_with_dimensions(image_url, width, height, text, output_name="fixed_result.png"):
    """Process an image with proper dimensions and add visual verification markers"""
    api_url = "http://localhost:5001/process_custom"
    
    # Use full width container for text
    payload = {
        "image_url": image_url,
        "text": text,
        "language": "ckb",
        "font_family": "Noto Sans Arabic",
        "font_size": 40,
        "text_color": "#FFFFFF",
        "background_color": "#000000",
        "alignment": "bottom-center",
        "padding": {"top": 20, "right": 20, "bottom": 20, "left": 20},
        "bg_opacity": 0.7,
        "bg_curve": 10,
        "container_margin": 20,
        "container_width_percent": 100,
        "width": width,
        "height": height
    }
    
    print(f"Processing image URL: {image_url}")
    print(f"Target dimensions: {width}x{height}")
    
    # Make the API request
    response = requests.post(api_url, json=payload)
    
    if response.status_code != 200:
        print(f"Error calling API: {response.status_code}")
        print(response.text)
        return False
    
    # Save the initial result
    temp_output = "temp_" + output_name
    with open(temp_output, "wb") as f:
        f.write(response.content)
    
    # Open the image and verify dimensions
    img = Image.open(temp_output)
    actual_width, actual_height = img.size
    print(f"Actual dimensions from API: {actual_width}x{actual_height}")
    
    # Force resize if dimensions don't match (shouldn't normally happen)
    if actual_width != width or actual_height != height:
        print(f"WARNING: Image dimensions don't match target. Forcing resize.")
        img = img.resize((width, height), Image.LANCZOS)
    
    # Add dimension markers
    img_with_markers = add_dimension_markers(img, width, height)
    
    # Save the final result with markers
    img_with_markers.save(output_name)
    os.remove(temp_output)  # Clean up temporary file
    
    # Set DPI metadata
    set_dpi_metadata(output_name)
    
    print(f"Processed image saved to {output_name}")
    
    # Get file size
    size_in_bytes = os.path.getsize(output_name)
    size_in_kb = size_in_bytes / 1024
    print(f"File size: {size_in_kb:.2f} KB")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Process image with enforced dimensions")
    parser.add_argument("--url", default="https://cdn.pixabay.com/photo/2016/11/22/19/08/hangers-1850082_1280.jpg", 
                         help="Image URL to process")
    parser.add_argument("--width", type=int, default=1080, help="Width in pixels")
    parser.add_argument("--height", type=int, default=1920, help="Height in pixels")
    parser.add_argument("--text", default="بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت", 
                        help="Text to overlay on the image")
    parser.add_argument("--output", default="fixed_result.png", help="Output filename")
    
    args = parser.parse_args()
    
    process_image_with_dimensions(args.url, args.width, args.height, args.text, output_name=args.output)

if __name__ == "__main__":
    main() 
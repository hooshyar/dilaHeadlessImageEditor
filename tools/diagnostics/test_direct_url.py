#!/usr/bin/env python3
"""
Direct URL Testing Script for Dila Headless Image Editor

This script tests the API with a specific image URL and portrait dimensions.
"""

import argparse
import requests
import os

def test_image_url(image_url, width, height, text, language="ckb", output_name="result.png"):
    """Test the API with a specific image URL and dimensions"""
    api_url = "http://localhost:5001/process_custom"
    
    payload = {
        "image_url": image_url,
        "text": text,
        "language": language,
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
    
    print(f"Testing with image URL: {image_url}")
    print(f"Dimensions: {width}x{height}")
    
    # Make the API request
    response = requests.post(api_url, json=payload)
    
    if response.status_code != 200:
        print(f"Error calling API: {response.status_code}")
        print(response.text)
        return False
    
    # Save the result
    with open(output_name, "wb") as f:
        f.write(response.content)
    
    print(f"Processed image saved to {output_name}")
    
    # Get file size
    size_in_bytes = os.path.getsize(output_name)
    size_in_kb = size_in_bytes / 1024
    print(f"File size: {size_in_kb:.2f} KB")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Test API with a specific image URL")
    parser.add_argument("--url", default="https://cdn.pixabay.com/photo/2016/11/22/19/08/hangers-1850082_1280.jpg", 
                         help="Image URL to process")
    parser.add_argument("--width", type=int, default=1080, help="Width in pixels")
    parser.add_argument("--height", type=int, default=1920, help="Height in pixels")
    parser.add_argument("--text", default="بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت", 
                        help="Text to overlay on the image")
    parser.add_argument("--output", default="direct_result.png", help="Output filename")
    
    args = parser.parse_args()
    
    test_image_url(args.url, args.width, args.height, args.text, output_name=args.output)

if __name__ == "__main__":
    main() 
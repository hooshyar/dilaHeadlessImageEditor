#!/usr/bin/env python3
"""
Dimension Testing Script for Dila Headless Image Editor

This script tests image dimension handling with visual verification.
It creates a test image with gridlines to clearly show the dimensions.
"""

import sys
import json
import os
import requests
from PIL import Image, ImageDraw, ImageFont

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
            draw.text((10, y+5), f"y={y}", fill=(0, 0, 0))
    
    # Draw vertical lines
    for x in range(grid_spacing, width, grid_spacing):
        line_color = (0, 0, 200) if x % 500 == 0 else (200, 200, 200)
        line_width = 2 if x % 500 == 0 else 1
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
        # Label major gridlines
        if x % 500 == 0:
            draw.text((x+5, 10), f"x={x}", fill=(0, 0, 0))
    
    # Add dimension information at the top
    draw.rectangle([(0, 0), (width, 40)], fill=(0, 0, 0))
    draw.text((10, 10), f"Dimensions: {width}x{height} px", fill=(255, 255, 255))
    
    # Save the image
    img.save(output_path)
    print(f"Created test image with dimensions {width}x{height} at {output_path}")
    return output_path

def test_dimensions(width, height, text, language="ckb", container_width_percent=100):
    """Test the image processing API with specific dimensions"""
    # First create a test image with gridlines
    test_image_path = create_dimension_test_image(width, height)
    
    # Upload the test image to a temporary hosting service
    # This is a simple approach - in production, you'd use your own storage
    files = {'image': open(test_image_path, 'rb')}
    upload_response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
    
    if upload_response.status_code != 200:
        print("Error uploading test image")
        return
    
    # Parse the response to get the URL
    upload_data = upload_response.json()
    file_url = upload_data.get('data', {}).get('url', '')
    
    if not file_url:
        print("Failed to get URL for uploaded image")
        return
    
    # Convert the share URL to a direct URL
    direct_url = file_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
    print(f"Test image uploaded to: {direct_url}")
    
    # Now test the API with this image
    api_url = "http://localhost:5001/process_custom"
    
    payload = {
        "image_url": direct_url,
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
        "container_width_percent": container_width_percent,
        "width": width,
        "height": height
    }
    
    # Make the API request
    response = requests.post(api_url, json=payload)
    
    if response.status_code != 200:
        print(f"Error calling API: {response.status_code}")
        print(response.text)
        return
    
    # Save the result
    output_filename = f"result_{width}x{height}.png"
    with open(output_filename, "wb") as f:
        f.write(response.content)
    
    print(f"Processed image saved to {output_filename}")
    print(f"Check that the result has dimensions {width}x{height}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_dimensions.py <width> <height> [text]")
        print("Example: python test_dimensions.py 1080 1920 'My test text'")
        sys.exit(1)
    
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    text = sys.argv[3] if len(sys.argv) > 3 else "بەرەو خۆر هەنگاو بنێ، سێبەرەکان دەکەونە پشتت"
    
    test_dimensions(width, height, text) 
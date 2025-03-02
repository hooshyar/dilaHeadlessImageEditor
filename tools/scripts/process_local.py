#!/usr/bin/env python3
"""
Local Image Processing Script

This script processes local images without requiring the API or web server to be running.
It demonstrates how to use the core image processing functionality directly.
"""

import os
import sys
import argparse
import datetime
import logging
from pathlib import Path

# Better path handling to support both direct execution and symbolic links
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
project_root = os.path.abspath(os.path.join(script_dir, '../..'))
sys.path.insert(0, project_root)

from PIL import Image, ImageDraw, ImageFont
from app.core.image_processing import apply_custom_text, crop_to_fit
from app.core.font_utils import get_font, get_available_fonts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('process_local.log')
    ]
)

logger = logging.getLogger(__name__)

def process_local_image(image_path, text, language, output_path, 
                       font_family=None, font_size=36, 
                       text_color=(255, 255, 255, 255),
                       bg_color=(0, 0, 0, 180),
                       alignment='bottom-center',
                       padding=20,
                       bg_curve=10,
                       container_margin=20,
                       container_width_percent=90,
                       target_width=None,
                       target_height=None):
    """
    Process a local image by adding text overlay
    
    Args:
        image_path (str): Path to the input image
        text (str): Text to overlay
        language (str): Language code (e.g., 'en', 'ckb')
        output_path (str): Path to save the output image
        font_family (str, optional): Font family name
        font_size (int, optional): Font size in pixels
        text_color (tuple, optional): RGBA text color
        bg_color (tuple, optional): RGBA background color
        alignment (str, optional): Text alignment (e.g., 'bottom-center')
        padding (int or dict, optional): Padding for text container
        bg_curve (int, optional): Corner radius for text background
        container_margin (int, optional): Margin for text container
        container_width_percent (int, optional): Width percentage of container
        target_width (int, optional): Target width for resizing
        target_height (int, optional): Target height for resizing
    
    Returns:
        str: Path to the processed image
    """
    logger.info(f"Processing local image: {image_path}")
    
    # Set default font family if not provided
    if font_family is None:
        if language in ['ar', 'arabic', 'ckb', 'kurdish', 'he', 'hebrew', 'ur', 'urdu']:
            font_family = 'Noto Sans Arabic'
        else:
            font_family = 'Roboto'
    
    # Load the image
    try:
        image = Image.open(image_path)
        logger.info(f"Image loaded successfully. Size: {image.width}x{image.height}")
    except Exception as e:
        logger.error(f"Error loading image: {e}")
        return None
    
    # Resize/crop if target dimensions are provided
    if target_width and target_height:
        image = crop_to_fit(image, target_width, target_height)
        logger.info(f"Image resized to {target_width}x{target_height}")
    
    # Apply text overlay
    result = apply_custom_text(
        image, text, language, font_family, font_size, text_color, bg_color,
        None, alignment, padding, bg_curve, container_margin, container_width_percent
    )
    
    # Save the result
    result.save(output_path, dpi=(300, 300))
    logger.info(f"Processed image saved to: {output_path}")
    
    return output_path

def add_verification_overlay(image_path, output_path):
    """
    Add a verification overlay to an image showing its dimensions
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the output image
    
    Returns:
        str: Path to the verified image
    """
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Load a font for the text
    try:
        font = get_font('Roboto', 36)
    except:
        font = ImageFont.load_default()
    
    # Draw dimension text
    text = f"{width}x{height}"
    draw.text((width/2, 50), text, fill=(255, 0, 0), font=font, anchor="mt")
    
    # Draw corner markers
    line_length = 50
    line_color = (255, 0, 0)
    line_width = 5
    
    # Top-left corner
    draw.line([(0, 0), (line_length, 0)], fill=line_color, width=line_width)
    draw.line([(0, 0), (0, line_length)], fill=line_color, width=line_width)
    
    # Top-right corner
    draw.line([(width-1, 0), (width-line_length, 0)], fill=line_color, width=line_width)
    draw.line([(width-1, 0), (width-1, line_length)], fill=line_color, width=line_width)
    
    # Bottom-left corner
    draw.line([(0, height-1), (line_length, height-1)], fill=line_color, width=line_width)
    draw.line([(0, height-1), (0, height-line_length)], fill=line_color, width=line_width)
    
    # Bottom-right corner
    draw.line([(width-1, height-1), (width-line_length, height-1)], fill=line_color, width=line_width)
    draw.line([(width-1, height-1), (width-1, height-line_length)], fill=line_color, width=line_width)
    
    # Save the result
    image.save(output_path, dpi=(300, 300))
    logger.info(f"Verification overlay added to: {output_path}")
    
    return output_path

def main():
    """Process local images from command line arguments"""
    parser = argparse.ArgumentParser(description='Process local images with text overlay')
    parser.add_argument('--image', required=True, help='Path to the input image')
    parser.add_argument('--text', required=True, help='Text to overlay')
    parser.add_argument('--language', default='en', help='Language code (e.g., en, ckb)')
    parser.add_argument('--output', help='Path to save the output image')
    parser.add_argument('--font', help='Font family name')
    parser.add_argument('--size', type=int, default=36, help='Font size')
    parser.add_argument('--width', type=int, help='Target width')
    parser.add_argument('--height', type=int, help='Target height')
    parser.add_argument('--verify', action='store_true', help='Add verification overlay')
    
    args = parser.parse_args()
    
    # Set default output path if not provided
    if not args.output:
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"processed_{timestamp}.png"
    else:
        output_path = Path(args.output)
    
    # Process the image
    result_path = process_local_image(
        args.image, args.text, args.language, str(output_path),
        font_family=args.font, font_size=args.size,
        target_width=args.width, target_height=args.height
    )
    
    # Add verification overlay if requested
    if args.verify and result_path:
        verify_path = output_path.with_name(f"{output_path.stem}_verified{output_path.suffix}")
        add_verification_overlay(result_path, str(verify_path))

if __name__ == '__main__':
    main() 
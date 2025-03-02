#!/usr/bin/env python3
"""
API Routes for Dila Headless Image Editor
"""

import os
import time
import uuid
import json
import logging
import requests
from PIL import Image
from io import BytesIO
from flask import Blueprint, request, jsonify, current_app, send_file

from app.core.image_processing import apply_custom_text, crop_to_fit
from app.core.font_utils import get_available_fonts
from app.api.validation import validate_process_custom_request

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "version": "1.0.0"})

@api_bp.route('/fonts', methods=['GET'])
def get_fonts():
    """Get a list of available fonts"""
    fonts = get_available_fonts()
    return jsonify({"fonts": fonts})

@api_bp.route('/process_custom', methods=['POST'])
def process_custom():
    """Process an image with custom text overlay"""
    start_time = time.time()
    
    # Validate request
    validation_result = validate_process_custom_request(request)
    if validation_result['success'] is False:
        return jsonify({"error": validation_result['message']}), 400
    
    # Get request data
    data = request.json
    
    try:
        # Download the image
        image_url = data.get('image_url')
        logger.info(f"Downloading image from: {image_url}")
        response = requests.get(image_url, stream=True)
        
        if response.status_code != 200:
            return jsonify({"error": f"Error downloading image: {response.status_code}"}), 400
        
        # Load the image
        img = Image.open(BytesIO(response.content))
        logger.info(f"Image loaded successfully. Original size: {img.width}x{img.height}")
        
        # Process image dimensions
        target_width = data.get('width', current_app.config['DEFAULT_WIDTH'])
        target_height = data.get('height', current_app.config['DEFAULT_HEIGHT'])
        if target_width != img.width or target_height != img.height:
            logger.info(f"Resizing image to: {target_width}x{target_height}")
            img = crop_to_fit(img, target_width, target_height)
        
        # Extract parameters
        text = data.get('text', '')
        language = data.get('language', 'en')
        font_family = data.get('font_family', current_app.config['DEFAULT_FONT_FAMILY'])
        font_size = data.get('font_size', current_app.config['DEFAULT_FONT_SIZE'])
        text_color = data.get('text_color', '#FFFFFF')
        background_color = data.get('background_color', '#000000')
        text_position = data.get('text_position')
        alignment = data.get('alignment', 'bottom-center')
        padding = data.get('padding', 20)
        bg_curve = data.get('bg_curve', 0)
        container_margin = data.get('container_margin', 0)
        container_width_percent = data.get('container_width_percent', 90)
        
        # Handle text color (convert hex to RGB tuple)
        if isinstance(text_color, str) and text_color.startswith('#'):
            text_color = hex_to_rgba(text_color)
        
        # Handle background color with opacity
        if isinstance(background_color, str) and background_color.startswith('#'):
            bg_opacity = data.get('bg_opacity', 1.0)
            bg_color = hex_to_rgba(background_color, bg_opacity)
        else:
            bg_color = background_color
        
        # Apply text overlay
        processed_img = apply_custom_text(
            img, text, language, font_family, font_size, text_color, bg_color,
            text_position, alignment, padding, bg_curve, container_margin, container_width_percent
        )
        
        # Generate a unique filename
        output_filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(current_app.config['OUTPUT_DIR'], output_filename)
        
        # Save the processed image with DPI information
        processed_img.save(output_path, dpi=(current_app.config['DEFAULT_DPI'], current_app.config['DEFAULT_DPI']))
        
        # Log processing time
        processing_time = time.time() - start_time
        logger.info(f"Image processed successfully in {processing_time:.2f} seconds. Size: {processed_img.width}x{processed_img.height}")
        
        # Return the processed image
        return send_file(output_path, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

def hex_to_rgba(hex_color, alpha=1.0):
    """Convert hex color to RGBA tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    a = int(alpha * 255)
    
    return (r, g, b, a) 
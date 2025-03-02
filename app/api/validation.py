#!/usr/bin/env python3
"""
Request validation utilities for the API
"""

import logging
from flask import current_app

logger = logging.getLogger(__name__)

def validate_process_custom_request(request):
    """
    Validate the request data for the process_custom endpoint
    
    Args:
        request: Flask request object
        
    Returns:
        dict: Validation result with 'success' and 'message' keys
    """
    # Check for JSON data
    if not request.is_json:
        return {
            'success': False,
            'message': 'Request must contain JSON data'
        }
    
    data = request.json
    
    # Required parameters
    if 'image_url' not in data:
        return {
            'success': False,
            'message': 'Missing required parameter: image_url'
        }
    
    # Validate image URL format
    image_url = data.get('image_url')
    if not isinstance(image_url, str) or (
        not image_url.startswith('http://') and 
        not image_url.startswith('https://') and 
        not image_url.startswith('file://')
    ):
        return {
            'success': False,
            'message': 'Invalid image_url format. Must be a valid HTTP, HTTPS, or file URL.'
        }
    
    # Validate padding format if provided
    padding = data.get('padding')
    if padding is not None and not isinstance(padding, (int, dict)):
        return {
            'success': False,
            'message': 'Invalid padding format. Must be an integer or a dictionary with top, right, bottom, left keys.'
        }
    
    # Validate dictionary padding if provided
    if isinstance(padding, dict):
        required_keys = ['top', 'right', 'bottom', 'left']
        for key in required_keys:
            if key not in padding:
                return {
                    'success': False,
                    'message': f'Missing required padding key: {key}'
                }
            if not isinstance(padding[key], (int, float)):
                return {
                    'success': False,
                    'message': f'Invalid padding value for {key}. Must be a number.'
                }
    
    # Optional parameters validation
    # Width and height
    width = data.get('width')
    height = data.get('height')
    
    if width is not None and not isinstance(width, int):
        return {
            'success': False,
            'message': 'Invalid width. Must be an integer.'
        }
    
    if height is not None and not isinstance(height, int):
        return {
            'success': False,
            'message': 'Invalid height. Must be an integer.'
        }
    
    # All validation passed
    return {
        'success': True,
        'message': 'Validation successful'
    } 
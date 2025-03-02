"""
Test script for verifying padding parameter handling in the image processing API.

This script tests both integer and dictionary padding formats to ensure they are
properly handled by the API.
"""

import unittest
import json
import os
from app import app, hex_to_rgba
from image_processing import apply_custom_text
from PIL import Image

class TestPaddingHandling(unittest.TestCase):
    """Test cases for padding parameter handling."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create a test image
        self.test_img = Image.new('RGBA', (800, 600), (100, 100, 100, 255))
        
    def tearDown(self):
        """Clean up after tests."""
        self.app_context.pop()
    
    def test_integer_padding_direct(self):
        """Test integer padding directly with apply_custom_text."""
        padding = 30
        result = apply_custom_text(
            self.test_img.copy(), 
            "Test Text", 
            "en", 
            "Arial", 
            36, 
            (255, 255, 255, 255), 
            (0, 0, 0, 200), 
            None, 
            "center-center", 
            padding,  # Integer padding
            10, 
            20, 
            80
        )
        self.assertIsNotNone(result, "Image processing with integer padding failed")
    
    def test_dict_padding_direct(self):
        """Test dictionary padding directly with apply_custom_text."""
        padding = {"top": 40, "bottom": 20, "left": 30, "right": 30}
        result = apply_custom_text(
            self.test_img.copy(), 
            "Test Text", 
            "en", 
            "Arial", 
            36, 
            (255, 255, 255, 255), 
            (0, 0, 0, 200), 
            None, 
            "center-center", 
            padding,  # Dictionary padding
            10, 
            20, 
            80
        )
        self.assertIsNotNone(result, "Image processing with dictionary padding failed")
    
    def test_process_custom_integer_padding(self):
        """Test /process_custom endpoint with integer padding."""
        # Create test data
        data = {
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            "text": "Test Text",
            "language": "en",
            "font_family": "Arial",
            "font_size": 36,
            "text_color": "#FFFFFF",
            "bg_color": "#000000",
            "padding": 30,  # Integer padding
            "corner_radius": 10
        }
        
        # Send request
        response = self.app.post(
            '/process_custom',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200, "API request with integer padding failed")
    
    def test_process_custom_dict_padding(self):
        """Test /process_custom endpoint with dictionary padding."""
        # Create test data
        data = {
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
            "text": "Test Text",
            "language": "en",
            "font_family": "Arial",
            "font_size": 36,
            "text_color": "#FFFFFF",
            "bg_color": "#000000",
            "padding": {"top": 40, "bottom": 20, "left": 30, "right": 30},  # Dictionary padding
            "corner_radius": 10
        }
        
        # Send request
        response = self.app.post(
            '/process_custom',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200, "API request with dictionary padding failed")

if __name__ == '__main__':
    unittest.main() 
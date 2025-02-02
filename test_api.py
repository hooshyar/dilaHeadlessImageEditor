import requests
import unittest
import os
import json
from PIL import Image, ImageDraw
import io

class TestImageEditorAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5001"
    TEST_IMAGE_PATH = "images/test.jpg"  # We'll create this
    TEST_LOGO_PATH = "logo.png"  # We'll create this
    
    def setUp(self):
        # Create a test image if it doesn't exist
        if not os.path.exists('images'):
            os.makedirs('images')
            
        # Create test image
        if not os.path.exists(self.TEST_IMAGE_PATH):
            # Create a more complex test image
            img = Image.new('RGB', (400, 300), color='white')
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 350, 250], fill='blue')
            draw.ellipse([100, 100, 300, 200], fill='red')
            img.save(self.TEST_IMAGE_PATH)
            
        # Create test logo
        if not os.path.exists(self.TEST_LOGO_PATH):
            logo = Image.new('RGBA', (100, 100), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(logo)
            draw.rectangle([10, 10, 90, 90], fill='green')
            draw.ellipse([20, 20, 80, 80], fill='yellow')
            logo.save(self.TEST_LOGO_PATH)
    
    def test_index_endpoint(self):
        """Test the index endpoint"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Welcome to the Image Editor API')
    
    def test_process_local_image(self):
        """Test processing a local image"""
        payload = {
            "image_url": f"http://localhost:5001/images/test.jpg",
            "text": "تاقیکردنەوە"  # "Test" in Kurdish
        }
        response = requests.post(f"{self.BASE_URL}/process", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'image/png')
        
        # Verify the response is a valid image
        img = Image.open(io.BytesIO(response.content))
        self.assertIsInstance(img, Image.Image)
    
    def test_missing_parameters(self):
        """Test error handling for missing parameters"""
        payload = {"text": "Test"}
        response = requests.post(f"{self.BASE_URL}/process", json=payload)
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_image_url(self):
        """Test error handling for invalid image URL"""
        payload = {
            "image_url": "http://invalid-url/image.jpg",
            "text": "Test"
        }
        response = requests.post(f"{self.BASE_URL}/process", json=payload)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main() 
import requests
from PIL import Image
import io

def test_gradient_feature():
    """Test the new gradient text feature"""
    url = "http://localhost:5001/process_custom"
    
    # Test case - Modern social media style image with gradient text
    payload = {
        "image_url": "http://localhost:5001/images/test.jpg",
        "text": "بەخێربێیت بۆ کوردستان",
        "language": "ku",
        "font_family": "NotoSansArabic-Bold",
        "font_size": 40,
        "text_color": "#FFFFFF",
        "background_color": "#222222",  # Solid dark background
        "text_position": None,  # Use default bottom-center
        "alignment": "bottom-center",
        "padding": {
            "top": 25,
            "bottom": 25,
            "left": 30,
            "right": 30
        },
        "bg_curve": 20,
        "bg_opacity": 0.85,
        "gradient_start_color": "#FF3CAC",  # Pink to purple gradient
        "gradient_end_color": "#784BA0",
        "gradient_direction": "horizontal"
    }
    
    print(f"Testing gradient feature with text: {payload['text']}")
    print(f"Using gradient from {payload['gradient_start_color']} to {payload['gradient_end_color']}")
    
    # Send the request
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # Save the processed image
        output_path = "gradient_test_output.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Success! Image saved as {output_path}")
        
        # Verify it's a valid image
        img = Image.open(output_path)
        print(f"Image size: {img.size}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error message: {error_data.get('error')}")
            if 'trace' in error_data:
                print(f"Error trace: {error_data.get('trace')}")
        except:
            print(f"Raw response: {response.text}")

if __name__ == "__main__":
    test_gradient_feature() 
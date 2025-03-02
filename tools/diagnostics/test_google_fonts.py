import requests
from PIL import Image
import io
import time

def test_google_fonts():
    """Test the Google Fonts functionality"""
    # First, get the list of available fonts
    response = requests.get("http://localhost:5001/fonts")
    if response.status_code != 200:
        print("Error getting fonts:", response.text)
        return
    
    fonts_data = response.json()
    print(f"Available local fonts: {len(fonts_data['local_fonts'])}")
    print(f"Available Google Fonts: {len(fonts_data['popular_google_fonts'])}")
    
    # Now test a few different Google Fonts
    test_fonts = [
        "Roboto:700",  # Bold weight
        "Open Sans",   # Regular weight
        "Merriweather:italic",  # Italic style
        "Montserrat:900",  # Black weight
        "Cairo"  # Arabic support
    ]
    
    url = "http://localhost:5001/process_custom"
    
    for font in test_fonts:
        print(f"\nTesting font: {font}")
        
        # Test case with gradient text
        payload = {
            "image_url": "http://localhost:5001/images/test.jpg",
            "text": "Testing Google Fonts بەخێربێیت بۆ کوردستان",
            "language": "ku",
            "font_family": font,
            "font_size": 40,
            "text_color": "#FFFFFF",
            "background_color": "#222222",
            "text_position": None,
            "alignment": "bottom-center",
            "padding": {
                "top": 25,
                "bottom": 25,
                "left": 30,
                "right": 30
            },
            "bg_curve": 20,
            "bg_opacity": 0.85,
            "gradient_start_color": "#FF3CAC",
            "gradient_end_color": "#784BA0",
            "gradient_direction": "horizontal"
        }
        
        # Send the request
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            # Save the processed image
            output_path = f"google_font_test_{font.replace(':', '_')}.png"
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
        
        # Small delay to avoid overwhelming the server
        time.sleep(1)

if __name__ == "__main__":
    test_google_fonts() 
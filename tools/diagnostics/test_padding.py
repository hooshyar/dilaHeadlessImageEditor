import requests
import json
import os
import traceback

# Set the Flask API URL (assuming it's running locally)
API_URL = "http://127.0.0.1:5001/process_custom"

# Test with integer padding
def test_integer_padding():
    try:
        print("Starting integer padding test...")
        payload = {
            "image_url": "http://127.0.0.1:5001/static/sample.jpg",  # Updated port to 5001
            "text": "سڵاو OpenAI - تێستی پەڕاوێزی ژمارەیی",  # Kurdish text with OpenAI
            "language": "ckb",
            "font_family": "Noto Sans Arabic",
            "font_size": 48,
            "text_color": "#FFFFFF",
            "bg_color": "#000066",
            "padding": 30,  # Integer padding
            "corner_radius": 15,
            "gradient_start": "#6600CC",
            "gradient_end": "#003366",
            "gradient_direction": "vertical"
        }
        
        print(f"Sending request to {API_URL} with payload: {json.dumps(payload, indent=2)}")
        
        # Make the API request
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            # Save the response image
            with open("test_integer_padding.png", "wb") as f:
                f.write(response.content)
            print("Integer padding test successful! Image saved as test_integer_padding.png")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception in integer padding test: {str(e)}")
        traceback.print_exc()

# Test with dictionary padding
def test_dict_padding():
    try:
        print("Starting dictionary padding test...")
        payload = {
            "image_url": "http://127.0.0.1:5001/static/sample.jpg",  # Updated port to 5001
            "text": "سڵاو OpenAI - تێستی پەڕاوێزی فەرهەنگی",  # Kurdish text with OpenAI
            "language": "ckb",
            "font_family": "Noto Sans Arabic",
            "font_size": 48,
            "text_color": "#FFFFFF", 
            "bg_color": "#660000",
            "padding": {
                "top": 40,
                "bottom": 20,
                "left": 30,
                "right": 30
            },  # Dictionary padding
            "corner_radius": 15,
            "gradient_start": "#CC0000",
            "gradient_end": "#660000",
            "gradient_direction": "vertical"
        }
        
        print(f"Sending request to {API_URL} with payload: {json.dumps(payload, indent=2)}")
        
        # Make the API request
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            # Save the response image
            with open("test_dict_padding.png", "wb") as f:
                f.write(response.content)
            print("Dictionary padding test successful! Image saved as test_dict_padding.png")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Exception in dictionary padding test: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing padding handling...")
    
    # Make sure we have a sample image
    if not os.path.exists("static"):
        os.makedirs("static")
    
    # Use an existing image if available, otherwise create a placeholder
    sample_path = "static/sample.jpg"
    if not os.path.exists(sample_path):
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1200, 630), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.rectangle([100, 100, 1100, 530], fill=(100, 149, 237))
            img.save(sample_path)
            print(f"Created sample image: {sample_path}")
        except Exception as e:
            print(f"Error creating sample image: {str(e)}")
            traceback.print_exc()
    
    # Run tests
    test_integer_padding()
    test_dict_padding()
    print("Tests completed!") 
import requests
from PIL import Image
import io

def test_kurdish_image():
    # The text to add (a Kurdish phrase meaning "Welcome to Kurdistan")
    text = "توێژینەوەی قوڵی OpenAI: یاریدەدەرێکی شۆڕشگێڕی زیرەکی دەستکرد بۆ توێژینەوە",

    
    # Prepare the request
    url = "http://localhost:5001/process"
    payload = {
        "image_url": "http://localhost:5001/images/0x0.jpg",
        "text": text
    }
    
    # Make the request
    print(f"Processing image with text: {text}")
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # Save the processed image
        output_path = "processed_kurdish.png"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Success! Image saved as {output_path}")
        
        # Verify it's a valid image by trying to open it
        img = Image.open(output_path)
        print(f"Image size: {img.size}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_kurdish_image() 
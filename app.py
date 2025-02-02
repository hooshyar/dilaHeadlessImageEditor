import os
import io
import datetime
from flask import Flask, request, send_file, jsonify, send_from_directory
import requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from urllib.parse import urlparse
import subprocess

app = Flask(__name__)

# Function to append a log entry to logger.txt
def append_log(message):
    log_entry = f"{datetime.datetime.now().isoformat()} - {message}\n"
    with open('logger.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)

# Function to download image from a URL
def download_image(url):
    parsed = urlparse(url)
    # If URL's hostname is localhost/127.0.0.1 and path starts with /images/
    if parsed.hostname in ['127.0.0.1', 'localhost'] and parsed.path.startswith('/images/'):
        filename = parsed.path.split('/images/')[-1]
        local_path = os.path.join('images', filename)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local image file not found: {local_path}")
        with open(local_path, 'rb') as f:
            img_data = f.read()
        img = Image.open(io.BytesIO(img_data)).convert('RGBA')
        img.load()
        return img
    else:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content)).convert('RGBA')
        img.load()
        return img

# Function to add text and logo to the image
# Parameters:
#   base_img: The PIL Image to modify
#   text: The text to overlay. Expected to be in Kurdish Sorani or Arabic.
#   logo_path: Path to the logo image file
# Returns modified PIL Image

def add_text_and_logo(base_img, text, logo_path='logo.png'):
    # For Kurdish Sorani text, we don't need to reverse or reshape
    try:
        # We'll use the text as is, since it's already in the correct form
        display_text = text
        append_log(f"Text preparation successful - Using original text: {text}")
    except Exception as e:
        append_log(f"Error in text preparation: {str(e)}")
        raise

    # Create a drawing context
    draw = ImageDraw.Draw(base_img)
    width, height = base_img.size

    # Use a font that properly supports Kurdish
    try:
        # Try different font paths with preference for Kurdish/Arabic support
        font_paths = [
            '/System/Library/Fonts/Supplemental/Tahoma.ttf',  # Tahoma has good Kurdish support
            '/Library/Fonts/Kurdish.ttf',  # Try Kurdish-specific font if available
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            'arial.ttf'
        ]
        
        font = None
        font_size = int(height * 0.07)  # Increased to 7% of height for better visibility
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, size=font_size)
                append_log(f"Successfully loaded font from: {font_path}")
                break
            except IOError:
                continue
        
        if font is None:
            append_log("Could not load any suitable font, using default")
            font = ImageFont.load_default()
            
    except Exception as e:
        append_log(f"Error loading fonts: {str(e)}")
        font = ImageFont.load_default()

    # Calculate text size and position it at the bottom center with more padding
    text_bbox = draw.textbbox((0, 0), display_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text higher from the bottom with more padding
    bottom_padding = int(height * 0.15)  # Increased to 15% of image height
    text_position = ((width - text_width) / 2, height - text_height - bottom_padding)

    # Draw text with a thicker black outline for better visibility
    outline_range = 5  # Increased outline thickness for better visibility
    outline_color = (0, 0, 0, 255)  # Solid black
    text_color = (255, 255, 255, 255)  # Solid white
    
    # Draw outline
    for x in range(-outline_range, outline_range + 1):
        for y in range(-outline_range, outline_range + 1):
            draw.text((text_position[0] + x, text_position[1] + y), 
                     display_text, font=font, fill=outline_color, align="center")
    
    # Draw main text
    draw.text(text_position, display_text, font=font, fill=text_color, align="center")
    append_log(f"Text rendered at position {text_position} with size {text_width}x{text_height}")

    # Try to add logo if it exists
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert('RGBA')
            # Resize logo to 8% of the base image width (slightly smaller)
            logo_width = int(width * 0.08)
            logo_ratio = logo_width / logo.width
            logo_height = int(logo.height * logo_ratio)
            logo = logo.resize((logo_width, logo_height))
            # Position logo at top-left corner with margin
            margin = int(width * 0.03)  # Increased margin to 3% of width
            base_img.paste(logo, (margin, margin), logo)
            append_log(f"Successfully added logo from {logo_path}")
        except Exception as e:
            append_log(f"Error adding logo: {str(e)}")
    else:
        append_log(f'Logo file {logo_path} not found. Skipping logo overlay.')

    return base_img


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Image Editor API'}), 200


@app.route('/process', methods=['POST'])

def process_image():
    try:
        data = request.get_json()
        image_url = data.get('image_url')
        text = data.get('text')
        if not image_url or not text:
            append_log(f"Missing parameters: image_url={image_url}, text={text}")
            return jsonify({'error': 'Missing image_url or text parameter'}), 400

        append_log(f"Processing request with image_url={image_url}, text={text}")
        
        # Download the image
        try:
            base_img = download_image(image_url)
            append_log(f"Successfully downloaded image from {image_url}")
        except Exception as e:
            append_log(f"Error downloading image from {image_url}: {str(e)}")
            raise

        # Modify the image by adding text and a logo
        try:
            modified_img = add_text_and_logo(base_img, text)
            append_log("Successfully modified image with text and logo")
        except Exception as e:
            append_log(f"Error modifying image: {str(e)}")
            raise

        # Save modified image to a BytesIO stream
        img_io = io.BytesIO()
        modified_img.save(img_io, 'PNG')
        img_io.seek(0)

        append_log(f"Successfully processed image from URL: {image_url} with text: {text}")
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        append_log(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/images/<path:filename>')
# New endpoint to serve static images from the 'images' directory
def serve_image(filename):
    return send_from_directory('images', filename)


def kill_port(port):
    """Kill any process using the specified port."""
    try:
        # Get list of process IDs using the port
        result = subprocess.check_output(["lsof", "-t", "-i", f":{port}"])
        pids = result.decode().strip().splitlines()
        for pid in pids:
            subprocess.call(["kill", "-9", pid])
            append_log(f"Killed process {pid} using port {port}")
    except subprocess.CalledProcessError:
        # No process is using the port
        append_log(f"No process using port {port} found.")
    except Exception as e:
        append_log(f"Error checking port {port}: {str(e)}")


if __name__ == '__main__':
    kill_port(5001)  # Kill any process using port 5001 before starting the server
    append_log("Starting Flask server on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True) 
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
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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
    # Ensure display_text is a string - robust conversion
    if not isinstance(text, str):
        if isinstance(text, (list, tuple)):
            display_text = ' '.join(str(item) for item in text)
        else:
            display_text = str(text)
    else:
        display_text = text
    append_log(f"Text preparation successful - Using original text: {display_text}")

    # Create a drawing context
    draw = ImageDraw.Draw(base_img)
    width, height = base_img.size

    # Use a font that properly supports Kurdish
    try:
        # Try different font paths with preference for Kurdish/Arabic support
        font_paths = [
            'fonts/NotoSansArabic_Condensed-Black.ttf',  # Google Noto Sans Arabic font
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

    # Define overall margins
    outer_margin = 20  # margin from image edges
    padding = 20       # padding inside container

    # Calculate available width for container: image width minus left/right outer margins
    available_container_width = width - 2 * outer_margin
    # Maximum text area width inside container = available container width minus padding on both sides
    available_text_width = available_container_width - 2 * padding

    # Wrap the text to fit within available_text_width
    words = display_text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = word if current_line == "" else current_line + " " + word
        # Measure test_line width
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width <= available_text_width:
            current_line = test_line
        else:
            if current_line == "":
                # Single word too long, force it in
                lines.append(test_line)
                current_line = ""
            else:
                lines.append(current_line)
                current_line = word
    if current_line:
        lines.append(current_line)

    # Join the wrapped lines
    wrapped_text = "\n".join(lines)

    # Recalculate text bounding box using multiline measurement
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Define container dimensions based on wrapped text
    container_width = text_width + 2 * padding
    container_height = text_height + 2 * padding

    # Position the container horizontally centered and above the bottom with outer margins
    bottom_padding = int(height * 0.15)  # 15% of image height padding at bottom
    container_x = (width - container_width) / 2
    # Ensure container is not closer than outer_margin from bottom
    container_y = height - container_height - bottom_padding

    # Text drawing position inside container
    text_position = (container_x + padding, container_y + padding)

    # --- Begin: Insert glossy background for text with curved border and padding ---
    bg_x0 = int(container_x)
    bg_y0 = int(container_y)
    bg_x1 = int(container_x + container_width)
    bg_y1 = int(container_y + container_height)
    bg_width = int(container_width)
    bg_height = int(container_height)

    # Create a gradient background for glossy effect
    bg_image = Image.new('RGBA', (bg_width, bg_height))
    for y in range(bg_height):
        ratio = y / float(bg_height)
        top_color = (255, 255, 255, 230)      # Bright at top
        bottom_color = (200, 200, 200, 230)   # Slightly darker at bottom
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        a = int(top_color[3] * (1 - ratio) + bottom_color[3] * ratio)
        for x in range(bg_width):
            bg_image.putpixel((x, y), (r, g, b, a))

    # Create a rounded rectangle mask for curved borders (radius 20 for smooth corners)
    mask = Image.new('L', (bg_width, bg_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (bg_width, bg_height)], radius=20, fill=255)

    # Create a glossy overlay: a white highlight on the top half that fades out
    gloss_overlay = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss_overlay)
    for y in range(int(bg_height/2)):
        alpha = int(150 * (1 - y/(bg_height/2)))  # Fades from 150 to 0
        gloss_draw.line([(0, y), (bg_width, y)], fill=(255, 255, 255, alpha))
    
    # Composite the glossy overlay with the gradient background
    bg_image = Image.alpha_composite(bg_image, gloss_overlay)

    # Paste the background onto the base image using the rounded mask
    base_img.paste(bg_image, (bg_x0, bg_y0), mask)
    append_log(f"Glossy text background added at {(bg_x0, bg_y0, bg_x1, bg_y1)}")
    # --- End: Glossy background insertion ---

    # Draw main text without stroke
    text_color = (255, 255, 255, 255)  # Solid white
    draw.text(text_position, wrapped_text, font=font, fill=text_color, align="center")
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


# ----------------- New Advanced Processing Functions and Endpoint -----------------

# Helper function: Convert hex color to RGBA tuple
def hex_to_rgba(hex_str, opacity=1.0):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 6:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        a = int(255 * opacity)
        return (r, g, b, a)
    elif len(hex_str) == 3:
        r = int(hex_str[0] * 2, 16)
        g = int(hex_str[1] * 2, 16)
        b = int(hex_str[2] * 2, 16)
        a = int(255 * opacity)
        return (r, g, b, a)
    else:
        raise ValueError('Invalid hex color format')

# Helper function: Crop image to fit target dimensions while maintaining aspect ratio
def crop_to_fit(image, target_width, target_height):
    src_width, src_height = image.size
    src_aspect = src_width / src_height
    target_aspect = target_width / target_height
    if src_aspect > target_aspect:
        # Image is wider than target aspect ratio, crop horizontally
        new_width = int(target_aspect * src_height)
        offset = (src_width - new_width) // 2
        cropped = image.crop((offset, 0, offset + new_width, src_height))
    else:
        # Image is taller than target aspect ratio, crop vertically
        new_height = int(src_width / target_aspect)
        offset = (src_height - new_height) // 2
        cropped = image.crop((0, offset, src_width, offset + new_height))
    return cropped.resize((target_width, target_height), Image.LANCZOS)

# Helper function: Apply custom text with advanced parameters
def apply_custom_text(base_img, text, language, font_family, font_size, text_color, background_color, text_position, alignment, padding, bg_curve, container_margin, container_width_percent):
    draw = ImageDraw.Draw(base_img)
    # Support separate paddings: if padding is a dict, extract individual paddings; otherwise, use uniform padding
    if isinstance(padding, dict):
        pad_top = int(padding.get('top', 0))
        pad_bottom = int(padding.get('bottom', 0))
        pad_left = int(padding.get('left', 0))
        pad_right = int(padding.get('right', 0))
    else:
        pad_top = pad_bottom = pad_left = pad_right = int(padding)

    # Ensure text_position values are integers
    tp_x = int(text_position.get('x', 0))
    tp_y = int(text_position.get('y', 0))

    # Load custom font from fonts directory (expects file in fonts/{font_family}.ttf)
    font_path = f'fonts/{font_family}.ttf'
    try:
        font = ImageFont.truetype(font_path, size=font_size)
        append_log(f"Successfully loaded custom font from: {font_path}")
    except Exception as e:
        append_log(f"Error loading custom font {font_family}: {str(e)}")
        font = ImageFont.load_default()
    
    # Wrap text if needed based on available width (using tp_x as starting x coordinate)
    available_width = base_img.width - tp_x - pad_left - pad_right
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = word if current_line == "" else current_line + " " + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= available_width:
            current_line = test_line
        else:
            if current_line == "":
                lines.append(test_line)
                current_line = ""
            else:
                lines.append(current_line)
                current_line = word
    if current_line:
        lines.append(current_line)
    wrapped_text = "\n".join(lines)
    
    # Get text bounding box with multiline text (centered horizontally as default for measurement)
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Parse alignment string in the format 'vertical-horizontal'
    parts = alignment.split('-')
    if len(parts) == 2:
        vert_align = parts[0].strip().lower()
        horiz_align = parts[1].strip().lower()
    else:
        vert_align = "center"
        horiz_align = "center"
    
    # Use explicit paddings for container dimensions
    top_padding = pad_top
    bottom_padding = pad_bottom
    
    # Compute container dimensions using separate horizontal paddings
    container_width = text_width + pad_left + pad_right
    container_height = text_height + top_padding + bottom_padding
    
    # Container top-left coordinates (anchor using tp_x, tp_y as the nominal starting point for container's top-left)
    container_x = tp_x - pad_left
    container_y = tp_y - top_padding
    # Clamp container coordinates to ensure the entire text overlay remains visible within the image boundaries
    container_x = max(0, min(container_x, base_img.width - container_width))
    container_y = max(0, min(container_y, base_img.height - container_height))
    # Ensure container_x and container_y are integers
    container_x = int(container_x)
    container_y = int(container_y)
    
    # Determine horizontal text position within container
    if horiz_align == "left":
        text_x = container_x + pad_left
    elif horiz_align == "right":
        text_x = container_x + container_width - text_width - pad_right
    else:  # center or default
        text_x = container_x + (container_width - text_width) // 2
    
    # Determine vertical text position within container based on alignment
    if vert_align == "top":
        text_y = container_y + top_padding
    elif vert_align == "bottom":
        text_y = container_y + container_height - text_height - bottom_padding
    else:  # center or default
        text_y = container_y + (container_height - text_height) // 2
    
    # Compute final background box coordinates
    bg_x = container_x
    bg_y = container_y
    bg_w = int(container_width)
    bg_h = int(container_height)
    
    # Create a background image and mask for rounded corners
    bg_image = Image.new('RGBA', (bg_w, bg_h), background_color)
    mask = Image.new('L', (bg_w, bg_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (bg_w, bg_h)], radius=int(bg_curve), fill=255)
    
    # Paste the rounded background onto the base image
    base_img.paste(bg_image, (bg_x, bg_y), mask)
    
    # Draw text on top of the background using the horizontal alignment
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=text_color, align=horiz_align)
    append_log("Custom text applied with parameters.")
    return base_img


# New endpoint for advanced custom processing
@app.route('/process_custom', methods=['POST'])
def process_custom():
    """
    Process custom image endpoint.
    ---
    post:
      summary: Process an image with custom text overlay and advanced styling.
      description: |
        Crops an image to target dimensions and overlays custom text with advanced styling options.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - image_url
                - text
                - language
                - font_family
                - font_size
                - text_color
                - background_color
                - text_position
                - alignment
                - output_dimensions
                - padding
                - text_opacity
                - bg_curve
                - bg_opacity
                - container_margin
                - container_width_percent
              properties:
                image_url:
                  type: string
                text:
                  type: string
                language:
                  type: string
                font_family:
                  type: string
                font_size:
                  type: integer
                text_color:
                  type: string
                background_color:
                  type: string
                text_position:
                  type: object
                  properties:
                    x:
                      type: number
                    y:
                      type: number
                alignment:
                  type: string
                output_dimensions:
                  type: object
                  properties:
                    width:
                      type: integer
                    height:
                      type: integer
                preset:
                  type: string
                padding:
                  type: object
                  properties:
                    top:
                      type: integer
                    bottom:
                      type: integer
                    left:
                      type: integer
                    right:
                      type: integer
                container_margin:
                  type: number
                  description: Additional margin (in pixels) from the image edge for the text container.
                  default: 0
                container_width_percent:
                  type: number
                  description: Specifies the text container's width as a percentage of the image width.
                text_opacity:
                  type: number
                bg_curve:
                  type: number
                bg_opacity:
                  type: number
      responses:
        '200':
          description: Processed image in PNG format
          content:
            image/png:
              schema:
                type: string
                format: binary
        '500':
          description: Processing error
    """
    try:
        append_log("Received /process_custom request with data: " + str(request.get_json()))
        data = request.get_json()
        image_url = data.get('image_url')
        text = data.get('text')
        language = data.get('language')
        font_family = data.get('font_family')
        font_size = data.get('font_size')
        text_color_hex = data.get('text_color')
        bg_color_hex = data.get('background_color')
        text_position = data.get('text_position')
        alignment = data.get('alignment')
        output_dimensions = data.get('output_dimensions')
        preset = data.get('preset')
        padding = data.get('padding')
        text_opacity = data.get('text_opacity', 1.0)
        bg_opacity = data.get('bg_opacity', 1.0)
        bg_curve = data.get('bg_curve')
        container_margin = data.get('container_margin', 0)
        container_width_percent = data.get('container_width_percent')
        
        if image_url.startswith('@'):
            image_url = image_url[1:]
        
        text_color = hex_to_rgba(text_color_hex, opacity=text_opacity)
        background_color = hex_to_rgba(bg_color_hex, opacity=bg_opacity)
        
        if preset:
            preset_lower = preset.lower()
            if preset_lower in ['instagram-stories', 'instagram-reels']:
                output_dimensions = {"width": 1080, "height": 1920}
            elif preset_lower in ['instagram-vertical', 'instagram-feed']:
                output_dimensions = {"width": 1080, "height": 1350}
            elif preset_lower in ['instagram-grid']:
                output_dimensions = {"width": 1080, "height": 1440}
        
        base_img = download_image(image_url)
        if output_dimensions and output_dimensions.get('width') and output_dimensions.get('height'):
            out_width = output_dimensions.get('width')
            out_height = output_dimensions.get('height')
            base_img = crop_to_fit(base_img, out_width, out_height)
        
        custom_img = apply_custom_text(base_img, text, language, font_family, font_size, text_color, background_color, text_position, alignment, padding, bg_curve, container_margin, container_width_percent)
        img_io = io.BytesIO()
        custom_img.save(img_io, 'PNG')
        img_io.seek(0)
        append_log("Successfully processed custom image.")
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        append_log("Error in custom processing: " + tb)
        return jsonify({'error': str(e), 'trace': tb}), 500

# ----------------- End of Advanced Processing Section -----------------

@app.route('/preview', methods=['GET'])
def preview():
    """
    Preview processed image by providing an image URL.
    ---
    get:
      summary: Preview processed image from a provided URL.
      description: |
        If a query parameter 'url' is provided, the endpoint processes the image using default overlay parameters and returns the processed image in PNG format. If not, an HTML form is rendered to input the image URL.
      parameters:
        - in: query
          name: url
          schema:
            type: string
          required: false
          description: The URL of the image to process.
      responses:
        '200':
          description: Processed image in PNG format or an HTML form.
          content:
            image/png:
              schema:
                type: string
                format: binary
            text/html:
              schema:
                type: string
        '500':
          description: Processing error
    """
    url_param = request.args.get('url')
    if not url_param:
        return '''
        <html>
         <body>
           <form action="/preview" method="get">
             Image URL: <input type="text" name="url">
             <input type="submit" value="Preview">
           </form>
         </body>
       </html>
        '''
    
    # Default parameters for processing
    payload = {
        "image_url": url_param,
        "text": "Default Overlay",
        "language": "en",
        "font_family": "Arial",
        "font_size": 36,
        "text_color": "#FFFFFF",
        "background_color": "#000000",
        "text_position": {"x": 50, "y": 100},
        "alignment": "center",
        "output_dimensions": {"width": 1080, "height": 1080},
        "preset": "",
        "padding": 10,
        "text_opacity": 1.0,
        "bg_curve": 20,
        "bg_opacity": 0.8
    }
    try:
        # Download the image
        base_img = download_image(url_param)
        # Crop image to default dimensions
        base_img = crop_to_fit(base_img, payload['output_dimensions']['width'], payload['output_dimensions']['height'])
        # Apply custom text overlay with default parameters
        custom_img = apply_custom_text(
            base_img,
            payload['text'],
            payload['language'],
            payload['font_family'],
            payload['font_size'],
            hex_to_rgba(payload['text_color'], opacity=payload['text_opacity']),
            hex_to_rgba(payload['background_color'], opacity=payload['bg_opacity']),
            payload['text_position'],
            payload['alignment'],
            payload['padding'],
            payload['bg_curve'],
            payload['container_margin'],
            payload['container_width_percent']
        )
        img_io = io.BytesIO()
        custom_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # kill_port(5001)  # Disabled in development mode to allow auto-reload
    append_log("Starting Flask server on port 5001 in development mode with auto-reload enabled")
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True) 
import datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Import append_log function from app.py
try:
    from app import append_log
except ImportError:
    # Fallback if direct import fails
    def append_log(message):
        log_entry = f"{datetime.datetime.now().isoformat()} - {message}\n"
        with open('logger.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)

# Import font utilities
import font_utils

def crop_to_fit(image, target_width, target_height):
    # Debug: Log target dimensions and their types
    append_log(f"crop_to_fit: Received target_width={target_width} (type: {type(target_width)}), target_height={target_height} (type: {type(target_height)})")
    src_width, src_height = image.size
    append_log(f"crop_to_fit: Source image dimensions: {src_width}x{src_height}")
    src_aspect = src_width / src_height
    target_aspect = target_width / target_height
    if src_aspect > target_aspect:
        new_width = int(target_aspect * src_height)
        offset = (src_width - new_width) // 2
        append_log(f"crop_to_fit: Horizontal crop chosen. new_width={new_width}, offset={offset}")
        cropped = image.crop((offset, 0, offset + new_width, src_height))
    else:
        new_height = int(src_width / target_aspect)
        offset = (src_height - new_height) // 2
        append_log(f"crop_to_fit: Vertical crop chosen. new_height={new_height}, offset={offset}")
        cropped = image.crop((0, offset, src_width, offset + new_height))
    final_width, final_height = int(target_width), int(target_height)
    append_log(f"crop_to_fit: Resizing cropped image to: {final_width}x{final_height}")
    return cropped.resize((final_width, final_height), Image.LANCZOS)

def apply_custom_text(base_img, text, language, font_family, font_size, text_color, background_color, text_position, alignment, padding, bg_curve, container_margin, container_width_percent, gradient_colors=None, gradient_direction="vertical"):
    from PIL import ImageFont, ImageDraw, Image
    import math
    draw = ImageDraw.Draw(base_img)
    append_log(f"apply_custom_text: container_margin={container_margin}, container_width_percent={container_width_percent}")
    
    # Handle RTL languages (Arabic, Kurdish, etc.)
    is_rtl = False
    if language and language.lower() in ['ar', 'arabic', 'ckb', 'kurdish', 'he', 'hebrew', 'ur', 'urdu']:
        is_rtl = True
        append_log(f"Processing RTL text for language: {language}")
        display_text = text
        append_log(f"Using original text for RTL rendering: {display_text}")
    else:
        display_text = text
    
    # Ensure container_margin is an integer
    container_margin = int(container_margin) if container_margin is not None else 0
    
    # Handle padding
    if isinstance(padding, dict):
        pad_top = int(padding.get('top', 0))
        pad_bottom = int(padding.get('bottom', 0))
        pad_left = int(padding.get('left', 0))
        pad_right = int(padding.get('right', 0))
    else:
        pad_top = pad_bottom = pad_left = pad_right = int(padding)

    # Parse font family for Google Fonts format: Family:weight
    font_weight = 400
    font_style = 'normal'
    if ':' in font_family:
        parts = font_family.split(':')
        font_family = parts[0]
        # Handle weight and style specifications if provided
        if len(parts) > 1:
            options = parts[1]
            if 'italic' in options:
                font_style = 'italic'
                options = options.replace('italic', '')
            if options:
                try:
                    font_weight = int(options)
                except ValueError:
                    append_log(f"Invalid font weight: {options}, defaulting to 400")

    # Load font using font_utils
    try:
        font_path = font_utils.get_font_path(font_family, font_weight, font_style)
        if font_path:
            font = ImageFont.truetype(font_path, size=font_size)
            append_log(f"Successfully loaded font: {font_family} (weight:{font_weight}, style:{font_style})")
        else:
            # Fall back to default font
            append_log(f"Font {font_family} not found, using default font")
            font = ImageFont.load_default()
    except Exception as e:
        append_log(f"Error loading font {font_family}: {str(e)}")
        font = ImageFont.load_default()

    # Parse alignment - default to bottom-center if not specified
    parts = alignment.split('-')
    if len(parts) == 2:
        vert_align = parts[0].strip().lower()
        horiz_align = parts[1].strip().lower()
    else:
        vert_align = "bottom"  # Default to bottom
        horiz_align = "center"  # Default to center

    # If text_position is None or empty, set default position at bottom center
    if not text_position or (isinstance(text_position, dict) and not text_position.get('x') and not text_position.get('y')):
        # Position at bottom center with some padding from bottom
        bottom_margin = int(base_img.height * 0.1)  # 10% margin from bottom
        text_position = {
            'x': base_img.width // 2,
            'y': base_img.height - bottom_margin
        }
        # Also set alignment to bottom-center
        vert_align = "bottom"
        horiz_align = "center"

    # Define minimum bottom margin (at least 20px)
    MIN_BOTTOM_MARGIN = 20

    # Preliminary check of text size to ensure font size is appropriate
    test_text = display_text
    test_bbox = draw.textbbox((0, 0), test_text, font=font)
    test_text_width = test_bbox[2] - test_bbox[0]
    
    # Calculate max available width (80% of image width as a safety)
    max_available_width = base_img.width * 0.8
    
    # If initial text width is too large, reduce font size
    if test_text_width > max_available_width and font_size > 16:
        scaling_factor = max_available_width / test_text_width
        new_font_size = max(int(font_size * scaling_factor * 0.9), 16)  # Keep font readable
        append_log(f"Text too wide ({test_text_width}px), reducing font size from {font_size} to {new_font_size}")
        font_size = new_font_size
        # Reload font with new size
        try:
            font = ImageFont.truetype(font_path, size=font_size)
        except Exception:
            font = ImageFont.load_default()

    if container_width_percent is not None:
        # Calculate container width based on percentage of the image width
        # For 100%, we want true full width (ignoring container_margin)
        if container_width_percent >= 100:
            target_container_width = base_img.width
            container_x = 0  # Start at the left edge for full width
        else:
            # For less than 100%, respect the container_margin
            target_container_width = (base_img.width - 2 * container_margin) * (container_width_percent / 100.0)
            # Position container based on alignment and container_margin
            if horiz_align == "left":
                container_x = container_margin
            elif horiz_align == "right":
                container_x = base_img.width - target_container_width - container_margin
            else:
                container_x = (base_img.width - target_container_width) / 2

        # Calculate available width for text inside the container
        available_text_width = target_container_width - pad_left - pad_right
        
        # Wrap text to fit within available_text_width - using improved wrapping for RTL languages
        # For RTL languages, we need special handling
        if is_rtl:
            # Improved word splitting for RTL text (using space but preserving words)
            words = []
            current_word = ""
            for char in display_text:
                if char == ' ':
                    if current_word:
                        words.append(current_word)
                        current_word = ""
                    words.append(' ')
                else:
                    current_word += char
            if current_word:
                words.append(current_word)
                
            lines = []
            current_line = ""
            for word in words:
                if word == ' ' and current_line == "":
                    continue  # Skip leading spaces
                
                test_line = current_line + word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]
                
                if line_width <= available_text_width:
                    current_line = test_line
                else:
                    # Don't start a new line with just a space
                    if word == ' ':
                        if current_line:
                            lines.append(current_line)
                            current_line = ""
                    # If current line is empty, we have a word longer than available width
                    elif current_line == "":
                        # Split the word into characters if necessary
                        char_line = ""
                        for char in word:
                            test_char_line = char_line + char
                            bbox = draw.textbbox((0, 0), test_char_line, font=font)
                            if (bbox[2] - bbox[0]) <= available_text_width:
                                char_line = test_char_line
                            else:
                                if char_line:
                                    lines.append(char_line)
                                char_line = char
                        if char_line:
                            lines.append(char_line)
                    else:
                        lines.append(current_line)
                        current_line = word
        else:
            # Standard text wrapping for LTR languages
            words = display_text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = word if current_line == "" else current_line + " " + word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]
                
                if line_width <= available_text_width:
                    current_line = test_line
                else:
                    if current_line == "":
                        # Handle case where a single word is too long
                        char_line = ""
                        for char in word:
                            test_char_line = char_line + char
                            bbox = draw.textbbox((0, 0), test_char_line, font=font)
                            if (bbox[2] - bbox[0]) <= available_text_width:
                                char_line = test_char_line
                            else:
                                if char_line:
                                    lines.append(char_line)
                                char_line = char
                        if char_line:
                            lines.append(char_line)
                    else:
                        lines.append(current_line)
                        current_line = word
        
        # Add the last line if there's content
        if current_line:
            lines.append(current_line)

        # Join the lines with newlines
        wrapped_text = "\n".join(lines)
        
        # Recalculate text dimensions with the wrapped text for accurate container sizing
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Ensure container is wide enough for the text plus padding
        actual_container_width = max(target_container_width, text_width + pad_left + pad_right)
        container_width = actual_container_width
        container_height = text_height + pad_top + pad_bottom
        
        # Re-center the container if needed
        if actual_container_width > target_container_width and horiz_align == "center":
            container_x = (base_img.width - actual_container_width) / 2
        
        # Vertical positioning
        if vert_align == "top":
            container_y = container_margin
        elif vert_align == "bottom":
            # Ensure at least MIN_BOTTOM_MARGIN pixels from bottom
            container_y = base_img.height - container_height - max(container_margin, MIN_BOTTOM_MARGIN)
        else:
            container_y = (base_img.height - container_height) / 2

    else:
        # Use provided text_position as anchor but respect container_margin
        tp_x = int(text_position.get('x', 0))
        tp_y = int(text_position.get('y', 0))
        
        # Calculate available width considering margins
        available_text_width = base_img.width - max(tp_x, container_margin) - pad_left - pad_right - container_margin

        # Use the improved text wrapping logic for both RTL and LTR languages
        if is_rtl:
            # Split RTL text appropriately
            words = []
            current_word = ""
            for char in display_text:
                if char == ' ':
                    if current_word:
                        words.append(current_word)
                        current_word = ""
                    words.append(' ')
                else:
                    current_word += char
            if current_word:
                words.append(current_word)
        else:
            words = display_text.split()
            
        lines = []
        current_line = ""
        
        for word in words:
            if is_rtl and word == ' ' and current_line == "":
                continue  # Skip leading spaces for RTL
                
            test_line = word if current_line == "" else (current_line + word if is_rtl else current_line + " " + word)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width <= available_text_width:
                current_line = test_line
            else:
                if current_line == "":
                    # Handle case where a single word is too long
                    char_line = ""
                    for char in word:
                        test_char_line = char_line + char
                        bbox = draw.textbbox((0, 0), test_char_line, font=font)
                        if (bbox[2] - bbox[0]) <= available_text_width:
                            char_line = test_char_line
                        else:
                            if char_line:
                                lines.append(char_line)
                            char_line = char
                    if char_line:
                        lines.append(char_line)
                else:
                    lines.append(current_line)
                    current_line = word
        
        if current_line:
            lines.append(current_line)
            
        wrapped_text = "\n".join(lines)

        # Calculate text dimensions for container sizing
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Ensure container is properly sized to fit text
        container_width = text_width + pad_left + pad_right
        container_height = text_height + pad_top + pad_bottom
        
        # Adjust positioning for bottom center if that's the alignment
        if vert_align == "bottom" and horiz_align == "center":
            container_x = (base_img.width - container_width) / 2
            # Ensure at least MIN_BOTTOM_MARGIN pixels from bottom
            container_y = base_img.height - container_height - max(container_margin, MIN_BOTTOM_MARGIN)
        else:
            # Position container while respecting margins
            container_x = max(container_margin, min(tp_x - pad_left, base_img.width - container_width - container_margin))
            # Ensure at least MIN_BOTTOM_MARGIN pixels from bottom if aligned to bottom
            if vert_align == "bottom":
                container_y = max(container_margin, min(tp_y - pad_top, base_img.height - container_height - MIN_BOTTOM_MARGIN))
            else:
                container_y = max(container_margin, min(tp_y - pad_top, base_img.height - container_height - container_margin))

    # Ensure container stays within image boundaries
    container_width = min(container_width, base_img.width - 2 * container_margin)
    container_x = max(container_margin, min(container_x, base_img.width - container_width - container_margin))
    
    # Cast coordinates to int
    container_x = int(container_x)
    container_y = int(container_y)
    container_width = int(container_width)
    container_height = int(container_height)

    # Determine text position within container
    if horiz_align == "left":
        text_x = container_x + pad_left
    elif horiz_align == "right":
        text_x = container_x + container_width - text_width - pad_right
    else:
        text_x = container_x + (container_width - text_width) // 2

    if vert_align == "top":
        text_y = container_y + pad_top
    elif vert_align == "bottom":
        text_y = container_y + container_height - text_height - pad_bottom
    else:
        text_y = container_y + (container_height - text_height) // 2

    # Cast text coordinates to int
    text_x = int(text_x)
    text_y = int(text_y)

    # Create background with rounded corners and gradient
    bg_x = container_x
    bg_y = container_y
    bg_w = container_width
    bg_h = container_height

    # Create a gradient background
    bg_image = Image.new('RGBA', (bg_w, bg_h), (0, 0, 0, 0))
    
    # Parse gradient colors or use the background_color if gradient not specified
    if gradient_colors:
        # If single color is provided, create a gradient from that color to a darker version
        if isinstance(gradient_colors, str) or len(gradient_colors) == 1:
            color1 = background_color if isinstance(gradient_colors, str) else gradient_colors[0]
            # Create a darker version of the color for the gradient
            r, g, b, a = color1
            color2 = (max(0, r-50), max(0, g-50), max(0, b-50), a)
        elif len(gradient_colors) >= 2:
            color1 = gradient_colors[0]
            color2 = gradient_colors[1]
        
        # Create gradient background
        if gradient_direction == "horizontal":
            for x in range(bg_w):
                ratio = x / float(bg_w)
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                a = int(color1[3] * (1 - ratio) + color2[3] * ratio)
                for y in range(bg_h):
                    bg_image.putpixel((x, y), (r, g, b, a))
        else:  # vertical gradient (default)
            for y in range(bg_h):
                ratio = y / float(bg_h)
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                a = int(color1[3] * (1 - ratio) + color2[3] * ratio)
                for x in range(bg_w):
                    bg_image.putpixel((x, y), (r, g, b, a))
    else:
        # Use solid background color if no gradient specified
        bg_image = Image.new('RGBA', (bg_w, bg_h), background_color)
        
        # Add a subtle gradient effect even for solid colors
        overlay = Image.new('RGBA', (bg_w, bg_h), (0, 0, 0, 0))
        for y in range(bg_h):
            alpha = int(50 * (1 - y/(bg_h)))  # Subtle darkening at the bottom
            for x in range(bg_w):
                overlay.putpixel((x, y), (0, 0, 0, alpha))
        bg_image = Image.alpha_composite(bg_image, overlay)

    # Create a glossy finish effect
    gloss = Image.new('RGBA', (bg_w, bg_h), (0, 0, 0, 0))
    for y in range(bg_h // 3):  # Only top third gets the gloss
        alpha = int(40 * (1 - y/(bg_h/3)))  # Fade out the gloss
        for x in range(bg_w):
            gloss.putpixel((x, y), (255, 255, 255, alpha))
    bg_image = Image.alpha_composite(bg_image, gloss)

    # Create mask for rounded corners
    mask = Image.new('L', (bg_w, bg_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    # When using full width (container_width_percent=100), only round the corners if explicitly requested
    if container_width_percent >= 100 and bg_x == 0:
        # For full width containers at the edge, only round corners if requested with bg_curve > 0
        radius = 0 if bg_curve is None or bg_curve == 0 else int(bg_curve)
    else:
        # For other containers, use default radius if not specified
        radius = 10 if bg_curve is None else int(bg_curve)
        
    mask_draw.rounded_rectangle([(0, 0), (bg_w, bg_h)], radius=radius, fill=255)
    
    # Paste the background onto the base image
    base_img.paste(bg_image, (bg_x, bg_y), mask)
    
    # Draw text on top of the background
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=text_color, align=horiz_align)
    
    # Log positioning information
    append_log(f"Custom text applied with background at ({bg_x},{bg_y}) size {bg_w}x{bg_h}, bottom margin: {base_img.height - (bg_y + bg_h)}px")
    append_log(f"Text dimensions: {text_width}x{text_height}, wrapped into {len(lines)} lines")
    
    return base_img 
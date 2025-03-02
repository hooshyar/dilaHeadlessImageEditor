#!/usr/bin/env python3
"""
Image processing functionality for Dila Headless Image Editor
"""

import os
import math
import logging
from PIL import Image, ImageDraw, ImageColor
import arabic_reshaper
from bidi.algorithm import get_display

from app.core.font_utils import get_font

logger = logging.getLogger(__name__)

def crop_to_fit(img, target_width, target_height):
    """
    Crop and resize an image to fit the target dimensions
    
    Args:
        img (PIL.Image): The source image
        target_width (int): Target width in pixels
        target_height (int): Target height in pixels
        
    Returns:
        PIL.Image: Resized and cropped image
    """
    # Log target dimensions
    logger.info(f"Resizing/cropping image to {target_width}x{target_height}")
    
    src_width, src_height = img.size
    logger.debug(f"Source image dimensions: {src_width}x{src_height}")
    
    src_aspect = src_width / src_height
    target_aspect = target_width / target_height
    
    if src_aspect > target_aspect:
        # Source image is wider than target aspect ratio
        new_width = int(target_aspect * src_height)
        offset = (src_width - new_width) // 2
        logger.debug(f"Horizontal crop chosen. new_width={new_width}, offset={offset}")
        cropped = img.crop((offset, 0, offset + new_width, src_height))
    else:
        # Source image is taller than target aspect ratio
        new_height = int(src_width / target_aspect)
        offset = (src_height - new_height) // 2
        logger.debug(f"Vertical crop chosen. new_height={new_height}, offset={offset}")
        cropped = img.crop((0, offset, src_width, offset + new_height))
    
    # Resize to target dimensions
    final_width, final_height = int(target_width), int(target_height)
    logger.debug(f"Resizing cropped image to: {final_width}x{final_height}")
    return cropped.resize((final_width, final_height), Image.LANCZOS)

def _process_padding(padding):
    """
    Process padding parameter to ensure it's in the correct format
    
    Args:
        padding: Integer or dictionary with top, right, bottom, left keys
        
    Returns:
        dict: Dictionary with top, right, bottom, left keys
    """
    if isinstance(padding, dict):
        # Ensure all required keys are present
        for key in ['top', 'right', 'bottom', 'left']:
            if key not in padding:
                padding[key] = 0
        return padding
    else:
        # Convert integer to dictionary
        padding_value = int(padding)
        return {
            'top': padding_value,
            'right': padding_value,
            'bottom': padding_value,
            'left': padding_value
        }

def create_gradient_background(width, height, colors, direction="vertical"):
    """
    Create a gradient background image
    
    Args:
        width (int): Width of the background
        height (int): Height of the background
        colors (list): List of RGB or RGBA color tuples
        direction (str): Gradient direction ('vertical', 'horizontal', 'diagonal')
        
    Returns:
        PIL.Image: Gradient background image
    """
    if not colors or len(colors) < 2:
        logger.warning("Not enough colors provided for gradient, falling back to single color")
        bg = Image.new('RGBA', (width, height), colors[0] if colors else (0, 0, 0, 255))
        return bg
    
    # Create a blank RGBA image
    gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)
    
    # Convert hex colors to RGBA if needed
    rgba_colors = []
    for color in colors:
        if isinstance(color, str) and color.startswith('#'):
            if len(color) == 7:  # #RRGGBB
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                rgba_colors.append((r, g, b, 255))
            elif len(color) == 9:  # #RRGGBBAA
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                a = int(color[7:9], 16)
                rgba_colors.append((r, g, b, a))
        else:
            rgba_colors.append(color)
    
    # Ensure we have at least 2 colors
    if len(rgba_colors) < 2:
        rgba_colors.append(rgba_colors[0])
    
    # Draw the gradient
    if direction == "vertical":
        for y in range(height):
            # Calculate the color at this position
            r = int(rgba_colors[0][0] + (rgba_colors[1][0] - rgba_colors[0][0]) * y / height)
            g = int(rgba_colors[0][1] + (rgba_colors[1][1] - rgba_colors[0][1]) * y / height)
            b = int(rgba_colors[0][2] + (rgba_colors[1][2] - rgba_colors[0][2]) * y / height)
            a = int(rgba_colors[0][3] + (rgba_colors[1][3] - rgba_colors[0][3]) * y / height)
            
            color = (r, g, b, a)
            draw.line([(0, y), (width, y)], fill=color)
    
    elif direction == "horizontal":
        for x in range(width):
            # Calculate the color at this position
            r = int(rgba_colors[0][0] + (rgba_colors[1][0] - rgba_colors[0][0]) * x / width)
            g = int(rgba_colors[0][1] + (rgba_colors[1][1] - rgba_colors[0][1]) * x / width)
            b = int(rgba_colors[0][2] + (rgba_colors[1][2] - rgba_colors[0][2]) * x / width)
            a = int(rgba_colors[0][3] + (rgba_colors[1][3] - rgba_colors[0][3]) * x / width)
            
            color = (r, g, b, a)
            draw.line([(x, 0), (x, height)], fill=color)
    
    else:  # diagonal
        for i in range(width + height):
            # Calculate the color at this position
            progress = i / (width + height)
            r = int(rgba_colors[0][0] + (rgba_colors[1][0] - rgba_colors[0][0]) * progress)
            g = int(rgba_colors[0][1] + (rgba_colors[1][1] - rgba_colors[0][1]) * progress)
            b = int(rgba_colors[0][2] + (rgba_colors[1][2] - rgba_colors[0][2]) * progress)
            a = int(rgba_colors[0][3] + (rgba_colors[1][3] - rgba_colors[0][3]) * progress)
            
            color = (r, g, b, a)
            draw.line([(0, i), (i, 0)], fill=color)
    
    return gradient

def draw_rounded_rectangle(draw, xy, corner_radius, fill=None, outline=None):
    """
    Draw a rounded rectangle
    
    Args:
        draw (PIL.ImageDraw.Draw): Draw object
        xy (tuple): Position (x0, y0, x1, y1)
        corner_radius (int): Radius of the corners
        fill: Fill color
        outline: Outline color
    """
    x0, y0, x1, y1 = xy
    
    if corner_radius <= 0:
        draw.rectangle(xy, fill=fill, outline=outline)
        return
    
    # Draw the main rectangle
    draw.rectangle((x0, y0 + corner_radius, x1, y1 - corner_radius), fill=fill, outline=None)
    draw.rectangle((x0 + corner_radius, y0, x1 - corner_radius, y1), fill=fill, outline=None)
    
    # Draw the four corners
    draw.pieslice((x0, y0, x0 + corner_radius * 2, y0 + corner_radius * 2), 180, 270, fill=fill, outline=None)
    draw.pieslice((x1 - corner_radius * 2, y0, x1, y0 + corner_radius * 2), 270, 360, fill=fill, outline=None)
    draw.pieslice((x0, y1 - corner_radius * 2, x0 + corner_radius * 2, y1), 90, 180, fill=fill, outline=None)
    draw.pieslice((x1 - corner_radius * 2, y1 - corner_radius * 2, x1, y1), 0, 90, fill=fill, outline=None)
    
    # Draw outline if specified
    if outline:
        draw.arc((x0, y0, x0 + corner_radius * 2, y0 + corner_radius * 2), 180, 270, fill=outline)
        draw.arc((x1 - corner_radius * 2, y0, x1, y0 + corner_radius * 2), 270, 360, fill=outline)
        draw.arc((x0, y1 - corner_radius * 2, x0 + corner_radius * 2, y1), 90, 180, fill=outline)
        draw.arc((x1 - corner_radius * 2, y1 - corner_radius * 2, x1, y1), 0, 90, fill=outline)
        draw.line((x0, y0 + corner_radius, x0, y1 - corner_radius), fill=outline)
        draw.line((x1, y0 + corner_radius, x1, y1 - corner_radius), fill=outline)
        draw.line((x0 + corner_radius, y0, x1 - corner_radius, y0), fill=outline)
        draw.line((x0 + corner_radius, y1, x1 - corner_radius, y1), fill=outline)

def apply_custom_text(img, text, language, font_family, font_size, text_color, bg_color,
                     text_position=None, alignment='bottom-center', padding=20, 
                     bg_curve=0, container_margin=0, container_width_percent=90,
                     gradient_colors=None, gradient_direction="vertical"):
    """
    Apply text overlay with custom styling to an image
    
    Args:
        img (PIL.Image): The source image
        text (str): Text content to overlay
        language (str): Language code
        font_family (str): Font family name
        font_size (int): Font size in pixels
        text_color (tuple): RGB(A) tuple for text color
        bg_color (tuple): RGB(A) tuple for background color
        text_position (dict, optional): Manual position for text
        alignment (str): Alignment position (e.g. 'bottom-center')
        padding (int or dict): Padding values
        bg_curve (int): Corner radius for text background
        container_margin (int): Margin for text container
        container_width_percent (int): Width of text container as percentage of image width
        gradient_colors (list, optional): List of colors for gradient background
        gradient_direction (str): Direction of gradient
        
    Returns:
        PIL.Image: Image with text overlay applied
    """
    logger.info(f"Applying text overlay: '{text[:30]}...' in {language}")
    logger.debug(f"Parameters: font={font_family}, size={font_size}, alignment={alignment}, "
                f"container_margin={container_margin}, container_width_percent={container_width_percent}")
    
    # Create a copy of the image to avoid modifying the original
    result_img = img.copy()
    draw = ImageDraw.Draw(result_img)
    img_width, img_height = img.size
    
    # Handle RTL languages (Arabic, Kurdish, etc.)
    is_rtl = False
    if language and language.lower() in ['ar', 'arabic', 'ckb', 'kurdish', 'he', 'hebrew', 'ur', 'urdu']:
        is_rtl = True
        logger.info(f"Processing RTL text for language: {language}")
    
    # Load the font
    font = get_font(font_family, font_size)
    if font is None:
        logger.warning(f"Failed to load font: {font_family}. Using default font.")
    
    # Process padding parameter
    padding_dict = _process_padding(padding)
    
    # Calculate text container width based on percentage
    container_width = int((img_width - (2 * container_margin)) * (container_width_percent / 100))
    
    # Calculate text position
    if text_position:
        # Use manual positioning if provided
        container_x = text_position.get('x', 0)
        container_y = text_position.get('y', 0)
    else:
        # Use alignment-based positioning
        if alignment.startswith('top'):
            container_y = container_margin
        elif alignment.startswith('bottom'):
            # Enforce minimum bottom margin of 20px
            min_bottom_margin = 20
            container_y = img_height - container_margin - min_bottom_margin
        else:  # center
            container_y = (img_height // 2)
        
        if alignment.endswith('left'):
            container_x = container_margin
        elif alignment.endswith('right'):
            container_x = img_width - container_width - container_margin
        else:  # center
            container_x = (img_width - container_width) // 2
    
    # Split text into lines that fit within the container width
    lines = []
    current_line = ""
    words = text.split()
    
    for word in words:
        # RTL languages need special handling
        if is_rtl:
            # Skip reshaping for RTL languages as it can cause issues with mixed scripts
            test_line = current_line + " " + word if current_line else word
        else:
            test_line = current_line + " " + word if current_line else word
        
        # Check if the line fits
        text_width = font.getbbox(test_line)[2] - font.getbbox(test_line)[0]
        max_width = container_width - padding_dict['left'] - padding_dict['right']
        
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # If a single word is too long, we need to split it
                if len(word) > 1:
                    logger.warning(f"Word too long for container: {word}")
                    chars = list(word)
                    current_part = ""
                    
                    for char in chars:
                        test_part = current_part + char
                        text_width = font.getbbox(test_part)[2] - font.getbbox(test_part)[0]
                        
                        if text_width <= max_width:
                            current_part = test_part
                        else:
                            lines.append(current_part)
                            current_part = char
                    
                    if current_part:
                        current_line = current_part
                else:
                    # If it's a single character that's too wide, we need to reduce font size
                    original_font_size = font_size
                    adjusted_font_size = int(font_size * 0.8)  # Reduce by 20%
                    logger.warning(f"Text too wide, reducing font size from {original_font_size} to {adjusted_font_size}")
                    font = get_font(font_family, adjusted_font_size)
                    lines.append(word)
    
    # Add the last line if there is one
    if current_line:
        lines.append(current_line)
    
    # Calculate text height
    line_spacing = 1.2
    total_text_height = 0
    for line in lines:
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        total_text_height += line_height * line_spacing
    
    # Adjust total_text_height to account for last line's spacing
    if lines:
        total_text_height -= (font.getbbox(lines[-1])[3] - font.getbbox(lines[-1])[1]) * (line_spacing - 1)
    
    # Calculate container height
    container_height = total_text_height + padding_dict['top'] + padding_dict['bottom']
    
    # Adjust container position for alignment
    if alignment.startswith('bottom'):
        container_y = container_y - container_height
    elif alignment.startswith('center'):
        container_y = container_y - (container_height // 2)
    
    # Ensure the container doesn't go off the edges
    if container_x < 0:
        container_x = 0
    if container_y < 0:
        container_y = 0
    if container_x + container_width > img_width:
        container_width = img_width - container_x
    if container_y + container_height > img_height:
        container_height = img_height - container_y
    
    logger.debug(f"Container position: x={container_x}, y={container_y}, width={container_width}, height={container_height}")
    
    # Draw the text background
    container_box = (container_x, container_y, container_x + container_width, container_y + container_height)
    
    # For full-width containers, only apply corner radius if explicitly requested
    apply_curve = bg_curve
    if container_width_percent == 100 and bg_curve > 0 and not text_position:
        # Skip corner radius for full-width containers unless explicitly positioned
        logger.debug("Full-width container detected, skipping corner radius")
        apply_curve = 0
    
    # Create background with gradient if colors are provided
    if gradient_colors:
        # Create gradient background
        gradient_bg = create_gradient_background(
            container_width, 
            container_height, 
            gradient_colors, 
            gradient_direction
        )
        
        # Create mask for rounded corners if needed
        if apply_curve > 0:
            mask = Image.new('L', (container_width, container_height), 0)
            mask_draw = ImageDraw.Draw(mask)
            draw_rounded_rectangle(
                mask_draw,
                (0, 0, container_width, container_height),
                apply_curve,
                fill=255
            )
            
            # Apply mask to gradient
            gradient_bg.putalpha(mask)
        
        # Paste gradient onto image
        result_img.paste(gradient_bg, (container_x, container_y), gradient_bg)
    else:
        # Draw standard background
        if apply_curve > 0:
            draw_rounded_rectangle(draw, container_box, apply_curve, fill=bg_color)
        else:
            draw.rectangle(container_box, fill=bg_color)
    
    # Draw text
    current_y = container_y + padding_dict['top']
    for line in lines:
        # Process line for RTL if needed
        display_line = line
        if is_rtl:
            # Skip reshaping for better compatibility with mixed scripts
            display_line = get_display(line)
        
        # Calculate line width for alignment
        bbox = font.getbbox(display_line)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        # Calculate x position based on alignment
        if alignment.endswith('left') or is_rtl and alignment.endswith('right'):
            text_x = container_x + padding_dict['left']
        elif alignment.endswith('right') or is_rtl and alignment.endswith('left'):
            text_x = container_x + container_width - line_width - padding_dict['right']
        else:  # center
            text_x = container_x + (container_width - line_width) // 2
        
        # Draw the line
        draw.text((text_x, current_y), display_line, font=font, fill=text_color)
        
        # Move to next line
        current_y += line_height * line_spacing
    
    return result_img 
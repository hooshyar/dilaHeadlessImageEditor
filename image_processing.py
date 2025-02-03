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

def apply_custom_text(base_img, text, language, font_family, font_size, text_color, background_color, text_position, alignment, padding, bg_curve, container_margin, container_width_percent):
    from PIL import ImageFont
    draw = ImageDraw.Draw(base_img)
    append_log(f"apply_custom_text: container_margin={container_margin}, container_width_percent={container_width_percent}")
    # Handle padding
    if isinstance(padding, dict):
        pad_top = int(padding.get('top', 0))
        pad_bottom = int(padding.get('bottom', 0))
        pad_left = int(padding.get('left', 0))
        pad_right = int(padding.get('right', 0))
    else:
        pad_top = pad_bottom = pad_left = pad_right = int(padding)

    # Load custom font
    font_path = f'fonts/{font_family}.ttf'
    try:
        font = ImageFont.truetype(font_path, size=font_size)
        append_log(f"Successfully loaded custom font from: {font_path}")
    except Exception as e:
        append_log(f"Error loading custom font {font_family}: {str(e)}")
        font = ImageFont.load_default()

    # Parse alignment
    parts = alignment.split('-')
    if len(parts) == 2:
        vert_align = parts[0].strip().lower()
        horiz_align = parts[1].strip().lower()
    else:
        vert_align = "center"
        horiz_align = "center"

    if container_width_percent is not None:
        # Ensure container parameters are proper types
        container_margin = int(container_margin)
        container_width_percent = float(container_width_percent)
        append_log(f"apply_custom_text: Converted container_margin={container_margin}, container_width_percent={container_width_percent}")

        # Calculate container width based on percentage within the safe area (accounting for margins)
        target_container_width = (base_img.width - 2 * container_margin) * (container_width_percent / 100.0)
        available_text_width = target_container_width - pad_left - pad_right

        # Wrap text to fit within available_text_width
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = word if current_line == "" else current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= available_text_width:
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

        # Recalculate text dimensions
        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        container_width = target_container_width
        container_height = text_height + pad_top + pad_bottom

        # Position container based on alignment and container_margin (ignoring text_position anchor)
        if horiz_align == "left":
            container_x = container_margin
        elif horiz_align == "right":
            container_x = base_img.width - container_width - container_margin
        else:
            container_x = (base_img.width - container_width) / 2

        if vert_align == "top":
            container_y = container_margin
        elif vert_align == "bottom":
            container_y = base_img.height - container_height - container_margin
        else:
            container_y = (base_img.height - container_height) / 2

        container_x = max(container_margin, min(int(container_x), base_img.width - int(container_width) - container_margin))
        container_y = max(container_margin, min(int(container_y), base_img.height - int(container_height) - container_margin))
        append_log(f"apply_custom_text: container position computed as (x={container_x}, y={container_y}), container size: ({container_width}x{container_height})")

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
    else:
        # Fallback: use provided text_position as anchor
        tp_x = int(text_position.get('x', 0))
        tp_y = int(text_position.get('y', 0))
        available_text_width = base_img.width - tp_x - pad_left - pad_right

        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = word if current_line == "" else current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= available_text_width:
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

        text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        container_width = text_width + pad_left + pad_right
        container_height = text_height + pad_top + pad_bottom
        container_x = tp_x - pad_left
        container_y = tp_y - pad_top
        container_x = max(container_margin, min(container_x, base_img.width - container_width - container_margin))
        container_y = max(container_margin, min(container_y, base_img.height - container_height - container_margin))
        container_x = int(container_x)
        container_y = int(container_y)

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

    # Create background with rounded corners
    bg_x = container_x
    bg_y = container_y
    bg_w = int(container_width)
    bg_h = int(container_height)

    bg_image = Image.new('RGBA', (bg_w, bg_h), background_color)
    mask = Image.new('L', (bg_w, bg_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (bg_w, bg_h)], radius=int(bg_curve), fill=255)
    base_img.paste(bg_image, (bg_x, bg_y), mask)
    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=text_color, align=horiz_align)
    append_log("Custom text applied with parameters.")
    return base_img 
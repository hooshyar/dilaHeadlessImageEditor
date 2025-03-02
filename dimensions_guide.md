# Portrait Dimensions Guide for Dila Headless Image Editor

## Overview

This guide addresses the issue of using portrait dimensions (like 1080x1920) in the Dila Headless Image Editor. 

## The Issue

When specifying dimensions like 1080x1920 (portrait orientation), the images sometimes appear to be incorrectly sized or cropped when viewed in certain applications.

## Diagnosis

Our testing has confirmed that:

1. The API is correctly processing images at the specified dimensions (1080x1920)
2. The image data itself has the correct pixel dimensions
3. The display issue may be related to:
   - Viewer applications auto-fitting images
   - Missing or incorrect DPI metadata
   - Display scaling in certain browsers or viewers

## Test Tools Created

We've created several testing tools to help diagnose and fix dimension issues:

### 1. `create_pattern.py`

Creates a test pattern image with gridlines and dimension indicators.

```bash
python create_pattern.py
```

This creates a 1080x1920 test pattern image with clear visual markers.

### 2. `process_local.py`

Processes local images directly with the image processing functions, bypassing the API.

```bash
python process_local.py portrait_pattern.png --output pattern_processed.png
```

### 3. `test_direct_url.py`

Tests the API with a specific image URL and dimensions.

```bash
python test_direct_url.py --url YOUR_IMAGE_URL --output result.png
```

### 4. `fix_dimensions.py`

Processes an image with proper dimensions and adds visual verification markers.

```bash
python fix_dimensions.py --url YOUR_IMAGE_URL --output fixed_result.png
```

### 5. `test_supermarket.py`

Specifically tests supermarket images with portrait dimensions.

```bash
python test_supermarket.py
```

## Best Practices for Portrait Dimensions

1. **Always verify dimensions of processed images**

   ```python
   from PIL import Image
   img = Image.open('output.png')
   print(f'Image dimensions: {img.width}x{img.height}')
   ```

2. **Set DPI metadata explicitly**

   ```python
   img.save('output.png', dpi=(300, 300))
   ```

3. **Add dimension indicators for debugging**

   Use the `add_verification_overlay` function from our test scripts to add visual dimension markers.

4. **Test in multiple viewers**

   Some image viewers may auto-fit or scale images differently. Test in multiple applications.

## API Usage for Portrait Dimensions

When using the API with portrait dimensions:

```python
payload = {
    "image_url": "YOUR_IMAGE_URL",
    "text": "Your text here",
    "width": 1080,      # Explicitly set width
    "height": 1920,     # Explicitly set height
    # Other parameters...
}

response = requests.post('http://localhost:5001/process_custom', json=payload)
```

## Common Issues and Solutions

### Issue: Image appears in landscape orientation despite setting portrait dimensions

**Solution 1:** Verify the image dimensions using code:

```python
from PIL import Image
img = Image.open('output.png')
print(f'Image dimensions: {img.width}x{img.height}')
```

**Solution 2:** Add dimension verification overlay:

```python
from PIL import Image, ImageDraw
img = Image.open('output.png')
draw = ImageDraw.Draw(img)
width, height = img.size
draw.rectangle([(0, 0), (width, 40)], fill=(0, 0, 0, 180))
draw.text((10, 10), f"Dimensions: {width}x{height}", fill=(255, 255, 255))
img.save('verified_output.png')
```

### Issue: DPI or metadata problems

**Solution:** Explicitly set DPI when saving:

```python
img.save('output.png', dpi=(300, 300))
```

## Conclusion

The Dila Headless Image Editor correctly processes images with portrait dimensions (1080x1920), but display issues may occur in certain viewers. Using the tools and techniques in this guide will help ensure your images appear correctly in all contexts. 
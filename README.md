# Dila Headless Image Editor

A Flask-based headless API service for adding Kurdish/Arabic text and logos to images. Perfect for automated image processing workflows that require RTL text support.

## Features

- Process images from URLs or local files
- Add Kurdish/Arabic text with proper RTL support
- Overlay logos with customizable positioning
- Automatic font selection with fallbacks
- Detailed logging system
- RESTful API endpoints
- Comprehensive error handling

## Requirements

- Python 3.x
- PIL (Pillow)
- Flask
- Arabic-Reshaper
- Python-Bidi
- Requests

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dilaHeadlessImageEditor.git
cd dilaHeadlessImageEditor
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
FLASK_DEBUG=1 FLASK_APP=app.py flask run --port 5001
```

2. API Endpoints:

### GET /
Health check endpoint
```bash
curl http://localhost:5001/
```

### POST /process
Process an image with text overlay
```bash
curl -X POST http://localhost:5001/process \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://example.com/image.jpg",
    "text": "بەخێربێن بۆ کوردستان"
  }'
```

### GET /images/<filename>
Serve static images from the images directory
```bash
curl http://localhost:5001/images/example.jpg
```

## Configuration

- Font size: Automatically scaled based on image height
- Logo size: 8% of image width
- Text position: Bottom center with 15% padding
- Logo position: Top-left corner with 3% margin

## Advanced Parameters

The `/process_custom` endpoint accepts the following advanced parameters:
- container_margin (integer): Additional margin (in pixels) from the edges of the image for the text container. Defaults to 0.
- container_width_percent (number): Specifies the text container's width as a percentage of the image's width. If provided, it determines the wrapping width for text.

## Directory Structure

```
dilaHeadlessImageEditor/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── images/            # Directory for local images
├── logo.png           # Default logo file
├── logger.txt         # Application logs
└── test_api.py        # API tests
```

## Testing

Run the test suite:
```bash
python test_api.py -v
```

Or test Kurdish text processing specifically:
```bash
python test_kurdish.py
```

## Error Handling

The API provides detailed error messages for:
- Missing parameters
- Invalid image URLs
- Image processing failures
- Font loading issues

## Logging

All operations are logged to `logger.txt` with timestamps and detailed information about:
- Request processing
- Image downloads
- Text rendering
- Logo placement
- Error conditions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For support, please open an issue in the GitHub repository. 
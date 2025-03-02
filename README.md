# Dila Headless Image Editor

A powerful headless API service for programmatic image manipulation with text overlays, supporting multiple languages including right-to-left scripts.

## Features

- **Text Overlay Processing**: Add customizable text to images
- **RTL Language Support**: Specialized handling for Arabic, Kurdish, and other RTL languages
- **Image Dimension Control**: Support for various image dimensions and orientations
- **API-First Design**: RESTful API endpoints for seamless integration

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

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

4. Run the application:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5001`.

## Docker Setup

### Using Docker Compose

The easiest way to run Dila Headless Image Editor is with Docker Compose:

1. Ensure Docker Desktop is running on your system.

2. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file to customize your settings (optional)

4. Start the application in production mode:
   ```bash
   docker-compose up -d
   ```

   The API will be available at `http://localhost:5000`.

5. For development mode with live reloading:
   ```bash
   docker-compose up -d dev
   ```

   The development server will be available at `http://localhost:5001`.

### Volume Mapping

The Docker setup includes volume mapping for:

- `./output:/app/output` - Processed images will be stored here
- `./images:/app/images` - Source images can be placed here
- `./fonts:/app/fonts` - Custom fonts can be added here

### Custom Configuration

You can customize the application by modifying the environment variables in the `.env` file or the `docker-compose.yml` file.

## API Usage

### Process Custom Image

```bash
curl -X POST http://localhost:5001/api/process_custom \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "text": "Your text here",
    "language": "en",
    "font_family": "Roboto",
    "font_size": 48,
    "text_color": "#FFFFFF",
    "background_color": "#000000",
    "alignment": "bottom-center",
    "padding": {"top": 20, "right": 20, "bottom": 20, "left": 20},
    "bg_opacity": 0.7,
    "bg_curve": 10,
    "container_margin": 20,
    "container_width_percent": 90,
    "width": 1080,
    "height": 1920
  }'
```

## Project Structure

```
dilaHeadlessImageEditor/
├── app/                  # Main application package
│   ├── api/              # API endpoints
│   ├── core/             # Core functionality
│   ├── utils/            # Utility functions
│   └── web/              # Web UI components
├── docs/                 # Documentation
├── fonts/                # Font files
├── output/               # Output images (not in repo)
├── tools/                # Tools and utilities
│   ├── diagnostics/      # Testing and diagnostic tools
│   ├── scripts/          # Command-line scripts
│   └── utils/            # Utility tools
├── run.py                # Application entry point
└── config.py             # Configuration settings
```

## Portrait Dimensions Guide

For working with portrait dimensions (like 1080x1920), refer to our [Portrait Dimensions Guide](dimensions_guide.md).

## Testing Tools

The project includes several testing and diagnostic tools in the `tools/` directory:

- `tools/scripts/process_local.py`: Process local images directly
- `tools/scripts/font_manager.py`: Manage fonts from the command line
- `tools/diagnostics/create_pattern.py`: Create test pattern images
- `tools/diagnostics/test_dimensions.py`: Test different image dimensions

## Documentation

- [Project Context](docs/context.md): Overview and architecture
- [Tasks](docs/tasks.md): Suggested improvements
- [File Structure](docs/files_structure.md): Codebase navigation
- [Changes Log](changes.log): History of changes

## Playground UI

The project includes an interactive playground UI for testing the API:

1. Start the server: `python run.py`
2. Open a browser and navigate to: `http://localhost:5001/playground`

## Command-line Scripts

### Process Local Images

Process images locally without using the API:

```bash
python tools/scripts/process_local.py --image input.jpg --text "Hello World" --output result.png
```

### Manage Fonts

List, download, and check fonts:

```bash
python tools/scripts/font_manager.py list
python tools/scripts/font_manager.py download "Open Sans" --weight 700
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing
- [Flask](https://flask.palletsprojects.com/) for the API server
- [Google Fonts](https://fonts.google.com/) for font integration 
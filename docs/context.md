# Dila Headless Image Editor - Project Context

## Project Overview
Dila Headless Image Editor is a Python-based application that provides image processing capabilities with a focus on text overlay. It's designed to be used as a headless service (via API) or through command-line tools, making it versatile for various integration scenarios.

## Core Functionality
- Adding text overlays to images with support for multiple languages (including RTL languages)
- Font management with Google Fonts integration
- Image cropping and resizing
- Background styling for text (solid colors, gradients, opacity)
- Text alignment and positioning options

## Project Structure
The project follows a modular structure:

- **app/**: Core application package
  - **core/**: Core image processing functionality
  - **api/**: REST API endpoints
  - **web/**: Web UI for interactive testing
  - **utils/**: Utility functions (cleanup, logging, etc.)

- **tools/**: Command-line tools and utilities
  - **scripts/**: Standalone scripts for processing images
  - **diagnostics/**: Tools for testing and debugging
  - **utils/**: Shared utilities for tools

- **docs/**: Project documentation
  - **context.md**: Project overview and context
  - **files_structure.md**: Detailed file structure
  - **changes.log**: Log of changes made to the project
  - **tasks.md**: Pending and completed tasks

- **fonts/**: Font files used by the application
- **output/**: Directory for processed images
  - **images/**: Final processed images
  - **temp/**: Temporary files

## Architecture
The application is built with Flask and follows a layered architecture:
1. **API Layer**: Handles HTTP requests and input validation
2. **Core Processing Layer**: Implements image processing logic
3. **Utility Layer**: Provides supporting functionality

## Recent Changes
The project has undergone significant restructuring to improve organization and maintainability:
1. Moved redundant files to appropriate directories
2. Created symbolic links for backward compatibility
3. Improved documentation
4. Enhanced error handling
5. Fixed import path issues for symbolic link execution

## Usage Patterns
The application can be used in several ways:
1. **API Mode**: Running as a web service to process images via HTTP requests
2. **CLI Mode**: Using command-line tools to process local images
3. **Interactive Mode**: Using the web UI for testing and experimentation

## Project Structure

The project follows a modular structure:

```
dila-headless-image-editor/
├── app/                    # Main application package
│   ├── api/                # API endpoints and handlers
│   ├── core/               # Core functionality modules
│   ├── utils/              # Utility functions
│   └── web/                # Web UI routes and templates
├── docs/                   # Documentation files
├── fonts/                  # Font files and mappings
├── tools/                  # Development and diagnostic tools
│   ├── diagnostics/        # Diagnostic utilities
│   ├── scripts/            # Utility scripts
│   └── utils/              # Helper utilities
├── static/                 # Static assets for web UI
└── templates/              # HTML templates
```

## Technical Stack

- **Backend**: Python with Flask
- **Image Processing**: Pillow (PIL Fork)
- **Text Processing**: arabic-reshaper, python-bidi
- **Font Management**: Custom font utilities with Google Fonts integration
- **Scheduling**: APScheduler for cleanup tasks
- **UI**: HTML, CSS, JavaScript for the playground

## Development Approach

The project follows these development principles:

1. **Modularity**: Code is organized into logical modules with clear responsibilities
2. **Documentation**: Comprehensive documentation for all components
3. **Testing**: Utilities for testing and verification
4. **Backward Compatibility**: Maintaining compatibility with existing integrations
5. **Extensibility**: Designed to be easily extended with new features

## Current Focus Areas

1. **Code Organization**: Improving structure and modularity
2. **Font Management**: Enhancing font handling capabilities
3. **Documentation**: Keeping documentation up-to-date with changes
4. **Testing Tools**: Developing utilities for testing and verification

## Integration Points

The service is designed to be integrated with:

1. **Web Applications**: Through RESTful API calls
2. **Mobile Apps**: As a backend service for image processing
3. **Content Management Systems**: For automated image processing
4. **Batch Processing Systems**: For bulk image processing

## Key Features

1. **Text Overlay Processing**: Add text to images with customizable properties:
   - Font family, size, and color
   - Text alignment and positioning
   - Background color and opacity
   - Padding and margins
   - Corner radius for text containers

2. **RTL Language Support**: Specialized handling for right-to-left languages:
   - Arabic text rendering
   - Kurdish (Sorani) text rendering
   - Mixed script handling (e.g., Latin characters within RTL text)

3. **Image Dimension Control**: Support for various image dimensions:
   - Custom width and height specification
   - Portrait and landscape orientations
   - Aspect ratio handling

4. **API-First Design**: RESTful API endpoints for image processing:
   - `/process_custom` endpoint for full customization
   - Parameter validation and error handling
   - JSON response format

## Technical Architecture

1. **Backend**: Python-based server using Flask
2. **Image Processing**: Pillow (PIL) library for image manipulation
3. **Text Rendering**: Custom text rendering with RTL support
4. **Deployment**: Containerized for easy deployment

## Recent Developments

1. **RTL Text Improvements**: Fixed issues with Kurdish text rendering and mixed script handling
2. **Padding Parameter Fix**: Enhanced padding parameter to support both integer and dictionary formats
3. **Text Container Enhancements**: Improved positioning, sizing, and overflow handling
4. **Portrait Dimension Handling**: Added tools and documentation for proper portrait dimension support
5. **Template Structure Fix**: Resolved template not found issues by creating proper template directory structure within the app package
6. **Web UI Improvements**: Enhanced the web interface with a proper index page and playground access
7. **Docker Containerization**: Implemented comprehensive Docker setup with production and development environments

## Recent Testing Results

1. **Web UI Testing**: Successfully verified that both the index page and playground are accessible
2. **API Health Check**: Confirmed that the API health endpoint returns proper status information
3. **Local Image Processing**: Verified that the process_local.py script works correctly with:
   - English text processing
   - Arabic text processing (RTL)
   - Kurdish text processing (RTL)

## Current Challenges

1. **Image Dimension Display**: Images with portrait dimensions (e.g., 1080x1920) sometimes display incorrectly in certain viewers
2. **DPI Metadata**: Missing or incorrect DPI metadata can affect image display
3. **Text Overflow**: Long text in RTL languages can sometimes overflow containers

## Project Goals

1. **Reliability**: Ensure consistent image processing results across all use cases
2. **Multilingual Support**: Excellent handling of various languages, especially RTL scripts
3. **Performance**: Fast image processing even with complex text overlays
4. **Flexibility**: Support for various image formats, dimensions, and text styling options

## Integration Use Cases

1. **Social Media Content Creation**: Generate images with text for social media platforms
2. **E-commerce Product Images**: Add text overlays to product images
3. **Educational Content**: Create images with explanatory text for educational purposes
4. **Marketing Materials**: Generate promotional images with custom text 
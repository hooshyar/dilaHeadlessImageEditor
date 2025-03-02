# Dila Headless Image Editor - File Structure

## Application Structure

```
dilaHeadlessImageEditor/
├── app/                  # Main application package
│   ├── api/              # API endpoints
│   │   ├── routes.py     # API route definitions
│   │   └── validation.py # Request validation
│   ├── core/             # Core functionality
│   │   ├── font_utils.py # Font utilities
│   │   └── image_processing.py # Image processing
│   ├── utils/            # Utility functions
│   │   └── cleanup.py    # Image cleanup
│   └── web/              # Web UI components
│       └── routes.py     # Web routes
├── docs/                 # Documentation
├── fonts/                # Font files
│   └── google_fonts/     # Downloaded Google Fonts
├── tools/                # Tools and utilities
│   ├── diagnostics/      # Testing and diagnostic tools
│   ├── scripts/          # Command-line scripts
│   └── utils/            # Utility tools
├── run.py                # Application entry point
└── config.py             # Configuration settings
```

## Core Application Files

- **run.py**: Entry point for the application, creates and runs the Flask app
- **config.py**: Configuration settings for the application
- **app/\_\_init\_\_.py**: Flask application factory

## App Core Module

- **app/core/image_processing.py**: Core image manipulation functionality
  - Contains functions for text overlay processing
  - Handles image resizing and cropping
  - Manages text positioning and container styling

- **app/core/font_utils.py**: Font utilities module
  - Handles font mapping and management
  - Provides Google Fonts download and caching
  - Implements font path resolution for both local and Google Fonts
  - Creates font objects with proper error handling and fallbacks

## API Module

- **app/api/routes.py**: API endpoint definitions
  - `/api/health`: Health check endpoint
  - `/api/fonts`: Font listing endpoint
  - `/api/process_custom`: Main image processing endpoint

- **app/api/validation.py**: Request validation utilities
  - Validates API requests
  - Processes request parameters

## Web Module

- **app/web/routes.py**: Web routes for the UI
  - `/`: Main index route
  - `/playground`: Interactive playground UI

## Utility Module

- **app/utils/cleanup.py**: Image cleanup utilities
  - Removes old processed images
  - Manages disk space

## Tools

### Diagnostic Tools (tools/diagnostics/)

- **create_pattern.py**: Creates a test pattern image with gridlines and dimension indicators
- **fix_dimensions.py**: Processes an image with proper dimensions and adds visual verification markers
- **test_dimensions.py**: Tests different image dimensions
- **test_supermarket.py**: Tests supermarket images with portrait dimensions

### Script Tools (tools/scripts/)

- **process_local.py**: Processes local images directly with the image processing functions
- **font_manager.py**: Command-line tool for managing fonts

## Documentation Files

- **docs/context.md**: Project overview and context
  - Describes the project's purpose and architecture
  - Documents key features and recent developments
  - Lists current challenges and project goals

- **docs/tasks.md**: Suggested improvements and tasks
  - Organizes tasks by priority
  - Tracks status of improvements
  - Documents feature requests

- **docs/files_structure.md**: This file - documents the project's file structure
  - Lists all important files and their purposes
  - Provides a quick reference for navigating the codebase

- **dimensions_guide.md**: Guide for working with portrait dimensions
  - Documents best practices for dimension handling
  - Provides solutions for common issues
  - Includes code examples for verification

- **changes.log**: Log of changes made to the project
  - Tracks enhancements, bug fixes, and features
  - Includes timestamps and affected files
  - Provides detailed descriptions of changes 
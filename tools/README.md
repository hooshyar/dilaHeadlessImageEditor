# Dila Headless Image Editor Tools

This directory contains various tools and utilities for the Dila Headless Image Editor project.

## Directory Structure

- **diagnostics/**: Tools for testing and diagnosing image processing issues
  - Test scripts for various image dimensions and aspects
  - Verification tools for image processing results
  - Scripts for testing specific features (Google Fonts, RTL text, gradients, etc.)

- **utils/**: Utility functions that don't fit into the core application
  - Helper scripts for development
  - Maintenance utilities
  - Specialized tools

- **scripts/**: Standalone scripts for various tasks
  - One-off scripts for specific operations
  - Scripts for data migration or conversion
  - Example usage scripts

## Usage

Most tools can be run directly from the command line:

```bash
python tools/diagnostics/test_dimensions.py
```

Some tools may require the main application to be installed or may need specific environment variables set. See individual tool documentation for details. 
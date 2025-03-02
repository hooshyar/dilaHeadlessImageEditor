#!/usr/bin/env python3
"""
Configuration settings for Dila Headless Image Editor
"""

import os

# Flask settings
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5001))
HOST = os.environ.get('HOST', '0.0.0.0')

# Directory settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')
OUTPUT_TEMP_DIR = os.path.join(OUTPUT_DIR, 'temp')

# Font directories
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
GOOGLE_FONTS_DIR = os.path.join(FONTS_DIR, 'google_fonts')
LOCAL_FONTS_DIR = os.path.join(FONTS_DIR, 'local_fonts')

# Image settings
DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 630
DEFAULT_DPI = 300
IMAGE_FORMAT = 'PNG'

# Storage settings
IMAGE_MAX_AGE = 20  # Maximum age of images in minutes before cleanup

# API settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

# Font settings
DEFAULT_FONT_FAMILY = 'Roboto'
DEFAULT_FONT_SIZE = 36
RTL_FONT_FAMILY = 'Noto Sans Arabic' 
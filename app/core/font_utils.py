#!/usr/bin/env python3
"""
Font utilities for Dila Headless Image Editor
"""

import os
import requests
import json
import logging
from pathlib import Path
from PIL import ImageFont

logger = logging.getLogger(__name__)

# Local paths
FONTS_DIR = Path('./fonts')
GOOGLE_FONTS_CACHE_DIR = FONTS_DIR / 'google_fonts'
GOOGLE_FONTS_MAPPING_FILE = FONTS_DIR / 'google_fonts_mapping.json'

# Ensure directories exist
FONTS_DIR.mkdir(exist_ok=True)
GOOGLE_FONTS_CACHE_DIR.mkdir(exist_ok=True)

def update_font_mapping():
    """
    Update the mapping of Google Font names to actual font files.
    
    Returns:
        dict: Mapping of font names to file paths
    """
    try:
        # Create a mapping from Google Font names to local file paths
        mapping = {}
        
        # Scan the google_fonts directory for downloaded fonts
        for font_file in GOOGLE_FONTS_CACHE_DIR.glob('*.ttf'):
            font_name = font_file.stem
            mapping[font_name] = str(font_file.relative_to(FONTS_DIR))
        
        # Add regular local fonts to the mapping too
        for font_file in FONTS_DIR.glob('*.ttf'):
            # Skip fonts in the google_fonts subdirectory as they're already handled
            if 'google_fonts' in str(font_file):
                continue
            font_name = font_file.stem
            mapping[font_name] = str(font_file.relative_to(FONTS_DIR))
        
        # Save the mapping to a JSON file
        with open(GOOGLE_FONTS_MAPPING_FILE, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        logger.info(f"Updated font mapping with {len(mapping)} fonts")
        return mapping
    except Exception as e:
        logger.error(f"Error updating font mapping: {str(e)}")
        return {}

def get_font_mapping():
    """
    Get the mapping of font names to file paths.
    
    Returns:
        dict: Mapping of font names to file paths
    """
    if not GOOGLE_FONTS_MAPPING_FILE.exists():
        return update_font_mapping()
    
    try:
        with open(GOOGLE_FONTS_MAPPING_FILE, 'r') as f:
            mapping = json.load(f)
        return mapping
    except Exception as e:
        logger.error(f"Error loading font mapping: {str(e)}")
        return update_font_mapping()

def download_google_font(font_family, font_weight=400, font_style='normal'):
    """
    Download a Google Font and return the path to the local file.
    
    Args:
        font_family (str): The name of the font family (e.g., 'Roboto', 'Open Sans')
        font_weight (int): The weight of the font (e.g., 400, 700)
        font_style (str): The style of the font ('normal', 'italic')
        
    Returns:
        Path: Path to the local font file or None if download failed
    """
    try:
        # Create a sanitized filename
        safe_name = font_family.replace(' ', '').lower()
        
        # Create a unique identifier for this specific font variant
        font_id = f"{safe_name}_{font_weight}_{font_style}"
        filename = f"{font_id}.ttf"
        font_path = GOOGLE_FONTS_CACHE_DIR / filename
        
        # Check if we already have this font
        if font_path.exists():
            logger.info(f"Using cached Google Font: {font_family} ({font_weight}, {font_style})")
            return font_path
            
        # Format the Google Fonts API URL for direct font file download
        # This uses the CSS2 API which doesn't require an API key
        css_url = f"https://fonts.googleapis.com/css2?family={font_family.replace(' ', '+')}"
        if font_weight != 400 or font_style != 'normal':
            css_url += f":wght@{font_weight}"
        if font_style == 'italic':
            css_url += f";ital,wght@1,{font_weight}"
            
        # Add user agent to ensure we get the TTF format
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get the CSS which contains the font file URL
        response = requests.get(css_url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to fetch Google Font CSS: {response.status_code}")
            return None
            
        # Extract the font URL from the CSS
        css = response.text
        url_start = css.find("src: url(") + 9
        url_end = css.find(")", url_start)
        if url_start < 9 or url_end < 0:
            logger.error(f"Could not find font URL in CSS")
            return None
            
        font_url = css[url_start:url_end]
        
        # Download the actual font file
        font_response = requests.get(font_url, headers=headers)
        if font_response.status_code != 200:
            logger.error(f"Failed to download Google Font file: {font_response.status_code}")
            return None
            
        # Save the font file
        with open(font_path, 'wb') as f:
            f.write(font_response.content)
            
        logger.info(f"Successfully downloaded Google Font: {font_family}")
        
        # Update the font mapping
        update_font_mapping()
        
        return font_path
    except Exception as e:
        logger.error(f"Error downloading Google Font {font_family}: {str(e)}")
        return None

def get_font_path(font_family, weight=400, style='normal'):
    """
    Get the path to a font file.
    
    This handles both local fonts and Google Fonts.
    
    Args:
        font_family (str): The name of the font family
        weight (int): The weight of the font (for Google Fonts)
        style (str): The style of the font (for Google Fonts)
        
    Returns:
        str: Path to the font file or None if not found
    """
    # First check if this is a local font
    mapping = get_font_mapping()
    if font_family in mapping:
        font_path = FONTS_DIR / mapping[font_family]
        if os.path.exists(font_path):
            return str(font_path)
    
    # If not found or not a local font, try with .ttf extension
    local_path = FONTS_DIR / f"{font_family}.ttf"
    if local_path.exists():
        return str(local_path)
    
    # If not a local font, try to download from Google Fonts
    google_font_path = download_google_font(font_family, weight, style)
    if google_font_path:
        return str(google_font_path)
    
    # Fallback to default font if nothing else works
    logger.warning(f"Font '{font_family}' not found locally and could not be downloaded. Using fallback.")
    return None

def get_font(font_family, font_size, weight=400, style='normal'):
    """
    Get a font object for the specified family and size
    
    Args:
        font_family (str): Font family name
        font_size (int): Font size in pixels
        weight (int): Font weight (e.g., 400, 700)
        style (str): Font style ('normal', 'italic')
        
    Returns:
        PIL.ImageFont: Font object or None if font could not be loaded
    """
    try:
        font_path = get_font_path(font_family, weight, style)
        if font_path:
            return ImageFont.truetype(font_path, font_size)
        
        # Fallback to default font
        logger.warning(f"Using default font instead of {font_family}")
        return ImageFont.load_default()
    except Exception as e:
        logger.error(f"Error loading font {font_family}: {str(e)}")
        return ImageFont.load_default()

def get_available_fonts():
    """
    Get a list of available fonts (local and Google Fonts)
    
    Returns:
        list: Available font families
    """
    mapping = get_font_mapping()
    return list(mapping.keys())

# Initialize the font mapping when the module is loaded
if not GOOGLE_FONTS_MAPPING_FILE.exists():
    update_font_mapping() 
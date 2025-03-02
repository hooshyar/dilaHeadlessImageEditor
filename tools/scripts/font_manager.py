#!/usr/bin/env python3
"""
Font Manager Script

This script provides command-line utilities for managing fonts in the Dila Headless Image Editor.
It can list available fonts, download Google Fonts, and update font mappings.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path to allow imports from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.font_utils import (
    get_available_fonts, 
    download_google_font, 
    update_font_mapping,
    get_font_path
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('font_manager.log')
    ]
)

logger = logging.getLogger(__name__)

def list_fonts():
    """List all available fonts"""
    fonts = get_available_fonts()
    if not fonts:
        logger.warning("No fonts found in the system")
        return
    
    logger.info(f"Found {len(fonts)} fonts:")
    for i, font in enumerate(sorted(fonts), 1):
        print(f"{i}. {font}")

def download_font(font_family, weight=400, style='normal'):
    """
    Download a Google Font
    
    Args:
        font_family (str): Font family name
        weight (int): Font weight (400, 700, etc.)
        style (str): Font style ('normal', 'italic')
    """
    logger.info(f"Downloading font: {font_family} (weight: {weight}, style: {style})")
    
    font_path = download_google_font(font_family, weight, style)
    
    if font_path:
        logger.info(f"Font downloaded successfully: {font_path}")
    else:
        logger.error(f"Failed to download font: {font_family}")

def update_mappings():
    """Update the font mappings file"""
    logger.info("Updating font mappings...")
    
    mapping = update_font_mapping()
    
    if mapping:
        logger.info(f"Font mappings updated successfully with {len(mapping)} fonts")
    else:
        logger.error("Failed to update font mappings")

def check_font(font_family):
    """
    Check if a font is available and show its path
    
    Args:
        font_family (str): Font family name
    """
    logger.info(f"Checking font: {font_family}")
    
    font_path = get_font_path(font_family)
    
    if font_path:
        logger.info(f"Font found: {font_path}")
        print(f"Font: {font_family}")
        print(f"Path: {font_path}")
    else:
        logger.warning(f"Font not found: {font_family}")
        print(f"Font '{font_family}' is not available in the system.")

def main():
    """Process command line arguments"""
    parser = argparse.ArgumentParser(description='Font management utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List fonts command
    list_parser = subparsers.add_parser('list', help='List available fonts')
    
    # Download font command
    download_parser = subparsers.add_parser('download', help='Download a Google Font')
    download_parser.add_argument('font_family', help='Font family name')
    download_parser.add_argument('--weight', type=int, default=400, help='Font weight')
    download_parser.add_argument('--style', choices=['normal', 'italic'], default='normal', help='Font style')
    
    # Update mappings command
    update_parser = subparsers.add_parser('update', help='Update font mappings')
    
    # Check font command
    check_parser = subparsers.add_parser('check', help='Check if a font is available')
    check_parser.add_argument('font_family', help='Font family name')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_fonts()
    elif args.command == 'download':
        download_font(args.font_family, args.weight, args.style)
    elif args.command == 'update':
        update_mappings()
    elif args.command == 'check':
        check_font(args.font_family)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 
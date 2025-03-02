#!/usr/bin/env python3
"""
Image Cleanup Utility

Removes processed images older than a specified time to prevent storage buildup.
"""

import os
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def cleanup_old_images(directory, max_age_minutes):
    """
    Remove images from the specified directory that are older than max_age_minutes.
    
    Args:
        directory (str): Directory containing images to clean
        max_age_minutes (int): Maximum age in minutes before deletion
    
    Returns:
        int: Number of files removed
    """
    if not os.path.exists(directory):
        logger.warning(f"Directory does not exist: {directory}")
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_minutes * 60
    removed_count = 0
    
    logger.info(f"Starting image cleanup in {directory} for files older than {max_age_minutes} minutes")
    
    # Process the main directory and its subdirectories
    directories_to_clean = [directory]
    
    # Check for images and temp subdirectories
    images_dir = os.path.join(directory, 'images')
    temp_dir = os.path.join(directory, 'temp')
    
    if os.path.exists(images_dir):
        directories_to_clean.append(images_dir)
    
    if os.path.exists(temp_dir):
        directories_to_clean.append(temp_dir)
    
    # Clean each directory
    for dir_path in directories_to_clean:
        removed_count += _cleanup_directory(dir_path, max_age_seconds)
    
    if removed_count > 0:
        logger.info(f"Cleanup complete: Removed {removed_count} images")
    else:
        logger.info("Cleanup complete: No images needed removal")
    
    return removed_count

def _cleanup_directory(directory, max_age_seconds):
    """Clean a single directory of old image files"""
    removed_count = 0
    current_time = time.time()
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # Skip directories and non-image files
        if os.path.isdir(filepath) or not is_image_file(filename):
            continue
        
        # Check file age
        file_age_seconds = current_time - os.path.getmtime(filepath)
        if file_age_seconds > max_age_seconds:
            try:
                os.remove(filepath)
                removed_count += 1
                logger.info(f"Removed old image: {filepath} (age: {file_age_seconds/60:.2f} minutes)")
            except Exception as e:
                logger.error(f"Error removing {filepath}: {e}")
    
    return removed_count

def is_image_file(filename):
    """Check if the filename is likely an image based on extension"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return any(filename.lower().endswith(ext) for ext in image_extensions) 
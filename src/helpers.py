"""File containing helper functions for the image overlap project"""

import os
import sys
from PIL import Image
from typing import List, Tuple, Dict, Optional
import logging

# Get logger
logger = logging.getLogger('ImageOverlapAutomation')

def get_image_info(image_path: str) -> Dict:
    """
    Get information about an image file.
    Args:
        image_path (str): Path to the image
    Returns:
        Dict: Dictionary containing image information
    """
    try:
        with Image.open(image_path) as image:
            info = {
                'filename': os.path.basename(image_path),
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height
            }
            return info
    except Exception as e:
        logger.error(f"Error getting image info for {image_path}: {str(e)}")
        return {
            'filename': os.path.basename(image_path),
            'error': str(e)
        }

def list_directory_images(directory: str, extensions: List[str] = ['.jpg', '.jpeg', '.png']) -> List[str]:
    """
    List all image files in a directory with specified extensions.
    Args:
        directory (str): Directory to search
        extensions (List[str], optional): List of file extensions to include. Defaults to ['.jpg', '.jpeg', '.png'].
    Returns:
        List[str]: List of full paths to image files
    """
    if not os.path.exists(directory):
        logger.warning(f"Directory does not exist: {directory}")
        return []
    
    image_files = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and any(filename.lower().endswith(ext) for ext in extensions):
            image_files.append(filepath)
    
    logger.debug(f"Found {len(image_files)} images in {directory}")
    return image_files

def calculate_centered_position(base_size: Tuple[int, int], overlay_size: Tuple[int, int]) -> Tuple[int, int]:
    """
    Calculate the position to center an overlay on a base image.
    Args:
        base_size (Tuple[int, int]): Width and height of the base image
        overlay_size (Tuple[int, int]): Width and height of the overlay image
    Returns:
        Tuple[int, int]: (x, y) position for the overlay
    """
    base_width, base_height = base_size
    overlay_width, overlay_height = overlay_size
    
    x = (base_width - overlay_width) // 2
    y = (base_height - overlay_height) // 2
    
    return (x, y)

def resize_image_proportionally(image_path: str, max_dimension: int) -> Optional[Image.Image]:
    """
    Resize an image proportionally, maintaining aspect ratio.
    Args:
        image_path (str): Path to the image
        max_dimension (int): Maximum width or height
    Returns:
        Optional[Image.Image]: Resized PIL Image object or None if error
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            return resized_img
    except Exception as e:
        logger.error(f"Error resizing image {image_path}: {str(e)}")
        return None
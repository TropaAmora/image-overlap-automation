"""Main file for image overlay application"""

# Import dependencies
import logging
import click
import os

# Local stuff
from src.log_config import setup_logger
from src.models import ImageOverlapManager

# Setup logger
logger = setup_logger()

def validate_folder_structure():
    """Validate that required folders exist and create them if necessary"""
    required_folders = [
        "inputs/images_jpeg",
        "inputs/logo_jpeg",
        "inputs/images_png",
        "inputs/logo_png",
        "outputs"
    ]
    
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f"Created folder: {folder}")
    
    logger.info("Folder structure validated")

# Define the click group 
@click.group()
def cli():
    """Image overlay application CLI"""
    pass

@click.command(help="Overlap logos on a list of images")
@click.option("--image_type", type=click.Choice(['jpeg', 'png'], case_sensitive=False), 
              prompt="Image type (jpeg/png)", help="Define image type (jpeg/png)")
@click.option("--position_x", type=int, prompt="Position x", 
              help="X coordinate to place the overlay")
@click.option("--position_y", type=int, prompt="Position y", 
              help="Y coordinate to place the overlay")
@click.option("--center_relative", is_flag=True, 
              help="If set, position coordinates are relative to the center of the image")
def overlap_images(image_type, position_x, position_y, center_relative):
    """Command to overlay logos on images"""
    try:
        # Validate folder structure
        validate_folder_structure()
        
        position = (position_x, position_y)
        position_type = "center-relative" if center_relative else "corner-relative"
        logger.info(f"Starting image overlap with type={image_type}, position={position} ({position_type})")
        
        manager = ImageOverlapManager(image_type=image_type, position=position, position_is_center=center_relative)
        count = manager.run()
        
        logger.info(f"Successfully processed {count} images")
        print(f"Successfully processed {count} images. Results saved in 'outputs' folder.")
        
    except click.Abort:
        logger.warning("Operation aborted by user")
        raise
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        print(f"Error: {str(e)}")
        raise click.Abort()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"An unexpected error occurred: {str(e)}")
        raise click.Abort()
    
cli.add_command(overlap_images)

if __name__ == '__main__':
    print("Welcome to Image Overlap Project.")
    cli()
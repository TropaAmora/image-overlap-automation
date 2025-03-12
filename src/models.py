"""File containing the project classes"""
import os
import glob
from typing import List
from PIL import Image

class ImageOverlapManager:
    """Class that manages the automation"""

    def __init__(self, image_type: str, position: tuple):
        # Ensure only available image types
        image_type = image_type.lower()
        if image_type not in ['jpeg', 'png']:
            raise ValueError("The only available image file types are 'jpeg' and 'png'")
        
        if image_type == 'jpeg':
            image_paths = glob.glob(os.path.join("inputs", "images_jpeg", "*.jpeg"))
            logo_paths = glob.glob(os.path.join("inputs", "logo_jpeg", "*.jpeg"))
        else:
            image_paths = glob.glob(os.path.join("inputs", "images_png", "*.png"))
            logo_paths = glob.glob(os.path.join("inputs", "logo_png", "*.png"))

        if len(image_paths) < 1 or len(logo_paths) < 1:
            raise ValueError("No images/logos present on input folder")

        self.logo_paths = logo_paths
        self.image_paths = image_paths
        self.image_type = image_type
        self.position = position

        
    def add_overlay(self, position, output_path):
        """
        Add an overlay image to a base image at the specified position.
        
        Args:
            base_image_path (str): Path to the base image
            overlay_image_path (str): Path to the overlay image
            position (tuple): (x, y) coordinates for the top-left corner of the overlay
            output_path (str, optional): Path to save the output image. If None, overwrites the base image.
        
        Returns:
            str: Path to the output image
        """
        # Open the base image
        base_image = Image.open(self.image_paths).convert("RGBA")
        
        # Open the overlay image
        overlay_image = Image.open(self.logo_paths).convert("RGBA")
        
        # Create a new blank image with the same size as the base image
        new_image = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
        
        # Paste the base image onto the new image
        new_image.paste(base_image, (0, 0))
        
        # Paste the overlay image onto the new image at the specified position
        new_image.paste(overlay_image, position, overlay_image)
        
        # Convert back to RGB mode (if saving as JPEG)
        new_image = new_image.convert("RGB")
        
        # Save the result
        if output_path is None:
            output_path = self.image_paths
        
        new_image.save(output_path)
        return output_path

    def process_directory(self, output_directory="outputs"):
        """
        Process all JPEG images in a directory.
        
        Args:
            directory_path (str): Path to directory containing images to process
            overlay_image_path (str): Path to the overlay image
            position (tuple): (x, y) coordinates for the overlay
            output_directory (str, optional): Directory to save output images. If None, overwrites original images.
        
        Returns:
            int: Number of images processed
        """
        count = 0
        
        # Create output directory if it doesn't exist
        if output_directory and not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Process each JPEG file in the directory
        for filename in os.listdir(self.image_paths):
            if filename.lower().endswith(('.jpg', '.jpeg')):
                base_image_path = os.path.join(self.image_paths, filename)
                
                if output_directory:
                    output_path = os.path.join(output_directory, filename)
                else:
                    output_path = None
                
                self.add_overlay(base_image_path, self.logo_paths, self.position, output_path)
                count += 1
                print(f"Processed: {filename}")
        
        return count

    def run(self):
        self.process_directory()
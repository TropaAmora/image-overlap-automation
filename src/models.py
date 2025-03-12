"""File containing the project classes"""
import os
import glob
import logging
from typing import List, Tuple, Optional
from PIL import Image

# Get logger
logger = logging.getLogger('ImageOverlapAutomation')

class ImageOverlapManager:
    """Class that manages the image overlay automation"""

    def __init__(self, image_type: str, position: Tuple[int, int], position_is_center: bool = False):
        """
        Initialize the ImageOverlapManager.
        
        Args:
            image_type (str): Type of images to process ('jpeg' or 'png')
            position (Tuple[int, int]): Position (x, y) to place the overlay
            position_is_center (bool): If True, position is relative to the center of the image
                                      If False, position is relative to the top-left corner
        
        Raises:
            ValueError: If image_type is not supported or if no images/logos are found
        """
        # Ensure only available image types
        image_type = image_type.lower()
        if image_type not in ['jpeg', 'png']:
            raise ValueError("The only available image file types are 'jpeg' and 'png'")
        
        # Find image files based on type
        if image_type == 'jpeg':
            # Look for both .jpg and .jpeg extensions
            image_paths = glob.glob(os.path.join("inputs", "images_jpeg", "*.jpg"))
            image_paths.extend(glob.glob(os.path.join("inputs", "images_jpeg", "*.jpeg")))
            
            logo_paths = glob.glob(os.path.join("inputs", "logo_jpeg", "*.jpg"))
            logo_paths.extend(glob.glob(os.path.join("inputs", "logo_jpeg", "*.jpeg")))
            
            if logo_paths:
                logo_path = logo_paths[0]  # Get the first logo
            else:
                logo_path = None
        else:  # png
            image_paths = glob.glob(os.path.join("inputs", "images_png", "*.png"))
            logo_paths = glob.glob(os.path.join("inputs", "logo_png", "*.png"))
            
            if logo_paths:
                logo_path = logo_paths[0]  # Get the first logo
            else:
                logo_path = None

        # Validate inputs
        if not image_paths:
            raise ValueError(f"No {image_type} images found in the inputs/images_{image_type} folder")
        
        if not logo_path:
            raise ValueError(f"No {image_type} logo found in the inputs/logo_{image_type} folder")
        
        logger.info(f"Found {len(image_paths)} {image_type} images and logo at {logo_path}")
        
        self.logo_path = logo_path
        self.image_paths = image_paths
        self.image_type = image_type
        self.position = position
        self.position_is_center = position_is_center

    def calculate_actual_position(self, base_image_size: Tuple[int, int], logo_size: Tuple[int, int]) -> Tuple[int, int]:
        """
        Calculate the actual pixel position based on whether position is center-relative or corner-relative.
        
        Args:
            base_image_size (Tuple[int, int]): Width and height of the base image
            logo_size (Tuple[int, int]): Width and height of the logo
        
        Returns:
            Tuple[int, int]: Actual pixel position (x, y) for the top-left corner of the logo
        """
        x, y = self.position
        base_width, base_height = base_image_size
        logo_width, logo_height = logo_size
        
        if self.position_is_center:
            # Convert center-relative position to top-left corner position
            # Center of the image
            center_x = base_width // 2
            center_y = base_height // 2
            
            # Calculate top-left corner position
            actual_x = center_x + x - (logo_width // 2)
            actual_y = center_y + y - (logo_height // 2)
        else:
            # Use position as is (top-left corner)
            actual_x = x
            actual_y = y
            
        return (actual_x, actual_y)
    
    def validate_position(self, base_image_size: Tuple[int, int], logo_size: Tuple[int, int]) -> bool:
        """
        Validate if the logo position is within the bounds of the base image.
        
        Args:
            base_image_size (Tuple[int, int]): Width and height of the base image
            logo_size (Tuple[int, int]): Width and height of the logo
        
        Returns:
            bool: True if position is valid, False otherwise
        """
        # Get the actual pixel position
        actual_x, actual_y = self.calculate_actual_position(base_image_size, logo_size)
        base_width, base_height = base_image_size
        logo_width, logo_height = logo_size
        
        # Check if the logo is completely outside the image
        if actual_x >= base_width or actual_y >= base_height or actual_x + logo_width <= 0 or actual_y + logo_height <= 0:
            return False
        
        return True

    def add_overlay(self, base_image_path: str, output_path: Optional[str] = None) -> str:
        """
        Add an overlay image to a base image at the specified position.
        
        Args:
            base_image_path (str): Path to the base image
            output_path (str, optional): Path to save the output image. If None, overwrites the base image.
        
        Returns:
            str: Path to the output image
        """
        # Open the base image
        base_image = Image.open(base_image_path).convert("RGBA")
        
        # Open the overlay image
        overlay_image = Image.open(self.logo_path).convert("RGBA")
        
        # Get actual pixel position based on whether it's center-relative or corner-relative
        actual_position = self.calculate_actual_position(base_image.size, overlay_image.size)
        
        # Validate position
        if not self.validate_position(base_image.size, overlay_image.size):
            logger.warning(f"Logo position {self.position} ({'center-relative' if self.position_is_center else 'corner-relative'}) " +
                          f"is out of bounds or partially out of bounds for image {base_image_path}. Adjusting...")
            
            # Adjust position to ensure logo is fully visible
            x, y = actual_position
            x = max(0, min(x, base_image.size[0] - overlay_image.size[0]))
            y = max(0, min(y, base_image.size[1] - overlay_image.size[1]))
            
            adjusted_position = (x, y)
            logger.info(f"Adjusted position to {adjusted_position}")
        else:
            adjusted_position = actual_position
        
        # Create a new blank image with the same size as the base image
        new_image = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
        
        # Paste the base image onto the new image
        new_image.paste(base_image, (0, 0))
        
        # Paste the overlay image onto the new image at the specified position
        new_image.paste(overlay_image, adjusted_position, overlay_image)
        
        # Convert back to RGB mode (if saving as JPEG)
        new_image = new_image.convert("RGB")
        
        # Save the result
        if output_path is None:
            output_path = base_image_path
        
        new_image.save(output_path)
        logger.debug(f"Saved overlaid image to {output_path}")
        return output_path

    def process_directory(self, output_directory: str = "outputs") -> int:
        """
        Process all images in the image_paths list.
        
        Args:
            output_directory (str, optional): Directory to save output images.
        
        Returns:
            int: Number of images processed
        """
        count = 0
        
        # Create output directory if it doesn't exist
        if output_directory and not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logger.info(f"Created output directory: {output_directory}")
        
        logger.info(f"Processing {len(self.image_paths)} images with logo overlay at position {self.position}")
        
        # Process each image file in the image_paths list
        for image_path in self.image_paths:
            filename = os.path.basename(image_path)
            
            if output_directory:
                output_path = os.path.join(output_directory, filename)
            else:
                output_path = None
            
            try:
                self.add_overlay(image_path, output_path)
                count += 1
                logger.info(f"Processed: {filename}")
                print(f"Processed: {filename}")
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")
                print(f"Error processing {filename}: {str(e)}")
        
        logger.info(f"Completed processing {count} images")
        return count

    def run(self) -> int:
        """
        Run the processing pipeline and return count of processed images
        
        Returns:
            int: Number of images processed
        """
        logger.info(f"Starting image overlay process with position {self.position} " +
                   f"({'center-relative' if self.position_is_center else 'corner-relative'})")
        count = self.process_directory()
        logger.info(f"Image overlay process completed. Processed {count} images.")
        return count
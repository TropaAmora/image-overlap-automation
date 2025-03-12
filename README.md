# Image Overlap Project

A Python application for overlaying logos on multiple images.

## Project Structure

```
image-overlap-project/
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── __init__.py      # Package initialization
│   ├── helpers.py       # Helper utility functions
│   ├── log_config.py    # Logging configuration
│   └── models.py        # Core functionality
├── inputs/
│   ├── images_jpeg/     # JPEG images to be processed
│   ├── logo_jpeg/       # JPEG logo for overlay
│   ├── images_png/      # PNG images to be processed
│   └── logo_png/        # PNG logo for overlay
├── outputs/             # Processed images are saved here
└── logs/                # Log files
```

## Requirements

- Python 3.7 or later
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-overlap-project.git
   cd image-overlap-project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create the required folder structure:
   ```
   mkdir -p inputs/images_jpeg inputs/logo_jpeg inputs/images_png inputs/logo_png outputs logs
   ```

## Usage

1. Place your source images in the appropriate folder:
   - JPEG images go in `inputs/images_jpeg/`
   - PNG images go in `inputs/images_png/`

2. Place your logo in the appropriate folder:
   - JPEG logo in `inputs/logo_jpeg/`
   - PNG logo in `inputs/logo_png/`

3. Run the application:
   ```
   python main.py overlap-images
   ```

4. Follow the prompts to specify:
   - Image type (jpeg or png)
   - Position X (horizontal position for the logo)
   - Position Y (vertical position for the logo)
   - Whether the position is relative to the center of the image (optional)

5. Processed images will be saved in the `outputs` folder

## Command Line Options

You can also specify options directly in the command:

```
python main.py overlap-images --image_type jpeg --position_x 100 --position_y 50
```

## Examples

### Corner-Relative Positioning (Default)

```
python main.py overlap-images --image_type jpeg --position_x 20 --position_y 20
```

This will overlay the JPEG logo on all JPEG images at position (20, 20) from the top-left corner.

### Center-Relative Positioning

```
python main.py overlap-images --image_type png --position_x 0 --position_y 0 --center_relative
```

This will overlay the PNG logo on all PNG images at the center of each image (position 0,0 relative to the center).

```
python main.py overlap-images --image_type jpeg --position_x -50 --position_y 30 --center_relative
```

This will overlay the JPEG logo 50 pixels to the left and 30 pixels below the center of each image.

## License

[Your License Here]
"""Main file"""

# Import dependencies
import logging
import click

# Local stuff
from src.log_config import setup_logger
from src.models import ImageOverlapManager

# Define the click group 
@click.group()
def cli():
    pass

@click.command(help="Overlap logos in list of images")
@click.option("--image_type", prompt="Image type", help="Define image type (jpeg/png)")
@click.option("--position_x", prompt="Position x", help="Position x to place the overlay")
@click.option("--position_y", prompt="Position y", help="Position x to place the overlay")
def overlap_images(image_type, position_x, position_y):
    try: 
        position = (float(position_x), float(position_y))
        manager = ImageOverlapManager(image_type=image_type, position=position)
        manager.run()
    except click.Abort:
        raise
    except Exception as e:
        print("Arguments provided not valid")
        raise click.Abort()
    
cli.add_command(overlap_images)

if __name__ == '__main__':
    print("Welcome to image overlap image project.")
    cli()


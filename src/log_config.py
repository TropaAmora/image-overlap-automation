# Import dependencies
import logging
import sys
from datetime import datetime
import os

def setup_logger(log_level=logging.INFO):
    """Configure and return a logger instance with both file and console handlers."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/bag_allocation_algo_{timestamp}.log'
    
    # Create logger
    logger = logging.getLogger('ImageOverlapAutomation')
    logger.setLevel(log_level)
    
    # Remove existing handlers if any
    if logger.handlers:
        logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info('Logger initialized')
    return logger
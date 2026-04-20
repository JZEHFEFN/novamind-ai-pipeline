# log.py
import logging
import sys

def setup_logger():
    """Setup logger for API client initialization messages"""
    
    # Create logger
    logger = logging.getLogger('api_client')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create file handler (writes to file)
    file_handler = logging.FileHandler('api_client.log')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    # Create console handler for errors only (optional)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)  # Only show warnings and errors
    console_handler.setFormatter(file_format)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger():
    """Get or create logger"""
    logger = logging.getLogger('api_client')
    if not logger.handlers:
        return setup_logger()
    return logger

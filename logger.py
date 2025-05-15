"""
Logging module for the LangChain and Streamlit application.

This module sets up logging configuration for the application with:
- INFO, WARNING, and ERROR levels
- File logging to logs/errors/error.log
- Console output for immediate feedback
- Automatic creation of log directories
"""

import os
import logging
from logging.handlers import RotatingFileHandler

# Constants
LOG_DIR = os.path.join("logs", "errors")
LOG_FILE = os.path.join(LOG_DIR, "error.log")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger instance
logger = logging.getLogger("estudamais")
logger.setLevel(logging.INFO)

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create file handler with rotation (10MB max size, keep 5 backup logs)
file_handler = RotatingFileHandler(
    LOG_FILE, 
    maxBytes=10_000_000, 
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Convenience functions
def info(message):
    """Log an info level message"""
    logger.info(message)

def warning(message):
    """Log a warning level message"""
    logger.warning(message)

def error(message, exc_info=False):
    """
    Log an error level message, optionally with exception info
    
    Args:
        message: The error message
        exc_info: If True, include exception traceback information
    """
    logger.error(message, exc_info=exc_info)

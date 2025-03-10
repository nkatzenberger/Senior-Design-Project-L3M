import os
import logging
from logging.handlers import RotatingFileHandler
from utils.path_utils import get_logs_path

# Ensure the logs directory exists
LOG_FILE = os.path.join(get_logs_path(), "L3M.log")

# Logging configuration
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
log_handler.setFormatter(log_formatter)

# Create logger
logger = logging.getLogger("L3MLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# Function to log messages
def log_message(level, message):
    """Helper function to log messages with different levels"""
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)

import logging
import os
from datetime import datetime

def setup_logger(name: str = "sayanox") -> logging.Logger:
    """Set up a unified logger for the framework"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", f"sayanox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # File handler (DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Console handler (INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
  

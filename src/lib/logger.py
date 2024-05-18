# -*- coding: utf-8 -*-
# lib/logger.py
import logging


def setup_logger(level="INFO", format="%(asctime)s - %(levelname)s - %(message)s"):
    """Set up logger configuration."""
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(level.upper()))

    # Create a file handler
    file_handler = logging.FileHandler("plugin_manager.log")
    file_handler.setLevel(logging.getLevelName(level.upper()))

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.getLevelName(level.upper()))

    # Create a formatter and set it for the handlers
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

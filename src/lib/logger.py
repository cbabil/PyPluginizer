# -*- coding: utf-8 -*-
# lib/logger.py
import logging


def setup_logger(
    level="INFO",
    file_level="INFO",
    console_level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s",
):
    """Set up logger configuration.

    Args:
        level (str): The general logging level
        file_level (str): The logging level for the file
        console_level (str): The logging level for the console
    """
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(level.upper()))
    # Create a file handler
    file_handler = logging.FileHandler("plugin_manager.log")
    file_handler.setLevel(logging.getLevelName(file_level.upper()))
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.getLevelName(console_level.upper()))
    # Create a formatter and set it for the handlers
    formatter = logging.Formatter(format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

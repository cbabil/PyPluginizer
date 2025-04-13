# -*- coding: utf-8 -*-
import logging
from logging import FileHandler, StreamHandler

from src.lib.logger import setup_logger


def test_setup_logger(mocker):
    """Test if the setup_logger function correctly configures the logger with both
    FileHandler and StreamHandler."""
    # Mock the getLogger method to prevent actual logger setup
    mock_logger = mocker.Mock(spec=logging.Logger)
    mocker.patch('logging.getLogger', return_value=mock_logger)

    # Call the setup_logger function
    logger = setup_logger()

    # Assertions to check if logger is setup correctly
    logging.getLogger.assert_called_once_with('src.lib.logger')
    assert len(logger.handlers) == 2
    assert any(isinstance(handler, FileHandler) for handler in logger.handlers)
    assert any(isinstance(handler, StreamHandler) for handler in logger.handlers)


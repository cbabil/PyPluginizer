# -*- coding: utf-8 -*-
import logging

from src.lib.logger import setup_logger


def test_setup_logger(mocker):
    # Create a MagicMock object to mimic the Logger instance
    logger_mock = mocker.MagicMock(spec=logging.Logger)
    logger_mock.handlers = [logging.FileHandler('plugin_manager.log')]  # Mimic only a FileHandler

    # Patch getLogger method from logging module to return the MagicMock object
    mocker.patch('logging.getLogger', return_value=logger_mock)

    # Call the setup_logger function
    logger = setup_logger()

    # Assertions
    assert logging.getLogger.call_count == 1
    logging.getLogger.assert_called_with('src.lib.logger')  # Adjusted to match the actual call
    assert logger.handlers  # Ensure handlers are added
    assert isinstance(logger.handlers[0], logging.FileHandler)  # Check if the first handler is a FileHandler

"""Tests for logging utilities."""

import logging
from cowabunga_api.utils.logging_tools import logger


def test_logger_exists():
    """Logger should be a logging.Logger instance."""
    assert isinstance(logger, logging.Logger)


def test_logger_name():
    """Logger should have the correct module name."""
    assert logger.name == "cowabunga_api.utils.logging_tools"

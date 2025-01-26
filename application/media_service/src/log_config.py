import logging
from typing import Any


def add_logger(name: Any) -> logging.Logger:
    """Custom logger"""
    logger = logging.getLogger(name)
    handler_logger = logging.FileHandler(filename="media.log")
    logger.addHandler(handler_logger)
    logger.setLevel("DEBUG")
    formatter_logger = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler_logger.setFormatter(formatter_logger)
    return logger

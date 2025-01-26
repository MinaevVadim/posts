import logging
from functools import wraps
from typing import Any, Callable


def add_logger(name: Any) -> logging.Logger:
    """Custom logger"""
    logger = logging.getLogger(name)
    handler_logger = logging.FileHandler(filename="app.log")
    logger.addHandler(handler_logger)
    logger.setLevel("DEBUG")
    formatter_logger = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler_logger.setFormatter(formatter_logger)
    return logger


def logged(my_logger: logging.Logger) -> Callable:
    """Logger for information and control about working classes"""

    def log_methods(func: Callable) -> Callable:
        """Logging methods before and after"""

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            my_logger.debug(
                "Function %s has started to work.",
                func.__name__,
            )
            obj = await func(self, *args, *kwargs)
            my_logger.debug(
                "Function result is object: %s was performed in %s of the function.",
                obj,
                func.__name__,
            )
            return obj

        return wrapper

    def decorator_logger(cls: Callable) -> Callable:
        """A decorator that allows you to log all methods inside a class"""

        @wraps(cls)
        def wrapper(*args, **kwargs):
            for method in dir(cls):
                if method.startswith("__") is False:
                    cur_method = getattr(cls, method)
                    decor_method = log_methods(cur_method)
                    setattr(cls, method, decor_method)
            return cls

        return wrapper

    return decorator_logger

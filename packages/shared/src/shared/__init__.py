from .constants import Constants
from .logger import logger, setup_logging


def hello() -> str:
    return "Hello from shared!"


__all__ = ["hello", "logger", "setup_logging", "Constants"]

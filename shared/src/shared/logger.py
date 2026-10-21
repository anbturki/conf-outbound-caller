import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Handler to intercept standard library logging and redirect to loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        logger.opt(exception=record.exc_info).log(level, record.getMessage())


class JsonFormatter:
    """
    Format logs as JSON for structured logging in production.
    """

    def __call__(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "name": record["name"],
            "function": record["function"],
            "line": record["line"],
            "thread": record["thread"].id,
        }

        # Add exception info if present
        if record["exception"]:
            log_record["exception"] = {
                "type": record["exception"].type.__name__,
                "value": str(record["exception"].value),
                "traceback": record["exception"].traceback,
            }

        # Add extra data if present
        if record["extra"]:
            log_record["extra"] = record["extra"]

        return json.dumps(log_record)


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "console",
    log_path: str = "logs/platform.log",
) -> None:
    """
    Set up logging configuration.
    """
    # Remove default logger
    logger.remove()

    # Set log level from settings
    # Console handler
    if log_format == "console":
        # Pretty console logging for development
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            level=log_level,
            colorize=True,
        )
    else:
        # Create log directory if it doesn't exist
        log_path_obj = Path(log_path)
        log_path_obj.mkdir(parents=True, exist_ok=True)

        # File handler - rotate at 10MB, keep 10 files
        logger.add(
            f"{log_path}/confera_{{time:YYYY-MM-DD}}.log",  # Use Loguru's {time} placeholder
            rotation="10 MB",
            retention=10,
            compression="gz",
            format=JsonFormatter()
            if log_format == "json"
            else "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            level=log_level,
        )
        # JSON logging for production
        logger.add(
            sys.stdout,
            format=JsonFormatter(),
            level=log_level,
            serialize=True,
        )

    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Update logger for uvicorn
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn") or logger_name.startswith("fastapi"):
            logging.getLogger(logger_name).handlers = [InterceptHandler()]

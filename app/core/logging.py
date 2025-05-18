import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

from app.core.config import config


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

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


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


def setup_logging() -> None:
    """
    Set up logging configuration.
    """
    # Remove default logger
    logger.remove()

    # Set log level from settings
    log_level = config.log.level
    # Console handler
    if config.log.format == "console":
        # Pretty console logging for development
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            level=log_level,
            colorize=True,
        )
    else:
        # Create log directory if it doesn't exist
        log_path = Path(config.log.path)
        log_path.mkdir(parents=True, exist_ok=True)

        # File handler - rotate at 10MB, keep 10 files
        logger.add(
            f"{config.log.path}/confera_{{time:YYYY-MM-DD}}.log",  # Use Loguru's {time} placeholder
            rotation="10 MB",
            retention=10,
            compression="gz",
            format=JsonFormatter()
            if config.log.format == "json"
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

    # Log startup info
    logger.info(
        f"Logging configured. Environment: {config.api.env}, Log level: {log_level}"
    )

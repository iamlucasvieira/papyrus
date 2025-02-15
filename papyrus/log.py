"""Logging setup."""

import logging

from rich.logging import RichHandler


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure logging with Rich handler and formatting."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    # Create a logger for the papyrus package
    logger = logging.getLogger("papyrus")
    logger.setLevel(level)

    return logger

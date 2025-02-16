"""Logging setup."""

import functools
import logging
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from rich.logging import RichHandler

T = TypeVar("T")
P = ParamSpec("P")


def log_time(logger: logging.Logger) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Log the time it takes for a function to execute.

    Args:
        logger: The logger instance to use for logging

    Returns:
        Callable: The decorator function

    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def get_function_repr(func: Callable[P, T]) -> str:
            return (
                f"[muted]{func.__module__}[/muted]:[b green]{func.__name__}[/b green]"
            )

        def get_execution_time_repr(start_time: float, end_time: float) -> str:
            return f"(took [yellow]{end_time - start_time:.4f}s[/yellow])"

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            function_repr = get_function_repr(func)
            start_msg = f"[bold blue]START[/bold blue] {function_repr}"
            logger.debug(start_msg, extra={"markup": True})
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                execution_time_repr = get_execution_time_repr(start_time, end_time)
                end_msg = (
                    f"[b green]END[/b green] {function_repr} {execution_time_repr}"
                )
                logger.debug(end_msg, extra={"markup": True})
                return result
            except Exception:
                end_time = time.perf_counter()
                execution_time_repr = get_execution_time_repr(start_time, end_time)
                error_msg = (
                    f"[b red]ERROR[/b red] {function_repr} {execution_time_repr}"
                )
                logger.debug(error_msg, extra={"markup": True})
                raise

        return wrapper

    return decorator


def setup_logging(level: str) -> None:
    """Configure logging with Rich handler and formatting."""
    level = logging.getLevelName(level)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

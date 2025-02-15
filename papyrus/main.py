"""Application entry point."""

import logging
import os
from pathlib import Path

import typer
from rich.console import Console

from papyrus.log import setup_logging
from papyrus.parsing import Parser

app = typer.Typer()
console = Console()


PAPYRUS_LOG_LEVEL = os.getenv("PAPYRUS_LOG_LEVEL", "DEBUG")


@app.command()
def main(
    routes_file: str = typer.Option(
        "routes.py", "--routes-file", "-r", help="The routes file to parse"
    ),
    views_dir: str = typer.Option(
        "views", "--views-dir", "-v", help="The views directory to parse"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Set log level to DEBUG, otherwise WARNING (log level can be "
        "set with PAPYRUS_LOG_LEVEL environment variable)",
    ),
) -> None:
    """Say hello to NAME."""
    setup_logging(level=PAPYRUS_LOG_LEVEL if verbose else "WARNING")
    logger = logging.getLogger("papyrus")

    if logger:
        logger.info("Starting Papyrus...")
    routes = Parser.get_routes(Path(), routes_file, views_dir)
    console.print(routes)


if __name__ == "__main__":
    app()

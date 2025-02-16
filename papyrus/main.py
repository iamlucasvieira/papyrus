"""Application entry point."""

import logging
import os
from pathlib import Path

import typer
from rich.console import Console

from papyrus.exceptions import RoutesFileNotFoundError, ViewsDirNotFoundError
from papyrus.log import setup_logging
from papyrus.parsing import Parser
from papyrus.pyramid import PyramidInfo

app = typer.Typer()
console = Console()

LOG_LEVEL = os.getenv("PAPYRUS_LOG_LEVEL", "DEBUG")
ROUTES_FILE_NAME = os.getenv("PAPYRUS_ROUTES_FILE_NAME", "routes.py")
VIEWS_DIR = os.getenv("PAPYRUS_VIEWS_DIR", "views")


@app.command()
def main(
    routes_file: str = typer.Option(
        ROUTES_FILE_NAME, "--routes-file", "-r", help="The routes file to parse"
    ),
    views_dir: str = typer.Option(
        VIEWS_DIR, "--views-dir", "-v", help="The views directory to parse"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Set log level to DEBUG, otherwise WARNING (log level can be "
        "set with PAPYRUS_LOG_LEVEL environment variable)",
    ),
    base_dir: Path | None = typer.Option(
        None, "--base-dir", "-b", help="The base directory to parse (defaults to cwd)"
    ),
) -> None:
    """Say hello to NAME."""
    setup_logging(level=LOG_LEVEL if verbose else "WARNING")
    logger = logging.getLogger("papyrus")
    pyramid_info = PyramidInfo(routes_file_name=routes_file, views_dir_name=views_dir)
    base_dir = base_dir or Path.cwd()

    if logger:
        logger.info("Starting Papyrus...")
    try:
        routes = Parser.get_routes(base_dir, pyramid_info)
    except RoutesFileNotFoundError as e:
        logger.error(e)
        return
    except ViewsDirNotFoundError as e:
        logger.error(e)
        return

    console.print(routes)


if __name__ == "__main__":
    app()

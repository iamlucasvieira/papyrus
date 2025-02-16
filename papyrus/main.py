"""Application entry point."""

import logging
from pathlib import Path
from typing import Annotated

import typer
import yaml
from openapi_spec_validator import validate
from openapi_spec_validator.exceptions import (
    OpenAPISpecValidatorError,
)
from openapi_spec_validator.validation.exceptions import UnresolvableParameterError
from rich.console import Console

from papyrus.exceptions import RoutesFileNotFoundError, ViewsDirNotFoundError
from papyrus.log import setup_logging
from papyrus.parsing import Parser
from papyrus.pyramid import PyramidInfo
from papyrus.writing import OpenAPI

app = typer.Typer()
console = Console()


@app.command()
def main(
    base_dir: Annotated[
        Path | None,
        typer.Argument(help="The base directory to parse (defaults to cwd)"),
    ] = None,
    routes_file: Annotated[
        str,
        typer.Option(
            "--routes-file",
            "-r",
            help="The routes file to parse",
            envvar="PAPYRUS_ROUTES_FILE_NAME",
        ),
    ] = "routes.py",
    views_dir: Annotated[
        str,
        typer.Option(
            "--views-dir",
            "-v",
            help="The views directory to parse",
            envvar="PAPYRUS_VIEWS_DIR",
        ),
    ] = "views",
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Set log level to DEBUG",
        ),
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            "-l",
            help="Set the log level",
            envvar="PAPYRUS_LOG_LEVEL",
        ),
    ] = "WARNING",
) -> None:
    """Parse Pyramid routes and views."""
    setup_logging(level="DEBUG" if verbose else log_level)
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

    filtered_routes = Parser.filter_routes_with_a_method(routes)
    openapi = OpenAPI.from_routes(filtered_routes)
    openapi_yaml = openapi.to_yaml()

    try:
        validate(yaml.safe_load(openapi_yaml))
    except OpenAPISpecValidatorError as e:
        logger.error(e)
    except UnresolvableParameterError as e:
        logger.info(e)

    console.print(openapi_yaml)


if __name__ == "__main__":
    app()

"""Module with pyramid related classes."""

import logging
from dataclasses import dataclass
from pathlib import Path

from papyrus.exceptions import (
    InvalidUrlPatternError,
    RoutesFileNotFoundError,
    ViewsDirNotFoundError,
)
from papyrus.finder import Finder
from papyrus.log import log_time

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Route:
    """Dataclass representing a route in a pyramid application."""

    name: str
    pattern: str
    methods: set[str]


def extract_url_parameters(pattern: str) -> list[str]:
    """Extract URL parameter names from a URL pattern.

    Args:
        pattern: A URL pattern string that may contain parameters in curly braces,
                e.g. "/user/{id}/profile/{section}"

    Returns:
        A list of parameter names found in the pattern, e.g. ["id", "section"]

    Raises:
        InvalidUrlPatternError: If the pattern contains invalid parameter syntax

    """
    parameters = []
    for part in pattern.split("{")[1:]:
        if "}" not in part:
            raise InvalidUrlPatternError(pattern, "Missing closing brace")
        param_name = part.split("}")[0]
        if not param_name:
            raise InvalidUrlPatternError(pattern, "Missing parameter name")
        parameters.append(param_name)
    return parameters


@dataclass(frozen=True)
class PyramidInfo:
    """Dataclass representing information about a pyramid application."""

    views_dir_name: str
    routes_file_name: str


class PyramidFiles:
    """Class with utilities for getting pyramid files."""

    @staticmethod
    @log_time(logger)
    def get_routes_path(base_dir: Path, file_name: str) -> Path:
        """Return the path to routes file, otherwise raise FileNotFounderror."""
        file_path = Finder.find_file(base_dir, file_name)
        if not file_path:
            raise RoutesFileNotFoundError(file_name, base_dir)
        return file_path

    @staticmethod
    @log_time(logger)
    def get_views_path(base_dir: Path, views_dir: str) -> Path:
        """Return the path to views directory, otherwise raise FileNotFounderror."""
        view_dir = Finder.find_dir(base_dir, views_dir)
        if not view_dir:
            raise ViewsDirNotFoundError(views_dir, base_dir)
        return view_dir

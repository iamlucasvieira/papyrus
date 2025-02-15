"""Module responsible for parsing information in a pyramid application."""

from dataclasses import dataclass
from pathlib import Path

from .finder import PyramidFiles


@dataclass(frozen=True)
class Route:
    """Dataclass representing a route in a pyramid application."""

    name: str
    pattern: str
    methods: list[str]


class Parser:
    """Class responsible for parsing information in a pyramid application."""

    def __init__(self: "Parser") -> None:
        """Initialize the parser with the request."""

    @staticmethod
    def get_routes_pattern(base_dir: Path, file_name: str | None) -> dict[str, str]:
        """Get all routes from a pyramid application.

        Returns dict with keys being route name and value the pattern
        """
        _ = PyramidFiles.get_routes(base_dir, file_name)

        return {}

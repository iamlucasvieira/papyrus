"""Module responsible for parsing information in a pyramid application."""

import ast
import logging
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

from papyrus.log import log_time

from .finder import PyramidFiles

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Route:
    """Dataclass representing a route in a pyramid application."""

    name: str
    pattern: str
    methods: list[str]


class Parser:
    """Class responsible for parsing information in a pyramid application."""

    @staticmethod
    @log_time(logger)
    def get_routes_pattern(base_dir: Path, file_name: str | None) -> dict[str, str]:
        """Get all routes from a pyramid application.

        Returns dict with keys being route name and value the pattern
        """
        routes_file = PyramidFiles.get_routes(base_dir, file_name)
        crawler = AstCrawler(routes_file)

        routes = {}
        for route_call in crawler.iter_add_route_calls():
            route_name, route_pattern = crawler.get_route_name_and_pattern(route_call)
            if route_name and route_pattern:
                routes[route_name] = route_pattern

        return routes


class AstCrawler:
    """Class responsible for crawling the AST of a pyramid application."""

    def __init__(self: "AstCrawler", file_path: Path) -> None:
        """Initialize the crawler with the request."""
        with file_path.open("r", encoding="utf-8") as file:
            self.tree = ast.parse(file.read())

    @log_time(logger)
    def iter_add_route_calls(self: "AstCrawler") -> Generator[ast.Call]:
        """Yield each call to .add_route() one at a time."""
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call)
                and hasattr(node.func, "attr")
                and node.func.attr == "add_route"
            ):
                yield node

    @staticmethod
    @log_time(logger)
    def get_route_name_and_pattern(node: ast.Call) -> tuple[str | None, str | None]:
        """Get the route name and pattern from an add_route call."""
        expected_length = 2
        if len(node.args) < expected_length:
            logger.warning("Skipping route call: %s", node)
            return None, None
        route_name, route_pattern = node.args[:expected_length]
        return getattr(route_name, "value", None), getattr(route_pattern, "value", None)

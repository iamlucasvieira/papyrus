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

        routes = {}
        for route_call in AstCrawler.iter_method_calls(routes_file, "add_route"):
            route_name, route_pattern = Parser.call_to_route_name_and_pattern(
                route_call
            )
            if route_name and route_pattern:
                routes[route_name] = route_pattern

        return routes

    @staticmethod
    @log_time(logger)
    def call_to_route_name_and_pattern(call: ast.Call) -> tuple[str | None, str | None]:
        """Get the route name and pattern from an add_route call."""
        expected_length = 2
        if len(call.args) < expected_length:
            logger.warning("Skipping route call: %s", call)
            return None, None
        route_name, route_pattern = call.args[:expected_length]
        return getattr(route_name, "value", None), getattr(route_pattern, "value", None)


class AstCrawler:
    """Class responsible for crawling the AST of a pyramid application."""

    @staticmethod
    @log_time(logger)
    def get_tree(file_path: Path) -> ast.AST:
        """Get the AST of a file."""
        with file_path.open("r", encoding="utf-8") as file:
            return ast.parse(file.read())

    @staticmethod
    @log_time(logger)
    def iter_method_calls(file_path: Path, method_name: str) -> Generator[ast.Call]:
        """Yield each call to a specific method one at a time.

        Args:
            file_path: The path to the file to search for method calls
            method_name: The name of the method to search for (e.g., 'add_route')

        """
        tree = AstCrawler.get_tree(file_path)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and hasattr(node.func, "attr")
                and node.func.attr == method_name
            ):
                yield node

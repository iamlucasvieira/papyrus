"""Module responsible for parsing information in a pyramid application."""

import ast
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

from papyrus.log import log_time

from .finder import Finder, PyramidFiles

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Route:
    """Dataclass representing a route in a pyramid application."""

    name: str
    pattern: str
    methods: set[str]


class Parser:
    """Class responsible for parsing information in a pyramid application."""

    @staticmethod
    @log_time(logger)
    def get_routes(
        base_dir: Path, routes_file_name: str | None, views_dir: str | None
    ) -> dict[str, Route]:
        """Get all routes from a pyramid application."""
        routes = Parser.get_routes_pattern(base_dir, routes_file_name)
        views = Parser.get_views_methods(base_dir, views_dir)
        return {
            route_name: Route(route_name, route_pattern, views[route_name])
            for route_name, route_pattern in routes.items()
        }

    @staticmethod
    @log_time(logger)
    def get_routes_pattern(base_dir: Path, file_name: str | None) -> dict[str, str]:
        """Get all routes from a pyramid application.

        Returns dict with keys being route name and value the pattern
        """
        routes_file = PyramidFiles.get_routes_path(base_dir, file_name)

        routes = {}
        crawler = AstCrawler(routes_file)
        for route_call in crawler.iter_calls([AstFilterMethodCall("add_route")]):
            route_name, route_pattern = Parser.route_call_to_route_name_and_pattern(
                route_call
            )
            if route_name and route_pattern:
                routes[route_name] = route_pattern

        return routes

    @staticmethod
    @log_time(logger)
    def get_views_methods(
        base_dir: Path, views_dir: str | None = None
    ) -> dict[str, set[str]]:
        """Get all views methods from a pyramid application."""
        views = defaultdict(set)
        views_path = base_dir / views_dir if views_dir else base_dir
        views_files = Finder.find_all_files(views_path, ".py")
        for views_file in views_files:
            crawler = AstCrawler(views_file)
            for view_call in crawler.iter_decorators_named("view_config"):
                view_name, view_method = Parser.view_call_to_route_name_and_method(
                    view_call
                )
                if view_name and view_method:
                    views[view_name].add(view_method)
        return views

    @staticmethod
    @log_time(logger)
    def route_call_to_route_name_and_pattern(
        route_call: ast.Call,
    ) -> tuple[str | None, str | None]:
        """Get the route name and pattern from an add_route call."""
        expected_length = 2
        if len(route_call.args) < expected_length:
            logger.warning("Skipping route call: %s", route_call)
            return None, None
        route_name, route_pattern = route_call.args[:expected_length]
        return getattr(route_name, "value", None), getattr(route_pattern, "value", None)

    @staticmethod
    @log_time(logger)
    def view_call_to_route_name_and_method(
        view_call: ast.Call,
    ) -> tuple[str | None, str | None]:
        """Get the view name and method from a decorator call."""
        expected_length = 2
        if len(view_call.keywords) < expected_length:
            logger.warning("Skipping view call: %s", view_call)
            return None, None
        keywords = {k.arg: k.value for k in view_call.keywords}
        route_name = getattr(keywords.get("route_name"), "value", None)
        request_method = getattr(keywords.get("request_method"), "value", None)
        return route_name, request_method


class AstFilter(ABC):
    """Abstract base class for AST filters."""

    @abstractmethod
    def __call__(self, node: ast.AST) -> bool:
        """Filter the AST node."""


class AstCrawler:
    """Class responsible for crawling the AST of a pyramid application."""

    def __init__(self, python_code: str | Path | ast.AST) -> None:
        """Initialize the AST crawler with a file path.

        Args:
            python_code: The Python code to parse. Can be a string, a path to a file,
                or an AST.

        """
        if isinstance(python_code, str):
            self.tree = ast.parse(python_code)
        elif isinstance(python_code, Path):
            self.tree = ast.parse(python_code.read_text())
        elif isinstance(python_code, ast.Module):
            self.tree = python_code
        else:
            msg = "Invalid python_code"
            raise ValueError(msg)

    @log_time(logger)
    def iter_calls(
        self,
        filters: list[AstFilter] | None = None,
        tree: ast.AST | None = None,
    ) -> Generator[ast.Call]:
        """Yield each call to a specific call node.

        Args:
            filters: The filters to apply to the AST.
            tree: The AST to search for method calls. If not provided,
                the AST of the file will be used.

        """
        filters = filters or []
        for node in ast.walk(tree or self.tree):
            if isinstance(node, ast.Call) and all(f(node) for f in filters):
                yield node

    @log_time(logger)
    def iter_decorators_named(
        self,
        decorator_name: str,
        filters: list[AstFilter] | None = None,
        tree: ast.AST | None = None,
    ) -> Generator[ast.Call]:
        """Yield each decorator named decorator_name from function/class definitions.

        Args:
            decorator_name: The name of the decorator to search for.
            filters: The filters to apply to the AST.
            tree: The AST to search for decorators. If not provided,
                the AST of the file will be used.

        Yields:
            ast.Call nodes representing decorators with the specified name

        """
        filters = filters or []
        filters.append(AstFilterDecorator(decorator_name))
        for node in ast.walk(tree or self.tree):
            is_function = isinstance(node, ast.FunctionDef)
            is_class = isinstance(node, ast.ClassDef)
            if (is_function or is_class) and hasattr(node, "decorator_list"):
                for decorator in node.decorator_list:
                    yield from self.iter_calls(filters, decorator)


class AstFilterMethodCall(AstFilter):
    """Filter for method calls."""

    def __init__(self, method_name: str) -> None:
        """Initialize the filter with a method name."""
        self.method_name = method_name

    def __call__(self, node: ast.AST) -> bool:
        """Filter the AST node."""
        return (
            isinstance(node, ast.Call)
            and hasattr(node.func, "attr")
            and node.func.attr == self.method_name
        )


class AstFilterDecorator(AstFilter):
    """Filter for decorators."""

    def __init__(self, decorator_name: str) -> None:
        """Initialize the filter with a decorator name."""
        self.decorator_name = decorator_name

    def __call__(self, node: ast.AST) -> bool:
        """Filter the AST node."""
        return (
            isinstance(node, ast.Call)
            and hasattr(node.func, "id")
            and node.func.id == self.decorator_name
        )

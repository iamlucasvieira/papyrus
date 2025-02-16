"""Tests for the parsing module."""

import ast
from pathlib import Path

import pytest

from papyrus.parsing import AstCrawler, AstFilterMethodCall, Parser
from papyrus.pyramid import PyramidInfo, Route


class TestParsing:
    """Tests for the Parsing class."""

    def test_get_routes_pattern(self: "TestParsing", pyramid_app_dir: Path) -> None:
        """Test the get_routes_pattern method."""
        results = Parser.get_routes_pattern(pyramid_app_dir, "routes.py")
        assert results == {
            "home": "/",
            "about": "/about",
            "user": "/user/{id}",
        }

    def test_get_routes_pattern_no_file(
        self: "TestParsing", pyramid_app_dir: Path
    ) -> None:
        """Test the get_routes_pattern method with no file."""
        with pytest.raises(FileNotFoundError, match="missing.py"):
            Parser.get_routes_pattern(pyramid_app_dir, "missing.py")

    def test_get_views_methods(self: "TestParsing", pyramid_app_dir: Path) -> None:
        """Test the get_views_methods method."""
        results = Parser.get_views_methods(pyramid_app_dir, "views")
        assert results == {
            "home": {"GET"},
            "about": {"GET"},
            "user": {"GET", "POST", "PUT", "DELETE"},
        }

    @pytest.mark.parametrize(
        ("call", "expected_name", "expected_pattern"),
        [
            ("config.add_route('about', '/about')", "about", "/about"),
            ("config.add_route('user')", None, None),
            ("config.add_route()", None, None),
            ("config.add_route('about', '/about', 'GET')", "about", "/about"),
        ],
        ids=["valid_call", "no_pattern", "no_args", "extra_args"],
    )
    def test_route_call_to_route_name_and_pattern(
        self: "TestParsing",
        call: str,
        expected_name: str | None,
        expected_pattern: str | None,
    ) -> None:
        """Test the call_to_route_name_and_pattern method."""
        node = getattr(ast.parse(call).body[0], "value", None)
        assert isinstance(node, ast.Call), "Expected a call node"
        route_name, route_pattern = Parser.route_call_to_route_name_and_pattern(node)
        assert route_name == expected_name
        assert route_pattern == expected_pattern

    def test_get_routes(self: "TestParsing", pyramid_app_dir: Path) -> None:
        """Test the get_routes method."""
        pyramid_info = PyramidInfo(routes_file_name="routes.py", views_dir_name="views")
        routes = Parser.get_routes(pyramid_app_dir, pyramid_info)
        assert routes == {
            "home": Route("home", "/", {"GET"}),
            "about": Route("about", "/about", {"GET"}),
            "user": Route("user", "/user/{id}", {"GET", "POST", "PUT", "DELETE"}),
        }


class TestAstCrawler:
    """Tests for the AstCrawler class."""

    @pytest.fixture
    def routes_file(self: "TestAstCrawler", pyramid_app_dir: Path) -> Path:
        """Fixture for a routes file."""
        return pyramid_app_dir / "routes.py"

    @pytest.fixture
    def views_file(self: "TestAstCrawler", pyramid_app_dir: Path) -> Path:
        """Fixture for a views file."""
        return pyramid_app_dir / "views" / "views.py"

    def test_iter_calls(self: "TestAstCrawler", routes_file: Path) -> None:
        """Test the iter_add_route_calls method."""
        crawler = AstCrawler(routes_file)
        calls = list(crawler.iter_calls())
        expected_calls = 3
        assert len(calls) == expected_calls, (
            f"Expected {expected_calls} calls to add_route"
        )
        args = {getattr(call.args[0], "value", None) for call in calls}
        assert args == {
            "home",
            "about",
            "user",
        }

    def test_iter_calls_with_filters(self: "TestAstCrawler") -> None:
        """Test the iter_calls method with filters."""
        tree = ast.parse(
            "config.called_twice(); config.called_once(); config.called_twice()"
        )
        crawler = AstCrawler(tree)
        calls = list(crawler.iter_calls([AstFilterMethodCall("called_twice")]))
        expected_calls = 2
        assert len(calls) == expected_calls, (
            f"Expected {expected_calls} calls to called_twice"
        )

    def test_iter_decorators_named(self: "TestAstCrawler", views_file: Path) -> None:
        """Test the iter_decorators_named method."""
        crawler = AstCrawler(views_file)
        calls = list(crawler.iter_decorators_named("view_config"))
        expected_calls = 6
        assert len(calls) == expected_calls, (
            f"Expected {expected_calls} calls to view_config"
        )

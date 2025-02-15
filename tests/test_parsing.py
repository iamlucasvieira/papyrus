"""Tests for the parsing module."""

import ast
from pathlib import Path

import pytest

from papyrus.parsing import AstCrawler, Parser


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

    def test_get_routes_pattern_use_default(
        self: "TestParsing", pyramid_app_dir: Path
    ) -> None:
        """Test the get_all_routes method with no file."""

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
    def test_call_to_route_name_and_pattern(
        self: "TestParsing",
        call: str,
        expected_name: str | None,
        expected_pattern: str | None,
    ) -> None:
        """Test the call_to_route_name_and_pattern method."""
        node = getattr(ast.parse(call).body[0], "value", None)
        assert isinstance(node, ast.Call), "Expected a call node"
        route_name, route_pattern = Parser.call_to_route_name_and_pattern(node)
        assert route_name == expected_name
        assert route_pattern == expected_pattern


class TestAstCrawler:
    """Tests for the AstCrawler class."""

    @pytest.fixture
    def routes_file(self: "TestAstCrawler", pyramid_app_dir: Path) -> Path:
        """Fixture for a routes file."""
        return pyramid_app_dir / "routes.py"

    def test_iter_add_route_calls(self: "TestAstCrawler", routes_file: Path) -> None:
        """Test the iter_add_route_calls method."""
        calls = list(AstCrawler.iter_method_calls(routes_file, "add_route"))
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

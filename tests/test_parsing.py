"""Tests for the parsing module."""

from pathlib import Path

import pytest

from papyrus.parsing import Parser


class TestParsing:
    """Tests for the Parsing class."""

    def test_get_routes_pattern(self: "TestParsing", pyramid_app_dir: Path) -> None:
        """Test the get_routes_pattern method."""
        results = Parser.get_routes_pattern(pyramid_app_dir, "routes.py")
        assert results

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

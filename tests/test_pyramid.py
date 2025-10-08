"""Tests for the pyramid module."""

from pathlib import Path

import pytest

from papyrus.exceptions import InvalidUrlPatternError
from papyrus.pyramid import PyramidFiles, extract_url_parameters


class TestPyramidFiles:
    """Tests for the PyramidFiles class."""

    def test_get_routes(self: "TestPyramidFiles", pyramid_app_dir: Path) -> None:
        """Assert get_routes returns existing file."""
        routes_file = PyramidFiles.get_routes_path(pyramid_app_dir, "routes.py")
        assert routes_file.exists()

    def test_get_routes_not_found(
        self: "TestPyramidFiles", pyramid_app_dir: Path
    ) -> None:
        """Assert get_routes raises error when routes file not found."""
        with pytest.raises(FileNotFoundError, match=r"missing\.py"):
            PyramidFiles.get_routes_path(pyramid_app_dir, "missing.py")


class TestExtractUrlParameters:
    """Tests for the extract_url_parameters function."""

    @pytest.mark.parametrize(
        ("pattern", "expected"),
        [
            ("/user/{id}/profile/{section}", ["id", "section"]),
            ("/user/{id}/profile", ["id"]),
            ("/user/", []),
        ],
        ids=["with_two_params", "with_one_param", "no_params"],
    )
    def test_extract_url_parameters(
        self: "TestExtractUrlParameters", pattern: str, expected: list[str]
    ) -> None:
        """Assert extract_url_parameters returns correct parameters."""
        assert extract_url_parameters(pattern) == expected

    @pytest.mark.parametrize(
        ("invalid_pattern", "match"),
        [
            ("/user/{id", "Missing closing brace"),
            ("/user/{id}/profile/{}", "Missing parameter name"),
        ],
        ids=["missing_closing_brace", "missing_parameter_name"],
    )
    def test_extract_url_parameters_invalid_pattern(
        self: "TestExtractUrlParameters", invalid_pattern: str, match: str
    ) -> None:
        """Assert extract_url_parameters raises error for invalid pattern."""
        with pytest.raises(InvalidUrlPatternError, match=match):
            extract_url_parameters(invalid_pattern)

"""Tests for the pyramid module."""

from pathlib import Path

import pytest

from papyrus.pyramid import PyramidFiles


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
        with pytest.raises(FileNotFoundError, match="missing.py"):
            PyramidFiles.get_routes_path(pyramid_app_dir, "missing.py")

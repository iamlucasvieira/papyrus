"""Tets for the finder module."""

from pathlib import Path

import pytest

from papyrus.finder import Finder


class TestFinder:
    """Test suite for the Finder class."""

    @pytest.fixture
    def tmp_dir(self: "TestFinder", tmp_path: Path) -> Path:
        """Create a temporary directory for testing."""
        base_path = tmp_path
        nested_path = tmp_path / "dir"
        double_nested_path = tmp_path / "dir" / "dir"

        nested_path.mkdir()
        double_nested_path.mkdir()

        files_config = [
            base_path / "test.py",
            nested_path / "nested.py",
            nested_path / "test.py",
            double_nested_path / "double_nested.py",
            double_nested_path / "test.py",
        ]

        for f in files_config:
            f.touch()

        return tmp_path

    def test_find_file_returns_first(self: "TestFinder", tmp_dir: Path) -> None:
        """Test the find_file method returns first found file."""
        result = Finder.find_file(tmp_dir, "test.py")
        assert result == tmp_dir / "test.py"

    def test_find_file_returns_none(self: "TestFinder", tmp_dir: Path) -> None:
        """Test the find_file method returns None when no file is found."""
        result = Finder.find_file(tmp_dir, "missing.py")
        assert result is None

    def test_find_file_returns_nested(self: "TestFinder", tmp_dir: Path) -> None:
        """Test the find_file method returns first found file in nested directories."""
        result = Finder.find_file(tmp_dir, "double_nested.py")
        assert result == tmp_dir / "dir" / "dir" / "double_nested.py"

    def test_find_all_files_returns_all(self: "TestFinder", tmp_dir: Path) -> None:
        """Test the find_all_files method returns all files of a certain type."""
        result = Finder.find_all_files(tmp_dir, ".py")
        expected_length = 5
        assert len(set(result)) == expected_length, "Expected 5 unique files."

    def test_find_all_files_returns_none(self: "TestFinder", tmp_dir: Path) -> None:
        """Test the find_all_files method returns an empty list when no files found."""
        result = Finder.find_all_files(tmp_dir, ".txt")
        assert result == []

"""Exceptions for Papyrus."""

from pathlib import Path


class RoutesFileNotFoundError(FileNotFoundError):
    """Exception raised when the routes file is not found."""

    def __init__(self, file_name: str, base_dir: Path) -> None:
        """Initialize the exception."""
        super().__init__(f"File {file_name} not found in {base_dir}.")


class ViewsDirNotFoundError(FileNotFoundError):
    """Exception raised when the views directory is not found."""

    def __init__(self, views_dir: str, base_dir: Path) -> None:
        """Initialize the exception."""
        super().__init__(f"Directory {views_dir} not found in {base_dir}.")


class InvalidUrlPatternError(ValueError):
    """Exception raised when the URL pattern is invalid."""

    def __init__(self, pattern: str, issue: str) -> None:
        """Initialize the exception."""
        super().__init__(f"Invalid URL pattern: {pattern} ({issue})")

"""Module responsible for finding information in a pyramid application."""

from pathlib import Path


class Finder:
    """Class responsible for finding information in a pyramid application."""

    def __init__(self: "Finder") -> None:
        """Initialize the finder with the request."""

    def find_file(self: "Finder", file_name: str) -> Path:
        """Find the file in the request."""
        return Path(file_name)

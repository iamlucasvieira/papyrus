"""Module responsible for finding information in a pyramid application."""

import logging
from pathlib import Path

from papyrus.exceptions import RoutesFileNotFoundError, ViewsDirNotFoundError
from papyrus.log import log_time

logger = logging.getLogger(__name__)


class Finder:
    """Class responsible for finding files in a pyramid application."""

    @staticmethod
    @log_time(logger)
    def find_path(current_dir: Path, name: str, is_dir: bool = False) -> Path | None:
        """Find a file or directory recursively, returns first match."""
        try:
            return next(p for p in current_dir.rglob(name) if p.is_dir() == is_dir)
        except StopIteration:
            return None

    @staticmethod
    @log_time(logger)
    def find_file(current_dir: Path, file_name: str) -> Path | None:
        """Find a file recursively, returns first match."""
        return Finder.find_path(current_dir, file_name, is_dir=False)

    @staticmethod
    @log_time(logger)
    def find_dir(current_dir: Path, dir_name: str) -> Path | None:
        """Find a directory recursively, returns first match."""
        return Finder.find_path(current_dir, dir_name, is_dir=True)

    @staticmethod
    @log_time(logger)
    def find_all_files(current_dir: Path, file_type: str) -> list[Path]:
        """Find all files of a certain type in a directory."""
        return list(current_dir.rglob(f"*{file_type}"))


class PyramidFiles:
    """Class with utilities for getting pyramid files."""

    @staticmethod
    @log_time(logger)
    def get_routes_path(base_dir: Path, file_name: str) -> Path:
        """Return the path to routes file, otherwise raise FileNotFounderror."""
        file_path = Finder.find_file(base_dir, file_name)
        if not file_path:
            raise RoutesFileNotFoundError(file_name, base_dir)
        return file_path

    @staticmethod
    @log_time(logger)
    def get_views_path(base_dir: Path, views_dir: str) -> Path:
        """Return the path to views directory, otherwise raise FileNotFounderror."""
        view_dir = Finder.find_dir(base_dir, views_dir)
        if not view_dir:
            raise ViewsDirNotFoundError(views_dir, base_dir)
        return view_dir

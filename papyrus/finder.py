"""Module responsible for finding information in a pyramid application."""

import logging
import os
from pathlib import Path

from papyrus.log import log_time

logger = logging.getLogger(__name__)

ROUTES_FILE_NAME = os.getenv("PAPYRUS_ROUTES_FILE_NAME", "routes.py")


class Finder:
    """Class responsible for finding files in a pyramid application."""

    @staticmethod
    @log_time(logger)
    def find_file(current_dir: Path, file_name: str) -> Path | None:
        """Find a file recursevely, returns first match."""
        if (current_dir / file_name).exists():
            return current_dir / file_name

        for path in current_dir.iterdir():
            if path.is_dir():
                result = Finder.find_file(path, file_name)
                if result:
                    return result

        return None

    @staticmethod
    @log_time(logger)
    def find_all_files(current_dir: Path, file_type: str) -> list[Path]:
        """Find all files of a certain type in a directory."""
        result = []
        for path in current_dir.iterdir():
            if path.is_dir():
                result += Finder.find_all_files(path, file_type)
            elif path.suffix == file_type:
                result.append(path)
        return result


class PyramidFiles:
    """Class with utilities for getting pyramid files."""

    @staticmethod
    @log_time(logger)
    def get_routes_path(base_dir: Path, file_name: str | None) -> Path:
        """Return the path to routes file, otherwise raise FileNotFounderror."""
        file_name = file_name or ROUTES_FILE_NAME
        file_path = Finder.find_file(base_dir, file_name)
        if not file_path:
            msg = f"File {file_name} not found in {base_dir}."
            raise FileNotFoundError(msg)
        return file_path

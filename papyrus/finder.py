"""Module responsible for finding information in a pyramid application."""

from pathlib import Path


class Finder:
    """Class responsible for finding files in a pyramid application."""

    def __init__(self: "Finder") -> None:
        """Initialize the finder with the request."""

    @staticmethod
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
    def find_all_files(current_dir: Path, file_type: str) -> list[Path]:
        """Find all files of a certain type in a directory."""
        result = []
        for path in current_dir.iterdir():
            if path.is_dir():
                result += Finder.find_all_files(path, file_type)
            elif path.suffix == file_type:
                result.append(path)
        return result

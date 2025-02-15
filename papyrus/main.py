"""Application entry point."""

import typer
from rich.console import Console

from papyrus.log import setup_logging

app = typer.Typer()
console = Console()

logger = setup_logging()


@app.command()
def main(name: str) -> None:
    """Say hello to NAME."""
    logger.info("Starting Papyrus...")
    console.print(f"Hello, {name}!")


if __name__ == "__main__":
    app()

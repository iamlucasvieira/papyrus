"""Application entry point."""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main(name: str) -> None:
    """Say hello to NAME."""
    console.print(f"Hello, {name}!")


if __name__ == "__main__":
    app()

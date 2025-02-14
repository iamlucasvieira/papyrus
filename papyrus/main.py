"""Application entry point."""

import typer

app = typer.Typer()


@app.command()
def main(name: str) -> None:
    """Say hello to NAME."""
    print(f"Hello {name}")


if __name__ == "__main__":
    app()

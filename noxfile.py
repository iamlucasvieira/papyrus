"""Nox file for running tests and linting."""

from typing import Any

import nox


def sync_install(session: nox.Session, *args: str, **kwargs: dict[str, Any]) -> None:
    """Install the package in synchronous mode."""
    session.run_install("uv", "sync", "--frozen", "--quiet", *args, **kwargs)


@nox.session(venv_backend="uv")
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests."""
    sync_install(session, env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location})
    session.run("pytest", *session.posargs)


@nox.session(venv_backend="uv")
def ruff(session: nox.Session) -> None:
    """Run ruff."""
    sync_install(session, env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location})
    session.run("ruff", "format")
    session.run("ruff", "check", "--fix")


@nox.session(venv_backend="uv")
def mypy(session: nox.Session) -> None:
    """Run mypy."""
    sync_install(session, env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location})
    session.run("mypy")

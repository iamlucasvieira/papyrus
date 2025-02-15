"""Pytest conftest file."""

from pathlib import Path

import pytest


@pytest.fixture
def pyramid_app_dir(tmp_path: Path) -> Path:
    """Fixture for a directory with routes."""
    routes_data = """
from pyramid.config import Configurator

def includeme(config: Configurator) -> None:
    config.add_route("home", "/")
    config.add_route("about", "/about")
    config.add_route("user", "/user/{id}")
    """

    views_data = """
from pyramid.view import view_config

@view_config(route_name="home", method="GET")
def home(request):
    return {"name": "home"}

@view_config(route_name="about", method="GET")
def about(request):
    return {"name": "about"}

@view_config(route_name="user", method="GET")
@view_config(route_name="user", method="POST")
@view_config(route_name="user", method="PUT")
@view_config(route_name="user", method="DELETE")
def user(request):
    return {"name": "user"}
    """
    views_dir = tmp_path / "views"
    views_dir.mkdir()

    routes_file = tmp_path / "routes.py"
    routes_file.write_text(routes_data)

    views_file = views_dir / "views.py"
    views_file.write_text(views_data)

    return tmp_path

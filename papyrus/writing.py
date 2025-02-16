"""Module responsible for writing OpenAPI documentation."""

from dataclasses import dataclass

import yaml
from cattrs import Converter
from cattrs.gen import make_dict_unstructure_fn, override

from papyrus.pyramid import Route, extract_url_parameters


@dataclass
class Info:
    """OpenAPI info object."""

    title: str
    version: str


@dataclass(frozen=True)
class Parameter:
    """OpenAPI parameter object."""

    name: str
    _in: str
    required: bool
    schema: dict[str, str]


@dataclass(frozen=True)
class Operation:
    """OpenAPI operation object."""

    summary: str
    description: str
    parameters: list[Parameter]
    responses: dict[str, dict[str, str]]

    @classmethod
    def from_route(
        cls: type["Operation"], route: Route, method: str
    ) -> "Operation | None":
        """Create an Operation from a Route."""
        if method not in route.methods:
            return None

        description = f"{method} {route.name}"
        params = extract_url_parameters(route.pattern)

        return cls(
            summary=description,
            description=description,
            parameters=[
                Parameter(
                    name=param,
                    _in="path",
                    required=True,
                    schema={"type": "string"},
                )
                for param in params
            ],
            responses={
                "200": {"description": "OK"},
                "404": {"description": "Not Found"},
                "401": {"description": "Unauthorized"},
            },
        )


@dataclass(frozen=True)
class PathItem:
    """OpenAPI path item object."""

    summary: str
    description: str
    get: Operation | None = None
    post: Operation | None = None
    put: Operation | None = None
    delete: Operation | None = None

    @classmethod
    def from_route(cls: type["PathItem"], route: Route) -> "PathItem":
        """Create a PathItem from a Route."""
        description = f"{route.name}"
        return cls(
            summary=description,
            description=description,
            get=Operation.from_route(route, "GET"),
            post=Operation.from_route(route, "POST"),
            put=Operation.from_route(route, "PUT"),
            delete=Operation.from_route(route, "DELETE"),
        )


c = Converter()
c.register_unstructure_hook(
    Parameter,
    make_dict_unstructure_fn(
        Parameter,
        c,
        _in=override(rename="in"),
    ),
)
c.register_unstructure_hook(
    PathItem,
    make_dict_unstructure_fn(
        PathItem,
        c,
        get=override(omit_if_default=True),
        post=override(omit_if_default=True),
        put=override(omit_if_default=True),
        delete=override(omit_if_default=True),
    ),
)


@dataclass(frozen=True)
class OpenAPI:
    """OpenAPI root object."""

    openapi: str
    info: Info
    paths: dict[str, PathItem]

    @classmethod
    def from_routes(cls: type["OpenAPI"], routes: list[Route]) -> "OpenAPI":
        """Create a OpenAPI object from a list of routes."""
        return cls(
            openapi="3.0.3",
            info=Info(title="API", version="1.0.0"),
            paths={route.pattern: PathItem.from_route(route) for route in routes},
        )

    def to_yaml(self) -> str:
        """Convert the OpenAPI object to a YAML string."""
        return yaml.dump(
            c.unstructure(self),
        )

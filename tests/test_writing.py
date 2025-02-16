"""Tests for the writing module."""

import pytest

from papyrus.pyramid import Route
from papyrus.writing import OpenAPI, Operation, Parameter, PathItem


class TestOperation:
    """Tests for the Operation class."""

    @pytest.mark.parametrize(
        ("route", "expected_parameters"),
        [
            (Route(name="test", pattern="/test", methods={"GET"}), []),
            (
                Route(name="test", pattern="/test/{id}", methods={"GET"}),
                [
                    Parameter(
                        name="id", _in="path", required=True, schema={"type": "string"}
                    )
                ],
            ),
        ],
        ids=["no_parameters", "one_parameter"],
    )
    def test_from_route(
        self: "TestOperation", route: Route, expected_parameters: list[Parameter]
    ) -> None:
        """Test the from_route method."""
        operation = Operation.from_route(route, "GET")
        assert isinstance(operation, Operation)
        assert operation.parameters == expected_parameters

    def test_from_route_method_missing(self: "TestOperation") -> None:
        """Test the from_route method with no method."""
        operation = Operation.from_route(
            Route(name="test", pattern="/test", methods=set()), "GET"
        )
        assert operation is None


class TestPathItem:
    """Tests for the PathItem class."""

    @pytest.mark.parametrize(
        "methods",
        [
            {"GET"},
            {"GET", "POST"},
            {"GET", "POST", "PUT", "DELETE"},
        ],
    )
    def test_from_route(self: "TestPathItem", methods: set[str]) -> None:
        """Test that methods are present in the path item."""
        all_methods = {"GET", "POST", "PUT", "DELETE"}
        route = Route(name="test", pattern="/test", methods=methods)
        path_item = PathItem.from_route(route)
        for method in methods:
            assert getattr(path_item, method.lower()) is not None

        for method in all_methods - methods:
            assert getattr(path_item, method.lower()) is None


class TestOpenAPI:
    """Tests for the OpenAPI class."""

    def test_from_routes(self: "TestOpenAPI") -> None:
        """Test the from_routes method."""
        routes = [
            Route(name="test", pattern="/test", methods={"GET"}),
            Route(name="test2", pattern="/test2", methods={"POST"}),
            Route(name="test3", pattern="/test3", methods={"PUT"}),
            Route(name="test4", pattern="/test4", methods={"DELETE"}),
        ]
        openapi = OpenAPI.from_routes(routes)
        expected_paths = 4
        assert len(openapi.paths) == expected_paths

    def test_to_yaml(self: "TestOpenAPI") -> None:
        """Test the to_yaml method."""
        routes = [
            Route(name="test", pattern="/test/{id}", methods={"GET"}),
        ]
        expected_yaml = """info:
  title: API
  version: 1.0.0
openapi: 3.0.3
paths:
  /test/{id}:
    description: test
    get:
      description: GET test
      parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
      responses:
        '200':
          description: OK
        '401':
          description: Unauthorized
        '404':
          description: Not Found
      summary: GET test
    summary: test
"""
        openapi = OpenAPI.from_routes(routes)
        assert openapi.to_yaml() == expected_yaml

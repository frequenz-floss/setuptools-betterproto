# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Tests for the setuptools_betterproto package."""

import dataclasses
import logging
from typing import Any
from unittest import mock

import pytest

from setuptools_betterproto import ProtobufConfig


@dataclasses.dataclass(frozen=True)
class DefaultsTestCase:
    """A test case for an error when loading the configuration from the `pyproject.toml` file."""

    name: str
    """The name of the test case."""

    defaults: dict[str, Any]
    """The default values for the configuration options."""

    def __str__(self) -> str:
        """Return the test case as a string."""
        return self.name


@pytest.mark.parametrize(
    "test_case",
    [
        DefaultsTestCase("defaults_empty", {}),
        DefaultsTestCase(
            "defaults_all",
            {
                "proto_path": "test_path",
                "proto_glob": "",
                "include_paths": ("proto",),
                "out_dir": "generated",
            },
        ),
    ],
    ids=str,
)
@pytest.mark.parametrize(
    "pyproject_toml_contents, expected_overrides",
    [
        (b"", {}),
        (b"[tool.setuptools_betterproto]", {}),
        (
            b"""
[tool.setuptools_betterproto]
proto_path = "test_path"
""",
            {"proto_path": "test_path"},
        ),
        (
            b"""
[tool.setuptools_betterproto]
proto_path = "test_path"
proto_glob = "test_glob"
include_paths = ["test_include"]
out_dir = "test_out"
""",
            {
                "proto_path": "test_path",
                "proto_glob": "test_glob",
                "include_paths": ["test_include"],
                "out_dir": "test_out",
            },
        ),
    ],
    ids=["file_empty", "file_empty_section", "file_proto_path", "file_all"],
)
def test_from_proto(
    test_case: DefaultsTestCase,
    pyproject_toml_contents: bytes,
    expected_overrides: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test from_proto() when it is successful."""
    expected = dataclasses.replace(
        ProtobufConfig(**test_case.defaults), **expected_overrides
    )

    with mock.patch(
        "setuptools_betterproto._config.open",
        mock.mock_open(read_data=pyproject_toml_contents),
    ):
        config = ProtobufConfig.from_pyproject_toml(**test_case.defaults)

    assert config == expected
    assert caplog.record_tuples == []


@pytest.mark.parametrize(
    "test_case",
    [
        DefaultsTestCase("empty-defaults", {}),
        DefaultsTestCase(
            "all-defaults",
            {
                "proto_path": "test_path",
                "proto_glob": "",
                "include_paths": ("proto",),
                "out_dir": "generated",
            },
        ),
    ],
    ids=str,
)
@pytest.mark.parametrize(
    "exception, should_warn",
    [
        (FileNotFoundError("Not found"), False),
        (OSError("Can't read"), True),
    ],
    ids=lambda x: x.__name__ if isinstance(x, type) else f"warn:{x}",
)
@pytest.mark.parametrize("pyproject_toml_path", [None, "pyproject.toml"], ids=str)
def test_from_proto_with_error(
    test_case: DefaultsTestCase,
    exception: type[Exception],
    should_warn: bool,
    pyproject_toml_path: str | None,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test from_proto() when there are errors loading the configuration file."""
    expected = ProtobufConfig(**test_case.defaults)

    with mock.patch("setuptools_betterproto._config.open", side_effect=exception):
        config = (
            ProtobufConfig.from_pyproject_toml(**test_case.defaults)
            if pyproject_toml_path is None
            else ProtobufConfig.from_pyproject_toml(
                pyproject_toml_path, **test_case.defaults
            )
        )

    assert config == expected

    warnings = []
    if should_warn:
        warnings = [
            (
                "setuptools_betterproto._config",
                logging.WARNING,
                f"WARNING: Failed to load {pyproject_toml_path or 'pyproject.toml'}: Can't read",
            )
        ]
    assert caplog.record_tuples == warnings


def test_from_proto_unknown_keys(caplog: pytest.LogCaptureFixture) -> None:
    """Test from_proto() when there are unknown keys in the configuration."""
    pyproject_toml = b"""
[tool.setuptools_betterproto]
unknown = "unknown"
"""
    with mock.patch(
        "setuptools_betterproto._config.open", mock.mock_open(read_data=pyproject_toml)
    ):
        config = ProtobufConfig.from_pyproject_toml()

    assert config == ProtobufConfig()
    assert (
        "setuptools_betterproto._config",
        logging.WARNING,
        "WARNING: There are some configuration keys in pyproject.toml we don't know "
        "about and will be ignored: 'unknown'",
    ) in caplog.record_tuples

# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Tests for the setuptools_betterproto package."""

import sys
from unittest import mock

from setuptools import Distribution

from setuptools_betterproto import CompileProto, ProtobufConfig

CONFIG = ProtobufConfig(
    proto_path="test_path",
    proto_glob="*.test",
    include_paths=["test_include1", "test_include2"],
    out_dir="test_out",
)


def create_command() -> CompileProto:
    """Create a new instance of the command with a mocked distribution."""
    dist = mock.MagicMock(spec=Distribution)
    dist.verbose = True
    return CompileProto(dist)


def test_initialize_options() -> None:
    """Test the initialization of the command options."""
    command = create_command()

    with mock.patch(
        "setuptools_betterproto._command._config",
    ) as config_module:
        config_module.ProtobufConfig.from_pyproject_toml.return_value = CONFIG
        command.initialize_options()

    assert command.proto_path == CONFIG.proto_path
    assert command.proto_glob == CONFIG.proto_glob
    assert command.include_paths == ",".join(CONFIG.include_paths)
    assert command.out_dir == CONFIG.out_dir


def test_run() -> None:
    """Test the initialization of the command options."""
    command = create_command()

    command.proto_path = CONFIG.proto_path
    command.proto_glob = CONFIG.proto_glob
    command.include_paths = ",".join(CONFIG.include_paths)
    command.out_dir = CONFIG.out_dir

    with (
        mock.patch(
            "setuptools_betterproto._command.subprocess",
        ) as subprocess_module,
        mock.patch.object(
            command,
            "_expand_paths",
            return_value=(
                "test_path/proto1.test",
                "test_path/proto2.test",
            ),
        ),
    ):
        command.run()

    subprocess_module.run.assert_called_once_with(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            "-Itest_path",
            "-Itest_include1",
            "-Itest_include2",
            "--python_betterproto_out=test_out",
            "test_path/proto1.test",
            "test_path/proto2.test",
        ],
        check=True,
    )

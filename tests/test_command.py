# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Tests for the setuptools_betterproto package."""

import sys
from unittest import mock

from setuptools import Distribution
from typing_extensions import override

from setuptools_betterproto import CompileProto, ProtobufConfig

CONFIG = ProtobufConfig(
    proto_path="test_path",
    proto_glob="*.test",
    include_paths=["test_include1", "test_include2"],
    out_path="test_out",
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
    assert command.out_path == CONFIG.out_path


def test_run() -> None:
    """Test the initialization of the command options."""
    command = create_command()

    command.proto_path = CONFIG.proto_path
    command.proto_glob = CONFIG.proto_glob
    command.include_paths = ",".join(CONFIG.include_paths)
    command.out_path = CONFIG.out_path

    class _FakeConfig(ProtobufConfig):

        @property
        @override
        def expanded_include_files(self) -> list[str]:
            return ["test_include1", "test_include2"]

        @property
        @override
        def expanded_proto_files(self) -> list[str]:
            return ["test_path/proto1.test", "test_path/proto2.test"]

    command.config = _FakeConfig(
        proto_path=CONFIG.proto_path,
        proto_glob=CONFIG.proto_glob,
        include_paths=CONFIG.include_paths,
        out_path=CONFIG.out_path,
    )

    with mock.patch(
        "setuptools_betterproto._command.subprocess",
    ) as subprocess_module:
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

# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Setuptool hooks to build protobuf files.

This module contains a setuptools command that can be used to compile protocol
buffer files in a project.

It also runs the command as the first sub-command for the build command, so
protocol buffer files are compiled automatically before the project is built.
"""

import logging
import subprocess
import sys

import setuptools
import setuptools.command.build as _build_command
from typing_extensions import override

from . import _config

_logger = logging.getLogger(__name__)


class BaseProtoCommand(setuptools.Command):
    """A base class for commands that deal with protobuf files."""

    proto_path: str
    """The path of the root directory containing the protobuf files."""

    proto_glob: str
    """The glob pattern to use to find the protobuf files."""

    include_paths: str
    """Comma-separated list of paths to include when compiling the protobuf files."""

    out_path: str
    """The path of the root directory where the Python files will be generated."""

    config: _config.ProtobufConfig
    """The configuration object for the command."""

    description: str = "compile protobuf files using betterproto"
    """Description of the command."""

    user_options: list[tuple[str, str | None, str]] = [
        (
            "proto-path=",
            None,
            "path of the root directory containing the protobuf files",
        ),
        ("proto-glob=", None, "glob pattern to use to find the protobuf files"),
        (
            "include-paths=",
            None,
            "comma-separated list of paths to include when compiling the protobuf files",
        ),
        (
            "out-dir=",
            None,
            "path of the root directory where the Python files will be generated",
        ),
    ]
    """Options of the command."""

    @override
    def initialize_options(self) -> None:
        """Initialize options."""
        self.config = _config.ProtobufConfig.from_pyproject_toml()

        self.proto_path = self.config.proto_path
        self.proto_glob = self.config.proto_glob
        self.include_paths = ",".join(self.config.include_paths)
        self.out_path = self.config.out_path

    @override
    def finalize_options(self) -> None:
        """Finalize options."""
        self.config = _config.ProtobufConfig.from_strings(
            proto_path=self.proto_path,
            proto_glob=self.proto_glob,
            include_paths=self.include_paths,
            out_path=self.out_path,
        )


class CompileBetterproto(BaseProtoCommand):
    """A command to compile the protobuf files."""

    @override
    def run(self) -> None:
        """Compile the Python protobuf files."""
        proto_files = self.config.expanded_proto_files

        if not proto_files:
            _logger.warning(
                "No proto files found in %s with glob "
                "%s, skipping compilation of proto files.",
                self.config.proto_path,
                self.config.proto_glob,
            )
            return

        protoc_cmd = [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            *(f"-I{p}" for p in [self.config.proto_path, *self.config.include_paths]),
            f"--python_betterproto_out={self.config.out_path}",
            *proto_files,
        ]

        _logger.info("compiling proto files via: %s", " ".join(protoc_cmd))
        subprocess.run(protoc_cmd, check=True)


# This adds the build_betterproto command to the build sub-command.
# The name of the command is mapped to the class name in the pyproject.toml file,
# in the [project.entry-points.distutils.commands] section.
# The None value is an optional function that can be used to determine if the
# sub-command should be executed or not.
_build_command.build.sub_commands.insert(0, ("compile_betterproto", None))

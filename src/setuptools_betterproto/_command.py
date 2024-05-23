# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Setuptools commands to compile and distribute protobuf files.

This module contains a setuptools command that can be used to compile protocol
buffer files in a project and to add the protobuf files to the source distribution.

To be able to ship the proto files with the source distribution, a command to replace
the `sdist` command is also provided. This command will copy the proto files to the
source distribution before building it.
"""

import logging
import os
import shutil
import subprocess
import sys

import setuptools
import setuptools.command.sdist
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
        """Initialize options with default values."""
        self.config = _config.ProtobufConfig.from_pyproject_toml()

        self.proto_path = self.config.proto_path
        self.proto_glob = self.config.proto_glob
        self.include_paths = ",".join(self.config.include_paths)
        self.out_path = self.config.out_path

    @override
    def finalize_options(self) -> None:
        """Finalize options by converting them to a ProtobufConfig object."""
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
        """Compile the protobuf files to Python."""
        proto_files = self.config.expanded_proto_files

        if not proto_files:
            _logger.warning(
                "No proto files were found in the `proto_path` (%s) using `proto_glob` "
                "(%s). You probably want to check if you `proto_path` and `proto_glob` "
                "are configured correctly. We are not compiling any proto files!",
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


class AddProtoFiles(BaseProtoCommand):
    """A command to add the proto files to the source distribution."""

    def run(self) -> None:
        """Copy the proto files to the source distribution."""
        proto_files = self.config.expanded_proto_files
        include_files = self.config.expanded_include_files

        if include_files and not proto_files:
            _logger.warning(
                "Some proto files (%s) were found in the `include_paths` (%s), but "
                "no proto files were found in the `proto_path`. You probably want to "
                "check if your `proto_path` (%s) and `proto_glob` (%s) are configured "
                "correctly. We are not adding the found include files to the source "
                "distribution automatically!",
                len(include_files),
                ", ".join(self.config.include_paths),
                self.config.proto_path,
                self.config.proto_glob,
            )
            return

        if not proto_files:
            _logger.warning(
                "No proto files were found in the `proto_path` (%s) using `proto_glob` "
                "(%s). You probably want to check if you `proto_path` and `proto_glob` "
                "are configured correctly. We are not adding any proto files to the "
                "source distribution automatically!",
                self.config.proto_path,
                self.config.proto_glob,
            )
            return

        dest_dir = self.distribution.get_fullname()

        for file in (*proto_files, *include_files):
            self.copy_with_directories(file, os.path.join(dest_dir, file))

        _logger.info("added %s proto files", len(proto_files) + len(include_files))

    def copy_with_directories(self, src: str, dest: str) -> None:
        """Copy a file from src to dest, creating the destination's directory tree.

        Any directories that do not exist in dest will be created.

        Args:
            src: The full path of the source file.
            dest: The full path of the destination file.
        """
        dest_dir = os.path.dirname(dest)
        if not os.path.exists(dest_dir):
            _logger.debug("creating directory %s", dest_dir)
            os.makedirs(dest_dir)
        _logger.info("adding proto file to %s", dest)
        shutil.copyfile(src, dest)


class SdistWithProtoFiles(setuptools.command.sdist.sdist):
    """A command to build the source distribution with the proto files."""

    @override
    def run(self) -> None:
        """Add the proto files to the source distribution before building it."""
        self.run_command("add_proto_files")
        super().run()

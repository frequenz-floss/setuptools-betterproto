# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Setuptools hook entry-point to finalize the distribution options.

The `finalize_distribution_options` function is called by setuptools to finalize the
distribution options. It adds the `compile_betterproto` command to the build sub-commands
and replaces the `sdist` command with a custom one that includes the proto files.

It will also build the proto files early if the distribution is a binary distribution.
This is necessary to include the generated Python files in the binary distribution,
otherwise the file discovery runs before we manage to compile the proto files.

We still need to hook the sub-command into the build command to make sure editable
installs work correctly.
"""

import logging
from collections.abc import Container

import setuptools.command.build as _build_command
from setuptools.dist import Distribution

from . import _command, _config

_logger = logging.getLogger(__name__)


def finalize_distribution_options(dist: Distribution) -> None:
    """Make some final adjustments to the distribution options.

    We need to do some stuff early when setuptools runs to make sure all files are
    compiled and distributed appropriately.

    1. Replace the sdist command with a custom one that includes the proto files.
    2. Add the `compile_betterproto` command to the build sub-commands.
    3. If the distribution is a binary distribution, build the proto files early.

    Args:
        dist: The distribution object.
    """
    config = _config.ProtobufConfig.from_pyproject_toml()
    replace_sdist_command(dist)
    add_build_subcommand_compile_betterproto(dist)

    if not building_bdist(dist):
        return

    if not config.expanded_proto_files:
        _logger.warning(
            "No proto files found in %s with glob %s, skipping early automatic "
            "compilation of proto files.",
            config.proto_path,
            config.proto_glob,
        )
        return

    build_proto(dist)


def add_build_subcommand_compile_betterproto(dist: Distribution) -> None:
    """Add the compile_betterproto command to the build sub-commands."""
    sdist_cmd = dist.get_command_obj("build")
    assert isinstance(sdist_cmd, _build_command.build)
    sdist_cmd.sub_commands.append(("compile_betterproto", None))


def replace_sdist_command(dist: Distribution) -> None:
    """Replace the sdist command with a custom one that includes the proto files."""
    dist.cmdclass.update(sdist=_command.SdistWithProtoFiles)


def building_bdist(dist: Distribution) -> bool:
    """Check if the distribution is a binary distribution."""
    if not isinstance(dist.script_args, Container):
        return False
    for arg in dist.script_args:
        if arg.startswith("bdist"):
            return True
    return False


def build_proto(dist: Distribution) -> None:
    """Build the Python protobuf files."""
    _logger.info(
        "Compiling protobuf files early so they are included in the binary distribution."
    )
    compile_cmg = _command.CompileBetterproto(dist)
    compile_cmg.initialize_options()
    compile_cmg.finalize_options()
    compile_cmg.run()

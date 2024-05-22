# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Setuptools hook entry-point to finalize the distribution options.

The `finalize_distribution_options` function is called by setuptools to finalize the
distribution options. It adds the `compile_betterproto` command to the build sub-commands
and replaces the `sdist` command with a custom one that includes the proto files.
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

    Args:
        dist: The distribution object.
    """
    config = _config.ProtobufConfig.from_pyproject_toml()
    replace_sdist_command(dist)
    add_build_subcommand_compile_betterproto(dist)


def add_build_subcommand_compile_betterproto(dist: Distribution) -> None:
    """Add the compile_betterproto command to the build sub-commands."""
    sdist_cmd = dist.get_command_obj("build")
    assert isinstance(sdist_cmd, _build_command.build)
    sdist_cmd.sub_commands.append(("compile_betterproto", None))


def replace_sdist_command(dist: Distribution) -> None:
    """Replace the sdist command with a custom one that includes the proto files."""
    dist.cmdclass.update(sdist=_command.SdistWithProtoFiles)

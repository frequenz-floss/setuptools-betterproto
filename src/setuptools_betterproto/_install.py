# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Setuptools hook entry-point to finalize the distribution options.

The `finalize_distribution_options` function is called by setuptools to finalize the
distribution options. It adds the `compile_betterproto` command to the build
sub-commands.
"""

import setuptools.command.build as _build_command
from setuptools.dist import Distribution


def finalize_distribution_options(dist: Distribution) -> None:
    """Make some final adjustments to the distribution options.

    We need to do some stuff early when setuptools runs to make sure all files are
    compiled and distributed appropriately.

    Args:
        dist: The distribution object.
    """
    add_build_subcommand_compile_betterproto(dist)


def add_build_subcommand_compile_betterproto(dist: Distribution) -> None:
    """Add the compile_betterproto command to the build sub-commands."""
    sdist_cmd = dist.get_command_obj("build")
    assert isinstance(sdist_cmd, _build_command.build)
    sdist_cmd.sub_commands.append(("compile_betterproto", None))

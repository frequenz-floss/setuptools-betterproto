# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""Manages the configuration to generate files from the protobuf files."""

import dataclasses
import logging
import tomllib
from collections.abc import Sequence
from typing import Any, Self

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ProtobufConfig:
    """A configuration for the protobuf files.

    The configuration can be loaded from the `pyproject.toml` file using the class
    method `from_pyproject_toml()`.
    """

    proto_path: str = "."
    """The path of the root directory containing the protobuf files."""

    proto_glob: str = "*.proto"
    """The glob pattern to use to find the protobuf files."""

    include_paths: Sequence[str] = ()
    """The paths to add to the include path when compiling the protobuf files."""

    out_path: str = "."
    """The path of the root directory where the Python files will be generated."""

    @classmethod
    def from_pyproject_toml(
        cls, path: str = "pyproject.toml", /, **defaults: Any
    ) -> Self:
        """Create a new configuration by loading the options from a `pyproject.toml` file.

        The options are read from the `[tool.frequenz-repo-config.protobuf]`
        section of the `pyproject.toml` file.

        Args:
            path: The path to the `pyproject.toml` file.
            **defaults: The default values for the options missing in the file.  If
                a default is missing too, then the default in this class will be used.

        Returns:
            The configuration.
        """
        try:
            with open(path, "rb") as toml_file:
                pyproject_toml = tomllib.load(toml_file)
        except FileNotFoundError:
            return cls(**defaults)
        except OSError as err:
            _logger.warning("WARNING: Failed to load pyproject.toml: %s", err)
            return cls(**defaults)

        try:
            config = pyproject_toml["tool"]["setuptools_betterproto"]
        except KeyError:
            return cls(**defaults)

        default = cls(**defaults)
        known_keys = frozenset(dataclasses.asdict(default).keys())
        config_keys = frozenset(config.keys())
        if unknown_keys := config_keys - known_keys:
            _logger.warning(
                "WARNING: There are some configuration keys in pyproject.toml we don't "
                "know about and will be ignored: %s",
                ", ".join(f"'{k}'" for k in unknown_keys),
            )

        attrs = dict(defaults, **{k: config[k] for k in (known_keys & config_keys)})
        return dataclasses.replace(default, **attrs)

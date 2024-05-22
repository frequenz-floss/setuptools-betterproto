# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""A modern setuptools plugin to generate Python files from proto files using betterproto."""

from ._command import AddProtoFiles, CompileBetterproto
from ._config import ProtobufConfig
from ._install import finalize_distribution_options

__all__ = [
    "AddProtoFiles",
    "CompileBetterproto",
    "ProtobufConfig",
    "finalize_distribution_options",
]

# License: MIT
# Copyright © 2024 Frequenz Energy-as-a-Service GmbH

"""A modern setuptools plugin to generate Python files from proto files using betterproto."""

from ._command import CompileBetterproto
from ._config import ProtobufConfig

__all__ = [
    "CompileBetterproto",
    "ProtobufConfig",
]

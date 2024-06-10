# Betterproto Setuptools plugin

[![Build Status](https://github.com/frequenz-floss/setuptools-betterproto/actions/workflows/ci.yaml/badge.svg)](https://github.com/frequenz-floss/setuptools-betterproto/actions/workflows/ci.yaml)
[![PyPI Package](https://img.shields.io/pypi/v/setuptools-betterproto)](https://pypi.org/project/setuptools-betterproto/)
[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://frequenz-floss.github.io/setuptools-betterproto/)

## Introduction

A modern [`setuptools`](https://setuptools.pypa.io/) plugin to generate Python
files from proto files using [betterproto].

This plugin is based on
[`repo-config`](https://frequenz-floss.github.io/frequenz-repo-config-python/)'s
[`grpc_tools`
plugin](https://frequenz-floss.github.io/frequenz-repo-config-python/v0.9/reference/frequenz/repo/config/setuptools/grpc_tools/).

## Supported Platforms

The following platforms are officially supported (tested):

- **Python:** 3.11
- **Operating System:** Ubuntu Linux 20.04
- **Architectures:** amd64, arm64

## Quick Start

To add automatic [betterproto] code generation to your project, you need to add
this package to your build-dependencies in the `pyproject.toml` file, for
example:

```toml
[build-system]
requires = [
  "setuptools == 68.1.0",
  "setuptools-betterproto == 0.1.0",
]
build-backend = "setuptools.build_meta"
```

This uses a default configuration as follows:

* `proto_path`: This is the root directory where the proto files are located.
  By default, it is set to `.`.
* `proto_glob`: This is the glob pattern to match the proto files. The search
  is done recursively. By default, it is set to `*.proto`.
* `include_paths`: This is a list of paths to be added to the protobuf
  compiler's include path. By default, it is set to `[]`, but the `proto_path`
  directory is always automatically added.
* `out_path`: This is the directory where the generated Python files will be
  placed. By default, it is set to `.`.

These defaults can be changed via the `pypackage.toml` file too. For example:

```toml
[tool.setuptools_betterproto]
proto_path = "proto"
include_paths = ["api-common-protos"]
out_path = "src"
```

You should add [betterproto] as a dependency too, for example:

```toml
dependencies = ["betterproto == 2.0.0b6"]
```

Once this is done, the conversion of the proto files to Python files should be
automatic. Just try building the package with:

```sh
python -m pip install build
python -m build
```

A new command to generate the files will be also added to `setuptools`, you can
run it manually with:
```sh
python -c 'import setuptools; setuptools.setup()' compile_betterproto
```

You can also pass the configuration options via command line for quick testing,
try passing `--help` at the end of the command to see the available options.

## Contributing

If you want to know how to build this project and contribute to it, please
check out the [Contributing Guide](CONTRIBUTING.md).

## Similar projects

* [`setuptools-proto`](https://github.com/jameslan/setuptools-proto/): We didn't use this project because it seems a bit inactive and not widely used. It also seems to need some configuration as code, which we wanted to avoid.

[betterproto]: https://github.com/danielgtaylor/python-betterproto

# Betterproto Setuptools plugin

[![Build Status](https://github.com/frequenz-floss/setuptools-betterproto/actions/workflows/ci.yaml/badge.svg)](https://github.com/frequenz-floss/setuptools-betterproto/actions/workflows/ci.yaml)
[![PyPI Package](https://img.shields.io/pypi/v/setuptools-betterproto)](https://pypi.org/project/setuptools-betterproto/)
[![Docs](https://img.shields.io/badge/docs-latest-informational)](https://frequenz-floss.github.io/setuptools-betterproto/)

## Introduction

A modern [`setuptools`](https://setuptools.pypa.io/) plugin to generate Python files from proto files using [`betterproto`](https://github.com/danielgtaylor/python-betterproto).

This plugin is based on [`repo-config`](https://frequenz-floss.github.io/frequenz-repo-config-python/)'s [`grpc_tools` plugin](https://frequenz-floss.github.io/frequenz-repo-config-python/v0.9/reference/frequenz/repo/config/setuptools/grpc_tools/).

## Supported Platforms

The following platforms are officially supported (tested):

- **Python:** 3.11
- **Operating System:** Ubuntu Linux 20.04
- **Architectures:** amd64, arm64

## Contributing

If you want to know how to build this project and contribute to it, please
check out the [Contributing Guide](CONTRIBUTING.md).

## Similar projects

* [`setuptools-proto`](https://github.com/jameslan/setuptools-proto/): We didn't use this project because it seems a bit inactive and not widely used. It also seems to need some configuration as code, which we wanted to avoid.

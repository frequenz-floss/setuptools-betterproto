# Betterproto Setuptools plugin Release Notes

## Summary

<!-- Here goes a general summary of what this release is about -->

## Upgrading

<!-- Here goes notes on how to upgrade from previous versions, including deprecations and what they should be replaced with -->

## New Features

 - *Partial support* of Python 3.10:

   The python package can be used as is. But for testing purposes,
   dependencies must be installed using `--ignore-requires-python`.

   ```bash
   python -m pip install --ignore-requires-python -e .[dev]
   ```

## Bug Fixes

 - Fix an issue when `include_paths` is not specified in the `pyproject.toml`.

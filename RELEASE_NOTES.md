# Betterproto Setuptools plugin Release Notes

## New Features

 - *Partial support* of Python 3.10:

   The python package can be used as is. But for testing purposes,
   dependencies must be installed using `--ignore-requires-python`.

   ```bash
   python -m pip install --ignore-requires-python -e .[dev]
   ```

## Bug Fixes

 - Fix an issue when `include_paths` is not specified in the `pyproject.toml`.

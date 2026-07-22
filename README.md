# Pre-Ingest Testing

A small pytest-based framework for running a named test against a specified file.

## Install

```bash
pip install -e .
```

or:

```bash
uv sync
```

## Run with pytest

```bash
pytest --test-name file_exists --filename /path/to/file
```

Examples:

```bash
pytest --test-name file_not_empty --filename data/example.txt
pytest --test-name valid_json --filename data/example.json
```

## Run through the CLI

```bash
pre-ingest-test file_exists /path/to/file
pre-ingest-test valid_json data/example.json
```

Pass additional pytest arguments after `--`:

```bash
pre-ingest-test valid_json data/example.json -- -v -s
```

## List available tests

```bash
pre-ingest-test --list-tests
```

## Add a new named test

Add a function to `src/pre_ingest_testing/checks.py` and register it with
the `@register_test("name")` decorator.

```python
@register_test("has_expected_suffix")
def has_expected_suffix(path: Path) -> None:
    assert path.suffix == ".nc", f"Expected a NetCDF file, got {path.suffix}"
```

Then run:

```bash
pytest --test-name has_expected_suffix --filename example.nc
```

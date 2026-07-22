# Pre-Ingest Testing

A small pytest-based framework for running a named test against a specified file.

## Install

```bash
uv sync
```

## Run with pytest

```bash
uv run pytest --test-name l2ss_spatial --filename /path/to/file
```

Examples:

```bash
uv run pytest --test-name l2ss --filename data/path/to/file
uv run pytest --test-name l2ss_temporal --filename data/path/to/file
```
## Adding a named test

Create a new test file under the `tests/` directory. Test files must be named
`test_*.py`, and test functions must be named `test_*` so that pytest can
discover them automatically.

Register the test with the `@pytest.mark.test_name()` decorator. One or more
names may be provided.

```python
import pytest
from pathlib import Path

@pytest.mark.test_name("l2ss", "l2ss_spatial")
def test_l2ss_spatial(
    input_file: Path,
    tmp_path: Path,
) -> None:
    ...
```

The names passed to `@pytest.mark.test_name()` are used with the
`--test-name` command-line option. For example:

```bash
uv run pytest --test-name l2ss --filename example.nc
```

or

```bash
uv run pytest --test-name l2ss_spatial --filename example.nc
```

The Python function name (`test_l2ss_spatial` in this example) is used only for
pytest test discovery and does not need to match the value passed to
`--test-name`.

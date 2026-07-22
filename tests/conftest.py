from pathlib import Path

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("pre-ingest")
    group.addoption(
        "--filename",
        action="store",
        dest="filename",
        help="Path to the input file under test",
    )
    group.addoption(
        "--test-name",
        action="store",
        dest="test_name",
        help="Logical group of tests to run",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    selected_name = config.getoption("test_name")

    if not selected_name:
        return

    selected_items = []
    deselected_items = []

    for item in items:
        marker = item.get_closest_marker("test_name")
        marker_names = marker.args if marker is not None else ()

        if selected_name in marker_names:
            selected_items.append(item)
        else:
            deselected_items.append(item)

    if deselected_items:
        config.hook.pytest_deselected(items=deselected_items)

    items[:] = selected_items

    if not selected_items:
        raise pytest.UsageError(f"No tests found for --test-name={selected_name!r}")


def pytest_terminal_summary(terminalreporter):
    terminalreporter.write_sep(
        "=",
        "Pre-ingest testing completed successfully",
    )


@pytest.fixture(scope="session")
def input_file(pytestconfig: pytest.Config) -> Path:
    filename = pytestconfig.getoption("filename")

    if not filename:
        raise pytest.UsageError("--filename is required")

    return Path(filename).expanduser().resolve()

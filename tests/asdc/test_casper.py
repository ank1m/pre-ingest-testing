from pathlib import Path

import pytest

from pre_ingest_testing.services.casper import (
    run_casper,
    file_valid_type_for_casper,
    valid_workable_file_for_casper
)


@pytest.mark.test_name("casper")
def test_casper_reformat(
    input_file: Path,
    tmp_path: Path,
) -> None:
  
    output_file = tmp_path / f"{input_file.name}.zip"
    run_casper(
        input_file=input_file,
        output_file=output_file
    )

    assert output_file.exists(), (
        f"CASPER did not create the expected output file while reformatting: {output_file}"
    )
    assert output_file.stat().st_size > 0, (
        f"CASPER created an empty output file while reformatting: {output_file}"
    )

@pytest.mark.test_name("casper", "casper_valid_file_type")
def test_casper_valid_file_type(
    input_file: Path,
) -> None:
  
    valid_file = file_valid_type_for_casper(
        input_file=input_file,
    )

    assert valid_file, (
        f"Input file is not valid type for CASPER processing: {input_file}"
    )

@pytest.mark.test_name("casper", "casper_valid_file")
def test_casper_file_workable (
    input_file: Path,
) -> None:
  
    valid_file = valid_workable_file_for_casper(
        input_file=input_file,
    )

    assert valid_file, (
        f"Input file is not valid for CASPER processing: {input_file}"
    )

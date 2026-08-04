from pathlib import Path

import pytest

from pre_ingest_testing.helpers.spatial import (
    generate_partial_spatial_box,
)
from pre_ingest_testing.helpers.temporal import generate_near_full_temporal_range
from pre_ingest_testing.services.l2ss import (
    run_l2ss_spatial_subset,
    run_l2ss_temporal_subset,
)


@pytest.mark.test_name("l2ss", "l2ss_spatial")
def test_l2ss_can_perform_spatial_subsetting(
    input_file: Path,
    tmp_path: Path,
) -> None:

    subset_box = generate_partial_spatial_box(input_file)

    output_file = tmp_path / f"{input_file.stem}_spatial_subset{input_file.suffix}"

    output_file = run_l2ss_spatial_subset(
        input_file=input_file,
        output_file=output_file,
        bbox=subset_box,
    )

    assert output_file.exists(), (
        f"L2SS did not create the expected output file after spatial subsetting: {output_file}"
    )
    assert output_file.stat().st_size > 0, (
        f"L2SS created an empty output file after spatial subsetting: {output_file}"
    )


@pytest.mark.test_name("l2ss", "l2ss_temporal")
def test_l2ss_can_perform_temporal_subsetting(
    input_file: Path, tmp_path: Path, monkeypatch
) -> None:

    output_file = tmp_path / f"{input_file.stem}_temporal_subset{input_file.suffix}"

    subset_range = generate_near_full_temporal_range(input_file)

    output_file = run_l2ss_temporal_subset(
        input_file=input_file,
        output_file=output_file,
        temporal_range=subset_range,
    )

    assert output_file.exists(), (
        f"L2SS did not create the expected output file after temporal subsetting: {output_file}"
    )
    assert output_file.stat().st_size > 0, (
        f"L2SS created an empty output file after temporal subsetting: {output_file}"
    )

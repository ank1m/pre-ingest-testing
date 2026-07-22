from pathlib import Path

import numpy as np
from podaac.subsetter import subset

def run_l2ss_spatial_subset(
    input_file: Path,
    output_file: Path,
    bbox
):
    subset.subset(
        file_to_subset=str(input_file),
        output_file=str(output_file),
        bbox=np.array([
            [bbox[0], bbox[2]],
            [bbox[1], bbox[3]],
        ]),
    )

    return output_file


def run_l2ss_temporal_subset(
    input_file: Path,
    output_file: Path,
    temporal_range,
):
    min_time, max_time = temporal_range
    
    subset.subset(
        file_to_subset=str(input_file),
        output_file=str(output_file),
        min_time=min_time.isoformat(),
        max_time=max_time.isoformat(),
        bbox=np.array(((-180, 180), (-90, 90))),
    )

    return output_file


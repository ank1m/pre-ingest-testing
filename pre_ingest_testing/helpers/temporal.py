from datetime import datetime
from pathlib import Path

import numpy as np
import xarray as xr
from podaac.subsetter.utils import coordinate_utils


def get_temporal_range(path: str | Path) -> tuple[datetime, datetime]:
    """
    Return the temporal range (start, end) of a NetCDF file.

    Searches all groups in the DataTree for a time coordinate and returns
    the earliest and latest timestamps.
    """

    with xr.open_datatree(path, decode_times=True) as tree:
        _, _, time_vars = coordinate_utils.get_coordinate_variable_names(tree)
        print("===================================")
        print(time_vars)

        starts = []
        ends = []

        for time_var in time_vars:
            time = tree[time_var]
            starts.append(time.min(skipna=True).values)
            ends.append(time.max(skipna=True).values)

    if not starts:
        raise ValueError("No time coordinate found in dataset.")

    start = min(starts)
    end = max(ends)
    print(start, end.dtype)

    return (
        _to_datetime(start),
        _to_datetime(end),
    )


def _to_datetime(value) -> datetime:
    """Convert a NumPy datetime64 to a Python datetime."""

    if isinstance(value, np.datetime64):
        return value.astype("datetime64[us]").tolist()

    if isinstance(value, datetime):
        return value

    raise TypeError(f"Unsupported time type: {type(value)}")


def generate_near_full_temporal_range(
    path: str | Path,
    fraction: float = 0.05,
) -> tuple[datetime, datetime]:
    """
    Generate a smaller time range within the given range.

    Returns
    -------
    tuple
        (start, end) of the trimmed range.
    """
    start, end = get_temporal_range(path)

    if not (0.0 <= fraction < 0.5):
        raise ValueError("fraction must be in the range [0, 0.5)")

    duration = end - start
    trim = duration * fraction

    return (
        start + trim,
        end - trim,
    )

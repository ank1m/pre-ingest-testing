from pathlib import Path

import xarray as xr
from xarray import DataTree


def get_bounding_box(path: str | Path) -> tuple[float, float, float, float]:
    """
    Return the bounding box (west, south, east, north) of a NetCDF file.

    Searches all groups in the DataTree for latitude and longitude
    coordinate variables.
    """
    with xr.open_datatree(path) as tree:
        lat = _find_coordinate(tree, "latitude")
        lon = _find_coordinate(tree, "longitude")

        west = float(lon.min(skipna=True).item())
        east = float(lon.max(skipna=True).item())
        south = float(lat.min(skipna=True).item())
        north = float(lat.max(skipna=True).item())

    return west, south, east, north


def _find_coordinate(tree: DataTree, coordinate_type: str) -> xr.DataArray:
    """
    Find the first latitude or longitude coordinate in a DataTree.
    """

    names = {
        "latitude": {"lat", "latitude", "y"},
        "longitude": {"lon", "longitude", "x"},
    }[coordinate_type]

    for node in tree.subtree:
        ds = node.dataset

        # Search coordinates
        for name, coord in ds.coords.items():
            if name.lower() in names:
                return coord

            if coord.attrs.get("standard_name", "").lower() == coordinate_type:
                return coord

            if coordinate_type == "latitude" and coord.attrs.get("units") == "degrees_north":
                return coord

            if coordinate_type == "longitude" and coord.attrs.get("units") == "degrees_east":
                return coord

        # Search data variables
        for name, var in ds.data_vars.items():
            if name.lower() in names:
                return var

            if var.attrs.get("standard_name", "").lower() == coordinate_type:
                return var

            if coordinate_type == "latitude" and var.attrs.get("units") == "degrees_north":
                return var

            if coordinate_type == "longitude" and var.attrs.get("units") == "degrees_east":
                return var

    raise ValueError(f"Could not find {coordinate_type} coordinate")



from math import sqrt


def generate_partial_spatial_box(
    path: str | Path,
    output_size: float = 0.05,
) -> tuple[float, float, float, float]:
    """
    Generate a centered spatial subset whose area is approximately
    `output_size` of the original bounding box.

    Parameters
    ----------
    west, south, east, north
        Original bounding box.
    output_size
        Fraction of the original area

    Returns
    -------
    tuple
        (west, south, east, north) of the subset bounding box.
    """

    west, south, east, north = get_bounding_box(path)

    if not 0 < output_size <= 1:
        raise ValueError("output_size must be in the range (0, 1].")

    width = east - west
    height = north - south

    width_trim = width * output_size
    height_trim = height * output_size

    return (
        west + width_trim,
        south + height_trim,
        east - width_trim,
        north - height_trim,
    )



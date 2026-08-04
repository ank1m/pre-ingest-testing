from pathlib import Path

from casper.convert_to_csv import convert_to_csv
from casper.file_ops import (
    valid_input_file, 
    valid_workable_file
)

def run_casper(input_file: Path, output_file: Path):
    convert_to_csv(
            input_file,
            output_file,
        )

    return 

def file_valid_type_for_casper(input_file: Path):
    valid = valid_input_file(
        input_file
    )

    return valid

def valid_workable_file_for_casper(input_file: Path):

    valid = valid_workable_file(
        input_file
    )

    return valid

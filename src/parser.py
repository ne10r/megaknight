"""Read the variable-width CSV assembly language."""

import csv
from pathlib import Path

from .commands import parse_row


def read_program(path: Path) -> list[dict]:
    """Parse instructions, ignoring empty rows and full-line comments."""
    program = []
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, strict=True)
        for row in reader:
            if not row or not any(value.strip() for value in row):
                continue
            if row[0].lstrip().startswith("#"):
                continue
            try:
                program.append(parse_row(row))
            except ValueError as error:
                raise ValueError(f"Line {reader.line_num}: {error}") from error
    if not program:
        raise ValueError("The program contains no instructions")
    return program

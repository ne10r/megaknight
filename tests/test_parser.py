"""Check the PDF examples, operand widths and CSV error handling."""

from pathlib import Path

import pytest

from src.commands import COMMANDS, parse_row
from src.parser import read_program

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIELDS = [
    {"A": 15, "B": 394, "C": 12},
    {"A": 23, "B": 13, "C": 38},
    {"A": 55, "B": 33, "C": 55},
    {"A": 53, "B": 35, "C": 297, "D": 2},
]


def test_specification_fields():
    """Match all four intermediate instructions from the assignment."""
    assert read_program(ROOT / "examples/spec.csv") == EXPECTED_FIELDS


@pytest.mark.parametrize("name", COMMANDS)
def test_field_limits(name):
    """Accept maximum unsigned values and reject the next integer."""
    _, widths = COMMANDS[name]
    row = [name, *[str((1 << width) - 1) for width in widths]]
    parse_row(row)
    for index, width in enumerate(widths, 1):
        invalid = row.copy()
        invalid[index] = str(1 << width)
        with pytest.raises(ValueError, match="must be between"):
            parse_row(invalid)


@pytest.mark.parametrize("row", [
    ["UNKNOWN", "1", "2"], ["LOAD_CONST", "1"],
    ["READ_MEM", "1", "2", "3"], ["LOAD_CONST", "-1", "2"],
    ["WRITE_MEM", "word", "2"], ["MUL", "1", "2"],
])
def test_invalid_instructions(row):
    """Reject unknown names, bad numbers, negative values and arity."""
    with pytest.raises(ValueError):
        parse_row(row)


def test_csv_comments_and_hex(tmp_path):
    """Preserve CSV quoting and allow documented whitespace and hex."""
    path = tmp_path / "program.csv"
    path.write_text('# comment\n\nLOAD_CONST," 0x18A ",12\n', encoding="utf-8")
    assert read_program(path) == [EXPECTED_FIELDS[0]]


def test_error_line(tmp_path):
    """Report the physical CSV line containing the invalid command."""
    path = tmp_path / "bad.csv"
    path.write_text("# comment\nREAD_MEM,13,64\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Line 2"):
        read_program(path)


def test_empty_program(tmp_path):
    """Reject an empty or comment-only input file."""
    path = tmp_path / "empty.csv"
    path.write_text("# comment\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no instructions"):
        read_program(path)

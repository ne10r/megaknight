"""Command line assembler, stage 1: readable intermediate fields."""

import argparse
import csv
import sys
from pathlib import Path

from .parser import read_program

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def parse_args() -> argparse.Namespace:
    """Read the source, reserved binary destination and test mode."""
    parser = argparse.ArgumentParser(description="UVM assembler, variant 21")
    parser.add_argument("source", type=Path, help="Source CSV program")
    parser.add_argument("binary", type=Path, help="Output binary path")
    parser.add_argument("--test", action="store_true", help="Print fields")
    return parser.parse_args()


def run(args: argparse.Namespace) -> None:
    """Parse all rows before printing their intermediate representation."""
    program = read_program(args.source)
    print(f"Parsed instructions: {len(program)}")
    if args.test:
        for fields in program:
            values = (f"{name}={value}" for name, value in fields.items())
            print(", ".join(values))


def main() -> int:
    """Return a useful CLI error without an implementation traceback."""
    args = parse_args()
    try:
        run(args)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())

"""Command line assembler for the six-byte UVM instruction format."""

import argparse
import csv
import sys
from pathlib import Path

from .parser import read_program
from .codec import encode_program, format_bytes
from .commands import INSTRUCTION_BYTES

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def parse_args() -> argparse.Namespace:
    """Read the source, binary destination and byte-dump mode."""
    parser = argparse.ArgumentParser(description="UVM assembler, variant 21")
    parser.add_argument("source", type=Path, help="Source CSV program")
    parser.add_argument("binary", type=Path, help="Output binary path")
    parser.add_argument("--test", action="store_true", help="Print bytes")
    return parser.parse_args()


def run(args: argparse.Namespace) -> None:
    """Assemble the entire source before writing a binary output file."""
    if args.source.resolve() == args.binary.resolve():
        raise ValueError("Source and binary paths must be different")
    program = read_program(args.source)
    binary = encode_program(program)
    args.binary.parent.mkdir(parents=True, exist_ok=True)
    args.binary.write_bytes(binary)
    print(f"Assembled instructions: {len(program)}")
    if args.test:
        for offset in range(0, len(binary), INSTRUCTION_BYTES):
            print(format_bytes(binary[offset:offset + INSTRUCTION_BYTES]))


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

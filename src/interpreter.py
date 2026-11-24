"""Execute assembled UVM programs and save an inclusive JSON memory dump."""

import argparse
import json
import sys
from pathlib import Path

from .machine import Machine, check_dump_range, execute_program

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def parse_args() -> argparse.Namespace:
    """Read instruction file, dump destination and inclusive memory range."""
    parser = argparse.ArgumentParser(description="UVM interpreter, variant 21")
    parser.add_argument("binary", type=Path, help="Assembled binary program")
    parser.add_argument("dump", type=Path, help="Output memory JSON")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    return parser.parse_args()


def run(args: argparse.Namespace) -> None:
    """Execute before creating the dump so failed programs leave no output."""
    if args.binary.resolve() == args.dump.resolve():
        raise ValueError("Binary and dump paths must be different")
    machine = Machine()
    check_dump_range(args.start, args.end)
    count = execute_program(args.binary.read_bytes(), machine)
    result = machine.dump(args.start, args.end)
    args.dump.parent.mkdir(parents=True, exist_ok=True)
    args.dump.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Executed instructions: {count}")
    print(f"Memory dump: {args.dump}")


def main() -> int:
    """Report invalid binaries, runtime addresses and filesystem errors."""
    args = parse_args()
    try:
        run(args)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())

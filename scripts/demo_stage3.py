"""Demonstrate a real array copy using the three memory instructions."""

from .demo_common import run_example, save_report


def main() -> None:
    """Compare the copied destination with all four initialized values."""
    result = run_example("examples/copy.csv", 200, 203, [7, 11, 19, 23])
    save_report("stage3.json", [result])


if __name__ == "__main__":
    main()

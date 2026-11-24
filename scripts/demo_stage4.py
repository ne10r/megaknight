"""Demonstrate multiplication, zero and a result larger than 29 bits."""

from .demo_common import run_example, save_report


def main() -> None:
    """Check the destination cells written by real MUL instructions."""
    expected = [42, 0, 3221225466]
    result = run_example("examples/multiply.csv", 400, 402, expected)
    save_report("stage4.json", [result])


if __name__ == "__main__":
    main()

"""Execute three eight-element vector programs with the scalar 82."""

from .demo_common import run_example, save_report

SCALAR = 82
SOURCE_START = 100
RESULT_START = 200
VECTOR_LENGTH = 8
CASES = [
    ("examples/vector_1.csv", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("examples/vector_2.csv", [0, 5, 10, 15, 20, 25, 30, 35]),
    ("examples/vector_3.csv", [7, 11, 13, 17, 19, 23, 29, 31]),
]


def run_vector(source: str, values: list[int]) -> dict:
    """Check the new result and independently verify the original vector."""
    expected = [value * SCALAR for value in values]
    result = run_example(
        source, RESULT_START, RESULT_START + VECTOR_LENGTH - 1, expected
    )
    original = run_example(
        source, SOURCE_START, SOURCE_START + VECTOR_LENGTH - 1, values
    )
    result["input"] = values
    result["scalar"] = SCALAR
    result["source_after_execution"] = original["actual"]
    return result


def main() -> None:
    """Build and execute three CSV sources rather than presetting VM data."""
    results = [run_vector(source, values) for source, values in CASES]
    save_report("stage5.json", results)


if __name__ == "__main__":
    main()

"""Check byte-for-byte compatibility with the assignment and decoding."""

import pytest

from src.codec import decode_instruction, encode_instruction

CASES = [
    ({"A": 15, "B": 394, "C": 12}, "8f6200006000"),
    ({"A": 23, "B": 13, "C": 38}, "570300002600"),
    ({"A": 55, "B": 33, "C": 55}, "777803000000"),
    ({"A": 53, "B": 35, "C": 297, "D": 2}, "f59812008000"),
]


@pytest.mark.parametrize("fields,expected", CASES)
def test_specification_bytes(fields, expected):
    """Match each exact six-byte example in the PDF in both directions."""
    binary = bytes.fromhex(expected)
    assert encode_instruction(fields) == binary
    assert decode_instruction(binary) == fields


@pytest.mark.parametrize("fields", [
    {"A": 0}, {"A": 15, "B": -1, "C": 0},
    {"A": 15, "B": 1 << 29, "C": 0},
    {"A": 23, "B": 0, "C": 64},
    {"A": 55, "B": 0, "C": 0, "D": 0},
    {"A": 53, "B": 0, "C": 0},
    {"A": True, "B": 0, "C": 0},
    {"A": 15, "B": "1", "C": 0},
])
def test_invalid_fields(fields):
    """Reject unsupported, incomplete, oversized and noninteger fields."""
    with pytest.raises(ValueError):
        encode_instruction(fields)


@pytest.mark.parametrize("binary", [
    b"", b"\x0f", bytes.fromhex("000000000000"),
    bytes.fromhex("8f6200006080"),
])
def test_invalid_binary(binary):
    """Reject truncated commands, unknown opcodes and reserved high bits."""
    with pytest.raises(ValueError):
        decode_instruction(binary)

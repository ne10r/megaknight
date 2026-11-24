"""Encode and decode the six-byte little-endian UVM instructions."""

from .commands import BYTE_ORDER, FIELD_NAMES, INSTRUCTION_BYTES
from .commands import OPCODE_BITS, check_value, get_widths


def encode_instruction(fields: dict) -> bytes:
    """Pack named fields, leaving all unused high bits equal to zero."""
    widths = get_widths(fields.get("A"))
    names = FIELD_NAMES[:len(widths)]
    if set(fields) != {"A", *names}:
        raise ValueError("Instruction fields do not match the opcode")
    result = fields["A"]
    offset = OPCODE_BITS
    for name, width in zip(names, widths):
        check_value(fields[name], width, name)
        result |= fields[name] << offset
        offset += width
    return result.to_bytes(INSTRUCTION_BYTES, BYTE_ORDER)


def decode_instruction(data: bytes) -> dict:
    """Decode one instruction and reject invalid padding or opcodes."""
    if len(data) != INSTRUCTION_BYTES:
        raise ValueError("An instruction must contain exactly six bytes")
    value = int.from_bytes(data, BYTE_ORDER)
    opcode = value & ((1 << OPCODE_BITS) - 1)
    widths = get_widths(opcode)
    fields = {"A": opcode}
    offset = OPCODE_BITS
    for name, width in zip(FIELD_NAMES, widths):
        fields[name] = (value >> offset) & ((1 << width) - 1)
        offset += width
    if value >> offset:
        raise ValueError("Unused instruction bits must be zero")
    return fields


def encode_program(program: list[dict]) -> bytes:
    """Validate every instruction before producing the output bytes."""
    return b"".join(encode_instruction(fields) for fields in program)


def format_bytes(data: bytes) -> str:
    """Use the comma-separated hexadecimal notation shown in the PDF."""
    return ", ".join(f"0x{value:02X}" for value in data)

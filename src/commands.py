"""Instruction fields from variant 21, pages 88 and 89."""

OPCODE_BITS = 6
INSTRUCTION_BYTES = 6
BYTE_ORDER = "little"
MIN_VALUE = 0
COMMAND_COLUMN_COUNT = 1
FIELD_NAMES = ("B", "C", "D")
LOAD_CONST = 15
READ_MEM = 23
WRITE_MEM = 55
MUL = 53
REGISTER_COUNT = 64
ADDRESS_BITS = 26
COMMANDS = {
    "LOAD_CONST": (LOAD_CONST, (29, 6)),
    "READ_MEM": (READ_MEM, (26, 6)),
    "WRITE_MEM": (WRITE_MEM, (6, 6)),
    "MUL": (MUL, (6, 26, 6)),
}
OPCODES = {opcode: widths for opcode, widths in COMMANDS.values()}


def check_value(value: int, width: int, field: str) -> None:
    """Reject unsigned values that do not fit the instruction field."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    limit = 1 << width
    if value < MIN_VALUE or value >= limit:
        raise ValueError(f"{field} must be between 0 and {limit - 1}")


def get_widths(opcode: int) -> tuple:
    """Find an instruction layout by its six-bit operation code."""
    check_value(opcode, OPCODE_BITS, "A")
    if opcode not in OPCODES:
        raise ValueError(f"Unknown opcode: {opcode}")
    return OPCODES[opcode]


def parse_number(text: str) -> int:
    """Accept decimal integers and positive hexadecimal 0x literals."""
    value = text.strip()
    base = 16 if value.lower().startswith("0x") else 10
    try:
        return int(value, base)
    except ValueError as error:
        raise ValueError(f"Invalid integer: {text!r}") from error


def parse_row(row: list[str]) -> dict:
    """Convert one CSV row to the A, B, C and optional D fields."""
    name = row[0].strip()
    if name not in COMMANDS:
        raise ValueError(f"Unknown command: {name!r}")
    opcode, widths = COMMANDS[name]
    if len(row) != len(widths) + COMMAND_COLUMN_COUNT:
        raise ValueError(f"{name} expects {len(widths)} operands")
    fields = {"A": opcode}
    for field, width, text in zip(FIELD_NAMES, widths, row[1:]):
        value = parse_number(text)
        check_value(value, width, field)
        fields[field] = value
    return fields

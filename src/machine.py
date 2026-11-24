"""Registers and sparse data memory, separate from instruction bytes."""

from .codec import decode_instruction
from .commands import ADDRESS_BITS, INSTRUCTION_BYTES, REGISTER_COUNT
from .commands import LOAD_CONST, READ_MEM, WRITE_MEM, check_value


def check_dump_range(start: int, end: int) -> None:
    """Validate a range without allocating its output dictionary."""
    check_value(start, ADDRESS_BITS, "Dump start")
    check_value(end, ADDRESS_BITS, "Dump end")
    if start > end:
        raise ValueError("Dump start must not exceed dump end")


class Machine:
    """Keep 64 integer registers and zero-initialized 26-bit data memory."""

    def __init__(self) -> None:
        """Start each execution with zero registers and empty sparse memory."""
        self.registers = [0] * REGISTER_COUNT
        self.memory = {}

    def read(self, address: int) -> int:
        """Return zero for a valid cell that has not been written yet."""
        check_value(address, ADDRESS_BITS, "Memory address")
        return self.memory.get(address, 0)

    def write(self, address: int, value: int) -> None:
        """Write an integer value after checking the indirect address."""
        check_value(address, ADDRESS_BITS, "Memory address")
        self.memory[address] = value

    def execute(self, fields: dict) -> None:
        """Execute the three memory instructions available in stage 3."""
        opcode = fields["A"]
        if opcode == LOAD_CONST:
            self.registers[fields["C"]] = fields["B"]
        elif opcode == READ_MEM:
            self.registers[fields["C"]] = self.read(fields["B"])
        elif opcode == WRITE_MEM:
            address = self.registers[fields["C"]]
            self.write(address, self.registers[fields["B"]])
        else:
            raise ValueError("MUL execution is introduced in stage 4")

    def dump(self, start: int, end: int) -> dict:
        """Return an inclusive address range, including zero-valued cells."""
        check_dump_range(start, end)
        memory = {str(address): self.read(address)
                  for address in range(start, end + 1)}
        return {"start": start, "end": end, "memory": memory}


def execute_program(binary: bytes, machine: Machine) -> int:
    """Fetch, decode and execute consecutive instructions until EOF."""
    if not binary or len(binary) % INSTRUCTION_BYTES:
        raise ValueError("Binary must contain complete six-byte instructions")
    for offset in range(0, len(binary), INSTRUCTION_BYTES):
        number = offset // INSTRUCTION_BYTES + 1
        try:
            data = binary[offset:offset + INSTRUCTION_BYTES]
            fields = decode_instruction(data)
            machine.execute(fields)
        except ValueError as error:
            raise ValueError(f"Instruction {number}: {error}") from error
    return len(binary) // INSTRUCTION_BYTES

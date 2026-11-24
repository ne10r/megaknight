"""Exercise the binary assembler contract in a separate process."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXIT_SUCCESS = 0
EXIT_ERROR = 1
ARGUMENT_ERROR_EXIT_CODE = 2


def run_cli(*arguments):
    """Use the same Python interpreter as the test runner."""
    return subprocess.run(
        [sys.executable, "-m", "src.assembler", *arguments], cwd=ROOT,
        capture_output=True, text=True, timeout=10,
    )


def test_test_mode(tmp_path):
    """Save machine code and print all byte rows from the specification."""
    destination = tmp_path / "program.bin"
    result = run_cli("examples/spec.csv", str(destination), "--test")
    assert result.returncode == EXIT_SUCCESS
    assert "0x8F, 0x62, 0x00, 0x00, 0x60, 0x00" in result.stdout
    assert "0xF5, 0x98, 0x12, 0x00, 0x80, 0x00" in result.stdout
    assert result.stderr == ""
    assert destination.read_bytes() == bytes.fromhex(
        "8f6200006000 570300002600 777803000000 f59812008000"
    )


def test_invalid_input_preserves_output(tmp_path):
    """Never replace an existing binary when a later CSV row is invalid."""
    source = tmp_path / "invalid.csv"
    source.write_text("LOAD_CONST,1,0\nUNKNOWN,1,2\n", encoding="utf-8")
    output = tmp_path / "program.bin"
    output.write_bytes(b"original")
    result = run_cli(str(source), str(output))
    assert result.returncode == EXIT_ERROR
    assert output.read_bytes() == b"original"


def test_same_input_and_output(tmp_path):
    """Prevent replacing the assembly source with binary bytes."""
    source = tmp_path / "source.csv"
    content = "LOAD_CONST,1,0\n"
    source.write_text(content, encoding="utf-8")
    result = run_cli(str(source), str(source))
    assert result.returncode == EXIT_ERROR
    assert source.read_text(encoding="utf-8") == content


def test_missing_source(tmp_path):
    """Report an absent input file without a traceback or output file."""
    destination = tmp_path / "program.bin"
    result = run_cli(str(tmp_path / "missing.csv"), str(destination))
    assert result.returncode == EXIT_ERROR
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr
    assert not destination.exists()


def test_missing_arguments():
    """Use argparse's named error code for an incomplete command."""
    assert run_cli().returncode == ARGUMENT_ERROR_EXIT_CODE

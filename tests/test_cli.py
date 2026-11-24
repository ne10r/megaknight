"""Exercise the stage-1 command line contract in a separate process."""

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
    """Print the PDF fields without prematurely creating machine code."""
    destination = tmp_path / "program.bin"
    result = run_cli("examples/spec.csv", str(destination), "--test")
    assert result.returncode == EXIT_SUCCESS
    assert "A=15, B=394, C=12" in result.stdout
    assert "A=53, B=35, C=297, D=2" in result.stdout
    assert result.stderr == ""
    assert not destination.exists()


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

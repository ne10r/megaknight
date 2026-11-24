"""Run real assembler/interpreter processes and retain JSON evidence."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_command(arguments: list[str]) -> str:
    """Require a successful real CLI process and return its stdout."""
    result = subprocess.run(
        [sys.executable, "-m", *arguments], cwd=ROOT,
        capture_output=True, text=True, timeout=20, check=True,
    )
    return result.stdout.strip()


def run_example(
    source: str, start: int, end: int, expected: list[int]
) -> dict:
    """Assemble a CSV file and verify a dump produced by the interpreter."""
    with tempfile.TemporaryDirectory() as temporary:
        binary = Path(temporary) / "program.bin"
        output = Path(temporary) / "memory.json"
        assembly = run_command([
            "src.assembler", source, str(binary),
        ])
        execution = run_command([
            "src.interpreter", str(binary), str(output),
            "--start", str(start), "--end", str(end),
        ])
        dump = json.loads(output.read_text(encoding="utf-8"))
    actual = [dump["memory"][str(address)]
              for address in range(start, end + 1)]
    if actual != expected:
        raise AssertionError(f"{source}: {actual} != {expected}")
    return {
        "source": source, "assembler": assembly,
        "interpreter": execution.splitlines()[0],
        "expected": expected, "actual": actual, "dump": dump,
        "matched": True,
    }


def save_report(name: str, results: list[dict]) -> None:
    """Save reproducible values without binaries or temporary file paths."""
    output = ROOT / "reports" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for item in results:
        print(f"{item['source']}: {item['actual']}")
    print(f"Saved report: reports/{name}")

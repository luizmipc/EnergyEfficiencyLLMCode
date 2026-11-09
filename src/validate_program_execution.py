"""Compiles (if needed) and runs every program in config/constants.py,
printing finished/failed with timing for each, across every source in
SOURCES (HUMAN, CLAUDE, CODEX).

Usage:
    python3 src/validate_program_execution.py
"""

import os
import subprocess
import sys
import time

from config.constants import PROGRAMS, SOURCE_DIRS, SOURCES, TIMEOUT_SECONDS
from utils import compile_program, run_cmd


def run_program(path, language):
    """Compiles (if needed) and runs path, returning (success, elapsed_seconds).
    elapsed_seconds times only the run itself, not compilation."""
    if not compile_program(path, language):
        return False, 0.0

    start = time.time()
    try:
        ok = subprocess.run(run_cmd(path, language), cwd=os.path.dirname(path), capture_output=True, timeout=TIMEOUT_SECONDS).returncode == 0
    except subprocess.TimeoutExpired:
        ok = False
    return ok, time.time() - start


def main():
    passed = total = 0
    for source in SOURCES:
        for program in PROGRAMS:
            for language, filename in program["files"].items():
                path = os.path.join(SOURCE_DIRS[source], program["folder"], filename)
                ok, elapsed = run_program(path, language)
                total, passed = total + 1, passed + ok
                print(f"{program['name']} ({language}, {source}): {'finished' if ok else 'failed'} ({elapsed:.2f}s)")

    print(f"\n{passed}/{total} programs finished successfully.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

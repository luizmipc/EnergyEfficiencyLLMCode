"""Runs every program in config/constants.py CODECARBON_RUNS times each
(with CODECARBON_INTERVAL_SECONDS between runs), measuring energy/CO2 with
codecarbon (https://docs.codecarbon.io/) and appending each run to:

    Analysis/data/code/claude/<Problem>/<Language>/emissions.csv
    Analysis/data/code/codex/<Problem>/<Language>/emissions.csv
    Analysis/data/code/human/<Problem>/<Language>/emissions.csv

Usage:
    .venv/bin/python3 src/codecarbon_metrics_from_code.py
"""

import os
import shutil
import subprocess
import sys
import time
from datetime import timedelta

from codecarbon import EmissionsTracker, OutputMethod

from config.constants import (
    CODECARBON_DATA_DIR,
    CODECARBON_INTERVAL_SECONDS,
    CODECARBON_RUNS,
    PROGRAMS,
    SOURCE_DIRS,
    SOURCES,
    TIMEOUT_SECONDS,
    get_codecarbon_output_dir,
)
from utils import compile_program, run_cmd


def main():
    shutil.rmtree(CODECARBON_DATA_DIR, ignore_errors=True)  # start every run from a clean slate

    for source in SOURCES:
        for program in PROGRAMS:
            for language, filename in program["files"].items():
                path = os.path.join(SOURCE_DIRS[source], program["folder"], filename)
                label = f"{program['name']} ({language}, {source})"
                if not compile_program(path, language):
                    print(f"{label}: skipped (compile failed)")
                    continue

                output_dir = get_codecarbon_output_dir(program, language, source=source)
                for i in range(1, CODECARBON_RUNS + 1):
                    tracker = EmissionsTracker(
                        output_dir=output_dir,
                        output_file="emissions.csv",
                        output_methods=[OutputMethod.CSV],
                        log_level="error",
                        allow_multiple_runs=True,
                    )
                    tracker.start()
                    try:
                        ok = subprocess.run(
                            run_cmd(path, language),
                            cwd=os.path.dirname(path),
                            capture_output=True,
                            timeout=TIMEOUT_SECONDS,
                        ).returncode == 0
                    except subprocess.TimeoutExpired:
                        ok = False
                    emissions = tracker.stop()

                    emissions_str = f"{emissions:.3e} kg CO2" if emissions is not None else "n/a"
                    print(f"{label} run {i}/{CODECARBON_RUNS}: {'finished' if ok else 'failed'} ({emissions_str})")

                    if i < CODECARBON_RUNS:
                        time.sleep(CODECARBON_INTERVAL_SECONDS)

    return 0


if __name__ == "__main__":
    start = time.monotonic()
    exit_code = main()
    elapsed = time.monotonic() - start
    print(f"Total time: {timedelta(seconds=round(elapsed))}")
    sys.exit(exit_code)

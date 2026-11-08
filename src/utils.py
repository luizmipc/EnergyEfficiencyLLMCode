"""Shared helpers for compiling and running a program, used by both
validate_program_execution.py and codecarbon_metrics_from_code.py."""

import os
import subprocess
import sys

from config.constants import CPP, JAVA


def compile_program(path, language):
    """Compiles cpp/java once; returns True on success (python: nothing to do)."""
    if language == CPP:
        binary = os.path.splitext(path)[0] + ".out"
        return subprocess.run(["g++", "-O2", "-std=c++17", path, "-o", binary], capture_output=True).returncode == 0
    if language == JAVA:
        return subprocess.run(["javac", os.path.basename(path)], cwd=os.path.dirname(path), capture_output=True).returncode == 0
    return True


def run_cmd(path, language):
    """Returns the argv to execute path (already compiled, if applicable)."""
    if language == CPP:
        return [os.path.splitext(path)[0] + ".out"]
    if language == JAVA:
        return ["java", "-ea", os.path.splitext(os.path.basename(path))[0]]
    return [sys.executable, path]

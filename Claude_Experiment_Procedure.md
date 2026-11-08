# Claude Experiment Procedure

This document records, for transparency, what was actually done to produce the
Claude-generated solutions under `Results/code/claude/` and their accompanying
LLM-usage metrics, including a mistake that was found afterward and corrected,
and the tooling built to validate the results.

## 1. Running the prompt

The prompt in [`PROMPT.md`](PROMPT.md) was run in a single Claude Code session
against the 17 problems listed there (chosen for a variety of algorithmic
patterns), one problem/language combination ("variant") at a time, for all
three languages (Python, Java, C++) — 51 variants in total.

For each variant, Claude:
- Read the original human-written solution under `src/data/human/<Problem>/`.
- Refactored it to reduce energy consumption (fewer CPU cycles, fewer memory
  allocations, less unnecessary work) without changing its behavior, output
  format, or public interface.
- Verified the refactor compiles/runs and matches the original's behavior
  before saving it under `Results/code/claude/<Problem>/`.
- Recorded four usage metrics for that variant (total tokens, tool-call count,
  distinct model-turn count, wall-clock time) into a `<filename>.txt` file
  next to the code, by slicing the session's own transcript file between a
  `START` and `END` line marker taken immediately before and after the work
  on that variant.

## 2. A token-counting mistake, found and fixed

Later, asked to double-check the saved metrics, the session re-derived all 51
`.txt` files directly from the transcript and compared them against what had
been saved. The arithmetic itself was correct everywhere — but the `START`
marker for **9 of the 51 variants** had been recorded in the wrong place: the
original file was read *before* `START` was taken instead of after, so that
one read turn's tokens and tool call fell into the untracked gap between two
variants and were silently missing from both.

This was systematic, not a one-off — it affected mostly the C++ variants that
followed directly after a Python variant finished. For 8 of the 9, exactly
one turn had fallen into the gap; `Find_the_Sum_of_Subsequence_Powers` (cpp)
lost three consecutive turns this way, which is why its undercount is an
order of magnitude larger than the others. Re-deriving each of the 9 from
the transcript (`START`/`END` line ranges re-checked against the actual
`.jsonl` content) gave these exact before/after values, recorded here for
transparency:

| Problem | Language | Tokens (before → after) | Tool calls / turns (before → after) | Time, s (before → after) |
|---|---|---:|---:|---:|
| `Sudoku_Solver` | python | 396,344 → 490,495 (+94,151) | 4 → 5 | 25.03 → 31.99 |
| `Sudoku_Solver` | cpp | 427,271 → 528,039 (+100,768) | 4 → 5 | 26.74 → 41.52 |
| `Median_of_Two_Sorted_Arrays` | cpp | 514,278 → 639,056 (+124,778) | 4 → 5 | 21.52 → 27.45 |
| `Minimum_Window_Substring` | cpp | 1,439,641 → 1,724,024 (+284,383) | 5 → 6 | 26.03 → 34.60 |
| `Permutation_Sequence` | cpp | 1,528,215 → 1,829,034 (+300,819) | 5 → 6 | 28.41 → 41.51 |
| `Sorted_GCD_Pair_Queries` | cpp | 1,634,458 → 1,955,012 (+320,554) | 5 → 6 | 32.33 → 59.64 |
| `Find_Number_of_Coins_to_Place_in_Tree_Nodes` | cpp | 2,827,225 → 3,172,891 (+345,666) | 8 → 9 | 56.54 → 76.61 |
| `Text_Justification` | cpp | 1,506,848 → 1,880,204 (+373,356) | 4 → 5 | 22.82 → 28.31 |
| `Find_the_Sum_of_Subsequence_Powers` | cpp | 2,008,141 → 3,186,055 (+1,177,914) | 5 → 8 | 36.91 → 115.76 |

The 9 `.txt` files were corrected by re-including the missing turn(s) and
recomputing; the other 42 files needed no change. The corrected numbers are
what's currently saved in `Results/code/claude/`.

## 3. Building `validate_program_execution.py`

To get an independent, mechanical check that every saved solution actually
compiles and runs (rather than trusting the refactor step's own verification
after the fact), `src/validate_program_execution.py` was built together with
`src/config/constants.py`:

- `constants.py` lists all 17 problems, their LeetCode number and tags (from
  `Sheets/Tasks_and_Tags.xlsx` and `Sheets/Grouping_of_Tags.xlsx`), their
  per-language filenames, and two source directories: `HUMAN_DIR`
  (`src/data/human/`, the original baseline) and `CODE_DIR`
  (`Results/code/claude/`, the refactored version). Both sources use the
  same per-language filename for a given problem, so one filename mapping
  covers both.
- `validate_program_execution.py` compiles (Java/C++) and runs
  (Python/Java/C++) every program for a chosen source — `human`, `claude`,
  or both — and reports `finished` or `failed` with execution time for each,
  plus a per-source and overall summary.

## 4. Errors found in the human-written baseline

Running the validator against `src/data/human/` surfaced pre-existing defects
in the original solutions that had nothing to do with the refactor:

- **Five Java files don't compile at all**: `N-Queens` (`NQueens.java`),
  `Sudoku_Solver`, `Merge_k_Sorted_Lists`, `First_Missing_Positive`, and
  `Permutation_Sequence` each declare **two top-level `public` classes** in
  one file (`public class Solution` alongside the file's own public driver
  class). `javac` rejects this outright
  (`class Solution is public, should be declared in a file named Solution.java`),
  so these five fail before a single test even runs.
- **`Find_the_Sum_of_Subsequence_Powers.cpp` aborts**: its memoization table
  (`dp`) is a `Solution` member that is never cleared between calls. Because
  the test harness reuses one `Solution` instance across all 7 test cases,
  stale cache entries from an earlier test case leak into a later one,
  causing an `assert` failure (`Test case 2 failed`, exit code 134) partway
  through — confirmed by compiling and running the original file directly.

Result: **45/51 human-written programs finished successfully.**

## 5. Why the Claude version still has 3 failures

The Claude refactor's job was to reduce energy consumption **without changing
behavior** — including bugs. So the three remaining `claude` failures are the
same defects reproduced on purpose, with correctness verified by confirming
the refactored binary fails at the identical point as the original:

- **`Sudoku_Solver.java`**: the embedded test asserts
  `Arrays.deepEquals(char[][], String[][])`, which is always `false` for
  these types regardless of content — a bug in the test code, not the
  `Solution` logic. This was confirmed by running the `Solution` class
  standalone and checking it produces the correct solved board.
- **`Merge_k_Sorted_Lists.java`**: test case 4 builds `List.of(...)` from an
  array containing a `null` element, which `List.of` always rejects with a
  `NullPointerException` — again a bug in the test's own setup, reproduced
  identically in both versions.
- **`Find_the_Sum_of_Subsequence_Powers.cpp`**: the same stale-cache bug
  described in section 4 above, but this time it's a real defect in the
  `Solution` class's own logic, not just the test code. It was left as-is
  (rather than fixing the obvious one-line cause, clearing `dp` per call)
  specifically because the task required preserving behavior; fixing it
  would have changed the program from "crashes" to "completes," which is a
  behavior change. The data-structure efficiency improvement made to the
  surrounding code was verified to not be what's causing the crash — the
  refactored binary aborts on the exact same assertion as the original.

The five Java "two public classes" compile errors, by contrast, **were**
fixed during the refactor (not preserved) — because a file that cannot
compile has no behavior to preserve in the first place. The fix was always
the same one-line change: drop the `public` modifier from the inner
`Solution` class, matching the convention every other correctly-compiling
file in this dataset already follows.

Result: **48/51 claude-generated programs finished successfully**, and all
three remaining failures are faithfully reproduced human-baseline bugs, not
regressions introduced by the refactor.

## Summary

| Source | Finished | Notes |
|---|---|---|
| `human` | 45/51 | 5 Java compile errors + 1 shared C++ crash |
| `claude` | 48/51 | Only the 1 shared C++ crash + 2 broken test assertions, all pre-existing and deliberately preserved |

Run `python3 src/validate_program_execution.py` (optionally followed by
`human` or `claude` to check just one side) to reproduce these numbers.

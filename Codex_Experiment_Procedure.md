# Codex Experiment Procedure

The Codex procedure in `PROMPT.md` was executed sequentially in one session
on 2026-11-08. All 17 selected human solutions were refactored independently
in Python, C++, and Java: 51 source files under `Results/code/codex/`.
The historical Claude procedure was not rerun; its artifacts are unchanged.

Each variant has its original filename, a `.txt` snapshot-metrics sidecar,
and a `.verification.json` record containing source hashes, rollout line
boundaries, baseline token snapshot, and the initial verification results.
`Results/code/codex/validation.json` contains the final independent checks.

## Verification and exceptions

Run `python3 -B src/verify_codex_replication.py` to reproduce the checks.
The script compiles C++ with `g++ -O2 -std=c++17` and Java with `javac`,
and enables Java assertions with `java -ea`. Builds are isolated in temporary
directories. Python embedded suites run through AST loading without invoking
the benchmark main loop. C++/Java repeated-test loops are reduced to one
iteration only in temporary build copies. All saved harness logic and
repetition counts remain the same as the baseline. These are correctness
checks, not full-duration benchmark runs or energy measurements.

The final check passes 48 of the 51 Codex embedded suites. Three remain
failed and must not be treated as successful executions:

- `Sudoku_Solver.java`: its test compares `char[][]` with `String[][]` and
  fails the first assertion.
- `Merge_k_Sorted_Lists.java`: its test passes a null element to `List.of`
  and raises `NullPointerException`.
- `Find_the_Sum_of_Subsequence_Powers.cpp`: the original persistent memo
  cache is deliberately retained; both versions abort at test case 2.

Five human Java files declare two top-level public classes. Their Codex
versions make `Solution` package-private, as the existing Claude experiment
did. This is an explicit exception to literal preservation of compile-error
behavior. The final verifier also runs temporary human copies with only
that declaration repaired, so the Sudoku and merge-k runtime failures can
be compared directly. The original human files are never edited.

The available interpreter is Python 3.8.10. The subsequence Python source
uses `functools.cache`, which needs Python 3.9 or newer. Both original and
Codex sources are tested using the equivalent `lru_cache(maxsize=None)`
shim in the verification process only; their saved imports are unchanged.

Additional deterministic differential checks use seed 1729 and compare
Python outputs, exceptions, and input mutations across 2,218 cases spanning
all 17 problems. Linked-list checks also compare original-node provenance
and detect cycles. All pass. These checks cover bounded inputs within the
problem domains; they are not a proof of equivalence for every possible input.

## Usage-metric limitations

The rollout file was selected by modification time before each variant.
`START` and the cumulative token baseline were captured before reading the
source, and `END` after the initial variant verification, before computing
metrics. The sidecar's four values use the document's literal formulas:

- `total_tokens`: last non-null `token_count` cumulative total in the slice,
  minus the pre-slice baseline.
- `tool_call_count`: rollout `response_item` events whose payload type is
  `function_call` or `custom_tool_call`.
- `turn_context_count`: distinct `turn_id` values in sliced `turn_context`
  events, with timestamp fallback when no identifier exists.
- `time_delta_seconds`: last minus first sliced timestamp, parsed as UTC.

The required initial audit found that the prompt's event assumptions do
not hold for this runtime. `turn_context` represents a user turn, not each
model response; there are no such events inside these variant slices, so
every literal turn count is zero. Token snapshots arrive after the enclosing
orchestration call completes. Because a call finalized a variant and then
read the next source, snapshot deltas can attribute a preceding response's
usage to the following variant. Nested editing, compilation, and execution
operations are not individual rollout tool-call events either.

Therefore the sidecars are labeled `snapshot_only_not_reliable_per_variant_effort`
in their verification records. They must not be used as independently
attributed per-variant token costs, model-response counts, or cross-model
effort comparisons. No substitute counts were invented. The recorded line
boundaries allow the literal calculations to be audited. Later aggregate
verification and documentation work is outside those initial slices.

## Changes by problem and language

Each item identifies the energy-relevant work targeted by that variant.
No energy improvement is claimed without measurements. Algorithms and public
method names are retained; the C++ regex table has a strictly smaller space
complexity, O(pattern length) instead of O(text length × pattern length).

### N-Queens

- Python: bitmask conflict tests, one placement stack, and cached row strings
  replace linear scans and repeated list/string construction.
- C++: column and diagonal occupancy arrays replace repeated board scans;
  the board is updated and restored in place.
- Java: constant-time occupancy checks replace nested board scans, and an
  array-backed result list replaces linked-list node allocations.

### Sudoku Solver

- Python: cached row/column/box sets and a row-major empty-cell list avoid
  repeated validity scans, coordinate conversions, and digit conversions.
- C++: bitmask constraints replace nine-cell scans for each candidate digit.
- Java: cached row and box coordinates eliminate duplicate array reads and
  redundant comparisons with `'.'` during validity checks.

### Median of Two Sorted Arrays

- Python: infinity sentinels are created once per call rather than per
  search step; direct comparisons replace repeated min/max calls.
- C++: an empty shorter array bypasses partition search.
- Java: an empty shorter array bypasses partition search.

### Trapping Rain Water

- Python: caches length and the selected height instead of rereading them.
- C++: loads each endpoint height once per loop iteration.
- Java: loads each endpoint height once per loop iteration.

### Largest Rectangle in Histogram

- Python: enumeration reuses the current height; explicit area comparison
  avoids repeated `max` function calls.
- C++: reserves monotonic-stack storage and reuses each computed area.
- Java: computes areas during the right-boundary pass, removing a third pass.

### Merge k Sorted Lists

- Python: recursive index ranges replace allocated list slices.
- C++: combines two vector erases and replaces recursive two-list merging
  with an iterative pointer walk, retaining the same tie selection.
- Java: reuses a static comparator instead of allocating one on every call.

### Reverse Nodes in k-Group

- Python: returns immediately for `k == 1`, avoiding allocation and traversal.
- C++: returns immediately for `k == 1`; a stack sentinel replaces a leaked
  heap-allocated sentinel.
- Java: returns immediately for `k == 1`, avoiding recursive calls and rewiring.

### Regular Expression Matching

- Python: returns already-known booleans without rereading the memo dictionary.
- C++: two rolling DP rows replace the full variable-length stack table.
- Java: reuses the retrieved memo entry and current pattern character.

### First Missing Positive

- Python: enumerates the sanitization pass and reuses the cached array length.
- C++: caches the current value and destination during in-place swaps.
- Java: caches loaded values and marks entries with unary negation.

### Find Edges in Shortest Paths

- Python: computes each candidate distance once and caches the final distance.
- C++: counts degrees to reserve adjacency-list storage before insertion.
- Java: an array deque replaces linked queue nodes; `Set.add` combines the
  membership test and insertion into one hash lookup.

### Length of the Longest Increasing Path

This is the coordinate/LIS problem (LeetCode 3288), despite the prompt's
graph-DFS label.

- Python: caches the anchor coordinates used throughout the sorted traversal.
- C++: searches populated tails only, avoiding full sentinel initialization.
- Java: searches populated tails only and removes sentinel-array filling and
  the final binary search.

### Minimum Window Substring

- Python: reuses retrieved character counts during expansion and contraction.
- C++: a stack ASCII table replaces a heap-allocated vector.
- Java: indexes the target string directly, avoiding its temporary char array.

### Permutation Sequence

- Python: `list(range(...))` constructs the digits; indexed `pop` replaces
  value lookup followed by a second linear search in `remove`.
- C++: reserves digit-vector and output-string capacity.
- Java: reserves list/builder capacity and appends removed digits directly,
  avoiding intermediate digit strings and a redundant list lookup.

### Sorted GCD Pair Queries

- Python: dense counts replace hash-table access; prefix sums reuse the
  finished GCD-count buffer.
- C++: prefix sums reuse the count buffer; query-result capacity is reserved.
- Java: prefix sums reuse the finished count array.

### Find Number of Coins to Place in Tree Nodes

- Python: sorts and truncates newly concatenated summaries in place instead
  of allocating additional sorted copies and slices.
- C++: skips insertion, sorting, and truncation for empty child summaries.
- Java: avoids `addAll` and its temporary-array work for empty child summaries.

### Text Justification

- Python: caches the gap count and appends words without singleton lists.
- C++: reserves line capacity, appends repeated spaces directly, and moves
  completed strings into the result vector.
- Java: fills one space buffer directly, avoiding the initial zero-filled
  String followed by character replacement.

### Find the Sum of Subsequence Powers

- Python: caches length and prunes states with too few remaining elements
  to complete a subsequence; the existing memoized recurrence is retained.
- C++: iterator-based nested-map lookup avoids repeated hash probes; the
  original cross-call cache behavior, including its failure, is retained.
- Java: a single map lookup replaces `containsKey` followed by `get`.

## Scope of this run

The prompt requests refactoring, verification, and session metrics. No
CodeCarbon measurement was run, existing measurement CSVs are unchanged,
and Codex has not been added to the measurement source configuration.
RQ3 therefore still has no Codex energy data. Existing notebook conclusions
remain descriptions of the earlier Claude measurement only.

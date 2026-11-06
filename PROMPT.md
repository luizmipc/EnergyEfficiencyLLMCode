# Prompt

This prompt was used to ask Claude to refactor 17 human-written solutions (chosen for a variety of algorithmic patterns) per language for energy efficiency, saving the results under `Results/code/claude/`. The original human-written solutions are at `src/data/human/`.

```
The original human-written solutions are at src/data/human/<ProblemName>/.

Refactor this code to reduce its energy consumption (fewer CPU cycles, fewer memory allocations, less unnecessary work), without changing its behavior or public interface (same function/class names, same inputs/outputs).

Run this as a single fresh session dedicated to this one file — do not reuse a session that already refactored another file, since the metrics below must reflect only this task.

Rules:
- Keep the same algorithm and time complexity unless a strictly better one exists — if you change it, say why in one line.
- Keep the code readable and idiomatic for the language (Python / Java / C++).
- Do not change output format, formatting, or error behavior.
- Save the refactored file under Results/code/claude/<ProblemName>/, using the same filename as the original (e.g. Results/code/claude/N-Queens/N-Queens.cpp).
- Verify the refactored file compiles/runs without errors and produces the same output as the original before treating it as final.
- Before writing the metrics file, note the wall-clock time you started this task and the time now, and compute the elapsed seconds — this is "time taken". Count how many tool calls you made to complete this task — this is "AI steps". Then run this command to read your own session's recorded token usage (do not estimate tokens yourself):
  grep -o '"usage":{[^}]*}' ~/.claude/projects/$(pwd | tr '/' '-')/$CLAUDE_CODE_SESSION_ID.jsonl
  Sum the input_tokens, output_tokens, cache_creation_input_tokens, and cache_read_input_tokens fields across all lines it prints — this is "tokens used".
- Save a .txt file named <filename-with-extension>.txt next to the refactored file (e.g. Results/code/claude/N-Queens/N-Queens.cpp.txt for the .cpp variant, N-Queens.py.txt for the .py variant — the language extension must be in the name so the three language variants don't overwrite each other's metrics file) containing the tokens used, AI steps, and time taken computed above.
- After saving, output a short bullet list (3-5 max) of the energy-relevant changes made.

Problems selected (17, chosen for variety of algorithmic patterns):
1. N-Queens — backtracking
2. Sudoku_Solver — backtracking / grid
3. Median_of_Two_Sorted_Arrays — binary search
4. Trapping_Rain_Water — two pointers
5. Largest_Rectangle_in_Histogram — monotonic stack
6. Merge_k_Sorted_Lists — heap / linked list
7. Reverse_Nodes_in_k-Group — linked list pointers
8. Regular_Expression_Matching — DP (string)
9. First_Missing_Positive — in-place array trick
10. Find_Edges_in_Shortest_Paths — graph / Dijkstra
11. Length_of_the_Longest_Increasing_Path — graph DFS + memoization
12. Minimum_Window_Substring — sliding window / hashmap
13. Permutation_Sequence — combinatorics / math
14. Sorted_GCD_Pair_Queries — number theory
15. Find_Number_of_Coins_to_Place_in_Tree_Nodes — tree DFS
16. Text_Justification — greedy / string formatting
17. Find_the_Sum_of_Subsequence_Powers — bitmask / subset DP

Apply this prompt separately to the .py, .java, and .cpp version of each problem listed above — 51 refactor runs total (17 x 3 languages), each in its own fresh session as noted above.
```

This prompt was used to ask Codex to refactor the same 17 human-written solutions per language for energy efficiency, saving the results under `Results/code/codex/`. The original human-written solutions are at `src/data/human/`.

```
The original human-written solutions are at src/data/human/<ProblemName>/.

Refactor this code to reduce its energy consumption (fewer CPU cycles, fewer memory allocations, less unnecessary work), without changing its behavior or public interface (same function/class names, same inputs/outputs).

Run this as a single fresh session dedicated to this one file — do not reuse a session that already refactored another file, since the metrics below must reflect only this task.

Rules:
- Keep the same algorithm and time complexity unless a strictly better one exists — if you change it, say why in one line.
- Keep the code readable and idiomatic for the language (Python / Java / C++).
- Do not change output format, formatting, or error behavior.
- Save the refactored file under Results/code/codex/<ProblemName>/, using the same filename as the original (e.g. Results/code/codex/N-Queens/N-Queens.cpp).
- Verify the refactored file compiles/runs without errors and produces the same output as the original before treating it as final.
- Before writing the metrics file, count how many tool calls you made to complete this task — this is "AI steps". Then find your own session's rollout log (the most recently modified file under ~/.codex/sessions/) and read it to compute, from its own recorded data rather than estimating:
  - "time taken": the difference between the first and last "timestamp" fields in that file, in seconds.
  - "tokens used": the "total_tokens" field inside the last "token_count" event's "total_token_usage" object in that file.
- Save a .txt file named <filename-with-extension>.txt next to the refactored file (e.g. Results/code/codex/N-Queens/N-Queens.cpp.txt for the .cpp variant, N-Queens.py.txt for the .py variant — the language extension must be in the name so the three language variants don't overwrite each other's metrics file) containing the tokens used, AI steps, and time taken computed above.
- After saving, output a short bullet list (3-5 max) of the energy-relevant changes made.

Problems selected (17, chosen for variety of algorithmic patterns):
1. N-Queens — backtracking
2. Sudoku_Solver — backtracking / grid
3. Median_of_Two_Sorted_Arrays — binary search
4. Trapping_Rain_Water — two pointers
5. Largest_Rectangle_in_Histogram — monotonic stack
6. Merge_k_Sorted_Lists — heap / linked list
7. Reverse_Nodes_in_k-Group — linked list pointers
8. Regular_Expression_Matching — DP (string)
9. First_Missing_Positive — in-place array trick
10. Find_Edges_in_Shortest_Paths — graph / Dijkstra
11. Length_of_the_Longest_Increasing_Path — graph DFS + memoization
12. Minimum_Window_Substring — sliding window / hashmap
13. Permutation_Sequence — combinatorics / math
14. Sorted_GCD_Pair_Queries — number theory
15. Find_Number_of_Coins_to_Place_in_Tree_Nodes — tree DFS
16. Text_Justification — greedy / string formatting
17. Find_the_Sum_of_Subsequence_Powers — bitmask / subset DP

Apply this prompt separately to the .py, .java, and .cpp version of each problem listed above — 51 refactor runs total (17 x 3 languages), each in its own fresh session as noted above.
```

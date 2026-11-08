"""Constants describing the programs under Results/code/claude (energy-refactored
by Claude) and src/data/human (the original human-written baseline).

PROGRAMS lists every problem together with the filename of its solution in
each language. Both sources use the exact same per-language filename for a
given program (the refactor kept "same filename as the original"), so one
"files" mapping per program covers both CODE_DIR and HUMAN_DIR. LANGUAGES
lists the language keys used throughout.

Each program's "leetcode_number" and "tags" come from Sheets/Tasks_and_Tags.xlsx.
TAG_CATEGORIES groups those tags the same way Sheets/Grouping_of_Tags.xlsx does
("Breadth-First Search"/"Depth-First Search" are added as aliases of "BFS"/"DFS"
since Tasks_and_Tags.xlsx spells them out in full).
"""

import os

# Repo root: src/config/constants.py -> src/config -> src -> repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CODE_DIR = os.path.join(REPO_ROOT, "Results", "code", "claude")
HUMAN_DIR = os.path.join(REPO_ROOT, "src", "data", "human")

PYTHON = "python"
JAVA = "java"
CPP = "cpp"

LANGUAGES = [PYTHON, JAVA, CPP]

# Which implementation to run: CLAUDE is the energy-refactored version under
# CODE_DIR, HUMAN is the original baseline under HUMAN_DIR.
CLAUDE = "claude"
HUMAN = "human"
SOURCES = [HUMAN, CLAUDE]

SOURCE_DIRS = {
    HUMAN: HUMAN_DIR,
    CLAUDE: CODE_DIR,
}

# How long (seconds) a single program is allowed to run before it is
# treated as failed.
TIMEOUT_SECONDS = 120

# Where codecarbon_metrics_from_code.py writes its per-run emissions.csv files:
# Analysis/data/code/<source>/<Problem>/<Language>/emissions.csv
CODECARBON_DATA_DIR = os.path.join(REPO_ROOT, "Analysis", "data", "code")

# Each program is executed this many times, with this many seconds of idle
# time between consecutive runs, when measuring with codecarbon.
CODECARBON_RUNS = 2
CODECARBON_INTERVAL_SECONDS = 5

# Each entry: problem name -> folder under CODE_DIR -> filename per language.
PROGRAMS = [
    {
        "name": "N-Queens",
        "leetcode_number": 51,
        "tags": ("Array", "Backtracking"),
        "folder": "N-Queens",
        "files": {
            PYTHON: "N-Queens_solution.py",
            JAVA: "NQueens.java",
            CPP: "N-Queens.cpp",
        },
    },
    {
        "name": "Sudoku_Solver",
        "leetcode_number": 37,
        "tags": ("Array", "Hash Table", "Backtracking", "Matrix"),
        "folder": "Sudoku_Solver",
        "files": {
            PYTHON: "Sudoku_Solver_solution.py",
            JAVA: "Sudoku_Solver.java",
            CPP: "Sudoku_Solver.cpp",
        },
    },
    {
        "name": "Median_of_Two_Sorted_Arrays",
        "leetcode_number": 4,
        "tags": ("Array", "Binary Search", "Divide and Conquer"),
        "folder": "Median_of_Two_Sorted_Arrays",
        "files": {
            PYTHON: "Median_of_Two_Sorted_Arrays_solution.py",
            JAVA: "Median_of_Two_Sorted_Arrays.java",
            CPP: "Median_of_Two_Sorted_Arrays.cpp",
        },
    },
    {
        "name": "Trapping_Rain_Water",
        "leetcode_number": 42,
        "tags": ("Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"),
        "folder": "Trapping_Rain_Water",
        "files": {
            PYTHON: "Trapping_Rain_Water_solution.py",
            JAVA: "Trapping_Rain_Water.java",
            CPP: "Trapping_Rain_Water.cpp",
        },
    },
    {
        "name": "Largest_Rectangle_in_Histogram",
        "leetcode_number": 84,
        "tags": ("Array", "Stack", "Monotonic Stack"),
        "folder": "Largest_Rectangle_in_Histogram",
        "files": {
            PYTHON: "Largest_Rectangle_in_Histogram_solution.py",
            JAVA: "Largest_Rectangle_in_Histogram.java",
            CPP: "Largest_Rectangle_in_Histogram.cpp",
        },
    },
    {
        "name": "Merge_k_Sorted_Lists",
        "leetcode_number": 23,
        "tags": ("Linked List", "Divide and Conquer", "Heap (Priority Queue)", "Merge Sort"),
        "folder": "Merge_k_Sorted_Lists",
        "files": {
            PYTHON: "Merge_k_Sorted_Lists_solution.py",
            JAVA: "Merge_k_Sorted_Lists.java",
            CPP: "Merge_k_Sorted_Lists.cpp",
        },
    },
    {
        "name": "Reverse_Nodes_in_k-Group",
        "leetcode_number": 25,
        "tags": ("Linked List", "Recursion"),
        "folder": "Reverse_Nodes_in_k-Group",
        "files": {
            PYTHON: "Reverse_Nodes_in_k-Group_solution.py",
            JAVA: "Reverse_Nodes_in_kGroup.java",
            CPP: "Reverse_Nodes_in_k-Group.cpp",
        },
    },
    {
        "name": "Regular_Expression_Matching",
        "leetcode_number": 10,
        "tags": ("String", "Dynamic Programming", "Recursion"),
        "folder": "Regular_Expression_Matching",
        "files": {
            PYTHON: "Regular_Expression_Matching_solution.py",
            JAVA: "Regular_Expression_Matching.java",
            CPP: "Regular_Expression_Matching.cpp",
        },
    },
    {
        "name": "First_Missing_Positive",
        "leetcode_number": 41,
        "tags": ("Array", "Hash Table"),
        "folder": "First_Missing_Positive",
        "files": {
            PYTHON: "First_Missing_Positive_solution.py",
            JAVA: "First_Missing_Positive.java",
            CPP: "First_Missing_Positive.cpp",
        },
    },
    {
        "name": "Find_Edges_in_Shortest_Paths",
        "leetcode_number": 3123,
        "tags": ("Depth-First Search", "Breadth-First Search", "Graph", "Heap (Priority Queue)", "Shortest Path"),
        "folder": "Find_Edges_in_Shortest_Paths",
        "files": {
            PYTHON: "Find_Edges_in_Shortest_Paths_solution.py",
            JAVA: "Find_Edges_in_Shortest_Paths.java",
            CPP: "Find_Edges_in_Shortest_Paths.cpp",
        },
    },
    {
        "name": "Length_of_the_Longest_Increasing_Path",
        "leetcode_number": 3288,
        "tags": ("Array", "Binary Search", "Sorting"),
        "folder": "Length_of_the_Longest_Increasing_Path",
        "files": {
            PYTHON: "Length_of_the_Longest_Increasing_Path_solution.py",
            JAVA: "Length_of_the_Longest_Increasing_Path.java",
            CPP: "Length_of_the_Longest_Increasing_Path.cpp",
        },
    },
    {
        "name": "Minimum_Window_Substring",
        "leetcode_number": 76,
        "tags": ("Hash Table", "String", "Sliding Window"),
        "folder": "Minimum_Window_Substring",
        "files": {
            PYTHON: "Minimum_Window_Substring_solution.py",
            JAVA: "Minimum_Window_Substring.java",
            CPP: "Minimum_Window_Substring.cpp",
        },
    },
    {
        "name": "Permutation_Sequence",
        "leetcode_number": 60,
        "tags": ("Math", "Recursion"),
        "folder": "Permutation_Sequence",
        "files": {
            PYTHON: "Permutation_Sequence_solution.py",
            JAVA: "Permutation_Sequence.java",
            CPP: "Permutation_Sequence.cpp",
        },
    },
    {
        "name": "Sorted_GCD_Pair_Queries",
        "leetcode_number": 3312,
        "tags": (
            "Array",
            "Hash Table",
            "Math",
            "Binary Search",
            "Combinatorics",
            "Counting",
            "Number Theory",
            "Prefix Sum",
        ),
        "folder": "Sorted_GCD_Pair_Queries",
        "files": {
            PYTHON: "Sorted_GCD_Pair_Queries_solution.py",
            JAVA: "Sorted_GCD_Pair_Queries.java",
            CPP: "Sorted_GCD_Pair_Queries.cpp",
        },
    },
    {
        "name": "Find_Number_of_Coins_to_Place_in_Tree_Nodes",
        "leetcode_number": 2973,
        "tags": ("Dynamic Programming", "Tree", "Depth-First Search", "Sorting", "Heap (Priority Queue)"),
        "folder": "Find_Number_of_Coins_to_Place_in_Tree_Nodes",
        "files": {
            PYTHON: "Find_Number_of_Coins_to_Place_in_Tree_Nodes_solution.py",
            JAVA: "Find_Number_of_Coins_to_Place_in_Tree_Nodes.java",
            CPP: "Find_Number_of_Coins_to_Place_in_Tree_Nodes.cpp",
        },
    },
    {
        "name": "Text_Justification",
        "leetcode_number": 68,
        "tags": ("Array", "String", "Simulation"),
        "folder": "Text_Justification",
        "files": {
            PYTHON: "Text_Justification_solution.py",
            JAVA: "Text_Justification.java",
            CPP: "Text_Justification.cpp",
        },
    },
    {
        "name": "Find_the_Sum_of_Subsequence_Powers",
        "leetcode_number": 3098,
        "tags": ("Array", "Dynamic Programming", "Sorting"),
        "folder": "Find_the_Sum_of_Subsequence_Powers",
        "files": {
            PYTHON: "Find_the_Sum_of_Subsequence_Powers_solution.py",
            JAVA: "Find_the_Sum_of_Subsequence_Powers.java",
            CPP: "Find_the_Sum_of_Subsequence_Powers.cpp",
        },
    },
]


# Broader category -> tags, mirroring Sheets/Grouping_of_Tags.xlsx. "Breadth-First
# Search" and "Depth-First Search" are added alongside "BFS"/"DFS" since
# Sheets/Tasks_and_Tags.xlsx spells those two tags out in full.
TAG_CATEGORIES = {
    "Array": ("Array", "Matrix", "Prefix Sum"),
    "Bit Manipulation": ("Bit Manipulation", "Bit Masking"),
    "Divide and Conquer": ("Divide and Conquer",),
    "Dynamic Programming": ("Dynamic Programming",),
    "Game Theory": ("Game Theory",),
    "Graph": ("Graph", "Shortest Path"),
    "Greedy": ("Greedy",),
    "Hashing": ("Hash Function", "Hash Table", "Rolling Hash"),
    "Linear structure": ("Ordered Set", "Stack", "Monotonic Stack", "Queue", "Linked List"),
    "Math": ("Math", "Counting", "Combinatorics", "Number Theory"),
    "Priority Queue": ("Heap (Priority Queue)",),
    "Recursion": ("Recursion", "Backtracking"),
    "Search algorithms": ("BFS", "Breadth-First Search", "DFS", "Depth-First Search", "Binary Search"),
    "Simulation": ("Simulation",),
    "Sliding Window": ("Sliding Window",),
    "Sorting": ("Merge Sort", "Sorting"),
    "String": ("String", "String Matching", "Suffix Array"),
    "Tree": ("Tree", "Trie", "Segment Tree"),
    "Two Pointers": ("Two Pointers",),
}

# tag -> category, built from TAG_CATEGORIES for O(1) lookups.
CATEGORY_OF_TAG = {
    tag: category for category, tags in TAG_CATEGORIES.items() for tag in tags
}


def get_program_path(program, language, source=CLAUDE):
    """Return the absolute path to a program's source file for a language.

    source selects which implementation to use: HUMAN (src/data/human, the
    original baseline) or CLAUDE (Results/code/claude, the energy-refactored
    version). Both use the same per-language filename for a given program.
    """
    base_dir = SOURCE_DIRS[source]
    return os.path.join(base_dir, program["folder"], program["files"][language])


def get_codecarbon_output_dir(program, language, source=CLAUDE):
    """Return Analysis/data/code/<source>/<Problem>/<language>, creating it
    if needed, for codecarbon_metrics_from_code.py's per-run emissions.csv."""
    output_dir = os.path.join(CODECARBON_DATA_DIR, source, program["folder"], language)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def get_tag_category(tag):
    """Return the broader category a tag belongs to, or None if unknown."""
    return CATEGORY_OF_TAG.get(tag)

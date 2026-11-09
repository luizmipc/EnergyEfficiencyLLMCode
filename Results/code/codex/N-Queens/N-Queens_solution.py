class Solution:
    def solveNQueens(self, n):
        if n < 0:
            return []
        mask = (1 << n) - 1
        row_strings = ["." * c + "Q" + "." * (n - c - 1) for c in range(n)]
        placement = []
        results = []

        def search(columns, left_diagonals, right_diagonals):
            if len(placement) == n:
                results.append([row_strings[c] for c in placement])
                return
            available = mask & ~(columns | left_diagonals | right_diagonals)
            while available:
                bit = available & -available
                available ^= bit
                placement.append(bit.bit_length() - 1)
                search(columns | bit, (left_diagonals | bit) << 1, (right_diagonals | bit) >> 1)
                placement.pop()

        search(0, 0, 0)
        return results

# Test cases for the Python solution
def testSolution(solution):
    # Test case 1: n = 1 (Single queen on the board)
    n = 1
    expected_result = [["Q"]]
    assert solution.solveNQueens(n) == expected_result, f"Test case 1 failed. Expected {expected_result}."

    # Test case 2: n = 2 (No solution exists)
    n = 2
    expected_result = []
    assert solution.solveNQueens(n) == expected_result, f"Test case 2 failed. Expected {expected_result}."

    # Test case 3: n = 3 (No solution exists)
    n = 3
    expected_result = []
    assert solution.solveNQueens(n) == expected_result, f"Test case 3 failed. Expected {expected_result}."

    # Test case 4: n = 4 (Two distinct solutions)
    n = 4
    expected_result = [
        [".Q..",  # Solution 1
         "...Q",
         "Q...",
         "..Q."],
        
        ["..Q.",  # Solution 2
         "Q...",
         "...Q",
         ".Q.."]
    ]
    assert sorted(solution.solveNQueens(n)) == sorted(expected_result), f"Test case 4 failed. Expected {expected_result}."

    # Test case 5: n = 5 (Check the number of solutions)
    n = 5
    result = solution.solveNQueens(n)
    expected_solution_count = 10
    assert len(result) == expected_solution_count, f"Test case 5 failed. Expected {expected_solution_count} solutions, got {len(result)}."

    # Test case 6: n = 6 (Check the number of solutions)
    n = 6
    result = solution.solveNQueens(n)
    expected_solution_count = 4
    assert len(result) == expected_solution_count, f"Test case 6 failed. Expected {expected_solution_count} solutions, got {len(result)}."


if __name__ == "__main__":
    solution = Solution()
    for i in range(100000):
        testSolution(solution)


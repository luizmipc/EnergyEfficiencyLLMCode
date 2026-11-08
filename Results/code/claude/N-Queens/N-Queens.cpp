#include <iostream>
#include <vector>
#include <string>
class Solution {
public:
    std::vector<std::vector<std::string> > solveNQueens(int n) {
        std::vector<std::vector<std::string> > res;
        std::vector<std::string> board(n, std::string(n, '.'));
        std::vector<bool> cols(n, false);
        std::vector<bool> diag1(2 * n, false); // index: row - col + n
        std::vector<bool> diag2(2 * n, false); // index: row + col
        solve(res, board, cols, diag1, diag2, 0, n);
        return res;
    }
private:
    void solve(std::vector<std::vector<std::string> > &res, std::vector<std::string> &board,
               std::vector<bool> &cols, std::vector<bool> &diag1, std::vector<bool> &diag2,
               int row, int n) {
        if (row == n) {
            res.push_back(board);
            return;
        }
        for (int col = 0; col < n; ++col) {
            int d1 = row - col + n;
            int d2 = row + col;
            if (cols[col] || diag1[d1] || diag2[d2])
                continue;
            cols[col] = diag1[d1] = diag2[d2] = true;
            board[row][col] = 'Q';
            solve(res, board, cols, diag1, diag2, row + 1, n);
            board[row][col] = '.';
            cols[col] = diag1[d1] = diag2[d2] = false;
        }
    }
};

//  Test cases for the C++ solution
#include <cassert>

// Test cases for the C++ solution
void testSolution(Solution& solution) {
    // Test case 1: n = 1 (Single queen on the board)
    int n = 1;
    std::vector<std::vector<std::string>> expected_result = {{"Q"}};
    assert(solution.solveNQueens(n) == expected_result && "Test case 1 failed.");

    // Test case 2: n = 2 (No solution exists)
    n = 2;
    expected_result = {};
    assert(solution.solveNQueens(n) == expected_result && "Test case 2 failed.");

    // Test case 3: n = 3 (No solution exists)
    n = 3;
    expected_result = {};
    assert(solution.solveNQueens(n) == expected_result && "Test case 3 failed.");

    // Test case 4: n = 4 (Two distinct solutions)
    n = 4;
    expected_result = {
        {".Q..",  // Solution 1
         "...Q",
         "Q...",
         "..Q."},

        {"..Q.",  // Solution 2
         "Q...",
         "...Q",
         ".Q.."}
    };
    assert(solution.solveNQueens(n) == expected_result && "Test case 4 failed.");

    // Test case 5: n = 5 (Check the number of solutions)
    n = 5;
    auto result = solution.solveNQueens(n);
    int expected_solution_count = 10;
    assert(result.size() == expected_solution_count && "Test case 5 failed.");

    // Test case 6: n = 6 (Check the number of solutions)
    n = 6;
    result = solution.solveNQueens(n);
    expected_solution_count = 4;
    assert(result.size() == expected_solution_count && "Test case 6 failed.");
}


int main() {
    Solution solution;
    for (int i = 0; i < 81920; ++i) {
        testSolution(solution);
    }
    return 0;
}

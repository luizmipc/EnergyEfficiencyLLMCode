#include <iostream>
#include <vector>
#include <algorithm>
class Solution {
public:
    std::vector<std::vector<std::string> > solveNQueens(int n) {
        std::vector<std::vector<std::string> > res;
        std::vector<std::string> nQueens(n, std::string(n, '.'));
        solveNQueens(res, nQueens, 0, n);
        return res;
    }
private:
    std::vector<unsigned char> columns, rising, falling;
    void solveNQueens(std::vector<std::vector<std::string>>& res,
                      std::vector<std::string>& board, int row, int& n) {
        if (row == 0) {
            columns.assign(n, 0);
            rising.assign(2 * n + 1, 0);
            falling.assign(2 * n + 1, 0);
        }
        if (row == n) {
            res.push_back(board);
            return;
        }
        for (int col = 0; col < n; ++col) {
            int a = row + col, b = row - col + n;
            if (columns[col] || rising[a] || falling[b]) continue;
            columns[col] = rising[a] = falling[b] = 1;
            board[row][col] = 'Q';
            solveNQueens(res, board, row + 1, n);
            board[row][col] = '.';
            columns[col] = rising[a] = falling[b] = 0;
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

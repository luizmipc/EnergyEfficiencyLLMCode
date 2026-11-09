#include <iostream>
#include <vector>
#include <climits>
#include <algorithm>
using namespace std;

class Solution {
private:
    unsigned rows[9]{}, cols[9]{}, boxes[9]{};
    bool isValid(vector<vector<char>>& board, int row, int col, char ch){
        return !((rows[row] | cols[col] | boxes[row / 3 * 3 + col / 3]) & (1u << (ch - '1')));
    }
    bool solve(vector<vector<char>>& board) {
        for(int i=0; i<board.size(); i++){
            for(int j=0; j<board[0].size(); j++){
                if(board[i][j] == '.'){
                    for(char ch='1'; ch<='9'; ch++){
                        if(isValid(board, i, j, ch)){
                            unsigned bit = 1u << (ch - '1');
                            int box = i / 3 * 3 + j / 3;
                            rows[i] |= bit; cols[j] |= bit; boxes[box] |= bit;
                            board[i][j] = ch;
                            if(solve(board) == true){
                                return true;
                            }
                            board[i][j] = '.';
                            rows[i] &= ~bit; cols[j] &= ~bit; boxes[box] &= ~bit;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }
public:
    void solveSudoku(vector<vector<char>>& board) {
        std::fill(rows, rows + 9, 0);
        std::fill(cols, cols + 9, 0);
        std::fill(boxes, boxes + 9, 0);
        for (int r = 0; r < 9; ++r)
            for (int c = 0; c < 9; ++c)
                if (board[r][c] != '.') {
                    unsigned bit = 1u << (board[r][c] - '1');
                    rows[r] |= bit; cols[c] |= bit; boxes[r / 3 * 3 + c / 3] |= bit;
                }
        solve(board);
    }
};

//  Test cases for the C++ solution
#include <cassert>

void testSolution(Solution& solution) {
    // Test case 1: A typical solvable Sudoku puzzle
    std::vector<std::vector<char>> board = {
        {'5','3','.','.','7','.','.','.','.'},
        {'6','.','.','1','9','5','.','.','.'},
        {'.','9','8','.','.','.','.','6','.'},
        {'8','.','.','.','6','.','.','.','3'},
        {'4','.','.','8','.','3','.','.','1'},
        {'7','.','.','.','2','.','.','.','6'},
        {'.','6','.','.','.','.','2','8','.'},
        {'.','.','.','4','1','9','.','.','5'},
        {'.','.','.','.','8','.','.','7','9'}
    };
    solution.solveSudoku(board);
    std::vector<std::vector<char>> expected_result = {
        {'5','3','4','6','7','8','9','1','2'},
        {'6','7','2','1','9','5','3','4','8'},
        {'1','9','8','3','4','2','5','6','7'},
        {'8','5','9','7','6','1','4','2','3'},
        {'4','2','6','8','5','3','7','9','1'},
        {'7','1','3','9','2','4','8','5','6'},
        {'9','6','1','5','3','7','2','8','4'},
        {'2','8','7','4','1','9','6','3','5'},
        {'3','4','5','2','8','6','1','7','9'}
    };
    assert(board == expected_result && "Test case 1 failed.");

    // Test case 2: A Sudoku puzzle that is already solved
    board = {
        {'8','3','5','4','1','6','9','2','7'},
        {'2','9','6','8','5','7','4','3','1'},
        {'4','1','7','2','9','3','6','5','8'},
        {'5','6','9','1','3','4','7','8','2'},
        {'1','2','3','6','7','8','5','4','9'},
        {'7','4','8','5','2','9','1','6','3'},
        {'6','5','2','7','8','1','3','9','4'},
        {'9','8','1','3','4','5','2','7','6'},
        {'3','7','4','9','6','2','8','1','5'}
    };
    solution.solveSudoku(board);
    expected_result = {
        {'8','3','5','4','1','6','9','2','7'},
        {'2','9','6','8','5','7','4','3','1'},
        {'4','1','7','2','9','3','6','5','8'},
        {'5','6','9','1','3','4','7','8','2'},
        {'1','2','3','6','7','8','5','4','9'},
        {'7','4','8','5','2','9','1','6','3'},
        {'6','5','2','7','8','1','3','9','4'},
        {'9','8','1','3','4','5','2','7','6'},
        {'3','7','4','9','6','2','8','1','5'}
    };
    assert(board == expected_result && "Test case 2 failed.");

    // Test case 3: Sudoku with only one missing cell
    board = {
        {'5','3','4','6','7','8','9','1','2'},
        {'6','7','2','1','9','5','3','4','8'},
        {'1','9','8','3','4','2','5','6','.'},
        {'8','5','9','7','6','1','4','2','3'},
        {'4','2','6','8','5','3','7','9','1'},
        {'7','1','3','9','2','4','8','5','6'},
        {'9','6','1','5','3','7','2','8','4'},
        {'2','8','7','4','1','9','6','3','5'},
        {'3','4','5','2','8','6','1','7','9'}
    };
    solution.solveSudoku(board);
    expected_result = {
        {'5','3','4','6','7','8','9','1','2'},
        {'6','7','2','1','9','5','3','4','8'},
        {'1','9','8','3','4','2','5','6','7'},
        {'8','5','9','7','6','1','4','2','3'},
        {'4','2','6','8','5','3','7','9','1'},
        {'7','1','3','9','2','4','8','5','6'},
        {'9','6','1','5','3','7','2','8','4'},
        {'2','8','7','4','1','9','6','3','5'},
        {'3','4','5','2','8','6','1','7','9'}
    };
    assert(board == expected_result && "Test case 3 failed.");
}


int main() {
    Solution solution;
    for (int i = 0; i < 5120; ++i) {
        testSolution(solution);  
    }
    return 0;
}

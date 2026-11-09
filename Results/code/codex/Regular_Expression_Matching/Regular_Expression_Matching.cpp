#include <vector>
#include <string>
#include <cstring>
using namespace std;

class Solution {
public:
    bool isMatch(string s, string p) {
        int n = s.length(), m = p.length();
        // Only the current and preceding DP rows are needed.
        vector<unsigned char> previous(m + 1, 0), current(m + 1, 0);
        previous[0] = 1;
        for (int j = 2; j <= m; ++j)
            if (p[j - 1] == '*') previous[j] = previous[j - 2];
        for (int i = 1; i <= n; ++i) {
            current[0] = 0;
            for (int j = 1; j <= m; ++j) {
                if (p[j - 1] == '*')
                    current[j] = current[j - 2] ||
                        ((s[i - 1] == p[j - 2] || p[j - 2] == '.') && previous[j]);
                else
                    current[j] = previous[j - 1] && (s[i - 1] == p[j - 1] || p[j - 1] == '.');
            }
            previous.swap(current);
        }
        return previous[m];

    }
};

//  Test cases for the C++ solution
#include <cassert>
void testSolution(Solution& solution) {
    // Test case 1: Simple match without special characters
    std::string s = "abc";
    std::string p = "abc";
    bool expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 1 failed.");

    // Test case 2: Match with '.' character
    s = "abc";
    p = "a.c";
    expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 2 failed.");

    // Test case 3: Match with '*' character (zero occurrence)
    s = "abc";
    p = "ab*c";
    expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 3 failed.");

    // Test case 4: Match with '*' character (multiple occurrences)
    s = "aab";
    p = "c*a*b";
    expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 4 failed.");

    // Test case 5: Non-match with different strings
    s = "abcd";
    p = "abc";
    expected_result = false;
    assert(solution.isMatch(s, p) == expected_result && "Test case 5 failed.");

    // Test case 6: Complex pattern with multiple '*' and '.'
    s = "mississippi";
    p = "mis*is*p*.";
    expected_result = false;
    assert(solution.isMatch(s, p) == expected_result && "Test case 6 failed.");

    // Test case 7: Full match with multiple '*' acting as zero occurrences
    s = "aa";
    p = "a*";
    expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 7 failed.");

    // Test case 8: Full match where '*' acts as multiple occurrences
    s = "aaa";
    p = "a*a";
    expected_result = true;
    assert(solution.isMatch(s, p) == expected_result && "Test case 8 failed.");
}

int main() {
    Solution solution;
    for (int i = 0; i < 1310720; ++i) {
        testSolution(solution);  
    }
    return 0;
}

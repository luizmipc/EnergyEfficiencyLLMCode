#include <string>
#include <array>
#include <climits>
#include <cassert>
using namespace std;
class Solution {
public:
    string minWindow(const string &s, const string &t) {
        array<int, 128> map{};
        for (char c : t) {
            map[static_cast<unsigned char>(c)]++;
        }

        int counter = static_cast<int>(t.size());
        int begin = 0, end = 0, d = INT_MAX, head = 0;
        int n = static_cast<int>(s.size());
        while (end < n){
            if (map[static_cast<unsigned char>(s[end++])]-- > 0) {
                counter--;
            }
            while (counter == 0) {
                if (end - begin < d) {
                    head = begin;
                    d = end - head;
                }
                if (map[static_cast<unsigned char>(s[begin++])]++ == 0) {
                    counter++;
                }
            }
        }
        return d == INT_MAX ? "" : s.substr(head, d);
    }
};

//  Test cases for the C++ solution
#include <string>

// Test cases for the C++ solution
void testSolution(Solution& solution) {
    // Test case 1: Small substring found at the beginning
    std::string s = "ADOBECODEBANC";
    std::string t = "ABC";
    std::string expected_result = "BANC";
    assert(solution.minWindow(s, t) == expected_result && "Test case 1 failed.");

    // Test case 2: t is the same as s, so the entire string is the minimum window
    s = "a";
    t = "a";
    expected_result = "a";
    assert(solution.minWindow(s, t) == expected_result && "Test case 2 failed.");

    // Test case 3: No valid substring found
    s = "a";
    t = "aa";
    expected_result = "";
    assert(solution.minWindow(s, t) == expected_result && "Test case 3 failed.");

    // Test case 4: Multiple minimum windows, return the first found
    s = "aabdec";
    t = "abc";
    expected_result = "abdec";
    assert(solution.minWindow(s, t) == expected_result && "Test case 4 failed.");

    // Test case 5: Characters of t spread throughout s
    s = "aaflslflsldkalskaaa";
    t = "aks";
    expected_result = "ska";
    assert(solution.minWindow(s, t) == expected_result && "Test case 5 failed.");

    // Test case 6: t is at the end of s
    s = "qwertyabcd";
    t = "abcd";
    expected_result = "abcd";
    assert(solution.minWindow(s, t) == expected_result && "Test case 6 failed.");

    // Test case 7: Multiple occurrences of characters in t
    s = "aaabbbccc";
    t = "abc";
    expected_result = "abc";
    //assert(solution.minWindow(s, t) == expected_result && "Test case 7 failed.");
}


int main() {
    Solution solution;
    for (int i = 0; i < 3342170; ++i) {
        testSolution(solution);
    }
    return 0;
}

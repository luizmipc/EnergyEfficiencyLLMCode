class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        return self.backtrack({}, s, p, len(s) - 1, len(p) - 1)

    def backtrack(self, cache, s, p, i, j):
        key = (i, j)
        cached = cache.get(key)
        if cached is not None:
            return cached

        if i == -1 and j == -1:
            result = True
        elif j == -1:
            result = False
        elif i == -1:
            if p[j] == '*':
                k = j
                while k != -1 and p[k] == '*':
                    k -= 2
                result = (k == -1)
            else:
                result = False
        elif p[j] == '*':
            result = self.backtrack(cache, s, p, i, j - 2) or \
                      ((p[j - 1] == s[i] or p[j - 1] == '.') and self.backtrack(cache, s, p, i - 1, j))
        elif p[j] == '.' or s[i] == p[j]:
            result = self.backtrack(cache, s, p, i - 1, j - 1)
        else:
            result = False

        cache[key] = result
        return result

# Test cases for the Python solution
def testSolution(solution):
    # Test case 1: Simple match without special characters
    s = "abc"
    p = "abc"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 1 failed. Expected {expected_result}."

    # Test case 2: Match with '.' character
    s = "abc"
    p = "a.c"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 2 failed. Expected {expected_result}."

    # Test case 3: Match with '*' character (zero occurrence)
    s = "abc"
    p = "ab*c"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 3 failed. Expected {expected_result}."

    # Test case 4: Match with '*' character (multiple occurrences)
    s = "aab"
    p = "c*a*b"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 4 failed. Expected {expected_result}."

    # Test case 5: Non-match with different strings
    s = "abcd"
    p = "abc"
    expected_result = False
    assert solution.isMatch(s, p) == expected_result, f"Test case 5 failed. Expected {expected_result}."

    # Test case 6: Complex pattern with multiple '*' and '.'
    s = "mississippi"
    p = "mis*is*p*."
    expected_result = False
    assert solution.isMatch(s, p) == expected_result, f"Test case 6 failed. Expected {expected_result}."

    # Test case 7: Full match with multiple '*' acting as zero occurrences
    s = "aa"
    p = "a*"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 7 failed. Expected {expected_result}."

    # Test case 8: Full match where '*' acts as multiple occurrences
    s = "aaa"
    p = "a*a"
    expected_result = True
    assert solution.isMatch(s, p) == expected_result, f"Test case 8 failed. Expected {expected_result}."

if __name__ == "__main__":
    solution = Solution()
    for i in range(700000):
        testSolution(solution)

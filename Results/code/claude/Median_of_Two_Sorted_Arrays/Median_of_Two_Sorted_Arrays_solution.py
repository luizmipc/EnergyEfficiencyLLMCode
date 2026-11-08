class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        # Ensure nums1 is the smaller array for simplicity
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        n1 = len(nums1)
        n2 = len(nums2)
        n = n1 + n2
        left = (n + 1) // 2  # Calculate the left partition size
        low = 0
        high = n1
        NEG_INF = float('-inf')
        POS_INF = float('inf')

        while low <= high:
            mid1 = (low + high) // 2  # Calculate mid index for nums1
            mid2 = left - mid1  # Calculate mid index for nums2

            # Determine values of l1, l2, r1, and r2
            l1 = nums1[mid1 - 1] if mid1 > 0 else NEG_INF
            l2 = nums2[mid2 - 1] if mid2 > 0 else NEG_INF
            r1 = nums1[mid1] if mid1 < n1 else POS_INF
            r2 = nums2[mid2] if mid2 < n2 else POS_INF

            if l1 <= r2 and l2 <= r1:
                # The partition is correct, we found the median
                if n % 2 == 1:
                    return max(l1, l2)
                else:
                    return (max(l1, l2) + min(r1, r2)) / 2.0
            elif l1 > r2:
                # Move towards the left side of nums1
                high = mid1 - 1
            else:
                # Move towards the right side of nums1
                low = mid1 + 1

        return 0  # If the code reaches here, the input arrays were not sorted.

# Test cases for the Python solution
def testSolution(solution):
    # Test case 1: Both arrays are of the same size and have a clear median
    nums1 = [1, 3]
    nums2 = [2]
    expected_result = 2.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 1 failed. Expected {expected_result}."

    # Test case 2: Arrays of different sizes with an even combined length
    nums1 = [1, 2]
    nums2 = [3, 4]
    expected_result = 2.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 2 failed. Expected {expected_result}."

    # Test case 3: One array is empty
    nums1 = []
    nums2 = [1]
    expected_result = 1.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 3 failed. Expected {expected_result}."

    # Test case 4: Both arrays have the same elements
    nums1 = [1, 1]
    nums2 = [1, 1]
    expected_result = 1.0
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 4 failed. Expected {expected_result}."

    # Test case 5: Arrays with negative and positive numbers
    nums1 = [-5, 3, 6]
    nums2 = [-2, 0, 9]
    expected_result = 1.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 5 failed. Expected {expected_result}."

    # Test case 6: Large arrays to check efficiency
    nums1 = list(range(100000))
    nums2 = list(range(100000, 200000))
    expected_result = 99999.5
    assert solution.findMedianSortedArrays(nums1, nums2) == expected_result, f"Test case 6 failed. Expected {expected_result}."

if __name__ == "__main__":
    solution = Solution()
    for i in range(5000):
        testSolution(solution)

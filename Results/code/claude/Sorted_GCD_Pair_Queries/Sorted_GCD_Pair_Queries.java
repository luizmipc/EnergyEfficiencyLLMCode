import java.util.Arrays;

class Solution {
    // Reused across calls (the test harness calls gcdValues repeatedly on the
    // same Solution instance) so these O(maxValue) buffers only ever grow,
    // instead of being freshly allocated on every single call.
    private int[] divisorCount = new int[0];
    private long[] gcdPairCount = new long[0];
    private long[] prefixSum = new long[0];

    public int[] gcdValues(int[] nums, long[] queries) {
        int maxValue = nums[0];
        for (int x : nums) {
            if (x > maxValue) maxValue = x;
        }

        int need = maxValue + 1;
        if (divisorCount.length < need) {
            divisorCount = new int[need];
            gcdPairCount = new long[need];
            prefixSum = new long[need];
        } else {
            Arrays.fill(divisorCount, 0, need, 0);
            Arrays.fill(gcdPairCount, 0, need, 0);
            Arrays.fill(prefixSum, 0, need, 0);
        }

        for (int number : nums) {
            for (int i = 1; i * i <= number; i++) {
                if (number % i == 0) {
                    divisorCount[i]++;
                    if (i != number / i) {
                        divisorCount[number / i]++;
                    }
                }
            }
        }

        for (int gcd = maxValue; gcd >= 1; gcd--) {
            long count = divisorCount[gcd];
            gcdPairCount[gcd] = count * (count - 1) / 2;
            for (int multiple = 2 * gcd; multiple <= maxValue; multiple += gcd) {
                gcdPairCount[gcd] -= gcdPairCount[multiple];
            }
        }

        for (int gcd = 1; gcd <= maxValue; gcd++) {
            prefixSum[gcd] = prefixSum[gcd - 1] + gcdPairCount[gcd];
        }

        int[] result = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            long query = queries[i];
            long left = 1, right = maxValue, answer = -1;
            while (left <= right) {
                long mid = (left + right) / 2;
                if (prefixSum[(int) mid] > query) {
                    answer = mid;
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            }
            result[i] = (int) answer;
        }

        return result;
    }
}

public class Sorted_GCD_Pair_Queries {
public static void runTests(Solution solution) {
        // Test case 1
        int[] nums = {2, 3};
        long[] queries = {0};
        int[] expectedResult = {1};  // Only one pair, GCD(2, 3) = 1
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 1 failed. Expected " + java.util.Arrays.toString(expectedResult);

        // Test case 2
        nums = new int[]{2, 3, 4};
        queries = new long[]{0, 2, 2};
        expectedResult = new int[]{1, 2, 2};  // GCD pairs sorted: [2, 2, 1]
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 2 failed. Expected " + java.util.Arrays.toString(expectedResult);

        // Test case 3
        nums = new int[]{4, 8, 12};
        queries = new long[]{0, 1, 2};
        expectedResult = new int[]{4, 4, 4};  // GCD pairs sorted: [4, 4, 4]
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 3 failed. Expected " + java.util.Arrays.toString(expectedResult);

        // Test case 4
        nums = new int[]{2, 3, 5, 7};
        queries = new long[]{0, 1, 2, 3, 4, 5};
        expectedResult = new int[]{1, 1, 1, 1, 1, 1};  // GCDs are all 1 for prime pairs
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 4 failed. Expected " + java.util.Arrays.toString(expectedResult);

        // Test case 5
        nums = new int[]{4, 4, 2, 1};
        queries = new long[]{5, 3, 1, 0};
        expectedResult = new int[]{4, 2, 1, 1};  // GCD pairs sorted: [4, 4, 2, 2, 2, 1]
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 5 failed. Expected " + java.util.Arrays.toString(expectedResult);

        // Test case 6
        nums = new int[]{100000, 100000};
        queries = new long[]{0};
        expectedResult = new int[]{100000};  // Only one GCD of the pair: [100000]
        assert java.util.Arrays.equals(solution.gcdValues(nums, queries), expectedResult)
            : "Test case 6 failed. Expected " + java.util.Arrays.toString(expectedResult);
}

    public static void main(String[] args) {
        Solution solution = new Solution();
        for (int i = 0; i < 20000; i++) {
            runTests(solution); // Ensure your test cases are implemented inside runTests
        }
    }
}

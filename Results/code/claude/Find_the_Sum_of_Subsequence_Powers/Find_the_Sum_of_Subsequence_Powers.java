import java.util.Arrays;
import java.util.HashMap;

class Solution {
    int mod = (int)1e9+7;
    HashMap<Long,Integer> memo;
    public int sumOfPowers(int[] nums, int k) {
        Arrays.sort(nums);
        memo=new HashMap<>();
        return dp(nums,k,0,Integer.MAX_VALUE,nums.length-1,nums.length);
    }

    // diff is always a non-negative difference of sorted values (fits in 32 bits),
    // and len/index/prev are all small (bounded by n), so the full state packs
    // into one long key -- avoiding the original's string concatenation
    // ("diff_len_index_prev") that had to be built and hashed character-by-character
    // on every memo access.
    private static long packKey(int diff, int len, int index, int prev) {
        return ((long) diff << 32)
                | ((long) (len & 0x3FF) << 20)
                | ((long) ((index + 1) & 0x3FF) << 10)
                | ((long) (prev & 0x3FF));
    }

    int dp(int[] nums,int k, int len, int diff, int index, int prev){
        if(len==k){
            return diff;
        }
        if(index<0) return Integer.MAX_VALUE;
        long key = packKey(diff, len, index, prev);
        Integer cached = memo.get(key);
        if(cached != null) return cached;
        int temp = dp(nums,k,len,diff,index-1,prev);
        int total=0;
        if(temp!=Integer.MAX_VALUE) total+=temp;
        if(prev!=nums.length) diff=Math.min(diff,nums[prev]-nums[index]);
        temp=dp(nums,k,len+1,diff,index-1,index);
        if(temp!=Integer.MAX_VALUE) total = total + temp;
        total%=mod;
        memo.put(key,total);
        return total;
    }
}

public class Find_the_Sum_of_Subsequence_Powers {
public static void runTests(Solution solution) {
    // Test case 1: Small array with subsequence length k
    int[] nums1 = {1, 2, 3, 4};
    int k1 = 3;
    int expected_result1 = 4;
    assert solution.sumOfPowers(nums1, k1) == expected_result1 : "Test case 1 failed. Expected " + expected_result1;

    // Test case 2: Array with identical elements
    int[] nums2 = {4, 4, 4};
    int k2 = 2;
    int expected_result2 = 0;
    assert solution.sumOfPowers(nums2, k2) == expected_result2 : "Test case 2 failed. Expected " + expected_result2;

    // Test case 3: Larger k than length of nums
    int[] nums3 = {1, 2, 3};
    int k3 = 4;
    int expected_result3 = 0;
    assert solution.sumOfPowers(nums3, k3) == expected_result3 : "Test case 3 failed. Expected " + expected_result3;

    // Test case 4: Entire array as subsequence
    int[] nums4 = {2, 5, 8};
    int k4 = 3;
    int expected_result4 = 3;
    assert solution.sumOfPowers(nums4, k4) == expected_result4 : "Test case 4 failed. Expected " + expected_result4;

    // Test case 5: Subsequence length 1 (all elements are valid)
    int[] nums5 = {7, 14, 21};
    int k5 = 1;
    int expected_result5 = 0;
    assert solution.sumOfPowers(nums5, k5) == expected_result5 : "Test case 5 failed. Expected " + expected_result5;

    // Test case 6: Mixed values in nums
    int[] nums6 = {4, 3, -1};
    int k6 = 2;
    int expected_result6 = 10;
    assert solution.sumOfPowers(nums6, k6) == expected_result6 : "Test case 6 failed. Expected " + expected_result6;

    // Test case 7: Large array with large values
    int[] nums7 = {1000000, 2000000, 3000000};
    int k7 = 2;
    int expected_result7 = 4000000;
    assert solution.sumOfPowers(nums7, k7) == expected_result7 : "Test case 7 failed. Expected " + expected_result7;
}


    public static void main(String[] args) {
        Solution solution = new Solution();
        for (int i = 0; i < 3000000; i++) {
            runTests(solution); // Ensure your test cases are implemented inside runTests
        }
    }
}

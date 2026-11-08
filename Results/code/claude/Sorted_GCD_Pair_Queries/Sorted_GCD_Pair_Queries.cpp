#include <vector>
#include <algorithm>
using namespace std;

class Solution{
public:
    // Reused across calls (the test harness calls gcdValues repeatedly on the
    // same Solution instance) so the O(maxx) buffers only ever grow, instead of
    // being heap-allocated and freed on every single call.
    vector<int> cntDivisors;
    vector<long long int> gcdCount, pref;

    vector<int> gcdValues(vector<int>& v, vector<long long>& q){
        int maxx = *max_element(v.begin(), v.end());
        size_t need = static_cast<size_t>(maxx) + 1;
        if(cntDivisors.size() < need){
            cntDivisors.assign(need, 0);
            gcdCount.assign(need, 0);
            pref.assign(need, 0);
        } else {
            fill(cntDivisors.begin(), cntDivisors.begin() + need, 0);
            fill(gcdCount.begin(), gcdCount.begin() + need, 0);
            fill(pref.begin(), pref.begin() + need, 0);
        }

        for(auto x : v){
            for(int i = 1; i * i <= x; i++){
                if(x % i == 0){
                    cntDivisors[i]++;
                    if(i != x / i){
                        cntDivisors[x / i]++;
                    }
                }
            }
        }
        for(int g = maxx; g >= 1; g--){
            long long int count = cntDivisors[g];
            gcdCount[g] = 1ll * count *(count - 1) / 2;
            for(int mult = 2 * g; mult <= maxx; mult += g){
                gcdCount[g] -= gcdCount[mult];
            }
        }

        for(int g = 1; g <= maxx; g++){
            pref[g] = pref[g - 1] + gcdCount[g];
        }
        vector<int> ans;
        ans.reserve(q.size());
        for(auto query : q){
            long long int left = 1, right = maxx, answer = -1;
            while(left <= right){
                long long int mid =(left + right) / 2;
                if(pref[mid] > query){
                    answer = mid;
                    right = mid - 1;
                } else{
                    left = mid + 1;
                }
            }
            ans.push_back(answer);
        }

        return ans;
    }
};

//  Test cases for the C++ solution
#include <cassert>

void testSolution(Solution& solution) {

    // Test case 1: Simple case with two numbers
    std::vector<int> nums = {2, 3};
    std::vector<long long> queries = {0};
    std::vector<int> expected_result = {1};  // Only one pair, GCD(2, 3) = 1
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 1 failed. Expected {1}.");

    // Test case 2: Multiple pairs with diverse GCDs
    nums = {2, 3, 4};
    queries = {0, 2, 2};
    expected_result = {1, 2, 2};  // GCD pairs sorted: [2, 2, 1]
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 2 failed. Expected {1, 2, 2}.");

    // Test case 3: All numbers are multiples of a common number
    nums = {4, 8, 12};
    queries = {0, 1, 2};
    expected_result = {4, 4, 4};  // GCD pairs sorted: [4, 4, 4]
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 3 failed. Expected {4, 4, 4}.");

    // Test case 4: GCD results in multiple distinct values
    nums = {2, 3, 5, 7};
    queries = {0, 1, 2, 3, 4, 5};
    expected_result = {1, 1, 1, 1, 1, 1};  // GCDs are all 1 for prime pairs
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 4 failed. Expected {1, 1, 1, 1, 1, 1}.");

    // Test case 5: GCD values with repeated elements in nums
    nums = {4, 4, 2, 1};
    queries = {5, 3, 1, 0};
    expected_result = {4, 2, 1, 1};  // GCD pairs sorted: [4, 4, 2, 2, 2, 1]
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 5 failed. Expected {4, 2, 1, 1}.");

    // Test case 6: Large number with single pair
    nums = {100000, 100000};
    queries = {0};
    expected_result = {100000};  // Only one GCD of the pair: [100000]
    assert(solution.gcdValues(nums, queries) == expected_result && "Test case 6 failed. Expected {100000}.");
}


int main() {
    Solution solution;
    for (int i = 0; i < 1280; ++i) {
        testSolution(solution);
    }
    return 0;
}

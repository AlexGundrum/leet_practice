import json

with open('c:\\Users\\alexg\\code\\leet_practice\\batch_45_59.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

enrichments = [
    {
        "solution_code": """class Solution:
    def merge_k_lists(self, lists: list[ListNode]) -> ListNode:
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))
        
        dummy = ListNode()
        curr = dummy
        
        while heap:
            val, i, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
                
        return dummy.next""",
        "solution_explanation": "A min-heap is ideal for tracking the minimum element across K sorted lists. By pushing the head of each list into the heap, we can continuously extract the smallest element overall. We include the list index `i` in the heap tuple `(val, i, node)` to break ties safely when two node values are equal, since `ListNode` might not implement comparison operators. After popping the smallest element, if its list has more nodes, we push the next node back into the heap.",
        "when_to_use": "Use when you need to combine multiple sorted arrays or linked lists into a single sorted output, or when finding the k-th smallest element across multiple sorted sequences.",
        "test_cases": [
            {"call": "def mk(vs):\n    if not vs:return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge_k_lists([mk([1,4,5]),mk([1,3,4]),mk([2,6])]))", "expected": "[1, 1, 2, 3, 4, 4, 5, 6]"},
            {"call": "ls(Solution().merge_k_lists([]))", "expected": "[]"},
            {"call": "ls(Solution().merge_k_lists([mk([])]))", "expected": "[]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def top_k_frequent(self, nums: list[int], k: int) -> list[int]:
        counts = Counter(nums)
        heap = []
        for num, freq in counts.items():
            heapq.heappush(heap, (freq, num))
            if len(heap) > k:
                heapq.heappop(heap)
        return [num for freq, num in heap]""",
        "solution_explanation": "We first count the frequencies of all elements. Then, we use a min-heap of size `k` to keep track of the most frequent elements seen so far. Pushing to a heap of size `k` takes O(log k) time. If the heap size exceeds `k`, we pop the element with the smallest frequency (at the root of the min-heap). By doing this, we maintain exactly the top `k` frequencies in O(N log K) time, which is optimal for small k.",
        "when_to_use": "Use when you need to find the top/bottom K elements of a dataset based on some property like frequency, value, or distance without fully sorting the entire dataset.",
        "test_cases": [
            {"call": "sorted(Solution().top_k_frequent([1,1,1,2,2,3],2))", "expected": "[1, 2]"},
            {"call": "Solution().top_k_frequent([1],1)", "expected": "[1]"},
            {"call": "sorted(Solution().top_k_frequent([-1,-1],1))", "expected": "[-1]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def max_sum(self, nums: list[int], k: int) -> int:
        if not nums or k <= 0:
            return 0
        window_sum = sum(nums[:k])
        max_sum = window_sum
        for i in range(len(nums) - k):
            window_sum += nums[i + k] - nums[i]
            max_sum = max(max_sum, window_sum)
        return max_sum""",
        "solution_explanation": "This uses a fixed-size sliding window. Instead of recalculating the sum of k elements at every step (which would take O(N*k) time), we compute the sum of the first window. Then, as the window slides to the right, we simply add the new element entering the window and subtract the old element leaving it. This takes O(1) time per step, reducing the overall time complexity to O(N).",
        "when_to_use": "Use when you need to compute a statistic (sum, average, max, min) over all contiguous subarrays of a specific fixed size.",
        "test_cases": [
            {"call": "Solution().max_sum([2,1,5,1,3,2],3)", "expected": "9"},
            {"call": "Solution().max_sum([2,3,4,1,5],2)", "expected": "7"},
            {"call": "Solution().max_sum([-1,-2,-3,-4],2)", "expected": "-3"}
        ]
    },
    {
        "solution_code": """class Solution:
    def length_of_longest(self, s: str) -> int:
        char_index = {}
        max_len = 0
        left = 0
        
        for right, char in enumerate(s):
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            char_index[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len""",
        "solution_explanation": "We use a variable-size sliding window with a dictionary to track the most recent index of each character. The `left` pointer marks the start of the valid window. If we encounter a character that is already in our dictionary and its recorded index is inside the current window (`>= left`), we must shrink the window by moving `left` to `char_index[char] + 1` to exclude the duplicate. Then we update the max length.",
        "when_to_use": "Use when finding the longest or shortest contiguous subarray/substring that meets a specific dynamic constraint (e.g., no duplicates, sum <= target).",
        "test_cases": [
            {"call": "Solution().length_of_longest(\"abcabcbb\")", "expected": "3"},
            {"call": "Solution().length_of_longest(\"bbbbb\")", "expected": "1"},
            {"call": "Solution().length_of_longest(\"pwwkew\")", "expected": "3"},
            {"call": "Solution().length_of_longest(\"\")", "expected": "0"}
        ]
    },
    {
        "solution_code": """class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        left, right = 0, len(nums) - 1
        
        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                return [left, right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return []""",
        "solution_explanation": "Because the array is sorted, we can use two pointers starting at both ends. The sum of the values at `left` and `right` gives a current sum. If the sum is too small, the only way to increase it is to move the `left` pointer to the right (to a larger number). If the sum is too large, we must decrease it by moving the `right` pointer to the left. This explores candidates in O(N) time with O(1) space.",
        "when_to_use": "Use when searching for pairs of elements in a sorted array that satisfy a condition relating to their sum, difference, or product.",
        "test_cases": [
            {"call": "Solution().two_sum([2,7,11,15],9)", "expected": "[0, 1]"},
            {"call": "Solution().two_sum([2,3,4],6)", "expected": "[0, 2]"},
            {"call": "Solution().two_sum([-1,0],-1)", "expected": "[0, 1]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def sort_colors(self, nums: list[int]) -> list[int]:
        low, mid, high = 0, 0, len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
        return nums""",
        "solution_explanation": "This algorithm partitions an array into three regions using three pointers: `low` bounds the 0s, `high` bounds the 2s, and `mid` is the current element under inspection. When `nums[mid]` is 0, we swap it with the `low` boundary and advance both. If it's 1, it's already in the correct middle region, so we just advance `mid`. If it's 2, we swap it with the `high` boundary and decrease `high` (we don't advance `mid` here because the swapped-in value needs to be evaluated). The loop invariant `mid <= high` ensures all elements are processed.",
        "when_to_use": "Use when sorting an array with a small number of distinct values (usually 3) in O(N) time and O(1) space, avoiding counting sort's two passes.",
        "test_cases": [
            {"call": "Solution().sort_colors([2,0,2,1,1,0])", "expected": "[0, 0, 1, 1, 2, 2]"},
            {"call": "Solution().sort_colors([2,0,1])", "expected": "[0, 1, 2]"},
            {"call": "Solution().sort_colors([0])", "expected": "[0]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def find_duplicate(self, nums: list[int]) -> int:
        slow, fast = nums[0], nums[nums[0]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]
            
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
            
        return slow""",
        "solution_explanation": "This models the array as a linked list where the index `i` points to `nums[i]`. Because there are n+1 numbers in the range [1, n], a cycle is guaranteed to exist. We use Floyd's Cycle Detection: first, advance `slow` by 1 step and `fast` by 2 steps until they intersect inside the cycle. Then, reset `slow` to the start (0) and move both pointers 1 step at a time. The point where they meet again is the start of the cycle, which corresponds exactly to the duplicate number.",
        "when_to_use": "Use for cycle detection in linked lists or when an array inherently forms a functional graph mapping indices to values with guaranteed cycles.",
        "test_cases": [
            {"call": "Solution().find_duplicate([1,3,4,2,2])", "expected": "2"},
            {"call": "Solution().find_duplicate([3,1,3,4,2])", "expected": "3"},
            {"call": "Solution().find_duplicate([2,2,2,2,2])", "expected": "2"}
        ]
    },
    {
        "solution_code": """class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]""",
        "solution_explanation": "We precompute an array `prefix` where `prefix[i]` stores the sum of elements from index `0` to `i-1`. This takes O(N) time upfront. Once built, the sum of any subarray from `left` to `right` can be computed in O(1) time by taking `prefix[right + 1] - prefix[left]`. The padding with a leading 0 prevents out-of-bounds indexing when `left == 0`.",
        "when_to_use": "Use when you need to answer multiple sum queries over continuous subarrays of an immutable array efficiently.",
        "test_cases": [
            {"call": "n=NumArray([-2,0,3,-5,2,-1]);[n.sum_range(0,2),n.sum_range(2,5),n.sum_range(0,5)]", "expected": "[1, -1, -3]"},
            {"call": "n=NumArray([1]);[n.sum_range(0,0)]", "expected": "[1]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def max_subarray(self, nums: list[int]) -> int:
        max_current = max_global = nums[0]
        for num in nums[1:]:
            max_current = max(num, max_current + num)
            max_global = max(max_global, max_current)
        return max_global""",
        "solution_explanation": "Kadane's algorithm uses dynamic programming. We maintain `max_current`, which represents the maximum sum of a subarray ending at the current element. At each step, we have a choice: either extend the previous subarray by adding the current element (`max_current + num`), or start a completely new subarray from the current element (`num`). We take the maximum of these choices. `max_global` tracks the highest `max_current` seen so far.",
        "when_to_use": "Use when finding the maximum/minimum sum of any contiguous subarray in a 1D array.",
        "test_cases": [
            {"call": "Solution().max_subarray([-2,1,-3,4,-1,2,1,-5,4])", "expected": "6"},
            {"call": "Solution().max_subarray([1])", "expected": "1"},
            {"call": "Solution().max_subarray([5,4,-1,7,8])", "expected": "23"},
            {"call": "Solution().max_subarray([-5,-2,-9])", "expected": "-2"}
        ]
    },
    {
        "solution_code": """class Solution:
    def climb_stairs(self, n: int) -> int:
        if n <= 2:
            return n
        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2, prev1 = prev1, curr
        return prev1""",
        "solution_explanation": "This is fundamentally the Fibonacci sequence. To reach step `i`, you could have come from step `i-1` (taking 1 step) or step `i-2` (taking 2 steps). Thus, the number of ways to reach step `i` is the sum of ways to reach `i-1` and `i-2`. Instead of using an O(N) array for DP, we optimize space to O(1) by only storing the two most recent values (`prev1` and `prev2`).",
        "when_to_use": "Use when the current state depends linearly on a fixed number of strictly previous states (e.g., computing paths, combinations in sequence).",
        "test_cases": [
            {"call": "Solution().climb_stairs(5)", "expected": "8"},
            {"call": "Solution().climb_stairs(3)", "expected": "3"},
            {"call": "Solution().climb_stairs(1)", "expected": "1"}
        ]
    },
    {
        "solution_code": """class Solution:
    def rob(self, nums: list[int]) -> int:
        rob_prev2, rob_prev1 = 0, 0
        for num in nums:
            current = max(rob_prev1, rob_prev2 + num)
            rob_prev2, rob_prev1 = rob_prev1, current
        return rob_prev1""",
        "solution_explanation": "For each house, you have two choices: rob it (which means you add its money to the max money from `i-2` houses ago) or skip it (which means you keep the max money from `i-1` houses ago). The relation is `DP[i] = max(DP[i-1], DP[i-2] + nums[i])`. Similar to Fibonacci, we only need to track the last two maximums to maintain O(1) space complexity.",
        "when_to_use": "Use when you need to select elements from an array to maximize a sum, subject to the constraint that no two adjacent elements can be selected.",
        "test_cases": [
            {"call": "Solution().rob([2,7,9,3,1])", "expected": "12"},
            {"call": "Solution().rob([1,2,3,1])", "expected": "4"},
            {"call": "Solution().rob([2,1])", "expected": "2"},
            {"call": "Solution().rob([0])", "expected": "0"}
        ]
    },
    {
        "solution_code": """class Solution:
    def coin_change(self, coins: list[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
                
        return dp[amount] if dp[amount] != float('inf') else -1""",
        "solution_explanation": "We use a 1D DP array where `dp[i]` represents the minimum coins needed for amount `i`. We initialize the array with infinity and `dp[0] = 0` (0 coins for amount 0). For each coin, we iterate from its value up to `amount`. If we use the coin, the new total is `1 + dp[x - coin]`. We take the minimum of using the coin or not using it. The unbounded nature means we traverse left-to-right so that a coin can be picked multiple times.",
        "when_to_use": "Use when filling a capacity (amount) with items (coins) where each item can be used an unlimited number of times, to minimize or maximize a count.",
        "test_cases": [
            {"call": "Solution().coin_change([1,5,6,9],11)", "expected": "2"},
            {"call": "Solution().coin_change([2],3)", "expected": "-1"},
            {"call": "Solution().coin_change([1],0)", "expected": "0"}
        ]
    },
    {
        "solution_code": """class Solution:
    def length_of_lis(self, nums: list[int]) -> int:
        sub = []
        for num in nums:
            idx = bisect.bisect_left(sub, num)
            if idx == len(sub):
                sub.append(num)
            else:
                sub[idx] = num
        return len(sub)""",
        "solution_explanation": "Instead of standard O(N^2) DP, we build an array `sub` that keeps track of the smallest tail elements for all increasing subsequences of various lengths. For each number, we use binary search (`bisect_left`) to find where it fits in `sub`. If it's larger than all elements, it extends the longest subsequence. Otherwise, it replaces the first element in `sub` that is `>= num`, keeping the end values as small as possible to allow future extensions. The length of `sub` is the LIS.",
        "when_to_use": "Use when finding the Longest Increasing/Decreasing Subsequence efficiently in O(N log N) time.",
        "test_cases": [
            {"call": "Solution().length_of_lis([10,9,2,5,3,7,101,18])", "expected": "4"},
            {"call": "Solution().length_of_lis([0,1,0,3,2,3])", "expected": "4"},
            {"call": "Solution().length_of_lis([7,7,7,7])", "expected": "1"}
        ]
    },
    {
        "solution_code": """class Solution:
    def lcs(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [0] * (n + 1)
        
        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if text1[i - 1] == text2[j - 1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev = temp
                
        return dp[n]""",
        "solution_explanation": "This computes LCS using an optimized 1D array instead of an O(M*N) 2D grid. The state `dp[j]` relates to `text2` prefix of length `j`. If the characters match, the LCS length is `1 + prev` (where `prev` holds the value from the diagonal, `dp[i-1][j-1]`). If they don't match, we take the max of skipping a character from `text1` (`dp[j]` from the previous row) or `text2` (`dp[j-1]` from the current row). We use `temp` to correctly update `prev` before overwriting.",
        "when_to_use": "Use when finding the similarity or maximum common non-contiguous elements between two sequences (strings or arrays).",
        "test_cases": [
            {"call": "Solution().lcs(\"abcde\",\"ace\")", "expected": "3"},
            {"call": "Solution().lcs(\"abc\",\"abc\")", "expected": "3"},
            {"call": "Solution().lcs(\"abc\",\"def\")", "expected": "0"}
        ]
    },
    {
        "solution_code": """class Solution:
    def min_distance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = list(range(n + 1))
        
        for i in range(1, m + 1):
            prev = dp[0]
            dp[0] = i
            for j in range(1, n + 1):
                temp = dp[j]
                if word1[i - 1] == word2[j - 1]:
                    dp[j] = prev
                else:
                    dp[j] = 1 + min(prev, dp[j], dp[j - 1])
                prev = temp
                
        return dp[n]""",
        "solution_explanation": "We determine the minimum operations to convert `word1` to `word2`. We optimize space to O(N) by using a 1D DP array where `dp[j]` tracks the edits for prefixes of length `j`. If the current characters match, no extra edit is needed (`dp[j] = prev`). If they differ, we choose the cheapest of three operations: insert (`dp[j-1]`), delete (`dp[j]`), or replace (`prev`), plus 1. The variable `prev` stores the `i-1, j-1` diagonal value before it gets overwritten.",
        "when_to_use": "Use when measuring the difference/distance between two strings by counting the minimum single-character insertions, deletions, and substitutions.",
        "test_cases": [
            {"call": "Solution().min_distance(\"horse\",\"ros\")", "expected": "3"},
            {"call": "Solution().min_distance(\"intention\",\"execution\")", "expected": "5"},
            {"call": "Solution().min_distance(\"\",\"a\")", "expected": "1"}
        ]
    }
]

for i in range(len(data)):
    data[i].update(enrichments[i])

with open('c:\\Users\\alexg\\code\\leet_practice\\enriched_batch_45_59.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Enrichment complete.")

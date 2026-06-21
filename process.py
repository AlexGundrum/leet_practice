import json

with open('c:/Users/alexg/code/leet_practice/algorithms.json', 'r') as f:
    data = json.load(f)

batch = data[30:45]

enrichment = [
    {
        "solution_code": """class Codec:
    def serialize(self, root: TreeNode) -> str:
        vals = []
        def dfs(node):
            if not node:
                vals.append("N")
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> TreeNode:
        vals = iter(data.split(","))
        def dfs():
            val = next(vals)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()""",
        "solution_explanation": "Preorder traversal provides a natural serialization order because the root is processed first. By including explicit markers (like \"N\") for null pointers, we eliminate ambiguity about the tree's structure. During deserialization, an iterator makes it easy to process values exactly in the preorder sequence. The recursive `dfs` reconstruction naturally rebuilds subtrees from the iterator sequence.",
        "when_to_use": "When you need to transmit a tree across a network or save it to a file. Preorder with null markers is optimal because it avoids the trailing nulls issue of level-order serialization and guarantees uniqueness.",
        "test_cases": [
            {"call": "c=Codec()\nres=c.deserialize('1,2,N,N,3,4,N,N,5,N,N')\nc.serialize(res)", "expected": "'1,2,N,N,3,4,N,N,5,N,N'"},
            {"call": "c=Codec()\nres=c.deserialize('N')\nc.serialize(res)", "expected": "'N'"},
            {"call": "c=Codec()\nres=c.deserialize('1,N,2,N,N')\nc.serialize(res)", "expected": "'1,N,2,N,N'"}
        ]
    },
    {
        "solution_code": """class Solution:
    def build_tree(self, preorder: list[int], inorder: list[int]) -> TreeNode:
        inorder_map = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0
        
        def build(left: int, right: int) -> TreeNode:
            if left > right:
                return None
            
            root_val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(root_val)
            
            mid = inorder_map[root_val]
            
            root.left = build(left, mid - 1)
            root.right = build(mid + 1, right)
            
            return root
            
        return build(0, len(inorder) - 1)""",
        "solution_explanation": "The first element in a preorder traversal is always the root. Once we know the root, we can find its position in the inorder traversal. Elements to the left of this position in the inorder array form the left subtree, and elements to the right form the right subtree. By tracking the boundaries (`left` and `right`) and using a hash map for $O(1)$ lookups in the inorder array, we can recursively build the tree in $O(N)$ time.",
        "when_to_use": "When you need to uniquely reconstruct a binary tree from traversal arrays. Remember that you need *inorder* plus either *preorder* or *postorder* to uniquely define a tree (preorder + postorder is not enough unless the tree is strictly full).",
        "test_cases": [
            {"call": "def ser(r):\n    return [] if not r else [r.val] + ser(r.left) + ser(r.right)\nser(Solution().build_tree([3,9,20,15,7], [9,3,15,20,7]))", "expected": "[3, 9, 20, 15, 7]"},
            {"call": "def ser(r):\n    return [] if not r else [r.val] + ser(r.left) + ser(r.right)\nser(Solution().build_tree([-1], [-1]))", "expected": "[-1]"},
            {"call": "def ser(r):\n    return [] if not r else [r.val] + ser(r.left) + ser(r.right)\nser(Solution().build_tree([1,2], [1,2]))", "expected": "[1, 2]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def reverse(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev""",
        "solution_explanation": "We maintain three pointers: `prev`, `curr`, and `next_temp`. In each iteration, we save the next node (`next_temp = curr.next`), reverse the current node's pointer (`curr.next = prev`), and then advance both `prev` and `curr` one step forward. The loop terminates when `curr` reaches `None`, at which point `prev` points to the new head of the reversed list.",
        "when_to_use": "A fundamental building block for many linked list problems (e.g., checking palindromes, reordering lists, reversing in groups of k). Always prefer the iterative approach over recursive for $O(1)$ extra space.",
        "test_cases": [
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().reverse(mk([1,2,3,4,5])))", "expected": "[5, 4, 3, 2, 1]"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().reverse(mk([1,2])))", "expected": "[2, 1]"},
            {"call": "def ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().reverse(None))", "expected": "[]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def has_cycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False""",
        "solution_explanation": "Floyd's Tortoise and Hare algorithm uses two pointers moving at different speeds. `slow` moves 1 step, while `fast` moves 2 steps. If there's a cycle, the fast pointer will eventually overlap with the slow pointer (the distance between them decreases by 1 in each step, guaranteeing they meet). If `fast` reaches the end (`None`), the list is acyclic.",
        "when_to_use": "To detect cycles in a linked list or sequence of states in $O(1)$ space. Also applicable for finding the duplicate number in an array when treating values as next-node pointers.",
        "test_cases": [
            {"call": "n1=ListNode(3); n2=ListNode(2); n3=ListNode(0); n4=ListNode(-4); n1.next=n2; n2.next=n3; n3.next=n4; n4.next=n2; Solution().has_cycle(n1)", "expected": "True"},
            {"call": "n1=ListNode(1); n2=ListNode(2); n1.next=n2; Solution().has_cycle(n1)", "expected": "False"},
            {"call": "Solution().has_cycle(None)", "expected": "False"}
        ]
    },
    {
        "solution_code": """class Solution:
    def find_middle(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow""",
        "solution_explanation": "By advancing `fast` by two steps and `slow` by one step, `slow` will reach exactly the midpoint when `fast` reaches the end of the list. For a list of even length, this standard formulation returns the second middle node (since `fast` lands on `None`).",
        "when_to_use": "When you need to split a linked list into two halves, such as during Merge Sort on a linked list, or verifying if a linked list is a palindrome.",
        "test_cases": [
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\nSolution().find_middle(mk([1,2,3,4,5])).val", "expected": "3"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\nSolution().find_middle(mk([1,2,3,4,5,6])).val", "expected": "4"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\nSolution().find_middle(mk([1])).val", "expected": "1"}
        ]
    },
    {
        "solution_code": """class Solution:
    def remove_nth(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        left = dummy
        right = head
        
        for _ in range(n):
            right = right.next
            
        while right:
            left = left.next
            right = right.next
            
        left.next = left.next.next
        return dummy.next""",
        "solution_explanation": "We use a two-pointer approach with a fixed gap of `n` nodes. By advancing `right` by `n` steps first, the distance between `left` and `right` becomes `n`. Then, moving both pointers at the same speed until `right` hits the end guarantees `left` will be exactly positioned at the node *before* the one we want to remove. Using a `dummy` node handles the edge case where the head itself needs to be removed.",
        "when_to_use": "Whenever you need to identify or modify an element based on its offset from the *end* of a singly linked list in a single pass.",
        "test_cases": [
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().remove_nth(mk([1,2,3,4,5]), 2))", "expected": "[1, 2, 3, 5]"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().remove_nth(mk([1]), 1))", "expected": "[]"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().remove_nth(mk([1,2]), 2))", "expected": "[2]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def merge(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        tail = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
            
        tail.next = l1 if l1 else l2
        return dummy.next""",
        "solution_explanation": "We maintain a `dummy` head to simplify the insertion logic and a `tail` pointer to build the new list. In each iteration, we compare the current nodes of both lists and append the smaller one to `tail.next`. Once one list is exhausted, we can just attach the remainder of the other list directly in $O(1)$ time, which avoids needing to traverse the rest.",
        "when_to_use": "The merge step of Merge Sort for linked lists. This logic extends easily to merging $K$ sorted lists by using a min-heap to pick the smallest element from the $K$ lists.",
        "test_cases": [
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge(mk([1,2,4]), mk([1,3,4])))", "expected": "[1, 1, 2, 3, 4, 4]"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge(None, None))", "expected": "[]"},
            {"call": "def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge(None, mk([0])))", "expected": "[0]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def is_valid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
                
        return not stack""",
        "solution_explanation": "Stacks operate on a Last-In-First-Out (LIFO) principle, which exactly aligns with the rules of nested brackets (the most recently opened bracket must be closed first). We iterate through the string, pushing opening brackets onto the stack. When we see a closing bracket, we pop from the stack and verify it's the matching opening bracket.",
        "when_to_use": "Parsing nested structures (e.g., JSON, HTML, expressions), matching brackets, or evaluating syntactic correctness.",
        "test_cases": [
            {"call": "Solution().is_valid('()[]{}')", "expected": "True"},
            {"call": "Solution().is_valid('(]')", "expected": "False"},
            {"call": "Solution().is_valid(']')", "expected": "False"},
            {"call": "Solution().is_valid('((()))')", "expected": "True"}
        ]
    },
    {
        "solution_code": """class Solution:
    def eval_rpn(self, tokens: list[str]) -> int:
        stack = []
        for token in tokens:
            if token in {"+", "-", "*", "/"}:
                b, a = stack.pop(), stack.pop()
                if token == "+": stack.append(a + b)
                elif token == "-": stack.append(a - b)
                elif token == "*": stack.append(a * b)
                else: stack.append(int(a / b))
            else:
                stack.append(int(token))
        return stack[0]""",
        "solution_explanation": "Reverse Polish Notation is designed to be evaluated using a stack without needing parentheses. Operands are pushed onto the stack. When an operator is encountered, it is applied to the top two operands popped from the stack (remembering that the first popped is the *right* operand), and the result is pushed back. Note: `int(a / b)` correctly truncates toward zero in Python.",
        "when_to_use": "When evaluating postfix expressions or designing simple expression evaluators / calculators.",
        "test_cases": [
            {"call": "Solution().eval_rpn(['2','1','+','3','*'])", "expected": "9"},
            {"call": "Solution().eval_rpn(['4','13','5','/','+'])", "expected": "6"},
            {"call": "Solution().eval_rpn(['10','6','9','3','+','-11','*','/','*','17','+','5','+'])", "expected": "22"}
        ]
    },
    {
        "solution_code": """class Solution:
    def next_greater(self, nums: list[int]) -> list[int]:
        res = [-1] * len(nums)
        stack = []
        
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] < val:
                idx = stack.pop()
                res[idx] = val
            stack.append(i)
            
        return res""",
        "solution_explanation": "We maintain a monotonically decreasing stack of *indices*. For each element, we check if it is greater than the element at the index currently on top of the stack. If it is, this current element is the \"next greater element\" for the element at the top index. We pop and update our result array until the stack top is greater, then push the current index. Each element is pushed and popped at most once, making it $O(N)$.",
        "when_to_use": "For \"next greater/smaller element\" queries across an array. Commonly used in daily temperatures, largest rectangle in histogram, and stock span problems.",
        "test_cases": [
            {"call": "Solution().next_greater([2,1,2,4,3])", "expected": "[4, 2, 4, -1, -1]"},
            {"call": "Solution().next_greater([1,3,2])", "expected": "[3, -1, -1]"},
            {"call": "Solution().next_greater([5,4,3,2,1])", "expected": "[-1, -1, -1, -1, -1]"}
        ]
    },
    {
        "solution_code": """from collections import deque

class Solution:
    def max_sliding_window(self, nums: list[int], k: int) -> list[int]:
        res = []
        q = deque()
        
        for i, val in enumerate(nums):
            while q and q[0] < i - k + 1:
                q.popleft()
                
            while q and nums[q[-1]] < val:
                q.pop()
                
            q.append(i)
            
            if i >= k - 1:
                res.append(nums[q[0]])
                
        return res""",
        "solution_explanation": "We maintain a monotonically decreasing doubly-linked queue (`deque`) of indices. The index of the absolute maximum in the current window is always at `q[0]`. As the window slides, we: 1) Remove indices from the left that are out of bounds. 2) Remove indices from the right whose values are smaller than the incoming value, as they can never be the maximum now that a larger, newer value exists. 3) Push the new index. 4) Record the maximum `nums[q[0]]`.",
        "when_to_use": "Whenever you need to query the maximum or minimum in a dynamically moving fixed-size window in $O(N)$ time.",
        "test_cases": [
            {"call": "Solution().max_sliding_window([1,3,-1,-3,5,3,6,7], 3)", "expected": "[3, 3, 5, 5, 6, 7]"},
            {"call": "Solution().max_sliding_window([1], 1)", "expected": "[1]"},
            {"call": "Solution().max_sliding_window([1,-1], 1)", "expected": "[1, -1]"},
            {"call": "Solution().max_sliding_window([7,2,4], 2)", "expected": "[7, 4]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]
        
        for start, end in intervals[1:]:
            last_end = res[-1][1]
            
            if start <= last_end:
                res[-1][1] = max(last_end, end)
            else:
                res.append([start, end])
                
        return res""",
        "solution_explanation": "First, sorting by the start time guarantees that intervals can only overlap if they are adjacent in the sorted array. As we iterate, if the current interval starts before or at the end of the last recorded interval, they overlap, and we greedily extend the last interval's end to the maximum of both. Otherwise, they are disjoint, and we append the new interval.",
        "when_to_use": "Unifying overlapping ranges or checking for overlap in scheduling/time problems.",
        "test_cases": [
            {"call": "Solution().merge([[1,3],[2,6],[8,10],[15,18]])", "expected": "[[1, 6], [8, 10], [15, 18]]"},
            {"call": "Solution().merge([[1,4],[4,5]])", "expected": "[[1, 5]]"},
            {"call": "Solution().merge([[1,4],[2,3]])", "expected": "[[1, 4]]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def insert(self, intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
        res = []
        i = 0
        n = len(intervals)
        
        while i < n and intervals[i][1] < new_interval[0]:
            res.append(intervals[i])
            i += 1
            
        while i < n and intervals[i][0] <= new_interval[1]:
            new_interval[0] = min(new_interval[0], intervals[i][0])
            new_interval[1] = max(new_interval[1], intervals[i][1])
            i += 1
        res.append(new_interval)
        
        while i < n:
            res.append(intervals[i])
            i += 1
            
        return res""",
        "solution_explanation": "The list is already sorted, so we can do this in $O(N)$ time instead of $O(N \\log N)$ sorting. The logic is handled in three distinct phases: 1) Add all intervals that strictly end before `new_interval` starts. 2) Greedily merge all intervals that overlap with `new_interval`, updating `new_interval`'s bounds. 3) Push the merged `new_interval`, followed by the remaining untouched intervals.",
        "when_to_use": "When injecting a single event/range into an already-sorted, non-overlapping collection of ranges.",
        "test_cases": [
            {"call": "Solution().insert([[1,3],[6,9]], [2,5])", "expected": "[[1, 5], [6, 9]]"},
            {"call": "Solution().insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8])", "expected": "[[1, 2], [3, 10], [12, 16]]"},
            {"call": "Solution().insert([], [5,7])", "expected": "[[5, 7]]"},
            {"call": "Solution().insert([[1,5]], [2,3])", "expected": "[[1, 5]]"}
        ]
    },
    {
        "solution_code": """class Solution:
    def find_min_arrows(self, points: list[list[int]]) -> int:
        if not points: return 0
        
        points.sort(key=lambda x: x[1])
        arrows = 1
        current_end = points[0][1]
        
        for start, end in points[1:]:
            if start > current_end:
                arrows += 1
                current_end = end
                
        return arrows""",
        "solution_explanation": "To burst balloons efficiently, we should shoot our arrows at the overlapping intersections. By sorting by the *end* coordinate, we ensure we process intervals in the order they must be dealt with. We place our first arrow greedily at the end of the first interval (`current_end`). Any subsequent interval that starts before or at `current_end` is burst by this arrow. As soon as an interval starts after `current_end`, we need a new arrow.",
        "when_to_use": "Finding the maximum number of non-overlapping intervals, or minimum points to cover all intervals (classic activity selection problem). Always sort by *end* time for activity selection.",
        "test_cases": [
            {"call": "Solution().find_min_arrows([[10,16],[2,8],[1,6],[7,12]])", "expected": "2"},
            {"call": "Solution().find_min_arrows([[1,2],[3,4],[5,6],[7,8]])", "expected": "4"},
            {"call": "Solution().find_min_arrows([[1,2],[2,3],[3,4],[4,5]])", "expected": "2"}
        ]
    },
    {
        "solution_code": """import heapq

class Solution:
    def kth_largest(self, nums: list[int], k: int) -> int:
        min_heap = []
        for num in nums:
            heapq.heappush(min_heap, num)
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        return min_heap[0]""",
        "solution_explanation": "A min-heap keeps the smallest element at the top. By maintaining a min-heap of exactly size `k`, we essentially hold the $k$ largest elements seen so far. When the heap exceeds size `k`, we pop the top element, which is the smallest of the $(k+1)$ largest elements, thus discarding it. At the end, the top of the heap is the smallest of the top $k$ elements—which precisely equals the $k$-th largest element in the array.",
        "when_to_use": "Finding the top $K$ largest or smallest elements in a stream of data or large array without fully sorting ($O(N \\log K)$ vs $O(N \\log N)$).",
        "test_cases": [
            {"call": "Solution().kth_largest([3,2,1,5,6,4], 2)", "expected": "5"},
            {"call": "Solution().kth_largest([3,2,3,1,2,4,5,5,6], 4)", "expected": "4"},
            {"call": "Solution().kth_largest([1], 1)", "expected": "1"}
        ]
    }
]

for item, enr in zip(batch, enrichment):
    item.update(enr)

with open('c:/Users/alexg/code/leet_practice/enriched_batch_30_44.json', 'w') as f:
    json.dump(batch, f, indent=2)

print("SUCCESS")

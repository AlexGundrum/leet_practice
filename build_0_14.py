import json

enrichments = {
    "drill_01_bs_standard_find_exact_target": {
        "solution_code": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return -1""",
        "solution_explanation": "The standard binary search algorithm maintains a search space defined by inclusive bounds `[l, r]`. The loop condition `l <= r` ensures we check the final single-element space. We calculate `mid = l + (r - l) // 2` to prevent potential integer overflow (though Python handles arbitrarily large integers, it's a good generic practice). If `nums[mid]` is less than `target`, the target must exist in the right half, so we safely exclude `mid` by setting `l = mid + 1`. If `nums[mid]` is greater, we exclude `mid` and search the left half with `r = mid - 1`.",
        "when_to_use": "Use when searching for an exact value in a sorted array.",
        "test_cases": [
            {"call": "Solution().search([-1,0,3,5,9,12], 9)", "expected": "4"},
            {"call": "Solution().search([-1,0,3,5,9,12], 2)", "expected": "-1"},
            {"call": "Solution().search([5], 5)", "expected": "0"},
            {"call": "Solution().search([5], 2)", "expected": "-1"}
        ]
    },
    "drill_02_bs_leftmost_occurrence": {
        "solution_code": """class Solution:
    def first_position(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        ans = -1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                ans = mid
                r = mid - 1  # Continue searching to the left
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return ans""",
        "solution_explanation": "To find the leftmost (or first) occurrence of a target, standard binary search is modified. When `nums[mid] == target`, instead of returning immediately, we record `mid` as a potential answer and narrow the search space to the left side by setting `r = mid - 1`. This ensures that if there are earlier occurrences of the target, we will find them. If not, the recorded `ans` remains our leftmost index.",
        "when_to_use": "Use when you need the lower bound or the first occurrence of duplicates in a sorted array.",
        "test_cases": [
            {"call": "Solution().first_position([5,7,7,8,8,10], 8)", "expected": "3"},
            {"call": "Solution().first_position([5,7,7,8,8,10], 6)", "expected": "-1"},
            {"call": "Solution().first_position([1,1,1,1], 1)", "expected": "0"}
        ]
    },
    "drill_03_bs_rightmost_occurrence": {
        "solution_code": """class Solution:
    def last_position(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        ans = -1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                ans = mid
                l = mid + 1  # Continue searching to the right
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return ans""",
        "solution_explanation": "Similar to the leftmost occurrence, finding the rightmost occurrence modifies the standard binary search by continuing the search after finding the target. Upon `nums[mid] == target`, we record `mid` and constrain the search space to the right by setting `l = mid + 1`. This greedily looks for subsequent occurrences of `target` on the right side of the array.",
        "when_to_use": "Use when finding the upper bound or the last occurrence of duplicates in a sorted array.",
        "test_cases": [
            {"call": "Solution().last_position([5,7,7,8,8,10], 8)", "expected": "4"},
            {"call": "Solution().last_position([5,7,7,8,8,10], 6)", "expected": "-1"},
            {"call": "Solution().last_position([1,1,1,1], 1)", "expected": "3"}
        ]
    },
    "drill_04_bs_rotated_sorted_array": {
        "solution_code": """class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                return mid
            
            # Left portion is strictly increasing
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    r = mid - 1
                else:
                    l = mid + 1
            # Right portion is strictly increasing
            else:
                if nums[mid] < target <= nums[r]:
                    l = mid + 1
                else:
                    r = mid - 1
        return -1""",
        "solution_explanation": "In a rotated sorted array, at least one half of the array (split at `mid`) will always be strictly increasing. We first identify which half is sorted by comparing `nums[l]` and `nums[mid]`. If the left side is sorted (`nums[l] <= nums[mid]`), we check if the `target` falls within its range. If it does, we discard the right half (`r = mid - 1`); otherwise, the target must be in the right half (`l = mid + 1`). If the left side is not sorted, the right side must be, and we apply the same logic symmetrically.",
        "when_to_use": "Use when searching for an element in an array that was originally sorted but has been cyclically shifted.",
        "test_cases": [
            {"call": "Solution().search([4,5,6,7,0,1,2], 0)", "expected": "4"},
            {"call": "Solution().search([4,5,6,7,0,1,2], 3)", "expected": "-1"},
            {"call": "Solution().search([1], 0)", "expected": "-1"},
            {"call": "Solution().search([5,1,3], 5)", "expected": "0"}
        ]
    },
    "drill_05_bs_on_answer_space_min_max_feasibility": {
        "solution_code": """class Solution:
    def min_capacity(self, weights: list[int], days: int) -> int:
        def can_ship(capacity: int) -> bool:
            days_needed = 1
            current_load = 0
            for w in weights:
                if current_load + w > capacity:
                    days_needed += 1
                    current_load = w
                else:
                    current_load += w
            return days_needed <= days

        l, r = max(weights), sum(weights)
        ans = r
        while l <= r:
            mid = l + (r - l) // 2
            if can_ship(mid):
                ans = mid
                r = mid - 1  # Try for a smaller capacity
            else:
                l = mid + 1  # Capacity is too small
        return ans""",
        "solution_explanation": "This solves a 'minimize the maximum' problem using Binary Search on the Answer Space. The minimum possible answer is `max(weights)` (we must be able to carry the heaviest single item) and the maximum is `sum(weights)` (carrying everything in one day). We define a monotonic condition function `can_ship(capacity)` which checks if a given capacity is feasible. By binary searching between `l` and `r`, we zero in on the smallest feasible capacity. When `can_ship(mid)` returns True, we record `mid` and try to find a smaller capacity (`r = mid - 1`). Otherwise, the capacity is insufficient, and we must increase it (`l = mid + 1`).",
        "when_to_use": "Use for problems asking to 'minimize the maximum' or 'maximize the minimum', or when the problem asks for a threshold value where values above/below it are uniformly valid/invalid.",
        "test_cases": [
            {"call": "Solution().min_capacity([1,2,3,4,5,6,7,8,9,10], 5)", "expected": "15"},
            {"call": "Solution().min_capacity([3,2,2,4,1,4], 3)", "expected": "6"},
            {"call": "Solution().min_capacity([1,2,3,1,1], 4)", "expected": "3"}
        ]
    },
    "drill_06_bfs_standard_graph_adjacency_list": {
        "solution_code": """from collections import deque

class Solution:
    def bfs(self, graph: dict, start: int) -> list[int]:
        if start not in graph and not graph: return []
        visited = set([start])
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return result""",
        "solution_explanation": "Breadth-First Search systematically explores a graph layer-by-layer. We use a queue (`collections.deque`) to process nodes in FIFO order. A `visited` set ensures we don't process a node multiple times, which prevents infinite loops in graphs with cycles. The invariant is that a node is marked as visited exactly when it is added to the queue, ensuring duplicate nodes aren't queued up multiple times in a single layer expansion.",
        "when_to_use": "Use when finding the shortest path in an unweighted graph, or to traverse a graph in expanding concentric layers.",
        "test_cases": [
            {"call": "Solution().bfs({0:[1,2],1:[2],2:[3],3:[1,2]}, 0)", "expected": "[0, 1, 2, 3]"},
            {"call": "Solution().bfs({0:[1,2],1:[3],2:[3],3:[]}, 0)", "expected": "[0, 1, 2, 3]"},
            {"call": "Solution().bfs({0:[]}, 0)", "expected": "[0]"}
        ]
    },
    "drill_07_bfs_level_order_tree_traversal": {
        "solution_code": """from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def level_order(self, root: TreeNode) -> list[list[int]]:
        if not root:
            return []
            
        queue = deque([root])
        result = []
        
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
            result.append(current_level)
            
        return result""",
        "solution_explanation": "Level-order traversal relies on BFS, but we must process nodes specifically by depth. We do this by capturing the `level_size = len(queue)` at the beginning of the while loop iteration. This size tells us exactly how many nodes exist at the current depth. We pop exactly `level_size` times, appending their children to the queue for the *next* depth level, effectively segmenting the queue into strict generation tiers.",
        "when_to_use": "Use when you need to process a tree level by level, or when searching for the shallowest node matching a certain condition.",
        "test_cases": [
            {
                "call": "n3=TreeNode(3); n9=TreeNode(9); n20=TreeNode(20); n15=TreeNode(15); n7=TreeNode(7); n3.left=n9; n3.right=n20; n20.left=n15; n20.right=n7; Solution().level_order(n3)",
                "expected": "[[3], [9, 20], [15, 7]]"
            },
            {
                "call": "Solution().level_order(TreeNode(1))",
                "expected": "[[1]]"
            },
            {
                "call": "Solution().level_order(None)",
                "expected": "[]"
            }
        ]
    },
    "drill_08_multi_source_bfs_grid": {
        "solution_code": """from collections import deque

class Solution:
    def oranges_rotting(self, grid: list[list[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0
        
        # Initialize queue with all rotten oranges (multi-source)
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    fresh_count += 1
                    
        if fresh_count == 0:
            return 0
                    
        minutes = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        while queue and fresh_count > 0:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh_count -= 1
                        queue.append((nr, nc))
                        
        return minutes if fresh_count == 0 else -1""",
        "solution_explanation": "Instead of starting BFS from a single node, Multi-Source BFS begins by enqueueing all initial \"sources\" (in this case, all rotten oranges at time 0). This causes the BFS layers to expand outward uniformly from multiple origins simultaneously. As we process a level, we increment our `minutes` tracker. Tracking `fresh_count` allows us to both short-circuit the execution efficiently, and to verify if any unreachable fresh oranges remain at the end.",
        "when_to_use": "Use when finding the shortest distance from *any* node in a set of sources to a target, or modeling simultaneous expansion like fires, diseases, or water flooding.",
        "test_cases": [
            {"call": "Solution().oranges_rotting([[2,1,1],[1,1,0],[0,1,1]])", "expected": "4"},
            {"call": "Solution().oranges_rotting([[2,1,1],[0,1,1],[1,0,1]])", "expected": "-1"},
            {"call": "Solution().oranges_rotting([[0,2]])", "expected": "0"}
        ]
    },
    "drill_09_dfs_iterative_explicit_stack": {
        "solution_code": """class Solution:
    def dfs(self, graph: dict, start: int) -> list[int]:
        stack = [start]
        visited = set()
        result = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                # Neighbors pushed in direct order -> popped in reverse.
                # Problem asks for 'last neighbor is popped and visited first'.
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        
        return result""",
        "solution_explanation": "Iterative DFS mimics recursion by using an explicit stack. Unlike BFS, we delay marking a node as visited until we actually pop it from the stack, because a node might be reached multiple times via different paths before we actually visit it. Pushing neighbors sequentially means the last neighbor pushed sits at the top of the stack, and thus will be evaluated first, going 'deep' rather than 'broad'.",
        "when_to_use": "Use when you need DFS but are constrained by recursion limits (e.g., extremely deep trees or massive graphs causing stack overflow), or when you prefer explicit state management.",
        "test_cases": [
            {"call": "Solution().dfs({0:[1,2],1:[3],2:[3],3:[]}, 0)", "expected": "[0, 2, 3, 1]"},
            {"call": "Solution().dfs({0:[1],1:[2],2:[]}, 0)", "expected": "[0, 1, 2]"}
        ]
    },
    "drill_10_dfs_recursive_graph_track_visited": {
        "solution_code": """class Solution:
    def dfs(self, graph: dict, start: int) -> list[int]:
        visited = set()
        result = []
        
        def explore(node):
            if node in visited:
                return
            visited.add(node)
            result.append(node)
            for neighbor in graph.get(node, []):
                explore(neighbor)
                
        explore(start)
        return result""",
        "solution_explanation": "Recursive DFS relies on the call stack to traverse deeply into a graph. When a node is evaluated, it is immediately marked as visited to block cycles. Then, the algorithm explores each of its neighbors completely before returning to explore the next neighbor. This results in the natural topological dive behavior of depth-first search, producing a straightforward and elegant implementation.",
        "when_to_use": "Use for standard backtracking, tree traversals (pre/in/post-order), path finding, or cycle detection where call stack limitations are not a concern.",
        "test_cases": [
            {"call": "Solution().dfs({0:[1,2],1:[3],2:[3],3:[]}, 0)", "expected": "[0, 1, 3, 2]"},
            {"call": "Solution().dfs({0:[1,2],1:[2,3],2:[3],3:[]}, 0)", "expected": "[0, 1, 2, 3]"}
        ]
    },
    "drill_11_connected_components_undirected": {
        "solution_code": """class Solution:
    def count_components(self, n: int, edges: list[list[int]]) -> int:
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            
        visited = set()
        components = 0
        
        def dfs(node):
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor)
                    
        for i in range(n):
            if i not in visited:
                components += 1
                visited.add(i)
                dfs(i)
                
        return components""",
        "solution_explanation": "To find connected components, we sweep through all nodes in the graph. Whenever we encounter an unvisited node, it represents a new, undiscovered component. We increment our component counter, and then dispatch a DFS (or BFS) to mark the entirety of that connected component as visited. By the time the loop finishes, we will have counted precisely the number of isolated subgraphs.",
        "when_to_use": "Use when identifying clusters, islands, or isolated groups within a network. (Note: Union-Find is another excellent approach for this).",
        "test_cases": [
            {"call": "Solution().count_components(5, [[0,1],[1,2],[3,4]])", "expected": "2"},
            {"call": "Solution().count_components(4, [[0,1],[2,3],[1,2]])", "expected": "1"},
            {"call": "Solution().count_components(3, [])", "expected": "3"}
        ]
    },
    "drill_12_cycle_detection_directed_graph_dfs_3_color": {
        "solution_code": """class Solution:
    def has_cycle(self, n: int, edges: list[list[int]]) -> bool:
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            
        # 0 = unvisited, 1 = visiting (in current path), 2 = visited (completely processed)
        state = [0] * n
        
        def dfs(node):
            if state[node] == 1:
                return True # Found a back-edge indicating a cycle
            if state[node] == 2:
                return False
                
            state[node] = 1
            for neighbor in adj[node]:
                if dfs(neighbor):
                    return True
            state[node] = 2
            return False
            
        for i in range(n):
            if state[i] == 0:
                if dfs(i):
                    return True
        return False""",
        "solution_explanation": "Cycle detection in directed graphs uses a '3-color' DFS. A node can be unvisited (0), actively visiting on the current recursion path (1), or fully visited and verified cycle-free (2). If we ever encounter a node with state 1, it means we looped back to a node currently in our ancestor path, representing a back-edge and therefore a cycle. State 2 guarantees we don't redundantly process or falsely flag cross-edges as cycles.",
        "when_to_use": "Use for resolving deadlocks, checking for circular dependencies, or validating if a directed graph can be topologically sorted.",
        "test_cases": [
            {"call": "Solution().has_cycle(4, [[0,1],[1,2],[2,3],[3,1]])", "expected": "True"},
            {"call": "Solution().has_cycle(3, [[0,1],[1,2]])", "expected": "False"},
            {"call": "Solution().has_cycle(2, [[0,1],[1,0]])", "expected": "True"}
        ]
    },
    "drill_13_bipartite_check_bfs_2_coloring": {
        "solution_code": """from collections import deque

class Solution:
    def is_bipartite(self, graph: list[list[int]]) -> bool:
        n = len(graph)
        color = [-1] * n
        
        for i in range(n):
            if color[i] == -1:
                queue = deque([i])
                color[i] = 0
                
                while queue:
                    node = queue.popleft()
                    for neighbor in graph[node]:
                        if color[neighbor] == -1:
                            # Color neighbor with the opposite color
                            color[neighbor] = 1 - color[node]
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            # Conflict found
                            return False
        return True""",
        "solution_explanation": "A graph is bipartite if its nodes can be colored with 2 colors such that no two adjacent nodes share the same color. We iterate through the graph (handling disconnected components). For each uncolored component, we BFS and alternate colors (`1 - color[node]`) layer by layer. If we ever discover an adjacent node that is already colored with the *same* color as the current node, a 2-coloring is impossible.",
        "when_to_use": "Use to check if a graph can be split into two mutually exclusive independent sets. Equivalent to checking if a graph contains any cycles of odd length.",
        "test_cases": [
            {"call": "Solution().is_bipartite([[1,3],[0,2],[1,3],[0,2]])", "expected": "True"},
            {"call": "Solution().is_bipartite([[1,2,3],[0,2],[0,1,3],[0,2]])", "expected": "False"}
        ]
    },
    "drill_14_bfs_on_grid_4_directional_flood_fill": {
        "solution_code": """from collections import deque

class Solution:
    def flood_fill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
        original_color = image[sr][sc]
        if original_color == color:
            return image
            
        ROWS, COLS = len(image), len(image[0])
        queue = deque([(sr, sc)])
        image[sr][sc] = color
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and image[nr][nc] == original_color:
                    image[nr][nc] = color
                    queue.append((nr, nc))
                    
        return image""",
        "solution_explanation": "Flood fill starts at a root pixel and recursively (or iteratively via BFS) overrides contiguous neighbor pixels sharing the original color. To prevent an infinite loop, we immediately abort if the `original_color` matches the target `color`. Otherwise, BFS traverses the grid. We mutate the grid in-place to the target color right as we add to the queue; this acts inherently as our 'visited' flag.",
        "when_to_use": "Use for paint-bucket tool behavior, resolving boundaries of a specific region in a grid, or solving classic island-traversal problems.",
        "test_cases": [
            {"call": "Solution().flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)", "expected": "[[2, 2, 2], [2, 2, 0], [2, 0, 1]]"},
            {"call": "Solution().flood_fill([[0,0,0],[0,0,0]], 0, 0, 0)", "expected": "[[0, 0, 0], [0, 0, 0]]"}
        ]
    },
    "drill_15_topo_sort_kahn_s_algorithm_bfs_in_degree": {
        "solution_code": """from collections import deque

class Solution:
    def topo_sort(self, n: int, edges: list[list[int]]) -> list[int]:
        adj = {i: [] for i in range(n)}
        in_degree = [0] * n
        
        for u, v in edges:
            adj[u].append(v)
            in_degree[v] += 1
            
        # Initialize queue with nodes having 0 dependencies
        queue = deque([i for i in range(n) if in_degree[i] == 0])
        topo_order = []
        
        while queue:
            node = queue.popleft()
            topo_order.append(node)
            
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(topo_order) == n:
            return topo_order
        return []  # Cycle detected, valid sort impossible""",
        "solution_explanation": "Kahn's Algorithm determines topological ordering by peeling away layers of dependencies. We track the `in_degree` (number of incoming edges) for all nodes. Nodes with an `in_degree` of 0 have no dependencies and are pushed to a queue. Processing a node means appending it to the ordered list and removing its outgoing edges by decrementing the `in_degree` of its neighbors. If a neighbor reaches 0, it is now \"freed\" and enters the queue. If cycles exist, those nodes' in-degrees will never reach 0, meaning `len(topo_order) < n`.",
        "when_to_use": "Use when finding a valid sequence of tasks given a set of dependencies (e.g. course scheduling, build systems).",
        "test_cases": [
            {"call": "r=Solution().topo_sort(6,[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]); len(r)==6 and r.index(5)<r.index(2) and r.index(2)<r.index(3) and r.index(4)<r.index(1)", "expected": "True"},
            {"call": "Solution().topo_sort(2, [[1,0]])", "expected": "[1, 0]"}
        ]
    }
}

if __name__ == "__main__":
    with open('c:/Users/alexg/code/leet_practice/algorithms.json', 'r') as f:
        data = json.load(f)
        
    subset = data[0:15]
    for item in subset:
        uid = item['id']
        if uid in enrichments:
            item.update(enrichments[uid])
        else:
            print(f"Warning: {uid} not in enrichments")
            
    with open('c:/Users/alexg/code/leet_practice/enriched_batch_0_14.json', 'w') as f:
        json.dump(subset, f, indent=2)

    print("Success")

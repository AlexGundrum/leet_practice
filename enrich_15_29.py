import json

def run():
    with open('c:/Users/alexg/code/leet_practice/algorithms.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    batch = data[15:30]
    
    # 0: drill_16_topo_sort_dfs_postorder
    batch[0]['solution_code'] = """class Solution:
    def topo_sort(self, n: int, edges: list[list[int]]) -> list[int]:
        adj = {i: [] for i in range(n)}
        for u, v in edges:
            adj[u].append(v)
            
        visited = [0] * n # 0: unvisited, 1: visiting, 2: visited
        order = []
        
        def dfs(node):
            if visited[node] == 1:
                return False
            if visited[node] == 2:
                return True
            
            visited[node] = 1
            for neighbor in adj[node]:
                if not dfs(neighbor):
                    return False
            visited[node] = 2
            order.append(node)
            return True
            
        for i in range(n):
            if visited[i] == 0:
                if not dfs(i):
                    return []
                    
        return order[::-1]"""
    batch[0]['solution_explanation'] = "We perform DFS to build a topological ordering. The key is to keep track of node states: 'unvisited' (0), 'visiting' (1), and 'visited' (2). If we encounter a node in the 'visiting' state, it means we have found a cycle, which prevents a valid topological sort. After fully exploring all descendants of a node, we mark it as 'visited' and add it to our postorder list. Reversing this postorder list yields the valid topological order."
    batch[0]['when_to_use'] = "Use Topological Sort when you need to resolve dependencies or find a valid sequence of tasks in a Directed Acyclic Graph (DAG) (e.g., course scheduling, build systems)."
    batch[0]['test_cases'] = [
        {"call": "Solution().topo_sort(4, [[1,0],[2,0],[3,1],[3,2]])", "expected": "[3, 1, 2, 0]"},
        {"call": "Solution().topo_sort(2, [[1,0],[0,1]])", "expected": "[]"},
        {"call": "Solution().topo_sort(3, [[0,1],[1,2]])", "expected": "[0, 1, 2]"}
    ]
    
    # 1: drill_17_dijkstra_s_min_heap_single_source
    batch[1]['solution_code'] = """import heapq

class Solution:
    def dijkstra(self, n: int, edges: list[list[int]], src: int) -> list[int]:
        adj = {i: [] for i in range(n)}
        for u, v, w in edges:
            adj[u].append((v, w))
            
        dist = [float('inf')] * n
        dist[src] = 0
        min_heap = [(0, src)] # (distance, node)
        
        while min_heap:
            d, node = heapq.heappop(min_heap)
            
            if d > dist[node]:
                continue
                
            for neighbor, weight in adj[node]:
                new_dist = d + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(min_heap, (new_dist, neighbor))
                    
        return [d if d != float('inf') else -1 for d in dist]"""
    batch[1]['solution_explanation'] = "Dijkstra's algorithm finds the shortest path from a single source node to all other nodes in a graph with non-negative edge weights. It uses a min-heap to always explore the closest reachable node next. The condition `d > dist[node]` is crucial to skip processing a node if we already found a shorter path to it before popping this particular entry from the heap. We update neighbors and push them to the heap if a shorter path is found."
    batch[1]['when_to_use'] = "Use Dijkstra's when you need the shortest path from a single source to all other nodes (or a specific target) in a graph with NO negative edge weights."
    batch[1]['test_cases'] = [
        {"call": "Solution().dijkstra(5, [[0,1,2],[0,2,4],[1,2,1],[1,3,7],[2,4,3],[3,4,1]], 0)", "expected": "[0, 2, 3, 9, 6]"},
        {"call": "Solution().dijkstra(3, [[0,1,5]], 0)", "expected": "[0, 5, -1]"},
        {"call": "Solution().dijkstra(1, [], 0)", "expected": "[0]"}
    ]

    # 2: drill_18_bellman_ford_handles_negative_weights
    batch[2]['solution_code'] = """class Solution:
    def bellman_ford(self, n: int, edges: list[list[int]], src: int) -> list[int]:
        dist = [float('inf')] * n
        dist[src] = 0
        
        for _ in range(n - 1):
            for u, v, w in edges:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    
        # Check for negative weight cycles
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                return [] # Negative cycle detected
                
        return [d if d != float('inf') else -1 for d in dist]"""
    batch[2]['solution_explanation'] = "Bellman-Ford finds the shortest paths from a single source to all nodes, handling negative edge weights. It relaxes all edges `n-1` times, which is the maximum number of edges in a simple shortest path. If we can still relax an edge on the `n`th iteration, the graph contains a negative weight cycle, and shortest paths are undefined (returning empty). The check `dist[u] != inf` prevents adding weights to unreachable nodes."
    batch[2]['when_to_use'] = "Use Bellman-Ford for single-source shortest path problems when the graph may contain negative edge weights, or when you explicitly need to detect negative weight cycles."
    batch[2]['test_cases'] = [
        {"call": "Solution().bellman_ford(3, [[0,1,2],[1,2,-5],[0,2,1]], 0)", "expected": "[0, 2, -3]"},
        {"call": "Solution().bellman_ford(3, [[0,1,2],[1,2,-5],[2,0,1]], 0)", "expected": "[]"},
        {"call": "Solution().bellman_ford(4, [[0,1,1],[1,2,1],[2,3,1]], 0)", "expected": "[0, 1, 2, 3]"}
    ]

    # 3: drill_19_floyd_warshall_all_pairs_shortest_path
    batch[3]['solution_code'] = """class Solution:
    def floyd_warshall(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        dist = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
            
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)
            
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                        
        # Replace inf with -1
        return [[d if d != float('inf') else -1 for d in row] for row in dist]"""
    batch[3]['solution_explanation'] = "Floyd-Warshall is a dynamic programming algorithm for the All-Pairs Shortest Path problem. The state transition evaluates if a path from `i` to `j` is shorter when routed through an intermediate node `k`. We iteratively allow nodes `0` to `n-1` as intermediate nodes. The time complexity is O(V^3), making it suitable only for small graphs."
    batch[3]['when_to_use'] = "Use Floyd-Warshall when you need the shortest path between ALL pairs of nodes in a small graph (typically V <= 400). Also handles negative weights but not negative cycles."
    batch[3]['test_cases'] = [
        {"call": "Solution().floyd_warshall(4, [[0,1,3],[1,2,1],[2,3,2],[0,3,10]])", "expected": "[[0, 3, 4, 6], [-1, 0, 1, 3], [-1, -1, 0, 2], [-1, -1, -1, 0]]"},
        {"call": "Solution().floyd_warshall(3, [[0,1,1],[1,2,-1],[0,2,5]])", "expected": "[[0, 1, 0], [-1, 0, -1], [-1, -1, 0]]"},
        {"call": "Solution().floyd_warshall(2, [[0,1,2],[1,0,3]])", "expected": "[[0, 2], [3, 0]]"}
    ]

    # 4: drill_20_prim_s_mst_min_heap_adjacency_list
    batch[4]['solution_code'] = """import heapq

class Solution:
    def prims(self, n: int, edges: list[list[int]]) -> int:
        adj = {i: [] for i in range(n)}
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
            
        min_heap = [(0, 0)] # (weight, node)
        visited = set()
        total_weight = 0
        
        while min_heap and len(visited) < n:
            weight, node = heapq.heappop(min_heap)
            
            if node in visited:
                continue
                
            visited.add(node)
            total_weight += weight
            
            for neighbor, edge_weight in adj[node]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (edge_weight, neighbor))
                    
        return total_weight if len(visited) == n else -1"""
    batch[4]['solution_explanation'] = "Prim's algorithm builds a Minimum Spanning Tree (MST) by starting from an arbitrary node (0) and greedily expanding the tree. It uses a min-heap to always pick the smallest weight edge that connects a node in the tree to a node outside the tree. A `visited` set ensures we don't form cycles. If the graph is disconnected, `len(visited)` won't reach `n`, so we return -1."
    batch[4]['when_to_use'] = "Use Prim's algorithm for finding the Minimum Spanning Tree in dense undirected graphs, where E is closer to V^2."
    batch[4]['test_cases'] = [
        {"call": "Solution().prims(4, [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]])", "expected": "4"},
        {"call": "Solution().prims(3, [[0,1,5]])", "expected": "-1"},
        {"call": "Solution().prims(1, [])", "expected": "0"}
    ]

    # 5: drill_21_kruskal_s_mst_sort_edges_union_find
    batch[5]['solution_code'] = """class Solution:
    def kruskals(self, n: int, edges: list[list[int]]) -> int:
        parent = list(range(n))
        rank = [0] * n
        
        def find(i):
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]
            
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                if rank[root_i] < rank[root_j]:
                    parent[root_i] = root_j
                elif rank[root_i] > rank[root_j]:
                    parent[root_j] = root_i
                else:
                    parent[root_j] = root_i
                    rank[root_i] += 1
                return True
            return False
            
        edges.sort(key=lambda x: x[2])
        total_weight = 0
        edges_used = 0
        
        for u, v, w in edges:
            if union(u, v):
                total_weight += w
                edges_used += 1
                if edges_used == n - 1:
                    break
                    
        return total_weight if edges_used == n - 1 and n > 0 else (0 if n == 1 else -1)"""
    batch[5]['solution_explanation'] = "Kruskal's algorithm finds the Minimum Spanning Tree by sorting all edges by weight, and then adding them one by one to the tree. It uses a Disjoint Set Union (Union-Find) data structure to keep track of connected components and efficiently check if adding an edge would create a cycle (if both endpoints have the same root). It stops early once `n - 1` edges are added."
    batch[5]['when_to_use'] = "Use Kruskal's algorithm to find the Minimum Spanning Tree in sparse graphs, or when edges are already sorted or easily sortable."
    batch[5]['test_cases'] = [
        {"call": "Solution().kruskals(4, [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]])", "expected": "4"},
        {"call": "Solution().kruskals(4, [[0,1,1],[2,3,1]])", "expected": "-1"},
        {"call": "Solution().kruskals(1, [])", "expected": "0"}
    ]

    # 6: drill_22_union_find_path_compression_union_by_rank
    batch[6]['solution_code'] = """class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            self.count -= 1
            return True
        return False

class Solution:
    def count_components(self, n: int, edges: list[list[int]]) -> int:
        uf = UnionFind(n)
        for u, v in edges:
            uf.union(u, v)
        return uf.count"""
    batch[6]['solution_explanation'] = "Union-Find is implemented with Path Compression (`find` flattens the tree structure) and Union by Rank (always attach the smaller tree under the root of the deeper tree). This bounds the time complexity to almost O(1) per operation (inverse Ackermann function). By keeping a `count` variable that decrements on successful unions, we can track the number of connected components efficiently."
    batch[6]['when_to_use'] = "Use Union-Find when dynamically connecting components, detecting cycles in undirected graphs, or finding the number of connected components."
    batch[6]['test_cases'] = [
        {"call": "Solution().count_components(5, [[0,1],[1,2],[3,4]])", "expected": "2"},
        {"call": "Solution().count_components(5, [[0,1],[1,2],[2,3],[3,4]])", "expected": "1"},
        {"call": "Solution().count_components(3, [])", "expected": "3"}
    ]

    # 7: drill_23_tarjan_s_bridges_critical_connections
    batch[7]['solution_code'] = """class Solution:
    def critical_connections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        adj = {i: [] for i in range(n)}
        for u, v in connections:
            adj[u].append(v)
            adj[v].append(u)
            
        discovery = [-1] * n
        lowest = [-1] * n
        self.time = 0
        bridges = []
        
        def dfs(node, parent):
            discovery[node] = lowest[node] = self.time
            self.time += 1
            
            for neighbor in adj[node]:
                if neighbor == parent:
                    continue
                if discovery[neighbor] == -1: # unvisited
                    dfs(neighbor, node)
                    lowest[node] = min(lowest[node], lowest[neighbor])
                    if lowest[neighbor] > discovery[node]:
                        bridges.append([node, neighbor])
                else:
                    lowest[node] = min(lowest[node], discovery[neighbor])
                    
        dfs(0, -1)
        return bridges"""
    batch[7]['solution_explanation'] = "Tarjan's algorithm finds bridges (critical connections) in an undirected graph. We track the `discovery` time and the `lowest` reachable discovery time for each node. During DFS, if the lowest reachable time of a neighbor `v` from node `u` is strictly greater than `u`'s discovery time (`lowest[v] > discovery[u]`), it means `v` has no back-edge to `u` or its ancestors. Thus, `(u, v)` is the only way to reach `v` and is a bridge."
    batch[7]['when_to_use'] = "Use Tarjan's bridge-finding algorithm to identify critical paths or single points of failure in an undirected network (e.g., removing the edge would split the graph)."
    batch[7]['test_cases'] = [
        {"call": "sorted([sorted(e) for e in Solution().critical_connections(4, [[0,1],[1,2],[2,0],[1,3]])])", "expected": "[[1, 3]]"},
        {"call": "sorted([sorted(e) for e in Solution().critical_connections(2, [[0,1]])])", "expected": "[[0, 1]]"},
        {"call": "sorted([sorted(e) for e in Solution().critical_connections(5, [[0,1],[1,2],[2,0],[1,3],[3,4],[4,1]])])", "expected": "[]"}
    ]

    # 8: drill_24_preorder_traversal_iterative_root_left_right
    batch[8]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def preorder(self, root: TreeNode) -> list[int]:
        if not root:
            return []
        
        stack = [root]
        res = []
        
        while stack:
            node = stack.pop()
            res.append(node.val)
            # Push right child first so left child is popped first (LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
                
        return res"""
    batch[8]['solution_explanation'] = "Iterative preorder traversal processes nodes in Root -> Left -> Right order. We use a stack initialized with the root. On each step, we pop a node, visit it (append value), and then push its right child followed by its left child. Pushing the right child first ensures the left child is at the top of the stack and processed next, preserving the Preorder sequence."
    batch[8]['when_to_use'] = "Use iterative preorder when you need to serialize a tree, copy a tree structure, or generally avoid recursive stack overflow on deep trees."
    batch[8]['test_cases'] = [
        {"call": "r=TreeNode(1); r.right=TreeNode(2); r.right.left=TreeNode(3); Solution().preorder(r)", "expected": "[1, 2, 3]"},
        {"call": "Solution().preorder(None)", "expected": "[]"},
        {"call": "r=TreeNode(1); r.left=TreeNode(2); r.right=TreeNode(3); Solution().preorder(r)", "expected": "[1, 2, 3]"}
    ]

    # 9: drill_25_inorder_traversal_iterative_left_root_right
    batch[9]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def inorder(self, root: TreeNode) -> list[int]:
        stack = []
        res = []
        curr = root
        
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
                
            curr = stack.pop()
            res.append(curr.val)
            curr = curr.right
            
        return res"""
    batch[9]['solution_explanation'] = "Iterative inorder traversal (Left -> Root -> Right). We traverse as far left as possible, pushing nodes onto the stack. When we reach a null node, we pop from the stack, visit the node, and then move to its right subtree. This perfectly mimics the call stack of a recursive inorder traversal."
    batch[9]['when_to_use'] = "Use iterative inorder traversal for Binary Search Trees (BSTs) when you need to process elements in sorted order efficiently without recursion."
    batch[9]['test_cases'] = [
        {"call": "r=TreeNode(1); r.right=TreeNode(2); r.right.left=TreeNode(3); Solution().inorder(r)", "expected": "[1, 3, 2]"},
        {"call": "Solution().inorder(None)", "expected": "[]"},
        {"call": "r=TreeNode(2); r.left=TreeNode(1); r.right=TreeNode(3); Solution().inorder(r)", "expected": "[1, 2, 3]"}
    ]

    # 10: drill_26_postorder_traversal_iterative_left_right_root
    batch[10]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorder(self, root: TreeNode) -> list[int]:
        if not root:
            return []
            
        stack = [root]
        res = []
        
        while stack:
            node = stack.pop()
            res.append(node.val)
            # Push left child first so right child is popped first
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
                
        # Result is Root -> Right -> Left. Reverse to get Left -> Right -> Root
        return res[::-1]"""
    batch[10]['solution_explanation'] = "Iterative postorder (Left -> Right -> Root) is trickier. A clean way is to generate a modified preorder traversal (Root -> Right -> Left) by reversing the push order of children. Then, reverse the entire resulting list to get Left -> Right -> Root. This avoids complex state tracking on the stack."
    batch[10]['when_to_use'] = "Use iterative postorder when you need to process children before their parents (e.g., deleting a tree, evaluating expression trees, aggregating values from subtrees) without recursion."
    batch[10]['test_cases'] = [
        {"call": "r=TreeNode(1); r.right=TreeNode(2); r.right.left=TreeNode(3); Solution().postorder(r)", "expected": "[3, 2, 1]"},
        {"call": "Solution().postorder(None)", "expected": "[]"},
        {"call": "r=TreeNode(1); r.left=TreeNode(2); r.right=TreeNode(3); Solution().postorder(r)", "expected": "[2, 3, 1]"}
    ]

    # 11: drill_27_lca_binary_tree_dfs_recursive
    batch[11]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lca(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if not root or root == p or root == q:
            return root
            
        left = self.lca(root.left, p, q)
        right = self.lca(root.right, p, q)
        
        if left and right:
            return root
            
        return left if left else right"""
    batch[11]['solution_explanation'] = "This recursive DFS searches for nodes `p` and `q`. The base case returns the node if it equals `p`, `q`, or null. We search both the left and right subtrees. If a node receives non-null returns from both children, it means `p` and `q` are on opposite sides, making this node their Lowest Common Ancestor. If only one side is non-null, both targets are located in that subtree, so we propagate the result upwards."
    batch[11]['when_to_use'] = "Use this to find the Lowest Common Ancestor in a standard Binary Tree. If the tree is a Binary Search Tree (BST), use the BST properties to route left/right instead for O(H) time without full traversal."
    batch[11]['test_cases'] = [
        {"call": "r=TreeNode(3); r.left=TreeNode(5); r.right=TreeNode(1); Solution().lca(r, r.left, r.right).val", "expected": "3"},
        {"call": "r=TreeNode(1); r.left=TreeNode(2); Solution().lca(r, r, r.left).val", "expected": "1"},
        {"call": "r=TreeNode(1); p=TreeNode(2); q=TreeNode(3); r.left=p; r.right=q; p.left=TreeNode(4); Solution().lca(r, p.left, q).val", "expected": "1"}
    ]

    # 12: drill_28_validate_bst_dfs_with_min_max_bounds
    batch[12]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def is_valid_bst(self, root: TreeNode) -> bool:
        def dfs(node, lower, upper):
            if not node:
                return True
                
            if node.val <= lower or node.val >= upper:
                return False
                
            return dfs(node.left, lower, node.val) and dfs(node.right, node.val, upper)
            
        return dfs(root, float('-inf'), float('inf'))"""
    batch[12]['solution_explanation'] = "To validate a BST, every node's value must strictly fall within a valid range `(lower, upper)`. We traverse top-down, passing these bounds. When we go to the left child, the current node's value becomes the new `upper` bound. When we go to the right child, the current node's value becomes the new `lower` bound. A violation immediately returns False."
    batch[12]['when_to_use'] = "Use this min/max bounding technique to validate BST properties. It's cleaner and safer than checking against previously visited nodes in an inorder traversal."
    batch[12]['test_cases'] = [
        {"call": "r=TreeNode(2); r.left=TreeNode(1); r.right=TreeNode(3); Solution().is_valid_bst(r)", "expected": "True"},
        {"call": "r=TreeNode(5); r.left=TreeNode(1); r.right=TreeNode(4); r.right.left=TreeNode(3); r.right.right=TreeNode(6); Solution().is_valid_bst(r)", "expected": "False"},
        {"call": "r=TreeNode(2); r.left=TreeNode(2); Solution().is_valid_bst(r)", "expected": "False"}
    ]

    # 13: drill_29_diameter_of_binary_tree_dfs_postorder
    batch[13]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameter(self, root: TreeNode) -> int:
        self.max_diam = 0
        
        def dfs(node):
            if not node:
                return 0
                
            left_depth = dfs(node.left)
            right_depth = dfs(node.right)
            
            # The diameter passing through this node is left_depth + right_depth
            self.max_diam = max(self.max_diam, left_depth + right_depth)
            
            # Return the depth of the longest path going down
            return 1 + max(left_depth, right_depth)
            
        dfs(root)
        return self.max_diam"""
    batch[13]['solution_explanation'] = "We compute the longest path recursively using postorder traversal. A node's contribution to its parent's depth is `1 + max(left_depth, right_depth)`. However, the longest path (diameter) might not pass through the root, but form an inverted 'V' at any node. Thus, at each node, we update a global maximum with `left_depth + right_depth`."
    batch[13]['when_to_use'] = "Use this pattern (Tree DP / returning depth while mutating a global answer) for tree problems involving paths that can form an inverted 'V' at any subtree root."
    batch[13]['test_cases'] = [
        {"call": "r=TreeNode(1); r.left=TreeNode(2); r.right=TreeNode(3); r.left.left=TreeNode(4); r.left.right=TreeNode(5); Solution().diameter(r)", "expected": "3"},
        {"call": "r=TreeNode(1); r.left=TreeNode(2); Solution().diameter(r)", "expected": "1"},
        {"call": "r=TreeNode(1); Solution().diameter(r)", "expected": "0"}
    ]

    # 14: drill_30_max_path_sum_in_binary_tree_tree_dp
    batch[14]['solution_code'] = """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def max_path_sum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')
        
        def dfs(node):
            if not node:
                return 0
                
            # Ignore paths with negative sums
            left_max = max(0, dfs(node.left))
            right_max = max(0, dfs(node.right))
            
            # Update the global max with the path that forms an inverted 'V'
            self.max_sum = max(self.max_sum, node.val + left_max + right_max)
            
            # Return the max straight path sum extendable to the parent
            return node.val + max(left_max, right_max)
            
        dfs(root)
        return self.max_sum"""
    batch[14]['solution_explanation'] = "This is Tree DP. For each node, we recursively find the maximum path sum in its left and right subtrees. We use `max(0, ...)` to ignore negative paths (as they would only reduce the sum). The local max path sum through the current node is `node.val + left_max + right_max`. However, a path can only branch once, so when returning to the parent, we can only supply a single straight branch: `node.val + max(left_max, right_max)`."
    batch[14]['when_to_use'] = "Use this logic for advanced Tree DP problems where a path can change direction exactly once (at the highest node of the path) but must be a straight line when viewed from above."
    batch[14]['test_cases'] = [
        {"call": "r=TreeNode(-10); r.left=TreeNode(9); r.right=TreeNode(20); r.right.left=TreeNode(15); r.right.right=TreeNode(7); Solution().max_path_sum(r)", "expected": "42"},
        {"call": "r=TreeNode(1); r.left=TreeNode(2); r.right=TreeNode(3); Solution().max_path_sum(r)", "expected": "6"},
        {"call": "r=TreeNode(-3); Solution().max_path_sum(r)", "expected": "-3"}
    ]

    with open('c:/Users/alexg/code/leet_practice/enriched_batch_15_29.json', 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2)

if __name__ == '__main__':
    run()

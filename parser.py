import json
import re

md = r"""
### 01 · BS — standard (find exact target)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        pass
```

**Inputs given:**
```
nums = [-1, 0, 3, 5, 9, 12]
target = 9
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().search([-1,0,3,5,9,12], 9)` | `5` |
| `Solution().search([-1,0,3,5,9,12], 2)` | `-1` |
| `Solution().search([5], 5)` | `0` |

---

### 02 · BS — leftmost occurrence
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def first_position(self, nums: list[int], target: int) -> int:
        pass
```

**Inputs given:**
```
nums = [5, 7, 7, 8, 8, 10]
target = 8
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().first_position([5,7,7,8,8,10], 8)` | `3` |
| `Solution().first_position([5,7,7,8,8,10], 6)` | `-1` |
| `Solution().first_position([1,1,1,1], 1)` | `0` |

---

### 03 · BS — rightmost occurrence
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def last_position(self, nums: list[int], target: int) -> int:
        pass
```

**Inputs given:**
```
nums = [5, 7, 7, 8, 8, 10]
target = 8
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().last_position([5,7,7,8,8,10], 8)` | `4` |
| `Solution().last_position([5,7,7,8,8,10], 6)` | `-1` |
| `Solution().last_position([1,1,1,1], 1)` | `3` |

---

### 04 · BS — rotated sorted array
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        pass
```

**Inputs given:**
```
nums = [4, 5, 6, 7, 0, 1, 2]
target = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().search([4,5,6,7,0,1,2], 0)` | `4` |
| `Solution().search([4,5,6,7,0,1,2], 3)` | `-1` |
| `Solution().search([1], 0)` | `-1` |

---

### 05 · BS — on answer space (min/max feasibility)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def min_capacity(self, weights: list[int], days: int) -> int:
        pass
```

**Inputs given:**
```
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().min_capacity([1,2,3,4,5,6,7,8,9,10], 5)` | `15` |
| `Solution().min_capacity([3,2,2,4,1,4], 3)` | `6` |
| `Solution().min_capacity([1,2,3,1,1], 4)` | `3` |

---

### 06 · BFS — standard graph (adjacency list)
**Difficulty:** Easy

**Stub:**
```python
from collections import deque

class Solution:
    def bfs(self, graph: dict, start: int) -> list[int]:
        pass
```

**Inputs given:**
```
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
start = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().bfs({0:[1,2],1:[3],2:[3],3:[]}, 0)` | `[0, 1, 2, 3]` |
| `Solution().bfs({0:[1],1:[2],2:[]}, 0)` | `[0, 1, 2]` |

---

### 07 · BFS — level order tree traversal
**Difficulty:** Easy

**Stub:**
```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def level_order(self, root: TreeNode) -> list[list[int]]:
        pass
```

**Inputs given:**
```
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(3);r.left=TreeNode(9);r.right=TreeNode(20);r.right.left=TreeNode(15);r.right.right=TreeNode(7);Solution().level_order(r)` | `[[3], [9, 20], [15, 7]]` |
| `Solution().level_order(None)` | `[]` |

---

### 08 · Multi-source BFS (grid)
**Difficulty:** Medium

**Stub:**
```python
from collections import deque

class Solution:
    def oranges_rotting(self, grid: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().oranges_rotting([[2,1,1],[1,1,0],[0,1,1]])` | `4` |
| `Solution().oranges_rotting([[2,1,1],[0,1,1],[1,0,1]])` | `-1` |
| `Solution().oranges_rotting([[0,2]])` | `0` |

---

### 09 · DFS — iterative (explicit stack)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def dfs(self, graph: dict, start: int) -> list[int]:
        pass
```

**Inputs given:**
```
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
start = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().dfs({0:[1,2],1:[3],2:[3],3:[]}, 0)` | `[0, 2, 3, 1]` |
| `Solution().dfs({0:[1],1:[2],2:[]}, 0)` | `[0, 1, 2]` |

---

### 10 · DFS — recursive (graph, track visited)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def dfs(self, graph: dict, start: int) -> list[int]:
        pass
```

**Inputs given:**
```
graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
start = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().dfs({0:[1,2],1:[3],2:[3],3:[]}, 0)` | `[0, 1, 3, 2]` |

---

### 11 · Connected components (undirected)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def count_components(self, n: int, edges: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
n = 5
edges = [[0,1],[1,2],[3,4]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().count_components(5, [[0,1],[1,2],[3,4]])` | `2` |
| `Solution().count_components(4, [[0,1],[2,3],[1,2]])` | `1` |
| `Solution().count_components(3, [])` | `3` |

---

### 12 · Cycle detection — directed graph (DFS 3-color)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def has_cycle(self, n: int, edges: list[list[int]]) -> bool:
        pass
```

**Inputs given:**
```
n = 4
edges = [[0,1],[1,2],[2,3],[3,1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().has_cycle(4, [[0,1],[1,2],[2,3],[3,1]])` | `True` |
| `Solution().has_cycle(3, [[0,1],[1,2]])` | `False` |

---

### 13 · Bipartite check (BFS 2-coloring)
**Difficulty:** Medium

**Stub:**
```python
from collections import deque

class Solution:
    def is_bipartite(self, graph: list[list[int]]) -> bool:
        pass
```

**Inputs given:**
```
graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().is_bipartite([[1,3],[0,2],[1,3],[0,2]])` | `True` |
| `Solution().is_bipartite([[1,2,3],[0,2],[0,1,3],[0,2]])` | `False` |

---

### 14 · BFS on grid — 4-directional flood fill
**Difficulty:** Easy

**Stub:**
```python
from collections import deque

class Solution:
    def flood_fill(self, image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
        pass
```

**Inputs given:**
```
image = [[1,1,1],[1,1,0],[1,0,1]]
sr = 1, sc = 1, color = 2
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)` | `[[2,2,2],[2,2,0],[2,0,1]]` |
| `Solution().flood_fill([[0,0,0],[0,0,0]], 0, 0, 0)` | `[[0,0,0],[0,0,0]]` |

---

### 15 · Topo sort — Kahn's algorithm (BFS + in-degree)
**Difficulty:** Medium

**Stub:**
```python
from collections import deque

class Solution:
    def topo_sort(self, n: int, edges: list[list[int]]) -> list[int]:
        pass
```

**Inputs given:**
```
n = 6
edges = [[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=Solution().topo_sort(6,[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]]);len(r)==6 and r.index(5)<r.index(2) and r.index(2)<r.index(3)` | `True` |
| `Solution().topo_sort(2, [[1,0]])` | `[1, 0]` |

---

### 16 · Topo sort — DFS postorder
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def topo_sort(self, n: int, edges: list[list[int]]) -> list[int]:
        pass
```

**Inputs given:**
```
n = 4
edges = [[0,1],[0,2],[1,3],[2,3]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=Solution().topo_sort(4,[[0,1],[0,2],[1,3],[2,3]]);r.index(0)<r.index(1)<r.index(3) and r.index(0)<r.index(2)<r.index(3)` | `True` |

---

### 17 · Dijkstra's (min-heap, single source)
**Difficulty:** Medium

**Stub:**
```python
import heapq

class Solution:
    def dijkstra(self, n: int, edges: list[list[int]], src: int) -> list[int]:
        pass
```

**Inputs given:**
```
n = 5
edges = [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,5]]
src = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().dijkstra(5,[[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,5]],0)` | `[0, 3, 1, 4, -1]` |

---

### 18 · Bellman-Ford (handles negative weights)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def bellman_ford(self, n: int, edges: list[list[int]], src: int) -> list[int]:
        pass
```

**Inputs given:**
```
n = 5
edges = [[0,1,-1],[0,2,4],[1,2,3],[1,3,2],[1,4,2],[3,2,5],[3,1,1],[4,3,-3]]
src = 0
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().bellman_ford(5,[[0,1,-1],[0,2,4],[1,2,3],[1,3,2],[1,4,2],[3,2,5],[3,1,1],[4,3,-3]],0)` | `[0, -1, 2, -2, 1]` |

---

### 19 · Floyd-Warshall (all-pairs shortest path)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def floyd_warshall(self, n: int, edges: list[list[int]]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
n = 4
edges = [[0,1,3],[0,3,7],[1,0,8],[1,2,2],[2,0,5],[2,3,1],[3,0,2]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().floyd_warshall(4,[[0,1,3],[0,3,7],[1,0,8],[1,2,2],[2,0,5],[2,3,1],[3,0,2]])[0]` | `[0, 3, 5, 6]` |

---

### 20 · Prim's MST (min-heap, adjacency list)
**Difficulty:** Hard

**Stub:**
```python
import heapq

class Solution:
    def prims(self, n: int, edges: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
n = 4
edges = [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().prims(4,[[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]])` | `4` |

---

### 21 · Kruskal's MST (sort edges + union-find)
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def kruskals(self, n: int, edges: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
n = 4
edges = [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().kruskals(4,[[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]])` | `4` |

---

### 22 · Union-Find — path compression + union by rank
**Difficulty:** Medium

**Stub:**
```python
class UnionFind:
    def __init__(self, n: int):
        pass
    def find(self, x: int) -> int:
        pass
    def union(self, x: int, y: int) -> bool:
        pass

class Solution:
    def count_components(self, n: int, edges: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
n = 5
edges = [[0,1],[1,2],[3,4]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().count_components(5,[[0,1],[1,2],[3,4]])` | `2` |
| `Solution().count_components(3,[])` | `3` |
| `Solution().count_components(4,[[0,1],[0,2],[0,3]])` | `1` |

---

### 23 · Tarjan's bridges (critical connections)
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def critical_connections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
n = 4
connections = [[0,1],[1,2],[2,0],[1,3]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `sorted(Solution().critical_connections(4,[[0,1],[1,2],[2,0],[1,3]]))` | `[[1, 3]]` |

---

### 24 · Preorder traversal — iterative (root, left, right)
**Difficulty:** Easy

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def preorder(self, root: TreeNode) -> list[int]:
        pass
```

**Inputs given:**
```
root = TreeNode(1)
root.right = TreeNode(2)
root.right.left = TreeNode(3)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(1);r.right=TreeNode(2);r.right.left=TreeNode(3);Solution().preorder(r)` | `[1, 2, 3]` |

---

### 25 · Inorder traversal — iterative (left, root, right)
**Difficulty:** Easy

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def inorder(self, root: TreeNode) -> list[int]:
        pass
```

**Inputs given:**
```
root = TreeNode(1)
root.right = TreeNode(2)
root.right.left = TreeNode(3)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(1);r.right=TreeNode(2);r.right.left=TreeNode(3);Solution().inorder(r)` | `[1, 3, 2]` |

---

### 26 · Postorder traversal — iterative (left, right, root)
**Difficulty:** Easy

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorder(self, root: TreeNode) -> list[int]:
        pass
```

**Inputs given:**
```
root = TreeNode(1)
root.right = TreeNode(2)
root.right.left = TreeNode(3)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(1);r.right=TreeNode(2);r.right.left=TreeNode(3);Solution().postorder(r)` | `[3, 2, 1]` |

---

### 27 · LCA — binary tree (DFS recursive)
**Difficulty:** Medium

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lca(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        pass
```

**Inputs given:**
```
root = [3,5,1,6,2,0,8,null,null,7,4]
p = node(5), q = node(1)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def build(v,l=None,r=None):\n    n=TreeNode(v);n.left=l;n.right=r;return n\nr=build(3,build(5,build(6),build(2,build(7),build(4))),build(1,build(0),build(8)))\np=r.left;q=r.right;Solution().lca(r,p,q).val` | `3` |

---

### 28 · Validate BST (DFS with min/max bounds)
**Difficulty:** Medium

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def is_valid_bst(self, root: TreeNode) -> bool:
        pass
```

**Inputs given:**
```
root = TreeNode(2)
root.left = TreeNode(1)
root.right = TreeNode(3)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(2);r.left=TreeNode(1);r.right=TreeNode(3);Solution().is_valid_bst(r)` | `True` |
| `r=TreeNode(5);r.left=TreeNode(1);r.right=TreeNode(4);r.right.left=TreeNode(3);r.right.right=TreeNode(6);Solution().is_valid_bst(r)` | `False` |

---

### 29 · Diameter of binary tree (DFS postorder)
**Difficulty:** Easy

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def diameter(self, root: TreeNode) -> int:
        pass
```

**Inputs given:**
```
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(1);r.left=TreeNode(2);r.right=TreeNode(3);r.left.left=TreeNode(4);r.left.right=TreeNode(5);Solution().diameter(r)` | `3` |
| `r=TreeNode(1);r.left=TreeNode(2);Solution().diameter(r)` | `1` |

---

### 30 · Max path sum in binary tree (tree DP)
**Difficulty:** Hard

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def max_path_sum(self, root: TreeNode) -> int:
        pass
```

**Inputs given:**
```
root = TreeNode(-10)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `r=TreeNode(-10);r.left=TreeNode(9);r.right=TreeNode(20);r.right.left=TreeNode(15);r.right.right=TreeNode(7);Solution().max_path_sum(r)` | `42` |
| `r=TreeNode(1);r.left=TreeNode(2);r.right=TreeNode(3);Solution().max_path_sum(r)` | `6` |

---

### 31 · Serialize / deserialize binary tree
**Difficulty:** Hard

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root: TreeNode) -> str:
        pass
    def deserialize(self, data: str) -> TreeNode:
        pass
```

**Inputs given:**
```
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.right.left = TreeNode(4)
root.right.right = TreeNode(5)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def inorder(r):\n    return [] if not r else inorder(r.left)+[r.val]+inorder(r.right)\nc=Codec();r=TreeNode(1);r.left=TreeNode(2);r.right=TreeNode(3);r.right.left=TreeNode(4);r.right.right=TreeNode(5)\ninorder(c.deserialize(c.serialize(r)))` | `[2, 1, 4, 3, 5]` |

---

### 32 · Build tree from preorder + inorder arrays
**Difficulty:** Medium

**Stub:**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def build_tree(self, preorder: list[int], inorder: list[int]) -> TreeNode:
        pass
```

**Inputs given:**
```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def post(r):\n    return [] if not r else post(r.left)+post(r.right)+[r.val]\npost(Solution().build_tree([3,9,20,15,7],[9,3,15,20,7]))` | `[9, 15, 7, 20, 3]` |

---

### 33 · Reverse linked list — iterative
**Difficulty:** Easy

**Stub:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverse(self, head: ListNode) -> ListNode:
        pass
```

**Inputs given:**
```
head = 1 -> 2 -> 3 -> 4 -> 5
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def mk(vs):\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().reverse(mk([1,2,3,4,5])))` | `[5, 4, 3, 2, 1]` |

---

### 34 · Cycle detection — Floyd's tortoise and hare
**Difficulty:** Easy

**Stub:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def has_cycle(self, head: ListNode) -> bool:
        pass
```

**Inputs given:**
```
head = 3 -> 2 -> 0 -> -4 -> (back to node at index 1)
```

**Test cases:**
| Call | Expected |
|------|----------|
| `a=ListNode(3);b=ListNode(2);c=ListNode(0);d=ListNode(-4);a.next=b;b.next=c;c.next=d;d.next=b;Solution().has_cycle(a)` | `True` |
| `a=ListNode(1);b=ListNode(2);a.next=b;Solution().has_cycle(a)` | `False` |

---

### 35 · Find middle — fast/slow pointers
**Difficulty:** Easy

**Stub:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def find_middle(self, head: ListNode) -> ListNode:
        pass
```

**Inputs given:**
```
head = 1 -> 2 -> 3 -> 4 -> 5
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def mk(vs):\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\nSolution().find_middle(mk([1,2,3,4,5])).val` | `3` |
| `def mk(vs):\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\nSolution().find_middle(mk([1,2,3,4])).val` | `3` |

---

### 36 · Remove Nth node from end (two-pointer gap)
**Difficulty:** Medium

**Stub:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def remove_nth(self, head: ListNode, n: int) -> ListNode:
        pass
```

**Inputs given:**
```
head = 1 -> 2 -> 3 -> 4 -> 5
n = 2
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def mk(vs):\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().remove_nth(mk([1,2,3,4,5]),2))` | `[1, 2, 3, 5]` |

---

### 37 · Merge two sorted lists
**Difficulty:** Easy

**Stub:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def merge(self, l1: ListNode, l2: ListNode) -> ListNode:
        pass
```

**Inputs given:**
```
l1 = 1 -> 2 -> 4
l2 = 1 -> 3 -> 4
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def mk(vs):\n    if not vs: return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge(mk([1,2,4]),mk([1,3,4])))` | `[1, 1, 2, 3, 4, 4]` |

---

### 38 · Stack — bracket matching (valid parentheses)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def is_valid(self, s: str) -> bool:
        pass
```

**Inputs given:**
```
s = "()[]{}"
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().is_valid("()[]{}")` | `True` |
| `Solution().is_valid("(]")` | `False` |
| `Solution().is_valid("{[]}")` | `True` |
| `Solution().is_valid("([)]")` | `False` |

---

### 39 · Stack — evaluate reverse polish notation
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def eval_rpn(self, tokens: list[str]) -> int:
        pass
```

**Inputs given:**
```
tokens = ["2","1","+","3","*"]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().eval_rpn(["2","1","+","3","*"])` | `9` |
| `Solution().eval_rpn(["4","13","5","/","+"])` | `6` |
| `Solution().eval_rpn(["10","6","9","3","+","-11","*","/","*","17","+","5","+"])` | `22` |

---

### 40 · Monotonic stack — next greater element
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def next_greater(self, nums: list[int]) -> list[int]:
        pass
```

**Inputs given:**
```
nums = [2, 1, 2, 4, 3]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().next_greater([2,1,2,4,3])` | `[4, 2, 4, -1, -1]` |
| `Solution().next_greater([1,3,2])` | `[3, -1, -1]` |

---

### 41 · Monotonic deque — sliding window maximum
**Difficulty:** Hard

**Stub:**
```python
from collections import deque

class Solution:
    def max_sliding_window(self, nums: list[int], k: int) -> list[int]:
        pass
```

**Inputs given:**
```
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().max_sliding_window([1,3,-1,-3,5,3,6,7],3)` | `[3, 3, 5, 5, 6, 7]` |
| `Solution().max_sliding_window([1],1)` | `[1]` |

---

### 42 · Merge intervals (sort + greedy)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
intervals = [[1,3],[2,6],[8,10],[15,18]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().merge([[1,3],[2,6],[8,10],[15,18]])` | `[[1, 6], [8, 10], [15, 18]]` |
| `Solution().merge([[1,4],[4,5]])` | `[[1, 5]]` |

---

### 43 · Insert interval (merge with new interval)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def insert(self, intervals: list[list[int]], new: list[int]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
intervals = [[1,3],[6,9]]
new = [2,5]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().insert([[1,3],[6,9]],[2,5])` | `[[1, 5], [6, 9]]` |
| `Solution().insert([[1,2],[3,5],[6,7],[8,10],[12,16]],[4,8])` | `[[1, 2], [3, 10], [12, 16]]` |

---

### 44 · Greedy interval scheduling (minimum arrows)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def find_min_arrows(self, points: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
points = [[10,16],[2,8],[1,6],[7,12]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().find_min_arrows([[10,16],[2,8],[1,6],[7,12]])` | `2` |
| `Solution().find_min_arrows([[1,2],[3,4],[5,6],[7,8]])` | `4` |

---

### 45 · Kth largest element (min-heap of size k)
**Difficulty:** Medium

**Stub:**
```python
import heapq

class Solution:
    def kth_largest(self, nums: list[int], k: int) -> int:
        pass
```

**Inputs given:**
```
nums = [3, 2, 1, 5, 6, 4]
k = 2
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().kth_largest([3,2,1,5,6,4],2)` | `5` |
| `Solution().kth_largest([3,2,3,1,2,4,5,5,6],4)` | `4` |

---

### 46 · Merge K sorted lists (min-heap)
**Difficulty:** Hard

**Stub:**
```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __lt__(self, other):
        return self.val < other.val

class Solution:
    def merge_k_lists(self, lists: list[ListNode]) -> ListNode:
        pass
```

**Inputs given:**
```
lists = [1->4->5,  1->3->4,  2->6]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `def mk(vs):\n    if not vs:return None\n    h=t=ListNode(vs[0])\n    for v in vs[1:]:t.next=ListNode(v);t=t.next\n    return h\ndef ls(h):\n    r=[]\n    while h:r.append(h.val);h=h.next\n    return r\nls(Solution().merge_k_lists([mk([1,4,5]),mk([1,3,4]),mk([2,6])]))` | `[1, 1, 2, 3, 4, 4, 5, 6]` |

---

### 47 · Top K frequent elements (heap + hash map)
**Difficulty:** Medium

**Stub:**
```python
import heapq
from collections import Counter

class Solution:
    def top_k_frequent(self, nums: list[int], k: int) -> list[int]:
        pass
```

**Inputs given:**
```
nums = [1, 1, 1, 2, 2, 3]
k = 2
```

**Test cases:**
| Call | Expected |
|------|----------|
| `sorted(Solution().top_k_frequent([1,1,1,2,2,3],2))` | `[1, 2]` |
| `Solution().top_k_frequent([1],1)` | `[1]` |

---

### 48 · Fixed window — max sum subarray of size k
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def max_sum(self, nums: list[int], k: int) -> int:
        pass
```

**Inputs given:**
```
nums = [2, 1, 5, 1, 3, 2]
k = 3
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().max_sum([2,1,5,1,3,2],3)` | `9` |
| `Solution().max_sum([2,3,4,1,5],2)` | `7` |

---

### 49 · Variable window — longest substring without repeating
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def length_of_longest(self, s: str) -> int:
        pass
```

**Inputs given:**
```
s = "abcabcbb"
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().length_of_longest("abcabcbb")` | `3` |
| `Solution().length_of_longest("bbbbb")` | `1` |
| `Solution().length_of_longest("pwwkew")` | `3` |

---

### 50 · Two pointers — pair sum in sorted array
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        pass
```

**Inputs given:**
```
nums = [2, 7, 11, 15]
target = 9
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().two_sum([2,7,11,15],9)` | `[0, 1]` |
| `Solution().two_sum([2,3,4],6)` | `[0, 2]` |

---

### 51 · Dutch National Flag (3-way partition)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def sort_colors(self, nums: list[int]) -> list[int]:
        pass
```

**Inputs given:**
```
nums = [2, 0, 2, 1, 1, 0]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().sort_colors([2,0,2,1,1,0])` | `[0, 0, 1, 1, 2, 2]` |
| `Solution().sort_colors([2,0,1])` | `[0, 1, 2]` |

---

### 52 · Fast/slow pointers — find duplicate (Floyd's on array)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def find_duplicate(self, nums: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums = [1, 3, 4, 2, 2]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().find_duplicate([1,3,4,2,2])` | `2` |
| `Solution().find_duplicate([3,1,3,4,2])` | `3` |

---

### 53 · Prefix sum — 1D range query
**Difficulty:** Easy

**Stub:**
```python
class NumArray:
    def __init__(self, nums: list[int]):
        pass
    def sum_range(self, left: int, right: int) -> int:
        pass
```

**Inputs given:**
```
nums = [-2, 0, 3, -5, 2, -1]
left = 0, right = 2
```

**Test cases:**
| Call | Expected |
|------|----------|
| `n=NumArray([-2,0,3,-5,2,-1]);[n.sum_range(0,2),n.sum_range(2,5),n.sum_range(0,5)]` | `[1, -1, -3]` |

---

### 54 · Kadane's algorithm (max subarray sum)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def max_subarray(self, nums: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().max_subarray([-2,1,-3,4,-1,2,1,-5,4])` | `6` |
| `Solution().max_subarray([1])` | `1` |
| `Solution().max_subarray([5,4,-1,7,8])` | `23` |

---

### 55 · 1D DP — climbing stairs / Fibonacci
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def climb_stairs(self, n: int) -> int:
        pass
```

**Inputs given:**
```
n = 5
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().climb_stairs(5)` | `8` |
| `Solution().climb_stairs(3)` | `3` |
| `Solution().climb_stairs(1)` | `1` |

---

### 56 · 1D DP — house robber (max non-adjacent)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums = [2, 7, 9, 3, 1]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().rob([2,7,9,3,1])` | `12` |
| `Solution().rob([1,2,3,1])` | `4` |
| `Solution().rob([2,1])` | `2` |

---

### 57 · 1D DP — coin change (unbounded knapsack)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def coin_change(self, coins: list[int], amount: int) -> int:
        pass
```

**Inputs given:**
```
coins = [1, 5, 6, 9]
amount = 11
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().coin_change([1,5,6,9],11)` | `2` |
| `Solution().coin_change([2],3)` | `-1` |
| `Solution().coin_change([1],0)` | `0` |

---

### 58 · 1D DP — LIS O(n log n) with binary search
**Difficulty:** Medium

**Stub:**
```python
import bisect

class Solution:
    def length_of_lis(self, nums: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums = [10, 9, 2, 5, 3, 7, 101, 18]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().length_of_lis([10,9,2,5,3,7,101,18])` | `4` |
| `Solution().length_of_lis([0,1,0,3,2,3])` | `4` |
| `Solution().length_of_lis([7,7,7,7])` | `1` |

---

### 59 · 2D DP — LCS (longest common subsequence)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def lcs(self, text1: str, text2: str) -> int:
        pass
```

**Inputs given:**
```
text1 = "abcde"
text2 = "ace"
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().lcs("abcde","ace")` | `3` |
| `Solution().lcs("abc","abc")` | `3` |
| `Solution().lcs("abc","def")` | `0` |

---

### 60 · 2D DP — edit distance (Levenshtein)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def min_distance(self, word1: str, word2: str) -> int:
        pass
```

**Inputs given:**
```
word1 = "horse"
word2 = "ros"
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().min_distance("horse","ros")` | `3` |
| `Solution().min_distance("intention","execution")` | `5` |
| `Solution().min_distance("","a")` | `1` |

---

### 61 · 2D DP — unique paths (grid)
**Difficulty:** Easy

**Stub:**
```python
class Solution:
    def unique_paths(self, m: int, n: int) -> int:
        pass
```

**Inputs given:**
```
m = 3
n = 7
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().unique_paths(3,7)` | `28` |
| `Solution().unique_paths(3,2)` | `3` |
| `Solution().unique_paths(1,1)` | `1` |

---

### 62 · 2D DP — minimum path sum (grid)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def min_path_sum(self, grid: list[list[int]]) -> int:
        pass
```

**Inputs given:**
```
grid = [[1,3,1],[1,5,1],[4,2,1]]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().min_path_sum([[1,3,1],[1,5,1],[4,2,1]])` | `7` |
| `Solution().min_path_sum([[1,2],[5,6],[1,1]])` | `8` |

---

### 63 · 0/1 Knapsack — partition equal subset sum
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def can_partition(self, nums: list[int]) -> bool:
        pass
```

**Inputs given:**
```
nums = [1, 5, 11, 5]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().can_partition([1,5,11,5])` | `True` |
| `Solution().can_partition([1,2,3,5])` | `False` |

---

### 64 · Interval DP — burst balloons
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def max_coins(self, nums: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums = [3, 1, 5, 8]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().max_coins([3,1,5,8])` | `167` |
| `Solution().max_coins([1,5])` | `10` |

---

### 65 · DP + memoization — word break
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def word_break(self, s: str, word_dict: list[str]) -> bool:
        pass
```

**Inputs given:**
```
s = "leetcode"
word_dict = ["leet", "code"]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().word_break("leetcode",["leet","code"])` | `True` |
| `Solution().word_break("applepenapple",["apple","pen"])` | `True` |
| `Solution().word_break("catsandog",["cats","dog","sand","and","cat"])` | `False` |

---

### 66 · Bitmask DP — minimum XOR sum / assignment
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def minimum_xor_sum(self, nums1: list[int], nums2: list[int]) -> int:
        pass
```

**Inputs given:**
```
nums1 = [1, 2]
nums2 = [2, 3]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().minimum_xor_sum([1,2],[2,3])` | `2` |
| `Solution().minimum_xor_sum([1,0,3],[5,3,4])` | `8` |

---

### 67 · Trie — build from scratch (insert / search / startsWith)
**Difficulty:** Medium

**Stub:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word: str) -> None:
        pass
    def search(self, word: str) -> bool:
        pass
    def starts_with(self, prefix: str) -> bool:
        pass
```

**Inputs given:**
```
ops: insert("apple"), search("apple"), search("app"), startsWith("app"), insert("app"), search("app")
```

**Test cases:**
| Call | Expected |
|------|----------|
| `t=Trie();t.insert("apple");[t.search("apple"),t.search("app"),t.starts_with("app")]` | `[True, False, True]` |
| `t=Trie();t.insert("app");[t.search("app"),t.starts_with("ap")]` | `[True, True]` |

---

### 68 · Backtracking — subsets (power set)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
nums = [1, 2, 3]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `sorted([sorted(s) for s in Solution().subsets([1,2,3])])` | `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]` |

---

### 69 · Backtracking — permutations
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        pass
```

**Inputs given:**
```
nums = [1, 2, 3]
```

**Test cases:**
| Call | Expected |
|------|----------|
| `len(Solution().permute([1,2,3]))` | `6` |
| `sorted(Solution().permute([1,2]))` | `[[1, 2], [2, 1]]` |

---

### 70 · Backtracking — combination sum (target)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def combination_sum(self, candidates: list[int], target: int) -> list[list[int]]:
        pass
```

**Inputs given:**
```
candidates = [2, 3, 6, 7]
target = 7
```

**Test cases:**
| Call | Expected |
|------|----------|
| `sorted([sorted(c) for c in Solution().combination_sum([2,3,6,7],7)])` | `[[2, 2, 3], [7]]` |
| `sorted([sorted(c) for c in Solution().combination_sum([2,3,5],8)])` | `[[2, 2, 2, 2], [2, 3, 3], [3, 5]]` |

---

### 71 · Backtracking — N-Queens
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def solve_n_queens(self, n: int) -> list[list[str]]:
        pass
```

**Inputs given:**
```
n = 4
```

**Test cases:**
| Call | Expected |
|------|----------|
| `len(Solution().solve_n_queens(4))` | `2` |
| `len(Solution().solve_n_queens(1))` | `1` |

---

### 72 · KMP — pattern matching (find first occurrence)
**Difficulty:** Hard

**Stub:**
```python
class Solution:
    def str_str(self, haystack: str, needle: str) -> int:
        pass
```

**Inputs given:**
```
haystack = "mississippi"
needle = "issip"
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().str_str("mississippi","issip")` | `4` |
| `Solution().str_str("hello","ll")` | `2` |
| `Solution().str_str("aaa","aaaa")` | `-1` |

---

### 73 · Sieve of Eratosthenes (count primes < n)
**Difficulty:** Medium

**Stub:**
```python
class Solution:
    def count_primes(self, n: int) -> int:
        pass
```

**Inputs given:**
```
n = 10
```

**Test cases:**
| Call | Expected |
|------|----------|
| `Solution().count_primes(10)` | `4` |
| `Solution().count_primes(0)` | `0` |
| `Solution().count_primes(1)` | `0` |
"""

algs = []

blocks = re.split(r'### (\d+) · (.*?)\n\*\*Difficulty:\*\* (.*?)\n\n\*\*Stub:\*\*\n```python\n(.*?)```\n\n\*\*Inputs given:\*\*\n```\n(.*?)```\n\n\*\*Test cases:\*\*\n.*?\| Call \| Expected \|\n\|------\|----------\|\n(.*?)(?=\n---|\Z)', md, flags=re.DOTALL)

for i in range(1, len(blocks), 7):
    num = blocks[i].strip()
    title = blocks[i+1].strip()
    difficulty = blocks[i+2].strip().lower()
    stub = blocks[i+3].strip()
    inputs = blocks[i+4].strip()
    test_cases_str = blocks[i+5].strip()
    
    tc_lines = [line.strip() for line in test_cases_str.split('\n') if line.strip()]
    test_cases = []
    for line in tc_lines:
        parts = line.split('|')
        if len(parts) >= 4:
            call_code = parts[1].strip().strip('`')
            expected_code = parts[2].strip().strip('`')
            test_cases.append({
                "call": call_code,
                "expected": expected_code
            })
            
    # generate a clean ID
    clean_id = re.sub(r'[^a-zA-Z0-9]+', '_', title.lower()).strip('_')
    
    algs.append({
        "id": f"drill_{num}_{clean_id}",
        "title": title,
        "stub": stub,
        "inputs_given": inputs,
        "test_cases": test_cases,
        "tags": [], # we could parse the table of contents but this is fine, or hardcode them
        "difficulty": difficulty
    })

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "w", encoding="utf-8") as f:
    json.dump(algs, f, indent=2)

print(f"Generated {len(algs)} algorithms.")

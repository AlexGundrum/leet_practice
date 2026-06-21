import json

descriptions = [
    "Given an array of integers <code>nums</code> which is sorted in ascending order, and an integer <code>target</code>, write a function to search <code>target</code> in <code>nums</code>. If <code>target</code> exists, then return its index. Otherwise, return <code>-1</code>.",
    "Given an array of integers <code>nums</code> sorted in non-decreasing order, find the starting position of a given <code>target</code> value. If target is not found in the array, return <code>-1</code>.",
    "Given an array of integers <code>nums</code> sorted in non-decreasing order, find the ending position of a given <code>target</code> value. If target is not found in the array, return <code>-1</code>.",
    "There is an integer array <code>nums</code> sorted in ascending order (with distinct values) that is rotated at an unknown pivot index. Given the array <code>nums</code> after the possible rotation and an integer <code>target</code>, return the index of <code>target</code> if it is in <code>nums</code>, or <code>-1</code> if it is not in <code>nums</code>.",
    "A conveyor belt has packages that must be shipped from one port to another within <code>days</code> days. The <code>i</code>-th package on the conveyor belt has a weight of <code>weights[i]</code>. Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within <code>days</code> days.",
    
    "Given a directed graph represented as an adjacency list <code>graph</code> where <code>graph[i]</code> is a list of nodes that node <code>i</code> points to, and a <code>start</code> node, return a list of nodes in the order they are visited using Breadth-First Search (BFS). Visit neighbors in the order they appear in the list.",
    "Given the <code>root</code> of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
    "You are given an <code>m x n</code> grid where each cell can have one of three values: <code>0</code> (empty), <code>1</code> (fresh orange), or <code>2</code> (rotten orange). Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return <code>-1</code>.",
    "Given a directed graph represented as an adjacency list <code>graph</code> where <code>graph[i]</code> is a list of nodes that node <code>i</code> points to, and a <code>start</code> node, return a list of nodes in the order they are visited using an iterative Depth-First Search (DFS) with a stack. Push neighbors in the order they appear, which means the last neighbor is popped and visited first.",
    "Given a directed graph represented as an adjacency list <code>graph</code> and a <code>start</code> node, return a list of nodes in the order they are visited using recursive Depth-First Search (DFS). Visit neighbors in the order they appear in the list.",
    "You have a graph of <code>n</code> nodes. You are given an integer <code>n</code> and an array <code>edges</code> where <code>edges[i] = [a, b]</code> indicates that there is an undirected edge between <code>a</code> and <code>b</code> in the graph. Return the number of connected components in the graph.",
    "Given <code>n</code> nodes labeled from <code>0</code> to <code>n-1</code> and a list of directed edges where <code>edges[i] = [u, v]</code> represents a directed edge from node <code>u</code> to node <code>v</code>, return <code>True</code> if the graph contains a cycle, and <code>False</code> otherwise.",
    "There is an undirected graph with <code>n</code> nodes, where each node is numbered between <code>0</code> and <code>n - 1</code>. You are given a 2D array <code>graph</code>, where <code>graph[u]</code> is an array of nodes that node <code>u</code> is adjacent to. Return <code>True</code> if and only if it is bipartite.",
    "An image is represented by an <code>m x n</code> integer grid <code>image</code> where <code>image[i][j]</code> represents the pixel value of the image. You are also given three integers <code>sr</code>, <code>sc</code>, and <code>color</code>. You should perform a flood fill on the image starting from the pixel <code>image[sr][sc]</code> and replacing its color and all connected adjacent pixels of the same color with <code>color</code>.",
    
    "Given <code>n</code> nodes and a list of directed edges where <code>edges[i] = [u, v]</code> indicates a directed edge from <code>u</code> to <code>v</code>, return a valid topological sort array of the nodes. If no such sort is possible (a cycle exists), behavior is undefined (or return an incomplete list).",
    "Given <code>n</code> nodes and a list of directed edges where <code>edges[i] = [u, v]</code> indicates a directed edge from <code>u</code> to <code>v</code>, return a valid topological sort array using DFS postorder reversal. Assume the graph is a DAG.",
    
    "Given <code>n</code> nodes and a list of directed weighted edges where <code>edges[i] = [u, v, weight]</code>, find the shortest path from the <code>src</code> node to all other nodes. Return an array of size <code>n</code> where the value at index <code>i</code> is the shortest distance to node <code>i</code>. If a node is unreachable, the value should be <code>-1</code>.",
    "Given <code>n</code> nodes and a list of directed weighted edges where <code>edges[i] = [u, v, weight]</code> (weights can be negative), find the shortest path from the <code>src</code> node to all other nodes. Return an array of size <code>n</code> where the value at index <code>i</code> is the shortest distance to node <code>i</code>. If a node is unreachable, the value should be <code>-1</code>.",
    "Given <code>n</code> nodes and a list of directed weighted edges where <code>edges[i] = [u, v, weight]</code>, find the shortest path between all pairs of nodes. Return an <code>n x n</code> matrix where <code>matrix[i][j]</code> is the shortest distance from <code>i</code> to <code>j</code>.",
    
    "Given <code>n</code> nodes and a list of undirected weighted edges where <code>edges[i] = [u, v, weight]</code>, return the total weight of the Minimum Spanning Tree (MST).",
    "Given <code>n</code> nodes and a list of undirected weighted edges where <code>edges[i] = [u, v, weight]</code>, return the total weight of the Minimum Spanning Tree (MST).",
    
    "Implement a <code>UnionFind</code> class with path compression and union by rank. Then, use it to solve the connected components problem: given <code>n</code> nodes and undirected <code>edges</code> (where <code>edges[i] = [u, v]</code>), return the number of connected components.",
    
    "There are <code>n</code> servers numbered from <code>0</code> to <code>n - 1</code> connected by undirected server-to-server connections forming a network where <code>connections[i] = [a, b]</code>. Return a list of all critical connections (bridges) in the network.",
    
    "Given the <code>root</code> of a binary tree, return the preorder traversal of its nodes' values iteratively.",
    "Given the <code>root</code> of a binary tree, return the inorder traversal of its nodes' values iteratively.",
    "Given the <code>root</code> of a binary tree, return the postorder traversal of its nodes' values iteratively.",
    "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes <code>p</code> and <code>q</code> in the tree.",
    "Given the <code>root</code> of a binary tree, determine if it is a valid binary search tree (BST).",
    "Given the <code>root</code> of a binary tree, return the length of the diameter of the tree. The diameter is the length of the longest path between any two nodes.",
    "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. Return the maximum path sum of any non-empty path.",
    "Design an algorithm to serialize and deserialize a binary tree. The <code>serialize</code> method converts a tree to a string, and <code>deserialize</code> converts the string back to a tree.",
    "Given two integer arrays <code>preorder</code> and <code>inorder</code> where <code>preorder</code> is the preorder traversal of a binary tree and <code>inorder</code> is the inorder traversal of the same tree, construct and return the binary tree.",
    
    "Given the <code>head</code> of a singly linked list, reverse the list, and return the reversed list.",
    "Given <code>head</code>, the head of a linked list, determine if the linked list has a cycle in it.",
    "Given the <code>head</code> of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.",
    "Given the <code>head</code> of a linked list, remove the <code>n</code>-th node from the end of the list and return its head.",
    "You are given the heads of two sorted linked lists <code>l1</code> and <code>l2</code>. Merge the two lists into one sorted list.",
    
    "Given a string <code>s</code> containing just the characters <code>'(', ')', '{', '}', '['</code> and <code>']'</code>, determine if the input string is valid.",
    "Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are <code>+, -, *, /</code>.",
    "Given an array <code>nums</code>, find the next greater element for each element in the array. Return an array of the same size. If no greater element exists, output <code>-1</code>.",
    "You are given an array of integers <code>nums</code>, there is a sliding window of size <code>k</code> which is moving from the very left of the array to the very right. Return the max sliding window.",
    
    "Given an array of <code>intervals</code> where <code>intervals[i] = [start, end]</code>, merge all overlapping intervals.",
    "You are given an array of non-overlapping intervals sorted by their start time, and a <code>new</code> interval. Insert the new interval into the array (merge if necessary).",
    "There are some spherical balloons taped onto a flat wall. You are given a 2D integer array <code>points</code> where <code>points[i] = [start, end]</code>. Return the minimum number of arrows that must be shot to burst all balloons.",
    
    "Given an integer array <code>nums</code> and an integer <code>k</code>, return the <code>k</code>-th largest element in the array.",
    "You are given an array of <code>k</code> linked-lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
    "Given an integer array <code>nums</code> and an integer <code>k</code>, return the <code>k</code> most frequent elements.",
    
    "Given an array of integers <code>nums</code> and an integer <code>k</code>, find the maximum sum of any contiguous subarray of size <code>k</code>.",
    "Given a string <code>s</code>, find the length of the longest substring without repeating characters.",
    
    "Given a 1-indexed array of integers <code>nums</code> that is already sorted in non-decreasing order, find two numbers such that they add up to a specific <code>target</code> number. Return their 0-indexed positions.",
    "Given an array <code>nums</code> with <code>n</code> objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red (0), white (1), and blue (2).",
    "Given an array of integers <code>nums</code> containing <code>n + 1</code> integers where each integer is in the range <code>[1, n]</code> inclusive. There is only one repeated number in <code>nums</code>, return this repeated number. You must solve the problem without modifying the array.",
    
    "Given an integer array <code>nums</code>, handle multiple queries to calculate the sum of the elements of <code>nums</code> between indices <code>left</code> and <code>right</code> inclusive.",
    "Given an integer array <code>nums</code>, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
    
    "You are climbing a staircase. It takes <code>n</code> steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
    "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, but adjacent houses have security systems connected. Given an integer array <code>nums</code> representing the money of each house, return the maximum amount of money you can rob tonight without alerting the police.",
    "You are given an integer array <code>coins</code> representing coins of different denominations and an integer <code>amount</code> representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If it cannot be made up, return <code>-1</code>.",
    "Given an integer array <code>nums</code>, return the length of the longest strictly increasing subsequence.",
    "Given two strings <code>text1</code> and <code>text2</code>, return the length of their longest common subsequence. If there is no common subsequence, return <code>0</code>.",
    "Given two strings <code>word1</code> and <code>word2</code>, return the minimum number of operations required to convert <code>word1</code> to <code>word2</code>. Operations are insert, delete, or replace a character.",
    "There is a robot on an <code>m x n</code> grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Given <code>m</code> and <code>n</code>, return the number of possible unique paths.",
    "Given a <code>m x n</code> grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path. You can only move down or right.",
    "Given an integer array <code>nums</code>, return <code>True</code> if you can partition the array into two subsets such that the sum of the elements in both subsets is equal.",
    "You are given <code>n</code> balloons, indexed from <code>0</code> to <code>n - 1</code>. Each balloon is painted with a number on it represented by an array <code>nums</code>. If you burst the <code>i</code>-th balloon, you will get <code>nums[i - 1] * nums[i] * nums[i + 1]</code> coins. Return the maximum coins you can collect by bursting the balloons wisely.",
    "Given a string <code>s</code> and a dictionary of strings <code>word_dict</code>, return <code>True</code> if <code>s</code> can be segmented into a space-separated sequence of one or more dictionary words.",
    "You are given two integer arrays <code>nums1</code> and <code>nums2</code> of length <code>n</code>. The XOR sum of the two arrays is <code>(nums1[0] XOR nums2[0]) + (nums1[1] XOR nums2[1]) + ... + (nums1[n - 1] XOR nums2[n - 1])</code>. Return the minimum XOR sum after rearranging the elements of <code>nums2</code>.",
    
    "A trie (pronounced as 'try') or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. Implement the <code>Trie</code> class with <code>insert</code>, <code>search</code>, and <code>starts_with</code> methods.",
    
    "Given an integer array <code>nums</code> of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets.",
    "Given an array <code>nums</code> of distinct integers, return all the possible permutations. You can return the answer in any order.",
    "Given an array of distinct integers <code>candidates</code> and a target integer <code>target</code>, return a list of all unique combinations of candidates where the chosen numbers sum to <code>target</code>. You may choose the same number from <code>candidates</code> an unlimited number of times.",
    "The n-queens puzzle is the problem of placing <code>n</code> queens on an <code>n x n</code> chessboard such that no two queens attack each other. Return all distinct solutions. Each solution contains a distinct board configuration of the n-queens' placement, where <code>'Q'</code> and <code>'.'</code> both indicate a queen and an empty space respectively.",
    
    "Given two strings <code>needle</code> and <code>haystack</code>, return the index of the first occurrence of <code>needle</code> in <code>haystack</code>, or <code>-1</code> if <code>needle</code> is not part of <code>haystack</code>. Implement using KMP or similar efficient algorithm.",
    "Given an integer <code>n</code>, return the number of prime numbers that are strictly less than <code>n</code>."
]

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "r", encoding="utf-8") as f:
    algs = json.load(f)

for i in range(len(algs)):
    if i < len(descriptions):
        algs[i]["description"] = descriptions[i]

with open("c:/Users/alexg/code/leet_practice/algorithms.json", "w", encoding="utf-8") as f:
    json.dump(algs, f, indent=2)

print("Added descriptions to algorithms.json")

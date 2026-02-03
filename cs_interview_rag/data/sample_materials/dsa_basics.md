# Data Structures and Algorithms - CS Interview Study Material

## Arrays

An **array** is a contiguous block of memory that stores elements of the same data type. Arrays provide O(1) random access using indices.

### Key Operations
- **Access**: O(1) - Direct index access
- **Search**: O(n) - Linear search, O(log n) for sorted arrays with binary search
- **Insertion**: O(n) - May require shifting elements
- **Deletion**: O(n) - May require shifting elements

### Common Interview Topics
1. Two-pointer technique for solving array problems
2. Sliding window for subarray problems
3. Prefix sums for range queries
4. Kadane's algorithm for maximum subarray sum

---

## Linked Lists

A **linked list** is a linear data structure where elements are stored in nodes, each containing data and a reference to the next node.

### Types of Linked Lists
- **Singly Linked List**: Each node points to the next node
- **Doubly Linked List**: Each node points to both next and previous nodes
- **Circular Linked List**: The last node points back to the first

### Key Operations
- **Access**: O(n) - Must traverse from head
- **Search**: O(n) - Linear traversal
- **Insertion**: O(1) if position is known, O(n) otherwise
- **Deletion**: O(1) if position is known, O(n) otherwise

### Common Interview Problems
1. Reverse a linked list
2. Detect cycle using Floyd's algorithm (fast and slow pointers)
3. Find middle element
4. Merge two sorted linked lists

---

## Trees

A **tree** is a hierarchical data structure with a root node and subtrees of children nodes.

### Binary Tree
A tree where each node has at most two children (left and right).

### Binary Search Tree (BST)
A binary tree where:
- Left subtree contains nodes with keys less than the parent
- Right subtree contains nodes with keys greater than the parent

### Tree Traversals
1. **Inorder** (Left, Root, Right): Gives sorted order for BST
2. **Preorder** (Root, Left, Right): Used for copying trees
3. **Postorder** (Left, Right, Root): Used for deleting trees
4. **Level Order**: BFS traversal using queue

### Balanced Trees
- **AVL Tree**: Self-balancing BST with height difference ≤ 1
- **Red-Black Tree**: Self-balancing with color properties
- **B-Tree**: Used in databases and file systems

---

## Graphs

A **graph** G = (V, E) consists of vertices V and edges E connecting pairs of vertices.

### Graph Representations
1. **Adjacency Matrix**: O(V²) space, O(1) edge lookup
2. **Adjacency List**: O(V + E) space, efficient for sparse graphs

### Graph Traversals
- **BFS (Breadth-First Search)**: Uses queue, finds shortest path in unweighted graphs
- **DFS (Depth-First Search)**: Uses stack/recursion, used for topological sort, cycle detection

### Important Graph Algorithms
1. **Dijkstra's Algorithm**: Single-source shortest path (non-negative weights)
2. **Bellman-Ford**: Shortest path with negative weights
3. **Floyd-Warshall**: All-pairs shortest path
4. **Kruskal's Algorithm**: Minimum spanning tree using Union-Find
5. **Prim's Algorithm**: Minimum spanning tree using priority queue
6. **Topological Sort**: Linear ordering of DAG vertices

---

## Sorting Algorithms

### Comparison-Based Sorting

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |

### Non-Comparison Sorting
- **Counting Sort**: O(n + k), for small integer ranges
- **Radix Sort**: O(d × (n + k)), for integers with d digits
- **Bucket Sort**: O(n + k), for uniformly distributed data

---

## Searching Algorithms

### Binary Search
Searches a sorted array by repeatedly dividing the search interval in half.
- **Time Complexity**: O(log n)
- **Requirement**: Array must be sorted

### Binary Search Variations
1. Find first occurrence of element
2. Find last occurrence of element
3. Find floor/ceiling of element
4. Search in rotated sorted array

---

## Hash Tables

A **hash table** uses a hash function to map keys to array indices for O(1) average-case operations.

### Collision Resolution
1. **Chaining**: Store colliding elements in a linked list
2. **Open Addressing**: 
   - Linear probing
   - Quadratic probing
   - Double hashing

### Load Factor
α = n/m where n is elements and m is table size.
- Chaining: Performance degrades linearly with α
- Open Addressing: Typically keep α < 0.7

---

## Dynamic Programming

**Dynamic Programming** solves problems by breaking them into overlapping subproblems and storing solutions.

### Key Concepts
1. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems**: Same subproblems are solved multiple times
3. **Memoization**: Top-down approach with caching
4. **Tabulation**: Bottom-up approach with table

### Classic DP Problems
1. Fibonacci sequence
2. Longest Common Subsequence (LCS)
3. Longest Increasing Subsequence (LIS)
4. 0/1 Knapsack problem
5. Edit distance
6. Matrix chain multiplication
7. Coin change problem

---

## Time Complexity

### Big O Notation
- O(1): Constant time
- O(log n): Logarithmic time
- O(n): Linear time
- O(n log n): Linearithmic time
- O(n²): Quadratic time
- O(2ⁿ): Exponential time
- O(n!): Factorial time

### Space Complexity
Consider both:
1. Auxiliary space (extra space used)
2. Total space (input + auxiliary)

# Editorial

## Approach A - Foundational

Use recursion and track depth; append values into depth-indexed lists.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Approach B - Optimized

Use a queue for breadth-first traversal and process one level at a time.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Trade-offs

Queue-based BFS maps directly to the requested output shape and is often easier to reason about for level grouping.

## Recommendation labels

- Interview Recommended: queue-bfs
- Production Practical: queue-bfs
- Advanced: iterative deque optimizations

# Editorial

## Approach A - Foundational

For each land cell, run DFS/BFS to mark all connected land as visited.

- Time complexity: `O(rows * cols)`
- Space complexity: `O(rows * cols)` worst-case recursion/queue

## Approach B - Optimized

In-place flood fill to avoid separate visited matrix.

- Time complexity: `O(rows * cols)`
- Space complexity: `O(rows * cols)` recursion stack worst-case

## Trade-offs

In-place marking saves memory and is common in interviews.

## Recommendation labels

- Interview Recommended: dfs-flood-fill
- Production Practical: iterative bfs for stack safety
- Advanced: union-find batch processing

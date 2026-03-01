# Editorial

## Approach A - Foundational

Use two nested loops and check every pair.

- Time complexity: `O(n^2)`
- Space complexity: `O(1)`

## Approach B - Optimized

Use a hash map to store seen values and their indices while iterating once.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Trade-offs

The nested-loop approach is straightforward but too slow for large input sizes. The hash approach is interview-friendly and scales better at the cost of additional memory.

## Recommendation labels

- Interview Recommended: hash-map single pass
- Production Practical: hash-map single pass
- Advanced: none required

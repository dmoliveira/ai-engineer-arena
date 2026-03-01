# Editorial

## Approach A - Foundational

Compare every interval pair and repeatedly merge until stable.

- Time complexity: `O(n^2)`
- Space complexity: `O(n)`

## Approach B - Optimized

Sort by start time, then scan once while merging into an output list.

- Time complexity: `O(n log n)`
- Space complexity: `O(n)`

## Trade-offs

The sort-and-scan strategy is standard, concise, and performant for large inputs.

## Recommendation labels

- Interview Recommended: sort-then-scan
- Production Practical: sort-then-scan
- Advanced: interval trees for dynamic updates

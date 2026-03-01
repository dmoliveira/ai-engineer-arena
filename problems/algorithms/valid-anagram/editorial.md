# Editorial

## Approach A - Foundational

Sort both strings and compare.

- Time complexity: `O(n log n)`
- Space complexity: `O(n)`

## Approach B - Optimized

Count each character frequency and compare count maps.

- Time complexity: `O(n)`
- Space complexity: `O(1)` for fixed alphabet, else `O(k)`

## Trade-offs

Sorting is concise and common. Frequency counting is faster for large inputs and preferred in interviews when linear time is required.

## Recommendation labels

- Interview Recommended: frequency-count
- Production Practical: frequency-count
- Advanced: unicode-normalized variant

# Editorial

## Approach A - Foundational

Loop through each probability and append `1` or `0`.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Approach B - Optimized

Use a list comprehension for concise vector-like mapping.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Trade-offs

Both are linear. Comprehensions are concise; explicit loops are easier for debugging and extension.

## Recommendation labels

- Interview Recommended: list-comprehension threshold
- Production Practical: vectorized implementation in NumPy/pandas
- Advanced: threshold tuning by precision-recall objective

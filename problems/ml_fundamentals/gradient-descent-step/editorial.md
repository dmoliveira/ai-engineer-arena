# Editorial

## Approach A - Foundational

Iterate by index and apply the update formula.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Approach B - Optimized

Use `zip(weights, gradients)` and list comprehension for cleaner code.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Trade-offs

Both are linear. The `zip` version reduces indexing mistakes and improves readability.

## Recommendation labels

- Interview Recommended: zip + formula
- Production Practical: vectorized tensor libraries
- Advanced: adaptive optimizers (Adam, RMSProp)

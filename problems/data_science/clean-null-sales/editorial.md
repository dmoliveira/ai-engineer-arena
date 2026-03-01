# Editorial

## Approach A - Foundational

Loop through rows and append valid rows to a result list.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Approach B - Optimized

Use a list comprehension with a helper predicate for cleaner logic.

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Trade-offs

Both approaches are linear. A helper predicate can improve readability and testability for larger ETL-style pipelines.

## Recommendation labels

- Interview Recommended: single-pass-filter
- Production Practical: predicate + list comprehension
- Advanced: schema-validation layer

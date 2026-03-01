# Editorial

## Approach A - Foundational

Run multiple scans: one pass per IP candidate. This is simple but too expensive.

## Approach B - Optimized

Use one pipeline:

```bash
grep ' ERROR ' app.log | awk '{print $1}' | sort | uniq -c | awk '{print $2, $1}' | sort -k2,2nr -k1,1 | head -n "$k"
```

## Trade-offs

A single pipeline is much faster for large files and is easier to automate.

## Recommendation labels

- Interview Recommended: one-pass aggregation pipeline
- Production Practical: same pipeline with format guards
- Advanced: streaming aggregation with awk-only script

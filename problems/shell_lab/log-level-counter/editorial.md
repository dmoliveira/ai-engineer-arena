# Editorial

## Approach A - Foundational

Use `grep` separately for each level and count with `wc -l`.

## Approach B - Optimized

Single pipeline:

```bash
cut -d' ' -f2 app.log | sort | uniq -c | awk '{print $2, $1}'
```

## Trade-offs

Multiple greps are simple but repeated scans are slower for large files. A single pipeline scans once and is better for scale.

## Recommendation labels

- Interview Recommended: single pipeline
- Production Practical: single pipeline with robust parsing
- Advanced: streaming parser with `awk`

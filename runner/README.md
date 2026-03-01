# Runner MVP

Run local Python solutions against public and hidden tests.

## Usage

```bash
python3 runner/run_problem.py \
  --problem-dir problems/algorithms/two-sum-hash \
  --solution examples/solutions/two_sum_hash.py
```

Public-only mode:

```bash
python3 runner/run_problem.py \
  --problem-dir problems/algorithms/two-sum-hash \
  --solution examples/solutions/two_sum_hash.py \
  --public-only
```

## Notes

- Runner expects a function named `solve` by default.
- `tests/public.json` may override function name via a `function` field.
- Hidden tests without explicit `expected` values are skipped in this MVP.

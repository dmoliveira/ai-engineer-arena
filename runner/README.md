# Runner

Run local Python solutions against public and hidden tests with timeout and safety guards.

## Usage

```bash
python3 runner/run_problem.py \
  --problem-dir problems/algorithms/two-sum-hash \
  --solution examples/solutions/two_sum_hash.py
```

Shell challenge runner:

```bash
python3 runner/run_shell_problem.py \
  --problem-dir problems/shell_lab/log-level-counter \
  --command "cut -d' ' -f2 {input_file} | sort | uniq -c | awk '{print $2, $1}'"
```

Public-only mode:

```bash
python3 runner/run_problem.py \
  --problem-dir problems/algorithms/two-sum-hash \
  --solution examples/solutions/two_sum_hash.py \
  --public-only
```

Custom fallback timeout per test:

```bash
python3 runner/run_problem.py \
  --problem-dir problems/algorithms/merge-intervals \
  --solution examples/solutions/merge_intervals.py \
  --timeout-ms 600
```

## Output notes

- Runner expects a function named `solve` by default.
- `tests/public.json` may override function name via a `function` field.
- Hidden tests without explicit `expected` values are skipped.
- `benchmark_tier` is `strict` when runtime limits are available for all executed tests; otherwise `advisory`.
- Runtime is enforced with per-test process timeouts; memory metrics are advisory.

## Safety notes

- Basic AST validation blocks dangerous calls (`exec`, `eval`, `open`, `compile`, `__import__`).
- Imports are restricted to an allowlist (plus optional `allowed_imports` in `tests/public.json`).

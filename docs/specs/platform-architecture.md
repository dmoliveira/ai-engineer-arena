# Platform Architecture (Phase 1)

## Goals

- Serve a static learning platform on GitHub Pages.
- Support Python 3 challenge execution in-browser for sample tests.
- Keep hidden/stress validation local for now.
- Maintain a local-first persistence model with no backend dependency.

## High-level architecture

```text
problem packs (yaml + tests + editorial)
            |
            v
      local runner (python)
            |
            v
   static web app (github pages)
            |
            v
 browser execution (pyodide) + localStorage progress
```

## Repository modules

- `problems/`: canonical content for challenge packs.
- `runner/`: Python evaluator for local correctness/performance checks.
- `web/`: static UI for browsing and executing sample tests.
- `docs/`: planning, specs, and contribution standards.

## Problem pack contract

Each problem folder should contain:

- `problem.yaml`
- `statement.md`
- `tests/public.json`
- `tests/hidden.json`
- `editorial.md`

Required metadata:

- `id`
- `title`
- `difficulty` (`easy|medium|hard`)
- `category`
- `tags`
- `constraints`
- `recommended_approach`

## Evaluation flow

### Local runner

1. load problem metadata and tests
2. execute user solution with timeout guards
3. evaluate correctness on public + hidden tests
4. measure runtime totals and average
5. record memory estimate where applicable
6. export result payload for CLI/web rendering

### Browser runner

1. load Pyodide runtime on demand
2. run solution against public sample tests only
3. return pass/fail and runtime advisory stats
4. persist run history in `localStorage`

## Constraints and compatibility

- GitHub Pages static hosting only (no server-side code).
- Browser metrics are advisory and may vary by client hardware.
- Hidden tests remain local to reduce brute-force overfitting.
- No authentication in phase 1.

## Security and safety baseline

- Restrict imports in local runner allowlist.
- Isolate execution with per-test timeout.
- Avoid shell access in browser runner.
- Keep challenge assets free of secrets.

## Observability baseline

- local runner prints deterministic JSON result payload.
- web UI displays pass counts, runtime summaries, and trend chart.
- optional local logs in `*.log` files excluded by `.gitignore`.

## Future extension points

- multi-language runners (C/C++, Rust, Go, Java, JS, R, Julia)
- remote submission API and account persistence
- global leaderboard and cohort tracks
- dynamic recommendation engine by user weak-topic profile

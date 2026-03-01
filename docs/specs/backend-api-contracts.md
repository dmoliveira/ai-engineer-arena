# Backend API Contracts (Future)

This document defines API contracts for future backend integration while keeping the current local-first architecture.

## Principles

- Keep current problem-pack schema as source of truth.
- Support stateless evaluation requests and deterministic result payloads.
- Version APIs to avoid breaking clients.

## Endpoints (v1 draft)

### `GET /api/v1/problems`

- Query: `topic`, `difficulty`, `tag`, `page`, `page_size`, `track`
- Response: paginated problem metadata list

### `GET /api/v1/problems/{id}`

- Response: full problem metadata + statement + public tests

### `POST /api/v1/submissions`

- Body:
  - `problem_id`
  - `language`
  - `source_code`
  - `mode` (`public` or `full`)
- Response:
  - pass/fail summary
  - runtime/memory stats
  - failed test identifiers
  - benchmark tier (`strict`/`advisory`)

### `GET /api/v1/progress/{user_id}`

- Response:
  - solved ids
  - topic completion stats
  - streak metrics

## Response contract example

```json
{
  "submission_id": "sub_123",
  "problem_id": "two-sum-hash",
  "passed": 8,
  "total": 8,
  "pass_rate": 100.0,
  "avg_runtime_ms": 1.27,
  "max_memory_peak_bytes": 129024,
  "benchmark_tier": "strict",
  "failed_tests": []
}
```

## Migration notes

- `web/full-catalog.json` can map directly to `GET /problems` responses.
- Current runner outputs should remain compatible with API submission responses.
- Hidden tests stay server-side when backend is enabled.

# Problem Pack Contract

This document defines the minimum required structure and schema for each challenge package.

## Directory contract

```text
problems/<category>/<problem-id>/
├── problem.yaml
├── statement.md
├── editorial.md
└── tests/
    ├── public.json
    └── hidden.json
```

## `problem.yaml` schema

Required fields:

- `id` (string, kebab-case, unique)
- `title` (string)
- `difficulty` (`easy|medium|hard`)
- `category` (string)
- `tags` (string array)
- `constraints` (string array)
- `languages` (string array)
- `recommended_approach` (string)
- `interview_recommended` (boolean)

## `tests/public.json` schema

```json
{
  "tests": [
    {
      "name": "string",
      "input": {},
      "expected": {}
    }
  ]
}
```

Guidelines:

- include simple and edge-case examples
- keep these visible to users

## `tests/hidden.json` schema

```json
{
  "tests": [
    {
      "name": "string",
      "generator": "string",
      "seed": 0,
      "size": 1000,
      "runtime_limit_ms": 500
    }
  ]
}
```

Guidelines:

- include stress and anti-bruteforce cases
- may include static fixtures or generator config
- hidden tests are not displayed in the web client

## Editorial minimum quality

- at least two approaches for standard algorithm problems
- complexity included for each approach
- trade-off discussion included
- recommendation labels included

# Count Log Levels in a File

## Description

Given a log file with entries like:

```text
2026-01-01T10:00:00Z INFO service started
2026-01-01T10:01:12Z ERROR db timeout
```

Print counts per level in alphabetical order.

## Input

- path to `app.log`

## Output

```text
ERROR 12
INFO 205
WARN 33
```

## Hints

- Start with one tool (`grep`).
- Evolve to a pipeline (`cut`, `sort`, `uniq -c`, `awk`).

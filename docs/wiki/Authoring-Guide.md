# Authoring Guide

## Create a new problem

```bash
python3 scripts/new_problem.py --id sample-problem --title "Sample Problem" --category algorithms --difficulty easy
```

## Validate before commit

```bash
make validate
make quality
make build-catalog
```

## Quality targets

- clear statement
- at least one public test
- hidden regression/stress test
- editorial trade-off notes

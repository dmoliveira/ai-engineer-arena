#!/usr/bin/env python3
"""Generate additional seed problem packs for catalog expansion."""

from __future__ import annotations

import json
from pathlib import Path

SEEDS = [
    (
        "algorithms",
        "sliding-window-max-sum",
        "Sliding Window Max Sum",
        "medium",
        "python",
    ),
    ("algorithms", "first-unique-char", "First Unique Character", "easy", "python"),
    (
        "algorithms",
        "kth-smallest-sorted-matrix",
        "Kth Smallest in Sorted Matrix",
        "hard",
        "python",
    ),
    (
        "algorithms",
        "detect-cycle-directed-graph",
        "Detect Cycle in Directed Graph",
        "medium",
        "python",
    ),
    ("algorithms", "min-stack-ops", "Min Stack Operations", "easy", "python"),
    (
        "data_science",
        "normalize-min-max-column",
        "Normalize Min-Max Column",
        "easy",
        "python",
    ),
    (
        "data_science",
        "group-mean-by-region",
        "Group Mean by Region",
        "medium",
        "python",
    ),
    ("data_science", "iqr-outlier-flag", "IQR Outlier Flagging", "medium", "python"),
    (
        "data_science",
        "rolling-average-window",
        "Rolling Average Window",
        "easy",
        "python",
    ),
    (
        "data_science",
        "dedupe-latest-record",
        "Deduplicate Latest Record",
        "hard",
        "python",
    ),
    (
        "ml_fundamentals",
        "binary-confusion-metrics",
        "Binary Confusion Metrics",
        "easy",
        "python",
    ),
    (
        "ml_fundamentals",
        "train-val-split-index",
        "Train Validation Split Index",
        "easy",
        "python",
    ),
    (
        "ml_fundamentals",
        "sgd-mini-batch-step",
        "SGD Mini-Batch Step",
        "medium",
        "python",
    ),
    (
        "ml_fundamentals",
        "precision-recall-threshold",
        "Precision Recall at Threshold",
        "medium",
        "python",
    ),
    ("ml_fundamentals", "early-stop-criteria", "Early Stop Criteria", "hard", "python"),
    (
        "shell_lab",
        "grep-count-unique-users",
        "Grep Count Unique Users",
        "easy",
        "shell",
    ),
    ("shell_lab", "csv-column-extract", "CSV Column Extract", "easy", "shell"),
    ("shell_lab", "top-response-codes", "Top Response Codes", "medium", "shell"),
    ("shell_lab", "join-two-files-on-key", "Join Two Files on Key", "medium", "shell"),
    ("shell_lab", "stream-anomaly-lines", "Stream Anomaly Lines", "hard", "shell"),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_problem(
    root: Path, category: str, problem_id: str, title: str, difficulty: str, track: str
) -> None:
    problem_dir = root / "problems" / category / problem_id
    if problem_dir.exists():
        return

    yaml_text = f"""id: {problem_id}
title: {title}
difficulty: {difficulty}
category: {category}
tags:
  - seed
constraints:
  - \"define realistic bounds\"
languages:
  - {track}
recommended_approach: reference-solution
interview_recommended: true
"""

    statement = f"""# {title}

## Description

Seed practice problem for {category}.

## Input

- See test payload.

## Output

- Return expected value for each case.
"""

    editorial = """# Editorial

## Approach A - Foundational

- Time complexity: `O(n)`
- Space complexity: `O(n)`

## Approach B - Optimized

- Time complexity: `O(n)`
- Space complexity: `O(1)` where applicable

## Trade-offs

Prefer clarity first, then optimize for constraints.
"""

    if track == "shell":
        public = {
            "tests": [
                {
                    "name": "example",
                    "input": "example.log",
                    "expected": ["TODO"],
                }
            ]
        }
        write(problem_dir / "tests" / "fixtures" / "example.log", "TODO\n")
    else:
        public = {
            "function": "solve",
            "tests": [
                {
                    "name": "example",
                    "input": {"values": [1, 2, 3]},
                    "expected": 6,
                    "runtime_limit_ms": 600,
                }
            ],
        }

    hidden = {"tests": []}

    write(problem_dir / "problem.yaml", yaml_text)
    write(problem_dir / "statement.md", statement)
    write(problem_dir / "editorial.md", editorial)
    write(problem_dir / "tests" / "public.json", json.dumps(public, indent=2) + "\n")
    write(problem_dir / "tests" / "hidden.json", json.dumps(hidden, indent=2) + "\n")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    for seed in SEEDS:
        make_problem(repo_root, *seed)
    print(f"generated {len(SEEDS)} seed problem packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

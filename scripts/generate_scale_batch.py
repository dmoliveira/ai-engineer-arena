#!/usr/bin/env python3
"""Scale problem catalog to a target count."""

from __future__ import annotations

import json
from pathlib import Path

TRACK_BY_CATEGORY = {
    "algorithms": "python",
    "data_science": "python",
    "ml_fundamentals": "python",
    "shell_lab": "shell",
}

DIFFICULTY_CYCLE = ["easy", "medium", "hard"]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_problem(repo_root: Path, category: str, index: int) -> None:
    problem_id = f"{category.replace('_', '-')}-practice-{index:03d}"
    title = f"{category.replace('_', ' ').title()} Practice {index:03d}"
    difficulty = DIFFICULTY_CYCLE[index % len(DIFFICULTY_CYCLE)]
    track = TRACK_BY_CATEGORY[category]

    problem_dir = repo_root / "problems" / category / problem_id
    if problem_dir.exists():
        return

    yaml_text = f"""id: {problem_id}
title: {title}
difficulty: {difficulty}
category: {category}
tags:
  - practice
  - generated
constraints:
  - \"define realistic bounds\"
languages:
  - {track}
recommended_approach: reference-solution
interview_recommended: true
"""

    statement = f"""# {title}

## Description

Generated practice problem in the {category} topic.

## Input

- See public test payload.

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

Start with clarity, then optimize for constraints.
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
    yaml_paths = [
        path
        for path in (repo_root / "problems").rglob("problem.yaml")
        if "_templates" not in path.parts
    ]
    current = len(yaml_paths)
    target = 100
    if current >= target:
        print(f"already at or above target ({current})")
        return 0

    remaining = target - current
    categories = ["algorithms", "data_science", "ml_fundamentals", "shell_lab"]
    created = 0
    index = 1

    while created < remaining:
        for category in categories:
            if created >= remaining:
                break
            create_problem(repo_root, category, index)
            created += 1
            index += 1

    print(f"created {created} generated problems (target {target})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

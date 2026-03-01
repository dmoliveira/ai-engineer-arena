#!/usr/bin/env python3
"""Scaffold a new problem pack quickly."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_CATEGORIES = {"algorithms", "data_science", "ml_fundamentals", "shell_lab"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a problem scaffold")
    parser.add_argument("--id", required=True, help="Problem id in kebab-case")
    parser.add_argument("--title", required=True, help="Problem title")
    parser.add_argument("--category", required=True, choices=sorted(VALID_CATEGORIES))
    parser.add_argument(
        "--difficulty", required=True, choices=sorted(VALID_DIFFICULTIES)
    )
    parser.add_argument("--track", choices=["python", "shell"], default="python")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    problem_dir = repo_root / "problems" / args.category / args.id
    if problem_dir.exists():
        raise SystemExit(f"Problem already exists: {problem_dir}")

    problem_yaml = f"""id: {args.id}
title: {args.title}
difficulty: {args.difficulty}
category: {args.category}
tags:
  - starter
constraints:
  - \"define constraints\"
languages:
  - {args.track}
recommended_approach: TODO
interview_recommended: true
"""

    statement = f"""# {args.title}

## Description

Describe the problem.

## Input

- Define input payload.

## Output

- Define output payload.
"""

    editorial = """# Editorial

## Approach A - Foundational

- Time complexity: `O(...)`
- Space complexity: `O(...)`

## Approach B - Optimized

- Time complexity: `O(...)`
- Space complexity: `O(...)`

## Trade-offs

Explain when to choose each approach.
"""

    public_payload = {
        "function": "solve",
        "tests": [{"name": "example", "input": {}, "expected": {}}],
    }
    if args.track == "shell":
        public_payload = {
            "tests": [
                {
                    "name": "example",
                    "input": "example.log",
                    "expected": ["TODO"],
                }
            ]
        }

    hidden_payload = {"tests": []}

    write(problem_dir / "problem.yaml", problem_yaml)
    write(problem_dir / "statement.md", statement)
    write(problem_dir / "editorial.md", editorial)
    write(
        problem_dir / "tests" / "public.json",
        json.dumps(public_payload, indent=2) + "\n",
    )
    write(
        problem_dir / "tests" / "hidden.json",
        json.dumps(hidden_payload, indent=2) + "\n",
    )

    if args.track == "shell":
        write(problem_dir / "tests" / "fixtures" / "example.log", "TODO\n")

    print(f"Created problem scaffold at {problem_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

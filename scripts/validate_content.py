#!/usr/bin/env python3
"""Validate challenge content contracts with zero external dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_YAML_KEYS = {
    "id",
    "title",
    "difficulty",
    "category",
    "tags",
    "constraints",
    "languages",
    "recommended_approach",
    "interview_recommended",
}


def parse_top_level_yaml_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            continue
        keys.add(line.split(":", 1)[0].strip())
    return keys


def validate_problem_pack(problem_dir: Path) -> list[str]:
    errors: list[str] = []

    required_files = [
        "problem.yaml",
        "statement.md",
        "editorial.md",
        "tests/public.json",
        "tests/hidden.json",
    ]
    for relative in required_files:
        if not (problem_dir / relative).exists():
            errors.append(f"missing file: {problem_dir / relative}")

    yaml_path = problem_dir / "problem.yaml"
    if yaml_path.exists():
        keys = parse_top_level_yaml_keys(yaml_path)
        missing = sorted(REQUIRED_YAML_KEYS - keys)
        if missing:
            errors.append(f"missing yaml keys in {yaml_path}: {', '.join(missing)}")

    for json_relative in ("tests/public.json", "tests/hidden.json"):
        json_path = problem_dir / json_relative
        if not json_path.exists():
            continue
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json at {json_path}: {exc}")
            continue

        tests = payload.get("tests")
        if not isinstance(tests, list):
            errors.append(f"tests must be a list in {json_path}")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    problems_root = repo_root / "problems"

    problem_dirs = [
        path
        for path in problems_root.rglob("problem.yaml")
        if "_templates" not in path.parts
    ]

    errors: list[str] = []
    for yaml_file in problem_dirs:
        errors.extend(validate_problem_pack(yaml_file.parent))

    web_catalog = repo_root / "web" / "problems.json"
    try:
        json.loads(web_catalog.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"invalid web catalog {web_catalog}: {exc}")

    if errors:
        print("content validation failed")
        for item in errors:
            print(f"- {item}")
        return 1

    print(f"content validation passed ({len(problem_dirs)} problem packs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

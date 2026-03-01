#!/usr/bin/env python3
"""Validate challenge content contracts with typed checks."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DIFFICULTIES = {"easy", "medium", "hard"}
VALID_CATEGORIES = {"algorithms", "data_science", "ml_fundamentals", "shell_lab"}
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


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(stripped[2:].strip())
            continue

        if line.startswith(" "):
            continue

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        current_key = key

        if value == "":
            data[key] = []
            continue

        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
            continue

        data[key] = value.strip('"')

    return data


def validate_problem_yaml(problem_dir: Path, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    missing = sorted(REQUIRED_YAML_KEYS - set(payload.keys()))
    if missing:
        errors.append(
            f"missing yaml keys in {problem_dir / 'problem.yaml'}: {', '.join(missing)}"
        )
        return errors

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(payload["id"])):
        errors.append(f"invalid id format in {problem_dir / 'problem.yaml'}")

    if payload["id"] != problem_dir.name:
        errors.append(
            f"id must match folder name for {problem_dir}: {payload['id']} != {problem_dir.name}"
        )

    if payload["difficulty"] not in DIFFICULTIES:
        errors.append(f"invalid difficulty in {problem_dir / 'problem.yaml'}")

    category = payload["category"]
    if category not in VALID_CATEGORIES:
        errors.append(f"invalid category in {problem_dir / 'problem.yaml'}")
    elif category != problem_dir.parent.name:
        errors.append(
            f"category mismatch in {problem_dir / 'problem.yaml'}: {category} != {problem_dir.parent.name}"
        )

    for key in ("tags", "constraints", "languages"):
        value = payload.get(key)
        if not isinstance(value, list) or not value:
            errors.append(
                f"{key} must be a non-empty list in {problem_dir / 'problem.yaml'}"
            )

    if not isinstance(payload.get("interview_recommended"), bool):
        errors.append(
            f"interview_recommended must be boolean in {problem_dir / 'problem.yaml'}"
        )

    if not str(payload["title"]).strip():
        errors.append(f"title must be non-empty in {problem_dir / 'problem.yaml'}")
    if not str(payload["recommended_approach"]).strip():
        errors.append(
            f"recommended_approach must be non-empty in {problem_dir / 'problem.yaml'}"
        )

    return errors


def validate_test_payload(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid json at {path}: {exc}"]

    tests = payload.get("tests")
    if not isinstance(tests, list):
        return [f"tests must be a list in {path}"]

    for index, test in enumerate(tests):
        if not isinstance(test, dict):
            errors.append(f"test entry #{index} must be an object in {path}")
            continue
        if "name" not in test or not str(test["name"]).strip():
            errors.append(f"test entry #{index} missing name in {path}")
        if "expected" in test and "input" not in test:
            errors.append(
                f"test entry #{index} has expected but missing input in {path}"
            )

    return errors


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
        payload = parse_simple_yaml(yaml_path)
        errors.extend(validate_problem_yaml(problem_dir, payload))

    for json_relative in ("tests/public.json", "tests/hidden.json"):
        path = problem_dir / json_relative
        if path.exists():
            errors.extend(validate_test_payload(path))

    return errors


def validate_web_catalog(repo_root: Path, known_problem_ids: set[str]) -> list[str]:
    errors: list[str] = []
    web_catalog = repo_root / "web" / "problems.json"

    try:
        payload = json.loads(web_catalog.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"invalid web catalog {web_catalog}: {exc}"]

    if not isinstance(payload, list):
        return [f"web catalog must be a list in {web_catalog}"]

    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            errors.append(f"catalog entry #{index} must be object in {web_catalog}")
            continue
        problem_id = item.get("id")
        if not isinstance(problem_id, str) or not problem_id:
            errors.append(f"catalog entry #{index} missing id in {web_catalog}")
            continue
        if problem_id not in known_problem_ids:
            errors.append(f"catalog entry references unknown problem id: {problem_id}")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    problems_root = repo_root / "problems"

    yaml_paths = [
        path
        for path in problems_root.rglob("problem.yaml")
        if "_templates" not in path.parts
    ]

    errors: list[str] = []
    problem_ids: set[str] = set()

    for yaml_file in yaml_paths:
        problem_ids.add(yaml_file.parent.name)
        errors.extend(validate_problem_pack(yaml_file.parent))

    errors.extend(validate_web_catalog(repo_root, problem_ids))

    if errors:
        print("content validation failed")
        for item in errors:
            print(f"- {item}")
        return 1

    print(f"content validation passed ({len(yaml_paths)} problem packs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

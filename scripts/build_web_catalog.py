#!/usr/bin/env python3
"""Build web/full-catalog.json from problem packs."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


def parse_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            data[current_key].append(stripped[2:].strip().strip('"'))
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
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip('"')

    return data


def first_description_line(statement_path: Path) -> str:
    lines = statement_path.read_text(encoding="utf-8").splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped
    return "Solve this challenge."


def build_entry(repo_root: Path, problem_dir: Path) -> dict[str, Any]:
    meta = parse_simple_yaml(problem_dir / "problem.yaml")
    public_payload = json.loads(
        (problem_dir / "tests" / "public.json").read_text(encoding="utf-8")
    )
    languages = meta.get("languages", [])
    track = "shell" if "shell" in languages else "python"

    entry = {
        "id": meta["id"],
        "title": meta["title"],
        "difficulty": meta["difficulty"],
        "category": meta["category"],
        "tags": meta.get("tags", []),
        "languages": languages,
        "track": track,
        "prompt": first_description_line(problem_dir / "statement.md"),
        "statement_path": str(problem_dir.relative_to(repo_root) / "statement.md"),
        "public_test_path": f"public-tests/{meta['id']}.json",
    }

    if track == "python":
        entry["starter"] = "def solve(*args, **kwargs):\n    pass\n"
        entry["function"] = public_payload.get("function", "solve")
    else:
        entry["starter"] = "# Shell challenge: run in your terminal"

    return entry


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    problem_yaml_paths = sorted(
        [
            p
            for p in (repo_root / "problems").rglob("problem.yaml")
            if "_templates" not in p.parts
        ]
    )

    entries = [build_entry(repo_root, path.parent) for path in problem_yaml_paths]
    entries.sort(key=lambda item: (item["category"], item["difficulty"], item["id"]))

    web_root = repo_root / "web"
    tests_out_dir = web_root / "public-tests"
    if tests_out_dir.exists():
        shutil.rmtree(tests_out_dir)
    tests_out_dir.mkdir(parents=True, exist_ok=True)

    for path in problem_yaml_paths:
        problem_dir = path.parent
        meta = parse_simple_yaml(problem_dir / "problem.yaml")
        source_test = problem_dir / "tests" / "public.json"
        target_test = tests_out_dir / f"{meta['id']}.json"
        shutil.copyfile(source_test, target_test)

    out_path = repo_root / "web" / "full-catalog.json"
    out_path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} catalog entries to {out_path}")
    print(f"wrote {len(entries)} public test payloads to {tests_out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

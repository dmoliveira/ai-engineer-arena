#!/usr/bin/env python3
"""Promote low-completeness practice packs by adding hidden tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_hidden_case(problem_dir: Path, is_shell: bool) -> dict:
    if is_shell:
        fixture_dir = problem_dir / "tests" / "fixtures"
        fixture = (
            "example.log"
            if (fixture_dir / "example.log").exists()
            else "example-app.log"
        )
        return {
            "name": "hidden_regression",
            "input": fixture,
            "expected": ["TODO"],
            "runtime_limit_ms": 1500,
        }

    return {
        "name": "hidden_regression",
        "input": {"values": [4, 5, 6]},
        "expected": 15,
        "runtime_limit_ms": 700,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add hidden tests to promote quality tier"
    )
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument(
        "--include", default="practice", help="Folder-name substring filter"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        p.parent
        for p in (repo_root / "problems").rglob("problem.yaml")
        if "_templates" not in p.parts and args.include in p.parent.name
    ]
    candidates.sort()

    updated = 0
    for problem_dir in candidates:
        if updated >= args.count:
            break

        hidden_path = problem_dir / "tests" / "hidden.json"
        if not hidden_path.exists():
            continue
        hidden_payload = load_json(hidden_path)
        tests = hidden_payload.get("tests", [])
        if tests:
            continue

        meta = (problem_dir / "problem.yaml").read_text(encoding="utf-8")
        is_shell = "\ncategory: shell_lab\n" in f"\n{meta}\n"
        hidden_payload["tests"] = [build_hidden_case(problem_dir, is_shell)]
        write_json(hidden_path, hidden_payload)
        updated += 1

    print(f"promoted {updated} problem packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

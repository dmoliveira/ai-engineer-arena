#!/usr/bin/env python3
"""Score problem packs and enforce a minimum quality gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def score_problem(problem_dir: Path) -> tuple[int, dict[str, int]]:
    statement = problem_dir / "statement.md"
    editorial = problem_dir / "editorial.md"
    public_tests = problem_dir / "tests" / "public.json"
    hidden_tests = problem_dir / "tests" / "hidden.json"
    meta = problem_dir / "problem.yaml"

    public_payload = json.loads(public_tests.read_text(encoding="utf-8"))
    hidden_payload = json.loads(hidden_tests.read_text(encoding="utf-8"))
    public_count = len(public_payload.get("tests", []))
    hidden_count = len(hidden_payload.get("tests", []))
    statement_lines = count_lines(statement)
    editorial_lines = count_lines(editorial)
    meta_text = meta.read_text(encoding="utf-8")

    breakdown = {
        "metadata": 20 if "recommended_approach:" in meta_text else 10,
        "statement_depth": 15 if statement_lines >= 10 else 8,
        "editorial_depth": 15 if editorial_lines >= 12 else 8,
        "public_tests": 25 if public_count >= 1 else 0,
        "hidden_tests": 15 if hidden_count >= 1 else 10,
    }
    return sum(breakdown.values()), breakdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Score and gate problem quality")
    parser.add_argument("--min-score", type=int, default=70)
    parser.add_argument("--target-gold", type=int, default=30)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    yaml_paths = [
        p
        for p in (repo_root / "problems").rglob("problem.yaml")
        if "_templates" not in p.parts
    ]

    report = []
    for yaml_path in yaml_paths:
        score, breakdown = score_problem(yaml_path.parent)
        report.append(
            {
                "id": yaml_path.parent.name,
                "category": yaml_path.parent.parent.name,
                "score": score,
                "tier": "gold"
                if score >= 90
                else "silver"
                if score >= args.min_score
                else "bronze",
                "breakdown": breakdown,
            }
        )

    report.sort(key=lambda item: (-item["score"], item["id"]))
    gold_count = sum(1 for item in report if item["tier"] == "gold")
    low = [item for item in report if item["score"] < args.min_score]

    out_path = repo_root / "docs" / "specs" / "problem-quality-report.json"
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"scored {len(report)} problems; gold={gold_count}; low={len(low)}")
    if low:
        print("failing problem ids:")
        for item in low[:20]:
            print(f"- {item['id']} ({item['score']})")
        return 1

    if gold_count < args.target_gold:
        print(f"gold target not met: {gold_count} < {args.target_gold}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

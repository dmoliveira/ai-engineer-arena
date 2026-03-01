#!/usr/bin/env python3
"""Run shell challenge commands against public tests."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT_MS = 1500


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_lines(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def evaluate_case(
    command_template: str,
    problem_dir: Path,
    case: dict[str, Any],
    timeout_ms: int,
) -> dict[str, Any]:
    test_name = case.get("name", "unnamed")
    fixture = case.get("input")
    if not fixture:
        return {
            "name": test_name,
            "passed": False,
            "error": "Missing input fixture in test payload",
        }

    input_file = problem_dir / "tests" / "fixtures" / fixture
    args = case.get("args", {})
    command = command_template.replace("{input_file}", shlex.quote(str(input_file)))
    for key, value in args.items():
        command = command.replace(f"{{{key}}}", str(value))

    started = time.perf_counter()
    try:
        proc = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True,
            text=True,
            timeout=timeout_ms / 1000,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "name": test_name,
            "passed": False,
            "runtime_ms": float(timeout_ms),
            "expected": case.get("expected", []),
            "output": [],
            "error": f"TimeoutError: exceeded {timeout_ms}ms",
        }

    runtime_ms = round((time.perf_counter() - started) * 1000, 3)
    output = normalize_lines(proc.stdout)
    expected = case.get("expected", [])
    passed = output == expected and proc.returncode == 0

    return {
        "name": test_name,
        "passed": passed,
        "runtime_ms": runtime_ms,
        "expected": expected,
        "output": output,
        "return_code": proc.returncode,
        "stderr": normalize_lines(proc.stderr),
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for item in results if item.get("passed"))
    return {
        "mode": "public",
        "passed": passed,
        "total": total,
        "pass_rate": round((passed / total) * 100, 2) if total else 0.0,
        "benchmark_tier": "strict",
        "metrics": {"runtime": "strict", "memory": "n/a"},
        "failed_tests": [item["name"] for item in results if not item.get("passed")],
        "public_results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run shell challenge tests")
    parser.add_argument(
        "--problem-dir", required=True, help="Path to shell problem folder"
    )
    parser.add_argument(
        "--command", required=True, help="Command template (supports {input_file})"
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=DEFAULT_TIMEOUT_MS,
        help="Per-test timeout in milliseconds",
    )
    args = parser.parse_args()

    problem_dir = Path(args.problem_dir).resolve()
    public_payload = load_json(problem_dir / "tests" / "public.json")

    results = [
        evaluate_case(args.command, problem_dir, case, timeout_ms=args.timeout_ms)
        for case in public_payload.get("tests", [])
    ]
    print(json.dumps(summarize(results), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

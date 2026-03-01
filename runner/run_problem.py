#!/usr/bin/env python3
"""Local challenge runner MVP for Python problems."""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
import tracemalloc
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_solution(solution_path: Path):
    spec = importlib.util.spec_from_file_location("user_solution", solution_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Unable to load solution module from {solution_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate_case(func, case: dict[str, Any]) -> dict[str, Any]:
    test_input = case.get("input", {})
    expected = case.get("expected")

    tracemalloc.start()
    start = time.perf_counter()
    output = func(**test_input)
    elapsed_ms = (time.perf_counter() - start) * 1000
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    passed = output == expected
    return {
        "name": case.get("name", "unnamed"),
        "passed": passed,
        "runtime_ms": round(elapsed_ms, 4),
        "memory_peak_bytes": peak,
        "expected": expected,
        "output": output,
    }


def run_tests(func, payload: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    skipped: list[str] = []
    results: list[dict[str, Any]] = []

    for case in payload.get("tests", []):
        if "expected" not in case:
            skipped.append(case.get("name", "unnamed"))
            continue
        results.append(evaluate_case(func, case))

    return results, skipped


def summarize(mode: str, public_results, hidden_results, skipped_hidden):
    all_results = public_results + hidden_results
    passed = sum(1 for item in all_results if item["passed"])
    total = len(all_results)
    total_runtime = sum(item["runtime_ms"] for item in all_results)
    avg_runtime = total_runtime / total if total else 0.0
    max_runtime = max((item["runtime_ms"] for item in all_results), default=0.0)
    max_memory = max((item["memory_peak_bytes"] for item in all_results), default=0)
    failed = [item["name"] for item in all_results if not item["passed"]]

    return {
        "mode": mode,
        "passed": passed,
        "total": total,
        "pass_rate": round((passed / total) * 100, 2) if total else 0.0,
        "avg_runtime_ms": round(avg_runtime, 4),
        "total_runtime_ms": round(total_runtime, 4),
        "max_runtime_ms": round(max_runtime, 4),
        "max_memory_peak_bytes": max_memory,
        "failed_tests": failed,
        "skipped_hidden_tests": skipped_hidden,
        "public_results": public_results,
        "hidden_results": hidden_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run solution against problem tests")
    parser.add_argument("--problem-dir", required=True, help="Path to problem folder")
    parser.add_argument(
        "--solution", required=True, help="Path to Python solution file"
    )
    parser.add_argument(
        "--public-only",
        action="store_true",
        help="Run only public tests",
    )
    args = parser.parse_args()

    problem_dir = Path(args.problem_dir).resolve()
    solution_path = Path(args.solution).resolve()

    public_payload = load_json(problem_dir / "tests" / "public.json")
    hidden_payload = load_json(problem_dir / "tests" / "hidden.json")

    module = load_solution(solution_path)
    function_name = public_payload.get("function", "solve")
    if not hasattr(module, function_name):
        raise AttributeError(f"Solution missing required function: {function_name}")
    func = getattr(module, function_name)

    public_results, _ = run_tests(func, public_payload)
    hidden_results: list[dict[str, Any]] = []
    skipped_hidden: list[str] = []

    if not args.public_only:
        hidden_results, skipped_hidden = run_tests(func, hidden_payload)

    mode = "public" if args.public_only else "public+hidden"
    print(
        json.dumps(
            summarize(mode, public_results, hidden_results, skipped_hidden), indent=2
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Local challenge runner with timeout and safety guards."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import multiprocessing as mp
import time
import tracemalloc
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT_MS = 800
ALLOWED_IMPORTS = {
    "math",
    "collections",
    "heapq",
    "itertools",
    "functools",
    "bisect",
    "statistics",
    "re",
    "string",
    "operator",
}
BLOCKED_CALLS = {"exec", "eval", "open", "compile", "__import__"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _safe_value(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def sanitize_test_result(payload: dict[str, Any]) -> dict[str, Any]:
    safe = dict(payload)
    for key in ("expected", "output", "error"):
        if key in safe:
            safe[key] = _safe_value(safe[key])
    return safe


def validate_solution_ast(solution_path: Path, allowlist: set[str]) -> list[str]:
    tree = ast.parse(solution_path.read_text(encoding="utf-8"))
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in allowlist:
                    violations.append(f"disallowed import: {alias.name}")
        if isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            root = node.module.split(".", 1)[0]
            if root not in allowlist:
                violations.append(f"disallowed import-from: {node.module}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_CALLS:
                violations.append(f"blocked call used: {node.func.id}")

    return violations


def _execute_case_worker(
    solution_path: str,
    function_name: str,
    test_input: dict[str, Any],
    expected: Any,
    queue: mp.Queue,
) -> None:
    try:
        spec = importlib.util.spec_from_file_location("user_solution", solution_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Unable to load solution module from {solution_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, function_name):
            raise AttributeError(f"Solution missing required function: {function_name}")
        func = getattr(module, function_name)

        tracemalloc.start()
        start = time.perf_counter()
        output = func(**test_input)
        elapsed_ms = (time.perf_counter() - start) * 1000
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        queue.put(
            {
                "ok": True,
                "output": output,
                "expected": expected,
                "runtime_ms": round(elapsed_ms, 4),
                "memory_peak_bytes": peak,
            }
        )
    except Exception as exc:  # noqa: BLE001
        queue.put({"ok": False, "error": f"{type(exc).__name__}: {exc}"})


def evaluate_case(
    solution_path: Path,
    function_name: str,
    case: dict[str, Any],
    timeout_ms: int,
) -> dict[str, Any]:
    test_name = case.get("name", "unnamed")
    test_input = case.get("input", {})
    expected = case.get("expected")

    queue: mp.Queue = mp.get_context("spawn").Queue()
    process = mp.get_context("spawn").Process(
        target=_execute_case_worker,
        args=(str(solution_path), function_name, test_input, expected, queue),
    )
    process.start()
    process.join(timeout_ms / 1000)

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "name": test_name,
            "passed": False,
            "runtime_ms": float(timeout_ms),
            "memory_peak_bytes": 0,
            "expected": expected,
            "output": None,
            "error": f"TimeoutError: exceeded {timeout_ms}ms",
        }

    if queue.empty():
        return {
            "name": test_name,
            "passed": False,
            "runtime_ms": 0.0,
            "memory_peak_bytes": 0,
            "expected": expected,
            "output": None,
            "error": "RuntimeError: worker finished without output",
        }

    worker_result = queue.get_nowait()
    if not worker_result["ok"]:
        return {
            "name": test_name,
            "passed": False,
            "runtime_ms": 0.0,
            "memory_peak_bytes": 0,
            "expected": expected,
            "output": None,
            "error": worker_result["error"],
        }

    output = worker_result["output"]
    return {
        "name": test_name,
        "passed": output == expected,
        "runtime_ms": worker_result["runtime_ms"],
        "memory_peak_bytes": worker_result["memory_peak_bytes"],
        "expected": expected,
        "output": output,
    }


def run_tests(
    solution_path: Path,
    function_name: str,
    payload: dict[str, Any],
    fallback_timeout_ms: int,
) -> tuple[list[dict[str, Any]], list[str], list[int]]:
    skipped: list[str] = []
    results: list[dict[str, Any]] = []
    applied_limits: list[int] = []

    for case in payload.get("tests", []):
        if "expected" not in case:
            skipped.append(case.get("name", "unnamed"))
            continue
        case_timeout = int(case.get("runtime_limit_ms", fallback_timeout_ms))
        applied_limits.append(case_timeout)
        results.append(
            sanitize_test_result(
                evaluate_case(
                    solution_path, function_name, case, timeout_ms=case_timeout
                )
            )
        )

    return results, skipped, applied_limits


def summarize(
    mode: str,
    public_results: list[dict[str, Any]],
    hidden_results: list[dict[str, Any]],
    skipped_hidden: list[str],
    applied_limits: list[int],
) -> dict[str, Any]:
    all_results = public_results + hidden_results
    passed = sum(1 for item in all_results if item["passed"])
    total = len(all_results)
    total_runtime = sum(item["runtime_ms"] for item in all_results)
    avg_runtime = total_runtime / total if total else 0.0
    max_runtime = max((item["runtime_ms"] for item in all_results), default=0.0)
    max_memory = max((item["memory_peak_bytes"] for item in all_results), default=0)
    failed = [item["name"] for item in all_results if not item["passed"]]
    strict = bool(applied_limits) and all(limit > 0 for limit in applied_limits)

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
        "benchmark_tier": "strict" if strict else "advisory",
        "metrics": {
            "runtime": "strict" if strict else "advisory",
            "memory": "advisory",
        },
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
        "--public-only", action="store_true", help="Run only public tests"
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=DEFAULT_TIMEOUT_MS,
        help="Fallback per-test timeout in milliseconds",
    )
    args = parser.parse_args()

    problem_dir = Path(args.problem_dir).resolve()
    solution_path = Path(args.solution).resolve()

    public_payload = load_json(problem_dir / "tests" / "public.json")
    hidden_payload = load_json(problem_dir / "tests" / "hidden.json")

    allowlist = set(public_payload.get("allowed_imports", [])) | ALLOWED_IMPORTS
    violations = validate_solution_ast(solution_path, allowlist)
    if violations:
        print(
            json.dumps(
                {
                    "mode": "validation",
                    "passed": 0,
                    "total": 0,
                    "failed_tests": [],
                    "error": "SecurityValidationError",
                    "violations": violations,
                },
                indent=2,
            )
        )
        return 1

    function_name = public_payload.get("function", "solve")

    public_results, _, public_limits = run_tests(
        solution_path,
        function_name,
        public_payload,
        fallback_timeout_ms=args.timeout_ms,
    )
    hidden_results: list[dict[str, Any]] = []
    hidden_limits: list[int] = []
    skipped_hidden: list[str] = []

    if not args.public_only:
        hidden_results, skipped_hidden, hidden_limits = run_tests(
            solution_path,
            function_name,
            hidden_payload,
            fallback_timeout_ms=args.timeout_ms,
        )

    mode = "public" if args.public_only else "public+hidden"
    print(
        json.dumps(
            summarize(
                mode,
                public_results,
                hidden_results,
                skipped_hidden,
                applied_limits=public_limits + hidden_limits,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

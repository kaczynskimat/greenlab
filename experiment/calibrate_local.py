"""Offline preliminary calibration for Green Lab (16 problems x 3 variants).

Run from repository root:
    PYTHONPATH=. python3 experiment/calibrate_local.py

Uses generator-produced repetition-0 cases *in memory*, never changes workload
files and never connects to gl3. Estimates baseline invocation counts for a
15-second benchmark. Estimates MUST be reviewed/recalibrated on gl3.
"""
import argparse
import copy
import csv
import hashlib
import importlib
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TARGET_SECONDS = 15.0
CASES = 20
SEED_BASE = "greenlab-pilot-v1"
WORKER_TIMEOUT = 12
MAX_ITERATIONS = 10_000_000


def worker(problem_id, variant):
    from experiment.workload_generator import create_workload
    from experiment.validate_workload import is_correct

    metadata = json.loads((ROOT / "metadata.json").read_text())
    entry = next(p for p in metadata["problems"].values()
                 if int(p["leetcode_id"]) == problem_id)
    workload = create_workload(problem_id, variant, 0, CASES, SEED_BASE)
    solution_cls = getattr(importlib.import_module(entry["modules"]["baseline"]),
                           entry["variants"][f"v{variant}"]["class_name"])
    method = entry["method_name"]
    cases = workload["cases"]

    def invoke(case):
        obj = solution_cls()
        args = copy.deepcopy(case["args"])
        return getattr(obj, method)(*args)

    # Validate all cases before timing (mirrors benchmark, no repeated output checks).
    for case in cases:
        actual = invoke(case)
        if not is_correct(problem_id, actual, case["expected"], case["args"]):
            raise ValueError(f"Incorrect baseline result for problem {problem_id}")

    n = 100
    timings = []
    while True:
        start = time.perf_counter()
        for i in range(n):
            invoke(cases[i % len(cases)])
        elapsed = time.perf_counter() - start
        timings.append((n, elapsed))
        if elapsed >= 0.3 or n >= 100_000:
            break
        n = min(100_000, max(n + 1, int(n * min(20, 0.5 / max(elapsed, 1e-6)))))

    # Record the estimate, not a real measured 15s energy run.
    seconds_per_iteration = elapsed / n
    iterations = max(1, min(MAX_ITERATIONS, round(TARGET_SECONDS / seconds_per_iteration)))
    print(json.dumps({
        "problem": problem_id,
        "variant": variant,
        "repetition": 0,
        "seed": workload["seed"],
        "input_sha256": workload["input_sha256"],
        "pilot_iterations": n,
        "pilot_seconds": round(elapsed, 8),
        "estimated_iterations_for_15s": iterations,
        "estimated_seconds_per_iteration": seconds_per_iteration,
        "warning": "CAP_REACHED" if iterations == MAX_ITERATIONS else "",
    }))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--problem", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--variant", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, default=ROOT / "experiment" / "calibration_local.csv")
    args = parser.parse_args()
    if args.worker:
        worker(args.problem, args.variant)
        return

    metadata = json.loads((ROOT / "metadata.json").read_text())
    problems = sorted({int(p["leetcode_id"]) for p in metadata["problems"].values()})
    result_rows = []
    fields = ["problem", "variant", "repetition", "seed", "input_sha256",
              "pilot_iterations", "pilot_seconds", "estimated_iterations_for_15s",
              "estimated_seconds_per_iteration", "warning"]
    for pid in problems:
        for v in (1, 2, 3):
            cmd = [sys.executable, str(Path(__file__).resolve()), "--worker",
                   "--problem", str(pid), "--variant", str(v)]
            try:
                p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                                   timeout=WORKER_TIMEOUT, check=True)
                data = json.loads(p.stdout.strip().splitlines()[-1])
                print(f"#{pid:3} V{v} : {data['pilot_seconds']:.3f}s / "
                      f"{data['pilot_iterations']} calls -> ~{data['estimated_iterations_for_15s']:,} calls")
            except subprocess.TimeoutExpired:
                data = dict.fromkeys(fields, "")
                data.update(problem=pid, variant=v, warning="TIMEOUT (12s worker)")
                print(f"#{pid:3} V{v} : TIMEOUT, investigate workload", flush=True)
            except (subprocess.CalledProcessError, ValueError, IndexError) as e:
                data = dict.fromkeys(fields, "")
                detail = (e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)) or "worker error"
                data.update(problem=pid, variant=v, warning="ERROR: " + detail.strip()[-200:])
                print(f"#{pid:3} V{v} : ERROR {data['warning']}", flush=True)
            result_rows.append(data)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_rows)
    print(f"\nSaved {len(result_rows)} preliminary combinations: {args.output}")
    print("Not final iteration counts: recheck on gl3 and across multiple repetitions.")


if __name__ == "__main__":
    main()

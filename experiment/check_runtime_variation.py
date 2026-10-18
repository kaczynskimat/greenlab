"""Offline workload runtime variation check (not energy calibration).

Run from repository root:
    PYTHONPATH=. python experiment/check_runtime_variation.py

Uses generated pilot inputs IN MEMORY; does not overwrite workload JSON.
Five predetermined repetition seeds per problem/variant, baseline only.
Results: experiment/runtime_variation_local.csv
"""
import argparse
import copy
import csv
import importlib
import json
import statistics
import subprocess
import sys
import time
import signal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
REPETITIONS = (0, 1, 17, 42, 84)
CASES = 20
SEED_BASE = "greenlab-pilot-v1"


def worker(pid, variant, repetition):
    from experiment.workload_generator import create_workload
    from experiment.validate_workload import is_correct

    metadata = json.loads((ROOT / "metadata.json").read_text())
    entry = next(x for x in metadata["problems"].values() if int(x["leetcode_id"]) == pid)
    cls = getattr(importlib.import_module(entry["modules"]["baseline"]),
                  entry["variants"][f"v{variant}"]["class_name"])
    method = entry["method_name"]
    workload = create_workload(pid, variant, repetition, CASES, SEED_BASE)
    cases = workload["cases"]

    def invoke(case):
        return getattr(cls(), method)(*copy.deepcopy(case["args"]))

    def timeout(*_):
        raise TimeoutError("Single case exceeded 1 second")

    signal.signal(signal.SIGALRM, timeout)
    for i, case in enumerate(cases):
        try:
            signal.setitimer(signal.ITIMER_REAL, 1)
            actual = invoke(case)
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        if not is_correct(pid, actual, case["expected"], case["args"]):
            raise ValueError(f"Wrong baseline result on case {i}")

    n = 20
    while True:
        start = time.perf_counter()
        for i in range(n):
            invoke(cases[i % CASES])
        elapsed = time.perf_counter() - start
        if elapsed >= 0.15 or n >= 20000:
            break
        n = min(20000, max(n + 1, int(n * min(10, 0.2 / max(elapsed, 0.000001)))))

    print(json.dumps({"problem": pid, "variant": variant, "repetition": repetition,
                      "seed": workload["seed"], "input_sha256": workload["input_sha256"],
                      "pilot_iterations": n, "pilot_seconds": round(elapsed, 7),
                      "seconds_per_iteration": elapsed / n}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--problem", type=int, help=argparse.SUPPRESS)
    ap.add_argument("--variant", type=int, help=argparse.SUPPRESS)
    ap.add_argument("--repetition", type=int, help=argparse.SUPPRESS)
    ap.add_argument("--output", type=Path, default=ROOT / "experiment" / "runtime_variation_local.csv")
    args = ap.parse_args()
    if args.worker:
        worker(args.problem, args.variant, args.repetition)
        return

    metadata = json.loads((ROOT / "metadata.json").read_text())
    ids = sorted(int(p["leetcode_id"]) for p in metadata["problems"].values())
    fields = ["problem", "variant", "repetition", "seed", "input_sha256", "pilot_iterations",
              "pilot_seconds", "seconds_per_iteration", "relative_to_repetition_0", "warning"]
    rows = []
    for pid in ids:
        for variant in (1, 2, 3):
            block = []
            for rep in REPETITIONS:
                cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", "--problem", str(pid),
                       "--variant", str(variant), "--repetition", str(rep)]
                try:
                    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                                       timeout=8, check=True)
                    row = json.loads(p.stdout.strip().splitlines()[-1])
                    row["warning"] = ""
                except subprocess.TimeoutExpired:
                    row = {"problem": pid, "variant": variant, "repetition": rep,
                           "warning": "WORKER_TIMEOUT_8S"}
                except (subprocess.CalledProcessError, ValueError, IndexError) as exc:
                    detail = exc.stderr if isinstance(exc, subprocess.CalledProcessError) else str(exc)
                    row = {"problem": pid, "variant": variant, "repetition": rep,
                           "warning": "ERROR: " + str(detail).strip()[-160:]}
                block.append(row)
            baseline = block[0].get("seconds_per_iteration")
            ratios = []
            for row in block:
                seconds = row.get("seconds_per_iteration")
                if baseline and seconds:
                    ratio = seconds / baseline
                    row["relative_to_repetition_0"] = round(ratio, 3)
                    ratios.append(ratio)
                    if ratio > 3 or ratio < 1/3:
                        row["warning"] = "HIGH_VARIATION" if not row["warning"] else row["warning"]
                rows.append(row)
            warnings = sum(bool(row.get("warning")) for row in block)
            if ratios:
                print(f"#{pid:3} V{variant}: range {min(ratios):.2f}x–{max(ratios):.2f}x vs r0; "
                      f"{warnings} warning(s)", flush=True)
            else:
                print(f"#{pid:3} V{variant}: no reliable timing; {warnings} warning(s)", flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} pilot records: {args.output}")
    print("CAUTION: These are 5-seed local screening results, NOT final gl3 calibration.")


if __name__ == "__main__":
    main()


import argparse
import csv
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

import psutil


ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--treatment",
        choices=["original", "modified"],
        required=True,
    )
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--problem", type=int, default=322)
    parser.add_argument("--variant", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    if args.iterations < 1:
        parser.error("--iterations must be positive")

    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        parser.error("Invalid run ID")

    output_dir = ROOT / "dryrun-results"
    output_dir.mkdir(exist_ok=True)

    energy_file = output_dir / f"{args.run_id}.csv"
    result_file = output_dir / f"{args.run_id}.json"

    if energy_file.exists() or result_file.exists():
        parser.error(f"Run ID already exists: {args.run_id}")

    command = [
        "energibridge",
        "--interval", "200",
        "--output", str(energy_file),
        "--summary",
        sys.executable,
        str(ROOT / "experiment" / "benchmark.py"),
        "--treatment", args.treatment,
        "--iterations", str(args.iterations),
        "--problem", str(args.problem),
        "--variant", str(args.variant),
    ]

    start = time.perf_counter()

    profiler = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    parent = psutil.Process(profiler.pid)

    rss_samples = []
    cpu_intervals = []
    previous_cpu = None
    previous_time = None

    while profiler.poll() is None:
        try:
            children = parent.children(recursive=True)

            python_children = [
                p for p in children
                if "python" in p.name().lower()
            ]

            if python_children:
                # Our benchmark launches one Python process.
                process = python_children[0]

                rss_samples.append(process.memory_info().rss)

                cpu_times = process.cpu_times()
                cpu_total = cpu_times.user + cpu_times.system
                sample_time = time.perf_counter()

                if previous_cpu is not None:
                    wall_delta = sample_time - previous_time
                    cpu_delta = cpu_total - previous_cpu

                    if wall_delta > 0 and cpu_delta >= 0:
                        cpu_intervals.append(
                            (cpu_delta, wall_delta)
                        )

                previous_cpu = cpu_total
                previous_time = sample_time

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

        time.sleep(0.05)

    stdout, _ = profiler.communicate()
    wrapper_elapsed = time.perf_counter() - start

    print(stdout)

    if profiler.returncode != 0:
        raise RuntimeError(
            f"EnergiBridge failed with exit code "
            f"{profiler.returncode}"
        )

    if "Validation: PASS" not in stdout:
        raise RuntimeError("Benchmark validation failed")

    match = re.search(
        r"^Elapsed time:\s*([0-9.]+)\s*seconds",
        stdout,
        re.MULTILINE,
    )
    if match is None:
        raise RuntimeError("Benchmark runtime not found")

    benchmark_runtime = float(match.group(1))

    with energy_file.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) < 2:
        raise RuntimeError("Insufficient energy samples")

    def energy_difference(column):
        difference = (
            float(rows[-1][column])
            - float(rows[0][column])
        )
        if not math.isfinite(difference) or difference < 0:
            raise RuntimeError(
                f"Invalid energy difference: {column}"
            )
        return difference

    package_energy = energy_difference("PACKAGE_ENERGY (J)")
    dram_energy = energy_difference("DRAM_ENERGY (J)")

    # EnergiBridge Time values are Unix timestamps in ms.
    measurement_duration = (
        float(rows[-1]["Time"])
        - float(rows[0]["Time"])
    ) / 1000.0

    if measurement_duration <= 0:
        raise RuntimeError("Invalid measurement duration")

    # CPU usage as a percentage of one logical CPU.
    # Multithreaded programs could exceed 100%.
    total_cpu_delta = sum(x[0] for x in cpu_intervals)
    total_wall_delta = sum(x[1] for x in cpu_intervals)

    avg_cpu_usage = (
        100.0 * total_cpu_delta / total_wall_delta
        if total_wall_delta > 0 else None
    )

    result = {
        "run_id": args.run_id,
        "problem": args.problem,
        "variant": args.variant,
        "treatment": args.treatment,
        "iterations": args.iterations,

        "package_energy_j": package_energy,
        "dram_energy_j": dram_energy,

        "benchmark_runtime_seconds": benchmark_runtime,
        "measurement_duration_seconds": measurement_duration,
        "average_power_w": (
            package_energy / measurement_duration
        ),

        # Retained for compatibility with our existing RunnerConfig.
        "elapsed_seconds": wrapper_elapsed,

        "avg_cpu_usage_percent": avg_cpu_usage,

        "avg_rss_bytes": (
            sum(rss_samples) / len(rss_samples)
            if rss_samples else None
        ),
        "peak_rss_bytes": (
            max(rss_samples) if rss_samples else None
        ),
        "rss_samples": len(rss_samples),
        "cpu_intervals": len(cpu_intervals),
    }

    result_file.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""External watchdog for the VU Green Lab Experiment Runner.

No modifications to Experiment Runner or EnergiBridge. Linux/POSIX only.
Run --self-test for an isolated test that never starts SSH.
"""
import argparse
import csv
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta


def completed_rows(path):
    try:
        with path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows or "__done" not in rows[0]:
            return None
        return sum(row["__done"] == "DONE" for row in rows), len(rows)
    except (OSError, csv.Error):
        return None


def stop_group(process, grace=8):
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def supervise(command, csv_path, stall_seconds, stop_at, poll_seconds=2, quiet=False):
    start = time.monotonic()
    last_progress_at = start
    last_count = None
    process = subprocess.Popen(command, start_new_session=True)
    if not quiet:
        print(f"Started launcher child PID {process.pid}; monitoring {csv_path}", flush=True)
    try:
        while True:
            now = time.monotonic()
            status = completed_rows(csv_path)
            if status is not None:
                if last_count is None or status[0] > last_count:
                    if not quiet:
                        print(f"Checkpoint: {status[0]}/{status[1]} DONE", flush=True)
                    last_count = status[0]
                    last_progress_at = now
            exitcode = process.poll()
            if exitcode is not None:
                if not quiet:
                    print(f"Experiment Runner exited with code {exitcode}", flush=True)
                if exitcode != 0:
                    return 1
                final_status = completed_rows(csv_path)
                if final_status is None:
                    print("Runner exited without a readable run_table.csv; inspect logs.", flush=True)
                    return 4
                if final_status[0] != final_status[1]:
                    print(f"Runner exited but {final_status[1] - final_status[0]} runs are still pending; investigate before restarting.", flush=True)
                    return 4
                return 0
            if stop_at is not None and datetime.now(stop_at.tzinfo) >= stop_at:
                print("Booking safety stop reached; terminating local process group.", flush=True)
                stop_group(process)
                return 2
            if now - last_progress_at > stall_seconds:
                print(f"No completed run for >{stall_seconds:g}s; terminating local process group.", flush=True)
                stop_group(process)
                return 3
            time.sleep(poll_seconds)
    except KeyboardInterrupt:
        print("Interrupted; stopping local process group.", flush=True)
        stop_group(process)
        return 130
    finally:
        if process.poll() is None:
            stop_group(process)


def self_test():
    with tempfile.TemporaryDirectory(prefix="greenlab_launcher_test_") as temp:
        folder = Path(temp)
        csv_path = folder / "run_table.csv"
        csv_path.write_text("__run_id,__done\nr0,TODO\nr1,TODO\n")
        child = folder / "mock_runner.py"
        child.write_text('''import csv,sys,time
from pathlib import Path
p=Path(sys.argv[1]); mode=sys.argv[2]
if mode=="progress":
    time.sleep(0.15)
    p.write_text("__run_id,__done\\nr0,DONE\\nr1,TODO\\n")
    time.sleep(0.15)
    p.write_text("__run_id,__done\\nr0,DONE\\nr1,DONE\\n")
elif mode=="hang":
    time.sleep(10)
''')
        rc = supervise([sys.executable, str(child), str(csv_path), "progress"], csv_path,
                       stall_seconds=2, stop_at=None, poll_seconds=0.05, quiet=True)
        assert rc == 0 and completed_rows(csv_path) == (2, 2)
        print("PASS: Progress detected and successful subprocess completed")
        rc = supervise([sys.executable, str(child), str(csv_path), "hang"], csv_path,
                       stall_seconds=0.25, stop_at=None, poll_seconds=0.05, quiet=True)
        assert rc == 3
        print("PASS: Hung subprocess terminated by watchdog")
        rc = supervise([sys.executable, str(child), str(csv_path), "hang"], csv_path,
                       stall_seconds=10, stop_at=datetime.now().astimezone() - timedelta(seconds=1),
                       poll_seconds=0.05, quiet=True)
        assert rc == 2
        print("PASS: Expired booking prevents continued execution")
        assert completed_rows(csv_path) == (2, 2)
        print("PASS: Saved CSV retained; no SSH or energy measurements used")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--runner-root", type=Path, default=Path.home() / "VU/GreenLab/experiment-runner")
    p.add_argument("--repo", type=Path, default=Path.home() / "VU/GreenLab/greenlab")
    p.add_argument("--deadline", help="Booking end as ISO datetime including offset, e.g. 2026-10-20T00:00:00+02:00")
    p.add_argument("--safety-minutes", type=float, default=10, help="Hard-stop this many minutes before booking ends")
    p.add_argument("--stall-seconds", type=float, default=600, help="Maximum time without an additional DONE row")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.deadline:
        p.error("--deadline is required for real runs")
    deadline = datetime.fromisoformat(args.deadline)
    if deadline.tzinfo is None or deadline.utcoffset() is None:
        p.error("--deadline must include a timezone offset")
    if args.safety_minutes < 1 or args.stall_seconds < 30:
        p.error("Use safety-minutes >= 1 and stall-seconds >= 30")
    stop_at = deadline - timedelta(minutes=args.safety_minutes)
    if datetime.now(stop_at.tzinfo) >= stop_at:
        p.error("Booking safety cutoff is already in the past")
    runner = args.runner_root.resolve()
    repo = args.repo.resolve()
    config = repo / "experiment" / "RunnerConfig.py"
    runner_script = runner / "experiment-runner"
    calibration = repo / "experiment" / "calibration_gl3.csv"
    if not config.is_file() or not runner_script.is_dir():
        p.error("Runner path or configuration file missing")
    if not calibration.is_file():
        p.error(f"Missing calibration file: {calibration}. Do not use laptop estimates as gl3 calibration.")
    # Name agrees with the current user-configured full experiment. Refuse to guess if changed.
    import ast
    tree = ast.parse(config.read_text())
    experiment_name = None
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "name" and isinstance(node.value, ast.Constant):
            experiment_name = node.value.value
            break
    if not isinstance(experiment_name, str) or not experiment_name:
        p.error("Could not determine the experiment name from RunnerConfig.py")
    csv_path = repo / "experiment" / "experiments" / experiment_name / "run_table.csv"
    python = runner / ".venv" / "bin" / "python"
    if not python.is_file():
        p.error(f"Missing Python interpreter: {python}")
    print(f"Experiment: {experiment_name}")
    print(f"Stop no later than: {stop_at.isoformat()}")
    print("NOTE: Stopping local SSH does not guarantee termination of remote gl3 processes.")
    return supervise([str(python), str(runner_script), str(config)], csv_path,
                     stall_seconds=args.stall_seconds, stop_at=stop_at)


if __name__ == "__main__":
    raise SystemExit(main())

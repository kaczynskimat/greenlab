
from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from pathlib import Path
from typing import Dict, Any, Optional
import json
import re
import shlex
import subprocess
from PairedRunTableModel import PairedRunTableModel
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import csv
import uuid


class RunnerConfig:
    ROOT_DIR = Path(__file__).resolve().parent

    name: str = "greenlab_full_20261019"
    results_output_path: Path = ROOT_DIR / "experiments"
    operation_type: OperationType = OperationType.AUTO
    time_between_runs_in_ms: int = 5000

    SSH_DESTINATION = "gl_thesunenjoyers@gl3"
    SSH_JUMP = "gl_thesunenjoyers@145.108.225.3:42224"
    REMOTE_PROJECT = "/home/gl_thesunenjoyers/greenlab-project"
    REMOTE_PYTHON = "/home/gl_thesunenjoyers/greenlab-venv/bin/python"
    ITERATIONS = 1000000
    CALIBRATION_FILE = ROOT_DIR / "calibration_gl3.csv"

    def __init__(self):
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment),
        ])

        self.run_table_model = None
        self.result = None
        self.remote_process = None
        output.console_log("Green Lab remote configuration loaded")

    def create_run_table_model(self) -> RunTableModel:
        with (self.ROOT_DIR.parent / "metadata.json").open() as f:
            metadata = json.load(f)

        problem_ids = sorted(
            int(entry["leetcode_id"])
            for entry in metadata["problems"].values()
        )

        if len(problem_ids) != 16 or len(set(problem_ids)) != 16:
            raise ValueError(
                f"Expected 16 unique problems, found {len(problem_ids)}"
            )

        problem = FactorModel("problem", problem_ids)
        variant = FactorModel("variant", [1, 2, 3])
        treatment = FactorModel("treatment", ["original", "modified"])

        self.run_table_model = PairedRunTableModel(
            factors=[problem, variant, treatment],
            exclude_combinations=[],
            repetitions=100,
            seed=20261019,
            data_columns=[
                "package_energy_j",
                "dram_energy_j",
                "benchmark_runtime_seconds",
                "measurement_duration_seconds",
                "average_power_w",
                "avg_cpu_usage_percent",
                "avg_rss_bytes",
                "peak_rss_bytes",
                "rss_samples",
                "workload_seed",
                "workload_sha256",
            ],
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        self.calibration = self.load_calibration()
        output.console_log(
            f"Loaded {len(self.calibration)} gl3 iteration counts"
        )

    def before_run(self) -> None:
        booking_end = datetime(
            2026, 10, 19, 12, 0,
            tzinfo=ZoneInfo("Europe/Amsterdam"),
        )
        safety_margin = timedelta(minutes=20)
        cutoff = booking_end - safety_margin

        now = datetime.now(ZoneInfo("Europe/Amsterdam"))

        if now >= cutoff:
            raise SystemExit(
                f"Booking cutoff reached at {now.isoformat()}. "
                "Stopping before the next measurement."
            )

    def start_run(self, context: RunnerContext) -> None:
        self.result = None

    def start_measurement(self, context: RunnerContext) -> None:
        treatment = context.execute_run["treatment"]
        problem = context.execute_run["problem"]
        variant = context.execute_run["variant"]
        iterations = self.calibration[(int(problem), int(variant))]

        run_table_id = str(context.execute_run["__run_id"])

        match = re.search(r"_repetition_(\d+)$", run_table_id)
        if match is None:
            raise ValueError(f"Cannot determine repetition from {run_table_id}")

        repetition = int(match.group(1))

        # Keep the Experiment Runner run ID stable, but give each
        # remote measurement attempt a unique identifier.
        attempt_id = uuid.uuid4().hex[:12]
        run_id = f"{self.name}_{context.run_dir.name}_{attempt_id}"

        if not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
            raise ValueError(f"Invalid run ID: {run_id}")

        remote_command = (
            f"cd {shlex.quote(self.REMOTE_PROJECT)} && "
            f"timeout --signal=TERM --kill-after=5s 115s "
            f"{shlex.quote(self.REMOTE_PYTHON)} "
            f"experiment/measure.py "
            f"--treatment {shlex.quote(str(treatment))} "
            f"--problem {shlex.quote(str(problem))} "
            f"--variant {shlex.quote(str(variant))} "
            f"--repetition {repetition} "
            f"--iterations {iterations} "
            f"--run-id {shlex.quote(run_id)} "
            f"&& printf '\\n__RESULT_JSON__\\n' "
            f"&& cat {shlex.quote('dryrun-results/' + run_id + '.json')}"
        )

        command = [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=15",
            "-J", self.SSH_JUMP,
            self.SSH_DESTINATION,
            remote_command,
        ]

        output.console_log(f"Starting {treatment}: {run_id}")

        self.remote_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def interact(self, context: RunnerContext) -> None:
        try:
            stdout, _ = self.remote_process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            self.remote_process.kill()
            self.remote_process.communicate()
            raise RuntimeError("Remote measurement timed out")

        (context.run_dir / "remote.log").write_text(stdout)

        if self.remote_process.returncode != 0:
            raise RuntimeError(
                f"Remote measurement failed "
                f"(exit {self.remote_process.returncode}). "
                f"See {context.run_dir / 'remote.log'}"
            )

        marker = "__RESULT_JSON__"

        if marker not in stdout:
            raise RuntimeError(
                "Missing result JSON in remote output; "
                "check remote.log"
            )

        self.result = json.loads(stdout.rsplit(marker, 1)[1].strip())

        output.console_log("Remote measurement completed")

    def stop_measurement(self, context: RunnerContext) -> None:
        pass

    def stop_run(self, context: RunnerContext) -> None:
        pass

    def populate_run_data(
        self, context: RunnerContext
    ) -> Optional[Dict[str, Any]]:
        if self.result is None:
            raise RuntimeError("No validated measurement result")

        return {
            "package_energy_j": self.result["package_energy_j"],
            "dram_energy_j": self.result["dram_energy_j"],
            "benchmark_runtime_seconds": self.result["benchmark_runtime_seconds"],
            "measurement_duration_seconds": self.result["measurement_duration_seconds"],
            "average_power_w": self.result["average_power_w"],
            "avg_cpu_usage_percent": self.result["avg_cpu_usage_percent"],
            "avg_rss_bytes": self.result["avg_rss_bytes"],
            "peak_rss_bytes": self.result["peak_rss_bytes"],
            "rss_samples": self.result["rss_samples"],
            "workload_seed": self.result["workload_seed"],
            "workload_sha256": self.result["workload_sha256"],
        }

    def after_experiment(self) -> None:
        pass

    experiment_path: Path = None

    def load_calibration(self):
        path = self.CALIBRATION_FILE

        if not path.is_file():
            raise RuntimeError(
                f"Missing gl3 calibration file: {path}. "
                "Run gl3 calibration before measurements."
            )

        counts = {}

        with path.open(newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames != ["problem", "variant", "iterations"]:
                raise ValueError(
                    "Calibration CSV must have columns: "
                    "problem,variant,iterations"
                )

            for row in reader:
                problem = int(row["problem"])
                variant = int(row["variant"])
                iterations = int(row["iterations"])

                if variant not in (1, 2, 3) or iterations < 1:
                    raise ValueError(f"Invalid calibration row: {row}")

                key = (problem, variant)

                if key in counts:
                    raise ValueError(f"Duplicate calibration: {key}")

                counts[key] = iterations

        with (self.ROOT_DIR.parent / "metadata.json").open() as f:
            metadata = json.load(f)

        expected = {
            (int(problem["leetcode_id"]), variant)
            for problem in metadata["problems"].values()
            for variant in (1, 2, 3)
    }

        missing = expected - counts.keys()
        extra = counts.keys() - expected

        if missing or extra:
            raise ValueError(
                f"Calibration mismatch: missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )

        return counts

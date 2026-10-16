
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


class RunnerConfig:
    ROOT_DIR = Path(__file__).resolve().parent

    name: str = "coin_ssh_smoke_03"
    results_output_path: Path = ROOT_DIR / "experiments"
    operation_type: OperationType = OperationType.AUTO
    time_between_runs_in_ms: int = 1000

    SSH_DESTINATION = "gl_thesunenjoyers@gl3"
    SSH_JUMP = "gl_thesunenjoyers@145.108.225.3:42224"
    REMOTE_PROJECT = "/home/gl_thesunenjoyers/greenlab-project"
    REMOTE_PYTHON = "/home/gl_thesunenjoyers/greenlab-venv/bin/python"
    ITERATIONS = 1000000

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
        problem = FactorModel("problem", [322])
        variant = FactorModel("variant", [1])
        treatment = FactorModel("treatment", ["original", "modified"])

        self.run_table_model = RunTableModel(
            factors=[problem, variant, treatment],
            exclude_combinations=[],
            repetitions=2,
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
            ],
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        pass

    def before_run(self) -> None:
        pass

    def start_run(self, context: RunnerContext) -> None:
        self.result = None

    def start_measurement(self, context: RunnerContext) -> None:
        treatment = context.execute_run["treatment"]
        problem = context.execute_run["problem"]
        variant = context.execute_run["variant"]

        # Include the experiment name to avoid collisions on gl3.
        run_id = f"{self.name}_{context.run_dir.name}"

        if not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
            raise ValueError(f"Invalid run ID: {run_id}")

        remote_command = (
            f"cd {shlex.quote(self.REMOTE_PROJECT)} && "
            f"{shlex.quote(self.REMOTE_PYTHON)} "
            f"experiment/measure.py "
            f"--treatment {shlex.quote(str(treatment))} "
            f"--problem {shlex.quote(str(problem))} "
            f"--variant {shlex.quote(str(variant))} "
            f"--iterations {self.ITERATIONS} "
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
        }

    def after_experiment(self) -> None:
        pass

    experiment_path: Path = None

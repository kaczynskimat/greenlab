"""Offline paired-schedule interruption/recovery test; no SSH or measurement.

Run from the Experiment Runner venv with PYTHONPATH including framework and
GreenLab experiment folder. Uses real run-table, event, and CSV components.
This is a component integration test, not the complete Runner CLI lifecycle.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from RunnerConfig import RunnerConfig
from EventManager.EventSubscriptionController import EventSubscriptionController
from EventManager.Models.RunnerEvents import RunnerEvents
from ProgressManager.Output.CSVOutputManager import CSVOutputManager
from ProgressManager.RunTable.Models.RunProgress import RunProgress


class SimulatedBookingCutoff(SystemExit):
    pass


def assert_pairs(rows):
    assert len(rows) == 9600, f"Expected 9600 experiment rows, got {len(rows)}"
    for i in range(0, len(rows), 2):
        a, b = rows[i:i + 2]
        assert (a["problem"], a["variant"]) == (b["problem"], b["variant"])
        assert {str(a["treatment"]), str(b["treatment"])} == {
            "original", "modified"
        }
        assert a["__run_id"].rsplit("_repetition_", 1)[1] == b["__run_id"].rsplit("_repetition_", 1)[1]


def main():
    config = RunnerConfig()
    generated = config.create_run_table_model().generate_experiment_run_table()
    assert_pairs(generated)

    # Use two complete pairs for the interruption/recovery simulation.
    generated = generated[:4]
    original_ids = [r["__run_id"] for r in generated]
    assert len(set(original_ids)) == 4

    with TemporaryDirectory(prefix="greenlab_offline_resume_") as folder:
        out = Path(folder)
        manager = CSVOutputManager(out)
        manager.write_run_table(deepcopy(generated))
        assert [r["__run_id"] for r in manager.read_run_table()] == original_ids

        completed_ids = []
        def mock_before_run():
            if len(completed_ids) >= 2:
                raise SimulatedBookingCutoff("Simulated cutoff after first pair")

        EventSubscriptionController.subscribe_to_single_event(
            RunnerEvents.BEFORE_RUN, mock_before_run
        )
        try:
            for row in manager.read_run_table():
                if row["__done"] == RunProgress.DONE:
                    continue
                EventSubscriptionController.raise_event(RunnerEvents.BEFORE_RUN)
                row["__done"] = RunProgress.DONE
                manager.update_row_data(row)
                completed_ids.append(row["__run_id"])
        except SimulatedBookingCutoff:
            pass
        else:
            raise AssertionError("Simulated cutoff did not stop execution")

        after_stop = manager.read_run_table()
        assert [r["__run_id"] for r in after_stop] == original_ids
        assert [r["__run_id"] for r in after_stop if r["__done"] == RunProgress.DONE] == original_ids[:2]
        assert [r["__run_id"] for r in after_stop if r["__done"] != RunProgress.DONE] == original_ids[2:]
        print("Saved first pair, stopped before second pair: PASS")

        # Simulate a fresh process: regenerate the same schedule and restore CSV.
        restarted_config = RunnerConfig()
        regenerated = restarted_config.create_run_table_model().generate_experiment_run_table()[:4]
        assert [r["__run_id"] for r in regenerated] == original_ids
        saved = manager.read_run_table()
        by_id = {r["__run_id"]: r for r in regenerated}
        resumed = []
        for old in saved:
            row = by_id[old["__run_id"]]
            assert str(row["problem"]) == str(old["problem"])
            assert str(row["variant"]) == str(old["variant"])
            assert str(row["treatment"]) == str(old["treatment"])
            row["__done"] = old["__done"]
            resumed.append(row)
        assert [r["__run_id"] for r in resumed] == original_ids

        executed_on_restart = []
        for row in resumed:
            if row["__done"] == RunProgress.DONE:
                continue
            row["__done"] = RunProgress.DONE
            manager.update_row_data(row)
            executed_on_restart.append(row["__run_id"])

        assert executed_on_restart == original_ids[2:]
        final = manager.read_run_table()
        assert len(final) == 4 and all(r["__done"] == RunProgress.DONE for r in final)
        assert [r["__run_id"] for r in final] == original_ids
        print("CSV checkpoint and restart: PASS")
        print("Only unfinished runs executed after restart: PASS")
        print("Saved randomized order unchanged: PASS")
        print("No SSH, no gl3, no measurements: PASS")


if __name__ == "__main__":
    main()

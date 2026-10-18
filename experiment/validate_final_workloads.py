
"""Validate every final workload against its matching baseline/guideline pair."""

import copy
import importlib
import json
import signal
import time
from pathlib import Path

from experiment.validate_workload import is_correct

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT_SECONDS = 1.0


def timeout_handler(_signum, _frame):
    raise TimeoutError("Case exceeded validation timeout")


def main():
    metadata = json.loads((ROOT / "metadata.json").read_text())
    signal.signal(signal.SIGALRM, timeout_handler)

    passed = 0
    failures = []
    started = time.monotonic()

    for entry in metadata["problems"].values():
        problem_id = int(entry["leetcode_id"])
        method_name = entry["method_name"]

        for variant in (1, 2, 3):
            class_name = entry["variants"][f"v{variant}"]["class_name"]

            implementations = {
                treatment: getattr(
                    importlib.import_module(module_path), class_name
                )
                for treatment, module_path in entry["modules"].items()
            }

            for repetition in range(100):
                path = (
                    ROOT / "experiment" / "workloads"
                    / f"p{problem_id}_v{variant}_r{repetition}.json"
                )
                workload = json.loads(path.read_text())

                for case_index, case in enumerate(workload["cases"]):
                    for treatment, solution_class in implementations.items():
                        try:
                            inputs = copy.deepcopy(case["args"])
                            signal.setitimer(
                                signal.ITIMER_REAL, TIMEOUT_SECONDS
                            )
                            try:
                                actual = getattr(
                                    solution_class(), method_name
                                )(*inputs)
                            finally:
                                signal.setitimer(signal.ITIMER_REAL, 0)

                            if not is_correct(
                                problem_id,
                                actual,
                                case["expected"],
                                case["args"],
                            ):
                                raise AssertionError(
                                    f"Wrong answer: {actual!r}"
                                )

                            passed += 1

                        except Exception as exc:
                            signal.setitimer(signal.ITIMER_REAL, 0)
                            failures.append(
                                f"#{problem_id} V{variant} R{repetition} "
                                f"case {case_index} {treatment}: "
                                f"{type(exc).__name__}: {exc}"
                            )

        print(
            f"#{problem_id}: completed validation",
            flush=True,
        )

    duration = time.monotonic() - started

    print(f"\nPassed: {passed}/192000")
    print(f"Failures: {len(failures)}")
    print(f"Duration: {duration:.1f} seconds")

    for failure in failures[:30]:
        print("FAIL:", failure)

    if failures:
        raise SystemExit(1)

    print("PASS: All final workloads validated")


if __name__ == "__main__":
    main()

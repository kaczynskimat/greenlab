
import argparse
import copy
import importlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=int, required=True)
    parser.add_argument("--variant", type=int, choices=[1, 2, 3], required=True)
    parser.add_argument("--repetition", type=int, default=0)
    parser.add_argument("--treatment", choices=["original", "modified"], required=True)
    parser.add_argument("--iterations", type=int, default=100)
    args = parser.parse_args()

    if args.iterations < 1:
        parser.error("--iterations must be positive")

    with (ROOT / "metadata.json").open() as f:
        metadata = json.load(f)

    problem = next(
        (
            entry for entry in metadata["problems"].values()
            if entry["leetcode_id"] == args.problem
        ),
        None,
    )
    if problem is None:
        parser.error(f"Unknown problem: {args.problem}")

    variant = problem["variants"][f"v{args.variant}"]
    treatment_key = "baseline" if args.treatment == "original" else "guideline"

    module = importlib.import_module(problem["modules"][treatment_key])
    Solution = getattr(module, variant["class_name"])
    method_name = problem["method_name"]

    workload_path = (
        ROOT / "experiment" / "workloads"
        / f"p{args.problem}_v{args.variant}_r{args.repetition}.json"
    )

    with workload_path.open() as f:
        workload = json.load(f)

    cases = workload["cases"]

    if not cases:
        raise RuntimeError("Workload contains no cases")

    def run_case(case):
        # Fresh instance and input for every invocation.
        solution = Solution()
        case_args = copy.deepcopy(case["args"])
        actual = getattr(solution, method_name)(*case_args)
        expected = case["expected"]

        if args.problem == 442:
            valid = isinstance(actual, list) and sorted(actual) == sorted(expected)
        else:
            valid = actual == expected

        if not valid:
            raise RuntimeError(
                f"Incorrect result: expected {expected}, got {actual}"
            )

    # Warm-up and validation before timing.
    for case in cases:
        run_case(case)

    start = time.perf_counter()

    for index in range(args.iterations):
        case = cases[index % len(cases)]
        run_case(case)

    elapsed = time.perf_counter() - start

    print(f"Problem: {args.problem}")
    print(f"Variant: {args.variant}")
    print(f"Repetition: {args.repetition}")
    print(f"Treatment: {args.treatment}")
    print(f"Iterations: {args.iterations}")
    print(f"Workload seed: {workload['seed']}")
    print(f"Elapsed time: {elapsed:.6f} seconds")
    print("Validation: PASS")


if __name__ == "__main__":
    main()

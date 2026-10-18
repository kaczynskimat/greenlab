"""Offline per-problem validation across both treatments and all 3 variants.

Usage: python experiment/validate_workload.py --problem 15 [--metadata metadata.json]
Requires metadata in the established 'problems' object schema.
"""
import argparse
import copy
import hashlib
import importlib
import json
import signal
from collections import Counter
from pathlib import Path


def canonical_groups(groups):
    return sorted(tuple(sorted(group)) for group in groups)


def canonical_triples(triples):
    return sorted(set(tuple(sorted(triple)) for triple in triples))


def is_correct(problem_id, actual, expected, args):
    if problem_id == 15:
        return isinstance(actual, list) and canonical_triples(actual) == canonical_triples(expected) and len(actual) == len(canonical_triples(actual))
    if problem_id == 49:
        return isinstance(actual, list) and canonical_groups(actual) == canonical_groups(expected)
    if problem_id == 442:
        return isinstance(actual, list) and sorted(actual) == sorted(expected)
    if problem_id == 905:
        # Output is valid if it is a permutation with all evens before odds.
        return (isinstance(actual, list) and Counter(actual) == Counter(args[0])
                and all(a % 2 <= b % 2 for a, b in zip(actual, actual[1:])))
    return actual == expected


def alarm_handler(_signum, _frame):
    raise TimeoutError('Solution exceeded the per-case timeout')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem', type=int, required=True)
    parser.add_argument('--variant', type=int, choices=[1, 2, 3], default=1)
    parser.add_argument('--repetition', type=int, default=0)
    parser.add_argument('--metadata', type=Path, default=Path('metadata.json'))
    parser.add_argument('--timeout', type=float, default=2.0)
    args = parser.parse_args()

    metadata = json.loads(args.metadata.read_text())

    problem = next(
        (
            entry
            for entry in metadata["problems"].values()
            if int(entry["leetcode_id"]) == args.problem
        ),
        None,
    )

    # Temporary fallback while the team merges metadata.json.
    if problem is None:
        for filename in (
            "metadata_Catarina.json",
            "metadata_Nikola.json",
            "metadata_mateusz.json",
        ):
            path = Path(filename)
            if not path.exists():
                continue

            other_metadata = json.loads(path.read_text())
            problem = next(
                (
                    entry
                    for entry in other_metadata.get("problems", {}).values()
                    if int(entry["leetcode_id"]) == args.problem
                ),
                None,
            )
            if problem is not None:
                break

    if problem is None:
        raise ValueError(f"Problem #{args.problem} not found in metadata")

    workload_path = (
        Path("experiment/workloads")
        / f"p{args.problem}_v{args.variant}_r{args.repetition}.json"
    )
    workload = json.loads(workload_path.read_text())
    cases = workload["cases"]

    data_bytes = json.dumps(
        cases, sort_keys=True, separators=(",", ":")
    ).encode()

    assert hashlib.sha256(data_bytes).hexdigest() == workload["input_sha256"], (
        "Workload checksum mismatch"
    )
    assert (
        workload["problem"],
        workload["variant"],
        workload["repetition"],
    ) == (args.problem, args.variant, args.repetition)


    passed, failures = 0, []
    signal.signal(signal.SIGALRM, alarm_handler)
    for treatment, module_path in problem['modules'].items():
        module = importlib.import_module(module_path)
        for variant_name, variant in problem['variants'].items():
            solution_cls = getattr(module, variant['class_name'])
            for index, case in enumerate(cases):
                inputs = copy.deepcopy(case['args'])
                try:
                    signal.setitimer(signal.ITIMER_REAL, args.timeout)
                    try:
                        actual = getattr(solution_cls(), problem['method_name'])(*inputs)
                    finally:
                        signal.setitimer(signal.ITIMER_REAL, 0)
                    if is_correct(args.problem, actual, case['expected'], case['args']):
                        passed += 1
                    else:
                        failures.append(f'{treatment} {variant_name} case {index}: wrong answer: {actual!r}')
                except Exception as exc:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    failures.append(f'{treatment} {variant_name} case {index}: {type(exc).__name__}: {exc}')

    total = len(cases) * 6
    print(f'Passed: {passed}/{total}')
    print(f'Failed: {len(failures)}')
    for failure in failures[:20]:
        print('FAIL:', failure)
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

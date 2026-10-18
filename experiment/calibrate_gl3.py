"""Calibrate fixed per-(problem, variant) invocation counts on gl3.

Run from the project root using the same Python interpreter as benchmark.py:
    python experiment/calibrate_gl3.py --check-only
    python experiment/calibrate_gl3.py

Uses only frozen experiment/workloads/ JSON files. No EnergiBridge, SSH,
Experiment Runner or final energy measurements are started by this script.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
REPETITIONS = (0, 1, 17, 42, 84)
DETAIL_FIELDS = (
    'problem', 'variant', 'repetition', 'seed', 'input_sha256',
    'pilot_iterations', 'pilot_seconds', 'seconds_per_iteration',
    'projected_seconds_at_selected_iterations', 'status',
)
ITER_FIELDS = ('problem', 'variant', 'iterations')
RUNTIME_RE = re.compile(r'^Elapsed time:\s*([0-9.]+)\s*seconds\s*$', re.M)


def workload_info(problem, variant, repetition):
    path = ROOT / 'experiment' / 'workloads' / f'p{problem}_v{variant}_r{repetition}.json'
    payload = json.loads(path.read_text())
    if (payload['problem'], payload['variant'], payload['repetition']) != (problem, variant, repetition):
        raise ValueError(f'Identifiers mismatch: {path}')
    cases = payload['cases']
    if not cases:
        raise ValueError(f'No workload cases: {path}')
    actual = hashlib.sha256(json.dumps(cases, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if actual != payload['input_sha256']:
        raise ValueError(f'Checksum mismatch: {path}')
    return payload


def pilot(problem, variant, repetition, target_pilot, timeout, max_calls):
    n = 100
    while True:
        cmd = [sys.executable, str(ROOT / 'experiment' / 'benchmark.py'),
               '--problem', str(problem), '--variant', str(variant),
               '--repetition', str(repetition), '--treatment', 'original',
               '--iterations', str(n)]
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True,
                                timeout=timeout, check=True)
        if 'Validation: PASS' not in result.stdout:
            raise ValueError('Benchmark did not validate successfully')
        match = RUNTIME_RE.search(result.stdout)
        if not match:
            raise ValueError('Benchmark elapsed time missing')
        elapsed = float(match.group(1))
        if elapsed <= 0 or not math.isfinite(elapsed):
            raise ValueError('Nonpositive or invalid benchmark time')
        if elapsed >= target_pilot or n >= max_calls:
            return n, elapsed
        multiplier = min(15.0, max(1.5, target_pilot / elapsed))
        next_n = min(max_calls, max(n + 1, int(n * multiplier)))
        n = next_n


def write_csv_atomic(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', newline='', encoding='utf-8',
                                     dir=path.parent, prefix=path.name + '.',
                                     suffix='.tmp', delete=False) as f:
        temp = Path(f.name)
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check-only', action='store_true', help='Validate required inputs without calibration')
    p.add_argument('--target-seconds', type=float, default=15.0)
    p.add_argument('--pilot-seconds', type=float, default=0.3)
    p.add_argument('--per-pilot-timeout', type=float, default=12.0)
    p.add_argument('--max-pilot-calls', type=int, default=100_000)
    p.add_argument('--max-final-iterations', type=int, default=10_000_000)
    p.add_argument('--output', type=Path, default=ROOT / 'experiment' / 'calibration_gl3.csv')
    p.add_argument('--details', type=Path, default=ROOT / 'experiment' / 'calibration_gl3_details.csv')
    args = p.parse_args()
    metadata = json.loads((ROOT / 'metadata.json').read_text())
    problems = sorted(int(x['leetcode_id']) for x in metadata['problems'].values())
    if len(problems) != 16 or len(set(problems)) != 16:
        p.error('Expected exactly 16 unique problems')
    if args.target_seconds <= 0 or args.pilot_seconds <= 0 or args.per_pilot_timeout <= 0:
        p.error('Durations must be positive')
    if args.max_pilot_calls < 100 or args.max_final_iterations < 1:
        p.error('Invalid iteration limits')
    # Catch missing/broken workloads before measuring anything.
    for problem in problems:
        for variant in (1, 2, 3):
            for repetition in REPETITIONS:
                workload_info(problem, variant, repetition)
    print('PASS: 240 frozen calibration workloads verified', flush=True)
    if args.check_only:
        print('CHECK ONLY: No calibration CSV written; no benchmarks started')
        return

    iterations = []
    detail_rows = []
    failed = False
    for problem in problems:
        for variant in (1, 2, 3):
            samples = []
            for repetition in REPETITIONS:
                payload = workload_info(problem, variant, repetition)
                row = {
                    'problem': problem, 'variant': variant, 'repetition': repetition,
                    'seed': payload['seed'], 'input_sha256': payload['input_sha256'],
                    'pilot_iterations': '', 'pilot_seconds': '',
                    'seconds_per_iteration': '',
                    'projected_seconds_at_selected_iterations': '', 'status': 'OK',
                }
                try:
                    calls, seconds = pilot(problem, variant, repetition,
                                           args.pilot_seconds, args.per_pilot_timeout,
                                           args.max_pilot_calls)
                    rate = seconds / calls
                    row.update(pilot_iterations=calls, pilot_seconds=f'{seconds:.6f}',
                               seconds_per_iteration=f'{rate:.12g}')
                    samples.append((rate, row))
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError,
                        ValueError, OSError) as error:
                    row['status'] = f'ERROR: {type(error).__name__}: {str(error)[-150:]}'
                    failed = True
                detail_rows.append(row)
            if len(samples) != len(REPETITIONS):
                print(f'#{problem} V{variant}: ERROR (incomplete pilots)', flush=True)
                continue
            median_rate = median(rate for rate, _ in samples)
            estimated = max(1, round(args.target_seconds / median_rate))
            if estimated > args.max_final_iterations:
                print(f'#{problem} V{variant}: ERROR (requires {estimated} > max iterations)', flush=True)
                failed = True
                continue
            iterations.append({'problem': problem, 'variant': variant, 'iterations': estimated})
            projections = []
            for rate, row in samples:
                projected = rate * estimated
                row['projected_seconds_at_selected_iterations'] = f'{projected:.3f}'
                projections.append(projected)
            print(f'#{problem:3} V{variant}: {estimated:>9,} calls | '
                  f'projected baseline {min(projections):.1f}–{max(projections):.1f}s '
                  f'(median ~{median(projections):.1f}s)', flush=True)

    # Save diagnostics even if calibration cannot be accepted.
    write_csv_atomic(args.details, DETAIL_FIELDS, detail_rows)
    if failed or len(iterations) != 48:
        print(f'FAILED: Detailed pilots saved to {args.details}. '
              f'Final calibration NOT written. Fix issues before proceeding.', file=sys.stderr)
        return 1
    if args.output.exists():
        print(f'FAILED: {args.output} already exists; refusing to overwrite frozen calibration. '
              'Move/archive it explicitly if recalibrating.', file=sys.stderr)
        return 1
    write_csv_atomic(args.output, ITER_FIELDS, iterations)
    print(f'PASS: Saved 48 iteration counts to {args.output}')
    print(f'Pilot evidence saved to {args.details}')
    print('Review projected ranges and confirm full-length pilots on gl3 before final measurements.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

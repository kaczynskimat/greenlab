"""Offline Green Lab readiness audit. Run from your repository root.

Usage: python experiment/check_readiness.py
No SSH, measurements, installs or modifications are made.
"""
import ast
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'metadata.json'
PROBLEMS = ROOT / 'problems'
WORKLOADS = ROOT / 'experiment' / 'workloads'
GENERATOR = ROOT / 'experiment' / 'workload_generator.py'
RUNNER = ROOT / 'experiment' / 'RunnerConfig.py'
BENCHMARK = ROOT / 'experiment' / 'benchmark.py'


def file_for_module(module_name):
    return ROOT.joinpath(*module_name.split('.')).with_suffix('.py')


def classes_in_file(path):
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def methods_in_class(node):
    return {item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}


def main():
    errors, warnings = [], []
    print('GREEN LAB OFFLINE READINESS CHECK')
    print('Repository:', ROOT)
    try:
        data = json.loads(META.read_text(encoding='utf-8'))
        problems = data['problems']
        if not isinstance(problems, dict) or not problems:
            raise ValueError('problems must be a nonempty object')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('BLOCKER: metadata.json missing/invalid:', exc)
        return 1

    seen_ids = set()
    for key, entry in sorted(problems.items()):
        leetcode_id = entry.get('leetcode_id')
        if leetcode_id in seen_ids:
            errors.append(f'{key}: duplicate leetcode_id {leetcode_id}')
        seen_ids.add(leetcode_id)
        variants = entry.get('variants', {})
        modules = entry.get('modules', {})
        method = entry.get('method_name')
        if set(variants) != {'v1', 'v2', 'v3'}:
            errors.append(f'{key}: expected variants v1,v2,v3; got {list(variants)}')
        for treatment in ('baseline', 'guideline'):
            module_path = modules.get(treatment)
            if not module_path:
                errors.append(f'{key}: missing {treatment} module')
                continue
            path = file_for_module(module_path)
            if not path.is_file():
                errors.append(f'{key}: missing {treatment} file {path.relative_to(ROOT)}')
                continue
            try:
                found = classes_in_file(path)
            except SyntaxError as exc:
                errors.append(f'{key}: syntax error in {path.relative_to(ROOT)}: {exc}')
                continue
            for variant, descriptor in variants.items():
                classname = descriptor.get('class_name')
                cls = found.get(classname)
                if cls is None:
                    errors.append(f'{key} {treatment} {variant}: missing class {classname}')
                elif method not in methods_in_class(cls):
                    errors.append(f'{key} {treatment} {variant}: missing method {method}')
        for variant in variants:
            path = WORKLOADS / f'p{leetcode_id}_{variant}_r0.json'
            if not path.exists():
                warnings.append(f'{key} {variant}: no repetition-0 workload yet')
            else:
                try:
                    payload = json.loads(path.read_text(encoding='utf-8'))
                    if (payload.get('problem'), payload.get('variant'), payload.get('repetition')) != (leetcode_id, int(variant[1:]), 0):
                        errors.append(f'{path.name}: workload identifiers do not match filename')
                except (ValueError, OSError):
                    errors.append(f'{path.name}: invalid workload JSON')
        print(f'  {key}: #{leetcode_id}, {len(variants)} variants')

    for label, path in [('Runner', RUNNER), ('Benchmark', BENCHMARK), ('Generator', GENERATOR)]:
        if not path.exists():
            errors.append(f'Missing {label} file {path}')
    if BENCHMARK.exists() and 'metadata_Nikola.json' in BENCHMARK.read_text():
        warnings.append('benchmark.py still reads metadata_Nikola.json, not metadata.json')
    if RUNNER.exists() and 'repetitions=2' in RUNNER.read_text().replace(' ', ''):
        warnings.append('RunnerConfig.py still uses 2 pilot repetitions')
    if RUNNER.exists() and '"--repetition"' not in RUNNER.read_text():
        warnings.append('RunnerConfig.py does not forward --repetition to measure.py')

    print(f'\nProblems in canonical metadata: {len(problems)}')
    print(f'Planned runs at 100 repetitions: {len(problems) * 3 * 2 * 100:,} (assuming 3 variants each)')
    print(f'Blockers: {len(errors)} | Preparations still needed: {len(warnings)}')
    for item in errors:
        print('BLOCKER:', item)
    for item in warnings[:30]:
        print('TODO:', item)
    if len(warnings) > 30:
        print(f'... and {len(warnings)-30} more TODOs')
    print('No gl3 access was used.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())

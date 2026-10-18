"""Deterministic, saved paired workloads for Green Lab experiments.

Generate before measuring; original and modified read the SAME dataset.
Example: python experiment/workload_generator.py --problem 15 --variant 1 --repetition 0
"""
import argparse
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

SUPPORTED = (3, 15, 49, 238, 240, 322, 383, 387, 442, 509, 605, 905, 977)


def coin_change_expected(coins, target):
    dp = [target + 1] * (target + 1)
    dp[0] = 0
    for amount in range(1, target + 1):
        dp[amount] = min((dp[amount - c] + 1 for c in coins if c <= amount), default=target + 1)
    return -1 if dp[target] > target else dp[target]


def fibonacci_expected(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def longest_substring_expected(s):
    return max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1)
                if len(set(s[i:j])) == j - i), default=0)


def three_sum_expected(nums):
    return [list(t) for t in sorted({tuple(sorted((nums[i], nums[j], nums[k])))
           for i in range(len(nums)) for j in range(i + 1, len(nums))
           for k in range(j + 1, len(nums)) if nums[i] + nums[j] + nums[k] == 0})]


def group_anagrams_expected(words):
    groups = {}
    for word in words:
        groups.setdefault(''.join(sorted(word)), []).append(word)
    return list(groups.values())


def product_except_self_expected(nums):
    return [__import__('math').prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]


def search_matrix_expected(matrix, target):
    return any(target in row for row in matrix)


def ransom_note_expected(note, magazine):
    return not (Counter(note) - Counter(magazine))


def first_unique_expected(s):
    counts = Counter(s)
    return next((i for i, ch in enumerate(s) if counts[ch] == 1), -1)


def flowers_expected(flowerbed, n):
    bed = flowerbed[:]
    count = 0
    for i, x in enumerate(bed):
        if x == 0 and (i == 0 or bed[i - 1] == 0) and (i == len(bed) - 1 or bed[i + 1] == 0):
            bed[i] = 1
            count += 1
    return count >= n


def make_case(problem, rng):
    if problem == 3:
        s = ''.join(rng.choices('abcde01234', k=rng.randint(0, 35)))
        return {'args': [s], 'expected': longest_substring_expected(s)}
    if problem == 15:
        nums = [rng.randint(-12, 12) for _ in range(rng.randint(3, 14))]
        return {'args': [nums], 'expected': three_sum_expected(nums)}
    if problem == 49:
        words = []
        for _ in range(rng.randint(2, 6)):
            root = ''.join(rng.choices('abcde', k=rng.randint(1, 6)))
            for _ in range(rng.randint(1, 4)):
                letters = list(root)
                rng.shuffle(letters)
                words.append(''.join(letters))
        rng.shuffle(words)
        return {'args': [words], 'expected': group_anagrams_expected(words)}
    if problem == 238:
        nums = [rng.randint(-4, 4) for _ in range(rng.randint(2, 12))]
        return {'args': [nums], 'expected': product_except_self_expected(nums)}
    if problem == 240:
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        # Globally sorted values satisfy both row and column nondecreasing constraints.
        values = sorted(rng.sample(range(-150, 151), rows * cols))
        matrix = [values[i * cols:(i + 1) * cols] for i in range(rows)]
        target = rng.choice(values) if rng.random() < 0.5 else rng.randint(-160, 160)
        return {'args': [matrix, target], 'expected': search_matrix_expected(matrix, target)}
    if problem == 322:
        # Limited size to protect exponential recursive baselines; calibrate before final freeze.
        coins = sorted(rng.sample(range(1, 13), rng.randint(2, 4)))
        target = rng.randint(0, 22)
        return {'args': [coins, target], 'expected': coin_change_expected(coins, target)}
    if problem == 383:
        magazine = ''.join(rng.choices('abcde', k=rng.randint(1, 45)))
        note = ''.join(rng.choices('abcde', k=rng.randint(1, 25)))
        return {'args': [note, magazine], 'expected': ransom_note_expected(note, magazine)}
    if problem == 387:
        s = ''.join(rng.choices('abcdef', k=rng.randint(1, 55)))
        return {'args': [s], 'expected': first_unique_expected(s)}
    if problem == 442:
        n = rng.randint(8, 35)
        d = rng.randint(1, min(5, n // 2))
        duplicates = rng.sample(range(1, n + 1), d)
        singles = rng.sample([x for x in range(1, n + 1) if x not in duplicates], n - 2 * d)
        nums = singles + duplicates + duplicates
        rng.shuffle(nums)
        return {'args': [nums], 'expected': sorted(duplicates)}
    if problem == 509:
        n = rng.randint(0, 20)
        return {'args': [n], 'expected': fibonacci_expected(n)}
    if problem == 605:
        bed = []
        for _ in range(rng.randint(1, 30)):
            bed.append(1 if (not bed or bed[-1] == 0) and rng.random() < 0.3 else 0)
        n = rng.randint(0, len(bed) // 2 + 1)
        return {'args': [bed, n], 'expected': flowers_expected(bed, n)}
    if problem == 905:
        nums = [rng.randint(0, 100) for _ in range(rng.randint(1, 40))]
        # Reference output only; valid algorithms may return different parity partitions.
        expected = [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2]
        return {'args': [nums], 'expected': expected}
    if problem == 977:
        nums = sorted(rng.randint(-100, 100) for _ in range(rng.randint(1, 45)))
        return {'args': [nums], 'expected': sorted(x * x for x in nums)}
    raise ValueError(f'Unsupported problem: {problem}')


def create_workload(problem, variant, repetition, cases, seed_base):
    if problem not in SUPPORTED or variant not in (1, 2, 3) or repetition < 0 or cases < 1:
        raise ValueError('Invalid problem/variant/repetition/cases')
    seed_material = f'{seed_base}:p{problem}:v{variant}:r{repetition}'
    seed = int.from_bytes(hashlib.sha256(seed_material.encode()).digest()[:8], 'big')
    rng = random.Random(seed)
    inputs = [make_case(problem, rng) for _ in range(cases)]
    case_bytes = json.dumps(inputs, sort_keys=True, separators=(',', ':')).encode()
    return {
        'problem': problem, 'variant': variant, 'repetition': repetition,
        'seed': seed, 'seed_base': seed_base, 'generator_version': 2,
        'case_count': cases, 'input_sha256': hashlib.sha256(case_bytes).hexdigest(),
        'cases': inputs,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem', type=int, choices=SUPPORTED, required=True)
    parser.add_argument('--variant', type=int, choices=[1, 2, 3], required=True)
    parser.add_argument('--repetition', type=int, required=True)
    parser.add_argument('--cases', type=int, default=20)
    parser.add_argument('--seed-base', default='greenlab-pilot-v2')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = create_workload(args.problem, args.variant, args.repetition, args.cases, args.seed_base)
    path = args.output or Path('experiment/workloads') / f'p{args.problem}_v{args.variant}_r{args.repetition}.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(data, indent=2) + '\n'
    if path.exists() and path.read_text() != serialized:
        parser.error(f'Refusing to overwrite different workload: {path}')
    path.write_text(serialized)
    print(f'Saved: {path} | cases={args.cases} | seed={data["seed"]} | sha256={data["input_sha256"][:16]}...')


if __name__ == '__main__':
    main()
